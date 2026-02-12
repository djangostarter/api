import os
import pytest

from apps.integrations.models import AppClient, AppClientStatus


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@pytest.mark.django_db
def test_app_client_api_key_header_success(client):
    if not _env_bool("DJANGO_STARTER_ENABLE_INTEGRATIONS_API", True):
        pytest.skip("integrations 模块已关闭")

    app_client = AppClient(
        app_id="third-party-demo",
        app_name="Third Party Demo",
        key_id="kid_1",
        allowed_ips="",
        scopes="project:read",
        status=AppClientStatus.ACTIVE,
    )
    secret = "secret_1"
    app_client.set_secret(secret)
    app_client.save()

    resp = client.get(
        "/api/integrations/third-party/ping",
        HTTP_X_API_KEY=f"{app_client.key_id}.{secret}",
    )
    assert resp.status_code == 200, resp.content
    assert resp.json()["data"]["app_id"] == app_client.app_id


@pytest.mark.django_db
def test_app_client_scope_required_forbidden(client):
    if not _env_bool("DJANGO_STARTER_ENABLE_INTEGRATIONS_API", True):
        pytest.skip("integrations 模块已关闭")

    app_client = AppClient(
        app_id="third-party-demo",
        app_name="Third Party Demo",
        key_id="kid_1",
        allowed_ips="",
        scopes="",
        status=AppClientStatus.ACTIVE,
    )
    secret = "secret_1"
    app_client.set_secret(secret)
    app_client.save()

    resp = client.get(
        "/api/integrations/third-party/projects",
        HTTP_X_API_KEY=f"{app_client.key_id}.{secret}",
    )
    assert resp.status_code == 403
