"""
Strategy generation module.
"""

from typing import List, Dict, Any
import json
import asyncio

from ..core.config import settings
from ..ai.gemini_client import GeminiClient

from ..core.interfaces import IStrategyGenerator
from ..core.conflict_models import (
    Conflict,
    AnalysisResult,
    ResolutionStrategy,
    ResolutionStep,
    RiskLevel,
    MergeConflict,
)
from .selector import StrategySelector
from .risk_assessor import RiskAssessor
from ..resolution.prompts import PromptEngine, PromptContext

from ..utils.logger import get_logger

logger = get_logger(__name__)


class StrategyGenerator(IStrategyGenerator):
    """
    Generates resolution strategies for conflicts.
    """

    def __init__(self):
        self.selector = StrategySelector()
        self.risk_assessor = RiskAssessor()
        self.prompt_engine = PromptEngine()
        self.ai_client = GeminiClient() if settings.use_ai_strategies else None

    async def generate_strategies(
        self,
        conflict: Conflict,
        analysis: AnalysisResult,
        context: Dict[str, Any] = None,
    ) -> List[ResolutionStrategy]:
        """
        Generate potential resolution strategies.
        """
        logger.info("Generating strategies", conflict_id=conflict.id)

        strategies = []

        # 1. Select primary strategy
        primary_strategy = self.selector.select_strategy(conflict, analysis, context)

        # 2. Populate steps for the strategy
        if primary_strategy.name == "Automated Semantic Merge":
            # This strategy relies on SemanticMerger
            # We assume the conflict has blocks that can be merged
            if conflict.blocks:
                steps = []
                for i, block in enumerate(conflict.blocks):
                    steps.append(
                        ResolutionStep(
                            id=f"semantic_merge_{i+1}",
                            description=f"Semantically merge block {i + 1}",
                            risk_level=RiskLevel.MEDIUM,
                            estimated_time=30,
                            validation_steps=["verify_syntax", "check_semantics"],
                        )
                    )
                    # In a real scenario, we'd need to handle multiple blocks and combine them.
                    # For now, we assume single block or sequential processing that updates the
                    # file content.
                    # The executor's write_file logic needs to be robust enough to handle full
                    # file writes.
                    # Here we assume the semantic merger returns the FULL merged content for the
                    # file
                    # OR we need a step to combine blocks.
                    # Simplified: We assume 1 block = 1 file content for this MVP.

                    steps.append(
                        ResolutionStep(
                            id=f"apply_merge_{i+1}",
                            description=f"Apply merged content to {block.file_path}",
                            risk_level=RiskLevel.LOW,
                            estimated_time=10,
                            validation_steps=["verify_file_write"],
                        )
                    )

                primary_strategy.steps = steps
            else:
                # Fallback if no blocks
                logger.warning("Automated strategy selected but no blocks found")
                # Fallback - strategy already created as manual if needed

        if primary_strategy.name == "Manual Resolution":
            primary_strategy.steps = [
                ResolutionStep(
                    id="manual_open_tool",
                    description="Open conflict resolution tool",
                    risk_level=RiskLevel.LOW,
                    estimated_time=5,
                    validation_steps=[],
                ),
                ResolutionStep(
                    id="manual_resolve",
                    description="Manually resolve conflicts",
                    risk_level=RiskLevel.HIGH,
                    estimated_time=300,
                    validation_steps=["verify_resolution", "run_tests"],
                ),
            ]
        elif primary_strategy.name == "Accept Incoming":
            primary_strategy.steps = [
                ResolutionStep(
                    id="checkout_incoming",
                    description="Checkout file from incoming branch",
                    risk_level=RiskLevel.LOW,
                    estimated_time=5,
                    validation_steps=["verify_checkout"],
                ),
                ResolutionStep(
                    id="stage_changes",
                    description="Stage changes",
                    risk_level=RiskLevel.LOW,
                    estimated_time=2,
                    validation_steps=["verify_staged"],
                ),
            ]
        elif primary_strategy.name == "Union Merge":
            primary_strategy.steps = [
                ResolutionStep(
                    id="read_versions",
                    description="Read both versions",
                    risk_level=RiskLevel.LOW,
                    estimated_time=2,
                    validation_steps=[],
                ),
                ResolutionStep(
                    id="merge_union",
                    description="Merge unique lines",
                    risk_level=RiskLevel.MEDIUM,
                    estimated_time=10,
                    validation_steps=["verify_merge"],
                ),
                ResolutionStep(
                    id="write_merged",
                    description="Write merged content",
                    risk_level=RiskLevel.LOW,
                    estimated_time=5,
                    validation_steps=["verify_file_write", "run_linting"],
                ),
            ]

        strategies.append(primary_strategy)

        # 3. Enhance with AI Prompt if applicable
        if primary_strategy.name == "Manual Resolution" and analysis.risk_level != RiskLevel.CRITICAL:
            try:
                # Create prompt context
                prompt_context = PromptContext(
                    conflict_type=conflict.type,
                    severity=conflict.severity.value,
                    confidence=analysis.confidence_score,
                    affected_files=conflict.file_paths,
                    system_context=context or {},
                    constraints=[],
                    success_criteria=[],
                    risk_tolerance="MEDIUM",
                    available_tools=["git", "ast_analyzer"],
                    performance_requirements={},
                )

                # Convert generic Conflict to MergeConflict for PromptEngine
                if conflict.blocks:
                    block = conflict.blocks[0]
                    # Create MergeConflict object required by PromptEngine
                    merge_conflict = MergeConflict(
                        pr1_id=conflict.pr_id or "unknown",
                        pr2_id="current",
                        file_path=block.file_path,
                        conflict_region=(
                            f"<<<<<<< HEAD\n{block.current_content}\n=======\n"
                            f"{block.incoming_content}\n>>>>>>> incoming"
                        ),
                        base_content=block.base_content,
                        content1=block.current_content,
                        content2=block.incoming_content,
                        similarity_score=0.5,  # Placeholder
                        conflict_type=conflict.type.value,
                        line_numbers={
                            "current": [block.start_line, block.end_line],
                            "incoming": [block.start_line, block.end_line],
                        },
                    )

                    prompt = self.prompt_engine.generate_strategy_prompt(
                        merge_conflict, prompt_context
                    )

                    # Execute AI strategy generation if enabled
                    if settings.use_ai_strategies and self.ai_client:
                        logger.info("Executing AI strategy generation", conflict_id=conflict.id)
                        ai_response = await self.ai_client.generate_content(prompt)
                        
                        if ai_response:
                            try:
                                # Clean up markdown code blocks if present
                                clean_response = ai_response.replace("```json", "").replace("```", "").strip()
                                strategy_data = json.loads(clean_response)
                                
                                if "strategy" in strategy_data:
                                    s_data = strategy_data["strategy"]
                                    
                                    # Convert steps to ResolutionStep objects
                                    ai_steps = []
                                    for i, step_data in enumerate(s_data.get("steps", [])):
                                        ai_steps.append(ResolutionStep(
                                            id=step_data.get("id", f"ai_step_{i}"),
                                            description=step_data.get("description", ""),
                                            risk_level=RiskLevel(step_data.get("risk_level", "MEDIUM")),
                                            estimated_time=step_data.get("estimated_time", 0),
                                            validation_steps=step_data.get("validation", [])
                                        ))

                                    ai_strategy = ResolutionStrategy(
                                        id=f"ai_gen_{conflict.id}",
                                        name=s_data.get("name", "AI Generated Strategy"),
                                        description=s_data.get("approach", "AI generated resolution"),
                                        approach=s_data.get("approach", ""),
                                        steps=ai_steps,
                                        pros=s_data.get("pros", []),
                                        cons=s_data.get("cons", []),
                                        confidence=s_data.get("confidence", 0.8),
                                        estimated_time=s_data.get("estimated_time", 300),
                                        risk_level=RiskLevel(s_data.get("risk_level", "MEDIUM")),
                                        requires_approval=s_data.get("requires_approval", True),
                                        success_criteria=s_data.get("success_criteria", []),
                                        rollback_strategy=s_data.get("rollback_strategy", ""),
                                        validation_approach=s_data.get("validation_approach", ""),
                                        ai_generated=True,
                                        model_used=settings.gemini_model
                                    )
                                    
                                    strategies.append(ai_strategy)
                                    logger.info("Successfully generated AI strategy", strategy_name=ai_strategy.name)
                            except json.JSONDecodeError:
                                logger.error("Failed to parse AI response as JSON", response=ai_response[:100])
                            except Exception as e:
                                logger.error("Error creating AI strategy object", error=str(e))

                    # Store generated prompt in strategy context (fallback or reference)
                    if not primary_strategy.prompt_context:
                        primary_strategy.prompt_context = {}
                    primary_strategy.prompt_context["generated_prompt"] = prompt
                    
                else:
                    logger.warning("No blocks available for AI prompt generation")

            except Exception as e:
                logger.warning("Failed to generate AI prompt/strategy", error=str(e))

        # 4. Always offer manual fallback if primary is not manual
        if primary_strategy.name != "Manual Resolution":
            manual_fallback = self.selector._create_manual_strategy(conflict, "Fallback option")
            manual_fallback.id = f"{manual_fallback.id}-fallback"
            strategies.append(manual_fallback)

        return strategies
