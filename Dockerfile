FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "ai_customer_support_agent.api.app:app", "--host", "0.0.0.0", "--port", "8000"]