from dataclasses import dataclass


@dataclass
class CodeChunk:
    content: str
    type: str
    name: str | None
    language: str
    file_path: str
    start_line: int
    end_line: int
    chunk_number: int | None = None

#chunking function

def chunk_code(
    structure,
    file_path: str
) -> list[CodeChunk]:

    chunks = []

    for node in structure.nodes:

        chunks.append(
            CodeChunk(
                content=node.content,
                type=node.type,
                name=node.name,
                language=structure.language,
                file_path=file_path,
                start_line=node.start_line,
                end_line=node.end_line,
            )
        )

        for child in node.children:

            chunks.append(
                CodeChunk(
                    content=child.content,
                    type=child.type,
                    name=child.name,
                    language=structure.language,
                    file_path=file_path,
                    start_line=child.start_line,
                    end_line=child.end_line,
                )
            )

    return chunks