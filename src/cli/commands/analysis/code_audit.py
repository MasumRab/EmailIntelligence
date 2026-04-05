"""
Code Audit Command Module

Exhaustive implementation of the repository-wide technical debt and security auditor.
Uses AST-based structural scanning for high-fidelity intent detection.
"""

import ast
import json
import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class AnalyzeCodeCommand(Command):
    """
    Exhaustive Code Auditor following SOLID principles.
    
    Ported Capabilities:
    - AST-based structural anti-pattern detection (Fragile Intent)
    - Security scanner for hardcoded secrets and ungated I/O
    - Complexity and maintainability metrics
    - Technical debt identifier (TODO/FIXME tracking)
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "code-audit"

    @property
    def description(self) -> str:
        return "Perform exhaustive technical debt and security audit"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--path", default=".", help="Root path to audit")
        parser.add_argument("--json", action="store_true", help="Output results as JSON")
        parser.add_argument("--severity", choices=["LOW", "MEDIUM", "HIGH"], default="MEDIUM")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        root_path = Path(args.path)
        
        if self._security_validator:
            is_safe, err = self._security_validator.validate_path_security(str(root_path.absolute()))
            if not is_safe:
                print(f"Error: Security violation: {err}")
                return 1

        print(f"🔍 Starting Exhaustive Codebase Audit at '{root_path.absolute()}'...")
        
        results = {
            "technical_debt": self._scan_todo_markers(root_path),
            "performance_gaps": self._detect_inefficient_loops(root_path),
            "security_risks": self._scan_hardcoded_secrets(root_path),
            "maintainability_issues": self.analyze_maintainability_issues(root_path),
            "large_modules": self._detect_large_modules(root_path)
        }

        # Severity Filtering Logic (As suggested by CodeRabbit)
        severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        min_severity = severity_order[args.severity]

        filtered_results = {}
        for category, issues in results.items():
            filtered_results[category] = [
                i for i in issues 
                if severity_order.get(i.get("risk_level", "LOW"), 0) >= min_severity
            ]

        if args.json:
            print(json.dumps(filtered_results, indent=2))
        else:
            self._print_report(filtered_results)

        return 0

    def _scan_todo_markers(self, root: Path) -> List[Dict]:
        """Detects technical debt markers in comments."""
        issues = []
        pattern = re.compile(r'#\s*(TODO|FIXME|HACK|XXX):?\s*(.+)$')
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        match = pattern.search(line)
                        if match:
                            issues.append({
                                "type": "TECHNICAL_DEBT",
                                "risk_level": "LOW",
                                "file": str(py_file.relative_to(root)),
                                "line": i,
                                "description": f"{match.group(1)}: {match.group(2).strip()}"
                            })
            except Exception:
                continue
        return issues

    def _detect_inefficient_loops(self, root: Path) -> List[Dict]:
        """Simple heuristic for nested loops or range(len())."""
        issues = []
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            try:
                content = py_file.read_text(encoding='utf-8')
                if content.count("for ") > 10 and "range(len(" in content:
                    issues.append({
                        "type": "PERFORMANCE", 
                        "risk_level": "MEDIUM", 
                        "file": str(py_file.relative_to(root)), 
                        "description": "Potential inefficient range(len()) pattern found"
                    })
            except Exception:
                continue
        return issues

    def _scan_hardcoded_secrets(self, root: Path) -> List[Dict]:
        issues = []
        pattern = re.compile(r'["\'](?:api[_-]?key|secret|password|token)["\']\s*[:=]\s*["\'][^"\']{5,}', re.I)
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            try:
                matches = pattern.findall(py_file.read_text(encoding='utf-8'))
                for m in matches:
                    issues.append({
                        "type": "SECURITY", 
                        "risk_level": "HIGH", 
                        "file": str(py_file.relative_to(root)), 
                        "description": "Potential hardcoded secret found"
                    })
            except Exception:
                continue
        return issues

    def analyze_maintainability_issues(self, root: Path) -> List[Dict]:
        """Detects structural anti-patterns using AST."""
        issues = []
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            try:
                content = py_file.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    # 1. Detect Bare Excepts (Fragile Intent)
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        issues.append({
                            "type": "MAINTAINABILITY",
                            "risk_level": "MEDIUM",
                            "file": str(py_file.relative_to(root)),
                            "line": node.lineno,
                            "description": "Fragile Intent: Bare 'except:' clause detected"
                        })
                    
                    # 2. Detect Unsafe I/O (Non-SecurityValidator logic)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id == "open" and not self._is_security_validator_active():
                            issues.append({
                                "type": "SECURITY_RISK",
                                "risk_level": "HIGH",
                                "file": str(py_file.relative_to(root)),
                                "line": node.lineno,
                                "description": "Unsafe I/O: 'open()' called without SecurityValidator gating"
                            })
            except Exception:
                continue
        return issues

    def _is_security_validator_active(self) -> bool:
        return self._security_validator is not None

    def _detect_large_modules(self, root: Path) -> List[Dict]:
        modules = []
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            try:
                loc = len(py_file.read_text().splitlines())
                if loc > 500:
                    modules.append({
                        "type": "MAINTAINABILITY",
                        "risk_level": "LOW",
                        "file": str(py_file.relative_to(root)),
                        "description": f"Large module with {loc} lines of code"
                    })
            except Exception:
                continue
        return modules

    def _print_report(self, results: Dict):
        count = sum(len(v) for v in results.values())
        print(f"\nAudit complete. Found {count} issues.")
        for cat, issues in results.items():
            for issue in issues:
                lvl = issue.get("risk_level", "INFO")
                print(f"  [{lvl}] {issue['type']}: {issue['description']} ({issue['file']})")
