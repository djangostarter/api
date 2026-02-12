from django.test import TestCase
from django.urls import reverse

from apps.integrations.models import AppClient, AppClientStatus


class AppClientApiKeyAuthTestCase(TestCase):
    def setUp(self):
        self.client_obj = AppClient(
            app_id="third-party-demo",
            app_name="Third Party Demo",
            key_id="kid_1",
            allowed_ips="",
            scopes="project:read",
            status=AppClientStatus.ACTIVE,
        )
        self.secret = "secret_1"
        self.client_obj.set_secret(self.secret)
        self.client_obj.save()

    def test_header_api_key_success(self):
        resp = self.client.get(
            reverse("api:integrations/ping"),
            HTTP_X_API_KEY=f"{self.client_obj.key_id}.{self.secret}",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        body = resp.json()
        self.assertEqual(body.get("data", {}).get("app_id"), self.client_obj.app_id, body)

    def test_header_api_key_invalid_secret(self):
        resp = self.client.get(
            reverse("api:integrations/ping"),
            HTTP_X_API_KEY=f"{self.client_obj.key_id}.wrong",
        )
        self.assertIn(resp.status_code, (401, 403))

    def test_ip_whitelist_denied(self):
        self.client_obj.allowed_ips = "10.0.0.1"
        self.client_obj.save(update_fields=["allowed_ips"])

        resp = self.client.get(
            reverse("api:integrations/ping"),
            HTTP_X_API_KEY=f"{self.client_obj.key_id}.{self.secret}",
            REMOTE_ADDR="127.0.0.1",
        )
        self.assertIn(resp.status_code, (401, 403))

    def test_scope_required_success(self):
        resp = self.client.get(
            reverse("api:integrations/projects"),
            HTTP_X_API_KEY=f"{self.client_obj.key_id}.{self.secret}",
        )
        self.assertEqual(resp.status_code, 200, resp.content)

    def test_scope_required_forbidden(self):
        self.client_obj.scopes = ""
        self.client_obj.save(update_fields=["scopes"])

        resp = self.client.get(
            reverse("api:integrations/projects"),
            HTTP_X_API_KEY=f"{self.client_obj.key_id}.{self.secret}",
        )
        self.assertEqual(resp.status_code, 403, resp.content)

