"""
Architecture Review Agent for Multi-Agent Code Review System

This agent reviews architectural consistency and design patterns,
including but not limited to:
- Layer separation
- Dependency management
- Module organization
- Design patterns
- Code cohesion
- Component coupling
"""

import ast
import re
from typing import List, Dict, Any
from tools.review.base_agent import BaseReviewAgent


class ArchitectureReviewAgent(BaseReviewAgent):
    """Agent that reviews code architecture and design patterns."""
    
    def __init__(self):
        super().__init__()
        self.name = "Architecture Review Agent"
        self.description = "Reviews architectural consistency and design patterns"
        
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file for architectural issues.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary containing architectural issues found
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
            
            # Check for various architectural issues
            issues.extend(self._check_layer_separation(file_path, tree))
            issues.extend(self._check_circular_dependencies(file_path, tree))
            issues.extend(self._check_dependency_injection(file_path, tree))
            issues.extend(self._check_module_organization(file_path, tree))
            issues.extend(self._check_code_cohesion(file_path, tree))
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return {"issues": issues}
        
    def _check_layer_separation(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for proper layer separation."""
        issues = []
        
        # Identify the module type based on file path
        module_type = self._identify_module_type(file_path)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if functions in specific layers are calling inappropriate layers
                if 'route' in file_path or 'api' in file_path or 'controller' in file_path:
                    # This looks like a controller/route layer - should not directly access database
                    for inner_node in ast.walk(node):
                        if (isinstance(inner_node, ast.Call) and 
                            isinstance(inner_node.func, ast.Attribute) and 
                            inner_node.func.attr in ['execute', 'connect', 'cursor']):
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"Controller layer directly accessing database - violates layer separation principle",
                                "priority": "high"
                            })
                            
                elif 'service' in file_path:
                    # This looks like a service layer - should not directly handle HTTP requests
                    for inner_node in ast.walk(node):
                        if (isinstance(inner_node, ast.Call) and 
                            isinstance(inner_node.func, ast.Attribute) and 
                            (inner_node.func.attr in ['json', 'request', 'Response', 'HTMLResponse'] or
                             (hasattr(inner_node.func, 'value') and 
                              isinstance(inner_node.func.value, ast.Name) and
                              inner_node.func.value.id in ['request', 'req']))):
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"Service layer directly handling HTTP request/response - violates layer separation principle",
                                "priority": "medium"
                            })
                            
                elif 'model' in file_path or 'database' in file_path:
                    # This looks like a data layer - should not handle business logic
                    for inner_node in ast.walk(node):
                        if (isinstance(inner_node, ast.Call) and 
                            isinstance(inner_node.func, ast.Name) and
                            inner_node.func.id in ['render', 'redirect', 'jsonify', 'Response']):
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "description": f"Data layer directly handling response rendering - violates layer separation principle",
                                "priority": "high"
                            })
                            
        return issues
        
    def _check_circular_dependencies(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for potential circular dependencies."""
        issues = []
        
        # Check for imports that might create circular dependencies
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    # Check if the module being imported is part of the same layer
                    current_module_parts = file_path.replace('/', '.').replace('\\', '.').split('.')
                    if len(current_module_parts) > 1:
                        current_layer = current_module_parts[1] if current_module_parts[0] == '' else current_module_parts[0]
                        
                        imported_module_parts = node.module.split('.')
                        if len(imported_module_parts) > 1:
                            imported_layer = imported_module_parts[1] if imported_module_parts[0] == '' else imported_module_parts[0]
                            
                            # If importing from the same layer, flag as potential circular dependency
                            if current_layer == imported_layer and current_layer in ['routes', 'controllers', 'services', 'models']:
                                issues.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "description": f"Potential circular dependency: importing from same layer '{current_layer}'",
                                    "priority": "medium"
                                })
                                
        return issues
        
    def _check_dependency_injection(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for proper dependency injection patterns."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if functions are creating their own dependencies instead of receiving them
                for inner_node in ast.walk(node):
                    if (isinstance(inner_node, ast.Call) and 
                        isinstance(inner_node.func, ast.Name) and
                        inner_node.func.id in ['open', 'connect', 'Client', 'Session']):
                        # Check if this is creating a dependency inside a function
                        # This is a basic check - more complex analysis needed for full validation
                        issues.append({
                            "file": file_path,
                            "line": inner_node.lineno,
                            "description": f"Function '{node.name}' creating its own dependency '{inner_node.func.id}' - consider dependency injection",
                            "priority": "medium"
                        })
                        
        return issues
        
    def _check_module_organization(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for proper module organization."""
        issues = []
        
        # Extract the module type from the file path
        module_type = self._identify_module_type(file_path)
        
        # Check if the file is in the right directory based on its content
        expected_patterns = {
            'route': ['app.route', 'router.get', 'router.post', 'FastAPI'],
            'model': ['class.*BaseModel', 'class.*Model', 'class.*Entity', 'sqlalchemy'],
            'service': ['def.*service', 'def.*process', 'def.*handle', 'class.*Service'],
            'util': ['def.*util', 'def.*helper', 'def.*format', 'def.*validate']
        }
        
        content = self._read_file_content(file_path)
        
        for pattern_type, patterns in expected_patterns.items():
            if pattern_type != module_type:
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append({
                            "file": file_path,
                            "line": 1,
                            "description": f"File contains {pattern_type} patterns but is located in {module_type} directory",
                            "priority": "medium"
                        })
                        
        return issues
        
    def _check_code_cohesion(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for proper code cohesion."""
        issues = []
        
        # Count the number of classes and functions in the file
        class_count = 0
        func_count = 0
        classes = []
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_count += 1
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                func_count += 1
                functions.append(node.name)
                
        # Check if the file has too many unrelated classes or functions
        if class_count > 3 or func_count > 10:
            issues.append({
                "file": file_path,
                "line": 1,
                "description": f"File has {class_count} classes and {func_count} functions - consider splitting into smaller, more cohesive modules",
                "priority": "medium"
            })
            
        # Check if the file has classes that don't seem related
        if class_count > 1:
            # This is a basic check - real cohesion analysis would require deeper semantic analysis
            issues.append({
                "file": file_path,
                "line": 1,
                "description": f"File has {class_count} classes - verify these classes are closely related and cohesive",
                "priority": "low"
            })
            
        return issues
        
    def _identify_module_type(self, file_path: str) -> str:
        """Identify the type of module based on its path."""
        path_parts = file_path.lower().split('/')
        
        for part in reversed(path_parts):
            if 'route' in part or 'api' in part or 'controller' in part:
                return 'route'
            elif 'model' in part or 'entity' in part:
                return 'model'
            elif 'service' in part or 'manager' in part:
                return 'service'
            elif 'util' in part or 'helper' in part:
                return 'util'
            elif 'test' in part:
                return 'test'
                
        return 'general'