from ai_customer_support_agent.core.context import (
    reset_current_customer_id,
    set_current_customer_id,
)
from ai_customer_support_agent.tools.database_tools import create_ticket


def test_ticket_creation_requires_authentication():
    result = create_ticket.invoke(
        {
            "subject": "Test issue",
            "description": "This should not create a ticket.",
            "priority": "medium",
        }
    )

    assert "error" in result
    assert "authentication is required" in result["error"].lower()


def test_ticket_rejects_invalid_priority():
    token = set_current_customer_id("CUST-002")

    try:
        result = create_ticket.invoke(
            {
                "subject": "Test issue",
                "description": "Testing priority validation.",
                "priority": "urgent",
            }
        )

        assert "error" in result
        assert "invalid priority" in result["error"].lower()

    finally:
        reset_current_customer_id(token)


def test_create_ticket_schema_does_not_expose_customer_id():
    schema = create_ticket.args_schema.model_json_schema()

    properties = schema["properties"]

    assert "customer_id" not in properties
    assert "subject" in properties
    assert "description" in properties
    assert "priority" in properties