"""
Semantic merger module.
"""

from typing import Optional
from ..core.models import ConflictBlock
from ..analysis.code.ast_analyzer import ASTAnalyzer
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SemanticMerger:
    """
    Handles semantic merging of code (AST-aware).
    """

    def __init__(self):
        self.analyzer = ASTAnalyzer()

    async def merge_blocks(self, block: ConflictBlock) -> Optional[str]:
        """
        Attempt to semantically merge a conflict block.
        Returns the merged content if successful, None otherwise.
        """
        # 1. Check for false conflicts (semantic equivalence)
        # If incoming (theirs) is semantically equivalent to current (ours),
        # keep ours (no change needed)
        # But wait, if they are equivalent, git might have flagged it because of whitespace.
        # If we return 'ours', we are effectively resolving it.

        # We need the base content to know who changed what.

        if not block.base_content:
            # If no base, it's an add/add conflict.
            if self.analyzer.are_equivalent(block.current_content, block.incoming_content):
                logger.info("Resolved add/add conflict via semantic equivalence")
                return block.current_content
            return None

        # 2. Check if one side is semantically equivalent to base (no semantic change)

        # Check if 'ours' is semantically unchanged
        ours_unchanged = self.analyzer.are_equivalent(block.current_content, block.base_content)

        # Check if 'theirs' is semantically unchanged
        theirs_unchanged = self.analyzer.are_equivalent(block.incoming_content, block.base_content)

        if ours_unchanged and theirs_unchanged:
            # Both semantically unchanged (maybe just formatting).
            # Prefer incoming (theirs) assuming it might be a style fix.
            logger.info("Resolved conflict: both sides semantically unchanged")
            return block.incoming_content

        if ours_unchanged:
            # We didn't change semantically, they did. Accept theirs.
            logger.info("Resolved conflict: local is semantically unchanged")
            return block.incoming_content

        if theirs_unchanged:
            # They didn't change semantically, we did. Keep ours.
            logger.info("Resolved conflict: remote is semantically unchanged")
            return block.current_content

        # 3. Both changed semantically.
        # Check if they are equivalent to EACH OTHER (e.g. both made same refactor)
        if self.analyzer.are_equivalent(block.current_content, block.incoming_content):
            logger.info("Resolved conflict: both sides semantically equivalent")
            return block.current_content

        return None
