"""
Code Quality Review Agent for Multi-Agent Code Review System

This agent evaluates code quality, maintainability, and best practices,
including but not limited to:
- Code complexity
- Documentation and comments
- Naming conventions
- Code duplication
- Error handling
- Test coverage
"""

import ast
import re
from typing import List, Dict, Any
from tools.review.base_agent import BaseReviewAgent


class QualityReviewAgent(BaseReviewAgent):
    """Agent that reviews code for quality and best practices."""
    
    def __init__(self):
        super().__init__()
        self.name = "Code Quality Review Agent"
        self.description = "Evaluates code quality, maintainability, and best practices"
        
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file for code quality issues.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary containing quality issues found
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
            
            # Check for various quality issues
            issues.extend(self._check_function_complexity(file_path, tree))
            issues.extend(self._check_naming_conventions(file_path, tree))
            issues.extend(self._check_docstrings(file_path, tree))
            issues.extend(self._check_error_handling(file_path, tree))
            issues.extend(self._check_imports(file_path, tree))
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return {"issues": issues}
        
    def _check_function_complexity(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for functions with high cyclomatic complexity."""
        issues = []
        
        # Count the number of decision points in a function to estimate complexity
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count decision points (if, elif, for, while, try, and, or)
                decision_points = 0
                for inner_node in ast.walk(node):
                    if isinstance(inner_node, (ast.If, ast.For, ast.While, ast.Try)):
                        decision_points += 1
                    elif isinstance(inner_node, ast.BoolOp):
                        # Each 'and' or 'or' in a boolean operation adds complexity
                        decision_points += len(inner_node.values) - 1
                    elif isinstance(inner_node, ast.ExceptHandler):
                        decision_points += 1
                        
                # Consider functions complex if they have more than 10 decision points
                if decision_points > 10:
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Function '{node.name}' has high cyclomatic complexity ({decision_points} decision points) - consider refactoring",
                        "priority": "medium"
                    })
                    
                # Check function length
                func_lines = node.end_lineno - node.lineno
                if func_lines > 50:
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Function '{node.name}' is too long ({func_lines} lines) - consider breaking into smaller functions",
                        "priority": "medium"
                    })
                    
        return issues
        
    def _check_naming_conventions(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for naming convention violations."""
        issues = []
        
        # Check function and variable names
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check function name follows snake_case
                if not re.match(r'^[a-z][a-z0-9_]*$', node.name) and not node.name.startswith('__'):
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Function name '{node.name}' doesn't follow snake_case naming convention",
                        "priority": "low"
                    })
                    
            elif isinstance(node, ast.Assign):
                # Check variable names
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if not re.match(r'^[a-z][a-z0-9_]*$', target.id):
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"Variable name '{target.id}' doesn't follow snake_case naming convention",
                                "priority": "low"
                            })
                            
            elif isinstance(node, ast.ClassDef):
                # Check class name follows CapWords
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Class name '{node.name}' doesn't follow CapWords naming convention",
                        "priority": "low"
                    })
                    
        return issues
        
    def _check_docstrings(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for missing or inadequate docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function has a docstring
                has_docstring = False
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    has_docstring = True
                    
                # Flag functions without docstrings (except simple ones)
                if not has_docstring and len(node.body) > 1:  # More than just pass or return
                    # Don't flag simple getter/setter functions or private methods
                    if not node.name.startswith('_') or node.name.startswith('__'):
                        issues.append({
                            "file": file_path,
                            "line": node.lineno,
                            "description": f"Function '{node.name}' is missing docstring",
                            "priority": "low"
                        })
                        
            elif isinstance(node, ast.ClassDef):
                # Check if class has a docstring
                has_docstring = False
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    has_docstring = True
                    
                if not has_docstring:
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": f"Class '{node.name}' is missing docstring",
                        "priority": "low"
                    })
                    
        return issues
        
    def _check_error_handling(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for proper error handling."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for function calls that might raise exceptions
                if isinstance(node.func, ast.Attribute):
                    # Check for file operations without proper error handling
                    if node.func.attr in ['read', 'write', 'open']:
                        # Look for this call inside a try-except block
                        parent = getattr(node, 'parent', None)
                        in_try_except = False
                        while parent:
                            if isinstance(parent, ast.Try):
                                in_try_except = True
                                break
                            parent = getattr(parent, 'parent', None)
                            
                        if not in_try_except:
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"File operation '{node.func.attr}' without try-except block",
                                "priority": "medium"
                            })
                            
                    # Check for network/database calls
                    elif node.func.attr in ['get', 'post', 'execute', 'connect']:
                        parent = getattr(node, 'parent', None)
                        in_try_except = False
                        while parent:
                            if isinstance(parent, ast.Try):
                                in_try_except = True
                                break
                            parent = getattr(parent, 'parent', None)
                            
                        if not in_try_except:
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"Network/Database operation '{node.func.attr}' without try-except block",
                                "priority": "high"
                            })
                            
        return issues
        
    def _check_imports(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for import issues."""
        issues = []
        
        # Check for wildcard imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.names:
                for alias in node.names:
                    if alias.name == '*':
                        issues.append({
                            "file": file_path,
                            "line": node.lineno,
                            "description": f"Wildcard import detected: from {node.module} import *",
                            "priority": "low"
                        })
                        
            # Check for unused imports
            # This is a basic check - a more thorough analysis would require deeper analysis
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if hasattr(node, 'module') and node.module == 'typing':
                    # Check if typing imports are used in the file
                    pass  # For now, we don't flag typing imports as unused
                    
        return issues