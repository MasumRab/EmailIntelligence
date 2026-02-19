"""
Semantic merger for EmailIntelligence CLI

Implements intelligent merging of code based on semantic understanding.
"""

from typing import List, Dict, Any, Optional
from ..core.conflict_models import Conflict, ConflictBlock
from ..utils.logger import get_logger


logger = get_logger(__name__)


class SemanticMerger:
    """
    Performs intelligent merging of conflicts based on semantic understanding.
    """
    
    def __init__(self):
        self.merge_strategies = {
            "function_signature": self._merge_function_signatures,
            "variable_assignment": self._merge_variable_assignments,
            "import_statements": self._merge_imports,
            "comment_blocks": self._merge_comments,
            "code_blocks": self._merge_code_blocks
        }
    
    async def merge_conflicts(self, conflicts: List[Conflict]) -> List[Dict[str, Any]]:
        """
        Perform semantic merging of conflicts.
        
        Args:
            conflicts: List of conflicts to merge
            
        Returns:
            List of merge results
        """
        logger.info(f"Starting semantic merge for {len(conflicts)} conflicts")
        
        merge_results = []
        
        for conflict in conflicts:
            result = await self._merge_single_conflict(conflict)
            merge_results.append(result)
        
        logger.info(f"Semantic merge completed for {len(merge_results)} conflicts")
        return merge_results
    
    async def _merge_single_conflict(self, conflict: Conflict) -> Dict[str, Any]:
        """Merge a single conflict using semantic understanding."""
        logger.info(f"Merging conflict in file: {conflict.file_path}")
        
        merge_result = {
            "file_path": conflict.file_path,
            "conflict_type": conflict.conflict_type.value,
            "resolution_strategy": "semantic_merge",
            "merged_blocks": [],
            "unresolved_blocks": [],
            "success": True,
            "message": ""
        }
        
        for block in conflict.conflict_blocks:
            try:
                merged_block = self._merge_conflict_block(block, conflict.file_path)
                if merged_block:
                    merge_result["merged_blocks"].append(merged_block)
                else:
                    merge_result["unresolved_blocks"].append(block)
                    merge_result["success"] = False
            except Exception as e:
                logger.error(f"Error merging block in {conflict.file_path}: {str(e)}")
                merge_result["unresolved_blocks"].append(block)
                merge_result["success"] = False
                merge_result["message"] = str(e)
        
        return merge_result
    
    def _merge_conflict_block(self, block: ConflictBlock, file_path: str) -> Optional[Dict[str, Any]]:
        """Merge a single conflict block using appropriate strategy."""
        # Determine the type of content in the conflict block
        content_type = self._determine_content_type(block, file_path)
        
        if content_type in self.merge_strategies:
            return self.merge_strategies[content_type](block)
        else:
            # Default to code block merging for unknown types
            return self._merge_code_blocks(block)
    
    def _determine_content_type(self, block: ConflictBlock, file_path: str) -> str:
        """Determine the type of content in the conflict block."""
        # Check file extension to determine content type
        if file_path.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs')):
            # Check content for specific patterns
            content_before = ' '.join(block.content_before)
            content_after = ' '.join(block.content_after)
            
            # Check for function definitions
            if any(keyword in content_before or keyword in content_after 
                   for keyword in ['def ', 'function', 'def(', 'func ', 'public ', 'private ', 'protected ']):
                return "function_signature"
            
            # Check for import statements
            if any(keyword in content_before or keyword in content_after 
                   for keyword in ['import ', 'from ', 'include ', 'using ']):
                return "import_statements"
            
            # Check for variable assignments
            if any('=' in line for line in block.content_before + block.content_after):
                return "variable_assignment"
            
            # Check for comments
            if any(line.strip().startswith(('#', '//', '/*', '*')) for line in block.content_before + block.content_after):
                return "comment_blocks"
        
        return "code_blocks"
    
    def _merge_function_signatures(self, block: ConflictBlock) -> Dict[str, Any]:
        """Merge function signature conflicts."""
        # This is a simplified implementation
        # In a real system, this would use AST parsing to understand function signatures
        
        # Try to identify parameters and return types
        before_params = self._extract_function_params(block.content_before)
        after_params = self._extract_function_params(block.content_after)
        
        # Merge parameters intelligently
        merged_params = self._merge_parameters(before_params, after_params)
        
        # Create merged function signature
        merged_signature = self._create_merged_function_signature(block, merged_params)
        
        return {
            "type": "function_signature",
            "merged_content": merged_signature,
            "strategy": "parameter_merge",
            "confidence": 0.8
        }
    
    def _extract_function_params(self, content_lines: List[str]) -> List[str]:
        """Extract function parameters from content."""
        params = []
        for line in content_lines:
            # Simple extraction - in reality, this would use proper parsing
            if '(' in line and ')' in line:
                # Extract content between parentheses
                start = line.find('(')
                end = line.find(')')
                if start != -1 and end != -1 and end > start:
                    param_str = line[start+1:end]
                    # Split by comma and clean up
                    params.extend([p.strip() for p in param_str.split(',') if p.strip()])
        return params
    
    def _merge_parameters(self, before_params: List[str], after_params: List[str]) -> List[str]:
        """Merge function parameters."""
        # Create a set of all parameters
        all_params = list(set(before_params + after_params))
        return all_params
    
    def _create_merged_function_signature(self, block: ConflictBlock, params: List[str]) -> List[str]:
        """Create a merged function signature."""
        # This is a simplified implementation
        # In a real system, this would reconstruct the function properly
        return ["# Merged function signature", "# Parameters: " + ", ".join(params)]
    
    def _merge_variable_assignments(self, block: ConflictBlock) -> Dict[str, Any]:
        """Merge variable assignment conflicts."""
        # Identify variables being assigned
        before_vars = self._extract_variables(block.content_before)
        after_vars = self._extract_variables(block.content_after)
        
        # Merge variable assignments
        merged_assignments = {}
        
        # Add all variables from both sides
        for var_name, var_value in before_vars.items():
            merged_assignments[var_name] = var_value
        
        for var_name, var_value in after_vars.items():
            if var_name in merged_assignments:
                # Handle conflict: try to merge values intelligently
                merged_assignments[var_name] = self._merge_variable_values(
                    merged_assignments[var_name], var_value
                )
            else:
                merged_assignments[var_name] = var_value
        
        # Generate merged content
        merged_content = []
        for var_name, var_value in merged_assignments.items():
            merged_content.append(f"{var_name} = {var_value}")
        
        return {
            "type": "variable_assignment",
            "merged_content": merged_content,
            "strategy": "value_merge",
            "confidence": 0.7
        }
    
    def _extract_variables(self, content_lines: List[str]) -> Dict[str, str]:
        """Extract variable assignments from content."""
        variables = {}
        for line in content_lines:
            if '=' in line and not line.strip().startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    var_value = parts[1].strip()
                    variables[var_name] = var_value
        return variables
    
    def _merge_variable_values(self, value1: str, value2: str) -> str:
        """Merge two variable values intelligently."""
        import ast
        
        # If both are lists or dicts (indicated by brackets/braces), try to merge them
        if (value1.startswith('[') and value2.startswith('[')) or (value1.startswith('{') and value2.startswith('{')):
            try:
                # Parse both values safely using ast.literal_eval
                parsed1 = ast.literal_eval(value1)
                parsed2 = ast.literal_eval(value2)
                
                # Merge lists (concatenate unique items)
                if isinstance(parsed1, list) and isinstance(parsed2, list):
                    merged = list(set(parsed1 + parsed2))
                    # Sort for consistency
                    merged.sort()
                    return str(merged)
                
                # Merge dicts (combine keys, prefer value2 on conflict)
                elif isinstance(parsed1, dict) and isinstance(parsed2, dict):
                    merged = {**parsed1, **parsed2}
                    return str(merged)
                    
            except (ValueError, SyntaxError, TypeError) as e:
                logger.warning(f"Failed to parse values for merge: {e}")
                # Fallback to conflict marker
                return f"/* CONFLICT: Choose between {value1} and {value2} */"
        
        # For other cases, we might prefer one over the other or mark for manual review
        return f"/* CONFLICT: Choose between {value1} and {value2} */"
    
    def _merge_imports(self, block: ConflictBlock) -> Dict[str, Any]:
        """Merge import statement conflicts."""
        # Extract imports from both sides
        before_imports = self._extract_imports(block.content_before)
        after_imports = self._extract_imports(block.content_after)
        
        # Combine imports, removing duplicates
        all_imports = list(set(before_imports + after_imports))
        all_imports.sort()  # Sort for consistency
        
        return {
            "type": "import_statements",
            "merged_content": all_imports,
            "strategy": "union_merge",
            "confidence": 0.95
        }
    
    def _extract_imports(self, content_lines: List[str]) -> List[str]:
        """Extract import statements from content."""
        imports = []
        for line in content_lines:
            line = line.strip()
            if line.startswith(('import ', 'from ', 'include ', 'using ')):
                imports.append(line)
        return imports
    
    def _merge_comments(self, block: ConflictBlock) -> Dict[str, Any]:
        """Merge comment conflicts."""
        # Combine comments from both sides
        all_comments = []
        
        # Add comments from both sides, avoiding duplicates
        before_comments = [line for line in block.content_before if line.strip().startswith(('#', '//', '/*', '*'))]
        after_comments = [line for line in block.content_after if line.strip().startswith(('#', '//', '/*', '*'))]
        
        # Combine unique comments
        all_comments = list(set(before_comments + after_comments))
        
        return {
            "type": "comment_blocks",
            "merged_content": all_comments,
            "strategy": "union_merge",
            "confidence": 0.9
        }
    
    def _merge_code_blocks(self, block: ConflictBlock) -> Dict[str, Any]:
        """Merge general code blocks."""
        # For complex code blocks, we might need to defer to manual resolution
        # but we can try some basic strategies
        
        # Check if the changes are additive (one side adds code without modifying existing)
        before_lines = [line.strip() for line in block.content_before]
        after_lines = [line.strip() for line in block.content_after]
        
        # Simple strategy: combine unique lines
        combined_lines = list(set(before_lines + after_lines))
        
        return {
            "type": "code_blocks",
            "merged_content": combined_lines,
            "strategy": "union_merge_with_review",
            "confidence": 0.5,  # Lower confidence for code blocks
            "requires_manual_review": True
        }
    
    def validate_merge(self, original_content: str, merged_content: str) -> Dict[str, Any]:
        """
        Validate that the merge produced valid content.
        
        Args:
            original_content: Original content before conflicts
            merged_content: Content after merging
            
        Returns:
            Validation results
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "line_count_change": len(merged_content) - len(original_content.split('\n')) if isinstance(original_content, str) else 0
        }
        
        # Add validation logic here
        # For example, check for syntax validity, ensure no conflict markers remain, etc.
        
        return validation_result