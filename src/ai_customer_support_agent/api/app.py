from fastapi import FastAPI, HTTPException

from ai_customer_support_agent.agents.support_agent import agent
from ai_customer_support_agent.api.schemas import (
    ChatRequest,
    ChatResponse,
)


app = FastAPI(
    title="AI Customer Support Agent API",
    description=(
        "Customer support API powered by LangChain, "
        "MySQL, and Pinecone RAG."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-customer-support-agent",
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    try:
        config = {
            "configurable": {
                "thread_id": request.thread_id,
            }
        }

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ]
            },
            config=config,
        )

        final_message = result["messages"][-1]

        return ChatResponse(
            response=final_message.content,
            thread_id=request.thread_id,
        )

    except Exception as exc:
        print(f"Chat error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the request.",
        ) from exc