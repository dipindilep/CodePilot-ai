from pathlib import Path

# Source code file extensions supported by CodePilot
SUPPORTED_EXTENSIONS = {
    ".py",      # Python
    ".java",    # Java
    ".c",       # C
    ".cpp",     # C++
    ".h",       # C Header
    ".hpp",     # C++ Header
    ".js",      # JavaScript
    ".ts",      # TypeScript
    ".jsx",     # React JavaScript
    ".tsx",     # React TypeScript
    ".go",      # Go
    ".rs",      # Rust
    ".php",     # PHP
    ".cs",      # C#
    ".kt",      # Kotlin
    ".swift",   # Swift
    ".rb",      # Ruby
    ".scala",   # Scala
    ".m",       # Objective-C
    ".mm",      # Objective-C++
}


def list_source_files(project_path: str) -> list[str]:
    """
    Recursively find all supported source code files inside a project.

    Args:
        project_path: Path to the project directory.

    Returns:
        List of source file paths.
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

    source_files = []

    # Search every file in the repository
    for file in project.rglob("*"):

        # Skip directories
        if not file.is_file():
            continue

        # Keep only supported source files
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            source_files.append(str(file))

    return sorted(source_files)


def read_file_content(file_path: str) -> str:
    """
    Read the content of a file.

    Args:
        file_path: Path to the file.

    Returns:
        Content of the file as a string.
    """

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(
            f"File '{file_path}' does not exist."
        )

    if not file.is_file():
        raise IsADirectoryError(
            f"'{file_path}' is not a file."
        )

    with open(file, "r", encoding="utf-8") as f:
        return f.read()