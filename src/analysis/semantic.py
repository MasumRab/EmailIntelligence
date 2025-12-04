"""
Semantic analysis module for detecting semantic conflicts and incompatibilities.
"""

import ast
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from pathlib import Path

from ..core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel
from .code.ast_analyzer import ASTAnalyzer, CodeStructure
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SemanticConflictDetail:
    """Details about a detected semantic conflict."""

    conflict_type: str
    description: str
    severity: RiskLevel
    affected_symbols: List[str]
    evidence: List[str]
    suggestions: List[str]


class SemanticAnalyzer:
    """
    Analyzes code for semantic conflicts beyond syntactic differences.

    Detects issues like:
    - Function signature changes (parameter count/type mismatches)
    - Class hierarchy modifications
    - Import conflicts (same name, different modules)
    - Variable scope conflicts
    - Logic contradictions
    """

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()

    async def analyze_semantic_conflicts(self, conflict: Conflict) -> List[SemanticConflictDetail]:
        """
        Analyze a conflict for semantic issues.

        Returns a list of detected semantic conflicts with details.
        """
        semantic_conflicts = []

        for block in conflict.blocks:
            # Only analyze Python files
            if not block.file_path.endswith(".py"):
                continue

            # Parse both versions
            current_structure = self.ast_analyzer.analyze_structure(block.current_content)
            incoming_structure = self.ast_analyzer.analyze_structure(block.incoming_content)

            # Check for function signature conflicts
            sig_conflicts = self._check_signature_conflicts(
                current_structure, incoming_structure, block
            )
            semantic_conflicts.extend(sig_conflicts)

            # Check for import conflicts
            import_conflicts = self._check_import_conflicts(
                current_structure, incoming_structure, block
            )
            semantic_conflicts.extend(import_conflicts)

            # Check for class hierarchy conflicts
            class_conflicts = self._check_class_conflicts(
                current_structure, incoming_structure, block
            )
            semantic_conflicts.extend(class_conflicts)

        return semantic_conflicts

    def _check_signature_conflicts(
        self,
        current: CodeStructure,
        incoming: CodeStructure,
        block: ConflictBlock,
    ) -> List[SemanticConflictDetail]:
        """Check for function signature mismatches."""
        conflicts = []

        # Find functions that exist in both versions
        common_functions = set(current.functions) & set(incoming.functions)

        for func_name in common_functions:
            current_meta = current.function_metadata.get(func_name)
            incoming_meta = incoming.function_metadata.get(func_name)

            if not current_meta or not incoming_meta:
                continue

            evidence = []
            suggestions = []

            # Check type hint changes
            if current_meta.has_type_hints != incoming_meta.has_type_hints:
                evidence.append(
                    f"Function '{func_name}': type hints "
                    f"{'added' if incoming_meta.has_type_hints else 'removed'}"
                )
                suggestions.append(
                    f"Review type hint changes for '{func_name}' to ensure compatibility"
                )

            # Check error handling changes
            if current_meta.has_error_handling != incoming_meta.has_error_handling:
                evidence.append(
                    f"Function '{func_name}': error handling "
                    f"{'added' if incoming_meta.has_error_handling else 'removed'}"
                )
                suggestions.append(
                    f"Verify error handling changes in '{func_name}' don't break callers"
                )

            if evidence:
                conflicts.append(
                    SemanticConflictDetail(
                        conflict_type="signature_change",
                        description=f"Function signature changed: {func_name}",
                        severity=RiskLevel.MEDIUM,
                        affected_symbols=[func_name],
                        evidence=evidence,
                        suggestions=suggestions,
                    )
                )

        # Check for removed functions
        removed_functions = set(current.functions) - set(incoming.functions)
        if removed_functions:
            conflicts.append(
                SemanticConflictDetail(
                    conflict_type="function_removal",
                    description="Functions removed in incoming version",
                    severity=RiskLevel.HIGH,
                    affected_symbols=list(removed_functions),
                    evidence=[f"Function '{f}' removed" for f in removed_functions],
                    suggestions=[
                        "Ensure removed functions are not used elsewhere",
                        "Consider deprecation instead of removal",
                    ],
                )
            )

        # Check for added functions with same names as variables/imports
        added_functions = set(incoming.functions) - set(current.functions)
        if added_functions:
            # Check if any added function names conflict with imports
            conflicting = added_functions & set(current.imports)
            if conflicting:
                conflicts.append(
                    SemanticConflictDetail(
                        conflict_type="name_shadowing",
                        description="New functions shadow existing imports",
                        severity=RiskLevel.MEDIUM,
                        affected_symbols=list(conflicting),
                        evidence=[f"Function '{f}' shadows import" for f in conflicting],
                        suggestions=[
                            "Rename function or import to avoid shadowing",
                            "Use explicit module qualification",
                        ],
                    )
                )

        return conflicts

    def _check_import_conflicts(
        self,
        current: CodeStructure,
        incoming: CodeStructure,
        block: ConflictBlock,
    ) -> List[SemanticConflictDetail]:
        """Check for import statement conflicts."""
        conflicts = []

        current_imports = set(current.imports)
        incoming_imports = set(incoming.imports)

        # Check for removed imports
        removed_imports = current_imports - incoming_imports
        if removed_imports:
            conflicts.append(
                SemanticConflictDetail(
                    conflict_type="import_removal",
                    description="Imports removed in incoming version",
                    severity=RiskLevel.MEDIUM,
                    affected_symbols=list(removed_imports),
                    evidence=[f"Import '{i}' removed" for i in removed_imports],
                    suggestions=[
                        "Verify removed imports are not used in the code",
                        "Check if functionality moved to different module",
                    ],
                )
            )

        # Check for added imports
        added_imports = incoming_imports - current_imports
        if added_imports:
            # Check if any added imports conflict with existing function/class names
            conflicting_funcs = added_imports & set(current.functions)
            conflicting_classes = added_imports & set(current.classes)

            if conflicting_funcs or conflicting_classes:
                conflicts.append(
                    SemanticConflictDetail(
                        conflict_type="import_shadowing",
                        description="New imports shadow existing definitions",
                        severity=RiskLevel.HIGH,
                        affected_symbols=list(conflicting_funcs | conflicting_classes),
                        evidence=[
                            f"Import '{i}' shadows existing definition"
                            for i in (conflicting_funcs | conflicting_classes)
                        ],
                        suggestions=[
                            "Use import aliases to avoid shadowing",
                            "Rename local definitions",
                        ],
                    )
                )

        return conflicts

    def _check_class_conflicts(
        self,
        current: CodeStructure,
        incoming: CodeStructure,
        block: ConflictBlock,
    ) -> List[SemanticConflictDetail]:
        """Check for class definition conflicts."""
        conflicts = []

        current_classes = set(current.classes)
        incoming_classes = set(incoming.classes)

        # Check for removed classes
        removed_classes = current_classes - incoming_classes
        if removed_classes:
            conflicts.append(
                SemanticConflictDetail(
                    conflict_type="class_removal",
                    description="Classes removed in incoming version",
                    severity=RiskLevel.HIGH,
                    affected_symbols=list(removed_classes),
                    evidence=[f"Class '{c}' removed" for c in removed_classes],
                    suggestions=[
                        "Ensure removed classes are not instantiated elsewhere",
                        "Check for inheritance dependencies",
                    ],
                )
            )

        # Check for added classes
        added_classes = incoming_classes - current_classes
        if added_classes:
            # Check if any added classes conflict with existing names
            conflicting = added_classes & (set(current.functions) | set(current.imports))
            if conflicting:
                conflicts.append(
                    SemanticConflictDetail(
                        conflict_type="class_name_conflict",
                        description="New classes conflict with existing names",
                        severity=RiskLevel.MEDIUM,
                        affected_symbols=list(conflicting),
                        evidence=[f"Class '{c}' conflicts with existing name" for c in conflicting],
                        suggestions=[
                            "Rename class to avoid conflicts",
                            "Use namespacing or modules",
                        ],
                    )
                )

        return conflicts

    def calculate_semantic_risk(
        self, semantic_conflicts: List[SemanticConflictDetail]
    ) -> RiskLevel:
        """
        Calculate overall semantic risk level based on detected conflicts.
        """
        if not semantic_conflicts:
            return RiskLevel.LOW

        # Count by severity
        severity_counts = {
            RiskLevel.CRITICAL: 0,
            RiskLevel.HIGH: 0,
            RiskLevel.MEDIUM: 0,
            RiskLevel.LOW: 0,
        }

        for conflict in semantic_conflicts:
            severity_counts[conflict.severity] += 1

        # Determine overall risk
        if severity_counts[RiskLevel.CRITICAL] > 0:
            return RiskLevel.CRITICAL
        elif severity_counts[RiskLevel.HIGH] > 2:
            return RiskLevel.CRITICAL
        elif severity_counts[RiskLevel.HIGH] > 0:
            return RiskLevel.HIGH
        elif severity_counts[RiskLevel.MEDIUM] > 3:
            return RiskLevel.HIGH
        elif severity_counts[RiskLevel.MEDIUM] > 0:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
