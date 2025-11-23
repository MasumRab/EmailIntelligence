"""
Resolution Strategy Generator with OpenAI Integration

This module provides AI-powered strategy generation for conflict resolution,
combining OpenAI's language capabilities with sophisticated conflict analysis
to generate multiple resolution approaches with confidence scoring.
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional, Union
import structlog
from dataclasses import dataclass

from .types import (
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    SemanticConflict,
    ResourceConflict,
    ResolutionStrategy,
    ResolutionStep,
    RiskLevel,
)
from .prompts import PromptEngine, PromptContext

# ARCHIVED: PR Resolution System - AI client moved to archive
# from ..ai.client import get_openai_client  # Original import commented out - moved to archive/pr-resolution-archive/src/ai/

logger = structlog.get_logger()


@dataclass
class StrategyGenerationContext:
    """Context for strategy generation"""

    system_info: Dict[str, Any]
    project_context: Dict[str, Any]
    development_standards: Dict[str, Any]
    performance_requirements: Dict[str, Any]
    risk_tolerance: str
    available_tools: List[str]
    success_criteria: List[str]
    constraints: List[str]


class StrategyGenerator:
    """
    AI-Powered Resolution Strategy Generator

    Generates intelligent resolution strategies using OpenAI, with:
    - Multiple resolution approaches analysis
    - Pros/cons evaluation
    - Risk assessment
    - Confidence scoring
    - Strategy ranking and recommendations
    """

    def __init__(self):
        self.prompt_engine = PromptEngine()
        self.openai_client = None
        self.strategy_cache = {}
        self.generation_stats = {
            "strategies_generated": 0,
            "successful_generations": 0,
            "average_confidence": 0.0,
            "total_execution_time": 0.0,
            "model_usage": {},
        }

    async def initialize(self) -> bool:
        """Initialize the strategy generator"""
        try:
            # ARCHIVED: OpenAI client moved to archive
            # self.openai_client = await get_openai_client()
            logger.warning("Strategy generator initialized without OpenAI client (archived)")
            return True
        except Exception as e:
            logger.error("Failed to initialize strategy generator", error=str(e))
            return False

    async def generate_strategies(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        context: StrategyGenerationContext,
        max_strategies: int = 3,
        confidence_threshold: float = 0.6,
    ) -> List[ResolutionStrategy]:
        """
        Generate multiple resolution strategies for a conflict

        Args:
            conflict_data: The conflict to resolve
            context: Generation context with project and system information
            max_strategies: Maximum number of strategies to generate
            confidence_threshold: Minimum confidence threshold for strategies

        Returns:
            List of generated resolution strategies
        """

        start_time = time.time()
        strategies = []

        try:
            logger.info(
                "Starting strategy generation",
                conflict_type=type(conflict_data).__name__,
                max_strategies=max_strategies,
            )

            # Create prompt context
            prompt_context = self._create_prompt_context(conflict_data, context)

            # Generate multiple strategies
            strategy_prompts = await self._generate_strategy_prompts(conflict_data, prompt_context, max_strategies)

            # Execute AI generation in parallel
            ai_responses = await self._execute_strategy_generation(strategy_prompts)

            # Parse and validate responses
            for i, response in enumerate(ai_responses):
                try:
                    strategy = await self._parse_strategy_response(response, conflict_data, i + 1)

                    if strategy and strategy.confidence >= confidence_threshold:
                        strategies.append(strategy)
                        logger.info(
                            "Strategy generated successfully",
                            strategy_id=strategy.id,
                            confidence=strategy.confidence,
                            strategy_index=i + 1,
                        )
                    else:
                        logger.info(
                            "Strategy filtered due to low confidence",
                            confidence=strategy.confidence if strategy else 0.0,
                            threshold=confidence_threshold,
                        )

                except Exception as e:
                    logger.error("Failed to parse strategy response", error=str(e), strategy_index=i + 1)

            # Rank strategies
            strategies = self._rank_strategies(strategies)

            # Cache successful strategies
            cache_key = self._generate_cache_key(conflict_data, context)
            self.strategy_cache[cache_key] = strategies

            # Update statistics
            execution_time = time.time() - start_time
            self._update_stats(strategies, execution_time)

            logger.info(
                "Strategy generation completed",
                total_strategies=len(strategies),
                execution_time=execution_time,
                average_confidence=sum(s.confidence for s in strategies) / len(strategies) if strategies else 0.0,
            )

            return strategies

        except Exception as e:
            logger.error("Strategy generation failed", error=str(e))
            return self._generate_fallback_strategies(conflict_data, context)

    async def analyze_strategy_approach(
        self,
        strategy: ResolutionStrategy,
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
        context: StrategyGenerationContext,
    ) -> Dict[str, Any]:
        """
        Analyze a strategy's approach in detail

        Args:
            strategy: Strategy to analyze
            conflict_data: Original conflict data
            context: Generation context

        Returns:
            Detailed analysis of the strategy approach
        """

        analysis_prompt = f"""Analyze this resolution strategy in detail:

**STRATEGY:**
{json.dumps(strategy.dict(), indent=2)}

**CONFLICT CONTEXT:**
{self._format_conflict_context(conflict_data)}

**ANALYSIS REQUIREMENTS:**
1. Evaluate the approach's effectiveness
2. Assess risk factors
3. Identify potential issues
4. Suggest improvements
5. Rate overall viability

Provide a comprehensive analysis in JSON format:
{{
  "approach_score": 0.85,
  "effectiveness": "How well this approach addresses the conflict",
  "risk_factors": ["Risk 1", "Risk 2"],
  "potential_issues": ["Issue 1", "Issue 2"],
  "improvements": ["Improvement 1", "Improvement 2"],
  "viability_rating": "HIGH|MEDIUM|LOW",
  "recommendation": "Final recommendation with reasoning"
}}"""

        try:
            response = await self.openai_client.chat_completion(
                [{"role": "user", "content": analysis_prompt}], max_tokens=800, temperature=0.3
            )

            if response and "choices" in response:
                content = response["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                raise Exception("Invalid AI response")

        except Exception as e:
            logger.error("Strategy analysis failed", error=str(e))
            return self._generate_fallback_analysis(strategy)

    async def generate_approach_comparison(
        self,
        strategies: List[ResolutionStrategy],
        conflict_data: Union[MergeConflict, DependencyConflict, ArchitectureViolation],
    ) -> Dict[str, Any]:
        """
        Generate a comparison of different resolution approaches

        Args:
            strategies: List of strategies to compare
            conflict_data: Original conflict data

        Returns:
            Detailed comparison analysis
        """

        comparison_prompt = f"""Compare these resolution strategies:

**CONFLICT:** {type(conflict_data).__name__}
{self._format_conflict_context(conflict_data)}

**STRATEGIES TO COMPARE:**
{json.dumps([s.dict() for s in strategies], indent=2)}

**COMPARISON CRITERIA:**
1. Overall effectiveness
2. Risk assessment
3. Implementation complexity
4. Time to resolution
5. Resource requirements
6. Maintainability impact

Provide comparison in JSON format:
{{
  "recommended_strategy": "strategy_id",
  "comparison_matrix": [
    {{
      "strategy_id": "strategy_1",
      "effectiveness": 0.9,
      "risk_level": "LOW",
      "complexity": "MEDIUM",
      "time_estimate": 300,
      "pros": ["Pro 1"],
      "cons": ["Con 1"]
    }}
  ],
  "decision_factors": {
    "primary_factor": "Factor that drove the recommendation",
    "trade_offs": ["Trade-off 1", "Trade-off 2"],
    "special_considerations": ["Consideration 1"]
    }
}}"""

        try:
            response = await self.openai_client.chat_completion(
                [{"role": "user", "content": comparison_prompt}], max_tokens=1000, temperature=0.2
            )

            if response and "choices" in response:
                content = response["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                raise Exception("Invalid AI response")

        except Exception as e:
            logger.error("Strategy comparison failed", error=str(e))
            return self._generate_fallback_comparison(strategies)

    def _create_prompt_context(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        generation_context: StrategyGenerationContext,
    ) -> PromptContext:
        """Create prompt context from generation context"""

        # Determine conflict severity
        if hasattr(conflict_data, "severity"):
            severity = conflict_data.severity.value
        else:
            severity = "MEDIUM"  # default

        # Extract affected files
        affected_files = []
        if hasattr(conflict_data, "file_path"):
            affected_files = [conflict_data.file_path]
        elif hasattr(conflict_data, "affected_components"):
            affected_files = conflict_data.affected_components
        elif hasattr(conflict_data, "affected_nodes"):
            affected_files = conflict_data.affected_nodes
        else:
            affected_files = ["unknown"]

        return PromptContext(
            conflict_type=type(conflict_data).__name__,
            severity=severity,
            confidence=0.8,  # Default confidence
            affected_files=affected_files,
            system_context=generation_context.system_info,
            constraints=generation_context.constraints,
            success_criteria=generation_context.success_criteria,
            risk_tolerance=generation_context.risk_tolerance,
            available_tools=generation_context.available_tools,
            performance_requirements=generation_context.performance_requirements,
        )

    async def _generate_strategy_prompts(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        prompt_context: PromptContext,
        max_strategies: int,
    ) -> List[str]:
        """Generate prompts for multiple strategy approaches"""

        prompts = []

        # Generate different approaches
        approaches = ["conservative", "aggressive", "innovative", "hybrid", "minimal"]

        for i in range(max_strategies):
            approach = approaches[i % len(approaches)]

            # Generate base prompt
            base_prompt = self.prompt_engine.generate_strategy_prompt(conflict_data, prompt_context)

            # Add approach-specific instructions
            approach_instruction = self._get_approach_instruction(approach)
            enhanced_prompt = f"{base_prompt}\n\n**APPROACH FOCUS:** {approach_instruction}"

            prompts.append(enhanced_prompt)

        return prompts

    def _get_approach_instruction(self, approach: str) -> str:
        """Get approach-specific instructions for strategy generation"""

        instructions = {
            "conservative": (
                "Focus on minimal changes and proven patterns. " "Prioritize safety and reliability over innovation."
            ),
            "aggressive": (
                "Consider comprehensive refactoring and architectural improvements. "
                "Optimize for long-term maintainability."
            ),
            "innovative": "Explore novel solutions and emerging patterns. Consider cutting-edge approaches and technologies.",
            "hybrid": "Combine multiple approaches strategically. Balance risk and benefit across different aspects.",
            "minimal": "Focus on the simplest possible solution that resolves the immediate conflict with minimal disruption.",
        }

        return instructions.get(approach, "Generate a balanced approach that considers multiple factors.")

    async def _execute_strategy_generation(self, prompts: List[str]) -> List[str]:
        """Execute strategy generation using OpenAI"""

        try:
            # Execute in parallel with rate limiting
            tasks = [
                self.openai_client.chat_completion(
                    [{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.7
                )
                for prompt in prompts
            ]

            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # Extract content from responses
            results = []
            for response in responses:
                if isinstance(response, dict) and "choices" in response:
                    content = response["choices"][0]["message"]["content"]
                    results.append(content)
                else:
                    logger.error("Invalid AI response", response=response)
                    results.append("")

            return results

        except Exception as e:
            logger.error("Strategy generation execution failed", error=str(e))
            return [""] * len(prompts)

    async def _parse_strategy_response(
        self,
        response_content: str,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        strategy_index: int,
    ) -> Optional[ResolutionStrategy]:
        """Parse AI response into ResolutionStrategy object"""

        try:
            # Extract JSON from response
            json_start = response_content.find("{")
            json_end = response_content.rfind("}") + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = response_content[json_start:json_end]
            response_data = json.loads(json_str)

            # Extract strategy data
            strategy_data = response_data.get("strategy", response_data)

            # Create ResolutionStrategy object
            strategy = ResolutionStrategy(
                id=f"strategy_{strategy_index}_{int(time.time())}",
                name=strategy_data.get("name", f"Strategy {strategy_index}"),
                description=strategy_data.get("description", ""),
                approach=strategy_data.get("approach", ""),
                steps=self._parse_strategy_steps(strategy_data.get("steps", [])),
                pros=strategy_data.get("pros", []),
                cons=strategy_data.get("cons", []),
                confidence=float(strategy_data.get("confidence", 0.0)),
                estimated_time=int(strategy_data.get("estimated_time", 0)),
                risk_level=RiskLevel(strategy_data.get("risk_level", "MEDIUM")),
                requires_approval=bool(strategy_data.get("requires_approval", False)),
                success_criteria=strategy_data.get("success_criteria", []),
                rollback_strategy=strategy_data.get("rollback_strategy"),
                validation_approach=strategy_data.get("validation_approach", ""),
                ai_generated=True,
                model_used="gpt-4o",
                prompt_context={"conflict_type": type(conflict_data).__name__},
            )

            return strategy

        except Exception as e:
            logger.error("Failed to parse strategy response", error=str(e))
            return None

    def _parse_strategy_steps(self, steps_data: List[Dict[str, Any]]) -> List[ResolutionStep]:
        """Parse strategy steps from AI response"""

        steps = []

        for i, step_data in enumerate(steps_data):
            try:
                step = ResolutionStep(
                    id=step_data.get("id", f"step_{i+1}"),
                    description=step_data.get("description", ""),
                    code_changes=[],  # Will be populated during code generation
                    validation_steps=step_data.get("validation", []),
                    estimated_time=int(step_data.get("estimated_time", 60)),
                    risk_level=RiskLevel(step_data.get("risk_level", "MEDIUM")),
                    can_rollback=bool(step_data.get("can_rollback", True)),
                    dependencies=step_data.get("dependencies", []),
                )
                steps.append(step)
            except Exception as e:
                logger.error("Failed to parse step", error=str(e))
                continue

        return steps

    def _rank_strategies(self, strategies: List[ResolutionStrategy]) -> List[ResolutionStrategy]:
        """Rank strategies by quality score"""

        def calculate_quality_score(strategy: ResolutionStrategy) -> float:
            """Calculate quality score for ranking"""

            # Base score from confidence
            confidence_score = strategy.confidence * 0.4

            # Risk factor (lower risk = higher score)
            risk_scores = {
                RiskLevel.VERY_LOW: 1.0,
                RiskLevel.LOW: 0.8,
                RiskLevel.MEDIUM: 0.6,
                RiskLevel.HIGH: 0.4,
                RiskLevel.VERY_HIGH: 0.2,
                RiskLevel.CRITICAL: 0.1,
            }
            risk_score = risk_scores.get(strategy.risk_level, 0.5) * 0.3

            # Time factor (faster = higher score, but not too fast)
            time_score = min(1.0, max(0.0, 1.0 - (strategy.estimated_time / 3600))) * 0.2

            # Completeness factor
            completeness = (
                len(strategy.steps) / 10.0
                + len(strategy.pros) / 5.0  # More steps = more thorough
                + len(strategy.success_criteria) / 5.0  # More pros = better analysis  # More criteria = better planning
            ) / 3.0
            completeness_score = min(1.0, completeness) * 0.1

            return confidence_score + risk_score + time_score + completeness_score

        # Sort by quality score
        strategies.sort(key=calculate_quality_score, reverse=True)

        return strategies

    def _generate_cache_key(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        context: StrategyGenerationContext,
    ) -> str:
        """Generate cache key for strategies"""

        import hashlib

        key_data = {
            "conflict_type": type(conflict_data).__name__,
            "severity": getattr(conflict_data, "severity", "MEDIUM"),
            "file_path": getattr(conflict_data, "file_path", ""),
            "risk_tolerance": context.risk_tolerance,
            "constraints": sorted(context.constraints),
            "success_criteria": sorted(context.success_criteria),
        }

        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _update_stats(self, strategies: List[ResolutionStrategy], execution_time: float):
        """Update generation statistics"""

        self.generation_stats["strategies_generated"] += len(strategies)
        self.generation_stats["successful_generations"] += 1
        self.generation_stats["total_execution_time"] += execution_time

        if strategies:
            avg_confidence = sum(s.confidence for s in strategies) / len(strategies)
            self.generation_stats["average_confidence"] = (
                self.generation_stats["average_confidence"] * (self.generation_stats["successful_generations"] - 1)
                + avg_confidence
            ) / self.generation_stats["successful_generations"]

    def _format_conflict_context(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
    ) -> str:
        """Format conflict data for prompts"""

        if isinstance(conflict_data, MergeConflict):
            return (
                f"File: {conflict_data.file_path}\\n"
                f"PR1: {conflict_data.pr1_id}\\n"
                f"PR2: {conflict_data.pr2_id}\\n"
                f"Similarity: {conflict_data.similarity_score}"
            )
        elif isinstance(conflict_data, DependencyConflict):
            return f"Type: {conflict_data.conflict_type}\\nModules: {', '.join(conflict_data.affected_nodes)}"
        elif isinstance(conflict_data, ArchitectureViolation):
            return f"Pattern: {conflict_data.pattern_name}\\nViolation: {conflict_data.violation_type}"
        else:
            return f"Type: {type(conflict_data).__name__}"

    def _generate_fallback_strategies(
        self,
        conflict_data: Union[
            MergeConflict, DependencyConflict, ArchitectureViolation, SemanticConflict, ResourceConflict
        ],
        context: StrategyGenerationContext,
    ) -> List[ResolutionStrategy]:
        """Generate fallback strategies when AI fails"""

        fallback_strategy = ResolutionStrategy(
            id=f"fallback_{int(time.time())}",
            name="Manual Resolution Required",
            description="AI-generated strategies failed. Manual intervention required.",
            approach="Manual analysis and resolution by experienced developer",
            steps=[
                ResolutionStep(
                    id="manual_analysis",
                    description="Manual analysis of the conflict",
                    validation_steps=["Code review", "Testing"],
                    estimated_time=300,
                    risk_level=RiskLevel.MEDIUM,
                    can_rollback=True,
                )
            ],
            pros=["Human expertise", "Custom solution"],
            cons=["Time consuming", "Subjective"],
            confidence=0.3,
            estimated_time=600,
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            success_criteria=["Conflict resolved", "Tests pass"],
            rollback_strategy="Git operations",
            validation_approach="Manual testing and review",
            ai_generated=False,
            model_used="fallback",
        )

        return [fallback_strategy]

    def _generate_fallback_analysis(self, strategy: ResolutionStrategy) -> Dict[str, Any]:
        """Generate fallback analysis when AI analysis fails"""

        return {
            "approach_score": strategy.confidence,
            "effectiveness": "Strategy appears viable based on confidence score",
            "risk_factors": ["Unknown - requires manual review"],
            "potential_issues": ["Implementation details need clarification"],
            "improvements": ["Add more specific validation steps"],
            "viability_rating": "MEDIUM" if strategy.confidence > 0.5 else "LOW",
            "recommendation": f"Review strategy with confidence score of {strategy.confidence}",
        }

    def _generate_fallback_comparison(self, strategies: List[ResolutionStrategy]) -> Dict[str, Any]:
        """Generate fallback comparison when AI comparison fails"""

        best_strategy = max(strategies, key=lambda s: s.confidence) if strategies else None

        return {
            "recommended_strategy": best_strategy.id if best_strategy else None,
            "decision_factors": {
                "primary_factor": "Confidence score (fallback comparison)",
                "trade_offs": ["Multiple approaches not fully evaluated"],
                "special_considerations": ["AI comparison failed, manual review recommended"],
            },
        }

    def get_generation_stats(self) -> Dict[str, Any]:
        """Get strategy generation statistics"""

        return {
            **self.generation_stats,
            "cache_size": len(self.strategy_cache),
            "cached_strategies": len([s for strategies in self.strategy_cache.values() for s in strategies]),
        }
