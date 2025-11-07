#!/usr/bin/env python3
"""
Task Validation Script

This script validates tasks before creation using the Task Master validation API.
It can be integrated into the task creation workflow to ensure quality standards.
"""

import sys
import json
import argparse
import requests
from typing import Dict, Any, List


class TaskValidator:
    """Client for task validation API."""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize the task validator.

        Args:
            api_base_url: Base URL for the Task Master API
        """
        self.api_base_url = api_base_url.rstrip("/")
        self.validation_url = f"{self.api_base_url}/api/task-validation/validate-creation"

    def validate_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task using the validation API.

        Args:
            task_data: Task data to validate

        Returns:
            Validation result
        """
        try:
            response = requests.post(
                self.validation_url,
                json=task_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "valid": False,
                    "errors": [f"API error: {response.status_code} - {response.text}"],
                    "warnings": [],
                    "recommendations": []
                }

        except requests.RequestException as e:
            return {
                "valid": False,
                "errors": [f"Connection error: {str(e)}"],
                "warnings": [],
                "recommendations": []
            }

    def get_requirements(self, complexity: str, branch_type: str) -> Dict[str, Any]:
        """Get testing requirements for a complexity/branch combination."""
        try:
            url = f"{self.api_base_url}/api/task-validation/requirements/{complexity}/{branch_type}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get requirements: {response.status_code}"}

        except requests.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}

    def get_complexity_hints(self) -> Dict[str, Any]:
        """Get hints for determining task complexity."""
        try:
            url = f"{self.api_base_url}/api/task-validation/complexity-hints"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get hints: {response.status_code}"}

        except requests.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}


def parse_acceptance_criteria(ac_string: str) -> List[str]:
    """Parse acceptance criteria from string format."""
    if not ac_string:
        return []

    # Split by newlines or semicolons
    criteria = []
    for line in ac_string.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            # Remove common prefixes
            line = line.lstrip('- ').lstrip('0123456789. ')
            if line:
                criteria.append(line)

    return criteria


def main():
    """Main entry point for task validation."""
    parser = argparse.ArgumentParser(description="Validate tasks for Task Master")
    parser.add_argument("--title", required=True, help="Task title")
    parser.add_argument("--description", required=True, help="Task description")
    parser.add_argument("--acceptance-criteria", help="Acceptance criteria (one per line)")
    parser.add_argument("--test-strategy", default="", help="Test strategy")
    parser.add_argument("--branch", default="", help="Target branch")
    parser.add_argument("--priority", default="medium", choices=["low", "medium", "high", "critical"],
                       help="Task priority")
    parser.add_argument("--api-url", default="http://localhost:8000",
                       help="Task Master API base URL")
    parser.add_argument("--json-output", action="store_true",
                       help="Output result as JSON")
    parser.add_argument("--strict", action="store_true",
                       help="Fail on warnings in addition to errors")

    args = parser.parse_args()

    # Prepare task data
    task_data = {
        "title": args.title,
        "description": args.description,
        "acceptance_criteria": parse_acceptance_criteria(args.acceptance_criteria or ""),
        "test_strategy": args.test_strategy,
        "branch": args.branch,
        "priority": args.priority,
        "dependencies": []  # Not supported in this basic version
    }

    # Validate the task
    validator = TaskValidator(args.api_url)
    result = validator.validate_task(task_data)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        if result["valid"]:
            print("✅ Task validation passed!")
            print(f"📊 Complexity: {result.get('complexity', 'unknown')}")
            print(f"🌿 Branch Type: {result.get('branch_type', 'unknown')}")

            if result.get("warnings"):
                print("\n⚠️  Warnings:")
                for warning in result["warnings"]:
                    print(f"  - {warning}")

            if result.get("recommendations"):
                print("\n💡 Recommendations:")
                for rec in result["recommendations"]:
                    print(f"  - {rec}")

        else:
            print("❌ Task validation failed!")
            if result.get("errors"):
                print("\n🔴 Errors:")
                for error in result["errors"]:
                    print(f"  - {error}")

            sys.exit(1)

    # Exit with appropriate code
    if not result["valid"]:
        sys.exit(1)
    elif args.strict and result.get("warnings"):
        print("\n❌ Strict mode: failing due to warnings")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()