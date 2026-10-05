from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

KNOWLEDGE_DIR = Path("data/knowledge")
INDEX_NAME = "customer-support-policies"


def load_documents() -> list[Document]:
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name},
            )
        )

    return documents


def split_documents(
    documents: list[Document],
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def ingest_documents():
    documents = load_documents()

    if not documents:
        raise ValueError(
            f"No knowledge documents found in {KNOWLEDGE_DIR}"
        )

    chunks = split_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME,
    )

    print("Documents uploaded to Pinecone successfully.")


if __name__ == "__main__":
    ingest_documents()
