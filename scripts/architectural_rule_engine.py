#!/usr/bin/env python3
"""
Dynamic Architectural Rule Engine for EmailIntelligenceAuto

This script implements a dynamic rule engine that parses and enforces
architectural rules defined in a centralized YAML specification.
It supports multi-service repositories and context-dependent rules.

Usage:
    python scripts/architectural_rule_engine.py --config rules.yaml --path src/

Author: opencode
"""

import argparse
import ast
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any
import re


class ArchitecturalRuleEngine:
    """
    Dynamic rule engine for enforcing architectural constraints.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.rules = self._load_rules()
        self.violations: List[Dict[str, Any]] = []

    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML configuration file."""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file {self.config_path} not found.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML configuration: {e}")
            sys.exit(1)

    def analyze_path(self, path: str) -> bool:
        """
        Analyze the given path for architectural violations.

        Returns True if no violations found, False otherwise.
        """
        path_obj = Path(path)
        if not path_obj.exists():
            print(f"Error: Path {path} does not exist.")
            return False

        # Find all Python files
        python_files = list(path_obj.rglob("*.py"))

        print(f"Analyzing {len(python_files)} Python files...")

        for py_file in python_files:
            self._analyze_file(py_file)

        return len(self.violations) == 0

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single Python file for violations."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content, filename=str(file_path))

            # Apply rules
            for rule_name, rule_config in self.rules.get("rules", {}).items():
                self._apply_rule(rule_name, rule_config, tree, file_path, content)

        except SyntaxError as e:
            self._add_violation(
                {
                    "rule": "syntax_error",
                    "file": str(file_path),
                    "line": e.lineno,
                    "message": f"Syntax error: {e.msg}",
                    "severity": "error",
                }
            )
        except Exception as e:
            self._add_violation(
                {
                    "rule": "analysis_error",
                    "file": str(file_path),
                    "line": 0,
                    "message": f"Analysis error: {str(e)}",
                    "severity": "error",
                }
            )
    def _apply_rule(
        self,
        rule_name: str,
        rule_config: Dict[str, Any],
        tree: ast.AST,
        file_path: Path,
        content: str,
    ) -> None:
        """Apply a specific rule to the AST."""
        rule_type = rule_config.get("type")

        if rule_type == "no_import":
            self._check_no_import_rule(rule_name, rule_config, tree, file_path)
        elif rule_type == "layer_dependency":
            self._check_layer_dependency_rule(rule_name, rule_config, tree, file_path)
        elif rule_type == "naming_convention":
            self._check_naming_convention_rule(rule_name, rule_config, tree, file_path)
        # Add more rule types as needed

    def _check_no_import_rule(
        self,
        rule_name: str,
        rule_config: Dict[str, Any],
        tree: ast.AST,
        file_path: Path,
    ) -> None:
        """Check for forbidden imports."""
        forbidden_modules = rule_config.get("forbidden_modules", [])
        allowed_in = rule_config.get("allowed_in", [])

        # Check if this file is in allowed locations
        file_str = str(file_path)
        if allowed_in and not any(pattern in file_str for pattern in allowed_in):
            return  # Rule doesn't apply to this file

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module_name = self._get_module_name(node)

                for forbidden in forbidden_modules:
                    if self._matches_pattern(module_name, forbidden):
                        self._add_violation(
                            {
                                "rule": rule_name,
                                "file": str(file_path),
                                "line": node.lineno,
                                "message": f"Forbidden import: {module_name} (matches {forbidden})",
                                "severity": rule_config.get("severity", "error"),
                            }
                        )

    def _check_layer_dependency_rule(
        self,
        rule_name: str,
        rule_config: Dict[str, Any],
        tree: ast.AST,
        file_path: Path,
    ) -> None:
        """Check layer dependency rules (e.g., domain shouldn't import infrastructure)."""
        from_layer = rule_config.get("from_layer")
        to_layer = rule_config.get("to_layer")
        forbidden = rule_config.get("forbidden", True)

        file_str = str(file_path)

        # Determine current layer
        current_layer = None
        for layer, patterns in self.rules.get("layers", {}).items():
            if any(pattern in file_str for pattern in patterns):
                current_layer = layer
                break

        if current_layer != from_layer:
            return  # Rule doesn't apply

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module_name = self._get_module_name(node)

                # Check if import is from forbidden layer
                for layer, patterns in self.rules.get("layers", {}).items():
                    if layer == to_layer and any(
                        self._matches_pattern(module_name, pattern)
                        for pattern in patterns
                    ):
                        if forbidden:
                            self._add_violation(
                                {
                                    "rule": rule_name,
                                    "file": str(file_path),
                                    "line": node.lineno,
                                    "message": (
                                        f"Layer violation: {from_layer} layer importing from "
                                        f"{to_layer} layer ({module_name})"
                                    ),
                                    "severity": rule_config.get("severity", "error"),
                                }
                            )

    def _check_naming_convention_rule(
        self,
        rule_name: str,
        rule_config: Dict[str, Any],
        tree: ast.AST,
        file_path: Path,
    ) -> None:
        """Check naming conventions."""
        patterns = rule_config.get("patterns", [])

        for pattern in patterns:
            convention_type = pattern.get("type")
            regex = pattern.get("regex")
            applies_to = pattern.get("applies_to", [])

            file_str = str(file_path)
            if applies_to and not any(app in file_str for app in applies_to):
                continue

            if convention_type == "class_name":
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        if not re.match(regex, node.name):
                            self._add_violation(
                                {
                                    "rule": rule_name,
                                    "file": str(file_path),
                                    "line": node.lineno,
                                    "message": f"Naming violation: Class '{node.name}' does not match pattern {regex}",
                                    "severity": rule_config.get("severity", "warning"),
                                }
                            )
            # Add more convention checks as needed

    def _get_module_name(self, node: ast.stmt) -> str:
        """Extract module name from import node."""
        if isinstance(node, ast.Import):
            return node.names[0].name if node.names else ""
        elif isinstance(node, ast.ImportFrom):
            return node.module or ""
        return ""

    def _matches_pattern(self, module_name: str, pattern: str) -> bool:
        """Check if module name matches pattern (supports wildcards)."""
        # Convert wildcard pattern to regex
        regex = re.escape(pattern).replace(r"\*", ".*")
        return re.match(f"^{regex}$", module_name) is not None

    def _add_violation(self, violation: Dict[str, Any]) -> None:
        """Add a violation to the list."""
        self.violations.append(violation)

    def print_report(self) -> None:
        """Print analysis report."""
        if not self.violations:
            print("✅ No architectural violations found.")
            return

        print(f"❌ Found {len(self.violations)} architectural violations:")
        print()

        # Group by severity
        errors = [v for v in self.violations if v.get("severity") == "error"]
        warnings = [v for v in self.violations if v.get("severity") == "warning"]

        if errors:
            print("🚨 ERRORS:")
            for violation in errors:
                print(
                    f"  {violation['file']}:{violation['line']} - {violation['message']}"
                )
            print()

        if warnings:
            print("⚠️  WARNINGS:")
            for violation in warnings:
                print(
                    f"  {violation['file']}:{violation['line']} - {violation['message']}"
                )
            print()

    def get_exit_code(self) -> int:
        """Get appropriate exit code based on violations."""
        has_errors = any(v.get("severity") == "error" for v in self.violations)
        return 1 if has_errors else 0


def main():
    parser = argparse.ArgumentParser(description="Dynamic Architectural Rule Engine")
    parser.add_argument(
        "--config", required=True, help="Path to YAML configuration file"
    )
    parser.add_argument("--path", required=True, help="Path to analyze")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )

    args = parser.parse_args()

    engine = ArchitecturalRuleEngine(args.config)

    success = engine.analyze_path(args.path)

    if args.format == "json":
        import json

        print(
            json.dumps({"success": success, "violations": engine.violations}, indent=2)
        )
    else:
        engine.print_report()

    sys.exit(engine.get_exit_code())


if __name__ == "__main__":
    main()
