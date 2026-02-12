from typing import Any, Mapping

import orjson
from django.conf import settings
from django.http import HttpRequest
from ninja import NinjaAPI, Swagger
from ninja.errors import ValidationError, HttpError
from ninja.renderers import JSONRenderer, BaseRenderer
from django_starter_core.apis import router
from apps.account.apis import router as account_router
from apps.billing.apis import router as billing_router
from apps.demo.apis import router as demo_router
from apps.health.apis import router as health_router
import logging


class ORJSONRenderer(JSONRenderer):
    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        ret = {
            'code': response_status,
            'data': data,
            'success': False
        }

        if isinstance(data, dict):
            ret['message'] = data.pop('detail', '请求成功')

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

api.add_router('django-starter', router)
api.add_router('health', health_router)
api.add_router('account', account_router)
api.add_router('billing', billing_router)
api.add_router('demo', demo_router)
