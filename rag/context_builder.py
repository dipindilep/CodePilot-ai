
from rag.retriever import RetrievedChunk


def build_context(
    chunks: list[RetrievedChunk],
    max_chars: int = 12000,
) -> str:
    """Format retrieved code within a character budget."""

    if max_chars < 1:
        raise ValueError(
            "max_chars must be at least 1."
        )

    if not chunks:
        return "No relevant code was found."

    sections = []
    used_chars = 0

    for chunk in chunks:
        header = (
            f"File: {chunk.file_path}\n"
            f"Symbol: {chunk.name} ({chunk.type})\n"
            f"Lines: {chunk.start_line}-{chunk.end_line}\n"
            f"Language: {chunk.language}\n"
        )

        section = (
            f"{header}"
            f"```{chunk.language}\n"
            f"{chunk.content}\n"
            f"```"
        )

        separator = "\n\n"
        additional_chars = len(section) + (
            len(separator) if sections else 0
        )

        if used_chars + additional_chars > max_chars:
            remaining = max_chars - used_chars

            if remaining > 0 and not sections:
                sections.append(section[:max_chars])
            break

        sections.append(section)
        used_chars += additional_chars

    if not sections:
        return "No code fits within the context limit."

    return "\n\n".join(sections)
