"""
Import Audit Command Module

Audits and automatically fixes Python import statements for path consistency.
Parameterised to support multiple project structures and migration patterns.
"""

import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class ImportAuditCommand(Command):
    """
    Command for identifying and fixing broken or deprecated imports.
    
    Allows for dynamic mapping of legacy module roots to new unified prefixes.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "import-audit"

    @property
    def description(self) -> str:
        return "Audit and normalize repository imports (Parameterised)"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--fix", 
            action="store_true", 
            help="Automatically normalize deprecated import roots"
        )
        parser.add_argument(
            "--path", 
            default=".", 
            help="Directory to scan"
        )
        parser.add_argument(
            "--legacy-roots", 
            default="backend,core,utils",
            help="Comma-separated list of legacy roots to look for"
        )
        parser.add_argument(
            "--new-prefix", 
            default="src",
            help="The new prefix to apply to legacy roots"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the import audit/fix command."""
        root_dir = Path(args.path)
        legacy_list = [r.strip() for l in args.legacy_roots.split(",") for r in [l]]
        
        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(root_dir.absolute()))
            if not is_safe:
                print(f"Error: Security violation: {error}"); return 1

        print(f"🔍 Auditing imports in '{root_dir.absolute()}'...")
        print(f"   Targeting Legacy Roots: {legacy_list} -> Prefix: {args.new_prefix}")
        
        py_files = list(root_dir.rglob("*.py"))
        total_fixed = 0
        total_issues = 0

        for py_file in py_files:
            if "venv" in str(py_file) or ".iflow" in str(py_file): continue
                
            issues = self._audit_file(py_file, legacy_list, args.new_prefix)
            total_issues += len(issues)

            if args.fix and issues:
                if self._fix_file_imports(py_file, legacy_list, args.new_prefix):
                    total_fixed += 1

        print("\n--- Scan Complete ---")
        print(f"Total Issues Found: {total_issues}")
        if args.fix:
            print(f"Files Automatically Fixed: {total_fixed}")
            
        return 0

    def _audit_file(self, file_path: Path, legacy_roots: List[str], prefix: str) -> List[str]:
        """Detect legacy import patterns using dynamic roots."""
        issues = []
        roots_pattern = "|".join(legacy_roots)
        # Matches 'import X' or 'from X' where X is a legacy root not preceded by prefix
        pattern = re.compile(fr'^(?:import|from)\s+({roots_pattern})(?:\.|\s|$)')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if pattern.match(line.strip()):
                        issues.append(f"Line {i}: Legacy root detected")
        except Exception: pass
        return issues

    def _fix_file_imports(self, file_path: Path, legacy_roots: List[str], prefix: str) -> bool:
        """Surgically normalize imports using parameterised roots and prefix."""
        try:
            content = file_path.read_text(encoding='utf-8')
            roots_pattern = "|".join(legacy_roots)
            
            # 1. Transform 'import root' -> 'import prefix.root'
            new_content = re.sub(fr'^import\s+({roots_pattern})', fr'import {prefix}.\1', content, flags=re.M)
            
            # 2. Transform 'from root' -> 'from prefix.root'
            new_content = re.sub(fr'^from\s+({roots_pattern})', fr'from {prefix}.\1', new_content, flags=re.M)
            
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"  [FIXED] {file_path.name}")
                return True
        except Exception as e:
            print(f"  [ERROR] Failed to fix {file_path.name}: {e}")
            
        return False
