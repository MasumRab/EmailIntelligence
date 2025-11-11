# Speckit Conversation Framework: Prompt Creation Guide

## Objective
Provide LLM with clear guidance to start productive conversations with users about creating effective Speckit prompts.

## Conversation Initiation Pattern

When a user asks about creating a Speckit specify prompt, the LLM should:

1. **Acknowledge the request**: "I can help you create an effective Speckit specify prompt."

2. **Explain the importance**: "A well-crafted Speckit prompt is crucial for generating useful specifications, plans, and implementation tasks."

3. **Guide through key elements**:

### Essential Information to Gather:
- **Problem/Goal**: What specific issue are you trying to solve?
- **Scope**: What is included/excluded from this feature?
- **Context**: What existing systems/components does this interact with?
- **Constraints**: Any limitations, deadlines, or requirements?
- **Success criteria**: How will you know this is done successfully?

### Template Framework:
```
/speckit.specify 

Feature: [Clear, concise name]
Goal: [What specific problem this solves]
Context: [Relevant background information]
Scope: [What's in/out of scope]
Requirements: [Key functional requirements]
Constraints: [Technical, timeline, or other constraints]
Success: [How to verify completion]
```

4. **Offer to help refine**: "Would you like to walk through these elements for your specific use case?"

5. **Be prepared to iterate**: "We can refine this prompt together until it captures all your needs."

## Important Notes for LLM:
- Always emphasize that Speckit generates plans/specifications but actual implementation requires separate execution
- Guide users toward specific, actionable language rather than vague concepts
- Remind them to consider their constitution principles during specification
- Explain that the output will be a plan that still requires manual implementation to execute Git operations, etc.
- Use examples relevant to their specific project domain when possible