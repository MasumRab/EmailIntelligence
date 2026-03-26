#!/usr/bin/env python3
"""
Parallel Validation Workers
Implement multiple validation processes running simultaneously.
"""

import os
import re
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum


class ValidationType(Enum):
    SYNTAX = "syntax"
    LINKS = "links"
    CONTENT = "content"
    STRUCTURE = "structure"
    COMPLETENESS = "completeness"


class ValidationResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class ValidationError:
    file_path: str
    line_number: Optional[int]
    error_type: str
    message: str
    severity: str
    suggestion: Optional[str] = None


@dataclass
class ValidationTask:
    task_id: str
    validation_type: ValidationType
    files: List[str]
    worker_id: str
    created_at: float
    completed_at: Optional[float] = None
    result: Optional[ValidationResult] = None
    errors: List[ValidationError] = field(default_factory=list)
    duration: float = 0.0


class ValidationWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.is_active = False
        self.tasks_processed = 0
        self.errors_found = 0
        
    def validate_syntax(self, file_path: Path) -> List[ValidationError]:
        """Validate syntax of a file."""
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for basic syntax issues
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Check for unbalanced brackets
                if line.count('(') != line.count(')'):
                    errors.append(ValidationError(
                        file_path=str(file_path),
                        line_number=i,
                        error_type="unbalanced_parentheses",
                        message=f"Unbalanced parentheses on line {i}",
                        severity="error"
                    ))
                    
                if line.count('[') != line.count(']'):
                    errors.append(ValidationError(
                        file_path=str(file_path),
                        line_number=i,
                        error_type="unbalanced_brackets",
                        message=f"Unbalanced brackets on line {i}",
                        severity="error"
                    ))
                    
                if line.count('{') != line.count('}'):
                    errors.append(ValidationError(
                        file_path=str(file_path),
                        line_number=i,
                        error_type="unbalanced_braces",
                        message=f"Unbalanced braces on line {i}",
                        severity="error"
                    ))
                    
        except Exception as e:
            errors.append(ValidationError(
                file_path=str(file_path),
                line_number=None,
                error_type="file_read_error",
                message=f"Could not read file: {str(e)}",
                severity="error"
            ))
            
        return errors
        
    def validate_links(self, file_path: Path) -> List[ValidationError]:
        """Validate links in a file."""
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, content)
            
            for text, url in links:
                # Check for broken URLs (simplified check)
                if url.startswith('http'):
                    # In a real implementation, we would check if URL is accessible
                    # For now, we'll just check basic URL format
                    if not (url.startswith('http://') or url.startswith('https://')):
                        errors.append(ValidationError(
                            file_path=str(file_path),
                            line_number=None,
                            error_type="invalid_url_format",
                            message=f"Invalid URL format: {url}",
                            severity="warning"
                        ))
                elif url.startswith('#'):
                    # Anchor link - check if it's a valid heading
                    pass  # Would need to check document structure
                else:
                    # Relative link - check if file exists
                    link_path = Path(file_path).parent / url
                    if not link_path.exists():
                        errors.append(ValidationError(
                            file_path=str(file_path),
                            line_number=None,
                            error_type="broken_link",
                            message=f"Broken link to file: {url}",
                            severity="error"
                        ))
                        
        except Exception as e:
            errors.append(ValidationError(
                file_path=str(file_path),
                line_number=None,
                error_type="file_read_error",
                message=f"Could not read file for link validation: {str(e)}",
                severity="error"
            ))
            
        return errors
        
    def validate_content(self, file_path: Path) -> List[ValidationError]:
        """Validate content quality."""
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for content issues
            if len(content.strip()) == 0:
                errors.append(ValidationError(
                    file_path=str(file_path),
                    line_number=None,
                    error_type="empty_file",
                    message="File is empty",
                    severity="warning"
                ))
                
            # Check for very short content
            word_count = len(content.split())
            if word_count < 10:
                errors.append(ValidationError(
                    file_path=str(file_path),
                    line_number=None,
                    error_type="short_content",
                    message=f"Content is very short ({word_count} words)",
                    severity="warning"
                ))
                
            # Check for placeholder text
            placeholder_patterns = [
                r'\{\{.*?\}\}',  # {{placeholder}}
                r'\[.*?\]\(.*?\)',  # [text](url) - but not markdown links
                r'TODO:', r'FIXME:', r'XXX:'
            ]
            
            for pattern in placeholder_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    errors.append(ValidationError(
                        file_path=str(file_path),
                        line_number=None,
                        error_type="placeholder_content",
                        message=f"Found placeholder content: {match}",
                        severity="warning"
                    ))
                    
        except Exception as e:
            errors.append(ValidationError(
                file_path=str(file_path),
                line_number=None,
                error_type="file_read_error",
                message=f"Could not read file for content validation: {str(e)}",
                severity="error"
            ))
            
        return errors
        
    def run_validation_task(self, task: ValidationTask) -> ValidationTask:
        """Run a validation task."""
        self.is_active = True
        start_time = time.time()
        
        try:
            all_errors = []
            
            for file_path in task.files:
                file_errors = []
                
                if task.validation_type == ValidationType.SYNTAX:
                    file_errors = self.validate_syntax(Path(file_path))
                elif task.validation_type == ValidationType.LINKS:
                    file_errors = self.validate_links(Path(file_path))
                elif task.validation_type == ValidationType.CONTENT:
                    file_errors = self.validate_content(Path(file_path))
                elif task.validation_type == ValidationType.STRUCTURE:
                    # Structure validation would check document organization
                    file_errors = []
                elif task.validation_type == ValidationType.COMPLETENESS:
                    # Completeness validation would check for required sections
                    file_errors = []
                    
                all_errors.extend(file_errors)
                
            task.errors = all_errors
            task.result = ValidationResult.FAIL if all_errors else ValidationResult.PASS
            self.errors_found += len(all_errors)
            
        except Exception as e:
            task.result = ValidationResult.FAIL
            task.errors.append(ValidationError(
                file_path="system",
                line_number=None,
                error_type="validation_error",
                message=f"Validation task failed: {str(e)}",
                severity="error"
            ))
            
        finally:
            self.is_active = False
            self.tasks_processed += 1
            task.completed_at = time.time()
            task.duration = task.completed_at - start_time
            
        return task


class ParallelValidationManager:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.workers: Dict[str, ValidationWorker] = {}
        self.validation_history: List[ValidationTask] = []
        self.validation_log_file = Path("validation_log.json")
        self.load_validation_log()
        
    def load_validation_log(self):
        """Load validation log from file."""
        if self.validation_log_file.exists():
            try:
                with open(self.validation_log_file, 'r') as f:
                    data = json.load(f)
                    # In a real implementation, we would reconstruct ValidationTask objects
                    self.validation_history = data
            except Exception as e:
                print(f"Error loading validation log: {e}")
                
    def save_validation_log(self):
        """Save validation log to file."""
        try:
            # Convert ValidationTask objects to serializable format
            serializable_history = []
            for task in self.validation_history:
                task_data = {
                    'task_id': task.task_id,
                    'validation_type': task.validation_type.value,
                    'files': task.files,
                    'worker_id': task.worker_id,
                    'created_at': task.created_at,
                    'completed_at': task.completed_at,
                    'result': task.result.value if task.result else None,
                    'errors': [
                        {
                            'file_path': error.file_path,
                            'line_number': error.line_number,
                            'error_type': error.error_type,
                            'message': error.message,
                            'severity': error.severity,
                            'suggestion': error.suggestion
                        }
                        for error in task.errors
                    ],
                    'duration': task.duration
                }
                serializable_history.append(task_data)
                
            with open(self.validation_log_file, 'w') as f:
                json.dump(serializable_history, f, indent=2)
        except Exception as e:
            print(f"Error saving validation log: {e}")
            
    def add_worker(self, worker_id: str) -> bool:
        """Add a validation worker."""
        if worker_id in self.workers:
            return False
            
        worker = ValidationWorker(worker_id)
        self.workers[worker_id] = worker
        return True
        
    def remove_worker(self, worker_id: str) -> bool:
        """Remove a validation worker."""
        if worker_id in self.workers:
            # Don't remove active workers
            if self.workers[worker_id].is_active:
                return False
            del self.workers[worker_id]
            return True
        return False
        
    def create_validation_task(self, validation_type: ValidationType, 
                             files: List[str], worker_id: str) -> ValidationTask:
        """Create a validation task."""
        task_id = f"val_{validation_type.value}_{worker_id}_{int(time.time())}"
        
        task = ValidationTask(
            task_id=task_id,
            validation_type=validation_type,
            files=files,
            worker_id=worker_id,
            created_at=time.time()
        )
        
        return task
        
    def run_validation_task(self, task: ValidationTask) -> ValidationTask:
        """Run a validation task on a specific worker."""
        if task.worker_id not in self.workers:
            # Assign to first available worker
            available_workers = [wid for wid, worker in self.workers.items() if not worker.is_active]
            if available_workers:
                task.worker_id = available_workers[0]
            else:
                # No workers available, return failed task
                task.result = ValidationResult.FAIL
                task.errors.append(ValidationError(
                    file_path="system",
                    line_number=None,
                    error_type="no_workers",
                    message="No validation workers available",
                    severity="error"
                ))
                return task
                
        worker = self.workers[task.worker_id]
        result = worker.run_validation_task(task)
        self.validation_history.append(result)
        self.save_validation_log()
        return result
        
    def run_parallel_validation(self, tasks: List[ValidationTask]) -> Dict[str, ValidationTask]:
        """Run multiple validation tasks in parallel."""
        if not self.workers:
            return {}
            
        results = {}
        
        # Use ThreadPoolExecutor for parallel validation
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all validation tasks
            future_to_task = {
                executor.submit(self.run_validation_task, task): task
                for task in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results[task.task_id] = result
                except Exception as e:
                    # Create failed task result
                    failed_task = ValidationTask(
                        task_id=task.task_id,
                        validation_type=task.validation_type,
                        files=task.files,
                        worker_id=task.worker_id,
                        created_at=task.created_at,
                        completed_at=time.time(),
                        result=ValidationResult.FAIL,
                        errors=[ValidationError(
                            file_path="system",
                            line_number=None,
                            error_type="execution_error",
                            message=f"Task execution failed: {str(e)}",
                            severity="error"
                        )],
                        duration=time.time() - task.created_at
                    )
                    results[task.task_id] = failed_task
                    
        return results
        
    def get_worker_status(self, worker_id: str) -> Optional[Dict]:
        """Get status of a specific worker."""
        if worker_id in self.workers:
            worker = self.workers[worker_id]
            return {
                'worker_id': worker_id,
                'is_active': worker.is_active,
                'tasks_processed': worker.tasks_processed,
                'errors_found': worker.errors_found
            }
        return None
        
    def get_all_workers_status(self) -> Dict[str, Dict]:
        """Get status of all workers."""
        return {
            worker_id: self.get_worker_status(worker_id)
            for worker_id in self.workers
        }
        
    def get_validation_summary(self) -> Dict:
        """Get summary of all validation operations."""
        total_tasks = len(self.validation_history)
        passed_tasks = len([t for t in self.validation_history if t.result == ValidationResult.PASS])
        failed_tasks = len([t for t in self.validation_history if t.result == ValidationResult.FAIL])
        warning_tasks = len([t for t in self.validation_history if t.result == ValidationResult.WARNING])
        
        total_errors = sum(len(task.errors) for task in self.validation_history)
        
        # Group errors by type
        error_types = {}
        for task in self.validation_history:
            for error in task.errors:
                error_type = error.error_type
                if error_type not in error_types:
                    error_types[error_type] = 0
                error_types[error_type] += 1
                
        return {
            'total_tasks': total_tasks,
            'passed_tasks': passed_tasks,
            'failed_tasks': failed_tasks,
            'warning_tasks': warning_tasks,
            'pass_rate': (passed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'total_errors': total_errors,
            'error_types': error_types,
            'worker_statuses': self.get_all_workers_status()
        }


def main():
    # Example usage
    print("Parallel Validation Workers System")
    print("=" * 35)
    
    # Create validation manager
    manager = ParallelValidationManager(max_workers=4)
    
    # Add some workers
    manager.add_worker("validator1")
    manager.add_worker("validator2")
    manager.add_worker("validator3")
    
    print("Parallel validation manager initialized with 3 workers")
    print("System ready to run multiple validation processes simultaneously")
    
    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Create validation tasks for different file types")
    print("  2. Run syntax validation on all markdown files")
    print("  3. Run link validation on documentation files")
    print("  4. Run content validation on user guides")
    print("  5. Aggregate results and generate reports")


if __name__ == "__main__":
    main()