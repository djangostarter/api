from typing import Optional, Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja.security import HttpBearer

from django_starter_core.contrib.auth.services import decode


def user_from_payload(payload: dict) -> Optional[User]:
    user_id = payload.get("user_id") or payload.get("uid")
    if user_id:
        try:
            return User.objects.filter(id=int(user_id)).first()
        except (TypeError, ValueError):
            return None

    username = payload.get("username")
    if username:
        return User.objects.filter(username=username).first()

    return None


class JwtBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        payload = decode(token)
        if not payload:
            return None
        return user_from_payload(payload)

