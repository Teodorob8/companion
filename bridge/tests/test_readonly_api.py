from fastapi.testclient import TestClient

from bridge.aegis_companion.readonly_api import app, pairing


def test_readonly_api_requires_pairing(monkeypatch):
    client = TestClient(app)
    assert client.get("/health").json()["live_authority"] is False
    assert client.get("/companion/status").status_code == 401
    code = pairing.issue_code()
    response = client.post("/pairing/redeem", json={"code": code})
    assert response.status_code == 200
    credential = response.json()["credential"]
    assert client.get("/companion/status", headers={"Authorization": f"Bearer {credential}"}).status_code == 200
