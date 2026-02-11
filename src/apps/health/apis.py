from ninja import Router, Schema

from django_starter_core.http.response import responses


router = Router(tags=["health"])


class HealthOut(Schema):
    detail: str
    status: str


@router.get("/ping", response=HealthOut, url_name="health/ping")
def ping(request):
    # 统一响应结构：所有成功响应至少包含 detail 字段
    return responses.ok("ok", {"status": "ok"})
