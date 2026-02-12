import time

from django_starter_core.contrib.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY


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
        endpoint = endpoint or request.path_info.rstrip('/').lstrip('/') or 'root'

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

