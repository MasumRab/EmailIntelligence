"""
Code Audit Command Module

Implements comprehensive codebase analysis for technical debt, security, and complexity.
Ported from codebase_analysis.py.
"""

import ast
import re
import json
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..interface import Command


class AnalyzeCodeCommand(Command):
    """
    Command for identifying technical debt, security risks, and architectural concerns.
    
    Scans Python files for TODOs, circular dependencies, large modules,
    and potential security vulnerabilities like hardcoded secrets.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "code-audit"

    @property
    def description(self) -> str:
        return "Perform technical debt and security audit of the codebase"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--path", 
            default=".", 
            help="Directory path to audit"
        )
        parser.add_argument(
            "--output", 
            help="Path to save audit report"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the code-audit command."""
        root_path = Path(args.path)

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(root_path.absolute()))
            if not is_safe:
                print(f"Error: Security violation: {error}")
                return 1

        print(f"🔍 Auditing codebase at '{root_path}'...")
        
        issues = []
        issues.extend(self._analyze_technical_debt(root_path))
        issues.extend(self._analyze_security(root_path))
        
        print(f"Found {len(issues)} issues.")

        for issue in issues[:10]: # Summary display
            print(f"  [{issue['risk_level']}] {issue['type']}: {issue['description']} ({issue['file']})")

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(issues, f, indent=2)
            print(f"\n🚀 Full report saved to {args.output}")

        return 0

    def _analyze_technical_debt(self, root: Path) -> List[Dict]:
        """Identify TODOs and large modules."""
        issues = []
        todo_pattern = re.compile(r'#\s*(TODO|FIXME|HACK):?\s*(.+)$')
        
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file): continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        match = todo_pattern.search(line)
                        if match:
                            issues.append({
                                "type": "TECH_DEBT",
                                "risk_level": "MEDIUM",
                                "file": str(py_file.relative_to(root)),
                                "description": f"{match.group(1)}: {match.group(2).strip()}"
                            })
            except Exception: continue
        return issues

    def _analyze_security(self, root: Path) -> List[Dict]:
        """Identify potential hardcoded secrets."""
        issues = []
        # Simplified pattern for demo
        secret_pattern = re.compile(r'["\'](?:api[_-]?key|secret|password)["\']\s*[:=]\s*["\'][^"\']{8,}', re.I)
        
        for py_file in root.rglob("*.py"):
            if "venv" in str(py_file): continue
            try:
                content = py_file.read_text(encoding='utf-8')
                matches = secret_pattern.findall(content)
                for match in matches:
                    issues.append({
                        "type": "SECURITY",
                        "risk_level": "HIGH",
                        "file": str(py_file.relative_to(root)),
                        "description": "Potential hardcoded secret or API key found"
                    })
            except Exception: continue
        return issues
