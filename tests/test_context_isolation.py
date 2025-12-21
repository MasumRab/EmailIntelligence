import os
import sys
import pytest

# Ensure src is in path
sys.path.append(os.path.abspath("src"))  # noqa: E402

from context_control.isolation import ContextIsolator  # noqa: E402
from context_control.models import AgentContext  # noqa: E402
from context_control.config import init_config  # noqa: E402


@pytest.fixture(scope="module", autouse=True)
def setup_config():
    try:
        init_config()
    except Exception:
        pass


def test_pattern_matching_optimization():
    cwd = os.getcwd()

    # Setup context with absolute patterns
    # ContextIsolator normalizes inputs to absolute paths, so patterns must generally match that
    # or be filename-only patterns.
    context = AgentContext(
        profile_id="test",
        agent_id="test",
        environment_type="test",
        accessible_files=[
            os.path.join(cwd, "src/*.py"),
            os.path.join(cwd, "config/*.json")
        ],
        restricted_files=[
            os.path.join(cwd, "src/secrets.py")
        ]
    )

    isolator = ContextIsolator(context)

    # Positive matches
    assert isolator.is_file_accessible(os.path.join(cwd, "src/main.py")), "Should match src/*.py"
    assert isolator.is_file_accessible(os.path.join(cwd, "config/settings.json")), "Should match config/*.json"

    # Negative matches (Restricted)
    assert not isolator.is_file_accessible(os.path.join(cwd, "src/secrets.py")), "Should be restricted"

    # Negative matches (No match)
    assert not isolator.is_file_accessible(os.path.join(cwd, "README.md")), "Should not match anything"

    # Check filename matching (legacy behavior check)
    # If pattern matches basename, it allows access.
    context_filename = AgentContext(
        profile_id="test_fn",
        agent_id="test_fn",
        environment_type="test",
        accessible_files=["safe_file.txt"],
        restricted_files=[]
    )
    isolator_fn = ContextIsolator(context_filename)
    assert isolator_fn.is_file_accessible(os.path.join(cwd, "any/dir/safe_file.txt")), "Should match by filename"

    # Check empty patterns
    context_empty = AgentContext(
        profile_id="test2",
        agent_id="test2",
        environment_type="test",
        accessible_files=[],
        restricted_files=[]
    )
    isolator_empty = ContextIsolator(context_empty)
    assert not isolator_empty.is_file_accessible("any_file.txt"), "Empty patterns should match nothing"
