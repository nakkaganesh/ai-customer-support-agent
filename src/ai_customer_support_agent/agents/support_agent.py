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
SUPPORT TICKET ACTION RULES:

SUPPORT TICKET ACTION RULES:

SUPPORT TICKET ACTION RULES:

- Creating a support ticket is a write action.

- ONLY begin the ticket-creation workflow when the user explicitly
  asks to create, open, raise, or submit a support ticket/request.

- A user reporting a problem does NOT mean they want a ticket created.

- Do not ask for ticket-creation information unless the user has
  explicitly requested ticket creation.

- If the user only reports a problem, help them with the problem.

- After the user explicitly requests ticket creation, a customer ID
  is required. Ask for it if it is not already available.

- Derive a concise ticket subject and description from the conversation
  when the user has already explained the problem.

- Do not make the user repeat information that is already available
  in the conversation.

- Ask for a subject or description only when the conversation does
  not contain enough information to determine them reliably.

- Never invent the customer ID.

- Never call create_ticket unless the user explicitly requested
  ticket creation.

- Never claim a ticket was created unless create_ticket successfully
  returns a ticket ID.

- Use medium priority by default unless the conversation clearly
  supports low or high priority.

- Valid priorities are low, medium, and high.

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