"""
Test runner module for validation.
"""

import asyncio
import re
from typing import Dict, Any
from pathlib import Path

from ..core.conflict_models import ValidationResult, ValidationStatus
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TestRunner:
    """
    Runs tests to validate code changes.
    """

    async def run_tests(self, context: Dict[str, Any]) -> ValidationResult:
        """
        Run tests relevant to the context.
        """
        logger.info("Running tests", context=context)

        # Determine which tests to run
        # If specific files are changed, we might want to run related tests
        # For now, we'll run all unit tests as a baseline

        try:
            # Validate test directory exists
            test_dir = Path("tests/unit")
            if not test_dir.is_dir():
                logger.error("Test directory not found", path=str(test_dir))
                return ValidationResult(
                    component="TestRunner",
                    status=ValidationStatus.ERROR,
                    details={"error": f"Test directory '{test_dir}' not found"},
                    score=0.0,
                )

            # Construct pytest command
            cmd = ["pytest", str(test_dir), "-v", "--junitxml=test-results.xml"]

            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            output = stdout.decode() + stderr.decode()

            success = process.returncode == 0

            # Parse output for details
            details = self._parse_pytest_output(output)

            return ValidationResult(
                component="TestRunner",
                status=ValidationStatus.PASSED if success else ValidationStatus.FAILED,
                details=details,
                score=1.0 if success else 0.0,
            )

        except Exception as e:
            logger.error("Test execution failed", error=str(e))
            return ValidationResult(
                component="TestRunner",
                status=ValidationStatus.ERROR,
                details={"error": str(e)},
                score=0.0,
            )

    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Parse pytest output for metrics."""
        # Simple regex parsing
        # Example: "=== 15 passed, 2 failed in 0.12s ==="
        match = re.search(r"===\s+(.*?)\s+===", output.splitlines()[-1] if output else "")

        summary = match.group(1) if match else "Unknown"

        return {"raw_output": output[:1000], "summary": summary}  # Truncate for safety
