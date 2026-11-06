import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ValidationResult:
    """Result of a single validation plugin or an aggregated check."""
    status: str
    checks_completed: int = 0
    errors_found: int = 0
    warnings_found: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

class ValidationPlugin(ABC):
    """Abstract interface for a validation integration plugin."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the name of the plugin."""
        pass

    @abstractmethod
    def run_check(self, branch_name: str) -> ValidationResult:
        """Runs the validation check and returns the result."""
        pass

class ValidationIntegrationFramework:
    """Minimal validation integration framework for Task 017."""

    def __init__(self, repo_path: str = ".", config_path: str = None):
        self.repo_path = repo_path
        self.config_path = config_path
        self.plugins: List[ValidationPlugin] = []

    def register_plugin(self, plugin: ValidationPlugin):
        """Registers a new validation plugin."""
        self.plugins.append(plugin)

    def run_pre_alignment_validation(self, branch_name: str) -> Dict[str, Any]:
        """Runs all registered pre-alignment validation checks."""
        start_time = time.time()

        phases = {}
        total_checks = 0
        total_errors = 0
        total_warnings = 0

        for plugin in self.plugins:
            result = plugin.run_check(branch_name)
            phases[plugin.get_name()] = {
                "status": result.status,
                "checks_completed": result.checks_completed,
                "errors_found": result.errors_found,
                "warnings_found": result.warnings_found,
            }
            total_checks += result.checks_completed
            total_errors += result.errors_found
            total_warnings += result.warnings_found

        overall_status = "passed" if total_errors == 0 else "failed"

        # Simple scoring logic: 1.0 if no errors, decrease by 0.1 per error
        aggregated_score = max(0.0, 1.0 - (total_errors * 0.1))

        return {
            "branch_name": branch_name,
            "validation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "validation_phases": phases,
            "aggregated_score": aggregated_score,
            "overall_status": overall_status,
            "execution_time_seconds": round(time.time() - start_time, 2)
        }
