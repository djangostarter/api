from django.http import HttpRequest
from ninja import Router

from django_starter_core.http.response import ResponseGenerator
from infra.app_client_auth import api_key_header_auth, api_key_bearer_auth, api_key_auth

from apps.integrations.permissions import require_app_client_scopes, AppClientScopes


router = Router(tags=["integrations"])
_resp = ResponseGenerator(router=router)


@router.get("/ping", auth=api_key_header_auth, url_name="integrations/ping")
def ping(request: HttpRequest):
    app_client = request.auth
    return _resp.ok(request, "OK", {"app_id": app_client.app_id, "app_name": app_client.app_name})


@router.get("/ping-bearer", auth=api_key_bearer_auth, url_name="integrations/ping_bearer")
def ping_bearer(request: HttpRequest):
    app_client = request.auth
    return _resp.ok(request, "OK", {"app_id": app_client.app_id, "app_name": app_client.app_name})


@router.get("/ping-query", auth=api_key_auth, url_name="integrations/ping_query")
def ping_query(request: HttpRequest):
    app_client = request.auth
    return _resp.ok(request, "OK", {"app_id": app_client.app_id, "app_name": app_client.app_name})


@router.get("/projects", auth=api_key_header_auth, url_name="integrations/projects")
@require_app_client_scopes([AppClientScopes.PROJECT_READ])
def list_projects(request: HttpRequest):
    return _resp.ok(request, "OK", {"projects": []})

