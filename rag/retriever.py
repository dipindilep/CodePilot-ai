
from dataclasses import dataclass

from rag.embeddings import embed_query
from rag.vector_store import CodeVectorStore


@dataclass
class RetrievedChunk:
    content: str
    file_path: str
    name: str
    type: str
    language: str
    start_line: int
    end_line: int
    chunk_number: int
    distance: float


class CodeRetriever:
    """Retrieve relevant code from one project."""

    def __init__(
        self,
        collection_name: str,
        persist_directory: str = "data/chroma",
    ):
        self.store = CodeVectorStore(
            persist_directory=persist_directory,
            collection_name=collection_name,
        )

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if n_results < 1:
            raise ValueError(
                "n_results must be at least 1."
            )

        query_embedding = embed_query(query)
        results = self.store.search(
            query_embedding,
            n_results=n_results,
        )

        retrieved = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for content, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved.append(
                RetrievedChunk(
                    content=content,
                    file_path=metadata["file_path"],
                    name=metadata["name"],
                    type=metadata["type"],
                    language=metadata["language"],
                    start_line=metadata["start_line"],
                    end_line=metadata["end_line"],
                    chunk_number=metadata.get(
                        "chunk_number", 0
                    ),
                    distance=distance,
                )
            )

        return retrieved
