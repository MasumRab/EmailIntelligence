#!/usr/bin/env python3
"""
MD File Enhancer for Taskmaster

This script helps enhance MD files by replacing common placeholders with more
specific content for successful Jules task completion.
"""

import re
from pathlib import Path
from typing import List, Dict


class MDFileEnhancer:
    """Enhances MD files by replacing placeholders with specific content."""
    
    # Mapping of common placeholders to suggested replacements
    PLACEHOLDER_REPLACEMENTS = {
        r'\[Method to verify completion\]': 'Run the associated test suite and confirm all tests pass with >95% coverage',
        r'\[Define technical interfaces, function signatures, API endpoints, etc\.\]': '''```
Class interface: MyComponent(input_param: str) -> dict
Function signature: process_data(data: list) -> dict
API endpoint: POST /api/v1/process with JSON payload
```''',
        r'\[Test requirements\]': 'Unit tests covering all code paths, integration tests for API endpoints, performance tests for critical operations',
        r'\[How to test\]': 'Create unit test with mock inputs, verify expected outputs match specification exactly',
        r'\[How it should be handled\]': 'Log error with context, return appropriate error code, notify monitoring system',
        r'\[Specific target\]': 'Response time < 2 seconds, memory usage < 100MB, throughput > 100 requests/second',
        r'\[What configuration changes are needed for branch analysis\]': 'Update config.yaml with new parameters, add environment variables, modify access controls',
        r'\[What branch analysis metrics to watch\]': 'Processing time, memory usage, accuracy of branch identification, false positive rate',
        r'\[Specific branch analysis test data sets needed for comprehensive testing\]': 'Sample repositories with various branch states, edge cases with deleted branches, large repositories with many branches',
        r'\[Branch analysis specific, observable outcome #\d+\]': 'Function returns correctly formatted branch analysis results with all required fields populated',
        r'\[Branch analysis edge case #\d+\]': 'Handles repositories with no branches, deleted branches, branches with special characters in names',
        r'\[What indicates this problem\]': 'Error messages in logs, unexpected behavior during execution, incorrect output format',
        r'\[Steps to migrate from previous implementation\]': '1. Backup current configuration 2. Update dependencies 3. Run migration script 4. Verify functionality',
        r'\[Step \d+ with detailed instructions\]': '1. Import required modules 2. Initialize configuration 3. Execute main function 4. Validate output',
        r'\[Specific, observable outcome #\d+\]': 'Function executes without errors and produces expected output format',
        r'\[How this integrates with existing components\]': 'Calls existing API endpoints, uses shared configuration, follows established patterns',
        r'\[param_name\]': 'detailed_parameter_name',
        r'\[type\]': 'str',
        r'\[default\]': '"default_value"',
        r'\[validation_rule\]': 'Required, must match expected format',
        r'\[var_name\]': 'DETAILED_ENVIRONMENT_VARIABLE_NAME',
        r'\[yes/no\]': 'yes',
        r'\[Time requirement\]': '< 2 seconds for typical inputs',
        r'\[Throughput requirement\]': '> 100 operations per second',
        r'\[Limit for.*?\]': '< 100MB memory, < 5 second execution time',
        r'\[Number\]': '10 concurrent operations',
        r'\[Size/quantity.*?\]': 'Up to 10,000 items',
        r'\[Expected increase.*?\]': 'Linear growth with input size',
        r'\[Current.*?\]': 'Baseline performance measured at project start',
        r'\[Coverage target\]': '> 95% code coverage',
        r'\[Specific.*?\]': 'As defined in requirements specification',
        r'\[Quantity\]': 'As many as needed for complete coverage',
        r'\[Symptom:.*?\]': '[Specific error message or behavior observed]',
        r'\[Cause:.*?\]': '[Root cause of the issue]',
        r'\[Solution:.*?\]': '[Specific steps to resolve the issue]',
        r'\[Branch analysis.*?\]': '[Specific to branch analysis requirements]',
        r'\[Step \d+\]': 'Detailed implementation step with specific instructions',
        r'\[Code example.*?\]': '''```python
# Example implementation
def example_function(param: str) -> dict:
    return {"result": param}
```'''
    }
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.tasks_dir = self.project_root / "tasks"
    
    def find_task_files(self) -> List[Path]:
        """Find all task MD files in the project."""
        if not self.tasks_dir.exists():
            return []
        
        task_files = []
        for file_path in self.tasks_dir.glob("*.md"):
            if "task-" in file_path.name.lower() or "task_" in file_path.name.lower():
                task_files.append(file_path)
                
        # Also check in subdirectories like task_data
        for file_path in (self.project_root / "task_data").rglob("*.md"):
            if "task-" in file_path.name.lower() or "task_" in file_path.name.lower():
                task_files.append(file_path)
                
        return task_files
    
    def enhance_file(self, file_path: Path) -> bool:
        """Enhance a single MD file by replacing placeholders."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            enhanced_content = original_content
            
            # Replace all known placeholders
            changes_made = 0
            for pattern, replacement in self.PLACEHOLDER_REPLACEMENTS.items():
                # Count matches before replacement
                matches_before = len(re.findall(pattern, enhanced_content))
                enhanced_content = re.sub(pattern, replacement, enhanced_content)
                matches_after = len(re.findall(pattern, enhanced_content))
                changes_made += matches_before - matches_after
            
            # Only write if changes were made
            if changes_made > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_content)
                
                print(f"✅ Enhanced {file_path.name}: {changes_made} placeholders replaced")
                return True
            else:
                print(f"ℹ️  No changes needed for {file_path.name}")
                return False
                
        except Exception as e:
            print(f"❌ Error enhancing {file_path.name}: {str(e)}")
            return False
    
    def enhance_all_files(self) -> Dict[str, any]:
        """Enhance all task files in the project."""
        task_files = self.find_task_files()
        results = {
            'processed': 0,
            'enhanced': 0,
            'errors': 0,
            'file_results': []
        }
        
        for file_path in task_files:
            results['processed'] += 1
            try:
                enhanced = self.enhance_file(file_path)
                if enhanced:
                    results['enhanced'] += 1
                results['file_results'].append({
                    'file': str(file_path),
                    'enhanced': enhanced
                })
            except Exception as e:
                results['errors'] += 1
                results['file_results'].append({
                    'file': str(file_path),
                    'error': str(e)
                })
        
        return results


def main():
    """Main function to run the enhancer."""
    print("🔧 Enhancing Taskmaster MD files...")
    
    enhancer = MDFileEnhancer()
    results = enhancer.enhance_all_files()
    
    print(f"\n📊 Enhancement Summary:")
    print(f"   Files processed: {results['processed']}")
    print(f"   Files enhanced: {results['enhanced']}")
    print(f"   Errors: {results['errors']}")
    
    if results['enhanced'] > 0:
        print(f"\n✅ Enhancement complete! {results['enhanced']} files updated.")
        print("The MD files now have more specific content for successful Jules task completion.")
    else:
        print("\nℹ️  No files needed enhancement or all files were already processed.")


if __name__ == "__main__":
    main()