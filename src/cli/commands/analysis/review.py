"""
Code Review Command Module

Wraps the CodeRabbit CLI to provide automated, AI-driven code reviews.
Defaults to incremental reviews (HEAD vs HEAD~1) to maintain technical integrity.
"""

import subprocess
from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class ReviewCommand(Command):
    """
    Command for performing AI-driven code reviews via CodeRabbit.
    
    Defaults to 'Incremental Mode' (comparing against the previous commit 
    on the current branch) to avoid massive changeset overhead.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "code-review"

    @property
    def description(self) -> str:
        return "Perform AI-driven code review of recent changes (Incremental)"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--base", 
            default="HEAD~1",
            help="Base commit/branch to compare against (default: HEAD~1)"
        )
        parser.add_argument(
            "--type", 
            choices=["all", "committed", "uncommitted"],
            default="committed",
            help="Review type"
        )
        parser.add_argument(
            "--full", 
            action="store_true", 
            help="Review against origin/main (Full branch review)"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    async def execute(self, args: Namespace) -> int:
        """Execute the CodeRabbit review."""
        base = "origin/main" if args.full else args.base
        
        print(f"🐇 Initiating CodeRabbit Review...")
        print(f"   Context: Current HEAD vs {base}")
        print(f"   Mode: {args.type}")

        cmd = [
            "coderabbit", "review",
            "-t", args.type,
            "--base-commit" if not args.full else "--base", base,
            "--plain"
        ]

        try:
            # Check if coderabbit is installed
            subprocess.run(["which", "coderabbit"], check=True, capture_output=True)
            
            # Run the review
            result = subprocess.run(cmd, capture_output=False, text=True)
            return result.returncode
        except subprocess.CalledProcessError:
            print("Error: 'coderabbit' CLI not found. Please install it first.")
            return 1
        except Exception as e:
            print(f"Error during review execution: {e}")
            return 1
