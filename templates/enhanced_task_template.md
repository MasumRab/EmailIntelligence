# Enhanced Task Template for Maximum PRD Generation Accuracy

## 1. Task Header with Complete Metadata
```
# Task ID: [XX.YY] [Descriptive Title That Clearly Indicates Functionality]

**Status:** [pending | in-progress | completed | blocked | deferred]
**Priority:** [critical | high | medium | low]
**Effort:** [XX-YY hours] (Range with specific estimate)
**Complexity:** [X/10] (With brief justification)
**Dependencies:** [Task IDs separated by commas, or "None"]
**Blocks:** [Task IDs this task unblocks, or "None"]
**Owner:** [Assignee, or "TBD"]
**Created:** [YYYY-MM-DD]
**Updated:** [YYYY-MM-DD]
**Tags:** [comma-separated tags for categorization]
```

## 2. Comprehensive Purpose/Overview Section
```
## Overview/Purpose

[2-3 sentences explaining what this task accomplishes and why it matters]

**Scope:** [Clear boundary of what is included/excluded]
**Focus:** [Primary objective of this task]
**Value Proposition:** [What value this delivers to users/developers]
**Success Indicator:** [How you'll know this is working]
```

## 3. Detailed Success Criteria with Verification Methods
```
## Success Criteria

Task [ID] is complete when:

### Functional Requirements
- [ ] [Specific, measurable outcome #1] - Verification: [How to verify completion]
- [ ] [Specific, measurable outcome #2] - Verification: [How to verify completion]
- [ ] [Specific, measurable outcome #3] - Verification: [How to verify completion]

### Non-Functional Requirements
- [ ] [Performance requirement] - Verification: [How to verify completion]
- [ ] [Security requirement] - Verification: [How to verify completion]
- [ ] [Compatibility requirement] - Verification: [How to verify completion]

### Quality Gates
- [ ] [Code quality gate] - Verification: [How to verify completion]
- [ ] [Test coverage gate] - Verification: [How to verify completion]
- [ ] [Documentation gate] - Verification: [How to verify completion]
```

## 4. Prerequisites & Dependencies with Justification
```
## Prerequisites & Dependencies

### Required Before Starting
- [ ] [Prerequisite #1] - Justification: [Why this is needed]
- [ ] [Prerequisite #2] - Justification: [Why this is needed]

### Blocks (What This Task Unblocks)
- [ ] Task [ID]: [Description of what becomes possible]
- [ ] Task [ID]: [Description of what becomes possible]

### External Dependencies
- [ ] [External dependency #1] - Version: [Version requirement]
- [ ] [External dependency #2] - Version: [Version requirement]

### Assumptions & Constraints
- [Constraint #1]: [Brief explanation]
- [Constraint #2]: [Brief explanation]
```

## 5. Comprehensive Sub-subtasks Breakdown
```
## Sub-subtasks Breakdown

### [ID.XX]: [Descriptive Subtask Title]
**Effort:** [X-Y hours]
**Depends on:** [Other subtasks or external dependencies]
**Priority:** [high | medium | low]

**Objective:** [What this subtask specifically accomplishes]

**Steps:**
1. [Detailed step #1 with specific actions]
2. [Detailed step #2 with specific actions]
3. [Detailed step #3 with specific actions]

**Deliverables:**
- [ ] [Specific deliverable #1]
- [ ] [Specific deliverable #2]

**Acceptance Criteria:**
- [ ] [Verifiable condition #1]
- [ ] [Verifiable condition #2]

**Resources Needed:**
- [Resource #1]
- [Resource #2]

---
```

## 6. Detailed Specification Details
```
## Specification Details

### Technical Interface
```
[Code interface specification - function signatures, API endpoints, data structures]
```

### Data Models
[Entity relationship diagrams, class diagrams, or data structure definitions]

### Business Logic
[Detailed explanation of the core algorithms, decision points, and business rules]

### Error Handling
- [Error condition #1]: Log error with context, return appropriate error code, notify monitoring system
- [Error condition #2]: Log error with context, return appropriate error code, notify monitoring system

### Performance Requirements
- [Requirement #1]: [Specific metric]
- [Requirement #2]: [Specific metric]

### Security Requirements
- [Requirement #1]: Validate all inputs, sanitize paths, implement access controls, log security events
- [Requirement #2]: Validate all inputs, sanitize paths, implement access controls, log security events
```

## 7. Implementation Guide with Code Patterns
```
## Implementation Guide

### Approach
Use a modular approach with clear interfaces. This approach provides better maintainability and testability compared to monolithic implementations.

### Code Structure
src/
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
  component_name.md

### Key Implementation Steps
1. 1. Identify the specific requirements for this step
2. Implement the functionality according to specifications
3. Test the implementation with various inputs
4. Document the implementation details
   ```python
   # Example code snippet
   def example_function():
       pass
   ```

2. 1. Identify the specific requirements for this step
2. Implement the functionality according to specifications
3. Test the implementation with various inputs
4. Document the implementation details
   ```javascript
   // Example code snippet
   const exampleFunction = () => {
     // Implementation
   };
   ```

### Integration Points
This component integrates with the existing system through the established API interfaces and follows the documented integration patterns.

### Configuration Requirements
Update config.yaml with new parameters, add environment variables, modify access controls

### Migration Steps (if applicable)
[Steps to migrate from previous implementation]
```

## 8. Configuration Parameters with Validation
```
## Configuration Parameters

### Required Parameters
| Parameter | Type | Default | Validation | Description |
|-----------|------|---------|------------|-------------|
| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |

### Optional Parameters
| Parameter | Type | Default | Validation | Description |
|-----------|------|---------|------------|-------------|
| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |

### Environmental Variables
| Variable | Required | Description |
|----------|----------|-------------|
| [var_name] | [yes/no] | [what it controls] |
```

## 9. Performance Targets with Benchmarks
```
## Performance Targets

### Response Time Requirements
- Process typical workload within performance targets: [Time requirement] (e.g., API calls respond in < 200ms)

### Throughput Requirements
- Process typical workload within performance targets: [Throughput requirement] (e.g., process 1000 requests/second)

### Resource Utilization
- Memory: [Limit] (e.g., < 100MB RAM usage)
- CPU: [Limit] (e.g., < 20% average CPU usage)
- Disk: [Limit] (e.g., < 10MB storage requirement)

### Scalability Targets
- Concurrent users: [Number]
- Data volume: [Size/quantity]
- Growth rate: [Expected increase over time period]

### Baseline Measurements
[Current performance metrics for comparison]
```

## 10. Comprehensive Testing Strategy
```
## Testing Strategy

### Unit Tests
- Core processing component handles input and produces output: Unit tests covering all code paths with >95% coverage, integration tests for all interfaces, performance tests for critical operations
- Core processing component handles input and produces output: Unit tests covering all code paths with >95% coverage, integration tests for all interfaces, performance tests for critical operations

### Integration Tests
- Integrates with existing pipeline via API calls: [Test requirements]
- Integrates with existing pipeline via API calls: [Test requirements]

### End-to-End Tests
- [User workflow]: [Test requirements]
- [User workflow]: [Test requirements]

### Performance Tests
- [Test scenario]: [Performance target]
- [Test scenario]: [Performance target]

### Security Tests
- Validate inputs to prevent injection attacks: [Test requirement]
- Validate inputs to prevent injection attacks: [Test requirement]

### Edge Case Tests
- Handles empty inputs: Create unit test with mock inputs, verify expected outputs match specification exactly
- Handles special character inputs: Create unit test with mock inputs, verify expected outputs match specification exactly

### Test Data Requirements
[Specific test data sets needed for comprehensive testing]
```

## 11. Common Gotchas & Solutions
```
## Common Gotchas & Solutions

### Known Pitfalls
1. **Memory exhaustion on large inputs**
   - **Symptom:** [What indicates this problem]
   - **Cause:** [Why this happens]
   - **Solution:** Implement proper validation, use defensive programming, add comprehensive error handling

2. **Infinite loops in processing**
   - **Symptom:** [What indicates this problem]
   - **Cause:** [Why this happens]
   - **Solution:** Implement proper validation, use defensive programming, add comprehensive error handling

### Performance Gotchas
- Slow processing due to inefficient algorithms: [How to avoid]

### Security Gotchas
- Injection vulnerabilities: [How to avoid]

### Integration Gotchas
- API incompatibilities with downstream systems: [How to avoid]
```

## 12. Integration Checkpoint with Validation
```
## Integration Checkpoint

### Pre-Integration Validation
- [ ] Verify all required fields present in output
- [ ] Confirm data types match specification

### Integration Steps
1. 1. Validate input parameters, check dependencies, initialize processing environment
2. 2. Execute main processing function with validated inputs, verify outputs match expected format

### Post-Integration Validation
- [ ] Verify all required fields present in output
- [ ] Confirm data types match specification

### Rollback Procedure
1. Stop new processing 2. Restore previous configuration 3. Rollback code changes 4. Notify stakeholders
```

## 13. Done Definition with Observable Proof
```
## Done Definition

### Observable Proof of Completion
- [ ] Function executes successfully and produces expected output format
- [ ] Processing completes without errors and returns valid results
- [ ] Results integrate properly with downstream systems

### Quality Gates Passed
- [ ] All tests pass and performance targets met
- [ ] Code review completed and approved

### Stakeholder Acceptance
- [ ] Technical approval received
- [ ] Requirements validated

### Documentation Complete
- [ ] Implementation guide updated updated
- [ ] API documentation updated updated
```

## 14. Next Steps with Handoff Information
```
## Next Steps

### Immediate Follow-ups
- [ ] Integration with pipeline - Owner: [Person/Team], Due: [Date]
- [ ] Performance optimization - Owner: [Person/Team], Due: [Date]

### Handoff Information
- **Code Ownership:** [Which team/module owns this code]
- **Maintenance Contact:** [Who to contact for issues]
- **Monitoring:** Processing time, memory usage, accuracy of results, error rates, throughput

### Future Considerations
- Support for additional systems
- Real-time processing capabilities
```

---

## Additional Guidelines for Maximum PRD Accuracy

### Information Density Requirements
- Each section should contain specific, actionable information
- Avoid generic phrases like "implement functionality" - be specific
- Include quantitative measures wherever possible
- Provide context for dependencies and relationships

### Terminology Consistency
- Use consistent technical terminology throughout
- Define domain-specific terms in the purpose section
- Link to external documentation if needed

### Verification Methods
- Each success criterion must have a clear verification method
- Include both automated and manual verification approaches
- Specify tools or techniques to use for verification

### Risk Considerations
- Identify potential risks in the implementation guide
- Include mitigation strategies in the gotchas section
- Consider performance, security, and scalability risks