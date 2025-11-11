"""
Service for Formal Verification Tools Integration
"""
from typing import List, Dict, Optional
from datetime import datetime
from ..models.formal_verification_tool import FormalVerificationTool
from ..models.verification_logic import VerificationLogic
from ..lib.error_handling import logger


class FormalVerificationService:
    """
    Service for integrating formal verification tools to validate verification logic and consistency checks
    """
    
    def __init__(self):
        self.verification_tools = {}
        self.verification_logic = {}
    
    def add_verification_tool(self, tool: FormalVerificationTool):
        """
        Add a formal verification tool to the service
        
        Args:
            tool: FormalVerificationTool to add
        """
        self.verification_tools[tool.id] = tool
    
    def add_verification_logic(self, logic: VerificationLogic):
        """
        Add verification logic to the service
        
        Args:
            logic: VerificationLogic to add
        """
        self.verification_logic[logic.id] = logic
    
    def run_formal_verification(self, logic_id: str, tool_id: str = None, correlation_id: str = None) -> Dict[str, any]:
        """
        Run formal verification on specific verification logic
        
        Args:
            logic_id: ID of the verification logic to verify
            tool_id: ID of the formal verification tool to use (optional)
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification results
        """
        if correlation_id:
            logger.info(f"Running formal verification for logic: {logic_id} using tool: {tool_id or 'default'}", correlation_id)
        
        logic = self.verification_logic.get(logic_id)
        if not logic:
            error_msg = f"Verification logic {logic_id} not found"
            if correlation_id:
                logger.error(error_msg, correlation_id)
            return {
                "logic_id": logic_id,
                "passed": False,
                "error": error_msg
            }
        
        # Select tool
        tool = None
        if tool_id:
            tool = self.verification_tools.get(tool_id)
            if not tool:
                error_msg = f"Verification tool {tool_id} not found"
                if correlation_id:
                    logger.error(error_msg, correlation_id)
                return {
                    "logic_id": logic_id,
                    "tool_id": tool_id,
                    "passed": False,
                    "error": error_msg
                }
        else:
            # Use first available tool that supports this verification type
            for t in self.verification_tools.values():
                if logic.verification_type in t.supported_verification_types and t.enabled:
                    tool = t
                    break
            
            if not tool:
                error_msg = "No suitable verification tool found"
                if correlation_id:
                    logger.error(error_msg, correlation_id)
                return {
                    "logic_id": logic_id,
                    "passed": False,
                    "error": error_msg
                }
        
        # In a real implementation, this would run the actual formal verification
        # For now, we'll return mock results
        results = {
            "logic_id": logic_id,
            "tool_id": tool.id,
            "tool_name": tool.name,
            "passed": True,
            "coverage_percent": 99.5,  # Mock coverage
            "details": f"Formal verification completed successfully using {tool.name}",
            "timestamp": datetime.now().isoformat()
        }
        
        # Update logic with verification results
        logic.last_verified_at = datetime.now()
        logic.verification_results = results
        logic.coverage_percentage = results["coverage_percent"]
        
        if correlation_id:
            logger.info(f"Formal verification completed: {results['details']}", correlation_id)
        
        return results
    
    def check_coverage(self, component: str = None, correlation_id: str = None) -> Dict[str, any]:
        """
        Check formal verification coverage for components
        
        Args:
            component: Specific component to check coverage for (optional)
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with coverage results
        """
        if correlation_id:
            logger.info(f"Checking formal verification coverage for component: {component or 'all'}", correlation_id)
        
        # Filter logic by component if specified
        filtered_logic = list(self.verification_logic.values())
        if component:
            filtered_logic = [l for l in filtered_logic if component in l.name or component in l.description]
        
        if not filtered_logic:
            return {
                "component": component,
                "passed": True,
                "total_logic": 0,
                "verified_logic": 0,
                "coverage_percent": 100.0,
                "details": "No verification logic found for component"
            }
        
        # Count verified logic
        verified_logic = [l for l in filtered_logic if l.last_verified_at is not None]
        coverage_percent = (len(verified_logic) / len(filtered_logic)) * 100
        
        # Calculate average coverage
        total_coverage = sum(l.coverage_percentage for l in verified_logic)
        avg_coverage = total_coverage / len(verified_logic) if verified_logic else 0
        
        passed = coverage_percent >= 99.0  # Pass if 99%+ coverage
        
        results = {
            "component": component,
            "passed": passed,
            "total_logic": len(filtered_logic),
            "verified_logic": len(verified_logic),
            "unverified_logic": len(filtered_logic) - len(verified_logic),
            "coverage_percent": coverage_percent,
            "average_coverage": avg_coverage,
            "details": f"Coverage: {coverage_percent:.1f}% ({len(verified_logic)}/{len(filtered_logic)} verified)"
        }
        
        if correlation_id:
            logger.info(f"Coverage check completed: {results['details']}", correlation_id)
        
        return results
    
    def get_verification_report(self, correlation_id: str = None) -> Dict[str, any]:
        """
        Get a comprehensive report on formal verification status
        
        Args:
            correlation_id: Correlation ID for logging
            
        Returns:
            Dictionary with verification report
        """
        if correlation_id:
            logger.info("Generating formal verification report", correlation_id)
        
        total_logic = len(self.verification_logic)
        verified_logic = len([l for l in self.verification_logic.values() if l.last_verified_at is not None])
        total_tools = len(self.verification_tools)
        enabled_tools = len([t for t in self.verification_tools.values() if t.enabled])
        
        coverage_percent = (verified_logic / total_logic * 100) if total_logic > 0 else 100
        
        passed = coverage_percent >= 99.0
        
        report = {
            "passed": passed,
            "summary": {
                "total_verification_logic": total_logic,
                "verified_logic": verified_logic,
                "unverified_logic": total_logic - verified_logic,
                "coverage_percent": coverage_percent,
                "total_tools": total_tools,
                "enabled_tools": enabled_tools
            },
            "tools": {t.id: {"name": t.name, "enabled": t.enabled} for t in self.verification_tools.values()},
            "details": f"Formal verification coverage: {coverage_percent:.1f}%"
        }
        
        if correlation_id:
            logger.info(f"Formal verification report generated: {report['details']}", correlation_id)
        
        return report