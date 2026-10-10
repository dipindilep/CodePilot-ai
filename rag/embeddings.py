#An embedding model converts text into a list of numbers called a vector. The vector represents aspects of the text's meaning in a numerical form.


from dataclasses import dataclass

import requests

from rag.chunker import CodeChunk


MODEL_NAME = "nomic-embed-text"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"


@dataclass
class EmbeddedChunk:
    chunk: CodeChunk
    embedding: list[float]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert a list of texts into numerical vectors."""

    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Embedding input cannot be empty.")

    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": MODEL_NAME,
            "input": texts,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["embeddings"]


def embed_chunks(
    chunks: list[CodeChunk],
) -> list[EmbeddedChunk]:
    """Generate an embedding for each code chunk."""

    if not chunks:
        return []

    texts = [
        f"search_document: {chunk.content}"
        for chunk in chunks
    ]

    embeddings = embed_texts(texts)

    if len(embeddings) != len(chunks):
        raise ValueError(
            "Number of embeddings does not match number of chunks."
        )

    return [
        EmbeddedChunk(chunk=chunk, embedding=embedding)
        for chunk, embedding in zip(chunks, embeddings)
    ]


def embed_query(query: str) -> list[float]:
    """Generate an embedding for a user's search query."""

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    embeddings = embed_texts([
        f"search_query: {query}"
    ])

    return embeddings[0]
