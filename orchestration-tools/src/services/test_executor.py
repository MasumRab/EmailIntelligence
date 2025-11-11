from typing import Dict, Any, List
from datetime import datetime
import uuid
from ..lib.test_scenarios import TestScenario, TestScenarioRegistry, test_scenario_registry
from ..lib.error_handling import logger


class TestExecutionResult:
    """
    Represents the result of executing a test scenario
    """
    
    def __init__(self, scenario_name: str, passed: bool, details: List[str], execution_time: float = 0.0):
        self.id = str(uuid.uuid4())
        self.scenario_name = scenario_name
        self.passed = passed
        self.details = details
        self.timestamp = datetime.now()
        self.execution_time = execution_time  # Execution time in seconds


class TestExecutor:
    """
    Engine for executing test scenarios
    """
    
    def __init__(self, registry: TestScenarioRegistry = None):
        self.registry = registry or test_scenario_registry
        self.results = {}
    
    def execute_scenario(self, scenario_id_or_name: str, context: Dict[str, Any], correlation_id: str = None) -> TestExecutionResult:
        """
        Execute a single test scenario
        
        Args:
            scenario_id_or_name: ID or name of the scenario to execute
            context: Context information for the test
            correlation_id: Correlation ID for logging
            
        Returns:
            TestExecutionResult with execution results
        """
        if correlation_id:
            logger.info(f"Executing test scenario: {scenario_id_or_name}", correlation_id)
        
        # Get the scenario
        scenario = self.registry.get_scenario(scenario_id_or_name)
        if not scenario:
            error_msg = f"Test scenario '{scenario_id_or_name}' not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return TestExecutionResult(scenario_name=scenario_id_or_name, passed=False, details=[error_msg])
        
        # Validate context
        if not scenario.validate(context):
            error_msg = f"Context validation failed for scenario '{scenario.name}'"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return TestExecutionResult(scenario_name=scenario.name, passed=False, details=[error_msg])
        
        # Execute the scenario
        start_time = datetime.now()
        try:
            result = scenario.execute(context)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            scenario_result = TestExecutionResult(
                scenario_name=scenario.name,
                passed=result.get("passed", False),
                details=result.get("details", []),
                execution_time=execution_time
            )
            
            if correlation_id:
                status = "PASSED" if scenario_result.passed else "FAILED"
                logger.info(f"Test scenario '{scenario.name}' {status}", correlation_id)
            
            # Store result
            self.results[scenario_result.id] = scenario_result
            return scenario_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Error executing scenario '{scenario.name}': {str(e)}"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            
            scenario_result = TestExecutionResult(
                scenario_name=scenario.name,
                passed=False,
                details=[error_msg],
                execution_time=execution_time
            )
            
            # Store result
            self.results[scenario_result.id] = scenario_result
            return scenario_result
    
    def execute_scenarios(self, scenario_ids_or_names: List[str], context: Dict[str, Any], correlation_id: str = None) -> List[TestExecutionResult]:
        """
        Execute multiple test scenarios
        
        Args:
            scenario_ids_or_names: List of scenario IDs or names to execute
            context: Context information for the tests
            correlation_id: Correlation ID for logging
            
        Returns:
            List of TestExecutionResult objects
        """
        results = []
        
        for scenario_id in scenario_ids_or_names:
            result = self.execute_scenario(scenario_id, context, correlation_id)
            results.append(result)
        
        return results
    
    def execute_scenarios_by_category(self, category: str, context: Dict[str, Any], correlation_id: str = None) -> List[TestExecutionResult]:
        """
        Execute all test scenarios in a specific category
        
        Args:
            category: Category of scenarios to execute
            context: Context information for the tests
            correlation_id: Correlation ID for logging
            
        Returns:
            List of TestExecutionResult objects
        """
        scenarios = self.registry.get_scenarios_by_category(category)
        results = []
        
        for scenario in scenarios:
            result = self.execute_scenario(scenario.id, context, correlation_id)
            results.append(result)
        
        return results
    
    def execute_all_scenarios(self, context: Dict[str, Any], correlation_id: str = None) -> List[TestExecutionResult]:
        """
        Execute all registered test scenarios
        
        Args:
            context: Context information for the tests
            correlation_id: Correlation ID for logging
            
        Returns:
            List of TestExecutionResult objects
        """
        scenarios = self.registry.get_all_scenarios()
        results = []
        
        for scenario in scenarios:
            result = self.execute_scenario(scenario.id, context, correlation_id)
            results.append(result)
        
        return results
    
    def get_result(self, result_id: str) -> TestExecutionResult:
        """
        Get a specific test execution result
        
        Args:
            result_id: ID of the result to retrieve
            
        Returns:
            TestExecutionResult if found, None otherwise
        """
        return self.results.get(result_id)
    
    def get_all_results(self) -> List[TestExecutionResult]:
        """
        Get all test execution results
        
        Returns:
            List of all TestExecutionResult objects
        """
        return list(self.results.values())


# Global test executor instance
test_executor = TestExecutor()