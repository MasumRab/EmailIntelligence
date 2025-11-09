#!/usr/bin/env python3
"""
Comprehensive Error Detection and Fixing Script for Email Intelligence Platform

This script systematically identifies and fixes common errors in the codebase,
including syntax errors, import issues, configuration problems, and more.
"""

import ast
import os
import sys
import importlib
from typing import List, Dict
from pathlib import Path


class ErrorDetector:
    """Detects and fixes various types of errors in the codebase."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.errors_found = []
        self.fixes_applied = []

    def check_syntax_errors(self) -> List[str]:
        """Check for syntax errors in all Python files."""
        errors = []
        print("Checking for syntax errors...")

        for py_file in self.root_dir.rglob("*.py"):
            # Skip venv directory
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                error_msg = f"Syntax error in {py_file}: {e}"
                errors.append(error_msg)
                self.errors_found.append(error_msg)
            except Exception as e:
                error_msg = f"Error reading {py_file}: {e}"
                errors.append(error_msg)
                self.errors_found.append(error_msg)

        return errors

    def check_import_errors(self) -> List[str]:
        """Check for import errors in key modules."""
        errors = []
        print("Checking for import errors...")

        # Add project root to Python path
        sys.path.insert(0, str(self.root_dir))

        # List of key modules to test
        key_modules = [
            "backend.python_backend.database",
            "backend.python_backend.ai_engine",
            "backend.python_backend.settings",
            "backend.node_engine.workflow_engine",
            "backend.node_engine.node_base",
        ]

        for module_name in key_modules:
            try:
                importlib.import_module(module_name)
                print(f"✓ {module_name} imported successfully")
            except ImportError as e:
                error_msg = f"Import error in {module_name}: {e}"
                errors.append(error_msg)
                self.errors_found.append(error_msg)
            except Exception as e:
                error_msg = f"Runtime error in {module_name}: {e}"
                errors.append(error_msg)
                self.errors_found.append(error_msg)

        return errors

    def check_configuration_errors(self) -> List[str]:
        """Check for configuration-related errors."""
        errors = []
        print("Checking for configuration errors...")

        # Check if required environment variables are set
        required_env_vars = [
            "OPENROUTER_API_KEY",
            "GEMINI_API_KEY",
            "DEEPSEEK_API_KEY",
            "GROQ_API_KEY",
            "COHERE_API_KEY",
        ]

        for var in required_env_vars:
            if not os.environ.get(var):
                warning_msg = f"Warning: Environment variable {var} not set"
                print(warning_msg)
                # This is a warning, not an error, so we don't add it to errors_found

        # Check if data directory exists
        data_dir = self.root_dir / "data"
        if not data_dir.exists():
            try:
                data_dir.mkdir(exist_ok=True)
                fix_msg = f"Created missing data directory: {data_dir}"
                self.fixes_applied.append(fix_msg)
                print(f"✓ {fix_msg}")
            except Exception as e:
                error_msg = f"Error creating data directory: {e}"
                errors.append(error_msg)
                self.errors_found.append(error_msg)

        return errors

    def check_deprecated_code(self) -> List[str]:
        """Check for deprecated code patterns."""
        errors = []
        print("Checking for deprecated code patterns...")

        deprecated_patterns = {
            "backend/python_backend": "src/main:create_app() for the new modular architecture"
        }

        for file_pattern, suggestion in deprecated_patterns.items():
            for py_file in self.root_dir.rglob("*.py"):
                if file_pattern in str(py_file):
                    try:
                        with open(py_file, "r", encoding="utf-8") as f:
                            content = f.read()
                        if file_pattern.replace("/", ".").replace(".py", "") in content:
                            warning_msg = f"Warning: {py_file} uses deprecated code. Use {suggestion}"
                            print(warning_msg)
                            # This is a warning, not an error
                    except Exception as e:
                        error_msg = f"Error reading {py_file}: {e}"
                        errors.append(error_msg)
                        self.errors_found.append(error_msg)

        return errors

    def run_all_checks(self) -> Dict[str, List[str]]:
        """Run all error checking functions."""
        results = {
            "syntax_errors": self.check_syntax_errors(),
            "import_errors": self.check_import_errors(),
            "config_errors": self.check_configuration_errors(),
            "deprecated_code": self.check_deprecated_code(),
        }

        return results

    def generate_report(self) -> str:
        """Generate a comprehensive report of findings."""
        report = []
        report.append("=" * 60)
        report.append("EMAIL INTELLIGENCE PLATFORM - ERROR DETECTION REPORT")
        report.append("=" * 60)
        report.append("")

        if self.errors_found:
            report.append("ERRORS FOUND:")
            report.append("-" * 20)
            for i, error in enumerate(self.errors_found, 1):
                report.append(f"{i}. {error}")
        else:
            report.append("✓ NO ERRORS FOUND")

        report.append("")

        if self.fixes_applied:
            report.append("FIXES APPLIED:")
            report.append("-" * 20)
            for i, fix in enumerate(self.fixes_applied, 1):
                report.append(f"{i}. {fix}")
        else:
            report.append("ℹ NO AUTOMATIC FIXES APPLIED")

        report.append("")
        report.append("RECOMMENDATIONS:")
        report.append("-" * 20)
        report.append("1. Set required environment variables for full functionality")
        report.append("2. Review deprecated code warnings and plan migration")
        report.append("3. Run tests to ensure all functionality works as expected")
        report.append("4. Check logs for any runtime warnings or errors")

        return "\n".join(report)


def main():
    """Main function to run the error detection."""
    print("Starting comprehensive error detection...")

    detector = ErrorDetector()
    results = detector.run_all_checks()

    # Print summary
    total_errors = sum(len(errors) for errors in results.values())
    print(f"\nCheck completed. Found {total_errors} issues.")

    # Generate and print report
    report = detector.generate_report()
    print("\n" + report)

    # Save report to file
    report_file = Path("error_detection_report.txt")
    with open(report_file, "w") as f:
        f.write(report)
    print(f"\nReport saved to {report_file}")


if __name__ == "__main__":
    main()
