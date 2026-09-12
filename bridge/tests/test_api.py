from fastapi.testclient import TestClient
from bridge.aegis_companion.main import app

client = TestClient(app)

def test_health_denies_live_authority():
    data = client.get("/health").json()
    assert data["live_authority"] is False

def test_aegis_status_is_read_only():
    response = client.get("/aegis/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READ_ONLY"
    assert data["live_authority"] is False
    assert data["orders_enabled"] is False
    assert data["frozen_scanner_modified"] is False

def test_duplicate_command_is_harmless():
    body = {
        "command":"status",
        "mode":"RESEARCH",
        "requested_capability":"READ_STATUS",
        "correlation_id":"corr-12345678",
        "idempotency_key":"idem-12345678",
        "args":{}
    }
    first = client.post("/command", json=body)
    second = client.post("/command", json=body)
    assert first.status_code == 200
    assert second.json()["status"] == "duplicate_suppressed"
