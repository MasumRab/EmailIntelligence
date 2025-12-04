"""
Strategy generation module.
"""

from typing import List, Dict, Any

from ..core.interfaces import IStrategyGenerator
from ..core.models import (
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
        if primary_strategy.type == "automated":
            # This strategy relies on SemanticMerger
            # We assume the conflict has blocks that can be merged
            if conflict.blocks:
                steps = []
                for i, block in enumerate(conflict.blocks):
                    steps.append(
                        ResolutionStep(
                            order=i * 2 + 1,
                            description=f"Semantically merge block {i + 1}",
                            action="semantic_merge",
                            params={"block": block.dict()},
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
                            order=i * 2 + 2,
                            description=f"Apply merged content to {block.file_path}",
                            action="apply_merge",
                            params={"file": block.file_path, "block": block.dict()},
                        )
                    )

                primary_strategy.steps = steps
            else:
                # Fallback if no blocks
                logger.warning("Automated strategy selected but no blocks found")
                primary_strategy.type = "manual"

        if primary_strategy.type == "manual":
            primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Open conflict resolution tool",
                    action="open_tool",
                    params={"file": conflict.file_paths[0]},
                ),
                ResolutionStep(
                    order=2,
                    description="Manually resolve conflicts",
                    action="manual_edit",
                    params={},
                ),
            ]
        elif primary_strategy.type == "accept_incoming":
            primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Checkout file from incoming branch",
                    action="git_checkout",
                    params={"source": "incoming", "file": conflict.file_paths[0]},
                ),
                ResolutionStep(
                    order=2,
                    description="Stage changes",
                    action="git_add",
                    params={"file": conflict.file_paths[0]},
                ),
            ]
        elif primary_strategy.type == "union":
            primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Read both versions",
                    action="read_content",
                    params={},
                ),
                ResolutionStep(
                    order=2,
                    description="Merge unique lines",
                    action="merge_union",
                    params={},
                ),
                ResolutionStep(
                    order=3,
                    description="Write merged content",
                    action="write_file",
                    params={"file": conflict.file_paths[0]},
                ),
            ]

        strategies.append(primary_strategy)

        # 3. Enhance with AI Prompt if applicable
        if primary_strategy.type == "manual" and analysis.risk_level != RiskLevel.CRITICAL:
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

                    # Store generated prompt in strategy context
                    if not primary_strategy.prompt_context:
                        primary_strategy.prompt_context = {}
                    primary_strategy.prompt_context["generated_prompt"] = prompt
                    logger.info("Generated AI strategy prompt", conflict_id=conflict.id)
                else:
                    logger.warning("No blocks available for AI prompt generation")

            except Exception as e:
                logger.warning("Failed to generate AI prompt", error=str(e))

        # 4. Always offer manual fallback if primary is not manual
        if primary_strategy.type != "manual":
            manual_fallback = self.selector._create_manual_strategy(conflict, "Fallback option")
            manual_fallback.id = f"{manual_fallback.id}-fallback"
            strategies.append(manual_fallback)

        return strategies
