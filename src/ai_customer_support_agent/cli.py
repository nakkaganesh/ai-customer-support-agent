from ai_customer_support_agent.agents.support_agent import agent


THREAD_ID = "local-customer-session"


def main():
    print("\nAI Customer Support Agent")
    print("Type 'exit' to quit.\n")

    config = {
        "configurable": {
            "thread_id": THREAD_ID,
        }
    }

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                },
                config=config,
            )

            final_message = result["messages"][-1]

            print(f"\nAssistant: {final_message.content}\n")

        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    main()