from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from ai_customer_support_agent.api.app import app


client = TestClient(app)


@patch("ai_customer_support_agent.api.app.agent")
def test_chat_success(mock_agent: MagicMock):
    mock_agent.invoke.return_value = {
        "messages": [
            AIMessage(content="Your order has been shipped.")
        ]
    }

    response = client.post(
        "/chat",
        headers={
            "X-API-Key": "dev-key-customer-002",
        },
        json={
            "message": "Where is my order?",
            "thread_id": "pytest-chat-001",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"] == "Your order has been shipped."
    assert data["thread_id"] == "pytest-chat-001"

    mock_agent.invoke.assert_called_once()


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        headers={
            "X-API-Key": "dev-key-customer-002",
        },
        json={
            "message": "",
            "thread_id": "pytest-chat-002",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_empty_thread_id():
    response = client.post(
        "/chat",
        headers={
            "X-API-Key": "dev-key-customer-002",
        },
        json={
            "message": "Hello",
            "thread_id": "",
        },
    )

    assert response.status_code == 422


@patch("ai_customer_support_agent.api.app.agent")
def test_chat_hides_internal_errors(mock_agent: MagicMock):
    mock_agent.invoke.side_effect = RuntimeError(
        "Secret internal database failure"
    )

    response = client.post(
        "/chat",
        headers={
            "X-API-Key": "dev-key-customer-002",
        },
        json={
            "message": "Hello",
            "thread_id": "pytest-chat-error",
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Unable to process the request."
    )

    assert "Secret internal database failure" not in response.text