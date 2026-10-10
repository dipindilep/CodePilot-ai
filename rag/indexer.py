
from dataclasses import dataclass, replace
from hashlib import sha1
from pathlib import Path
import re

import chromadb

from parser import detect_language, parse_file
from rag.chunker import CodeChunk, chunk_code
from rag.embeddings import embed_chunks
from rag.vector_store import CodeVectorStore


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".next",
    "build",
    "dist",
    "chroma",
}


@dataclass
class IndexingResult:
    project_path: str
    collection_name: str
    files_discovered: int
    files_processed: int
    chunks_indexed: int


def discover_source_files(
    project_path: str | Path,
) -> list[Path]:
    root = Path(project_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Project directory does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Expected a project directory: {root}"
        )

    source_files = []

    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_parts[:-1]
        ):
            continue

        if not path.is_file():
            continue

        if detect_language(str(path)) is None:
            continue

        source_files.append(path)

    return sorted(source_files)


def project_collection_name(
    project_path: str | Path,
) -> str:
    root = Path(project_path).resolve()

    readable_name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        root.name.lower(),
    ).strip("_-")

    readable_name = readable_name[:40] or "project"
    path_hash = sha1(
        str(root).encode("utf-8")
    ).hexdigest()[:8]

    return f"project_{readable_name}_{path_hash}"


def parse_project(
    project_path: str | Path,
) -> list[CodeChunk]:
    root = Path(project_path).resolve()
    files = discover_source_files(root)
    all_chunks = []

    for file_path in files:
        try:
            structure = parse_file(str(file_path))
            chunks = chunk_code(
                structure,
                str(file_path),
            )

            # Assign sequential numbers across this project.
            for chunk in chunks:
                numbered_chunk = replace(
                    chunk,
                    chunk_number=len(all_chunks) + 1,
                )
                all_chunks.append(numbered_chunk)

            print(
                f"Parsed: {file_path} "
                f"({len(chunks)} chunks)"
            )

        except Exception as exc:
            print(f"Skipped {file_path}: {exc}")

    return all_chunks


def index_project(
    project_path: str | Path,
    persist_directory: str = "data/chroma",
    reset: bool = True,
    batch_size: int = 32,
) -> IndexingResult:
    root = Path(project_path).resolve()

    if batch_size < 1:
        raise ValueError("batch_size must be at least 1.")

    files = discover_source_files(root)
    chunks = parse_project(root)

    collection_name = project_collection_name(root)
    db_path = Path(persist_directory).resolve()

    # A full reindex removes stale records for this project only.
    if reset:
        client = chromadb.PersistentClient(
            path=str(db_path)
        )
        existing = {
            collection.name
            for collection in client.list_collections()
        }

        if collection_name in existing:
            client.delete_collection(
                name=collection_name
            )

    store = CodeVectorStore(
        persist_directory=str(db_path),
        collection_name=collection_name,
    )

    # Embed and store in batches to limit memory use.
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        embedded = embed_chunks(batch)
        store.add_chunks(embedded)

        print(
            f"Indexed chunks: "
            f"{min(start + len(batch), len(chunks))}"
            f"/{len(chunks)}"
        )

    return IndexingResult(
        project_path=str(root),
        collection_name=collection_name,
        files_discovered=len(files),
        files_processed=len({
            chunk.file_path for chunk in chunks
        }),
        chunks_indexed=store.collection.count(),
    )
