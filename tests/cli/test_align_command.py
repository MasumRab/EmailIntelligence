"""Tests for the align command."""

import pytest
from argparse import Namespace
from src.cli.commands.align_command import AlignCommand, AlignmentRule, AlignmentResult, AlignmentReport

class TestAlignCommand:
    @pytest.mark.asyncio
    async def test_execute_success(self):
        cmd = AlignCommand()
        args = Namespace(branch="feature/test")
        result = await cmd.execute(args)
        assert result == 0

    @pytest.mark.asyncio
    async def test_execute_failure(self):
        cmd = AlignCommand()
        args = Namespace(branch="main")
        result = await cmd.execute(args)
        assert result == 1

class TestAlignmentModels:
    def test_alignment_rule_creation(self):
        rule = AlignmentRule(name="test_rule", description="A test rule")
        assert rule.name == "test_rule"
        assert rule.description == "A test rule"
        assert rule.is_blocking is True

    def test_alignment_report_creation(self):
        result = AlignmentResult(rule_name="test_rule", passed=True)
        report = AlignmentReport(branch_name="feature/test", results=[result])
        assert report.branch_name == "feature/test"
        assert len(report.results) == 1
        assert report.results[0].passed is True

    @pytest.mark.asyncio
    async def test_execute_no_branch_argument(self, monkeypatch):
        # When no branch is passed, it falls back to the current branch.
        # We mock git rev-parse to return a valid branch name.
        import subprocess
        def mock_run(*args, **kwargs):
            class MockResult:
                stdout = "feature/current-branch"
                returncode = 0
            return MockResult()
        
        monkeypatch.setattr(subprocess, "run", mock_run)
        
        cmd = AlignCommand()
        args = Namespace(branch=None)
        result = await cmd.execute(args)
        assert result == 0

    @pytest.mark.asyncio
    async def test_execute_no_branch_detached_head(self, monkeypatch):
        import subprocess
        def mock_run(*args, **kwargs):
            class MockResult:
                stdout = "HEAD"
                returncode = 0
            return MockResult()
        
        monkeypatch.setattr(subprocess, "run", mock_run)
        
        cmd = AlignCommand()
        args = Namespace(branch=None)
        result = await cmd.execute(args)
        assert result == 1
