from pathlib import Path

from backend.app.services.repository_service import (
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)


def search_repository(
    project_path: str,
    query: str,
) -> list[dict]:
    """
    Search for a text query across source files in a repository.

    Args:
        project_path: Path to the project directory.
        query: Text to search for.

    Returns:
        A list of matching files, line numbers, and lines.
    """

    project = Path(project_path)

    if not project.exists():
        raise FileNotFoundError(
            f"Project '{project_path}' does not exist."
        )

    if not project.is_dir():
        raise NotADirectoryError(
            f"'{project_path}' is not a directory."
        )

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    results = []

    for file in project.rglob("*"):

        if not file.is_file():
            continue

        if any(
            directory in file.parts
            for directory in IGNORED_DIRECTORIES
        ):
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f, start=1):

                    if query.lower() in line.lower():
                        results.append({
                            "file": str(file),
                            "line": line_number,
                            "content": line.strip(),
                        })

        except UnicodeDecodeError:
            continue

    return results