from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Optional

from django.conf import settings
from django.http import HttpRequest
from ninja.security import APIKeyQuery, APIKeyHeader, HttpBearer

from apps.integrations.models import AppClient


@dataclass(frozen=True)
class ParsedApiKey:
    key_id: str
    secret: str


def parse_api_key(raw: str) -> Optional[ParsedApiKey]:
    if not raw:
        return None
    raw = raw.strip()
    if "." not in raw:
        return None
    key_id, secret = raw.split(".", 1)
    key_id = key_id.strip()
    secret = secret.strip()
    if not key_id or not secret:
        return None
    return ParsedApiKey(key_id=key_id, secret=secret)


class AppClientAuthMixin:
    def _get_client_ip(self, request: HttpRequest) -> str:
        if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR") or ""

    def _validate_ip_access(self, app_client: AppClient, request: HttpRequest) -> bool:
        allowed_ips = app_client.get_allowed_ips_list()
        if not allowed_ips:
            return True

        client_ip = self._get_client_ip(request)
        if not client_ip:
            return False

        for allowed_ip in allowed_ips:
            try:
                if "/" in allowed_ip:
                    network = ipaddress.ip_network(allowed_ip, strict=False)
                    if ipaddress.ip_address(client_ip) in network:
                        return True
                else:
                    if client_ip == allowed_ip:
                        return True
            except (ipaddress.AddressValueError, ValueError):
                continue
        return False

    def _authenticate_app_client(self, request: HttpRequest, raw_key: str) -> Optional[AppClient]:
        parsed = parse_api_key(raw_key)
        if not parsed:
            return None

        app_client = AppClient.objects.filter(key_id=parsed.key_id).first()
        if not app_client:
            return None
        if not app_client.is_active():
            return None
        if not app_client.verify_secret(parsed.secret):
            return None
        if not self._validate_ip_access(app_client, request):
            return None

        request.app_client_scopes = app_client.get_scopes_list()
        return app_client


class AppClientApiKeyQuery(AppClientAuthMixin, APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request: HttpRequest, key: str) -> Optional[AppClient]:
        return self._authenticate_app_client(request, key)


class AppClientApiKeyHeader(AppClientAuthMixin, APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str) -> Optional[AppClient]:
        return self._authenticate_app_client(request, key)


class AppClientBearer(AppClientAuthMixin, HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[AppClient]:
        return self._authenticate_app_client(request, token)


api_key_auth = AppClientApiKeyQuery()
api_key_header_auth = AppClientApiKeyHeader()
api_key_bearer_auth = AppClientBearer()

