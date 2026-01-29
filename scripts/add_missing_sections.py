#!/usr/bin/env python3
"""
Add Missing Sections to MD Files

This script adds missing required sections to MD files according to the 14-section standard.
"""

import re
from pathlib import Path


def add_missing_sections(file_path: Path):
    """Add missing required sections to a task file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = content
    changes_made = False
    
    # Required sections in the correct order according to the 14-section standard
    required_sections = [
        "Task Header",
        "Overview/Purpose", 
        "Success Criteria",
        "Prerequisites & Dependencies",
        "Sub-subtasks Breakdown",
        "Specification Details",
        "Implementation Guide",
        "Configuration Parameters",
        "Performance Targets",
        "Testing Strategy",
        "Common Gotchas & Solutions",
        "Integration Checkpoint",
        "Done Definition",
        "Next Steps"
    ]
    
    for section in required_sections:
        # Check if section exists (with various possible formats)
        section_exists = (
            f"## {section}" in updated_content or
            f"### {section}" in updated_content or
            f"# {section}" in updated_content
        )
        
        if not section_exists:
            # Add the missing section with a basic template
            if section == "Overview/Purpose":
                section_content = f"## {section}\n\n[Provide a brief explanation of what this task accomplishes and why it matters]\n\n"
            elif section == "Success Criteria":
                section_content = f"## {section}\n\n- [ ] [Specific, measurable outcome #1] - Verification: [Method to verify completion]\n- [ ] [Specific, measurable outcome #2] - Verification: [Method to verify completion]\n- [ ] [Specific, measurable outcome #3] - Verification: [Method to verify completion]\n\n"
            elif section == "Prerequisites & Dependencies":
                section_content = f"## {section}\n\n### Required Before Starting\n- [ ] [Prerequisite #1]\n- [ ] [Prerequisite #2]\n\n### Dependencies\n- [ ] [Dependency #1]\n- [ ] [Dependency #2]\n\n### External Dependencies\n- [ ] [External dependency #1]\n\n"
            elif section == "Sub-subtasks Breakdown":
                section_content = f"## {section}\n\n### 1.1: [Subtask title]\n- **Status**: pending\n- **Dependencies**: [dependency list]\n- **Details**: [Detailed description of what this subtask involves]\n\n### 1.2: [Subtask title]\n- **Status**: pending\n- **Dependencies**: [dependency list]\n- **Details**: [Detailed description of what this subtask involves]\n\n"
            elif section == "Specification Details":
                section_content = f"## {section}\n\n### Technical Interface\n```\n[Define technical interfaces, function signatures, API endpoints, etc.]\n```\n\n### Data Models\n[Define data models, schemas, and structures]\n\n### Business Logic\n[Describe core algorithms, decision points, and business rules]\n\n### Error Handling\n[How different error conditions should be handled]\n\n"
            elif section == "Implementation Guide":
                section_content = f"## {section}\n\n### Approach\n[Recommended approach for implementation with rationale]\n\n### Code Structure\n[Recommended file structure and organization]\n\n### Key Implementation Steps\n1. [Step 1 with detailed instructions]\n   ```\n   [Code example]\n   ```\n\n2. [Step 2 with detailed instructions]\n   ```\n   [Code example]\n   ```\n\n### Integration Points\n[How this integrates with existing components]\n\n### Configuration Requirements\n[What configuration changes are needed]\n\n### Migration Steps (if applicable)\n[Steps to migrate from previous implementation]\n\n"
            elif section == "Configuration Parameters":
                section_content = f"## {section}\n\n### Required Parameters\n| Parameter | Type | Default | Validation | Description |\n|-----------|------|---------|------------|-------------|\n| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |\n\n### Optional Parameters\n| Parameter | Type | Default | Validation | Description |\n|-----------|------|---------|------------|-------------|\n| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |\n\n### Environmental Variables\n| Variable | Required | Description |\n|----------|----------|-------------|\n| [var_name] | [yes/no] | [what it controls] |\n\n"
            elif section == "Performance Targets":
                section_content = f"## {section}\n\n### Response Time Requirements\n- [Scenario]: [Time requirement]\n\n### Throughput Requirements\n- [Scenario]: [Throughput requirement]\n\n### Resource Utilization\n- Memory: [Limit]\n- CPU: [Limit]\n- Disk: [Limit]\n\n### Scalability Targets\n- Concurrent users: [Number]\n- Data volume: [Size/quantity]\n- Growth rate: [Expected increase over time period]\n\n### Baseline Measurements\n[Current performance metrics for comparison]\n\n"
            elif section == "Testing Strategy":
                section_content = f"## {section}\n\n### Unit Tests\n- [Component]: [Test requirements and coverage target]\n\n### Integration Tests\n- [Integration point]: [Test requirements]\n\n### End-to-End Tests\n- [User workflow]: [Test requirements]\n\n### Performance Tests\n- [Test scenario]: [Performance target]\n\n### Security Tests\n- [Security aspect]: [Test requirement]\n\n### Edge Case Tests\n- [Edge case #1]: [How to test]\n- [Edge case #2]: [How to test]\n\n### Test Data Requirements\n[Specific test data sets needed for comprehensive testing]\n\n"
            elif section == "Common Gotchas & Solutions":
                section_content = f"## {section}\n\n### Known Pitfalls\n1. **[Pitfall #1]**\n   - **Symptom:** [What indicates this problem]\n   - **Cause:** [Why this happens]\n   - **Solution:** [How to avoid or fix]\n\n2. **[Pitfall #2]**\n   - **Symptom:** [What indicates this problem]\n   - **Cause:** [Why this happens]\n   - **Solution:** [How to avoid or fix]\n\n### Performance Gotchas\n- [Performance pitfall]: [How to avoid]\n\n### Security Gotchas\n- [Security pitfall]: [How to avoid]\n\n### Integration Gotchas\n- [Integration pitfall]: [How to avoid]\n\n"
            elif section == "Integration Checkpoint":
                section_content = f"## {section}\n\n### Pre-Integration Validation\n- [ ] [Validation check #1]\n- [ ] [Validation check #2]\n\n### Integration Steps\n1. [Step 1 with specific instructions]\n2. [Step 2 with specific instructions]\n\n### Post-Integration Validation\n- [ ] [Validation check #1]\n- [ ] [Validation check #2]\n\n### Rollback Procedure\n[Steps to revert the integration if issues arise]\n\n"
            elif section == "Done Definition":
                section_content = f"## {section}\n\n### Observable Proof of Completion\n- [ ] [Specific, observable outcome #1]\n- [ ] [Specific, observable outcome #2]\n- [ ] [Specific, observable outcome #3]\n\n### Quality Gates Passed\n- [ ] [Quality gate #1]\n- [ ] [Quality gate #2]\n\n### Stakeholder Acceptance\n- [ ] [Stakeholder approval #1]\n- [ ] [Stakeholder approval #2]\n\n### Documentation Complete\n- [ ] [Document #1] updated\n- [ ] [Document #2] updated\n\n"
            elif section == "Next Steps":
                section_content = f"## {section}\n\n### Immediate Follow-ups\n- [ ] [Next task #1] - Owner: [Person/Team], Due: [Date]\n- [ ] [Next task #2] - Owner: [Person/Team], Due: [Date]\n\n### Handoff Information\n- **Code Ownership:** [Which team/module owns this code]\n- **Maintenance Contact:** [Who to contact for issues]\n- **Monitoring:** [What metrics to watch]\n\n### Future Considerations\n- [Future enhancement #1]\n- [Future enhancement #2]\n\n"
            else:  # For Task Header (should already be handled separately)
                section_content = f"## {section}\n\n[Task header content should go here]\n\n"
            
            # Add the section content to the updated content
            updated_content += section_content
            changes_made = True
            print(f"  Added section: {section}")
    
    # Only write if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ {file_path.name}: Added missing sections")
        return True
    else:
        print(f"ℹ️  {file_path.name}: No missing sections to add")
        return False


def main():
    """Main function to process all task files."""
    print("🔧 Adding missing sections to Taskmaster MD files...")
    
    tasks_dir = Path("tasks")
    task_files = list(tasks_dir.glob("task*.md"))
    
    if not task_files:
        print("No task files found in tasks/ directory")
        return 1
    
    print(f"Processing {len(task_files)} task files...")
    
    updated_count = 0
    for task_file in task_files:
        try:
            if add_missing_sections(task_file):
                updated_count += 1
        except Exception as e:
            print(f"❌ Error processing {task_file.name}: {e}")
    
    print(f"\n✅ Added missing sections to {updated_count} files")
    print("Files now have all required sections according to the 14-section standard.")
    
    return 0


if __name__ == "__main__":
    exit(main())