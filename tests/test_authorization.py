from ai_customer_support_agent.core.context import (
    reset_current_customer_id,
    set_current_customer_id,
)
from ai_customer_support_agent.tools.database_tools import lookup_order


def test_customer_can_access_own_order():
    token = set_current_customer_id("CUST-002")

    try:
        result = lookup_order.invoke(
            {
                "order_id": "ORD-1002",
            }
        )

        assert result["order_id"] == "ORD-1002"

    finally:
        reset_current_customer_id(token)


def test_customer_cannot_access_another_customers_order():
    token = set_current_customer_id("CUST-002")

    try:
        result = lookup_order.invoke(
            {
                "order_id": "ORD-1001",
            }
        )

        assert "error" in result
        assert "not authorized" in result["error"].lower()

    finally:
        reset_current_customer_id(token)


def test_order_lookup_requires_authentication():
    result = lookup_order.invoke(
        {
            "order_id": "ORD-1002",
        }
    )

    assert "error" in result
    assert "authentication is required" in result["error"].lower()