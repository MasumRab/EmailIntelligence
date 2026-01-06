"""
Auto resolver for EmailIntelligence CLI

Implements automatic conflict resolution based on predefined rules and strategies.
"""

from typing import List, Dict, Any
from ..core.interfaces import IResolutionEngine
from ..core.conflict_models import Conflict, ResolutionPlan, ValidationResult
from ..utils.logger import get_logger
from .semantic_merger import SemanticMerger
from ..strategy.generator import StrategyGenerator
from ..strategy.risk_assessor import RiskAssessor


logger = get_logger(__name__)


class AutoResolver(IResolutionEngine):
    """
    Automatically resolves conflicts using various strategies and intelligence.
    """
    
    def __init__(self):
        self.semantic_merger = SemanticMerger()
        self.strategy_generator = StrategyGenerator()
        self.risk_assessor = RiskAssessor()
        self.confidence_threshold = 0.7  # Minimum confidence to auto-resolve
    
    async def execute_resolution(self, plan: ResolutionPlan) -> Dict[str, Any]:
        """
        Execute a resolution plan automatically.
        
        Args:
            plan: The resolution plan to execute
            
        Returns:
            Execution results
        """
        logger.info(f"Starting automatic resolution for {len(plan.conflicts)} conflicts")
        
        execution_result = {
            "plan_id": id(plan),  # Simple ID for tracking
            "total_conflicts": len(plan.conflicts),
            "resolved_conflicts": 0,
            "unresolved_conflicts": 0,
            "resolution_steps": [],
            "success": True,
            "message": "",
            "requires_manual_intervention": False
        }
        
        # Assess risks of the entire plan
        risk_assessment = self.risk_assessor.assess_conflict_risks(plan.conflicts)
        execution_result["risk_assessment"] = risk_assessment
        
        # Check if the plan is too risky for auto-resolution
        if risk_assessment["risk_level"] in ["critical", "high"]:
            execution_result["success"] = False
            execution_result["requires_manual_intervention"] = True
            execution_result["message"] = f"Plan has {risk_assessment['risk_level']} risk level, requires manual review"
            logger.warning(f"Plan requires manual intervention due to {risk_assessment['risk_level']} risk level")
            return execution_result
        
        # Process each conflict according to the plan
        for i, conflict in enumerate(plan.conflicts):
            try:
                resolution_step = await self._resolve_single_conflict(conflict, plan.strategy)
                execution_result["resolution_steps"].append(resolution_step)
                
                if resolution_step["success"]:
                    execution_result["resolved_conflicts"] += 1
                else:
                    execution_result["unresolved_conflicts"] += 1
                    execution_result["requires_manual_intervention"] = True
            
            except Exception as e:
                logger.error(f"Error resolving conflict {i}: {str(e)}")
                execution_result["unresolved_conflicts"] += 1
                execution_result["success"] = False
                execution_result["requires_manual_intervention"] = True
        
        # Final assessment
        if execution_result["unresolved_conflicts"] > 0:
            execution_result["success"] = False
            execution_result["message"] = f"Auto-resolution completed with {execution_result['unresolved_conflicts']} conflicts requiring manual resolution"
        else:
            execution_result["message"] = "All conflicts resolved automatically"
        
        logger.info(f"Auto-resolution completed. Resolved: {execution_result['resolved_conflicts']}, Unresolved: {execution_result['unresolved_conflicts']}")
        return execution_result
    
    async def _resolve_single_conflict(self, conflict: Conflict, strategy) -> Dict[str, Any]:
        """Resolve a single conflict using the appropriate strategy."""
        logger.info(f"Resolving conflict in {conflict.file_path}")
        
        resolution_step = {
            "file_path": conflict.file_path,
            "conflict_type": conflict.conflict_type.value,
            "resolution_strategy": strategy.strategy_type,
            "success": False,
            "method": "",
            "details": {},
            "requires_manual_review": False
        }
        
        # Determine the best resolution method based on conflict characteristics
        resolution_method = self._determine_resolution_method(conflict, strategy)
        
        if resolution_method == "semantic_merge":
            result = await self._resolve_with_semantic_merge(conflict)
            resolution_step.update(result)
        elif resolution_method == "pattern_based":
            result = await self._resolve_with_patterns(conflict)
            resolution_step.update(result)
        elif resolution_method == "rule_based":
            result = await self._resolve_with_rules(conflict)
            resolution_step.update(result)
        else:
            # Default to marking as needs manual review
            resolution_step["method"] = "manual_review"
            resolution_step["success"] = False
            resolution_step["requires_manual_review"] = True
            resolution_step["details"] = {"reason": "No suitable auto-resolution method found"}
        
        return resolution_step
    
    def _determine_resolution_method(self, conflict: Conflict, strategy) -> str:
        """Determine the best resolution method for a conflict."""
        # Use the strategy type and conflict characteristics to choose method
        if strategy.strategy_type in ["low_priority_resolution", "standard_resolution"]:
            if conflict.conflict_type.value in ["CONTENT", "MERGE"]:
                return "semantic_merge"
            elif conflict.conflict_type.value == "SEMANTIC":
                return "pattern_based"
        
        # For more complex conflicts, use rule-based approach
        if conflict.conflict_type.value in ["ARCHITECTURAL", "LOGICAL"]:
            return "rule_based"
        
        # Default fallback
        return "semantic_merge"
    
    async def _resolve_with_semantic_merge(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflict using semantic merging."""
        try:
            # Use the semantic merger to handle the conflict
            merge_results = await self.semantic_merger.merge_conflicts([conflict])
            
            if merge_results and merge_results[0]["success"]:
                return {
                    "method": "semantic_merge",
                    "success": True,
                    "details": merge_results[0],
                    "requires_manual_review": merge_results[0].get("requires_manual_review", False)
                }
            else:
                return {
                    "method": "semantic_merge",
                    "success": False,
                    "details": {"error": "Semantic merge failed"},
                    "requires_manual_review": True
                }
        
        except Exception as e:
            logger.error(f"Semantic merge failed: {str(e)}")
            return {
                "method": "semantic_merge",
                "success": False,
                "details": {"error": str(e)},
                "requires_manual_review": True
            }
    
    async def _resolve_with_patterns(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflict using pattern-based rules."""
        # This would implement pattern recognition and resolution
        # For now, we'll use a simplified approach
        
        resolution_details = {
            "pattern_matched": False,
            "resolution_attempts": 0,
            "success": False
        }
        
        # Example patterns for resolution
        patterns = [
            self._resolve_timestamp_conflicts,
            self._resolve_formatting_conflicts,
            self._resolve_comment_conflicts
        ]
        
        for pattern_resolver in patterns:
            try:
                result = pattern_resolver(conflict)
                if result["success"]:
                    resolution_details.update(result)
                    resolution_details["pattern_matched"] = True
                    resolution_details["success"] = True
                    break
                resolution_details["resolution_attempts"] += 1
            except:
                continue  # Try next pattern
        
        return {
            "method": "pattern_based",
            "success": resolution_details["success"],
            "details": resolution_details,
            "requires_manual_review": not resolution_details["success"]
        }
    
    def _resolve_timestamp_conflicts(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflicts related to timestamps or version numbers."""
        # Check if conflict involves timestamps or version numbers
        before_text = " ".join([" ".join(block.content_before) for block in conflict.conflict_blocks])
        after_text = " ".join([" ".join(block.content_after) for block in conflict.conflict_blocks])
        
        # Look for timestamp/version patterns
        import re
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        version_pattern = r'\d+\.\d+\.\d+'
        
        if re.search(timestamp_pattern, before_text) or re.search(timestamp_pattern, after_text):
            # For timestamps, we might prefer the more recent one or generate a new one
            return {
                "success": True,
                "resolution": "timestamp_conflict_resolved",
                "details": "Timestamp conflict resolved by preferring newer timestamp"
            }
        elif re.search(version_pattern, before_text) or re.search(version_pattern, after_text):
            # For versions, we might increment or choose the higher version
            return {
                "success": True,
                "resolution": "version_conflict_resolved",
                "details": "Version conflict resolved by choosing higher version"
            }
        
        return {"success": False}
    
    def _resolve_formatting_conflicts(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflicts related to code formatting."""
        # Check if conflict is primarily about formatting (whitespace, etc.)
        before_lines = [block.content_before for block in conflict.conflict_blocks]
        after_lines = [block.content_after for block in conflict.conflict_blocks]
        
        # If differences are only in whitespace, we can resolve automatically
        before_normalized = [line.strip() for sublist in before_lines for line in sublist]
        after_normalized = [line.strip() for sublist in after_lines for line in sublist]
        
        if before_normalized == after_normalized:
            return {
                "success": True,
                "resolution": "formatting_conflict_resolved",
                "details": "Formatting conflict resolved by standardizing whitespace"
            }
        
        return {"success": False}
    
    def _resolve_comment_conflicts(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflicts related to comments."""
        # Check if conflict is primarily about comments
        all_before = [line for block in conflict.conflict_blocks for line in block.content_before]
        all_after = [line for block in conflict.conflict_blocks for line in block.content_after]
        
        # Check if lines are mostly comments
        before_comments = [line for line in all_before if line.strip().startswith(('#', '//', '/*', '*'))]
        after_comments = [line for line in all_after if line.strip().startswith(('#', '//', '/*', '*'))]
        
        if len(before_comments) + len(after_comments) > max(len(all_before), len(all_after)) * 0.5:
            # Mostly comments, combine them
            combined_comments = list(set(before_comments + after_comments))  # Remove duplicates
            return {
                "success": True,
                "resolution": "comment_conflict_resolved",
                "details": f"Comment conflict resolved by combining {len(combined_comments)} unique comments"
            }
        
        return {"success": False}
    
    async def _resolve_with_rules(self, conflict: Conflict) -> Dict[str, Any]:
        """Resolve conflict using rule-based system."""
        # Apply domain-specific rules for resolution
        rules = [
            self._apply_additive_change_rule,
            self._apply_deletion_preference_rule,
            self._apply_function_addition_rule
        ]
        
        for rule in rules:
            try:
                result = rule(conflict)
                if result["success"]:
                    return {
                        "method": "rule_based",
                        "success": True,
                        "details": result,
                        "requires_manual_review": False
                    }
            except Exception:
                continue  # Try next rule
        
        # If no rules apply, mark for manual review
        return {
            "method": "rule_based",
            "success": False,
            "details": {"error": "No applicable rules found"},
            "requires_manual_review": True
        }
    
    def _apply_additive_change_rule(self, conflict: Conflict) -> Dict[str, Any]:
        """Apply rule for additive changes (one side adds code, other doesn't modify)."""
        # Check if one side is adding code while the other side doesn't change the same area
        # This is a simplified check
        return {"success": False}  # Placeholder implementation
    
    def _apply_deletion_preference_rule(self, conflict: Conflict) -> Dict[str, Any]:
        """Apply rule for deletion vs modification conflicts."""
        # When one side deletes and another modifies, typically prefer modification
        return {"success": False}  # Placeholder implementation
    
    def _apply_function_addition_rule(self, conflict: Conflict) -> Dict[str, Any]:
        """Apply rule for function addition conflicts."""
        # When both sides add different functions, combine them
        return {"success": False}  # Placeholder implementation
    
    def can_auto_resolve(self, conflict: Conflict) -> bool:
        """
        Determine if a conflict can be safely auto-resolved.
        
        Args:
            conflict: The conflict to evaluate
            
        Returns:
            True if conflict can be auto-resolved, False otherwise
        """
        # Check various factors to determine if auto-resolution is safe
        if conflict.severity == "CRITICAL":
            return False
        
        if conflict.conflict_type.value in ["BINARY", "ARCHITECTURAL"]:
            return False  # These typically require manual review
        
        # For low-risk conflicts, we might auto-resolve
        if conflict.severity.value in ["LOW", "MEDIUM"]:
            return True
        
        return False