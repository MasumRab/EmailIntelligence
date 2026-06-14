"""
Sonar Issues Command Module

Provides a CLI command to interact with SonarQube / SonarCloud issues.
"""

from argparse import Namespace
from typing import Any, Dict
import json

from .interface import Command

class SonarIssuesCommand(Command):
    """
    Command for fetching and listing SonarQube issues.
    """

    @property
    def name(self) -> str:
        return "sonar-issues"

    @property
    def description(self) -> str:
        return "Fetch and list SonarQube/SonarCloud issues"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments to the argument parser.

        Args:
            parser: Subparser for this command
        """
        parser.add_argument(
            "--limit",
            type=int,
            default=50,
            help="Maximum number of issues to retrieve (default: 50)"
        )
        parser.add_argument(
            "--severities",
            type=str,
            help="Comma-separated list of severities (e.g. BLOCKER,CRITICAL,MAJOR,MINOR,INFO)"
        )
        parser.add_argument(
            "--types",
            type=str,
            help="Comma-separated list of types (e.g. BUG,VULNERABILITY,CODE_SMELL)"
        )
        parser.add_argument(
            "--issue",
            type=str,
            help="Specific issue key to retrieve details for"
        )
        parser.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format (default: text)"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.
        Loads the SonarQubeClient dynamically to prevent import errors if requirements aren't met.
        """
        dependencies = {}
        try:
            from src.core.integrations.sonarqube_api import SonarQubeClient
            dependencies["sonar_client"] = SonarQubeClient()
        except ImportError as e:
            dependencies["sonar_client_error"] = str(e)
            dependencies["sonar_client"] = None

        return dependencies

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._sonar_client = dependencies.get("sonar_client")
        self._init_error = dependencies.get("sonar_client_error")

    async def execute(self, args: Namespace) -> int:
        """
        Execute the sonar-issues command.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code
        """
        if self._init_error or not self._sonar_client:
            print(f"Error initializing SonarQube client: {self._init_error}")
            print("Ensure you have 'requests' installed and the module is accessible.")
            return 1

        try:
            if args.issue:
                # Fetch specific issue
                issue = self._sonar_client.get_issue_details(args.issue)
                self._print_output([issue], args.format, detail_view=True)
            else:
                # Fetch list of issues
                issues = self._sonar_client.get_issues(
                    severities=args.severities,
                    types=args.types,
                    limit=args.limit
                )

                if not issues:
                    print("No issues found matching the criteria.")
                    return 0

                self._print_output(issues, args.format)

            return 0

        except Exception as e:  # NOSONAR
            print(f"Error communicating with SonarQube API: {e}")
            return 1

    def _print_output(self, issues: list, fmt: str, detail_view: bool = False) -> None:
        """Format and print the issues based on requested format."""
        if fmt == "json":
            print(json.dumps(issues, indent=2))
            return

        # Text output
        if detail_view and issues:
            issue = issues[0]
            print(f"\nIssue: {issue.get('key')}")
            print(f"Message: {issue.get('message')}")
            print(f"Type: {issue.get('type')}")
            print(f"Severity: {issue.get('severity')}")
            print(f"Status: {issue.get('status')} / {issue.get('resolution', 'UNRESOLVED')}")
            print(f"Component: {issue.get('component')}")
            if issue.get('line'):
                print(f"Line: {issue.get('line')}")
            if issue.get('author'):
                print(f"Author: {issue.get('author')}")
        else:
            print(f"\nFound {len(issues)} issues:")
            print("-" * 80)
            print(f"{'KEY':<20} | {'SEVERITY':<10} | {'TYPE':<15} | {'FILE'}")
            print("-" * 80)
            for issue in issues:
                key = issue.get('key', '')
                sev = issue.get('severity', '')
                type_ = issue.get('type', '')

                # Extract filename from component (format: project_key:path/to/file)
                comp = issue.get('component', '')
                file_path = comp.split(':')[-1] if ':' in comp else comp

                # Add line number if available
                if issue.get('line'):
                    file_path = f"{file_path}:{issue['line']}"

                print(f"{key:<20} | {sev:<10} | {type_:<15} | {file_path}")
            print("-" * 80)
