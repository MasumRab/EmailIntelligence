
"""
Validation orchestrator module.
"""

import asyncio
from typing import Dict, Any, List

from ..core.interfaces import IValidator
from ..core.models import ValidationResult, ValidationStatus
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
        tasks = [
            self.test_runner.run_tests(context),
            # self.security_scanner.scan(context),
            self.quality_checker.check(context)
        ]
        
        validator_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in validator_results:
            if isinstance(res, ValidationResult):
                results.append(res)
            else:
                logger.error("Validator failed", error=str(res))
                results.append(ValidationResult(
                    component="Unknown",
                    status=ValidationStatus.ERROR,
                    details={"error": str(res)},
                    score=0.0
                ))
                
        return results
