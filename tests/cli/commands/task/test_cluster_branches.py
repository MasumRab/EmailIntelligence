import pytest
from src.cli.commands.task.engine.branch_clustering import BranchAnalyzer

CODE_BEFORE = """
import os
import sys

def calculate_total(a: int, b: int) -> int:
    '''Calculate the total of two integers.'''
    # Add the numbers
    return a + b

class DataProcessor:
    def process(self, data):
        return [calculate_total(x, 1) for x in data]
"""

# Test Fixtures covering standard semantic edge cases
SCENARIOS = [
    # (name, source_code, expected_delta_key, expected_delta_val)
    ("whitespace_only", CODE_BEFORE.replace("    return a + b", "\n\n    return a + b"), "structural_hash", "MATCH"),
    ("comment_only", CODE_BEFORE.replace("# Add the numbers", "# Simply add numbers"), "comments", ["# Simply add numbers"]),
    ("docstring_only", CODE_BEFORE.replace("Calculate the total of two integers", "Returns sum of a and b"), "docstrings", ["Returns sum of a and b."]),
    ("import_added", "import json\n" + CODE_BEFORE, "imports", ["json", "os", "sys"]),
    ("import_removed", CODE_BEFORE.replace("import sys\n", ""), "imports", ["os"]),
    ("import_reorder", CODE_BEFORE.replace("import os\nimport sys", "import sys\nimport os"), "imports", ["sys", "os"]),
    ("logic_change", CODE_BEFORE.replace("return a + b", "if a<0: return 0\n    return a + b"), "structural_hash", "MISMATCH"),
    ("rename_func", CODE_BEFORE.replace("calculate_total", "get_sum"), "functions", ["get_sum", "process"]),
    ("class_added", CODE_BEFORE + "\nclass Helper:\n    pass\n", "classes", ["DataProcessor", "Helper"]),
    ("decorator_added", "from functools import lru_cache\n" + CODE_BEFORE.replace("def calculate_total", "@lru_cache(maxsize=128)\ndef calculate_total"), "imports", ["functools.lru_cache", "os", "sys"]),
    ("parameter_changed", CODE_BEFORE.replace("(a: int, b: int)", "(a: int, b: int, c: int = 0)"), "structural_hash", "MISMATCH")
]

@pytest.fixture
def analyzer():
    return BranchAnalyzer()

def test_baseline_extraction(analyzer):
    """Ensure baseline extracts expected standard symbols."""
    res = analyzer.analyze_file(CODE_BEFORE)
    assert "os" in res["imports"]
    assert "sys" in res["imports"]
    assert "calculate_total" in res["functions"]
    assert "DataProcessor" in res["classes"]
    assert len(res["docstrings"]) == 1
    assert len(res["comments"]) == 1

@pytest.mark.parametrize("name, code, delta_key, delta_val", SCENARIOS)
def test_semantic_extraction_scenarios(analyzer, name, code, delta_key, delta_val):
    """
    Consolidated AST evaluation suite ensuring that `libcst` and `ast` accurately
    detect changes without polluting the repo with dozens of physical fixture files.
    """
    base_res = analyzer.analyze_file(CODE_BEFORE)
    test_res = analyzer.analyze_file(code)

    if delta_val == "MATCH":
        assert test_res[delta_key] == base_res[delta_key], f"Failed {name}: {delta_key} should match but differed"
    elif delta_val == "MISMATCH":
        assert test_res[delta_key] != base_res[delta_key], f"Failed {name}: {delta_key} should mismatch but matched"
    else:
        # Check list intersections
        assert test_res[delta_key] == delta_val, f"Failed {name}: expected {delta_key} to be {delta_val}, got {test_res[delta_key]}"

    # Content hash should ALWAYS mismatch if code string is different
    if name != "identical":
        assert test_res["content_hash"] != base_res["content_hash"]

from argparse import Namespace
from src.cli.commands.task.cluster_branches import ClusterBranchesCommand

@pytest.mark.asyncio
async def test_validation_success(monkeypatch):
    """Ensure the execution correctly passes validation."""
    cmd = ClusterBranchesCommand()
    args = Namespace(primary="main", mode="hybrid", output=None, validate="dummy.yaml")

    # Mock branches to avoid git subprocess
    monkeypatch.setattr(cmd, "_get_remote_branches", lambda: ["feat/test-branch"])

    # Mock engine execution
    class MockEngine:
        def execute(self, branches, primary):
            return {"feat/test-branch": {"target": "main", "confidence": 0.8, "reasoning": "mock", "tags": []}}
    cmd.engine = MockEngine()

    # Mock Validator to return True (Pass)
    # Note: This mocks the yaml file loading in __init__ by accepting any argument
    class MockValidator:
        def __init__(self, f): pass  # noqa: ARG001 - intentionally unused
        def validate(self, res): return True
    monkeypatch.setattr("src.cli.commands.task.engine.validation_framework.Validator", MockValidator)

    # Execute and assert exit code 0
    assert await cmd.execute(args) == 0

@pytest.mark.asyncio
async def test_validation_failure(monkeypatch):
    """Ensure the execution correctly fails and returns exit code 1 when validation fails."""
    cmd = ClusterBranchesCommand()
    args = Namespace(primary="main", mode="hybrid", output=None, validate="dummy.yaml")

    monkeypatch.setattr(cmd, "_get_remote_branches", lambda: ["feat/test-branch"])

    class MockEngine:
        def execute(self, branches, primary):
            return {"feat/test-branch": {"target": "main", "confidence": 0.8, "reasoning": "mock", "tags": []}}
    cmd.engine = MockEngine()

    # Mock Validator to return False (Fail)
    # Note: This mocks the yaml file loading in __init__ by accepting any argument
    class MockValidator:
        def __init__(self, f): pass  # noqa: ARG001 - intentionally unused
        def validate(self, res): return False
    monkeypatch.setattr("src.cli.commands.task.engine.validation_framework.Validator", MockValidator)

    # Execute and assert exit code 1
    assert await cmd.execute(args) == 1
