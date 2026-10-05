from langchain_core.tools import tool

from ai_customer_support_agent.db.repositories import (
    get_customer_by_customer_id,
    get_order_by_order_id,
    get_product_by_product_id,
    get_tickets_by_customer_id,
    create_support_ticket
)


@tool
def lookup_order(order_id: str) -> dict:
    """Look up an order using its order ID, such as ORD-1001.

    Use this tool when the user asks about an order's status,
    tracking number, total amount, or order date.
    """
    order = get_order_by_order_id(order_id)

    if order is None:
        return {
            "error": f"Order {order_id} was not found."
        }

    return order


@tool
def lookup_customer(customer_id: str) -> dict:
    """Look up a customer using a customer ID, such as CUST-001.

    Use this tool when customer account information is required.
    """
    customer = get_customer_by_customer_id(customer_id)

    if customer is None:
        return {
            "error": f"Customer {customer_id} was not found."
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
def lookup_customer_tickets(customer_id: str) -> list[dict]:
    """Look up support tickets belonging to a customer.

    Use this tool when the user asks about support requests,
    ticket status, ticket priority, or existing issues.
    """
    return get_tickets_by_customer_id(customer_id)


@tool
def create_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "medium",
) -> dict:
    """Create a new customer support ticket.

    Use this tool only when the user explicitly asks to create,
    open, or raise a support ticket.

    Valid priorities are low, medium, and high.
    """

    allowed_priorities = {"low", "medium", "high"}

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
            "error": f"Customer {customer_id} was not found."
        }

    return result

DATABASE_TOOLS = [
    lookup_order,
    lookup_customer,
    lookup_product,
    lookup_customer_tickets,
    create_ticket
]