"""
Requirement checker module for constitutional analysis.

Implements various checkers for different aspects of code quality.
"""

from typing import List
from ..core.conflict_models import RiskLevel
from .analyzer import RequirementViolation


class BaseChecker:
    """
    Base class for all requirement checkers.
    """
    
    def check(self, code: str) -> List[RequirementViolation]:
        """
        Check the code for violations.
        
        Args:
            code: The code to check
            
        Returns:
            List of violations found
        """
        raise NotImplementedError("Subclasses must implement the check method")


class ErrorHandlingChecker(BaseChecker):
    """
    Checks for proper error handling in code.
    """
    
    def check(self, code: str) -> List[RequirementViolation]:
        violations = []
        
        # Check for try/except blocks
        if "try:" in code and "except" not in code:
            violations.append(RequirementViolation(
                rule_id="error-handling-001",
                description="Try block without corresponding except block",
                severity=RiskLevel.HIGH
            ))
        
        # Check for bare except statements
        if "except:" in code:
            violations.append(RequirementViolation(
                rule_id="error-handling-002",
                description="Bare except statement found (except: without exception type)",
                severity=RiskLevel.MEDIUM
            ))
        
        # Check for pass in except blocks
        if "except" in code and "pass" in code:
            lines = code.split('\n')
            in_except_block = False
            for i, line in enumerate(lines):
                if 'except' in line and ':' in line:
                    in_except_block = True
                elif in_except_block and line.strip() == 'pass':
                    violations.append(RequirementViolation(
                        rule_id="error-handling-003",
                        description="Empty except block with 'pass' statement",
                        severity=RiskLevel.MEDIUM
                    ))
                    in_except_block = False
                elif line.strip() and not line.strip().startswith('#') and in_except_block:
                    in_except_block = False  # End of except block
        
        return violations


class TypeHintChecker(BaseChecker):
    """
    Checks for proper type hints in code.
    """
    
    def check(self, code: str) -> List[RequirementViolation]:
        violations = []
        
        # Check for function definitions without type hints
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and '->' not in line and '(' in line:
                violations.append(RequirementViolation(
                    rule_id="type-hint-001",
                    description=f"Function definition without return type hint at line {i+1}",
                    severity=RiskLevel.MEDIUM
                ))
        
        return violations


class DocstringChecker(BaseChecker):
    """
    Checks for proper docstrings in code.
    """
    
    def check(self, code: str) -> List[RequirementViolation]:
        violations = []
        
        lines = code.split('\n')
        in_function = False
        has_docstring = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for function definition
            if stripped.startswith('def '):
                if in_function and not has_docstring:
                    violations.append(RequirementViolation(
                        rule_id="docstring-001",
                        description=f"Function without docstring at line {i}",
                        severity=RiskLevel.MEDIUM
                    ))
                
                in_function = True
                has_docstring = False
            elif in_function and ('"""' in stripped or "'''" in stripped):
                has_docstring = True
            elif in_function and stripped and not stripped.startswith('#'):
                if not has_docstring:
                    violations.append(RequirementViolation(
                        rule_id="docstring-001",
                        description=f"Function without docstring",
                        severity=RiskLevel.MEDIUM
                    ))
                in_function = False
                has_docstring = False
        
        # Check the last function
        if in_function and not has_docstring:
            violations.append(RequirementViolation(
                rule_id="docstring-001",
                description="Last function without docstring",
                severity=RiskLevel.MEDIUM
            ))
        
        return violations


class SecurityChecker(BaseChecker):
    """
    Checks for security-related issues in code.
    """
    
    def check(self, code: str) -> List[RequirementViolation]:
        violations = []
        
        # Check for potential SQL injection vulnerabilities
        dangerous_patterns = [
            ("eval(", "Use of eval() is dangerous and should be avoided", RiskLevel.CRITICAL),
            ("exec(", "Use of exec() is dangerous and should be avoided", RiskLevel.CRITICAL),
            ("os.system(", "Use of os.system() with dynamic input can be dangerous", RiskLevel.HIGH),
            ("subprocess.call(", "Direct use of subprocess with dynamic input can be dangerous", RiskLevel.MEDIUM),
        ]
        
        for pattern, description, severity in dangerous_patterns:
            if pattern in code:
                violations.append(RequirementViolation(
                    rule_id=f"security-{severity.value}-001",
                    description=description,
                    severity=severity
                ))
        
        # Check for hardcoded passwords or secrets
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if ('password' in line.lower() or 'secret' in line.lower() or 'key' in line.lower()) and ('=' in line) and ('"' in line or "'" in line):
                # Check if it's a variable assignment with a string value
                if ('password' in line.lower() or 'secret' in line.lower() or 'key' in line.lower()) and ('"' in line or "'" in line):
                    violations.append(RequirementViolation(
                        rule_id="security-secret-001",
                        description=f"Potential hardcoded secret found at line {i+1}",
                        severity=RiskLevel.HIGH
                    ))
        
        return violations