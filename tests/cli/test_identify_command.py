import pytest
from argparse import Namespace
from src.cli.commands.identify_command import IdentifyCommand

class FakeProc:
    """Stand-in for an asyncio subprocess created by create_subprocess_exec."""

    def __init__(self, out: str):
        self.returncode = 0
        self._out = out.encode()

    async def communicate(self):
        return self._out, b""


def _patch_async_exec(monkeypatch, out: str):
    async def fake_exec(*args, **kwargs):
        return FakeProc(out)

    monkeypatch.setattr(
        "src.cli.commands.identify_command.asyncio.create_subprocess_exec",
        fake_exec,
    )

class TestIdentifyCommand:
    def test_command_properties(self):
        cmd = IdentifyCommand()
        assert cmd.name == "identify-branches"
        assert "categorize" in cmd.description.lower()

    @pytest.mark.asyncio
    async def test_execute_basic(self, capsys, monkeypatch):
        cmd = IdentifyCommand()
        
        _patch_async_exec(
            monkeypatch,
            "  main\n* feature/test-1\n  hotfix/bug-1\n  fix/issue-2\n  unknown-branch",
        )
        
        args = Namespace(json=False)
        result = await cmd.execute(args)
        
        assert result == 0
        captured = capsys.readouterr()
        
        assert "main [primary]" in captured.out
        assert "feature/test-1 [feature]" in captured.out
        assert "hotfix/bug-1 [hotfix]" in captured.out
        assert "fix/issue-2 [maintenance]" in captured.out
        assert "unknown-branch [feature]" in captured.out

    @pytest.mark.asyncio
    async def test_execute_json(self, capsys, monkeypatch):
        cmd = IdentifyCommand()
        
        _patch_async_exec(monkeypatch, "  main\n* feature/test-1")
        
        args = Namespace(json=True)
        result = await cmd.execute(args)
        
        assert result == 0
        captured = capsys.readouterr()
        
        import json
        output_json = json.loads(captured.out)
        
        assert len(output_json) == 2
        assert output_json[0] == {"name": "main", "category": "primary"}
        assert output_json[1] == {"name": "feature/test-1", "category": "feature"}
