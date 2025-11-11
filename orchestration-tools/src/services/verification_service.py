import uuid
from datetime import datetime
from typing import Optional, Dict, List
from ..models.verification import VerificationResult, VerificationStatus, ReviewStatus
from ..models.user import User
from ..services.auth_service import AuthService
from ..services.git_service import GitService
from ..services.config_service import ConfigService
from ..services.context_verification_service import ContextVerificationService
from ..lib.error_handling import logger
from ..services.test_executor import TestExecutor, TestExecutionResult
from ..lib.test_scenarios import test_scenario_registry


class VerificationService:
    """
    Service for running and managing verifications
    """
    
    def __init__(self, auth_service: AuthService, git_service: GitService, config_service: ConfigService):
        self.auth_service = auth_service
        self.git_service = git_service
        self.config_service = config_service
        self.test_executor = TestExecutor()
        self.context_verification_service = ContextVerificationService()
        self.verification_results = {}  # In-memory storage for verification results
    
    def run_verification(self, source_branch: str, target_branch: str, profile_name: Optional[str] = None) -> VerificationResult:
        """
        Run verification for a branch against a target branch
        
        Args:
            source_branch: Name of the source branch
            target_branch: Name of the target branch
            profile_name: Name of the verification profile to use (optional)
            
        Returns:
            VerificationResult with the verification results
        """
        correlation_id = str(uuid.uuid4())
        logger.info(f"Starting verification: {source_branch} -> {target_branch}", correlation_id)
        
        # Determine profile to use
        if not profile_name:
            target_branch_info = self.git_service.get_branch_info(target_branch)
            if target_branch_info:
                target_type = target_branch_info.type.value
                profile = self.config_service.get_profile_for_branch_type(target_type)
                if profile:
                    profile_name = profile.name
            else:
                # Fallback to default profile
                profile_name = "feature-branch"
        
        # Create verification result
        verification_id = str(uuid.uuid4())
        result = VerificationResult(
            id=verification_id,
            branch_name=source_branch,
            target_branch=target_branch,
            status=VerificationStatus.PENDING,
            timestamp=datetime.now(),
            initiator="cli_user",  # In a real implementation, this would be the authenticated user
            profile=profile_name,
            correlation_id=correlation_id
        )
        
        # Store the result
        self.verification_results[verification_id] = result
        
        # Simulate running verification checks
        result.status = VerificationStatus.RUNNING
        self.verification_results[verification_id] = result
        
        # Get the profile
        profile = self.config_service.get_verification_profile(profile_name)
        if profile:
            # Prepare context for test scenarios
            context = {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "environment": {},  # In a real implementation, this would contain actual environment data
                "dependencies": {},  # In a real implementation, this would contain actual dependency data
                "config_files": []  # In a real implementation, this would contain actual config file data
            }
            
            # Perform context verification if required
            context_verification_passed = True
            context_verification_details = []
            
            if "context-check" in profile.required_checks or "context-check" in profile.context_requirements:
                logger.info("Performing context verification", correlation_id)
                
                # Define context specification based on profile
                context_spec = {
                    "environment_variables": ["PATH", "HOME"],  # Example required vars
                    "dependencies": {
                        "GitPython": ">=3.1.0",
                        "PyYAML": ">=6.0"
                    },
                    "config_files": [
                        "config/verification_profiles.yaml",
                        "config/auth_config.yaml"
                    ]
                }
                
                context_result = self.context_verification_service.verify_all_context(context_spec, correlation_id)
                context_verification_passed = context_result["passed"]
                context_verification_details = context_result.get("details", [])
                
                # Add context verification details to overall context
                context["context_verification"] = context_result
            
            # Execute required test scenarios if context verification passed
            required_scenario_results = []
            failed_scenarios = []
            
            if context_verification_passed:
                for check_name in profile.required_checks:
                    # Skip context-check since we already performed it
                    if check_name == "context-check":
                        continue
                    
                    # Execute the test scenario
                    scenario_result = self.test_executor.execute_scenario(check_name, context, correlation_id)
                    required_scenario_results.append(scenario_result)
                    
                    if not scenario_result.passed:
                        failed_scenarios.append(scenario_result.scenario_name)
            
            # Execute optional test scenarios
            optional_scenario_results = []
            for check_name in profile.optional_checks:
                # Execute the test scenario
                scenario_result = self.test_executor.execute_scenario(check_name, context, correlation_id)
                optional_scenario_results.append(scenario_result)
            
            # Update result with check details
            all_results = required_scenario_results + optional_scenario_results
            passed_checks = [r.scenario_name for r in all_results if r.passed]
            failed_checks = [r.scenario_name for r in all_results if not r.passed]
            
            # Include context check in results if it was performed
            if "context-check" in profile.required_checks or "context-check" in profile.context_requirements:
                if context_verification_passed:
                    passed_checks.append("context-check")
                else:
                    failed_checks.append("context-check")
            
            result.details = {
                "passed_checks": passed_checks,
                "failed_checks": failed_checks,
                "total_scenarios": len(all_results),
                "passed_scenarios": len(passed_checks),
                "failed_scenarios": len(failed_checks),
                "context_verification_details": context_verification_details
            }
            
            # Determine overall status
            if context_verification_passed and len(failed_scenarios) == 0:
                result.status = VerificationStatus.PASS
                result.report = f"All {len(passed_checks)} checks passed successfully"
            else:
                failed_items = []
                if not context_verification_passed:
                    failed_items.append("context verification")
                if failed_scenarios:
                    failed_items.append(f"{len(failed_scenarios)} scenarios")
                
                result.status = VerificationStatus.FAIL
                result.report = f"Verification failed: {', '.join(failed_items)}"
        else:
            # Profile not found, fail verification
            result.status = VerificationStatus.FAIL
            result.report = f"Verification profile '{profile_name}' not found"
        
        result.completed_at = datetime.now()
        self.verification_results[verification_id] = result
        
        logger.info(f"Verification completed with status: {result.status}", correlation_id)
        
        return result
    
    def get_verification_result(self, verification_id: str) -> Optional[VerificationResult]:
        """
        Get a verification result by ID
        
        Args:
            verification_id: ID of the verification result to retrieve
            
        Returns:
            VerificationResult if found, None otherwise
        """
        return self.verification_results.get(verification_id)
    
    def approve_verification(self, verification_id: str, approver: User, comment: Optional[str] = None) -> Optional[VerificationResult]:
        """
        Approve a verification result
        
        Args:
            verification_id: ID of the verification to approve
            approver: User who is approving the verification
            comment: Optional comment for the approval
            
        Returns:
            Updated VerificationResult if successful, None if verification not found
        """
        result = self.get_verification_result(verification_id)
        if not result:
            return None
        
        # Check if user has permission to approve
        if not self.auth_service.has_role(approver, "REVIEW"):
            raise Exception("User does not have permission to approve verifications")
        
        # Update result
        result.review_status = ReviewStatus.APPROVED
        result.approved_by = approver.username
        result.approved_at = datetime.now()
        if comment:
            result.report += f"\nApproved by {approver.username}: {comment}"
        
        self.verification_results[verification_id] = result
        return result
    
    def reject_verification(self, verification_id: str, rejector: User, comment: str) -> Optional[VerificationResult]:
        """
        Reject a verification result
        
        Args:
            verification_id: ID of the verification to reject
            rejector: User who is rejecting the verification
            comment: Required comment for the rejection
            
        Returns:
            Updated VerificationResult if successful, None if verification not found
        """
        result = self.get_verification_result(verification_id)
        if not result:
            return None
        
        # Check if user has permission to reject
        if not self.auth_service.has_role(rejector, "REVIEW"):
            raise Exception("User does not have permission to reject verifications")
        
        # Update result
        result.review_status = ReviewStatus.REJECTED
        result.rejected_by = rejector.username
        result.rejected_at = datetime.now()
        if comment:
            result.report += f"\nRejected by {rejector.username}: {comment}"
        
        self.verification_results[verification_id] = result
        return result
    
    def get_branch_verifications(self, branch_name: str) -> List[VerificationResult]:
        """
        Get all verification results for a specific branch
        
        Args:
            branch_name: Name of the branch to get verifications for
            
        Returns:
            List of VerificationResult objects for the branch
        """
        results = []
        for result in self.verification_results.values():
            if result.branch_name == branch_name:
                results.append(result)
        return results
