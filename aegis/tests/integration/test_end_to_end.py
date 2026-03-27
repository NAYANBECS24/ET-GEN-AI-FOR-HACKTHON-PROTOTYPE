from fastapi.testclient import TestClient

from app.main import app


def test_end_to_end_verify_and_correlate():
    client = TestClient(app)
    verify = client.post(
        "/api/v1/package/verify",
        json={"package_name": "requests", "context_code": "import requests", "development_context": {}},
    )
    assert verify.status_code == 200

    correlate = client.post(
        "/api/v1/threat/correlate",
        json={
            "development_events": [verify.json()],
            "runtime_events": [{"event_type": "ssh_bruteforce"}],
        },
    )
    assert correlate.status_code == 200
    assert "correlation_score" in correlate.json()
    assert "confidence" in correlate.json()
