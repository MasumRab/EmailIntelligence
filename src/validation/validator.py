"""
Validator module for EmailIntelligence CLI

Implements validation functionality for various components.
"""

from typing import Any, Dict, List
from ..core.interfaces import IValidator
from ..core.conflict_models import ValidationResult
from ..utils.logger import get_logger


logger = get_logger(__name__)


class Validator(IValidator):
    """
    Main validator implementation that implements the IValidator interface.
    """
    
    def __init__(self):
        self.validators = {}
    
    async def validate(self, target: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """
        Validate the target object.
        
        Args:
            target: The object to validate
            context: Additional context for validation
            
        Returns:
            Validation result
        """
        logger.info(f"Starting validation for target of type: {type(target)}")
        
        errors = []
        warnings = []
        details = {}
        
        # Perform basic validation based on target type
        if target is None:
            errors.append("Target cannot be None")
        elif hasattr(target, '__dict__') or hasattr(target, '__slots__'):
            # Object validation
            errors.extend(self._validate_object(target))
        elif isinstance(target, (list, tuple)):
            # List/tuple validation
            errors.extend(self._validate_list(target))
        elif isinstance(target, dict):
            # Dictionary validation
            errors.extend(self._validate_dict(target))
        elif isinstance(target, str):
            # String validation
            errors.extend(self._validate_string(target))
        
        is_valid = len(errors) == 0
        
        result = ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details=details
        )
        
        logger.info(f"Validation completed. Valid: {is_valid}, Errors: {len(errors)}, Warnings: {len(warnings)}")
        return result
    
    def _validate_object(self, obj: Any) -> List[str]:
        """Validate an object."""
        errors = []
        
        # Check for required attributes if specified
        if hasattr(obj, '_required_fields'):
            for field in obj._required_fields:
                if not hasattr(obj, field) or getattr(obj, field) is None:
                    errors.append(f"Required field '{field}' is missing or None")
        
        return errors
    
    def _validate_list(self, lst: List) -> List[str]:
        """Validate a list."""
        errors = []
        
        # Check for None items
        for i, item in enumerate(lst):
            if item is None:
                errors.append(f"Item at index {i} is None")
        
        return errors
    
    def _validate_dict(self, d: Dict) -> List[str]:
        """Validate a dictionary."""
        errors = []
        
        # Check for None values
        for key, value in d.items():
            if value is None:
                errors.append(f"Value for key '{key}' is None")
        
        return errors
    
    def _validate_string(self, s: str) -> List[str]:
        """Validate a string."""
        errors = []
        
        # Check for empty string if not allowed
        if len(s) == 0:
            errors.append("String is empty")
        
        return errors


class ConstitutionalValidator(Validator):
    """
    Validator that specifically validates against constitutional requirements.
    """
    
    def __init__(self, constitution_file: str = None):
        super().__init__()
        self.constitution_file = constitution_file
    
    async def validate(self, target: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """
        Validate against constitutional requirements.
        """
        logger.info("Starting constitutional validation")
        
        # First run the base validation
        base_result = await super().validate(target, context)
        
        # Then run constitutional validation
        constitutional_errors = self._validate_constitutional(target, context)
        
        # Combine results
        all_errors = base_result.errors + constitutional_errors
        
        result = ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=base_result.warnings,
            details=base_result.details
        )
        
        logger.info(f"Constitutional validation completed. Valid: {result.is_valid}")
        return result
    
    def _validate_constitutional(self, target: Any, context: Dict[str, Any] = None) -> List[str]:
        """Perform constitutional validation."""
        errors = []
        
        # This would check against constitutional requirements
        # Implementation would depend on the specific constitution file
        if self.constitution_file:
            # Load and validate against constitution
            pass
        
        return errors