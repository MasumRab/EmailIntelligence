"""
AI Prompt Engineering System for Conflict Resolution

This module provides sophisticated prompt generation for AI-powered conflict resolution,
including specialized templates for different conflict types, few-shot learning examples,
and context-aware prompt adaptation.
"""

import json
from typing import List, Dict, Any, Union
from enum import Enum
from dataclasses import dataclass
import structlog

from .types import (
    ConflictTypeExtended, MergeConflict, DependencyConflict,
    ArchitectureViolation
)

logger = structlog.get_logger()


class PromptTemplateType(str, Enum):
    """Types of prompt templates"""
    STRATEGY_GENERATION = "strategy_generation"
    CODE_GENERATION = "code_generation"
    VALIDATION = "validation"
    ANALYSIS = "analysis"
    FEW_SHOT_EXAMPLE = "few_shot_example"
    ITERATIVE_REFINEMENT = "iterative_refinement"
    QUALITY_ASSESSMENT = "quality_assessment"


@dataclass
class PromptContext:
    """Context for prompt generation"""
    conflict_type: ConflictTypeExtended
    severity: str
    confidence: float
    affected_files: List[str]
    system_context: Dict[str, Any]
    constraints: List[str]
    success_criteria: List[str]
    risk_tolerance: str
    available_tools: List[str]
    performance_requirements: Dict[str, Any]


@dataclass
class FewShotExample:
    """Few-shot learning example for prompts"""
    input: Dict[str, Any]
    output: Dict[str, Any]
    quality_score: float
    success_rate: float
    context: Dict[str, Any]


class PromptEngine:
    """
    AI Prompt Engineering System for Conflict Resolution
    
    Provides sophisticated prompt generation with:
    - Specialized templates for different conflict types
    - Few-shot learning with successful resolution examples  
    - Context-aware adaptation based on conflict severity
    - Iterative refinement for complex resolutions
    - Quality assessment prompts
    """
    
    def __init__(self):
        self.templates = self._load_templates()
        self.examples = self._load_few_shot_examples()
        self.performance_cache = {}
        self.template_stats = {
            "total_generated": 0,
            "successful_prompts": 0,
            "average_quality": 0.0,
            "template_usage": {}
        }
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load prompt templates for different conflict types and purposes"""
        return {
            # Strategy Generation Templates
            "merge_conflict_strategy": {
                "template": """You are an expert software engineer specializing in merge conflict resolution.

**CONFLICT CONTEXT:**
- File: {file_path}
- Conflict Type: {conflict_type}
- Severity: {severity}
- PR1: {pr1_id} - {content1_preview}
- PR2: {pr2_id} - {content2_preview}
- Base: {base_content_preview}

**TASK:** Generate a comprehensive resolution strategy that:
1. Analyzes the semantic differences between the conflicting changes
2. Preserves the intent and functionality of both PRs
3. Minimizes code duplication and complexity
4. Maintains code quality and testability

**OUTPUT FORMAT:**
Return a JSON object with:
{{
  "strategy": {{
    "name": "Clear, descriptive strategy name",
    "approach": "High-level approach description",
    "steps": [
      {{
        "id": "step_1",
        "description": "Detailed step description",
        "code_changes": ["Specific code change description"],
        "validation": ["Validation step"],
        "estimated_time": 60,
        "risk_level": "LOW|MEDIUM|HIGH"
      }}
    ],
    "pros": ["Advantage 1", "Advantage 2"],
    "cons": ["Disadvantage 1", "Disadvantage 2"],
    "confidence": 0.95,
    "estimated_time": 300,
    "risk_level": "LOW|MEDIUM|HIGH",
    "requires_approval": true,
    "success_criteria": ["Criterion 1", "Criterion 2"],
    "rollback_strategy": "Rollback approach",
    "validation_approach": "How to validate the solution"
  }}
}}""",
                
                "variables": [
                    "file_path", "conflict_type", "severity", "pr1_id", "pr2_id",
                    "content1_preview", "content2_preview", "base_content_preview"
                ]
            },
            
            "dependency_conflict_strategy": {
                "template": """You are an expert software architect specializing in dependency conflict resolution.

**CONFLICT CONTEXT:**
- Conflict Type: {conflict_type}
- Affected Modules: {affected_modules}
- Cycle Path: {cycle_path}
- Version Conflicts: {version_conflicts}
- Severity: {severity}

**ARCHITECTURAL PRINCIPLES TO CONSIDER:**
- Single Responsibility Principle
- Dependency Inversion Principle
- Acyclic Dependencies Principle
- Interface Segregation Principle

**TASK:** Generate a resolution strategy that:
1. Breaks circular dependencies
2. Resolves version conflicts
3. Maintains architectural integrity
4. Minimizes refactoring impact

**OUTPUT FORMAT:**
{{
  "strategy": {{
    "name": "Strategy name",
    "approach": "Architectural approach",
    "steps": [
      {{
        "id": "refactor_step_1",
        "description": "Refactoring step",
        "architectural_changes": ["Change 1", "Change 2"],
        "validation": ["Architecture check"],
        "estimated_time": 120,
        "risk_level": "MEDIUM"
      }}
    ],
    "pros": ["Benefit 1", "Benefit 2"],
    "cons": ["Cost 1", "Cost 2"],
    "confidence": 0.88,
    "estimated_time": 600,
    "risk_level": "HIGH",
    "requires_approval": true,
    "success_criteria": ["No circular dependencies", "Version conflicts resolved"],
    "rollback_strategy": "Git-based rollback with dependency restoration"
  }}
}}""",
                
                "variables": [
                    "conflict_type", "affected_modules", "cycle_path", 
                    "version_conflicts", "severity"
                ]
            },
            
            "architecture_violation_strategy": {
                "template": (
                    """You are a software architecture expert specializing in """
                    """pattern violations and refactoring.

**VIOLATION CONTEXT:**
- Pattern: {pattern_name}
- Violation Type: {violation_type}
- Affected Components: {affected_components}
- Violating PRs: {violating_prs}
- Severity: {severity}
- Layer Violations: {layer_violations}

**ARCHITECTURAL PATTERNS TO CONSIDER:**
- Layered Architecture
- Model-View-Controller (MVC)
- Repository Pattern
- Service Layer Pattern
- Dependency Injection
- Factory Pattern

**TASK:** Generate a refactoring strategy that:
1. Restores architectural compliance
2. Maintains functional behavior
3. Minimizes business logic disruption
4. Improves code organization

**OUTPUT FORMAT:**
{{
  "strategy": {{
    "name": "Refactoring strategy",
    "approach": "Architectural refactoring approach",
    "steps": [
      {{
        "id": "refactor_layer_1",
        "description": "Layer separation step",
        "architectural_changes": ["Implement service layer", "Move database access"],
        "validation": ["Architecture validation", "Functional testing"],
        "estimated_time": 180,
        "risk_level": "HIGH"
      }}
    ],
    "pros": ["Improved maintainability", "Pattern compliance"],
    "cons": ["Refactoring effort", "Testing overhead"],
    "confidence": 0.92,
    "estimated_time": 480,
    "risk_level": "HIGH",
    "requires_approval": true,
    "success_criteria": ["Pattern compliance", "Functionality preserved"],
    "rollback_strategy": "Incremental rollback with partial refactoring"
  }}
}}"""
                ),
                
                "variables": [
                    "pattern_name", "violation_type", "affected_components",
                    "violating_prs", "severity", "layer_violations"
                ]
            },
            
            # Code Generation Templates
            "semantic_merge_code": {
                "template": """You are a senior software engineer with expertise in semantic code merging.

**MERGE CONTEXT:**
- File: {file_path}
- Function/Class: {target_symbol}
- Original Implementation: 
{original_code}

- Version 1 (from PR {pr1_id}):
{pr1_code}

- Version 2 (from PR {pr2_id}):
{pr2_code}

**SEMANTIC ANALYSIS:**
- Business Logic: {business_logic_analysis}
- API Changes: {api_changes}
- Performance Impact: {performance_analysis}
- Test Coverage: {test_coverage}

**TASK:** Generate merged code that:
1. Preserves the business logic of both implementations
2. Combines complementary features
3. Resolves semantic conflicts intelligently
4. Maintains backward compatibility
5. Follows code style guidelines

**OUTPUT FORMAT:**
Return a JSON object with the merged code and analysis:

{{
  "merged_code": "Complete merged implementation",
  "analysis": {{
    "approach": "How the merge was performed",
    "preserved_features": ["Feature 1", "Feature 2"],
    "combined_functionality": ["Combined feature 1"],
    "potential_issues": ["Issue 1"],
    "test_requirements": ["Test case 1"]
  }},
  "confidence": 0.94,
  "requires_review": true,
  "validation_steps": ["Unit tests", "Integration tests", "Performance tests"]
}}""",
                
                "variables": [
                    "file_path", "target_symbol", "original_code", "pr1_code", "pr2_code",
                    "business_logic_analysis", "api_changes", "performance_analysis", "test_coverage"
                ]
            },
            
            # Validation Templates
            "code_quality_validation": {
                "template": """You are a code quality expert. Validate the following resolution for quality issues.

**RESOLUTION TO VALIDATE:**
Strategy: {strategy_name}
Code Changes: {code_changes}
Context: {resolution_context}

**QUALITY CRITERIA:**
1. Code Maintainability
2. Readability and Documentation
3. Performance Impact
4. Security Considerations
5. Testability
6. Error Handling
7. Edge Case Coverage

**VALIDATION OUTPUT:**
{{
  "overall_score": 0.85,
  "quality_metrics": {{
    "maintainability": 0.9,
    "readability": 0.8,
    "performance": 0.85,
    "security": 0.95,
    "testability": 0.75,
    "error_handling": 0.8,
    "edge_cases": 0.7
  }},
  "validation_results": [
    {{
      "category": "maintainability",
      "score": 0.9,
      "findings": ["Good modularization", "Clear function names"],
      "recommendations": ["Consider extracting common logic"]
    }}
  ],
  "critical_issues": ["Issue 1", "Issue 2"],
  "minor_issues": ["Issue 3", "Issue 4"],
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}}""",
                
                "variables": ["strategy_name", "code_changes", "resolution_context"]
            },
            
            # Few-shot Examples
            "successful_merge_example": {
                "template": """Example of a successful merge conflict resolution:

Input:
- File: src/user_service.py
- Conflict: Two PRs added different validation logic to user registration
- PR1: Added email validation with regex
- PR2: Added phone number validation with format checking

AI Analysis: Both PRs add complementary validation. Need to combine validations.

Output:
Strategy: Combine Complementary Validations
- Step 1: Merge validation functions into comprehensive validation
- Step 2: Create unified validation interface
- Step 3: Update test cases to cover both validations

Result: Successfully merged with enhanced validation functionality.""",
                
                "variables": []
            }
        }
    
    def _load_few_shot_examples(self) -> List[FewShotExample]:
        """Load few-shot learning examples"""
        return [
            FewShotExample(
                input={
                    "conflict_type": "MERGE_CONFLICT",
                    "file_path": "src/auth/service.py",
                    "description": "Two PRs modified authentication logic"
                },
                output={
                    "strategy": "Incremental authentication enhancement",
                    "confidence": 0.92,
                    "approach": "Preserve both security enhancements"
                },
                quality_score=0.94,
                success_rate=0.96,
                context={"complexity": "medium", "risk": "low"}
            ),
            FewShotExample(
                input={
                    "conflict_type": "DEPENDENCY_CONFLICT",
                    "description": "Circular dependency between modules A and B"
                },
                output={
                    "strategy": "Dependency inversion with interface abstraction",
                    "confidence": 0.87,
                    "approach": "Break cycle through dependency injection"
                },
                quality_score=0.89,
                success_rate=0.83,
                context={"complexity": "high", "risk": "high"}
            ),
            FewShotExample(
                input={
                    "conflict_type": "ARCHITECTURE_VIOLATION", 
                    "description": "Direct database access from UI layer"
                },
                output={
                    "strategy": "Implement service layer pattern",
                    "confidence": 0.91,
                    "approach": "Add abstraction layer between UI and data"
                },
                quality_score=0.93,
                success_rate=0.95,
                context={"complexity": "medium", "risk": "medium"}
            )
        ]
    
    def generate_strategy_prompt(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: PromptContext
    ) -> str:
        """Generate a strategy generation prompt for the given conflict"""
        
        # Select appropriate template
        if isinstance(conflict_data, MergeConflict):
            template_key = "merge_conflict_strategy"
        elif isinstance(conflict_data, DependencyConflict):
            template_key = "dependency_conflict_strategy"
        elif isinstance(conflict_data, ArchitectureViolation):
            template_key = "architecture_violation_strategy"
        else:
            template_key = "merge_conflict_strategy"  # default
        
        template = self.templates[template_key]["template"]
        
        # Extract variables from conflict data
        variable_values = self._extract_template_variables(conflict_data, context)
        
        # Generate prompt with variables
        try:
            prompt = template.format(**variable_values)
            
            # Add few-shot examples if confidence is low
            if context.confidence < 0.7:
                prompt = self._add_few_shot_examples(prompt, conflict_data, context)
            
            # Add context-specific constraints
            prompt = self._add_constraints(prompt, context)
            
            self.template_stats["template_usage"][template_key] = \
                self.template_stats["template_usage"].get(template_key, 0) + 1
            
            return prompt
            
        except KeyError as e:
            logger.error(
                "Template variable missing",
                template=template_key, variable=str(e)
            )
            return self._generate_fallback_prompt(conflict_data, context)
    
    def generate_code_prompt(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        strategy: Dict[str, Any],
        context: PromptContext
    ) -> str:
        """Generate a code generation prompt"""
        
        template = self.templates["semantic_merge_code"]["template"]
        variables = self._extract_code_variables(conflict_data, strategy, context)
        
        try:
            prompt = template.format(**variables)
            return self._add_code_constraints(prompt, context)
        except KeyError as e:
            logger.error("Code template variable missing", variable=str(e))
            return self._generate_fallback_code_prompt(conflict_data, strategy)
    
    def generate_validation_prompt(
        self, 
        resolution: Dict[str, Any],
        context: PromptContext
    ) -> str:
        """Generate a validation prompt for assessing resolution quality"""
        
        template = self.templates["code_quality_validation"]["template"]
        variables = {
            "strategy_name": resolution.get("name", "Unknown Strategy"),
            "code_changes": json.dumps(resolution.get("code_changes", []), indent=2),
            "resolution_context": json.dumps(context.system_context, indent=2)
        }
        
        try:
            prompt = template.format(**variables)
            return self._add_validation_constraints(prompt, context)
        except Exception as e:
            logger.error("Validation prompt generation failed", error=str(e))
            return self._generate_fallback_validation_prompt(resolution)
    
    def _extract_template_variables(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: PromptContext
    ) -> Dict[str, str]:
        """Extract variables for template formatting"""
        
        if isinstance(conflict_data, MergeConflict):
            return {
                "file_path": conflict_data.file_path,
                "conflict_type": conflict_data.conflict_type,
                "severity": context.severity,
                "pr1_id": conflict_data.pr1_id,
                "pr2_id": conflict_data.pr2_id,
                "content1_preview": (
                    conflict_data.content1[:100] + "..."
                    if len(conflict_data.content1) > 100
                    else conflict_data.content1
                ),
                "content2_preview": (
                    conflict_data.content2[:100] + "..."
                    if len(conflict_data.content2) > 100
                    else conflict_data.content2
                ),
                "base_content_preview": (
                    conflict_data.base_content[:100] + "..."
                    if conflict_data.base_content and len(conflict_data.base_content) > 100
                    else (conflict_data.base_content or "Not available")
                )
            }
        
        elif isinstance(conflict_data, DependencyConflict):
            return {
                "conflict_type": conflict_data.conflict_type,
                "affected_modules": ", ".join(conflict_data.affected_nodes),
                "cycle_path": " -> ".join(conflict_data.cycle_path) if conflict_data.cycle_path else "No cycle",
                "version_conflicts": json.dumps(conflict_data.version_conflicts),
                "severity": context.severity
            }
        
        elif isinstance(conflict_data, ArchitectureViolation):
            return {
                "pattern_name": conflict_data.pattern_name,
                "violation_type": conflict_data.violation_type,
                "affected_components": ", ".join(conflict_data.affected_components),
                "violating_prs": ", ".join(conflict_data.violating_prs),
                "severity": context.severity,
                "layer_violations": json.dumps(conflict_data.layer_violations)
            }
        
        return {"error": "Unknown conflict type"}
    
    def _extract_code_variables(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        strategy: Dict[str, Any],
        context: PromptContext
    ) -> Dict[str, str]:
        """Extract variables for code generation templates"""
        
        base_vars = {
            "file_path": getattr(conflict_data, 'file_path', 'unknown'),
            "target_symbol": "merge_function",  # Default target
            "original_code": "Original implementation",
            "pr1_code": getattr(conflict_data, 'content1', 'Version 1'),
            "pr2_code": getattr(conflict_data, 'content2', 'Version 2'),
            "business_logic_analysis": "Both versions add complementary features",
            "api_changes": "No breaking changes detected",
            "performance_analysis": "Minimal performance impact",
            "test_coverage": "Good test coverage for both versions"
        }
        
        if isinstance(conflict_data, MergeConflict):
            base_vars["pr1_id"] = conflict_data.pr1_id
            base_vars["pr2_id"] = conflict_data.pr2_id
        
        return base_vars
    
    def _add_few_shot_examples(
        self, 
        prompt: str, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: PromptContext
    ) -> str:
        """Add few-shot examples to improve prompt quality"""
        
        # Select relevant examples based on conflict type
        relevant_examples = [
            ex for ex in self.examples 
            if ex.input["conflict_type"] == context.conflict_type.value
        ]
        
        if relevant_examples:
            examples_text = "\\n\\n**FEW-SHOT EXAMPLES:**\\n"
            for i, example in enumerate(relevant_examples[:2]):  # Limit to 2 examples
                examples_text += f"\\nExample {i+1}:\\n{example.input['description']}\\n"
                examples_text += f"Recommended approach: {example.output['approach']}\\n"
                examples_text += f"Expected confidence: {example.quality_score}\\n"
            
            prompt += examples_text
        
        return prompt
    
    def _add_constraints(self, prompt: str, context: PromptContext) -> str:
        """Add context-specific constraints to the prompt"""
        
        constraints_text = "\\n\\n**CONSTRAINTS:**\\n"
        
        # Performance constraints
        if context.performance_requirements.get("max_time", 0) > 0:
            constraints_text += f"- Maximum execution time: {context.performance_requirements['max_time']} seconds\\n"
        
        # Risk constraints
        if context.risk_tolerance == "LOW":
            constraints_text += "- Risk tolerance is LOW: prefer safer, more conservative approaches\\n"
        elif context.risk_tolerance == "HIGH":
            constraints_text += "- Risk tolerance is HIGH: consider more aggressive optimizations\\n"
        
        # Tool constraints
        if context.available_tools:
            constraints_text += f"- Available tools: {', '.join(context.available_tools)}\\n"
        
        # Success criteria
        if context.success_criteria:
            constraints_text += "- Success criteria: " + "; ".join(context.success_criteria) + "\\n"
        
        return prompt + constraints_text
    
    def _add_code_constraints(self, prompt: str, context: PromptContext) -> str:
        """Add code generation specific constraints"""
        
        constraints = [
            "- Follow existing code style and conventions",
            "- Include comprehensive error handling",
            "- Add necessary imports and dependencies",
            "- Ensure backward compatibility where possible",
            "- Include inline comments for complex logic",
            "- Consider edge cases and error conditions"
        ]
        
        return prompt + "\\n\\n**CODE CONSTRAINTS:**\\n" + "\\n".join(constraints)
    
    def _add_validation_constraints(self, prompt: str, context: PromptContext) -> str:
        """Add validation specific constraints"""
        
        constraints = [
            "- Focus on critical quality issues that could cause failures",
            "- Consider both functional and non-functional requirements",
            "- Evaluate test coverage and testability",
            "- Assess security implications",
            "- Consider performance and scalability",
            "- Rate each category on a 0.0-1.0 scale"
        ]
        
        return prompt + "\\n\\n**VALIDATION FOCUS:**\\n" + "\\n".join(constraints)
    
    def _generate_fallback_prompt(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: PromptContext
    ) -> str:
        """Generate a fallback prompt when template formatting fails"""
        
        return f"""Generate a resolution strategy for a {context.conflict_type.value} conflict.

Context: {json.dumps(context.system_context, indent=2)}
Constraints: {', '.join(context.constraints)}
Success criteria: {', '.join(context.success_criteria)}

Please provide a comprehensive strategy with steps, risk assessment, and validation approach."""
    
    def _generate_fallback_code_prompt(
        self, 
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        strategy: Dict[str, Any]
    ) -> str:
        """Generate fallback code generation prompt"""
        
        return f"""Generate code to resolve the conflict based on strategy: {strategy.get('name', 'Unknown')}

Please provide:
1. Complete implementation
2. Analysis of approach
3. Validation requirements
4. Potential issues to watch for"""
    
    def _generate_fallback_validation_prompt(self, resolution: Dict[str, Any]) -> str:
        """Generate fallback validation prompt"""
        
        return """Assess the quality of this resolution:
1. Identify critical issues
2. Provide improvement suggestions
3. Rate overall quality (0.0-1.0)
4. Recommend validation steps"""
    
    def create_iterative_refinement_prompt(
        self, 
        original_prompt: str, 
        feedback: Dict[str, Any],
        iteration: int
    ) -> str:
        """Create prompt for iterative refinement based on feedback"""
        
        refinement_template = f"""{original_prompt}

**FEEDBACK FROM PREVIOUS ITERATION:**
Quality Score: {feedback.get('quality_score', 'N/A')}
Critical Issues: {', '.join(feedback.get('critical_issues', []))}
Suggestions: {', '.join(feedback.get('suggestions', []))}

**REFINEMENT REQUEST (Iteration {iteration}):**
Please refine your approach to address the feedback while maintaining the core strategy.

Focus on:
1. Resolving critical issues
2. Implementing suggested improvements  
3. Increasing overall quality
4. Maintaining original intent

Provide an updated resolution with explanations of changes made."""
        
        return refinement_template
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """Get prompt generation statistics"""
        return {
            **self.template_stats,
            "cache_size": len(self.performance_cache),
            "template_count": len(self.templates),
            "example_count": len(self.examples)
        }