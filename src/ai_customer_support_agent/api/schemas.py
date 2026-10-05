from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Customer message",
    )

    thread_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Conversation thread identifier",
    )


class ChatResponse(BaseModel):
    response: str
    thread_id: str