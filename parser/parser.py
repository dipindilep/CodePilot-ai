from pathlib import Path

from tree_sitter_language_pack import get_parser

from parser.languages import detect_language
from parser.structure import CodeNode, CodeStructure


def parse_file(file_path: str) -> CodeStructure:
    """
    Parse a source code file using Tree-sitter.

    Args:
        file_path: Path to the source file.

    Returns:
        A language-independent CodeStructure.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File '{file_path}' does not exist."
        )

    if not path.is_file():
        raise IsADirectoryError(
            f"'{file_path}' is not a file."
        )

    language = detect_language(file_path)

    if language is None:
        raise ValueError(
            f"Unsupported programming language: '{path.suffix}'"
        )

    source_code = path.read_text(encoding="utf-8")

    parser = get_parser(language)

    tree = parser.parse(source_code.encode("utf-8"))

    root_node = tree.root_node

    structure = CodeStructure(
        language=language
    )

    for node in root_node.children:

        code_node = _convert_node(
            node,
            source_code
        )

        if code_node is not None:
            structure.nodes.append(code_node)

    return structure


def _convert_node(
    node,
    source_code: str
) -> CodeNode | None:
    """
    Convert a Tree-sitter node into our common CodeNode structure.
    """

    node_type = node.type

    if node_type in {
        "class_definition",
        "class_declaration",
        "function_definition",
        "function_declaration",
        "method_definition",
        "method_declaration",
    }:

        name = _extract_node_name(node)

        return CodeNode(
            type=_normalise_node_type(node_type),
            name=name,
            start_line=node.start_point.row + 1,
            end_line=node.end_point.row + 1,
            content=source_code[
                node.start_byte:node.end_byte
            ],
        )

    return None


def _extract_node_name(node) -> str | None:
    """
    Extract a name from common Tree-sitter declaration nodes.
    """

    for child in node.children:

        if child.type in {
            "identifier",
            "type_identifier",
        }:
            return child.text.decode("utf-8")

    return None


def _normalise_node_type(node_type: str) -> str:

    if "class" in node_type:
        return "class"

    if "method" in node_type:
        return "method"

    if "function" in node_type:
        return "function"

    return "unknown"