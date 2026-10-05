from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from ai_customer_support_agent.tools.database_tools import DATABASE_TOOLS

from ai_customer_support_agent.tools.knowledge_tools import search_company_knowledge


from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

model=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

SYSTEM_PROMPT = """
You are an AI customer support assistant.

You have access to business database tools and a company
knowledge-base search tool.

Use database tools for:
- customers
- orders
- products
- inventory
- support tickets

Use search_company_knowledge for:
- return policies
- refund policies
- shipping policies
- warranty policies
- replacement policies

For questions that require both customer/order information
and company policy, use all necessary tools before answering.

Never invent customer data, order data, tracking information,
prices, stock levels, ticket information, or company policies.

Base company-policy answers on information returned by the
knowledge-base tool.

If the available information is insufficient, say so clearly.

Be concise, helpful, and professional.
"""


checkpointer=InMemorySaver()

ALL_TOOLS = [
    *DATABASE_TOOLS,
    search_company_knowledge,
]


agent=create_agent(
    model=model,
    tools=ALL_TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)

if __name__ == "__main__":

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Order ORD-1002 was delivered and I want to return it.Check my order and tell me what the company's return policy says..",
                }
            ]
        }
    )

    print("\n--- AGENT MESSAGE HISTORY ---")

    for message in result["messages"]:
        print(
            type(message).__name__,
            ":",
            message.content,
        )

        if hasattr(message, "tool_calls") and message.tool_calls:
            print("Tool calls:", message.tool_calls)

    print("-----------------------------")

    print("\nFINAL ANSWER:")
    print(result["messages"][-1].content)