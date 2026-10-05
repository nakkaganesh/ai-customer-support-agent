import os

from dotenv import load_dotenv
from sqlalchemy import URL


load_dotenv()


DB_HOST = os.getenv("DB_HOST", "127.0.0.1").strip()
DB_PORT = int(os.getenv("DB_PORT", "3306").strip())
DB_NAME = os.getenv("DB_NAME", "ai_customer_support").strip()
DB_USER = os.getenv("DB_USER", "root").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()


if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not configured in .env")


DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)