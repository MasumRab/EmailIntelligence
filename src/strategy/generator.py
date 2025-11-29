
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
    RiskLevel
)
from .selector import StrategySelector
from .risk_assessor import RiskAssessor
from ..utils.logger import get_logger

logger = get_logger(__name__)

class StrategyGenerator(IStrategyGenerator):
    """
    Generates resolution strategies for conflicts.
    """
    
    def __init__(self):
        self.selector = StrategySelector()
        self.risk_assessor = RiskAssessor()
        
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
            
        strategies.append(primary_strategy)
        
        # 3. Always offer manual fallback if primary is not manual
        if primary_strategy.type != "manual":
            manual_fallback = self.selector._create_manual_strategy(conflict, "Fallback option")
            manual_fallback.id = f"{manual_fallback.id}-fallback"
            strategies.append(manual_fallback)
            
        return strategies
