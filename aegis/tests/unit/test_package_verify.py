from fastapi.testclient import TestClient

from app.main import app


def test_verify_package_endpoint():
    client = TestClient(app)
    response = client.post(
        "/api/v1/package/verify",
        json={"package_name": "definitely_fake_pkg_name", "context_code": "import definitely_fake_pkg_name", "development_context": {}},
    )
    assert response.status_code == 200
    assert response.json()["hallucination"] is True
