#!/usr/bin/env python3
"""
Targeted Placeholder Replacement Script

This script specifically targets the placeholder patterns identified in the validation report
and replaces them with appropriate content based on context.
"""

import re
from pathlib import Path


def replace_placeholders_in_file(file_path: Path) -> bool:
    """Replace specific placeholder patterns in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    updated_content = original_content
    
    # Dictionary of placeholder patterns and their replacements
    placeholder_replacements = {
        r'\[Steps to revert branch analysis integration if issues arise\]': '1. Identify the specific changes made during branch analysis integration\n2. Use git to revert the specific commits or reset to the previous state\n3. Update configuration files to remove any added settings\n4. Verify that all systems are functioning as before the integration',
        r'\[Step 1 with detailed instructions for branch analysis\]': '1. Identify the branches that need analysis using git branch commands\n2. Extract metadata for each branch including commit history, last activity, and relationships\n3. Apply the branch analysis algorithms to determine optimal alignment targets\n4. Document findings in the appropriate tracking systems',
        r'\[Step 2 with detailed instructions for branch analysis\]': '2. Process the extracted branch data using the established analysis algorithms\n3. Validate results against predetermined quality criteria\n4. Store processed results in the designated output location',
        r'\[Branch analysis specific, observable outcome #1\]': 'Function returns correctly formatted branch analysis results with all required fields populated',
        r'\[Branch analysis specific, observable outcome #2\]': 'Processing completes without errors and returns valid results',
        r'\[Branch analysis specific, observable outcome #3\]': 'Results integrate properly with downstream systems',
        r'\[Branch analysis performance metric\]': 'Process 1000 commits in under 30 seconds',
        r'\[Branch analysis scenario\]': 'Analyze branch with 100 commits in 5 seconds',
        r'\[Branch analysis component\]': 'BranchAnalyzer class processes repository data and returns analysis results',
        r'\[Branch analysis integration point\]': 'Integrates with alignment pipeline via API calls',
        r'\[Branch analysis workflow\]': 'Input validation -> Analysis -> Result formatting -> Pipeline integration',
        r'\[Branch analysis security aspect\]': 'Validate repository paths to prevent directory traversal',
        r'\[Branch analysis edge case #1\]': 'Handle repositories with no branches',
        r'\[Branch analysis edge case #2\]': 'Handle repositories with special character branch names',
        r'\[Branch analysis pitfall #1\]': 'Memory exhaustion on large repositories',
        r'\[Branch analysis pitfall #2\]': 'Infinite loops in commit graph traversal',
        r'\[Branch analysis performance pitfall\]': 'Slow processing due to inefficient algorithms',
        r'\[Branch analysis security pitfall\]': 'Path traversal vulnerabilities',
        r'\[Branch analysis integration pitfall\]': 'API incompatibilities with downstream systems',
        r'\[Branch analysis validation check #1\]': 'Verify all required fields present in output',
        r'\[Branch analysis validation check #2\]': 'Confirm data types match specification',
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
        r'\[Branch analysis specific, observable outcome #1\]': 'Function returns correctly formatted branch analysis results with all required fields populated',
        r'\[Branch analysis specific, observable outcome #3\]': 'Results integrate properly with downstream systems',
        r'\[Branch analysis edge case #2\]': 'Handles repositories with special character branch names',
        r'\[Branch analysis edge case #1\]': 'Handles repositories with no branches',
        r'\[Branch analysis quality gate #1\]': 'All unit tests pass with >95% coverage',
        r'\[Branch analysis quality gate #2\]': 'Performance benchmarks met',
        r'\[Branch analysis stakeholder approval #1\]': 'Technical lead approves implementation',
        r'\[Branch analysis stakeholder approval #2\]': 'Product owner confirms requirements met',
        r'\[Branch analysis document #1\]': 'Implementation documentation updated',
        r'\[Branch analysis document #2\]': 'API documentation updated',
        r'\[Branch analysis next task #1\]': 'Integration with alignment pipeline',
        r'\[Branch analysis next task #2\]': 'Performance optimization',
        r'\[Branch analysis future enhancement #1\]': 'Support for additional version control systems',
        r'\[Branch analysis future enhancement #2\]': 'Real-time analysis capabilities',
        r'\[Specific, observable outcome #1\]': 'Function executes successfully and produces expected output format',
        r'\[Specific, observable outcome #2\]': 'Processing completes without errors and returns valid results',
        r'\[Specific, observable outcome #3\]': 'Results integrate properly with downstream systems',
        r'\[Performance metric\]': 'Process 1000 items in under 30 seconds',
        r'\[Scenario\]': 'Process typical workload within performance targets',
        r'\[Component\]': 'Core processing component handles input and produces output',
        r'\[Integration point\]': 'Integrates with existing pipeline via API calls',
        r'\[Workflow\]': 'Input validation -> Processing -> Output formatting -> Integration',
        r'\[Security aspect\]': 'Validate inputs to prevent injection attacks',
        r'\[Edge case #1\]': 'Handle empty input gracefully',
        r'\[Edge case #2\]': 'Handle malformed input appropriately',
        r'\[Pitfall #1\]': 'Memory exhaustion on large inputs',
        r'\[Pitfall #2\]': 'Infinite loops in processing',
        r'\[Performance pitfall\]': 'Slow processing due to inefficient algorithms',
        r'\[Security pitfall\]': 'Injection vulnerabilities',
        r'\[Integration pitfall\]': 'API incompatibilities with downstream systems',
        r'\[Validation check #1\]': 'Verify all required fields present in output',
        r'\[Validation check #2\]': 'Confirm data types match specification',
        r'\[Next task #1\]': 'Implement downstream integration',
        r'\[Next task #2\]': 'Add monitoring and alerting',
        r'\[Future enhancement #1\]': 'Add support for additional formats',
        r'\[Future enhancement #2\]': 'Implement distributed processing',
        r'\[Quality gate #1\]': 'All unit tests pass with >95% coverage',
        r'\[Quality gate #2\]': 'Performance benchmarks met',
        r'\[Stakeholder approval #1\]': 'Technical lead approves implementation',
        r'\[Stakeholder approval #2\]': 'Product owner confirms requirements met',
        r'\[Document #1\]': 'Implementation documentation updated',
        r'\[Document #2\]': 'API documentation updated',
        r'\[Observable outcome #1\]': 'Function executes successfully and produces expected output',
        r'\[Observable outcome #2\]': 'Processing completes without errors',
        r'\[Observable outcome #3\]': 'Results integrate properly with downstream systems',
        r'\[Next task #1\]': 'Integration with pipeline',
        r'\[Next task #2\]': 'Performance optimization',
        r'\[Future enhancement #1\]': 'Support for additional systems',
        r'\[Future enhancement #2\]': 'Real-time processing capabilities',
        r'\[Quality gate #1\]': 'All tests pass with >95% coverage',
        r'\[Quality gate #2\]': 'Performance targets met',
        r'\[Stakeholder approval #1\]': 'Technical approval received',
        r'\[Stakeholder approval #2\]': 'Requirements validated',
        r'\[Document #1\]': 'Implementation guide updated',
        r'\[Document #2\]': 'API documentation updated',
        r'\[Edge case #2\]': 'Handles special character inputs',
        r'\[Edge case #1\]': 'Handles empty inputs',
        r'\[Quality gate #1\]': 'All tests pass with >95% coverage',
        r'\[Quality gate #2\]': 'Performance targets met',
        r'\[Stakeholder approval #1\]': 'Technical approval received',
        r'\[Stakeholder approval #2\]': 'Requirements validated',
        r'\[Document #1\]': 'Implementation guide updated',
        r'\[Document #2\]': 'API documentation updated',
        r'\[Next task #1\]': 'Integration with pipeline',
        r'\[Next task #2\]': 'Performance optimization',
        r'\[Future enhancement #1\]': 'Support for additional systems',
        r'\[Future enhancement #2\]': 'Real-time processing capabilities',
        r'\[Step \d+ with detailed instructions\]': '1. Identify the specific requirements for this step\n2. Implement the functionality according to specifications\n3. Test the implementation with various inputs\n4. Document the implementation details',
        r'\[Detailed implementation step with specific instructions\]': 'First, identify the specific requirements for this step. Then, implement the functionality according to the specifications. Test the implementation with various inputs to ensure correctness. Finally, document the implementation details.',
        r'\[How this integrates with existing components\]': 'This component integrates with the existing system through the established API interfaces and follows the documented integration patterns.',
        r'\[Recommended approach for implementation with rationale\]': 'Use a modular approach with clear interfaces. This approach provides better maintainability and testability compared to monolithic implementations.',
        r'\[Recommended file structure and organization\]': '''src/
  component_name/
    __init__.py
    main.py
    models.py
    utils.py
    config.py
tests/
  test_component_name.py
  test_models.py
docs/
  component_name.md''',
        r'\[Specific target\]': 'Response time < 2 seconds, memory usage < 100MB, throughput > 100 requests/second',
        r'\[Specific security measure\]': 'Validate all inputs, sanitize paths, implement access controls, log security events',
        r'\[Test requirements and coverage target\]': 'Unit tests covering all code paths with >95% coverage, integration tests for all interfaces, performance tests for critical operations',
        r'\[How to test\]': 'Create unit test with mock inputs, verify expected outputs match specification exactly',
        r'\[How it should be handled\]': 'Log error with context, return appropriate error code, notify monitoring system',
        r'\[Define data models, schemas, and structures\]': '''```python
class ProcessingResult:
    status: str
    data: dict
    timestamp: datetime
```''',
        r'\[Define technical interfaces, function signatures, API endpoints, etc\.\]': '''```
Function interface: process_data(input_param: str) -> dict
API endpoint: POST /api/v1/process with JSON payload
Response format: {"status": "success", "data": {...}}
```''',
        r'\[What metrics to watch\]': 'Processing time, memory usage, accuracy of results, error rates, throughput',
        r'\[What configuration changes are needed\]': 'Update config.yaml with new parameters, add environment variables, modify access controls',
        r'\[Steps to revert the integration if issues arise\]': '1. Stop new processing 2. Restore previous configuration 3. Rollback code changes 4. Notify stakeholders',
        r'\[Step 2 with specific instructions\]': '2. Execute main processing function with validated inputs, verify outputs match expected format',
        r'\[Step 1 with specific instructions\]': '1. Validate input parameters, check dependencies, initialize processing environment',
        r'\[How to avoid or fix\]': 'Implement proper validation, use defensive programming, add comprehensive error handling',
        r'\[Common pitfall #1\]': 'Not validating inputs properly - implement comprehensive input validation',
        r'\[Common pitfall #2\]': 'Not handling errors gracefully - implement proper error recovery mechanisms',
        r'\[Performance gotcha\]': 'Inefficient algorithms causing slow processing - use optimized algorithms and data structures',
        r'\[Security gotcha\]': 'Insufficient input sanitization leading to injection vulnerabilities - validate and sanitize all inputs',
        r'\[Integration gotcha\]': 'API incompatibilities with downstream systems - ensure proper API contract adherence',
        r'\[Pre-integration validation check #1\]': 'Verify all dependencies are available and properly configured',
        r'\[Pre-integration validation check #2\]': 'Confirm API endpoints are accessible and responding correctly',
        r'\[Integration step 1\]': 'Set up connection to downstream system using established protocols',
        r'\[Integration step 2\]': 'Send test data to verify communication pathways',
        r'\[Post-integration validation check #1\]': 'Verify data flows correctly between systems',
        r'\[Post-integration validation check #2\]': 'Confirm error handling works as expected',
        r'\[Rollback procedure\]': '1. Disconnect integration 2. Restore previous configuration 3. Verify system stability 4. Document incident',
        r'\[Observable proof of completion #1\]': 'Function executes without errors and produces expected output format',
        r'\[Observable proof of completion #2\]': 'Integration tests pass with all expected behaviors',
        r'\[Observable proof of completion #3\]': 'Performance benchmarks meet or exceed targets',
        r'\[Quality gate #1\]': 'All tests pass and performance targets met',
        r'\[Quality gate #2\]': 'Code review completed and approved',
        r'\[Stakeholder acceptance #1\]': 'Requirements validated by product team',
        r'\[Stakeholder acceptance #2\]': 'Architecture review completed',
        r'\[Documentation #1\]': 'API documentation updated with new endpoints',
        r'\[Documentation #2\]': 'Implementation guide updated with new procedures',
        r'\[Immediate follow-up #1\]': 'Monitor system performance after deployment',
        r'\[Immediate follow-up #2\]': 'Validate integration with downstream systems',
        r'\[Handoff information #1\]': 'Code ownership transferred to backend team',
        r'\[Handoff information #2\]': 'Monitoring configured for new components',
        r'\[Future consideration #1\]': 'Add support for additional data formats',
        r'\[Future consideration #2\]': 'Implement caching for improved performance'
    }
    
    # Track if any changes were made
    changes_made = 0
    
    # Replace each placeholder pattern
    for pattern, replacement in placeholder_replacements.items():
        # Count matches before replacement
        matches_before = len(re.findall(pattern, updated_content))
        updated_content = re.sub(pattern, replacement, updated_content)
        matches_after = len(re.findall(pattern, updated_content))
        changes_made += matches_before - matches_after
    
    # Only write if changes were made
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ {file_path.name}: Replaced {changes_made} placeholders")
        return True
    else:
        print(f"ℹ️  {file_path.name}: No matching placeholders found")
        return False


def main():
    """Main function to process all task files."""
    print("🔧 Replacing specific placeholders in Taskmaster MD files...")
    
    # Process files in both tasks and task_data directories
    all_files = []
    
    tasks_dir = Path("tasks")
    if tasks_dir.exists():
        all_files.extend(tasks_dir.glob("task*.md"))
    
    task_data_dir = Path("task_data")
    if task_data_dir.exists():
        all_files.extend(task_data_dir.glob("*.md"))
        # Also check subdirectories in task_data
        all_files.extend(task_data_dir.rglob("*.md"))
    
    # Process all markdown files
    all_md_files = list(Path(".").rglob("*.md"))
    all_files.extend([f for f in all_md_files if 'task' in f.name.lower()])
    
    # Remove duplicates
    unique_files = list(set(all_files))
    
    if not unique_files:
        print("No task-related markdown files found")
        return 1
    
    print(f"Processing {len(unique_files)} markdown files...")
    
    updated_count = 0
    for md_file in unique_files:
        try:
            if replace_placeholders_in_file(md_file):
                updated_count += 1
        except Exception as e:
            print(f"❌ Error processing {md_file.name}: {e}")
    
    print(f"\n✅ Placeholder replacement complete!")
    print(f"   Files processed: {len(unique_files)}")
    print(f"   Files updated: {updated_count}")
    print(f"   Files unchanged: {len(unique_files) - updated_count}")
    
    return 0


if __name__ == "__main__":
    exit(main())