"""
Validation orchestrator module.
"""

import asyncio
from typing import Dict, Any, List

from ..core.interfaces import IValidator
from ..core.conflict_models import ValidationResult, ValidationStatus
from .test_runner import TestRunner

# from .security_scanner import SecurityScanner # Not yet implemented
from .quality_checker import QualityChecker
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ValidationOrchestrator(IValidator):
    """
    Orchestrates all validation checks.
    """

    def __init__(self):
        self.test_runner = TestRunner()
        # self.security_scanner = SecurityScanner()
        self.quality_checker = QualityChecker()

    async def validate(self, context: Dict[str, Any]) -> List[ValidationResult]:
        """
        Run all validators.
        """
        logger.info("Starting validation orchestration")

        results = []

        # Run validators in parallel
        # Convert coroutines to tasks to allow proper cancellation
        task_list = [
            asyncio.create_task(self.test_runner.run_tests(context)),
            # asyncio.create_task(self.security_scanner.scan(context)),
            asyncio.create_task(self.quality_checker.check(context)),
        ]

        timeout_seconds = 300.0  # Adjust timeout as needed

        try:
            validator_results = await asyncio.wait_for(
                asyncio.gather(*task_list, return_exceptions=True), timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            logger.error("Validation orchestration timed out")
            # Cancel all running tasks to prevent resource leaks
            for task in task_list:
                if not task.done():
                    task.cancel()
            # Wait briefly for cancellations to complete
            await asyncio.gather(*task_list, return_exceptions=True)
            return [
                ValidationResult(
                    component="Orchestrator",
                    status=ValidationStatus.ERROR,
                    details={"error": "Validation timeout"},
                    score=0.0,
                )
            ]

        for res in validator_results:
            if isinstance(res, ValidationResult):
                results.append(res)
            else:
                logger.error("Validator failed", error=str(res))
                results.append(
                    ValidationResult(
                        component="Unknown",
                        status=ValidationStatus.ERROR,
                        details={"error": str(res)},
                        score=0.0,
                    )
                )

        return results
