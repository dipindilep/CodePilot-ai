from pathlib import Path


EXTENSION_TO_LANGUAGE = {
    ".py": "python",

    ".java": "java",

    ".c": "c",
    ".h": "c",

    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",

    ".js": "javascript",
    ".jsx": "javascript",

    ".ts": "typescript",
    ".tsx": "tsx",

    ".go": "go",

    ".rs": "rust",

    ".php": "php",

    ".cs": "c_sharp",

    ".kt": "kotlin",

    ".swift": "swift",

    ".rb": "ruby",

    ".scala": "scala",

    ".m": "objc",
    ".mm": "objc",
}


def detect_language(file_path: str) -> str | None:
    """
    Detect the programming language from a file extension.

    Args:
        file_path: Path to the source file.

    Returns:
        Tree-sitter language name, or None if unsupported.
    """

    extension = Path(file_path).suffix.lower()

    return EXTENSION_TO_LANGUAGE.get(extension)