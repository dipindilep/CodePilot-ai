from dataclasses import dataclass, field

@dataclass
class CodeNode:
    """
    Language-independent representation of a code element.
    """

    type: str
    name: str | None
    start_line: int
    end_line: int
    content: str
    children: list["CodeNode"] = field(default_factory=list)


@dataclass
class CodeStructure:
    """
    Parsed representation of a source file.
    """

    language: str
    nodes: list[CodeNode] = field(default_factory=list)