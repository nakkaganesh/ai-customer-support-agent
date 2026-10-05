from ai_customer_support_agent.db.database import Base, engine
from ai_customer_support_agent.db import models


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()