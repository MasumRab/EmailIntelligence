import pytest
from src.core.validation_integration import (
    ValidationIntegrationFramework,
    ValidationPlugin,
    ValidationResult
)

class ExampleValidationPlugin(ValidationPlugin):
    """An example validation plugin for testing."""
    
    def get_name(self) -> str:
        return "pre_alignment"
        
    def run_check(self, branch_name: str) -> ValidationResult:
        if branch_name == "invalid-branch":
            return ValidationResult(
                status="failed",
                checks_completed=1,
                errors_found=1,
                warnings_found=0
            )
        
        return ValidationResult(
            status="passed",
            checks_completed=5,
            errors_found=0,
            warnings_found=1
        )

def test_validation_framework_register_and_run():
    framework = ValidationIntegrationFramework()
    
    # Register the example plugin
    plugin = ExampleValidationPlugin()
    framework.register_plugin(plugin)
    
    # Run the validation on a valid branch
    result = framework.run_pre_alignment_validation("feature/auth")
    
    assert result["branch_name"] == "feature/auth"
    assert result["overall_status"] == "passed"
    assert result["aggregated_score"] == 1.0
    
    phases = result["validation_phases"]
    assert "pre_alignment" in phases
    assert phases["pre_alignment"]["status"] == "passed"
    assert phases["pre_alignment"]["checks_completed"] == 5
    assert phases["pre_alignment"]["errors_found"] == 0
    assert phases["pre_alignment"]["warnings_found"] == 1
    
    # Run the validation on an invalid branch
    result_invalid = framework.run_pre_alignment_validation("invalid-branch")
    
    assert result_invalid["branch_name"] == "invalid-branch"
    assert result_invalid["overall_status"] == "failed"
    assert result_invalid["aggregated_score"] < 1.0
    
    phases_invalid = result_invalid["validation_phases"]
    assert phases_invalid["pre_alignment"]["status"] == "failed"
    assert phases_invalid["pre_alignment"]["errors_found"] == 1
