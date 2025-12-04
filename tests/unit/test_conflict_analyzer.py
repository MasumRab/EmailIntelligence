import pytest
from src.analysis.conflict_analyzer import ConflictAnalyzer
from src.core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel


class TestConflictAnalyzer:

    @pytest.fixture
    def analyzer(self):
        return ConflictAnalyzer()

    @pytest.fixture
    def sample_conflict(self):
        block1 = ConflictBlock(
            file_path="test.py",
            start_line=10,
            end_line=15,
            current_content="def foo():\n    return 1",
            incoming_content="def foo():\n    return 2",
            conflict_marker_type="git",
        )
        return Conflict(
            id="test-conflict",
            type=ConflictTypeExtended.MERGE_CONFLICT,
            severity=RiskLevel.MEDIUM,
            description="Test conflict",
            file_paths=["test.py"],
            blocks=[block1],
        )

    def test_calculate_complexity(self, analyzer, sample_conflict):
        # 1 hunk (10) + 2 lines current + 2 lines incoming = 14
        complexity = analyzer._calculate_complexity(sample_conflict)
        assert complexity == 14

    def test_calculate_overlap(self, analyzer, sample_conflict):
        # "def foo():\n    return 1" vs "def foo():\n    return 2"
        # High similarity
        overlap = analyzer._calculate_overlap(sample_conflict)
        assert overlap > 0.8

    def test_calculate_semantic_compatibility(self, analyzer, sample_conflict):
        # Both are valid python
        semantic = analyzer._calculate_semantic_compatibility(sample_conflict)
        assert semantic == 1.0

    def test_calculate_semantic_compatibility_invalid(self, analyzer):
        block = ConflictBlock(
            file_path="test.py",
            start_line=1,
            end_line=2,
            current_content="def foo(",  # Invalid
            incoming_content="def foo)",  # Invalid
            conflict_marker_type="git",
        )
        conflict = Conflict(
            id="invalid",
            type=ConflictTypeExtended.MERGE_CONFLICT,
            severity=RiskLevel.HIGH,
            description="Invalid",
            file_paths=["test.py"],
            blocks=[block],
        )
        semantic = analyzer._calculate_semantic_compatibility(conflict)
        assert semantic == 0.0

    def test_calculate_merge_feasibility(self, analyzer, sample_conflict):
        # Small diff (0.5) but contains 'def' (sensitive keyword, * 0.5) -> 0.25
        feasibility = analyzer._calculate_merge_feasibility(sample_conflict)
        assert feasibility == 0.25

    def test_calculate_alignment_score(self, analyzer, sample_conflict):
        score = analyzer.calculate_alignment_score(sample_conflict)
        assert 0.0 <= score <= 1.0
        # Should be relatively high for this simple conflict
        assert score > 0.5

    def test_check_structural_integrity(self, analyzer):
        assert analyzer._check_structural_integrity("def foo():\n    return (1 + 2)")
        assert analyzer._check_structural_integrity("x = [1, 2, {3: 4}]")
        assert not analyzer._check_structural_integrity(
            "def foo():\n    return (1 + 2"
        )  # Missing )
        assert not analyzer._check_structural_integrity("x = [1, 2, {3: 4]")  # Missing }

    def test_calculate_complexity_fragmentation(self, analyzer):
        # Create a conflict with many small hunks
        blocks = []
        for i in range(5):
            blocks.append(
                ConflictBlock(
                    file_path="test.py",
                    start_line=i * 10,
                    end_line=i * 10 + 2,
                    current_content=f"line {i}",
                    incoming_content=f"Line {i}",
                    conflict_marker_type="git",
                )
            )

        conflict = Conflict(
            id="fragmented",
            type=ConflictTypeExtended.MERGE_CONFLICT,
            severity=RiskLevel.HIGH,
            description="Fragmented",
            file_paths=["test.py"],
            blocks=blocks,
        )

        complexity = analyzer._calculate_complexity(conflict)
        # 5 hunks * 10 = 50
        # 5 * 2 lines = 10 lines
        # Fragmentation penalty: 5 hunks * 5 = 25 (since avg lines/hunk is 2 < 3)
        # Total = 85
        assert complexity == 85

    def test_calculate_merge_feasibility_sensitive(self, analyzer):
        block = ConflictBlock(
            file_path="test.py",
            start_line=10,
            end_line=15,
            current_content="class MyClass:",
            incoming_content="class YourClass:",
            conflict_marker_type="git",
        )
        conflict = Conflict(
            id="sensitive",
            type=ConflictTypeExtended.MERGE_CONFLICT,
            severity=RiskLevel.HIGH,
            description="Sensitive",
            file_paths=["test.py"],
            blocks=[block],
        )

        feasibility = analyzer._calculate_merge_feasibility(conflict)
        # Diff size < 5 -> 0.5
        # Sensitive keyword 'class' -> 0.5 * 0.5 = 0.25
        assert feasibility == 0.25
