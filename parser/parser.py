from pathlib import Path

from tree_sitter_language_pack import get_parser

from parser.languages import detect_language
from parser.structure import CodeNode, CodeStructure


CLASS_NODE_TYPES = {
    "class_definition",
    "class_declaration",
    "class_specifier",
}

FUNCTION_NODE_TYPES = {
    "function_definition",
    "function_declaration",
    "function_item",
}

METHOD_NODE_TYPES = {
    "method_definition",
    "method_declaration",
}


def parse_file(file_path: str) -> CodeStructure:
    """
    Parse a source code file using Tree-sitter.
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

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    nodes = _extract_nodes(
        tree.root_node,
        source_code,
        inside_class=False
    )

    return CodeStructure(
        language=language,
        nodes=nodes
    )


def _extract_nodes(
    node,
    source_code: str,
    inside_class: bool = False
) -> list[CodeNode]:

    node_type = node.type

    # Class
    if node_type in CLASS_NODE_TYPES:

        class_node = CodeNode(
            type="class",
            name=_extract_node_name(node),
            start_line=node.start_point.row + 1,
            end_line=node.end_point.row + 1,
            content=_get_node_content(
                node,
                source_code
            ),
        )

        for child in node.children:

            child_nodes = _extract_nodes(
                child,
                source_code,
                inside_class=True
            )

            class_node.children.extend(
                child_nodes
            )

        return [class_node]

    # Function or method
    if node_type in FUNCTION_NODE_TYPES:

        code_type = (
            "method"
            if inside_class
            else "function"
        )

        return [
            CodeNode(
                type=code_type,
                name=_extract_node_name(node),
                start_line=node.start_point.row + 1,
                end_line=node.end_point.row + 1,
                content=_get_node_content(
                    node,
                    source_code
                ),
            )
        ]

    # Explicit method
    if node_type in METHOD_NODE_TYPES:

        return [
            CodeNode(
                type="method",
                name=_extract_node_name(node),
                start_line=node.start_point.row + 1,
                end_line=node.end_point.row + 1,
                content=_get_node_content(
                    node,
                    source_code
                ),
            )
        ]

    # Continue recursively through structural nodes
    nodes = []

    for child in node.children:

        child_nodes = _extract_nodes(
            child,
            source_code,
            inside_class
        )

        nodes.extend(child_nodes)

    return nodes


def _extract_node_name(node) -> str | None:

    for child in node.children:

        if child.type in {
            "identifier",
            "type_identifier",
            "field_identifier",
        }:
            return child.text.decode("utf-8")

    return None


def _get_node_content(
    node,
    source_code: str
) -> str:

    return source_code[
        node.start_byte:node.end_byte
    ]