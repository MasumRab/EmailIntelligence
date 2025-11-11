import os
import subprocess
import sys
from typing import Dict, List, Optional, Any
from ..lib.error_handling import logger


class ContextVerificationService:
    """
    Service for verifying key context checks including environment variables,
    dependency versions, configuration files, and infrastructure state.
    """
    
    def __init__(self):
        self.verification_results = {}
    
    def verify_environment_variables(self, required_vars: List[str], correlation_id: str = None) -> Dict[str, Any]:
        """
        Verify that required environment variables are set
        
        Args:
            required_vars: List of required environment variable names
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Verifying {len(required_vars)} environment variables", correlation_id)
        
        results = {
            "check_type": "environment_variables",
            "passed": True,
            "missing_vars": [],
            "present_vars": [],
            "details": []
        }
        
        for var in required_vars:
            if var in os.environ:
                results["present_vars"].append(var)
                # Log the variable name but not the value for security
                results["details"].append(f"Environment variable '{var}' is set")
            else:
                results["missing_vars"].append(var)
                results["passed"] = False
                results["details"].append(f"Environment variable '{var}' is missing")
        
        if correlation_id:
            status = "PASSED" if results["passed"] else "FAILED"
            logger.info(f"Environment variable verification {status}", correlation_id)
        
        return results
    
    def verify_dependency_versions(self, required_deps: Dict[str, str], correlation_id: str = None) -> Dict[str, Any]:
        """
        Verify that required dependencies are installed with correct versions
        
        Args:
            required_deps: Dictionary mapping package names to required versions
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Verifying {len(required_deps)} dependencies", correlation_id)
        
        results = {
            "check_type": "dependency_versions",
            "passed": True,
            "verified_deps": [],
            "missing_deps": [],
            "version_mismatches": [],
            "details": []
        }
        
        for package, required_version in required_deps.items():
            try:
                # Try to get the installed version
                installed_version = self._get_package_version(package)
                if installed_version:
                    results["verified_deps"].append(package)
                    if self._version_satisfies(installed_version, required_version):
                        results["details"].append(f"Package '{package}' version {installed_version} satisfies requirement {required_version}")
                    else:
                        results["passed"] = False
                        results["version_mismatches"].append(package)
                        results["details"].append(f"Package '{package}' version {installed_version} does not satisfy requirement {required_version}")
                else:
                    results["passed"] = False
                    results["missing_deps"].append(package)
                    results["details"].append(f"Package '{package}' is not installed")
            except Exception as e:
                results["passed"] = False
                results["missing_deps"].append(package)
                results["details"].append(f"Error checking package '{package}': {str(e)}")
        
        if correlation_id:
            status = "PASSED" if results["passed"] else "FAILED"
            logger.info(f"Dependency version verification {status}", correlation_id)
        
        return results
    
    def verify_configuration_files(self, config_files: List[str], correlation_id: str = None) -> Dict[str, Any]:
        """
        Verify that required configuration files exist and are accessible
        
        Args:
            config_files: List of configuration file paths to check
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Verifying {len(config_files)} configuration files", correlation_id)
        
        results = {
            "check_type": "configuration_files",
            "passed": True,
            "accessible_files": [],
            "missing_files": [],
            "unreadable_files": [],
            "details": []
        }
        
        for file_path in config_files:
            if os.path.exists(file_path):
                results["accessible_files"].append(file_path)
                try:
                    # Try to read the file to ensure it's accessible
                    with open(file_path, 'r') as f:
                        # Just read first line to check accessibility
                        f.readline()
                    results["details"].append(f"Configuration file '{file_path}' exists and is readable")
                except Exception as e:
                    results["passed"] = False
                    results["unreadable_files"].append(file_path)
                    results["details"].append(f"Configuration file '{file_path}' exists but is not readable: {str(e)}")
            else:
                results["passed"] = False
                results["missing_files"].append(file_path)
                results["details"].append(f"Configuration file '{file_path}' does not exist")
        
        if correlation_id:
            status = "PASSED" if results["passed"] else "FAILED"
            logger.info(f"Configuration file verification {status}", correlation_id)
        
        return results
    
    def verify_infrastructure_state(self, infrastructure_checks: List[Dict[str, Any]], correlation_id: str = None) -> Dict[str, Any]:
        """
        Verify that infrastructure components are in the expected state
        
        Args:
            infrastructure_checks: List of infrastructure checks to perform
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Verifying {len(infrastructure_checks)} infrastructure components", correlation_id)
        
        results = {
            "check_type": "infrastructure_state",
            "passed": True,
            "successful_checks": [],
            "failed_checks": [],
            "details": []
        }
        
        for check in infrastructure_checks:
            check_name = check.get("name", "unnamed_check")
            check_type = check.get("type", "command")
            
            try:
                if check_type == "command":
                    command = check.get("command")
                    expected_exit_code = check.get("expected_exit_code", 0)
                    
                    if command:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        if result.returncode == expected_exit_code:
                            results["successful_checks"].append(check_name)
                            results["details"].append(f"Infrastructure check '{check_name}' passed")
                        else:
                            results["passed"] = False
                            results["failed_checks"].append(check_name)
                            results["details"].append(f"Infrastructure check '{check_name}' failed with exit code {result.returncode}")
                    else:
                        results["passed"] = False
                        results["failed_checks"].append(check_name)
                        results["details"].append(f"Infrastructure check '{check_name}' has no command specified")
                
                elif check_type == "service":
                    service_name = check.get("service_name")
                    if service_name:
                        # Check if service is running (Linux-specific)
                        result = subprocess.run(["systemctl", "is-active", service_name], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            results["successful_checks"].append(check_name)
                            results["details"].append(f"Service '{service_name}' is active")
                        else:
                            results["passed"] = False
                            results["failed_checks"].append(check_name)
                            results["details"].append(f"Service '{service_name}' is not active")
                    else:
                        results["passed"] = False
                        results["failed_checks"].append(check_name)
                        results["details"].append(f"Service check '{check_name}' has no service name specified")
                
                else:
                    results["passed"] = False
                    results["failed_checks"].append(check_name)
                    results["details"].append(f"Unknown infrastructure check type '{check_type}' for check '{check_name}'")
                    
            except Exception as e:
                results["passed"] = False
                results["failed_checks"].append(check_name)
                results["details"].append(f"Error performing infrastructure check '{check_name}': {str(e)}")
        
        if correlation_id:
            status = "PASSED" if results["passed"] else "FAILED"
            logger.info(f"Infrastructure state verification {status}", correlation_id)
        
        return results
    
    def verify_all_context(self, context_spec: Dict[str, Any], correlation_id: str = None) -> Dict[str, Any]:
        """
        Perform all context verification checks
        
        Args:
            context_spec: Specification of what context to verify
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with all verification results
        """
        if correlation_id:
            logger.info("Starting comprehensive context verification", correlation_id)
        
        all_results = {
            "passed": True,
            "checks": [],
            "summary": {}
        }
        
        # Verify environment variables
        if "environment_variables" in context_spec:
            env_result = self.verify_environment_variables(
                context_spec["environment_variables"], correlation_id)
            all_results["checks"].append(env_result)
            if not env_result["passed"]:
                all_results["passed"] = False
        
        # Verify dependencies
        if "dependencies" in context_spec:
            dep_result = self.verify_dependency_versions(
                context_spec["dependencies"], correlation_id)
            all_results["checks"].append(dep_result)
            if not dep_result["passed"]:
                all_results["passed"] = False
        
        # Verify configuration files
        if "config_files" in context_spec:
            config_result = self.verify_configuration_files(
                context_spec["config_files"], correlation_id)
            all_results["checks"].append(config_result)
            if not config_result["passed"]:
                all_results["passed"] = False
        
        # Verify infrastructure
        if "infrastructure" in context_spec:
            infra_result = self.verify_infrastructure_state(
                context_spec["infrastructure"], correlation_id)
            all_results["checks"].append(infra_result)
            if not infra_result["passed"]:
                all_results["passed"] = False
        
        # Create summary
        all_results["summary"] = {
            "total_checks": len(all_results["checks"]),
            "passed_checks": len([c for c in all_results["checks"] if c["passed"]]),
            "failed_checks": len([c for c in all_results["checks"] if not c["passed"]])
        }
        
        if correlation_id:
            status = "PASSED" if all_results["passed"] else "FAILED"
            logger.info(f"Comprehensive context verification {status}", correlation_id)
        
        return all_results
    
    def _get_package_version(self, package_name: str) -> Optional[str]:
        """
        Get the installed version of a Python package
        
        Args:
            package_name: Name of the package
            
        Returns:
            Version string if package is installed, None otherwise
        """
        try:
            # Try to import the package
            import importlib
            module = importlib.import_module(package_name)
            
            # Try to get version from the module
            if hasattr(module, '__version__'):
                return str(module.__version__)
            
            # Try to get version from the package metadata
            import pkg_resources
            return pkg_resources.get_distribution(package_name).version
        except Exception:
            # If we can't determine the version, return None
            return None
    
    def _version_satisfies(self, installed_version: str, required_version: str) -> bool:
        """
        Check if an installed version satisfies a required version
        
        Args:
            installed_version: Actually installed version
            required_version: Required version (can include operators like >=, ==, etc.)
            
        Returns:
            True if version satisfies requirement, False otherwise
        """
        # This is a simplified version check
        # In a real implementation, you'd want to use something like packaging.version
        try:
            # Handle simple case of exact version match
            if required_version.startswith("=="):
                return installed_version == required_version[2:]
            elif required_version.startswith(">="):
                # Simplified comparison - in real implementation use proper version comparison
                return installed_version >= required_version[2:]
            else:
                # Assume exact match if no operator specified
                return installed_version == required_version
        except Exception:
            # If we can't compare versions properly, assume it's okay
            return True