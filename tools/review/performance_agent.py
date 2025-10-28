"""
Performance Review Agent for Multi-Agent Code Review System

This agent identifies performance bottlenecks and optimization opportunities,
including but not limited to:
- Inefficient loops and algorithms
- Memory usage issues
- Database query optimization
- File I/O optimization
- Network call optimization
"""

import ast
import re
from typing import List, Dict, Any
from tools.review.base_agent import BaseReviewAgent


class PerformanceReviewAgent(BaseReviewAgent):
    """Agent that reviews code for performance issues."""
    
    def __init__(self):
        super().__init__()
        self.name = "Performance Review Agent"
        self.description = "Identifies performance bottlenecks and optimization opportunities"
        
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file for performance issues.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary containing performance issues found
        """
        issues = []
        
        # Only review Python files for now
        if not file_path.endswith('.py'):
            return {"issues": issues}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Parse AST for deeper analysis
            tree = ast.parse(content)
            
            # Check for various performance issues
            issues.extend(self._check_inefficient_loops(file_path, tree))
            issues.extend(self._check_string_concatenation(file_path, tree))
            issues.extend(self._check_database_queries(file_path, tree))
            issues.extend(self._check_file_operations(file_path, tree))
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return {"issues": issues}
        
    def _check_inefficient_loops(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for inefficient loops that could be optimized."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for nested loops that might be inefficient
            if isinstance(node, ast.For):
                # Look for nested for loops
                nested_loops = 0
                current_node = node
                while current_node:
                    if isinstance(current_node, ast.For):
                        nested_loops += 1
                    current_node = getattr(current_node, 'parent', None)
                    
                if nested_loops > 2:
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Deeply nested loop ({nested_loops} levels) - potential performance bottleneck",
                        "priority": "medium"
                    })
                    
                # Check for loops with expensive operations
                for inner_node in ast.walk(node):
                    if isinstance(inner_node, ast.Call):
                        # Check for expensive operations inside loops
                        if isinstance(inner_node.func, ast.Name):
                            expensive_funcs = ['print', 'len', 'str', 'int', 'float']
                            if inner_node.func.id in expensive_funcs:
                                # Check if this is inside a loop
                                parent = getattr(inner_node, 'parent', None)
                                in_loop = False
                                while parent:
                                    if isinstance(parent, ast.For):
                                        in_loop = True
                                        break
                                    parent = getattr(parent, 'parent', None)
                                    
                                if in_loop:
                                    issues.append({
                                        "file": file_path,
                                        "line": inner_node.lineno,
                                        "description": f"Potentially expensive operation '{inner_node.func.id}' inside loop",
                                        "priority": "low"
                                    })
                                    
        return issues
        
    def _check_string_concatenation(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for inefficient string concatenation in loops."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                # Check if this is string concatenation
                if (isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant) and
                    isinstance(node.left.value, str) and isinstance(node.right.value, str)):
                    # This is a simple string concatenation, not necessarily problematic
                    pass
                elif isinstance(node.left, ast.Name) or isinstance(node.right, ast.Name):
                    # Check if this is in a loop
                    parent = getattr(node, 'parent', None)
                    in_loop = False
                    while parent:
                        if isinstance(parent, ast.For) or isinstance(parent, ast.While):
                            in_loop = True
                            break
                        parent = getattr(parent, 'parent', None)
                        
                    if in_loop:
                        issues.append({
                            "file": file_path,
                            "line": node.lineno,
                            "description": "String concatenation in loop - consider using join() for better performance",
                            "priority": "medium"
                        })
                        
        return issues
        
    def _check_database_queries(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for potential database query performance issues."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for database operations
                if isinstance(node.func, ast.Attribute):
                    db_methods = ['execute', 'executemany', 'fetchall', 'fetchone', 'fetchmany']
                    if node.func.attr in db_methods:
                        # Check for SELECT * queries
                        if node.args:
                            first_arg = node.args[0]
                            if (isinstance(first_arg, ast.Constant) and 
                                isinstance(first_arg.value, str) and
                                'select *' in first_arg.value.lower()):
                                issues.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "description": "SELECT * query detected - consider specifying only needed columns for better performance",
                                    "priority": "medium"
                                })
                                
                        # Check for N+1 query problems
                        # Look for database calls inside loops
                        parent = getattr(node, 'parent', None)
                        in_loop = False
                        while parent:
                            if isinstance(parent, ast.For) or isinstance(parent, ast.While):
                                in_loop = True
                                break
                            parent = getattr(parent, 'parent', None)
                            
                        if in_loop:
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": "Database query inside loop - potential N+1 query problem",
                                "priority": "high"
                            })
                            
        return issues
        
    def _check_file_operations(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for inefficient file operations."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for file operations
                if isinstance(node.func, ast.Name) and node.func.id in ['open']:
                    # Check if file is being opened in a loop
                    parent = getattr(node, 'parent', None)
                    in_loop = False
                    while parent:
                        if isinstance(parent, ast.For) or isinstance(parent, ast.While):
                            in_loop = True
                            break
                        parent = getattr(parent, 'parent', None)
                        
                    if in_loop:
                        issues.append({
                            "file": file_path,
                            "line": node.lineno,
                            "description": "File operation inside loop - consider batching operations",
                            "priority": "medium"
                        })
                        
                # Check for repeated file reads
                if (isinstance(node.func, ast.Attribute) and
                    node.func.attr in ['read', 'readline', 'readlines']):
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": "File read operation - ensure proper file handling and buffering",
                        "priority": "low"
                    })
                    
        return issues