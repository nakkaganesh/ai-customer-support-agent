from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ai_customer_support_agent.db.database import SessionLocal
from ai_customer_support_agent.db.models import (
    Customer,
    Order,
    Product,
    SupportTicket,
)


def get_order_by_order_id(order_id: str) -> dict | None:
    with SessionLocal() as session:
        statement = (
            select(Order)
            .where(Order.order_id == order_id)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items),
            )
        )

        order = session.scalar(statement)

        if order is None:
            return None

        return {
            "order_id": order.order_id,
            "customer": order.customer.name,
            "status": order.status,
            "tracking_number": order.tracking_number,
            "total_amount": float(order.total_amount),
            "ordered_at": order.ordered_at.isoformat(),
        }


def get_customer_by_customer_id(customer_id: str) -> dict | None:
    with SessionLocal() as session:
        statement = select(Customer).where(
            Customer.customer_id == customer_id
        )

        customer = session.scalar(statement)

        if customer is None:
            return None

        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        }


def get_product_by_product_id(product_id: str) -> dict | None:
    with SessionLocal() as session:
        statement = select(Product).where(
            Product.product_id == product_id
        )

        product = session.scalar(statement)

        if product is None:
            return None

        return {
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "price": float(product.price),
            "stock": product.stock,
        }


def get_tickets_by_customer_id(customer_id: str) -> list[dict]:
    with SessionLocal() as session:
        customer = session.scalar(
            select(Customer).where(
                Customer.customer_id == customer_id
            )
        )

        if customer is None:
            return []

        tickets = session.scalars(
            select(SupportTicket).where(
                SupportTicket.customer_id == customer.id
            )
        ).all()

        return [
            {
                "ticket_id": ticket.ticket_id,
                "subject": ticket.subject,
                "description": ticket.description,
                "status": ticket.status,
                "priority": ticket.priority,
            }
            for ticket in tickets
        ]