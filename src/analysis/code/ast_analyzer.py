
"""
AST-based code analysis module.
"""

import ast
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass

@dataclass
class CodeStructure:
    """Represents the structure of analyzed code."""
    functions: List[str]
    classes: List[str]
    imports: List[str]
    docstrings: Dict[str, str]
    has_type_hints: bool
    has_error_handling: bool

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
            return CodeStructure([], [], [], {}, False, False)
            
        functions = []
        classes = []
        imports = []
        docstrings = {}
        has_type_hints = False
        has_error_handling = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
                if ast.get_docstring(node):
                    docstrings[node.name] = ast.get_docstring(node)
                if node.returns or any(arg.annotation for arg in node.args.args):
                    has_type_hints = True
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
                if ast.get_docstring(node):
                    docstrings[node.name] = ast.get_docstring(node)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                else:
                    module = node.module or ""
                    for name in node.names:
                        imports.append(f"{module}.{name.name}")
            elif isinstance(node, ast.Try):
                has_error_handling = True
                
        return CodeStructure(
            functions=functions,
            classes=classes,
            imports=imports,
            docstrings=docstrings,
            has_type_hints=has_type_hints,
            has_error_handling=has_error_handling
        )
