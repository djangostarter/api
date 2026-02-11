"""
API v1 入口文件。

约定：
- 所有对外 API 都挂载在 /api/v1/ 下
- 使用 Django-Ninja 提供 OpenAPI 文档与类型校验
"""

from ninja import NinjaAPI
from ninja.errors import HttpError

from apps.authentication.apis import router as auth_router
from apps.health.apis import router as health_router
from apps.demo_crud.apis import router as demo_crud_router

# 注意：这里的 version 是 OpenAPI /docs 里显示的版本号，不是 URL 前缀版本号。
api_v1 = NinjaAPI(title="DjangoStarter API", version="1.0")


@api_v1.exception_handler(HttpError)
def http_error_handler(request, exc):
    return api_v1.create_response(
        request,
        {"detail": exc.message},
        status=exc.status_code,
    )


@api_v1.exception_handler(Exception)
def server_error_handler(request, exc):
    return api_v1.create_response(
        request,
        {"detail": "Internal Server Error", "error": str(exc)},
        status=500,
    )


# 路由分组：/api/v1/health/...
api_v1.add_router("/health", health_router)

# 路由分组：/api/v1/auth/...
api_v1.add_router("/auth", auth_router)

# 路由分组：/api/v1/demo-crud/...
api_v1.add_router("/demo-crud", demo_crud_router)
