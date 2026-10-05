from datetime import datetime
from decimal import Decimal

from sqlalchemy import select

from ai_customer_support_agent.db.database import SessionLocal
from ai_customer_support_agent.db.models import (
    Customer,
    Order,
    OrderItem,
    Product,
    SupportTicket,
)


def seed_database():
    with SessionLocal() as session:

        # Prevent duplicate seeding
        existing_customer = session.scalar(
            select(Customer).limit(1)
        )

        if existing_customer:
            print("Database already contains data. Skipping seed.")
            return

        # --------------------
        # CUSTOMERS
        # --------------------

        customer1 = Customer(
            customer_id="CUST-001",
            name="Arjun Rao",
            email="arjun@example.com",
            phone="9876543210",
        )

        customer2 = Customer(
            customer_id="CUST-002",
            name="Priya Sharma",
            email="priya@example.com",
            phone="9876543211",
        )

        customer3 = Customer(
            customer_id="CUST-003",
            name="Rahul Verma",
            email="rahul@example.com",
            phone="9876543212",
        )

        # --------------------
        # PRODUCTS
        # --------------------

        product1 = Product(
            product_id="PROD-001",
            name="Wireless Headphones",
            category="Electronics",
            price=Decimal("4999.00"),
            stock=25,
        )

        product2 = Product(
            product_id="PROD-002",
            name="Mechanical Keyboard",
            category="Electronics",
            price=Decimal("3499.00"),
            stock=15,
        )

        product3 = Product(
            product_id="PROD-003",
            name="Laptop Stand",
            category="Accessories",
            price=Decimal("1999.00"),
            stock=40,
        )

        session.add_all(
            [
                customer1,
                customer2,
                customer3,
                product1,
                product2,
                product3,
            ]
        )

        # Flush assigns database IDs without committing yet
        session.flush()

        # --------------------
        # ORDERS
        # --------------------

        order1 = Order(
            order_id="ORD-1001",
            customer_id=customer1.id,
            status="shipped",
            tracking_number="TRK-928374",
            total_amount=Decimal("4999.00"),
            ordered_at=datetime(2026, 9, 25, 10, 30),
        )

        order2 = Order(
            order_id="ORD-1002",
            customer_id=customer2.id,
            status="delivered",
            tracking_number="TRK-928375",
            total_amount=Decimal("5498.00"),
            ordered_at=datetime(2026, 9, 20, 14, 15),
        )

        order3 = Order(
            order_id="ORD-1003",
            customer_id=customer3.id,
            status="processing",
            tracking_number=None,
            total_amount=Decimal("3499.00"),
            ordered_at=datetime(2026, 10, 2, 9, 45),
        )

        session.add_all([order1, order2, order3])
        session.flush()

        # --------------------
        # ORDER ITEMS
        # --------------------

        items = [
            OrderItem(
                order_id=order1.id,
                product_id=product1.id,
                quantity=1,
                unit_price=product1.price,
            ),
            OrderItem(
                order_id=order2.id,
                product_id=product2.id,
                quantity=1,
                unit_price=product2.price,
            ),
            OrderItem(
                order_id=order2.id,
                product_id=product3.id,
                quantity=1,
                unit_price=product3.price,
            ),
            OrderItem(
                order_id=order3.id,
                product_id=product2.id,
                quantity=1,
                unit_price=product2.price,
            ),
        ]

        session.add_all(items)

        # --------------------
        # SUPPORT TICKETS
        # --------------------

        ticket1 = SupportTicket(
            ticket_id="TKT-001",
            customer_id=customer1.id,
            subject="Delivery delay",
            description="My order has not arrived yet.",
            status="open",
            priority="high",
        )

        ticket2 = SupportTicket(
            ticket_id="TKT-002",
            customer_id=customer3.id,
            subject="Change delivery address",
            description="I need to update my delivery address.",
            status="open",
            priority="medium",
        )

        session.add_all([ticket1, ticket2])

        session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()