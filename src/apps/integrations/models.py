from __future__ import annotations

import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.hashers import check_password, make_password

from django_starter_core.db.models import ModelExt
from django_starter_core.utilities import table_name_wrapper


class AppClientStatus(models.TextChoices):
    ACTIVE = "active", "启用"
    INACTIVE = "inactive", "禁用"


class AppClient(ModelExt):
    guid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="全局唯一标识")

    app_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="应用标识",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_-]+$",
                message="应用标识只能包含字母、数字、下划线和连字符",
            )
        ],
    )
    app_name = models.CharField(max_length=200, verbose_name="应用名称")

    key_id = models.CharField(max_length=64, unique=True, verbose_name="Key ID")
    secret_hash = models.CharField(max_length=256, verbose_name="密钥哈希")

    allowed_ips = models.TextField(blank=True, default="", verbose_name="允许访问的IP")
    scopes = models.TextField(blank=True, default="", verbose_name="权限范围")

    status = models.CharField(max_length=10, choices=AppClientStatus.choices, default=AppClientStatus.ACTIVE, verbose_name="状态")

    class Meta:
        db_table = table_name_wrapper("integration_app_client")
        verbose_name = "应用客户端"
        verbose_name_plural = "应用客户端"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["app_id"]),
            models.Index(fields=["key_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.app_name} ({self.app_id})"

    def is_active(self) -> bool:
        return self.status == AppClientStatus.ACTIVE and not self.is_deleted

    def get_scopes_list(self) -> list[str]:
        if not self.scopes:
            return []
        return [scope.strip() for scope in self.scopes.split(",") if scope.strip()]

    def get_allowed_ips_list(self) -> list[str]:
        if not self.allowed_ips:
            return []
        return [ip.strip() for ip in self.allowed_ips.split(",") if ip.strip()]

    def set_secret(self, secret: str) -> None:
        self.secret_hash = make_password(secret)

    def verify_secret(self, secret: str) -> bool:
        if not self.secret_hash:
            return False
        return check_password(secret, self.secret_hash)
