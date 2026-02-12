from typing import Any, Mapping

import orjson
import os
import logging
from django.conf import settings
from django.http import HttpRequest
from ninja import NinjaAPI, Swagger
from ninja.errors import ValidationError, HttpError
from ninja.renderers import JSONRenderer, BaseRenderer
from django_starter_core.apis import router
from apps.health.apis import router as health_router


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


class ORJSONRenderer(JSONRenderer):
    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        ret = {
            'code': response_status,
            'data': data,
            'success': False
        }

        message = None
        if isinstance(data, dict):
            message = data.get('detail')
            ret['data'] = {k: v for k, v in data.items() if k != 'detail'}

        if message is None:
            message = '请求成功' if 200 <= response_status < 300 else '请求失败'

        ret['message'] = message

        if 200 <= response_status < 300:
            ret['success'] = True

        return orjson.dumps(ret, **self.json_dumps_params)


api = NinjaAPI(
    title=f'{settings.DJANGO_STARTER["project_info"]["name"]} APIs',
    description=settings.DJANGO_STARTER["project_info"]["description"],
    renderer=ORJSONRenderer(),
    urls_namespace='api',
    docs=Swagger(settings={"persistAuthorization": True}) if getattr(settings, "NINJA_DOCS_ENABLED", False) else None
)

logger = logging.getLogger("django.request")


@api.exception_handler(ValidationError)
def _handle_validation_error(request: HttpRequest, exc: ValidationError):
    return api.create_response(
        request,
        {
            "detail": "参数校验失败",
            "error_code": "VALIDATION_ERROR",
            "errors": exc.errors,
        },
        status=422,
    )


@api.exception_handler(HttpError)
def _handle_http_error(request: HttpRequest, exc: HttpError):
    return api.create_response(
        request,
        {
            "detail": str(exc),
            "error_code": "HTTP_ERROR",
        },
        status=exc.status_code,
    )


@api.exception_handler(Exception)
def _handle_unhandled_error(request: HttpRequest, exc: Exception):
    logger.exception("Unhandled exception", exc_info=exc)
    return api.create_response(
        request,
        {
            "detail": "服务器内部错误",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
        status=500,
    )

_core_prefix = os.environ.get("DJANGO_STARTER_API_PREFIX", "django-starter").strip().strip("/")
if not _core_prefix:
    _core_prefix = "django-starter"

api.add_router(_core_prefix, router)
api.add_router('health', health_router)

if _env_bool("DJANGO_STARTER_ENABLE_ACCOUNT_API", True):
    from apps.account.apis import router as account_router
    api.add_router('account', account_router)

if _env_bool("DJANGO_STARTER_ENABLE_BILLING_API", True):
    from apps.billing.apis import router as billing_router
    api.add_router('billing', billing_router)

if _env_bool("DJANGO_STARTER_ENABLE_DEMO_API", True):
    from apps.demo.apis import router as demo_router
    api.add_router('demo', demo_router)

if _env_bool("DJANGO_STARTER_ENABLE_INTEGRATIONS_API", True):
    from apps.integrations.apis import router as integrations_router
    api.add_router('integrations', integrations_router)
