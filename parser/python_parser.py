import ast

def parse_python_code(source_code: str) -> ast.AST:
    """
    Parse Python source code into an Abstract Syntax Tree (AST).

    Args:
        source_code: A string containing Python source code.

    Returns:
        An AST object representing the parsed code.
    """
    try:
        return ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in source code: {e}")




def extract_code_structure(tree: ast.AST) -> dict:
    """
    Extract high-level code structure from a Python AST.

    Args:
        tree: Parsed Python AST.

    Returns:
        A dictionary containing imports, classes, and functions.
    """

    structure = {
        "imports": [],
        "classes": [],
        "functions": [],
    }

    for node in tree.body:

        if isinstance(node, ast.Import):
            for alias in node.names:
                structure["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                structure["imports"].append(
                    f"{node.module}.{alias.name}"
                )

        elif isinstance(node, ast.ClassDef):
            methods = []

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(item.name)

            structure["classes"].append({
                "name": node.name,
                "methods": methods,
            })

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            structure["functions"].append(node.name)

    return structure
    