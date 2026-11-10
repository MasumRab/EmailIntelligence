import pytest
from argparse import Namespace
from src.cli.commands.guide import GuideCommand

@pytest.mark.asyncio
async def test_guide_command_execution(capsys):
    command = GuideCommand()
    args = Namespace()
    
    # Execute should return 0
    result = await command.execute(args)
    assert result == 0
    
    # Check output
    captured = capsys.readouterr()
    assert "Interactive Workflow Guide" in captured.out
    assert "speckit.specify.toml" in captured.out

def test_guide_command_properties():
    command = GuideCommand()
    assert command.name == "guide"
    assert "Interactive workflow guide" in command.description
    
def test_guide_command_dependencies():
    command = GuideCommand()
    deps = command.get_dependencies()
    assert "security_validator" in deps
    assert "nlp" in deps
    
    command.set_dependencies({
        "security_validator": "mock_validator",
        "nlp": "mock_nlp"
    })
    
    assert command._security_validator == "mock_validator"
    assert command._nlp == "mock_nlp"
