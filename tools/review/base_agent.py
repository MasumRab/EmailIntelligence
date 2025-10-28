"""
Base Agent Class for Multi-Agent Code Review System
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import ast
import os


class BaseReviewAgent(ABC):
    """Base class for all review agents."""
    
    def __init__(self):
        self.name = "Base Review Agent"
        self.description = "Base class for review agents"
        
    @abstractmethod
    def review_file(self, file_path: str) -> Dict[str, Any]:
        """
        Review a single file and return issues found.
        
        Args:
            file_path: Path to the file to review
            
        Returns:
            Dictionary containing review results
        """
        pass
        
    def review_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Review multiple files and return aggregated results.
        
        Args:
            file_paths: List of file paths to review
            
        Returns:
            Dictionary containing aggregated review results
        """
        all_issues = []
        file_count = 0
        
        for file_path in file_paths:
            if os.path.isfile(file_path):
                try:
                    file_result = self.review_file(file_path)
                    if file_result.get("issues"):
                        all_issues.extend(file_result["issues"])
                    file_count += 1
                except Exception as e:
                    print(f"Error reviewing {file_path}: {e}")
                    
        return {
            "agent": self.name,
            "description": self.description,
            "files_reviewed": file_count,
            "issues": all_issues
        }
        
    def _read_file_content(self, file_path: str) -> str:
        """Read file content as string."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    def _parse_python_ast(self, file_path: str) -> ast.AST:
        """Parse Python file into AST."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return ast.parse(content)