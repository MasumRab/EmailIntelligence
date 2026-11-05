"""
AST-based code analysis module.
"""

import ast
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class FunctionMetadata:
    name: str
    has_docstring: bool
    has_type_hints: bool
    has_error_handling: bool


@dataclass
class CodeStructure:
    """Represents the structure of analyzed code."""

    functions: List[str]
    classes: List[str]
    imports: List[str]
    docstrings: Dict[str, str]
    has_type_hints: bool
    has_error_handling: bool
    function_metadata: Dict[str, FunctionMetadata]


class ASTAnalyzer:
    """
    Analyzes Python code using the Abstract Syntax Tree (AST).
    """

    def parse_code(self, code: str) -> Optional[ast.AST]:
        """Parse code string into AST."""
        try:
            return ast.parse(code)
        except SyntaxError:
            return None

    def analyze_structure(self, code: str) -> CodeStructure:
        """
        Analyze the structure of the code (functions, classes, etc.).
        """
        tree = self.parse_code(code)
        if not tree:
            return CodeStructure([], [], [], {}, False, False, {})

        functions = []
        classes = []
        imports = []
        docstrings = {}
        has_type_hints = False
        has_error_handling = False
        function_metadata = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

                # Check docstring
                func_has_docstring = False
                if ast.get_docstring(node):
                    docstrings[node.name] = ast.get_docstring(node)
                    func_has_docstring = True

                # Check type hints
                func_has_type_hints = False
                if node.returns or any(arg.annotation for arg in node.args.args):
                    has_type_hints = True
                    func_has_type_hints = True

                # Check error handling in function body
                func_has_error_handling = False
                for child in ast.walk(node):
                    if isinstance(child, ast.Try):
                        has_error_handling = True
                        func_has_error_handling = True
                        break

                function_metadata[node.name] = FunctionMetadata(
                    name=node.name,
                    has_docstring=func_has_docstring,
                    has_type_hints=func_has_type_hints,
                    has_error_handling=func_has_error_handling,
                )

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
                if ast.get_docstring(node):
                    docstrings[node.name] = ast.get_docstring(node)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                else:
                    for name in node.names:
                        # Store the imported name as it appears in the namespace
                        imported_name = name.asname if name.asname else name.name
                        imports.append(imported_name)
            elif isinstance(node, ast.Try):
                has_error_handling = True

        return CodeStructure(
            functions=functions,
            classes=classes,
            imports=imports,
            docstrings=docstrings,
            has_type_hints=has_type_hints,
            has_error_handling=has_error_handling,
            function_metadata=function_metadata,
        )

    def are_equivalent(self, code1: str, code2: str) -> bool:
        """
        Check if two code snippets are semantically equivalent (ignoring formatting).
        """
        try:
            tree1 = self.parse_code(code1)
            tree2 = self.parse_code(code2)

            if not tree1 or not tree2:
                return False

            # Compare AST dumps ignoring attributes (like line numbers)
            return ast.dump(tree1, include_attributes=False) == ast.dump(
                tree2, include_attributes=False
            )
        except Exception:
            return False
