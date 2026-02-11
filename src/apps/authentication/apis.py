"""
JWT 鉴权骨架（Headless 版）。

提供：
- POST /api/v1/auth/token  ：用户名密码换取 JWT
- GET  /api/v1/auth/me     ：获取当前用户（示例：受保护接口）

说明：
- 这里复用了 django-starter-core 中的 JWT 生成/解析逻辑与 Bearer 鉴权实现（Python import 命名空间仍为 kunai）
- 核心库内部读取 settings.DJANGO_STARTER['auth']['jwt']，因此 django-starter-api settings 中需要提供同结构配置
"""

from django.contrib.auth import authenticate
from ninja import Router

from django_starter_core.contrib.auth.bearers import JwtBearer
from django_starter_core.contrib.auth.services import generate_token, get_user
from django_starter_core.http.response import responses

from .schemas import ErrorOut, MeOut, TokenIn, TokenOut


router = Router(tags=["auth"])


@router.post("/token", response={200: TokenOut, 401: ErrorOut}, url_name="auth/token")
def issue_token(request, payload: TokenIn):
    """
    使用 Django 内置认证系统校验用户名与密码，成功后签发 JWT。

    注意：
    - 这是一个骨架实现，适用于内部系统或 PoC
    - 若要更安全，可增加验证码/限流/登录审计等（可在 Kunai 生态内扩展）
    """

    user = authenticate(request, username=payload.username, password=payload.password)
    if not user:
        return responses.unauthorized("用户名或密码错误")

    token = generate_token(
        payload={
            "user_id": user.id,
            "username": user.get_username(),
        }
    )
    return responses.ok("ok", {"token": token.token, "exp": token.exp})


@router.get("/me", auth=JwtBearer(), response={200: MeOut, 401: ErrorOut}, url_name="auth/me")
def me(request):
    """
    受保护的示例接口：返回当前用户信息。

    说明：
    - JwtBearer 负责校验 Token 是否有效（解码成功视为通过）
    - get_user 会进一步根据 Token 中的 username 去数据库取 User
    """

    user = get_user(request)
    if not user:
        return responses.unauthorized("未登录或 Token 无效")

    return responses.ok(
        "ok",
        {
            "user_id": user.id,
            "username": user.get_username(),
        },
    )
