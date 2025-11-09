#!/usr/bin/env python3
"""
Comprehensive Codebase Analysis Tool

This script analyzes the Email Intelligence Platform codebase to identify:
- Technical debt
- Architecture concerns
- Performance bottlenecks
- Security vulnerabilities
- Maintainability issues

It provides risk assessments, impact analysis, and remediation steps.
"""

import ast
import re
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class CodebaseAnalyzer:
    """Analyzes the codebase for various issues and provides timeline estimates."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.risk_levels = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1}

    def analyze_technical_debt(self) -> List[Dict]:
        """Analyze technical debt in the codebase."""
        issues = []

        # Check for TODO/FIXME comments
        todo_pattern = re.compile(r"#\s*(TODO|FIXME|HACK|XXX):?\s*(.+)$")

        for py_file in self.root_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    match = todo_pattern.search(line)
                    if match:
                        issue_type = match.group(1)
                        description = match.group(2).strip()

                        risk_level = (
                            "HIGH" if issue_type in ["FIXME", "HACK"] else "MEDIUM"
                        )
                        timeline = (
                            "1-2 weeks" if issue_type == "FIXME" else "1-3 months"
                        )

                        issues.append(
                            {
                                "type": "TECHNICAL_DEBT",
                                "risk_level": risk_level,
                                "file": str(py_file.relative_to(self.root_dir)),
                                "line": line_num,
                                "description": f"{issue_type}: {description}",
                                "impact": "Code maintainability and quality",
                                "remediation": f"Address the {issue_type} comment",
                                "timeline": timeline,
                                "effort": "1-4 hours",
                            }
                        )
            except Exception:
                continue

        return issues

    def analyze_architecture_concerns(self) -> List[Dict]:
        """Analyze architecture-related concerns."""
        issues = []

        # Check for circular dependencies
        circular_deps = self._detect_circular_dependencies()
        for dep in circular_deps:
            issues.append(
                {
                    "type": "ARCHITECTURE_CONCERN",
                    "risk_level": "HIGH",
                    "file": dep["file"],
                    "description": f"Circular dependency: {dep['cycle']}",
                    "impact": "Maintainability and testability",
                    "remediation": "Refactor to eliminate circular dependency",
                    "timeline": "2-4 weeks",
                    "effort": "2-5 days",
                }
            )

        # Check for large classes/modules
        large_modules = self._detect_large_modules()
        for module in large_modules:
            if module["loc"] > 1000:
                issues.append(
                    {
                        "type": "ARCHITECTURE_CONCERN",
                        "risk_level": "MEDIUM",
                        "file": module["file"],
                        "description": f"Large module ({module['loc']} lines)",
                        "impact": "Maintainability and readability",
                        "remediation": "Split into smaller, focused modules",
                        "timeline": "1-2 months",
                        "effort": "3-7 days",
                    }
                )

        return issues

    def analyze_performance_bottlenecks(self) -> List[Dict]:
        """Analyze potential performance bottlenecks."""
        issues = []

        # Check for inefficient loops and operations
        for py_file in self.root_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for nested loops that might be inefficient
                if content.count("for ") > 10 and "range(len(" in content:
                    issues.append(
                        {
                            "type": "PERFORMANCE_BOTTLENECK",
                            "risk_level": "MEDIUM",
                            "file": str(py_file.relative_to(self.root_dir)),
                            "description": "Potential inefficient nested loops",
                            "impact": "Execution time and resource usage",
                            "remediation": "Optimize loops, consider using list comprehensions or numpy operations",
                            "timeline": "1-2 months",
                            "effort": "2-4 days",
                        }
                    )

                # Check for repeated file I/O operations
                if content.count("open(") > 5 and "read()" in content:
                    issues.append(
                        {
                            "type": "PERFORMANCE_BOTTLENECK",
                            "risk_level": "MEDIUM",
                            "file": str(py_file.relative_to(self.root_dir)),
                            "description": "Multiple file I/O operations",
                            "impact": "I/O performance",
                            "remediation": "Implement caching or batch operations",
                            "timeline": "2-3 weeks",
                            "effort": "3-5 days",
                        }
                    )

            except Exception:
                continue

        return issues

    def analyze_security_vulnerabilities(self) -> List[Dict]:
        """Analyze potential security vulnerabilities."""
        issues = []

        # Check for hardcoded secrets
        secret_patterns = [
            (
                r'["\'](?:api[_-]?key|secret|password|token)["\']\s*[:=]\s*["\'][^"\']{5,}',
                "API Key/Secret",
            ),
            (r'["\'][a-zA-Z0-9]{32,}["\']', "Potential Secret"),
        ]

        for py_file in self.root_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                for pattern, desc in secret_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        issues.append(
                            {
                                "type": "SECURITY_VULNERABILITY",
                                "risk_level": "HIGH",
                                "file": str(py_file.relative_to(self.root_dir)),
                                "description": f"Hardcoded {desc} found",
                                "impact": "Security breach risk",
                                "remediation": "Use environment variables or secure configuration management",
                                "timeline": "1-2 weeks",
                                "effort": "2-8 hours",
                            }
                        )

            except Exception:
                continue

        return issues

    def analyze_maintainability_issues(self) -> List[Dict]:
        """Analyze maintainability issues."""
        issues = []

        # Check for code duplication
        duplicate_patterns = self._detect_code_duplication()
        for pattern in duplicate_patterns:
            issues.append(
                {
                    "type": "MAINTAINABILITY_ISSUE",
                    "risk_level": "MEDIUM",
                    "file": pattern["file"],
                    "description": f"Code duplication ({pattern['count']} occurrences)",
                    "impact": "Maintenance overhead",
                    "remediation": "Extract common code into reusable functions/classes",
                    "timeline": "2-4 weeks",
                    "effort": "1-3 days",
                }
            )

        # Check for complex functions
        complex_functions = self._detect_complex_functions()
        for func in complex_functions:
            if func["complexity"] > 15:
                issues.append(
                    {
                        "type": "MAINTAINABILITY_ISSUE",
                        "risk_level": "MEDIUM",
                        "file": func["file"],
                        "description": f"High complexity function '{func['name']}' (cyclomatic complexity: {func['complexity']})",
                        "impact": "Code readability and testability",
                        "remediation": "Refactor into smaller, simpler functions",
                        "timeline": "1-2 months",
                        "effort": "2-5 days",
                    }
                )

        return issues

    def _detect_circular_dependencies(self) -> List[Dict]:
        """Detect circular dependencies between modules."""
        # Simplified detection - in a real implementation, this would be more sophisticated
        circular_deps = []

        # Check for obvious circular imports in key files
        key_files = [
            "backend/python_backend/database.py",
            "backend/python_backend/ai_engine.py",
            "backend/python_backend/settings.py",
        ]

        for file_path in key_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Look for imports that might create circular dependencies
                    if (
                        "from .database import" in content
                        and "from .settings import" in content
                    ):
                        circular_deps.append(
                            {"file": file_path, "cycle": "database <-> settings"}
                        )
                except Exception:
                    continue

        return circular_deps

    def _detect_large_modules(self) -> List[Dict]:
        """Detect large modules that might need refactoring."""
        large_modules = []

        for py_file in self.root_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                loc = len(
                    [
                        line
                        for line in lines
                        if line.strip() and not line.strip().startswith("#")
                    ]
                )
                if loc > 500:  # Threshold for large modules
                    large_modules.append(
                        {"file": str(py_file.relative_to(self.root_dir)), "loc": loc}
                    )
            except Exception:
                continue

        return large_modules

    def _detect_code_duplication(self) -> List[Dict]:
        """Detect potential code duplication."""
        # Simplified detection - in a real implementation, this would be more sophisticated
        duplicates = []

        # Look for common patterns that might be duplicated
        patterns_to_check = [
            "await db.get_all_categories()",
            "logger.error(f",
            "except Exception as e:",
        ]

        for pattern in patterns_to_check:
            occurrences = 0
            file_with_most = ""

            for py_file in self.root_dir.rglob("*.py"):
                if "venv" in str(py_file):
                    continue

                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    count = content.count(pattern)
                    if count > 0:
                        occurrences += count
                        if count > 2:  # More than 2 occurrences in a file
                            file_with_most = str(py_file.relative_to(self.root_dir))
                except Exception:
                    continue

            if occurrences > 5:  # More than 5 total occurrences
                duplicates.append(
                    {"file": file_with_most, "pattern": pattern, "count": occurrences}
                )

        return duplicates

    def _detect_complex_functions(self) -> List[Dict]:
        """Detect functions with high cyclomatic complexity."""
        complex_functions = []

        for py_file in self.root_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse the AST to analyze function complexity
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = self._calculate_complexity(node)
                        if complexity > 10:  # Threshold for complex functions
                            complex_functions.append(
                                {
                                    "file": str(py_file.relative_to(self.root_dir)),
                                    "name": node.name,
                                    "complexity": complexity,
                                }
                            )
            except Exception:
                continue

        return complex_functions

    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and isinstance(
                child.op, (ast.And, ast.Or)
            ):
                complexity += len(child.values) - 1

        return complexity

    def run_full_analysis(self) -> List[Dict]:
        """Run all analysis functions and return consolidated results."""
        all_issues = []

        print("Running technical debt analysis...")
        all_issues.extend(self.analyze_technical_debt())

        print("Running architecture concerns analysis...")
        all_issues.extend(self.analyze_architecture_concerns())

        print("Running performance bottlenecks analysis...")
        all_issues.extend(self.analyze_performance_bottlenecks())

        print("Running security vulnerabilities analysis...")
        all_issues.extend(self.analyze_security_vulnerabilities())

        print("Running maintainability issues analysis...")
        all_issues.extend(self.analyze_maintainability_issues())

        return all_issues

    def generate_report(self, issues: List[Dict]) -> str:
        """Generate a comprehensive report of all identified issues."""
        # Sort issues by risk level (highest first)
        sorted_issues = sorted(
            issues, key=lambda x: self.risk_levels[x["risk_level"]], reverse=True
        )

        report = []
        report.append("=" * 80)
        report.append("EMAIL INTELLIGENCE PLATFORM - CODEBASE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Issues Identified: {len(sorted_issues)}")
        report.append("")

        # Group issues by type
        issues_by_type = {}
        for issue in sorted_issues:
            issue_type = issue["type"]
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # Report by type
        for issue_type, issues in issues_by_type.items():
            report.append(
                f"{issue_type.replace('_', ' ').title()} ({len(issues)} issues)"
            )
            report.append("-" * 50)

            # Group by risk level within each type
            issues_by_risk = {}
            for issue in issues:
                risk = issue["risk_level"]
                if risk not in issues_by_risk:
                    issues_by_risk[risk] = []
                issues_by_risk[risk].append(issue)

            # Display by risk level (highest first)
            for risk in sorted(
                issues_by_risk.keys(), key=lambda x: self.risk_levels[x], reverse=True
            ):
                risk_issues = issues_by_risk[risk]
                report.append(f"  {risk} Risk ({len(risk_issues)} issues):")

                for issue in risk_issues:
                    report.append(f"    • {issue['description']}")
                    report.append(f"      File: {issue['file']}")
                    if "line" in issue:
                        report.append(f"      Line: {issue['line']}")
                    report.append(f"      Impact: {issue['impact']}")
                    report.append(f"      Remediation: {issue['remediation']}")
                    report.append(f"      Timeline: {issue['timeline']}")
                    report.append(f"      Effort: {issue['effort']}")
                    report.append("")

            report.append("")

        # Summary by risk level
        report.append("SUMMARY BY RISK LEVEL")
        report.append("-" * 30)
        risk_summary = {}
        for issue in sorted_issues:
            risk = issue["risk_level"]
            risk_summary[risk] = risk_summary.get(risk, 0) + 1

        for risk in sorted(
            risk_summary.keys(), key=lambda x: self.risk_levels[x], reverse=True
        ):
            report.append(f"{risk}: {risk_summary[risk]} issues")

        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 20)
        report.append("1. Prioritize CRITICAL and HIGH risk issues immediately")
        report.append("2. Schedule MEDIUM risk issues for the next development cycle")
        report.append("3. Plan regular code reviews to prevent new technical debt")
        report.append("4. Implement automated code quality checks in CI/CD pipeline")
        report.append("5. Establish coding standards and guidelines for the team")

        return "\n".join(report)


def main():
    """Main function to run the codebase analysis."""
    print("Starting comprehensive codebase analysis...")

    analyzer = CodebaseAnalyzer()
    issues = analyzer.run_full_analysis()

    print(f"\nAnalysis completed. Found {len(issues)} issues.")

    # Generate and print report
    report = analyzer.generate_report(issues)
    print("\n" + report)

    # Save report to file
    report_file = Path("codebase_analysis_report.txt")
    with open(report_file, "w") as f:
        f.write(report)
    print(f"\nReport saved to {report_file}")

    # Also save issues in JSON format for further processing
    issues_file = Path("codebase_issues.json")
    with open(issues_file, "w") as f:
        json.dump(issues, f, indent=2)
    print(f"Issues data saved to {issues_file}")


if __name__ == "__main__":
    main()
