from fastapi.testclient import TestClient

from ai_customer_support_agent.api.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "ai-customer-support-agent",
    }