import os

from fastapi.testclient import TestClient

from ai_customer_support_agent.api.app import app


client = TestClient(app)


def test_chat_rejects_invalid_api_key():
    response = client.post(
        "/chat",
        headers={
            "X-API-Key": "definitely-invalid-key",
        },
        json={
            "message": "Hello",
            "thread_id": "pytest-invalid-auth",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key."


def test_chat_rejects_missing_api_key():
    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "thread_id": "pytest-missing-auth",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "API key is required."