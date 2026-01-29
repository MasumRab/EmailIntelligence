#!/usr/bin/env python3
"""
Advanced MD File Enhancer for Taskmaster

This script helps enhance MD files by replacing additional placeholder patterns 
with more specific content for successful Jules task completion.
"""

import re
from pathlib import Path
from typing import List, Dict


class AdvancedMDFileEnhancer:
    """Enhances MD files by replacing additional placeholder patterns."""
    
    # Additional mapping of remaining placeholders to suggested replacements
    ADDITIONAL_PLACEHOLDER_REPLACEMENTS = {
        r'\[Test requirements and coverage target\]': 'Unit tests covering all code paths with >95% coverage, integration tests for all interfaces, performance tests for critical operations',
        r'\[How to avoid\]': 'Follow established patterns, validate inputs, implement proper error handling, use defensive programming techniques',
        r'\[What indicates this problem in branch analysis\]': 'Incorrect branch identification, mismatched analysis results, unexpected processing errors',
        r'\[Steps to migrate from previous branch analysis approaches\]': '1. Backup current configuration 2. Update dependencies 3. Run migration script 4. Validate results 5. Update documentation',
        r'\[Step 2 with detailed instructions for branch analysis\]': '2. Process branch data using established algorithms, validate results against expected format, store in designated location',
        r'\[Specific to branch analysis requirements\]': 'Accurate branch identification, proper handling of merge commits, correct lineage tracking',
        r'\[How to avoid or fix branch analysis issue\]': 'Validate branch data before processing, implement proper error recovery, use consistent data formats',
        r'\[How branch analysis integrates with alignment pipeline\]': 'Pass analysis results to alignment engine, update status tracking, trigger downstream processes',
        r'\[Define technical interfaces, function signatures, API endpoints, etc\. specific to branch analysis\]': '''```
Function: analyze_branch(repo_path: str, branch_name: str) -> dict
API: GET /api/v1/branches/{branch_name}/analysis
Response: {"branch_name": str, "analysis": {...}}
```''',
        r'\[Define data models for branch analysis results, clustering outputs, or identification data\]': '''```python
class BranchAnalysis:
    branch_name: str
    commit_count: int
    last_activity: datetime
    analysis_result: dict
```''',
        r'\[What metrics to watch\]': 'Processing time, memory usage, accuracy of analysis, error rates, throughput',
        r'\[What configuration changes are needed\]': 'Update config.yaml with new parameters, add environment variables, modify access controls',
        r'\[Steps to revert the integration if issues arise\]': '1. Stop new processing 2. Restore previous configuration 3. Rollback code changes 4. Notify stakeholders',
        r'\[Step 2 with specific instructions\]': '2. Execute main processing function with validated inputs, verify outputs match expected format',
        r'\[Step 1 with specific instructions\]': '1. Validate input parameters, check dependencies, initialize processing environment',
        r'\[How to avoid or fix\]': 'Implement proper validation, use defensive programming, add comprehensive error handling',
        r'\[Define data models, schemas, and structures\]': '''```python
class ProcessingResult:
    status: str
    data: dict
    timestamp: datetime
```''',
        r'\[What this subtask accomplishes\]': 'Implements the core functionality for the defined requirements, ensuring all success criteria are met',
        r'\[Recommended approach for branch analysis implementation with rationale\]': '''Use GitPython for repository access, implement efficient commit traversal algorithms, cache results for performance.
Rationale: GitPython provides reliable access to git data, efficient algorithms ensure performance, caching reduces redundant operations.''',
        r'\[Recommended file structure and organization for branch analysis components\]': '''
src/
  branch_analysis/
    __init__.py
    analyzer.py
    models.py
    utils.py
    config.py
tests/
  test_branch_analysis.py
  test_models.py
''',
        r'\[Branch analysis performance metric\]': 'Process 1000 commits in under 30 seconds',
        r'\[Specific security measure\]': 'Validate all inputs, sanitize paths, implement access controls, log security events',
        r'\[Branch analysis scenario\]': 'Analyze branch with 100 commits in 5 seconds',
        r'\[Branch analysis component\]': 'BranchAnalyzer class processes repository data and returns analysis results',
        r'\[Branch analysis integration point\]': 'Integrates with alignment pipeline via API calls',
        r'\[Branch analysis workflow\]': 'Input validation -> Analysis -> Result formatting -> Pipeline integration',
        r'\[Branch analysis security aspect\]': 'Validate repository paths to prevent directory traversal',
        r'\[Branch analysis edge case #1\]': 'Handle repositories with no commits',
        r'\[Branch analysis edge case #2\]': 'Handle repositories with special character branch names',
        r'\[Branch analysis pitfall #1\]': 'Memory exhaustion on large repositories',
        r'\[Branch analysis pitfall #2\]': 'Infinite loops in commit graph traversal',
        r'\[Branch analysis performance pitfall\]': 'Slow processing due to inefficient algorithms',
        r'\[Branch analysis security pitfall\]': 'Path traversal vulnerabilities',
        r'\[Branch analysis integration pitfall\]': 'API incompatibilities with downstream systems',
        r'\[Branch analysis validation check #1\]': 'Verify all required fields present in output',
        r'\[Branch analysis validation check #2\]': 'Confirm data types match specification',
        r'\[Branch analysis specific, observable outcome #2\]': 'Processing completes without errors and returns valid results',
        r'\[Branch analysis next task #1\]': 'Implement downstream integration with alignment engine',
        r'\[Branch analysis next task #2\]': 'Add monitoring and alerting for processing failures',
        r'\[Branch analysis future enhancement #1\]': 'Add support for additional repository formats',
        r'\[Branch analysis future enhancement #2\]': 'Implement distributed processing for large repositories',
        r'\[Branch analysis quality gate #1\]': 'All unit tests pass with >95% coverage',
        r'\[Branch analysis quality gate #2\]': 'Performance benchmarks met',
        r'\[Branch analysis stakeholder approval #1\]': 'Technical lead approves implementation',
        r'\[Branch analysis stakeholder approval #2\]': 'Product owner confirms requirements met',
        r'\[Branch analysis document #1\]': 'Implementation documentation updated',
        r'\[Branch analysis document #2\]': 'API documentation updated',
        r'\[Branch analysis specific, observable outcome #1\]': 'Function executes successfully and produces expected output format',
        r'\[Branch analysis specific, observable outcome #3\]': 'Results integrate properly with downstream systems',
        r'\[Branch analysis edge case #2\]': 'Handles repositories with special character branch names',
        r'\[Branch analysis edge case #1\]': 'Handles repositories with no branches',
        r'\[Branch analysis quality gate #1\]': 'All tests pass and performance targets met',
        r'\[Branch analysis quality gate #2\]': 'Code review completed and approved',
        r'\[Branch analysis stakeholder approval #1\]': 'Requirements validated by product team',
        r'\[Branch analysis stakeholder approval #2\]': 'Architecture review completed',
        r'\[Branch analysis document #1\]': 'API documentation updated with new endpoints',
        r'\[Branch analysis document #2\]': 'Implementation guide updated with new procedures',
        r'\[Branch analysis next task #1\]': 'Integration with alignment pipeline',
        r'\[Branch analysis next task #2\]': 'Performance optimization',
        r'\[Branch analysis future enhancement #1\]': 'Support for additional version control systems',
        r'\[Branch analysis future enhancement #2\]': 'Real-time analysis capabilities'
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
        """Enhance a single MD file by replacing additional placeholders."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            enhanced_content = original_content
            
            # Replace all additional known placeholders
            changes_made = 0
            for pattern, replacement in self.ADDITIONAL_PLACEHOLDER_REPLACEMENTS.items():
                # Count matches before replacement
                matches_before = len(re.findall(pattern, enhanced_content))
                enhanced_content = re.sub(pattern, replacement, enhanced_content)
                matches_after = len(re.findall(pattern, enhanced_content))
                changes_made += matches_before - matches_after
            
            # Only write if changes were made
            if changes_made > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_content)
                
                print(f"✅ Enhanced {file_path.name}: {changes_made} additional placeholders replaced")
                return True
            else:
                print(f"ℹ️  No additional changes needed for {file_path.name}")
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
    """Main function to run the advanced enhancer."""
    print("🔧 Enhancing Taskmaster MD files with additional patterns...")
    
    enhancer = AdvancedMDFileEnhancer()
    results = enhancer.enhance_all_files()
    
    print(f"\n📊 Enhancement Summary:")
    print(f"   Files processed: {results['processed']}")
    print(f"   Files enhanced: {results['enhanced']}")
    print(f"   Errors: {results['errors']}")
    
    if results['enhanced'] > 0:
        print(f"\n✅ Additional enhancement complete! {results['enhanced']} files updated.")
        print("More placeholder content has been replaced with specific requirements for successful Jules task completion.")
    else:
        print("\nℹ️  No additional files needed enhancement.")


if __name__ == "__main__":
    main()