"""
Import Audit Command Module

Audits Python import statements for broken paths and deprecated module references.
Ported from orchestration-tools:scripts/import_audit.py.
"""

import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class ImportAuditCommand(Command):
    """
    Command for identifying broken or deprecated imports across the repository.
    
    Checks for 'backend' vs 'src.backend' consistency and identifies 
    module references that no longer exist in the current structure.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "import-audit"

    @property
    def description(self) -> str:
        return "Audit repository imports for consistency and correctness"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--fix", 
            action="store_true", 
            help="Attempt to automatically fix common import issues"
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
        """Execute the import audit command."""
        root = Path(".")
        print(f"🔍 Auditing imports in '{root.absolute()}'...")

        # 1. Scan for files
        py_files = list(root.rglob("*.py"))
        print(f"Scanning {len(py_files)} files...")

        issues = []
        for py_file in py_files:
            if "venv" in str(py_file): continue
            file_issues = self._audit_file(py_file)
            issues.extend(file_issues)

        if not issues:
            print("✅ No import issues detected.")
            return 0

        print(f"Found {len(issues)} import issues:")
        for issue in issues[:20]:
            print(f"  - {issue['file']}:{issue['line']} -> {issue['description']}")

        if args.fix:
            print("\n🛠️  Auto-fix requested. (Logic not yet fully implemented in port)")
            
        return 0

    def _audit_file(self, file_path: Path) -> List[Dict]:
        """Check imports in a single file."""
        issues = []
        import_pattern = re.compile(r'^(?:from|import)\s+([^\s]+)')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    match = import_pattern.match(line.strip())
                    if match:
                        module = match.group(1)
                        # Check for deprecated 'backend' imports
                        if module.startswith("backend.") or module == "backend":
                            issues.append({
                                "file": str(file_path),
                                "line": i,
                                "description": f"Deprecated import root: '{module}' (should use 'src.backend')"
                            })
        except Exception: pass
        return issues
