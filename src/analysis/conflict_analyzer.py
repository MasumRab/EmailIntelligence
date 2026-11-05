import ast
import difflib
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

from ..core.conflict_models import Conflict, ConflictBlock

logger = logging.getLogger(__name__)


class ConflictAnalyzer:
    """
    Analyzes conflicts to calculate alignment scores and other metrics.
    """

    def __init__(self):
        self.weights = {
            "complexity": 0.3,
            "overlap": 0.2,
            "semantic": 0.3,
            "feasibility": 0.2,
        }

    def calculate_alignment_score(self, conflict: Conflict) -> float:
        """
        Calculate the alignment score (0.0 - 1.0) for a conflict.

        The score is a weighted combination of:
        - Complexity (inverse): Lower complexity -> Higher score
        - Code Overlap: Higher overlap -> Higher score (indicates similar intent?)
          *Wait, usually high overlap in changes means more conflict.
          The user said: "code_overlap_score (ratio of overlapping changed lines / total changed lines)"
          and "overlap and semantic positive".
          If lines are identical in both branches, git usually handles it.
          If they are different but similar, it might be easier to merge.
          Let's interpret "overlap" as similarity between the conflicting blocks.*
        - Semantic Compatibility: Higher compatibility -> Higher score
        - Merge Feasibility: Higher feasibility -> Higher score
        """

        metrics = self.analyze_conflict_metrics(conflict)

        # Normalize complexity to 0-1 (inverse: 0 complexity = 1.0 score)
        # Assuming max complexity is around 100 lines/hunks for normalization
        complexity_score = max(0.0, 1.0 - (metrics["complexity"] / 100.0))

        overlap_score = metrics["overlap"]
        semantic_score = metrics["semantic"]
        feasibility_score = metrics["feasibility"]

        raw_score = (
            complexity_score * self.weights["complexity"]
            + overlap_score * self.weights["overlap"]
            + semantic_score * self.weights["semantic"]
            + feasibility_score * self.weights["feasibility"]
        )

        final_score = max(0.0, min(1.0, raw_score))

        logger.info(
            "Calculated alignment score",
            extra={"conflict_id": conflict.id, "metrics": metrics, "final_score": final_score},
        )

        return final_score

    def analyze_conflict_metrics(self, conflict: Conflict) -> Dict[str, float]:
        """
        Gather numeric metrics for conflict analysis.
        """
        return {
            "complexity": self._calculate_complexity(conflict),
            "overlap": self._calculate_overlap(conflict),
            "semantic": self._calculate_semantic_compatibility(conflict),
            "feasibility": self._calculate_merge_feasibility(conflict),
        }

    def _calculate_overlap(self, conflict: Conflict) -> float:
        """
        Calculate overlap score based on similarity between current and incoming content.
        """
        if not conflict.blocks:
            return 1.0

        total_score = 0.0
        for block in conflict.blocks:
            matcher = difflib.SequenceMatcher(None, block.current_content, block.incoming_content)
            total_score += matcher.ratio()

        return total_score / len(conflict.blocks)

    def _check_structural_integrity(self, content: str) -> bool:
        """
        Check if code block has balanced delimiters.
        """
        delimiters = {"(": ")", "[": "]", "{": "}"}
        stack = []

        for char in content:
            if char in delimiters:
                stack.append(char)
            elif char in delimiters.values():
                if not stack:
                    return False
                if delimiters[stack.pop()] != char:
                    return False

        return len(stack) == 0

    def _is_valid_python(self, content: str) -> bool:
        """
        Check if content is valid Python code.
        """
        try:
            ast.parse(content)
            return True
        except SyntaxError:
            return False

    def _calculate_complexity(self, conflict: Conflict) -> float:
        """
        Calculate complexity based on number of hunks, lines, and fragmentation.
        Returns a raw number (not necessarily 0-1).
        """
        if not conflict.blocks:
            return 0.0

        num_hunks = len(conflict.blocks)
        total_lines = 0
        for block in conflict.blocks:
            current_lines = len(block.current_content.splitlines())
            incoming_lines = len(block.incoming_content.splitlines())
            total_lines += current_lines + incoming_lines

        # Calculate fragmentation (hunk density)
        # If we have many hunks but few lines, it's fragmented and messy.
        avg_lines_per_hunk = total_lines / num_hunks if num_hunks > 0 else 0
        fragmentation_penalty = 0
        if num_hunks > 1 and avg_lines_per_hunk < 3:
            fragmentation_penalty = num_hunks * 5

        # Heuristic: 1 hunk = 10 points, 1 line = 1 point
        return (num_hunks * 10) + total_lines + fragmentation_penalty

    def _calculate_semantic_compatibility(self, conflict: Conflict) -> float:
        """
        Calculate semantic compatibility (0.0 - 1.0).
        Checks if both versions are valid code (AST parseable) and structurally sound.
        """
        if not conflict.blocks:
            return 1.0  # No conflict blocks, assume compatible

        # Check file extension to decide if we can use AST
        is_python = any(path.endswith(".py") for path in conflict.file_paths)

        valid_blocks = 0
        for block in conflict.blocks:
            # Check structural integrity (balanced brackets) - useful for all languages
            current_struct = self._check_structural_integrity(block.current_content)
            incoming_struct = self._check_structural_integrity(block.incoming_content)

            if not (current_struct and incoming_struct):
                # If structure is broken, it's a messy conflict
                continue

            if not is_python:
                valid_blocks += 1.0  # Assume valid if structure is ok
                continue

            current_valid = self._is_valid_python(block.current_content)
            incoming_valid = self._is_valid_python(block.incoming_content)

            if current_valid and incoming_valid:
                valid_blocks += 1.0
            elif current_valid or incoming_valid:
                valid_blocks += 0.5
            else:
                # If neither parses, but structure is ok, give some credit
                valid_blocks += 0.2

        return valid_blocks / len(conflict.blocks)

    def _calculate_merge_feasibility(self, conflict: Conflict) -> float:
        """
        Estimate merge feasibility (0.0 - 1.0).
        Automatable vs manual steps estimate.
        """
        if not conflict.blocks:
            return 1.0

        # Sensitive keywords that suggest complex logic changes
        sensitive_keywords = {"class", "def", "async", "await", "import", "from", "return", "yield"}

        feasible_blocks = 0
        for block in conflict.blocks:
            current_lines = block.current_content.strip().splitlines()
            incoming_lines = block.incoming_content.strip().splitlines()

            # Simple addition/deletion
            if not current_lines or not incoming_lines:
                feasible_blocks += 1.0
                continue

            # Whitespace only changes
            if block.current_content.strip() == block.incoming_content.strip():
                feasible_blocks += 1.0
                continue

            # Check for sensitive keywords
            has_sensitive = any(
                kw in block.current_content or kw in block.incoming_content
                for kw in sensitive_keywords
            )

            # Otherwise, assume it requires manual intervention, but give some points for small diffs
            diff_size = abs(len(current_lines) - len(incoming_lines))

            block_score = 0.0
            if diff_size < 5:
                block_score = 0.5
            else:
                block_score = 0.2

            if has_sensitive:
                block_score *= 0.5  # Penalize sensitive changes

            feasible_blocks += block_score

        return feasible_blocks / len(conflict.blocks)
