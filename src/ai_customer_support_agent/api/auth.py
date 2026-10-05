import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status


load_dotenv()


def get_authenticated_customer(
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> str:
    if not x_api_key:
     raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API key is required.",
    )
    api_key_map = {
        os.getenv("CUSTOMER_001_API_KEY"): "CUST-001",
        os.getenv("CUSTOMER_002_API_KEY"): "CUST-002",
        os.getenv("CUSTOMER_003_API_KEY"): "CUST-003",
    }

    for expected_key, customer_id in api_key_map.items():
        if (
            expected_key
            and secrets.compare_digest(x_api_key, expected_key)
        ):
            return customer_id

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key.",
    )