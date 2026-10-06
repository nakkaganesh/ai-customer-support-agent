from langchain_core.tools import tool

from ai_customer_support_agent.db.repositories import (
    get_customer_by_customer_id,
    get_product_by_product_id,
    get_tickets_by_customer_id,
    create_support_ticket,get_order_for_customer
)
from ai_customer_support_agent.core.context import (
    get_current_customer_id,
)



@tool
def lookup_order(order_id: str) -> dict:
    """Look up an order belonging to the authenticated customer.

    Use this tool when the user asks about their order status,
    tracking number, total amount, or order date.
    """

    customer_id = get_current_customer_id()

    if customer_id is None:
        return {
            "error": "Authentication is required to access order information."
        }

    order = get_order_for_customer(
        order_id=order_id,
        customer_id=customer_id,
    )

    if order is None:
        return {
            "error": (
                "Order not found or you are not authorized "
                "to access this order."
            )
        }

    return order

@tool
def lookup_customer() -> dict:
    """Look up the authenticated customer's account information.

    Use this tool when the user asks about their own customer
    account, profile, email, phone, or customer information.
    """

    customer_id = get_current_customer_id()

    if customer_id is None:
        return {
            "error": "Authentication is required to access customer information."
        }

    customer = get_customer_by_customer_id(customer_id)

    if customer is None:
        return {
            "error": "Customer account was not found."
        }

    return customer


@tool
def lookup_product(product_id: str) -> dict:
    """Look up a product using a product ID, such as PROD-001.

    Use this tool for product information including name,
    category, price, and current stock.
    """
    product = get_product_by_product_id(product_id)

    if product is None:
        return {
            "error": f"Product {product_id} was not found."
        }

    return product


@tool
def lookup_customer_tickets() -> list[dict] | dict:
    """Look up support tickets belonging to the authenticated customer.

    Use this tool when the user asks about their own support tickets,
    ticket statuses, priorities, or previously reported issues.
    """

    customer_id = get_current_customer_id()

    if customer_id is None:
        return {
            "error": "Authentication is required to access support tickets."
        }

    return get_tickets_by_customer_id(customer_id)


@tool
def create_ticket(
    subject: str,
    description: str,
    priority: str = "medium",
) -> dict:
    """Create a support ticket for the authenticated customer.

    Use this tool only when the user explicitly asks to create,
    open, raise, or submit a support ticket.

    Derive the subject and description from the conversation when
    enough information is already available.

    Valid priorities are low, medium, and high.
    """

    customer_id = get_current_customer_id()

    if customer_id is None:
        return {
            "error": "Authentication is required to create a support ticket."
        }

    allowed_priorities = {
        "low",
        "medium",
        "high",
    }

    priority = priority.lower()

    if priority not in allowed_priorities:
        return {
            "error": (
                "Invalid priority. "
                "Priority must be low, medium, or high."
            )
        }

    result = create_support_ticket(
        customer_id=customer_id,
        subject=subject,
        description=description,
        priority=priority,
    )

    if result is None:
        return {
            "error": "Authenticated customer account was not found."
        }

    return result

DATABASE_TOOLS = [
    lookup_order,
    lookup_customer,
    lookup_product,
    lookup_customer_tickets,
    create_ticket
]