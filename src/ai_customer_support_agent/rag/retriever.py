from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()

INDEX_NAME = "customer-support-policies"


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings,
)


def search_policies(query: str, k: int = 3):
    return vectorstore.similarity_search(
        query=query,
        k=k,
    )