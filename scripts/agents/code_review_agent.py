#!/usr/bin/env python3
"""
Code Review Agent Template for OpenCode AI CLI Tool

This agent provides automated code review capabilities including:
- Code quality analysis
- Security vulnerability detection
- Performance issue identification
- Best practice compliance checking
- Automated review comment generation

Usage:
    python code_review_agent.py --pr-url <url> [--config config.json]
    python code_review_agent.py --files file1.py file2.py [--output review.md]
    python code_review_agent.py --diff <diff_file> [--interactive]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from datetime import datetime
import tempfile


@dataclass
class ReviewComment:
    """Represents a single code review comment."""
    file_path: str
    line_number: int
    severity: str  # 'info', 'warning', 'error', 'suggestion'
    category: str  # 'security', 'performance', 'quality', 'style', etc.
    message: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    rule_id: Optional[str] = None


@dataclass
class CodeReviewResult:
    """Represents the complete code review result."""
    summary: Dict[str, Any] = field(default_factory=dict)
    comments: List[ReviewComment] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)


class CodeReviewAgent:
    """Main code review agent class."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = self.load_config(config_path)
        self.checkers = self.initialize_checkers()

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "enabled_checkers": [
                "security",
                "performance",
                "code_quality",
                "imports",
                "documentation",
                "testing"
            ],
            "severity_thresholds": {
                "error": 0,
                "warning": 5,
                "info": 10
            },
            "file_extensions": [".py", ".js", ".ts", ".java", ".cpp", ".c"],
            "exclude_patterns": [
                "test_*.py",
                "*_test.py",
                "__pycache__",
                "node_modules",
                ".git"
            ],
            "max_file_size": 1000000,  # 1MB
            "ai_model": "claude-3-5-sonnet-20241022",
            "output_format": "markdown"
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def initialize_checkers(self) -> Dict[str, Callable[..., List[ReviewComment]]]:
        """Initialize all code checkers."""
        return {
            "security": self.check_security_issues,
            "performance": self.check_performance_issues,
            "code_quality": self.check_code_quality,
            "imports": self.check_import_issues,
            "documentation": self.check_documentation,
            "testing": self.check_testing_coverage
        }

    def review_files(self, file_paths: List[str]) -> CodeReviewResult:
        """Review a list of files."""
        result = CodeReviewResult()
        result.summary = {
            "total_files": len(file_paths),
            "files_reviewed": 0,
            "total_comments": 0,
            "severity_breakdown": {"error": 0, "warning": 0, "info": 0, "suggestion": 0}
        }

        for file_path in file_paths:
            if self.should_review_file(file_path):
                comments = self.review_single_file(file_path)
                result.comments.extend(comments)
                result.summary["files_reviewed"] += 1

        # Update summary statistics
        result.summary["total_comments"] = len(result.comments)
        for comment in result.comments:
            result.summary["severity_breakdown"][comment.severity] += 1

        # Calculate metrics
        result.metrics = self.calculate_metrics(result)

        return result

    def review_diff(self, diff_content: str) -> CodeReviewResult:
        """Review changes from a diff."""
        result = CodeReviewResult()

        # Parse diff and extract changed files
        changed_files = self.parse_diff(diff_content)

        # Review only changed lines
        for file_path, changes in changed_files.items():
            comments = self.review_file_changes(file_path, changes)
            result.comments.extend(comments)

        result.summary = {
            "diff_analysis": True,
            "changed_files": len(changed_files),
            "total_comments": len(result.comments)
        }

        return result

    def should_review_file(self, file_path: str) -> bool:
        """Determine if a file should be reviewed."""
        # Check file extension
        if not any(file_path.endswith(ext) for ext in self.config["file_extensions"]):
            return False

        # Check file size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > self.config["max_file_size"]:
                return False

        # Check exclude patterns
        for pattern in self.config["exclude_patterns"]:
            if pattern in file_path:
                return False

        return True

    def review_single_file(self, file_path: str) -> List[ReviewComment]:
        """Review a single file comprehensively."""
        comments = []

        if not os.path.exists(file_path):
            return comments

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            # Run all enabled checkers
            for checker_name in self.config["enabled_checkers"]:
                if checker_name in self.checkers:
                    checker_comments = self.checkers[checker_name](file_path, content, lines)
                    comments.extend(checker_comments)

        except Exception as e:
            comments.append(ReviewComment(
                file_path=file_path,
                line_number=1,
                severity="error",
                category="system",
                message=f"Failed to review file: {str(e)}"
            ))

        return comments

    def review_file_changes(self, file_path: str, changes: List[Dict]) -> List[ReviewComment]:
        """Review only the changed lines in a file."""
        comments = []

        # Focus review on changed lines only
        for change in changes:
            line_number = change.get("line_number", 1)
            content = change.get("content", "")

            # Run targeted checks on changed content
            security_comments = self.check_security_issues(file_path, content, [content], line_number)
            performance_comments = self.check_performance_issues(file_path, content, [content], line_number)

            comments.extend(security_comments)
            comments.extend(performance_comments)

        return comments

    # Security Checkers
    def check_security_issues(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for security vulnerabilities."""
        comments = []

        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']*["\']',
            r'secret\s*=\s*["\'][^"\']*["\']',
            r'api_key\s*=\s*["\'][^"\']*["\']',
            r'token\s*=\s*["\'][^"\']*["\']'
        ]

        for i, line in enumerate(lines):
            line_num = start_line + i
            for pattern in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    comments.append(ReviewComment(
                        file_path=file_path,
                        line_number=line_num,
                        severity="error",
                        category="security",
                        message="Potential hardcoded secret detected",
                        suggestion="Use environment variables or secure credential storage",
                        code_snippet=line.strip(),
                        rule_id="SEC-001"
                    ))

        # Check for SQL injection vulnerabilities
        if "sql" in content.lower():
            sql_injection_patterns = [
                r'execute\s*\(\s*["\'].*?%s.*?["\']',
                r'cursor\.execute\s*\(\s*f["\']'
            ]

            for i, line in enumerate(lines):
                line_num = start_line + i
                for pattern in sql_injection_patterns:
                    if re.search(pattern, line):
                        comments.append(ReviewComment(
                            file_path=file_path,
                            line_number=line_num,
                            severity="warning",
                            category="security",
                            message="Potential SQL injection vulnerability",
                            suggestion="Use parameterized queries or prepared statements",
                            code_snippet=line.strip(),
                            rule_id="SEC-002"
                        ))

        return comments

    def check_performance_issues(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for performance issues."""
        comments = []

        # Check for inefficient list operations
        for i, line in enumerate(lines):
            line_num = start_line + i

            # Check for list concatenation in loops
            if re.search(r'(\w+)\s*\+\s*=\s*\[', line):
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity="warning",
                    category="performance",
                    message="Inefficient list concatenation in loop",
                    suggestion="Use list.extend() or list comprehension",
                    code_snippet=line.strip(),
                    rule_id="PERF-001"
                ))

            # Check for unnecessary list comprehensions
            if re.search(r'\[.*for.*in.*\].*\[.*for.*in.*\]', line):
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity="info",
                    category="performance",
                    message="Nested list comprehensions may impact readability",
                    suggestion="Consider breaking into separate comprehensions or using loops",
                    code_snippet=line.strip(),
                    rule_id="PERF-002"
                ))

        return comments

    def check_code_quality(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for code quality issues."""
        comments = []

        # Check line length
        max_line_length = 88
        for i, line in enumerate(lines):
            line_num = start_line + i
            if len(line) > max_line_length:
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity="info",
                    category="quality",
                    message=f"Line too long ({len(line)} > {max_line_length} characters)",
                    suggestion="Break line into multiple lines or refactor",
                    code_snippet=line.strip(),
                    rule_id="QUAL-001"
                ))

        # Check for TODO comments
        for i, line in enumerate(lines):
            line_num = start_line + i
            if re.search(r'#\s*TODO', line, re.IGNORECASE):
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=line_num,
                    severity="info",
                    category="quality",
                    message="TODO comment found",
                    suggestion="Consider addressing the TODO or creating a task",
                    code_snippet=line.strip(),
                    rule_id="QUAL-002"
                ))

        return comments

    def check_import_issues(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for import-related issues."""
        comments = []

        # Check for unused imports (basic check)
        imports = []
        for line in lines[:50]:  # Check first 50 lines for imports
            match = re.match(r'^(?:from\s+(\w+)|import\s+(\w+))', line.strip())
            if match:
                module = match.group(1) or match.group(2)
                imports.append(module)

        # This is a basic check - real unused import detection requires AST parsing
        if len(imports) > 20:
            comments.append(ReviewComment(
                file_path=file_path,
                line_number=1,
                severity="info",
                category="imports",
                message=f"High number of imports ({len(imports)})",
                suggestion="Consider consolidating imports or splitting into modules",
                rule_id="IMP-001"
            ))

        return comments

    def check_documentation(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for documentation issues."""
        comments = []

        # Check for missing docstrings in functions/classes
        if file_path.endswith('.py'):
            # Basic check for functions without docstrings
            function_pattern = r'def\s+\w+\s*\('
            docstring_pattern = r'""".*?"""'

            in_function = False
            function_start = 0

            for i, line in enumerate(lines):
                if re.search(function_pattern, line):
                    if in_function:
                        # Previous function ended without docstring
                        comments.append(ReviewComment(
                            file_path=file_path,
                            line_number=function_start + start_line,
                            severity="info",
                            category="documentation",
                            message="Function missing docstring",
                            suggestion="Add docstring describing function purpose and parameters",
                            rule_id="DOC-001"
                        ))
                    in_function = True
                    function_start = i
                elif in_function and re.search(docstring_pattern, line):
                    in_function = False

        return comments

    def check_testing_coverage(self, file_path: str, content: str, lines: List[str], start_line: int = 1) -> List[ReviewComment]:
        """Check for testing coverage issues."""
        comments = []

        # This is a placeholder - real test coverage requires running coverage tools
        if not file_path.endswith('_test.py') and not file_path.startswith('test_'):
            # Check if corresponding test file exists
            test_file_candidates = [
                f"test_{os.path.basename(file_path)}",
                f"{os.path.basename(file_path).replace('.py', '')}_test.py",
                f"tests/test_{os.path.basename(file_path)}"
            ]

            test_exists = False
            for test_file in test_file_candidates:
                if os.path.exists(test_file):
                    test_exists = True
                    break

            if not test_exists:
                comments.append(ReviewComment(
                    file_path=file_path,
                    line_number=1,
                    severity="info",
                    category="testing",
                    message="No corresponding test file found",
                    suggestion="Consider adding unit tests for this module",
                    rule_id="TEST-001"
                ))

        return comments

    def calculate_metrics(self, result: CodeReviewResult) -> Dict[str, Any]:
        """Calculate review metrics."""
        metrics = {
            "quality_score": 100,
            "severity_score": 0,
            "category_breakdown": {},
            "file_breakdown": {}
        }

        # Calculate severity score
        severity_weights = {"error": 10, "warning": 3, "info": 1, "suggestion": 0}
        total_severity = 0

        for comment in result.comments:
            # Category breakdown
            if comment.category not in metrics["category_breakdown"]:
                metrics["category_breakdown"][comment.category] = 0
            metrics["category_breakdown"][comment.category] += 1

            # File breakdown
            if comment.file_path not in metrics["file_breakdown"]:
                metrics["file_breakdown"][comment.file_path] = 0
            metrics["file_breakdown"][comment.file_path] += 1

            # Severity scoring
            total_severity += severity_weights.get(comment.severity, 0)

        metrics["severity_score"] = total_severity
        metrics["quality_score"] = max(0, 100 - total_severity)

        return metrics

    def parse_diff(self, diff_content: str) -> Dict[str, List[Dict]]:
        """Parse diff content to extract changed files and lines."""
        changed_files = {}
        current_file = None
        current_changes = []

        for line in diff_content.split('\n'):
            if line.startswith('+++ b/'):
                if current_file and current_changes:
                    changed_files[current_file] = current_changes
                current_file = line[6:]  # Remove '+++ b/'
                current_changes = []
            elif line.startswith('+') and not line.startswith('+++'):
                # Added line
                current_changes.append({
                    "type": "addition",
                    "content": line[1:],
                    "line_number": len(current_changes) + 1
                })
            elif line.startswith('-') and not line.startswith('---'):
                # Removed line
                current_changes.append({
                    "type": "deletion",
                    "content": line[1:],
                    "line_number": len(current_changes) + 1
                })

        if current_file and current_changes:
            changed_files[current_file] = current_changes

        return changed_files

    def generate_report(self, result: CodeReviewResult, output_format: str = "markdown") -> str:
        """Generate a formatted review report."""
        if output_format == "markdown":
            return self.generate_markdown_report(result)
        elif output_format == "json":
            return json.dumps({
                "summary": result.summary,
                "comments": [vars(comment) for comment in result.comments],
                "metrics": result.metrics,
                "generated_at": result.generated_at.isoformat()
            }, indent=2)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def generate_markdown_report(self, result: CodeReviewResult) -> str:
        """Generate a markdown-formatted review report."""
        report = []

        # Header
        report.append("# Code Review Report")
        report.append(f"**Generated:** {result.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary
        report.append("## Summary")
        report.append(f"- **Files Reviewed:** {result.summary.get('files_reviewed', 0)}")
        report.append(f"- **Total Comments:** {result.summary.get('total_comments', 0)}")
        report.append(f"- **Quality Score:** {result.metrics.get('quality_score', 0)}/100")
        report.append("")

        # Severity Breakdown
        if 'severity_breakdown' in result.summary:
            report.append("### Severity Breakdown")
            for severity, count in result.summary['severity_breakdown'].items():
                if count > 0:
                    report.append(f"- **{severity.title()}:** {count}")
            report.append("")

        # Category Breakdown
        if 'category_breakdown' in result.metrics:
            report.append("### Issues by Category")
            for category, count in result.metrics['category_breakdown'].items():
                report.append(f"- **{category.title()}:** {count}")
            report.append("")

        # Comments
        if result.comments:
            report.append("## Review Comments")
            report.append("")

            # Group comments by file
            comments_by_file = {}
            for comment in result.comments:
                if comment.file_path not in comments_by_file:
                    comments_by_file[comment.file_path] = []
                comments_by_file[comment.file_path].append(comment)

            for file_path, file_comments in comments_by_file.items():
                report.append(f"### {file_path}")
                report.append("")

                for comment in file_comments:
                    severity_emoji = {
                        "error": "🚨",
                        "warning": "⚠️",
                        "info": "ℹ️",
                        "suggestion": "💡"
                    }.get(comment.severity, "❓")

                    report.append(f"**{severity_emoji} {comment.category.title()}** (Line {comment.line_number})")
                    report.append(f"{comment.message}")

                    if comment.code_snippet:
                        report.append(f"```")
                        report.append(comment.code_snippet)
                        report.append("```")

                    if comment.suggestion:
                        report.append(f"**Suggestion:** {comment.suggestion}")

                    if comment.rule_id:
                        report.append(f"**Rule:** {comment.rule_id}")

                    report.append("")

        return "\n".join(report)


def main():
    """Main entry point for the code review agent."""
    parser = argparse.ArgumentParser(description="OpenCode AI Code Review Agent")
    parser.add_argument("--files", nargs="+", help="Files to review")
    parser.add_argument("--pr-url", help="Pull request URL to review")
    parser.add_argument("--diff", help="Diff file or content to review")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                       help="Output format")
    parser.add_argument("--interactive", action="store_true",
                       help="Run in interactive mode")

    args = parser.parse_args()

    # Initialize agent
    agent = CodeReviewAgent(args.config)

    result = None

    if args.files:
        # Review specific files
        result = agent.review_files(args.files)
    elif args.pr_url:
        # Review pull request (would need GitHub API integration)
        print(f"PR review not yet implemented. URL: {args.pr_url}")
        return
    elif args.diff:
        # Review diff content
        if os.path.exists(args.diff):
            with open(args.diff, 'r') as f:
                diff_content = f.read()
        else:
            diff_content = args.diff
        result = agent.review_diff(diff_content)
    else:
        print("Error: Must specify --files, --pr-url, or --diff")
        return

    if result:
        # Generate report
        report = agent.generate_report(result, args.format)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Review report saved to: {args.output}")
        else:
            print(report)

        # Exit with appropriate code based on findings
        if result.summary.get('severity_breakdown', {}).get('error', 0) > 0:
            sys.exit(1)  # Fail if errors found
        elif result.summary.get('severity_breakdown', {}).get('warning', 0) > agent.config['severity_thresholds']['warning']:
            sys.exit(1)  # Fail if too many warnings


if __name__ == "__main__":
    main()