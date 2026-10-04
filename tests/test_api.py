from fastapi.testclient import TestClient
from app.api import app


def test_api_health_and_agent():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}

    response = client.post(
        "/agent",
        json={"request": "calculate: 9 * 9", "session_id": "api-test"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["response"] == "81"
    assert payload["tool_used"] == "calculator"
    assert len(payload["memory"]) == 2
