"""
Requirement checker module for constitutional analysis.

Implements various checkers for different aspects of code quality.
"""

from typing import List
from src.core.conflict_models import RiskLevel
from src.analysis.constitutional.violations import RequirementViolation


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
            violations.append(
                RequirementViolation(
                    rule_id="error-handling-001",
                    description="Try block without corresponding except block",
                    severity=RiskLevel.HIGH,
                )
            )

        # Check for bare except statements
        if "except:" in code:
            violations.append(
                RequirementViolation(
                    rule_id="error-handling-002",
                    description="Bare except statement found (except: without exception type)",
                    severity=RiskLevel.MEDIUM,
                )
            )

        # Check for pass in except blocks
        if "except" in code and "pass" in code:
            lines = code.split("\n")
            in_except_block = False
            for i, line in enumerate(lines):
                if "except" in line and ":" in line:
                    in_except_block = True
                elif in_except_block and line.strip() == "pass":
                    violations.append(
                        RequirementViolation(
                            rule_id="error-handling-003",
                            description="Empty except block with 'pass' statement",
                            severity=RiskLevel.MEDIUM,
                        )
                    )
                    in_except_block = False
                elif (
                    line.strip()
                    and not line.strip().startswith("#")
                    and in_except_block
                ):
                    in_except_block = False  # End of except block

        return violations


class TypeHintChecker(BaseChecker):
    """
    Checks for proper type hints in code.
    """

    def check(self, code: str) -> List[RequirementViolation]:
        violations = []

        # Check for function definitions without return type hints
        import re

        func_pattern = r"def\s+\w+\s*\([^)]*\)\s*:"
        funcs = re.findall(func_pattern, code)
        for func in funcs:
            if "->" not in func:
                violations.append(
                    RequirementViolation(
                        rule_id="type-hint-001",
                        description="Function missing return type hint",
                        severity=RiskLevel.MEDIUM,
                    )
                )

        return violations


class DocstringChecker(BaseChecker):
    """
    Checks for proper docstrings in code.
    """

    def check(self, code: str) -> List[RequirementViolation]:
        violations = []

        # Check for function definitions without docstrings
        import re

        func_pattern = r"def\s+(\w+)\s*\([^)]*\):"
        funcs = re.findall(func_pattern, code)
        for func in funcs:
            if '"""' not in code[code.find(func) : code.find(func) + 200]:
                violations.append(
                    RequirementViolation(
                        rule_id="docstring-001",
                        description=f"Function '{func}' missing docstring",
                        severity=RiskLevel.LOW,
                    )
                )

        return violations


class SecurityChecker(BaseChecker):
    """
    Checks for security issues in code.
    """

    def check(self, code: str) -> List[RequirementViolation]:
        violations = []

        # Check for eval/exec usage
        if "eval(" in code or "exec(" in code:
            violations.append(
                RequirementViolation(
                    rule_id="security-001",
                    description="Use of eval() or exec() detected",
                    severity=RiskLevel.CRITICAL,
                )
            )

        # Check for subprocess with shell=True
        if "shell=True" in code:
            violations.append(
                RequirementViolation(
                    rule_id="security-002",
                    description="subprocess with shell=True detected",
                    severity=RiskLevel.HIGH,
                )
            )

        # Check for hardcoded secrets
        import re

        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code):
                violations.append(
                    RequirementViolation(
                        rule_id="security-003",
                        description="Potential hardcoded secret detected",
                        severity=RiskLevel.CRITICAL,
                    )
                )

        return violations
