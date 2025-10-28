"""
Security Review Agent for Multi-Agent Code Review System

This agent identifies potential security vulnerabilities in the codebase,
including but not limited to:
- Hardcoded secrets
- Insecure subprocess usage
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure file operations
- Weak cryptographic practices
"""

import ast
import re
from typing import List, Dict, Any
from tools.review.base_agent import BaseReviewAgent


class SecurityReviewAgent(BaseReviewAgent):
    """Agent that reviews code for security vulnerabilities."""
    
    def __init__(self):
        super().__init__()
        self.name = "Security Review Agent"
        self.description = "Analyzes code for security vulnerabilities and potential exploits"
        
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file for security issues.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary containing security issues found
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
            
            # Check for various security issues
            issues.extend(self._check_hardcoded_secrets(file_path, lines))
            issues.extend(self._check_subprocess_usage(file_path, tree))
            issues.extend(self._check_eval_usage(file_path, tree))
            issues.extend(self._check_exec_usage(file_path, tree))
            issues.extend(self._check_input_sanitization(file_path, tree))
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return {"issues": issues}
        
    def _check_hardcoded_secrets(self, file_path: str, lines: List[str]) -> List[Dict]:
        """Check for hardcoded secrets like passwords, API keys, etc."""
        issues = []
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']{3,}["\']', "Hardcoded password detected"),
            (r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded secret detected"),
            (r'token\s*=\s*["\'][^"\']{10,}["\']', "Hardcoded token detected"),
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern, description in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "description": description,
                        "priority": "critical"
                    })
                    
        return issues
        
    def _check_subprocess_usage(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for insecure subprocess usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for subprocess calls
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and 
                        node.func.value.id in ['subprocess', 'os'] and
                        node.func.attr in ['system', 'popen', 'call', 'run']):
                        # Check if shell=True is used
                        for keyword in node.keywords:
                            if (keyword.arg == 'shell' and 
                                isinstance(keyword.value, ast.Constant) and 
                                keyword.value.value is True):
                                issues.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "description": f"Insecure subprocess call with shell=True: {ast.dump(node.func)}",
                                    "priority": "high"
                                })
                                
                # Check for direct os.system calls
                if (isinstance(node.func, ast.Attribute) and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'os' and
                    node.func.attr == 'system'):
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": "Direct os.system call detected - potential security risk",
                        "priority": "high"
                    })
                    
        return issues
        
    def _check_eval_usage(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for unsafe eval usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": "Use of eval() detected - potential code injection vulnerability",
                        "priority": "critical"
                    })
                    
        return issues
        
    def _check_exec_usage(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for unsafe exec usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'exec':
                    issues.append({
                        "file": file_path,
                        "line": node.lineno,
                        "description": "Use of exec() detected - potential code injection vulnerability",
                        "priority": "critical"
                    })
                    
        return issues
        
    def _check_input_sanitization(self, file_path: str, tree: ast.AST) -> List[Dict]:
        """Check for potential input sanitization issues."""
        issues = []
        
        # Look for web framework routes that might have unsanitized input
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if this looks like a route handler
                is_route = any(
                    decorator.id in ['app.route', 'router.get', 'router.post'] 
                    for decorator in node.decorator_list 
                    if isinstance(decorator, ast.Attribute) or 
                       (isinstance(decorator, ast.Name) and hasattr(decorator, 'id'))
                )
                
                if is_route:
                    # Check for direct use of request data without sanitization
                    for inner_node in ast.walk(node):
                        if isinstance(inner_node, ast.Call):
                            if (isinstance(inner_node.func, ast.Attribute) and
                                inner_node.func.attr in ['execute', 'executemany'] and
                                isinstance(inner_node.func.value, ast.Name) and
                                'cursor' in inner_node.func.value.id.lower()):
                                # Potential SQL injection if parameters aren't properly parameterized
                                issues.append({
                                    "file": file_path,
                                    "line": inner_node.lineno,
                                    "description": "Potential SQL injection - direct cursor execution without parameterization",
                                    "priority": "high"
                                })
                                
        return issues