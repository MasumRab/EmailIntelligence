#!/usr/bin/env python3
"""
import_audit.py - Audit and fix import statements

Usage:
    python3 import_audit.py <repo_root> [--auto-fix]

Example:
    python3 import_audit.py /home/masum/github/EmailIntelligence
    python3 import_audit.py . --auto-fix
"""

import ast
import sys
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class ImportIssue:
    file: str
    line_number: int
    import_statement: str
    issue_type: str
    suggested_fix: str
    severity: str  # ERROR, WARNING, INFO


class ImportAuditor:
    def __init__(self, repo_root: str, auto_fix: bool = False):
        self.repo_root = Path(repo_root)
        self.issues: List[ImportIssue] = []
        self.auto_fix = auto_fix
        self.known_modules: Dict[str, Set[str]] = {
            "src": set(),
            "backend": set(),
            "setup": set(),
            "root": set(),
        }
        self.fixes_applied = 0

    def scan_repository(self) -> List[ImportIssue]:
        """Scan entire repository for import issues"""
        print("=== Scanning Repository ===")
        print(f"Repository: {self.repo_root}")
        print("")

        # Build module list from current structure
        self._build_module_list()

        # Scan all Python files
        for py_file in self.repo_root.rglob("*.py"):
            if "venv" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            self._scan_file(py_file)

        return self.issues

    def _build_module_list(self):
        """Build list of known modules from directory structure"""
        print("Building module list...")

        for src_dir in ["src", "backend", "setup"]:
            src_path = self.repo_root / src_dir
            if src_path.exists():
                for py_file in src_path.rglob("*.py"):
                    if py_file.stem == "__init__":
                        continue
                    module_path = py_file.relative_to(self.repo_root).with_suffix("")
                    module_name = str(module_path).replace("/", ".")
                    self.known_modules[src_dir].add(module_name)

        # Also check root-level Python files
        for py_file in self.repo_root.glob("*.py"):
            if py_file.stem not in ["__init__", "setup"]:
                self.known_modules["root"].add(py_file.stem)

        print(f"  Found {sum(len(s) for s in self.known_modules.values())} modules")

    def _scan_file(self, file_path: Path):
        """Scan a single file for import issues"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
        except (UnicodeDecodeError, FileNotFoundError):
            return

        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()

            if not line_stripped.startswith(("import ", "from ")):
                continue

            self._check_import(file_path, line_num, line_stripped)

    def _check_import(self, file_path: Path, line_num: int, import_stmt: str):
        """Check an import statement for issues"""

        # Parse the import statement
        if import_stmt.startswith("from "):
            parts = import_stmt.split()
            if len(parts) >= 2:
                module = parts[1]
                # Handle 'from src.core import X'
                if module in ["src", "backend", "setup"]:
                    if len(parts) >= 4 and parts[2] == "import":
                        submodule = parts[3]
                        full_module = f"{module}.{submodule}"
                    else:
                        full_module = module
                else:
                    full_module = module
            else:
                return
        elif import_stmt.startswith("import "):
            parts = import_stmt.split()
            if len(parts) >= 2:
                module = parts[1].split(".")[0]
                full_module = module
            else:
                return
        else:
            return

        # Check if module exists
        module_exists = self._module_exists(full_module)

        if not module_exists:
            # Try to find similar modules
            similar = self._find_similar_modules(full_module)

            issue = ImportIssue(
                file=str(file_path.relative_to(self.repo_root)),
                line_number=line_num,
                import_statement=import_stmt,
                issue_type="BROKEN_IMPORT",
                suggested_fix=self._suggest_fix(full_module, similar),
                severity="ERROR",
            )
            self.issues.append(issue)

        # Check for common issues
        if "backend.python_backend" in import_stmt and "src.backend" not in import_stmt:
            # Old backend path used
            issue = ImportIssue(
                file=str(file_path.relative_to(self.repo_root)),
                line_number=line_num,
                import_statement=import_stmt,
                issue_type="DEPRECATED_PATH",
                suggested_fix="Update 'backend.python_backend' to 'src.backend.python_backend'",
                severity="WARNING",
            )
            self.issues.append(issue)

        if (
            "from core import" in import_stmt
            and "from src.core import" not in import_stmt
        ):
            # Missing src prefix
            issue = ImportIssue(
                file=str(file_path.relative_to(self.repo_root)),
                line_number=line_num,
                import_statement=import_stmt,
                issue_type="MISSING_PREFIX",
                suggested_fix="Add 'src.' prefix: 'from src.core import'",
                severity="WARNING",
            )
            self.issues.append(issue)

    def _module_exists(self, module: str) -> bool:
        """Check if a module exists in the repository"""
        # Check known modules
        for module_set in self.known_modules.values():
            if module in module_set:
                return True

        # Check if file exists
        module_path = module.replace(".", "/")
        for ext in [".py", "/__init__.py"]:
            if (self.repo_root / f"{module_path}{ext}").exists():
                return True

        return False

    def _find_similar_modules(self, module: str) -> List[str]:
        """Find similar module names"""
        similar = []

        # Check for common patterns
        common_patterns = {
            "core": ["src.core", "core"],
            "backend": ["src.backend", "backend"],
            "python_backend": ["backend.python_backend", "src.backend.python_backend"],
            "context_control": ["src.context_control", "context_control"],
            "agent_context": [
                "src.context_control.agent_context",
                "context_control.agent_context",
            ],
            "security": ["src.core.security", "core.security"],
            "database": ["src.core.database", "core.database"],
        }

        for pattern, alternatives in common_patterns.items():
            if module in alternatives:
                similar = [alt for alt in alternatives if alt != module]
                break

        # Fuzzy match against known modules
        module_parts = module.split(".")
        for part in reversed(module_parts):
            for module_set in self.known_modules.values():
                for known_module in module_set:
                    if part in known_module and known_module not in similar:
                        similar.append(known_module)

        return similar[:5]

    def _suggest_fix(self, module: str, similar: List[str]) -> str:
        """Suggest a fix for a broken import"""
        if similar:
            return f"Possibly meant: {' or '.join(similar)}"
        return f"Module '{module}' not found - manual review required"

    def generate_report(self) -> str:
        """Generate audit report"""
        report = []
        report.append("# Import Audit Report")
        report.append(f"")
        report.append(f"Repository: {self.repo_root}")
        report.append(f"Total issues found: {len(self.issues)}")
        report.append(f"")

        # Group by severity
        errors = [i for i in self.issues if i.severity == "ERROR"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]
        infos = [i for i in self.issues if i.severity == "INFO"]

        # Summary
        report.append(f"## Summary")
        report.append(f"- Errors (must fix): {len(errors)}")
        report.append(f"- Warnings (should review): {len(warnings)}")
        report.append(f"- Info (suggestions): {len(infos)}")
        report.append(f"")

        if errors:
            report.append("## ERRORS (Must Fix)")
            report.append(f"")
            for issue in errors:
                report.append(f"### {issue.file}:{issue.line_number}")
                report.append(f"")
                report.append(f"```python")
                report.append(f"{issue.import_statement}")
                report.append(f"```")
                report.append(f"")
                report.append(f"**Fix:** {issue.suggested_fix}")
                report.append(f"")
                report.append(f"---")
                report.append(f"")

        if warnings:
            report.append("## WARNINGS (Should Review)")
            report.append(f"")
            for issue in warnings:
                report.append(
                    f"- **{issue.file}:{issue.line_number}** - {issue.import_statement}"
                )
                report.append(f"  {issue.suggested_fix}")
            report.append(f"")

        if infos:
            report.append("## INFO (Suggestions)")
            for issue in infos:
                report.append(
                    f"- {issue.file}:{issue.line_number} - {issue.import_statement}"
                )

        return "\n".join(report)

    def auto_fix_simple_issues(self):
        """Automatically fix simple issues"""
        print("\n=== Auto-Fixing Simple Issues ===")

        fixes_applied = 0

        # Fix 1: Update deprecated backend paths
        deprecated_patterns = [
            ("backend.python_backend", "src.backend.python_backend"),
            ("from backend", "from src.backend"),
        ]

        # Fix 2: Add missing src prefix
        missing_prefix_patterns = [
            ("from core import", "from src.core import"),
            ("from context_control import", "from src.context_control import"),
        ]

        for issue in self.issues:
            if issue.severity in ["ERROR", "WARNING"]:
                file_path = self.repo_root / issue.file

                try:
                    with open(file_path, "r") as f:
                        content = f.read()

                    original_content = content

                    # Apply fixes
                    for old, new in deprecated_patterns + missing_prefix_patterns:
                        if old in content:
                            content = content.replace(old, new)

                    if content != original_content:
                        with open(file_path, "w") as f:
                            f.write(content)

                        print(f"  ✅ Fixed: {issue.file}:{issue.line_number}")
                        fixes_applied += 1
                        self.issues.remove(issue)

                except Exception as e:
                    print(f"  ❌ Failed: {issue.file}: {e}")

        print(f"\nTotal fixes applied: {fixes_applied}")
        self.fixes_applied = fixes_applied
        return fixes_applied


def main():
    repo_root = "."
    auto_fix = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage: python3 import_audit.py [repo_root] [--auto-fix]")
            print("")
            print("Arguments:")
            print("  repo_root  - Root directory to scan (default: current directory)")
            print("  --auto-fix - Automatically fix simple issues")
            print("")
            print("Example:")
            print("  python3 import_audit.py /home/masum/github/EmailIntelligence")
            print("  python3 import_audit.py . --auto-fix")
            sys.exit(0)

        if sys.argv[1] == "--auto-fix":
            auto_fix = True
        else:
            repo_root = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--auto-fix":
        auto_fix = True

    # Run audit
    auditor = ImportAuditor(repo_root, auto_fix)
    issues = auditor.scan_repository()

    # Generate report
    report = auditor.generate_report()
    print(report)

    # Save report
    with open("IMPORT_AUDIT_REPORT.md", "w") as f:
        f.write(report)

    print(f"\n📊 Audit complete: {len(issues)} issues found")

    # Auto-fix if requested
    if auto_fix:
        fixes = auditor.auto_fix_simple_issues()
        print(f"✅ {fixes} issues auto-fixed")

        # Re-audit
        print("\n=== Re-auditing after fixes ===")
        issues = auditor.scan_repository()
        report = auditor.generate_report()
        with open("IMPORT_AUDIT_REPORT.md", "w") as f:
            f.write(report)
        print(f"📊 Remaining issues: {len(issues)}")

    print(f"📄 Report saved to: IMPORT_AUDIT_REPORT.md")


if __name__ == "__main__":
    main()
