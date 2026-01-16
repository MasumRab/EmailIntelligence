"""
Enhanced PRD Generation Prompts

This module contains improved prompts and templates for better task-to-PRD conversion.
These prompts are designed to address the low similarity scores identified in the
Ralph loop analysis by providing more explicit guidance for each aspect of PRD generation.
"""

# Enhanced prompts for extracting information from task markdown files
EXTRACT_TASK_INFO_PROMPT = """
You are analyzing a task markdown file to extract key information for PRD generation.
Follow these steps to extract information accurately:

1. Extract the task ID from the filename or the heading (look for patterns like 'Task ID: XX' or '# Task XX')
2. Extract the task title from the main heading (after removing 'Task ID:' prefix)
3. Extract metadata from bold sections:
   - Status: Look for "**Status:**" or "**Status**"
   - Priority: Look for "**Priority:**" or "**Priority**"
   - Effort: Look for "**Effort:**" or "**Effort**" (should contain hour estimates)
   - Complexity: Look for "**Complexity:**" or "**Complexity**" (should be a number/level)
   - Dependencies: Look for "**Dependencies:**" or "**Dependencies**" (comma-separated task IDs)
   - Blocks: Look for "**Blocks:**" or "**Blocks**" (task IDs this task blocks)
4. Extract content from specific sections:
   - Purpose: Content under "## Purpose" section
   - Details: Content under "## Details" section
   - Test Strategy: Content under "## Test Strategy" section
   - Success Criteria: Checklist items under "## Success Criteria" (items starting with '- [ ]' or '- [x]')
5. Extract subtasks if they exist in table format (look for tables with columns like ID, Subtask, Status, Effort)

Return the extracted information in a structured format with clear separation of each element.
"""

# Enhanced prompt for generating capability names
GENERATE_CAPABILITY_NAME_PROMPT = """
Create a meaningful capability name based on the task information provided.
The capability name should be descriptive and reflect the core functionality or purpose of the task.

Guidelines:
1. If the task title is already descriptive, use it as the capability name
2. If the title is generic, create a name based on the purpose/description
3. Use patterns like "[Action]: [Domain]" or "[Domain] [Action]" where appropriate
4. Action words might include: Analysis, Implementation, Design, Testing, Documentation, Integration, Validation
5. Domain words might reflect the specific area of functionality

Example transformations:
- "Align feature branches" → "Branch Alignment Capability"
- "Implement validation framework" → "Validation Framework Implementation"
- "Create CI/CD integration" → "CI/CD Pipeline Integration"

Input: {task_info}
Output only the capability name:
"""

# Enhanced prompt for generating feature descriptions
GENERATE_FEATURE_DESCRIPTION_PROMPT = """
Create a comprehensive feature description based on the task information.
The description should be clear, concise, and capture the essence of what the feature does.

Requirements:
1. Start with an action verb (Implement, Create, Design, Validate, etc.)
2. Describe what the feature does in 1-2 sentences
3. Mention the key benefit or value it provides
4. If the purpose section is available, incorporate key elements from it
5. Limit to 100-150 words maximum

Input task information:
Title: {title}
Purpose: {purpose}
Details: {details}

Output the feature description:
"""

# Enhanced prompt for generating dependency relationships
GENERATE_DEPENDENCY_GRAPH_PROMPT = """
Analyze the task information to create an accurate dependency graph.
Follow these steps:

1. Identify all tasks that this task depends on (from the dependencies field)
2. Parse the dependencies string to extract individual task IDs
3. Handle various formats: comma-separated, space-separated, or "and" separated
4. Remove common prefixes like "Task" or "task" from dependency strings
5. Create relationships showing which tasks must be completed before others
6. Group tasks by dependency layers for topological ordering:
   - Foundation layer: Tasks with no dependencies
   - Layer 1: Tasks that depend only on foundation layer tasks
   - Layer 2: Tasks that depend on foundation or Layer 1 tasks
   - And so on...

Input tasks with dependencies:
{task_dependencies}

Output the dependency graph with proper layering and relationships:
"""

# Enhanced prompt for structuring success criteria
STRUCTURE_SUCCESS_CRITERIA_PROMPT = """
Transform the success criteria into a standardized, structured format.
Each criterion should be:
1. Specific and measurable
2. Action-oriented
3. Testable
4. Clear and unambiguous

Convert each success criterion into an acceptance criteria table format:
- Create a meaningful Criteria ID based on the first few words of the criterion
- Use the original criterion text as the description
- Add a placeholder for the verification method

Input criteria:
{criteria_list}

Output in this format:
| Criteria ID | Description | Verification Method |
|-------------|-------------|-------------------|
| [ID based on criterion] | [Original criterion text] | [Test method] |

Also suggest improvements if any criteria seem vague or unmeasurable.
"""

# Enhanced prompt for effort and complexity assessment
ASSESS_EFFORT_COMPLEXITY_PROMPT = """
Analyze the task information to provide standardized effort and complexity assessments.

For effort estimation:
1. Extract hour ranges from the effort field (e.g., "2-4 hours" or "3 hours")
2. Convert to a standardized format: "X-Y hours (approximately X-Y hours)"
3. If only a single number is provided, create a range (e.g., "3 hours" becomes "2-4 hours")

For complexity assessment:
1. Convert complexity levels to standardized format (e.g., "Medium" to "5/10", "High" to "8/10")
2. If numeric, keep as is (e.g., "7/10" or "7")
3. Add context about what the complexity encompasses

Input:
Effort: {effort}
Complexity: {complexity}
Task details: {details}

Output standardized assessments:
"""

# Enhanced template for capability sections
CAPABILITY_TEMPLATE = """### Capability: {capability_name}
[Brief description of what this capability domain covers: {capability_description}]

#### Feature: {feature_title}
- **Description**: {feature_description}
- **Inputs**: [What it needs - {inputs}]
- **Outputs**: [What it produces - {outputs}]
- **Behavior**: [Key logic - {behavior}]

{effort_section}{complexity_section}{acceptance_criteria_section}
"""

# Enhanced template for dependency graph sections
DEPENDENCY_GRAPH_TEMPLATE = """## Dependency Chain

### Foundation Layer (Phase 0)
{foundation_tasks}

{layer_definitions}
"""

# Enhanced prompt for PRD validation
VALIDATE_PRD_PROMPT = """
Validate that the generated PRD follows the expected RPG (Repository Planning Graph) structure.

Required sections:
1. <overview> with Problem Statement, Target Users, Success Metrics
2. <functional-decomposition> with Capability Tree
3. <structural-decomposition> with Repository Structure
4. <dependency-graph> with Dependency Chain
5. <implementation-roadmap> with Development Phases
6. <test-strategy> with Critical Test Scenarios
7. <architecture> with System Components and Tech Stack
8. <risks> with Technical Risks
9. <appendix> with Open Questions
10. <task-master-integration> section

Check that:
- All required opening and closing tags are present
- Each section contains appropriate content
- Capability and feature mappings are meaningful
- Dependencies are properly structured
- Success criteria are in standardized format
- Effort and complexity are in standardized format

PRD content to validate:
{prd_content}

List any missing sections or formatting issues:
"""

# Enhanced prompt for improving PRD based on validation feedback
IMPROVE_PRD_PROMPT = """
Based on the validation feedback, improve the PRD content to address the identified issues.

Validation feedback:
{validation_feedback}

Original PRD content:
{original_prd}

Make specific corrections to address each issue mentioned in the validation feedback.
Maintain the RPG structure and ensure all required sections are present with appropriate content.
Focus on improving:
1. Missing sections
2. Improper formatting
3. Incomplete capability/feature mappings
4. Incorrect dependency structures
5. Unstructured success criteria
6. Non-standardized effort/complexity assessments

Output the improved PRD:
"""

# Enhanced prompt for measuring PRD quality
MEASURE_PRD_QUALITY_PROMPT = """
Evaluate the quality of the PRD based on these criteria:

1. Completeness: Does it contain all required RPG sections?
2. Accuracy: Do the capabilities/features accurately represent the original tasks?
3. Structure: Is the information organized according to RPG method?
4. Clarity: Are descriptions clear and unambiguous?
5. Consistency: Are effort, complexity, and criteria standardized?
6. Relationships: Are dependencies properly mapped?

Rate each criterion from 1-10 and provide specific feedback.

PRD content to evaluate:
{prd_content}

Evaluation:
"""