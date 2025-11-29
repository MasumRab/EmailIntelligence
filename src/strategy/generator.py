
"""
Strategy generation module.
"""

from typing import List, Dict, Any, Optional

from ..core.interfaces import IStrategyGenerator
from ..core.models import (
    Conflict, 
    AnalysisResult, 
    ResolutionStrategy, 
    ResolutionStep,
    RiskLevel
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
        context: Dict[str, Any] = None
    ) -> List[ResolutionStrategy]:
        """
        Generate potential resolution strategies.
        """
        logger.info("Generating strategies", conflict_id=conflict.id)
        
        strategies = []
        
        # 1. Select primary strategy
        primary_strategy = self.selector.select_strategy(conflict, analysis, context)
        
        # 2. Populate steps for the strategy
        if primary_strategy.type == "manual":
            primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Open conflict resolution tool",
                    action="open_tool",
                    params={"file": conflict.file_paths[0]}
                ),
                ResolutionStep(
                    order=2,
                    description="Manually resolve conflicts",
                    action="manual_edit",
                    params={}
                )
            ]
        elif primary_strategy.type == "accept_incoming":
            primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Checkout file from incoming branch",
                    action="git_checkout",
                    params={"source": "incoming", "file": conflict.file_paths[0]}
                ),
                ResolutionStep(
                    order=2,
                    description="Stage changes",
                    action="git_add",
                    params={"file": conflict.file_paths[0]}
                )
            ]
        elif primary_strategy.type == "union":
             primary_strategy.steps = [
                ResolutionStep(
                    order=1,
                    description="Read both versions",
                    action="read_content",
                    params={}
                ),
                ResolutionStep(
                    order=2,
                    description="Merge unique lines",
                    action="merge_union",
                    params={}
                ),
                ResolutionStep(
                    order=3,
                    description="Write merged content",
                    action="write_file",
                    params={"file": conflict.file_paths[0]}
                )
            ]
        
        # 3. Enhance with AI Prompt if applicable
        if primary_strategy.type == "manual" and analysis.risk_level != RiskLevel.CRITICAL:
            # If it's manual but not critical, maybe AI can help?
            # Let's generate a prompt for the user/AI agent to use
            try:
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
                    performance_requirements={}
                )
                
                # We need to adapt the conflict object to what PromptEngine expects
                # For now, we'll pass the raw conflict object and let PromptEngine handle it
                # (Assuming PromptEngine has been updated or we wrap it)
                # Since PromptEngine expects specific types, we might need a wrapper or update it.
                # For this step, we'll just log that we would generate a prompt.
                # prompt = self.prompt_engine.generate_strategy_prompt(conflict, prompt_context)
                # primary_strategy.ai_prompt = prompt
                pass
            except Exception as e:
                logger.warning("Failed to generate AI prompt", error=str(e))

        strategies.append(primary_strategy)
        
        # 4. Always offer manual fallback if primary is not manual
        if primary_strategy.type != "manual":
            manual_fallback = self.selector._create_manual_strategy(conflict, "Fallback option")
            manual_fallback.id = f"{manual_fallback.id}-fallback"
            strategies.append(manual_fallback)
            
        return strategies
