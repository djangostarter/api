"""
认证相关 Schema 定义。

约定：
- 所有响应都至少包含 `detail` 字段（统一响应）
- Token 返回 `token` 与 `exp`（过期时间戳）
"""

from ninja import Schema


class ErrorOut(Schema):
    """
    统一错误响应结构（最小化字段）。
    """

    detail: str


class TokenIn(Schema):
    """
    登录换取 JWT 的输入。
    """

    username: str
    password: str


class TokenOut(Schema):
    """
    登录换取 JWT 的输出（成功响应）。
    """

    detail: str
    token: str
    exp: int


class MeOut(Schema):
    """
    当前登录用户信息（成功响应）。
    """

    detail: str
    user_id: int
    username: str

