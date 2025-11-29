
"""
Requirement checking module for Constitutional Analysis.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from ...core.models import ValidationResult, ValidationStatus
from ..code.ast_analyzer import ASTAnalyzer

@dataclass
class RequirementViolation:
    """Represents a violation of a constitutional requirement."""
    rule_id: str
    description: str
    severity: str
    file_path: str
    line_number: Optional[int] = None

class BaseChecker(ABC):
    """Abstract base class for requirement checkers."""
    
    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    @abstractmethod
    def check(self, code: str, file_path: str, context: Dict[str, Any] = None) -> List[RequirementViolation]:
        """Check code against requirements."""
        pass

class ErrorHandlingChecker(BaseChecker):
    """
    Checks for proper error handling (try/except blocks).
    Corresponds to 'error_recovery_procedures' rule.
    """
    
    def check(self, code: str, file_path: str, context: Dict[str, Any] = None) -> List[RequirementViolation]:
        violations = []
        structure = self.ast_analyzer.analyze_structure(code)
        
        # If file has functions but no error handling
        if structure.functions and not structure.has_error_handling:
            violations.append(RequirementViolation(
                rule_id="error_recovery_procedures",
                description=f"File {file_path} contains functions but no error handling (try/except).",
                severity="major",
                file_path=file_path
            ))
            
        return violations

class TypeHintChecker(BaseChecker):
    """
    Checks for type hints in function definitions.
    Corresponds to 'quality_gates_integration' (implied code quality).
    """
    
    def check(self, code: str, file_path: str, context: Dict[str, Any] = None) -> List[RequirementViolation]:
        violations = []
        structure = self.ast_analyzer.analyze_structure(code)
        
        if structure.functions and not structure.has_type_hints:
            violations.append(RequirementViolation(
                rule_id="type_hints_required",
                description=f"File {file_path} contains functions without type hints.",
                severity="major",
                file_path=file_path
            ))
            
        return violations

class DocstringChecker(BaseChecker):
    """
    Checks for docstrings in functions and classes.
    Corresponds to 'documentation_requirements' rule.
    """
    
    def check(self, code: str, file_path: str, context: Dict[str, Any] = None) -> List[RequirementViolation]:
        violations = []
        structure = self.ast_analyzer.analyze_structure(code)
        
        missing_docstrings = []
        for func in structure.functions:
            if func not in structure.docstrings:
                missing_docstrings.append(f"function '{func}'")
                
        for cls in structure.classes:
            if cls not in structure.docstrings:
                missing_docstrings.append(f"class '{cls}'")
                
        if missing_docstrings:
            violations.append(RequirementViolation(
                rule_id="documentation_requirements",
                description=f"Missing docstrings in {file_path}: {', '.join(missing_docstrings)}",
                severity="major",
                file_path=file_path
            ))
            
        return violations

class SecurityChecker(BaseChecker):
    """
    Checks for basic security issues (e.g., hardcoded secrets).
    Corresponds to 'security_considerations' rule.
    """
    
    def check(self, code: str, file_path: str, context: Dict[str, Any] = None) -> List[RequirementViolation]:
        violations = []
        
        # Very basic check for hardcoded secrets (placeholder for more advanced scanning)
        # In a real implementation, we'd use a tool like bandit or detect-secrets
        dangerous_terms = ["password =", "secret =", "api_key =", "token ="]
        
        for i, line in enumerate(code.splitlines()):
            for term in dangerous_terms:
                if term in line and "os.getenv" not in line and "config" not in line:
                     violations.append(RequirementViolation(
                        rule_id="security_considerations",
                        description=f"Potential hardcoded secret found: '{term.strip()}'",
                        severity="critical",
                        file_path=file_path,
                        line_number=i + 1
                    ))
        
        return violations
