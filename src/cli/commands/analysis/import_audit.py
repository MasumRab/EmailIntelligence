"""
Import Audit Command Module

Audits and automatically fixes Python import statements for path consistency.
Ported from orchestration-tools with enhanced --fix logic for consolidation.
"""

import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class ImportAuditCommand(Command):
    """
    Command for identifying and fixing broken or deprecated imports.
    
    This tool ensures that all imports follow the 'src.' prefix standard
    required for the consolidated modular architecture.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "import-audit"

    @property
    def description(self) -> str:
        return "Audit and normalize repository imports"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--fix", 
            action="store_true", 
            help="Automatically normalize deprecated import roots (backend -> src.backend)"
        )
        parser.add_argument(
            "--path", 
            default=".", 
            help="Directory to scan"
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
        """Execute the import audit/fix command."""
        root_dir = Path(args.path)
        
        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(root_dir.absolute()))
            if not is_safe:
                print(f"Error: Security violation: {error}")
                return 1

        print(f"🔍 Scanning for import issues in '{root_dir.absolute()}'...")
        
        py_files = list(root_dir.rglob("*.py"))
        total_fixed = 0
        total_issues = 0

        for py_file in py_files:
            if "venv" in str(py_file) or ".iflow" in str(py_file):
                continue
                
            issues = self._audit_file(py_file)
            total_issues += len(issues)

            if args.fix and issues:
                if self._fix_file_imports(py_file):
                    total_fixed += 1

        print(f"\n--- Scan Complete ---")
        print(f"Total Issues Found: {total_issues}")
        if args.fix:
            print(f"Files Automatically Fixed: {total_fixed}")
            
        return 0

    def _audit_file(self, file_path: Path) -> List[str]:
        """Detect legacy import patterns."""
        issues = []
        # Matches 'import backend' or 'from backend' (not src.backend)
        pattern = re.compile(r'^(?:import|from)\s+(backend|core|utils)(?:\.|\s|$)')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if pattern.match(line.strip()):
                        issues.append(f"Line {i}: Legacy root detected")
        except Exception:
            pass
        return issues

    def _fix_file_imports(self, file_path: Path) -> bool:
        """Surgically normalize imports in a file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 1. Transform 'import backend' -> 'import src.backend'
            new_content = re.sub(r'^import\s+(backend|core|utils)', r'import src.\1', content, flags=re.M)
            
            # 2. Transform 'from backend' -> 'from src.backend'
            new_content = re.sub(r'^from\s+(backend|core|utils)', r'from src.\1', new_content, flags=re.M)
            
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"  [FIXED] {file_path.name}")
                return True
        except Exception as e:
            print(f"  [ERROR] Failed to fix {file_path.name}: {e}")
            
        return False
