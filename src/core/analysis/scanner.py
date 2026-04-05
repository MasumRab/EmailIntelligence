import ast
from typing import List
from pathlib import Path
from src.core.models.analysis import Violation, ConstitutionalRule

class ASTScanner(ast.NodeVisitor):
    """Scans python code for architectural violations."""
    
    def __init__(self, rules: List[ConstitutionalRule]):
        self.rules = rules
        self.violations: List[Violation] = []
        self.current_file: Optional[Path] = None

    def scan_file(self, file_path: Path) -> List[Violation]:
        self.current_file = file_path
        content = file_path.read_text()
        try:
            tree = ast.parse(content)
            self.visit(tree)
        except SyntaxError:
            # Report syntax errors as critical violations if needed
            pass
        return self.violations

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Example rule: No function definitions in scripts/ directory
        if "scripts/" in str(self.current_file):
            self.violations.append(Violation(
                rule_id="IX.1",
                severity="CRITICAL",
                file_path=str(self.current_file),
                line_no=node.lineno,
                message=f"Logic (Function '{node.name}') detected in script file. Logic must reside in src/core/."
            ))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if "scripts/" in str(self.current_file):
            self.violations.append(Violation(
                rule_id="IX.1",
                severity="CRITICAL",
                file_path=str(self.current_file),
                line_no=node.lineno,
                message=f"Logic (Class '{node.name}') detected in script file. Logic must reside in src/core/."
            ))
        self.generic_visit(node)
