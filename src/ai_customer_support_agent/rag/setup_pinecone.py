import os
import time

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not configured in .env")


INDEX_NAME = "customer-support-policies"

pc = Pinecone(api_key=PINECONE_API_KEY)


def create_index():
    existing_indexes = [
        index["name"]
        for index in pc.list_indexes()
    ]

    if INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

        print(f"Creating Pinecone index: {INDEX_NAME}")

        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)

        print("Pinecone index is ready.")

    else:
        print(f"Pinecone index already exists: {INDEX_NAME}")


if __name__ == "__main__":
    create_index()