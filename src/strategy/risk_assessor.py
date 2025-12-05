"""
Risk assessment module for resolution strategies.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from ..core.conflict_models import Conflict, ConflictBlock, RiskLevel
from ..analysis.code.ast_analyzer import ASTAnalyzer
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RiskAssessor:
    """
    Assesses the risk of conflicts and potential resolutions.
    """

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    async def assess_conflict_risk(
        self, conflict: Conflict, context: Optional[Dict[str, Any]] = None
    ) -> RiskLevel:
        """
        Assess the inherent risk of a conflict.
        """
        risk_score = 0

        # 1. File type risk
        for file_path in conflict.file_paths:
            path_parts = set(Path(file_path).parts)
            if (
                file_path.endswith(".lock")
                or file_path.endswith(".toml")
                or file_path.endswith(".json")
            ):
                risk_score += 2  # Dependency/Config files are risky
            elif path_parts.intersection({"core", "auth"}):
                risk_score += 3  # Core/Auth modules are high risk
            elif path_parts.intersection({"test", "tests"}):
                risk_score += 0  # Tests are generally safe
            else:
                risk_score += 1

        # 2. Complexity risk (lines of conflict)
        # Count total lines involved in conflict (both incoming and current)
        total_lines = sum(
            len(b.incoming_content.splitlines()) + len(b.current_content.splitlines())
            for b in conflict.blocks
        )
        if total_lines > 50:
            risk_score += 3
        elif total_lines > 20:
            risk_score += 2
        elif total_lines > 0:
            risk_score += 1

        # 3. AST-based risk (Breaking changes)
        for block in conflict.blocks:
            if await self._detect_breaking_changes(block):
                risk_score += 5

        return self._score_to_level(risk_score)

    async def _detect_breaking_changes(self, block: ConflictBlock) -> bool:
        """
        Detect if a block contains breaking changes (e.g. function signature changes).
        """
        # Parse both versions
        current_structure = self.ast_analyzer.analyze_structure(block.current_content)
        incoming_structure = self.ast_analyzer.analyze_structure(block.incoming_content)

        # Check if functions were removed or renamed
        current_funcs = set(current_structure.functions)
        incoming_funcs = set(incoming_structure.functions)

        if not current_funcs.issubset(incoming_funcs):
            # Functions removed!
            return True

        # TODO: Check signature changes (arguments) - requires deeper AST analysis

        return False

    def _score_to_level(self, score: int) -> RiskLevel:
        """Convert numeric score to RiskLevel."""
        if score >= 8:
            return RiskLevel.CRITICAL
        elif score >= 5:
            return RiskLevel.HIGH
        elif score >= 3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
