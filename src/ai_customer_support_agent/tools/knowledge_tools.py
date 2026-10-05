from langchain_core.tools import tool

from ai_customer_support_agent.rag.retriever import search_policies


@tool
def search_company_knowledge(query: str) -> dict:
    """Search company policies and support knowledge.

    Use this tool for questions about returns, refunds, shipping,
    warranties, replacements, damaged products, delivery rules,
    and other company policies.
    """

    documents = search_policies(
        query=query,
        k=3,
    )

    if not documents:
        return {
            "answer": "No relevant company policy was found.",
            "sources": [],
        }

    results = []

    for document in documents:
        results.append(
            {
                "content": document.page_content,
                "source": document.metadata.get("source", "unknown"),
            }
        )

    return {
        "results": results,
    }