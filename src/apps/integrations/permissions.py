from __future__ import annotations

from functools import wraps
from typing import Callable, Any

from django.http import HttpRequest

from .exceptions import AppClientPermissionError
from .models import AppClient


def _has_scope(client_scopes: list[str], required_scope: str) -> bool:
    if not client_scopes:
        return False
    if required_scope in client_scopes:
        return True
    for scope in client_scopes:
        if scope == "*":
            return True
        if scope.endswith(":*"):
            prefix = scope[:-1]
            if required_scope.startswith(prefix):
                return True
    return False


def require_app_client_scopes(required_scopes: list[str]):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs) -> Any:
            auth_obj = getattr(request, "auth", None)
            if not isinstance(auth_obj, AppClient):
                raise AppClientPermissionError("未认证的请求")

            client_scopes: list[str] = getattr(request, "app_client_scopes", [])
            for required_scope in required_scopes:
                if not _has_scope(client_scopes, required_scope):
                    raise AppClientPermissionError(f"缺少权限: {required_scope}")

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class AppClientScopes:
    PROJECT_READ = "project:read"
    PROJECT_WRITE = "project:write"
    PROJECT_DELETE = "project:delete"
    PROJECT_ALL = "project:*"

    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    USER_ALL = "user:*"

    SUPER_ADMIN = "*"


class AppClientScopeChecker:
    @staticmethod
    def get_client_scopes(request: HttpRequest) -> list[str]:
        return getattr(request, "app_client_scopes", [])

    @staticmethod
    def check_scopes(request: HttpRequest, required_scopes: list[str]) -> bool:
        client_scopes = getattr(request, "app_client_scopes", [])
        return all(_has_scope(client_scopes, s) for s in required_scopes)

    @staticmethod
    def has_any_scope(request: HttpRequest, scopes: list[str]) -> bool:
        client_scopes = getattr(request, "app_client_scopes", [])
        return any(_has_scope(client_scopes, s) for s in scopes)

