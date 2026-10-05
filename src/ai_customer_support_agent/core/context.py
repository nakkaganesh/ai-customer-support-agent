from contextvars import ContextVar


current_customer_id: ContextVar[str | None] = ContextVar(
    "current_customer_id",
    default=None,
)


def get_current_customer_id() -> str | None:
    return current_customer_id.get()


def set_current_customer_id(customer_id: str):
    return current_customer_id.set(customer_id)


def reset_current_customer_id(token) -> None:
    current_customer_id.reset(token)