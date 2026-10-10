
from pathlib import Path

import chromadb

from rag.embeddings import EmbeddedChunk


class CodeVectorStore:
    """Persist and search embedded code chunks."""

    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "codepilot_code",
    ):
        db_path = Path(persist_directory).resolve()
        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(db_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        embedded_chunks: list[EmbeddedChunk],
    ) -> None:
        if not embedded_chunks:
            return

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for item in embedded_chunks:
            chunk = item.chunk

            chunk_id = (
                f"{chunk.file_path}:"
                f"{chunk.type}:"
                f"{chunk.start_line}:"
                f"{chunk.end_line}"
            )

            ids.append(chunk_id)
            documents.append(chunk.content)
            embeddings.append(item.embedding)

            metadatas.append({
                "file_path": chunk.file_path,
                "type": chunk.type,
                "name": chunk.name or "",
                "language": chunk.language,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "chunk_number": chunk.chunk_number or 0,
            })

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
    ) -> dict:
        total = self.collection.count()

        if total == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, total),
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )
