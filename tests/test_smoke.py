import pytest


@pytest.mark.django_db
def test_openapi_json(client):
    resp = client.get("/api/openapi.json")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["info"]["title"]
