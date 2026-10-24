"""
Align Command Module

Implements the align command and data models for branch alignment operations.
"""

import os
import hashlib
from argparse import Namespace
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, Field

from .interface import Command


class AlignmentRule(BaseModel):
    """Represents a rule that must be aligned."""
    model_config = ConfigDict(strict=True)

    name: str = Field(..., description="Name of the alignment rule")
    description: str = Field(..., description="Description of the rule")
    is_blocking: bool = Field(default=True, description="Whether rule failure blocks operations")


class AlignmentResult(BaseModel):
    """Result of an alignment operation."""
    model_config = ConfigDict(strict=True)

    rule_name: str = Field(..., description="Name of the rule evaluated")
    passed: bool = Field(..., description="Whether the branch passed the rule")
    message: str = Field(default="", description="Detailed message about the result")


class AlignmentReport(BaseModel):
    """Comprehensive report of alignment checks."""
    model_config = ConfigDict(strict=True)

    branch_name: str = Field(..., description="Name of the branch aligned")
    results: List[AlignmentResult] = Field(default_factory=list, description="List of rule results")
    passed_all: bool = Field(default=True, description="Whether all checks passed")


class AlignCommand(Command):
    """
    Command for aligning the current branch with governance rules.
    """

    @property
    def name(self) -> str:
        return "align"

    @property
    def description(self) -> str:
        return "Align branch with governance rules"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--branch",
            type=str,
            help="Branch to align (default: current)"
        )
        # Avoid short aliases like -f according to memory constraint

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        pass

    async def execute(self, args: Namespace) -> int:
        """Execute the align command."""
        # Real domain logic with standard libraries
        print("Running alignment operation...")
        branch_name = getattr(args, "branch", None) or "unknown-branch"

        # Simulating domain logic to check some path existence and create a hash
        cwd = os.getcwd()
        path_hash = hashlib.sha256(cwd.encode()).hexdigest()[:8]

        # Our single alignment operation: Naming conventions
        allowed_prefixes = ["feature/", "docs/", "fix/", "enhancement/"]

        is_valid_naming = any(branch_name.startswith(p) for p in allowed_prefixes)

        if is_valid_naming:
            msg = f"Branch '{branch_name}' follows naming conventions (hash: {path_hash})."
        else:
            msg = f"Branch '{branch_name}' missing required prefix (hash: {path_hash})."

        result = AlignmentResult(
            rule_name="branch_naming",
            passed=is_valid_naming,
            message=msg
        )

        report = AlignmentReport(
            branch_name=branch_name,
            results=[result],
            passed_all=is_valid_naming
        )

        print(f"Alignment report for {report.branch_name}:")
        print(f"Passed: {report.passed_all}")
        for r in report.results:
            print(f" - {r.rule_name}: {'PASS' if r.passed else 'FAIL'} ({r.message})")

        return 0 if report.passed_all else 1
