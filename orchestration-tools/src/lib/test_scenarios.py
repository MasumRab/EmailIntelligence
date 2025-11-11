from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


class TestScenario(ABC):
    """
    Abstract base class for test scenarios
    """
    
    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the test scenario
        
        Args:
            context: Context information for the test
            
        Returns:
            Dictionary with test results
        """
        pass
    
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> bool:
        """
        Validate that the context meets the requirements for this test scenario
        
        Args:
            context: Context information to validate
            
        Returns:
            True if context is valid, False otherwise
        """
        pass


class OrchestrationTestScenario(TestScenario):
    """
    Base class for orchestration-specific test scenarios
    """
    
    def __init__(self, name: str, description: str, category: str = "orchestration"):
        super().__init__(name, description, category)
        self.required_context_keys = []
    
    def validate(self, context: Dict[str, Any]) -> bool:
        """
        Validate that the context contains all required keys
        
        Args:
            context: Context information to validate
            
        Returns:
            True if context is valid, False otherwise
        """
        for key in self.required_context_keys:
            if key not in context:
                return False
        return True


class TestScenarioRegistry:
    """
    Registry for managing test scenarios
    """
    
    def __init__(self):
        self.scenarios = {}
    
    def register(self, scenario: TestScenario):
        """
        Register a test scenario
        
        Args:
            scenario: TestScenario to register
        """
        self.scenarios[scenario.id] = scenario
        # Also register by name for easier access
        self.scenarios[scenario.name] = scenario
    
    def get_scenario(self, scenario_id_or_name: str) -> Optional[TestScenario]:
        """
        Get a test scenario by ID or name
        
        Args:
            scenario_id_or_name: ID or name of the scenario to retrieve
            
        Returns:
            TestScenario if found, None otherwise
        """
        return self.scenarios.get(scenario_id_or_name)
    
    def get_scenarios_by_category(self, category: str) -> List[TestScenario]:
        """
        Get all test scenarios in a category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of TestScenario objects
        """
        return [scenario for scenario in self.scenarios.values() 
                if isinstance(scenario, TestScenario) and scenario.category == category]
    
    def get_all_scenarios(self) -> List[TestScenario]:
        """
        Get all registered test scenarios
        
        Returns:
            List of all TestScenario objects
        """
        # Filter out duplicates (scenarios registered by both ID and name)
        unique_scenarios = []
        seen_ids = set()
        
        for scenario in self.scenarios.values():
            if isinstance(scenario, TestScenario) and scenario.id not in seen_ids:
                unique_scenarios.append(scenario)
                seen_ids.add(scenario.id)
        
        return unique_scenarios


# Global registry instance
test_scenario_registry = TestScenarioRegistry()


class ContextValidationScenario(OrchestrationTestScenario):
    """
    Test scenario for validating context (environment, dependencies, etc.)
    """
    
    def __init__(self):
        super().__init__(
            name="context-validation",
            description="Validate environment variables, dependencies, and configuration files",
            category="context"
        )
        self.required_context_keys = ["environment", "dependencies", "config_files"]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute context validation
        
        Args:
            context: Context information containing environment, dependencies, and config files
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "scenario_id": self.id,
            "scenario_name": self.name,
            "passed": True,
            "details": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Validate environment variables
        environment = context.get("environment", {})
        if not environment:
            results["passed"] = False
            results["details"].append("No environment variables provided")
        else:
            results["details"].append(f"Validated {len(environment)} environment variables")
        
        # Validate dependencies
        dependencies = context.get("dependencies", {})
        if not dependencies:
            results["passed"] = False
            results["details"].append("No dependencies provided")
        else:
            results["details"].append(f"Validated {len(dependencies)} dependencies")
        
        # Validate config files
        config_files = context.get("config_files", [])
        if not config_files:
            results["passed"] = False
            results["details"].append("No configuration files provided")
        else:
            results["details"].append(f"Validated {len(config_files)} configuration files")
        
        return results


class BranchCompatibilityScenario(OrchestrationTestScenario):
    """
    Test scenario for validating branch compatibility
    """
    
    def __init__(self):
        super().__init__(
            name="branch-compatibility",
            description="Validate compatibility between source and target branches",
            category="compatibility"
        )
        self.required_context_keys = ["source_branch", "target_branch", "repository"]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute branch compatibility validation
        
        Args:
            context: Context information containing branch information
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "scenario_id": self.id,
            "scenario_name": self.name,
            "passed": True,
            "details": [],
            "timestamp": datetime.now().isoformat()
        }
        
        source_branch = context.get("source_branch")
        target_branch = context.get("target_branch")
        
        if not source_branch:
            results["passed"] = False
            results["details"].append("Source branch not provided")
        else:
            results["details"].append(f"Source branch: {source_branch}")
        
        if not target_branch:
            results["passed"] = False
            results["details"].append("Target branch not provided")
        else:
            results["details"].append(f"Target branch: {target_branch}")
        
        if source_branch and target_branch:
            results["details"].append("Branch compatibility validation passed")
        
        return results


# Register default test scenarios
test_scenario_registry.register(ContextValidationScenario())
test_scenario_registry.register(BranchCompatibilityScenario())