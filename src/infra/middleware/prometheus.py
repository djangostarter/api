import time

from django_starter_core.contrib.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY
import re


_SEGMENT_INT_RE = re.compile(r"^\d+$")
_SEGMENT_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_SEGMENT_HEX32_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def _normalize_endpoint(path: str) -> str:
    path = (path or "").strip()
    path = path.split("?", 1)[0].split("#", 1)[0]
    path = path.strip("/")
    if not path:
        return "root"

    normalized_parts: list[str] = []
    for seg in path.split("/"):
        if _SEGMENT_INT_RE.match(seg):
            normalized_parts.append(":id")
        elif _SEGMENT_UUID_RE.match(seg):
            normalized_parts.append(":uuid")
        elif _SEGMENT_HEX32_RE.match(seg):
            normalized_parts.append(":hex")
        else:
            normalized_parts.append(seg)
    return "/".join(normalized_parts)


class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        match = getattr(request, "resolver_match", None)
        endpoint = None
        if match is not None:
            endpoint = getattr(match, "view_name", None) or getattr(match, "route", None)
        endpoint = _normalize_endpoint(endpoint or request.path_info)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        return response
