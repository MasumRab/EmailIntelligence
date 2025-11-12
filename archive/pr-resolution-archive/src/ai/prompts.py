"""
Prompt engineering templates for AI analysis
"""

from typing import Dict, List, Any
import json

class PromptTemplates:
    """Templates for AI analysis prompts"""
    
    # System prompt for consistent AI behavior
    SYSTEM_PROMPT = """
You are an expert software engineering AI assistant specializing in code conflict analysis and pull request resolution. 
Your role is to analyze conflicts, assess complexity, and suggest resolution strategies for software development teams.

Guidelines:
- Provide detailed, actionable analysis
- Consider technical feasibility and impact
- Be conservative with confidence scores
- Focus on practical resolution strategies
- Consider team expertise and available resources
- Always provide alternative approaches when possible
- Rate complexity on a scale of 1-10 (1=trivial, 10=impossible)
- Rate confidence on a scale of 0.0-1.0 (0.0=very low confidence, 1.0=very high confidence)

When analyzing conflicts, consider:
1. File dependencies and relationships
2. Code complexity and changes scope
3. Potential impact on existing functionality
4. Risk assessment and rollback considerations
5. Required expertise and resources
6. Timeline and business impact
"""

    # Conflict analysis prompt
    CONFLICT_ANALYSIS_PROMPT = """
Analyze the following pull request conflicts and provide detailed assessment:

PR Information:
- Title: {title}
- Description: {description}
- Source Branch: {source_branch}
- Target Branch: {target_branch}
- Files Changed: {file_count} files
- Total Lines Changed: {lines_changed}

Conflicts Detected:
{conflicts}

Provide analysis in the following JSON format:
{{
    "overall_assessment": "Brief summary of the conflicts",
    "complexity_score": <1-10 integer>,
    "estimated_resolution_time": <minutes>,
    "confidence_score": <0.0-1.0 float>,
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "detailed_analysis": {{
        "dependency_conflicts": "Analysis of file dependencies",
        "semantic_conflicts": "Analysis of code semantics",
        "merge_conflicts": "Analysis of text-level conflicts",
        "architectural_impact": "Impact on system architecture"
    }},
    "resolution_strategies": [
        {{
            "strategy": "Brief strategy name",
            "description": "Detailed description",
            "pros": ["advantage 1", "advantage 2"],
            "cons": ["disadvantage 1", "disadvantage 2"],
            "complexity": <1-10>,
            "time_estimate": <minutes>,
            "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
            "required_expertise": ["skill 1", "skill 2"]
        }}
    ]
}}
"""

    # Resolution suggestion prompt
    RESOLUTION_SUGGESTION_PROMPT = """
Based on the following conflict analysis, suggest 3 specific resolution strategies:

Conflict Analysis:
{analysis}

Context:
- Team Size: {team_size}
- Developer Experience Level: {experience_level}
- Available Timeline: {timeline}
- Business Priority: {priority}

For each strategy, provide:
1. Step-by-step implementation plan
2. Required code changes
3. Testing approach
4. Rollback plan
5. Success criteria
6. Potential blockers

Format as JSON:
{{
    "strategies": [
        {{
            "name": "Strategy name",
            "approach": "High-level approach",
            "steps": ["step 1", "step 2", "step 3"],
            "code_changes": "Description of required changes",
            "testing_plan": "How to test the solution",
            "rollback_plan": "How to rollback if needed",
            "success_criteria": ["criteria 1", "criteria 2"],
            "potential_blockers": ["blocker 1", "blocker 2"],
            "estimated_time": <minutes>,
            "complexity": <1-10>,
            "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
            "confidence": <0.0-1.0>
        }}
    ],
    "recommended_approach": "Which strategy to use first and why",
    "alternative_approaches": "What to try if the primary approach fails"
}}
"""

    # Complexity assessment prompt
    COMPLEXITY_ASSESSMENT_PROMPT = """
Assess the complexity of the following pull request changes:

PR Details:
{pr_details}

Changed Files:
{file_details}

Dependencies:
{dependency_info}

Provide a detailed complexity assessment:

{{
    "overall_complexity": <1-10 integer>,
    "technical_complexity": <1-10 integer>,
    "coordination_complexity": <1-10 integer>,
    "testing_complexity": <1-10 integer>,
    "maintenance_complexity": <1-10 integer>,
    "detailed_breakdown": {{
        "code_changes": "Analysis of code changes",
        "testing_effort": "Analysis of testing required",
        "documentation_effort": "Analysis of documentation required",
        "coordination_effort": "Analysis of team coordination needed",
        "deployment_complexity": "Analysis of deployment challenges"
    }},
    "risk_factors": [
        {{
            "factor": "Risk factor name",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "probability": <0.0-1.0>,
            "impact": <1-10 integer>,
            "mitigation": "How to mitigate this risk"
        }}
    ],
    "confidence_score": <0.0-1.0>,
    "reasoning": "Detailed explanation of complexity assessment"
}}
"""

    # Solution validation prompt
    SOLUTION_VALIDATION_PROMPT = """
Validate the proposed solution for this conflict:

Conflict: {conflict_description}
Proposed Solution: {proposed_solution}
Current Code State: {current_code}
Target Code State: {target_code}

Assess the solution using these criteria:
1. Technical correctness
2. Code quality and style
3. Performance impact
4. Security implications
5. Maintainability
6. Testability
7. Backward compatibility

Provide validation result in JSON format:
{{
    "validation_result": "APPROVED|CONDITIONAL|REJECTED",
    "confidence_score": <0.0-1.0>,
    "detailed_assessment": {{
        "technical_correctness": {{
            "score": <0.0-1.0>,
            "feedback": "Analysis of technical correctness"
        }},
        "code_quality": {{
            "score": <0.0-1.0>,
            "feedback": "Analysis of code quality"
        }},
        "performance": {{
            "score": <0.0-1.0>,
            "feedback": "Analysis of performance impact"
        }},
        "security": {{
            "score": <0.0-1.0>,
            "feedback": "Security implications"
        }},
        "maintainability": {{
            "score": <0.0-1.0>,
            "feedback": "Maintainability analysis"
        }}
    }},
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ],
    "potential_issues": [
        {{
            "issue": "Potential problem",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "likelihood": <0.0-1.0>,
            "mitigation": "How to address this issue"
        }}
    ],
    "overall_feedback": "General feedback on the solution"
}}
"""

    @classmethod
    def format_prompt(
        cls, 
        template: str, 
        **kwargs
    ) -> str:
        """Format a prompt template with provided values"""
        return template.format(**kwargs)
    
    @classmethod
    def create_messages(
        cls, 
        system_prompt: str = None,
        user_prompt: str = None,
        **kwargs
    ) -> List[Dict[str, str]]:
        """Create messages for OpenAI chat completion"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        if user_prompt:
            formatted_prompt = cls.format_prompt(user_prompt, **kwargs)
            messages.append({
                "role": "user", 
                "content": formatted_prompt
            })
        
        return messages
    
    @classmethod
    def analyze_conflict_prompt(
        cls,
        pr_data: Dict[str, Any],
        conflict_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Create conflict analysis prompt"""
        conflicts_text = "\n".join([
            f"- Type: {c.get('type', 'Unknown')}\n  Description: {c.get('description', 'N/A')}\n  Files: {', '.join(c.get('files', []))}"
            for c in conflict_data.get('conflicts', [])
        ])
        
        return cls.create_messages(
            system_prompt=cls.SYSTEM_PROMPT,
            user_prompt=cls.CONFLICT_ANALYSIS_PROMPT,
            title=pr_data.get('title', 'N/A'),
            description=pr_data.get('description', 'N/A'),
            source_branch=pr_data.get('source_branch', 'N/A'),
            target_branch=pr_data.get('target_branch', 'N/A'),
            file_count=len(pr_data.get('files', [])),
            lines_changed=pr_data.get('lines_changed', 0),
            conflicts=conflicts_text or "No conflicts detected"
        )
    
    @classmethod
    def resolution_suggestion_prompt(
        cls,
        analysis: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Create resolution suggestion prompt"""
        return cls.create_messages(
            system_prompt=cls.SYSTEM_PROMPT,
            user_prompt=cls.RESOLUTION_SUGGESTION_PROMPT,
            analysis=json.dumps(analysis, indent=2),
            team_size=context.get('team_size', 5),
            experience_level=context.get('experience_level', 'intermediate'),
            timeline=context.get('timeline', 'standard'),
            priority=context.get('priority', 'medium')
        )
    
    @classmethod
    def complexity_assessment_prompt(
        cls,
        pr_data: Dict[str, Any],
        dependency_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Create complexity assessment prompt"""
        return cls.create_messages(
            system_prompt=cls.SYSTEM_PROMPT,
            user_prompt=cls.COMPLEXITY_ASSESSMENT_PROMPT,
            pr_details=json.dumps(pr_data, indent=2),
            file_details=json.dumps(dependency_data.get('files', []), indent=2),
            dependency_info=json.dumps(dependency_data, indent=2)
        )
    
    @classmethod
    def solution_validation_prompt(
        cls,
        conflict: Dict[str, Any],
        solution: str,
        code_context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Create solution validation prompt"""
        return cls.create_messages(
            system_prompt=cls.SYSTEM_PROMPT,
            user_prompt=cls.SOLUTION_VALIDATION_PROMPT,
            conflict_description=json.dumps(conflict, indent=2),
            proposed_solution=solution,
            current_code=code_context.get('current_code', 'N/A'),
            target_code=code_context.get('target_code', 'N/A')
        )


# Few-shot examples for complex scenarios
FEW_SHOT_EXAMPLES = {
    "merge_conflict": {
        "input": "Two developers modified the same function in different ways",
        "output": {
            "complexity": 6,
            "strategy": "Manual merge with code review",
            "confidence": 0.8
        }
    },
    "dependency_conflict": {
        "input": "PR changes version of dependency that affects multiple modules",
        "output": {
            "complexity": 8,
            "strategy": "Update all dependent modules, extensive testing",
            "confidence": 0.7
        }
    },
    "architectural_violation": {
        "input": "PR introduces pattern that violates system architecture",
        "output": {
            "complexity": 9,
            "strategy": "Refactor architecture or redesign approach",
            "confidence": 0.6
        }
    }
}


def get_few_shot_examples(conflict_type: str) -> List[Dict[str, str]]:
    """Get few-shot examples for specific conflict type"""
    return FEW_SHOT_EXAMPLES.get(conflict_type, [])