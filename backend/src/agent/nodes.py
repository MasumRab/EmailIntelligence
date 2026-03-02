import os
from pathlib import Path

# Module path: backend/src/agent/nodes.py
# Parents:
# [0] agent
# [1] src
# [2] backend
# [3] root directory
ROOT_DIR = Path(__file__).resolve().parents[3]
CONTEXT_FILE = ROOT_DIR / "docs" / "ACTIVE_CONTEXT.md"
MAX_CONTEXT_LENGTH = 4000

def _get_active_context() -> str:
    """Reads the active context to prevent agents from duplicating work."""
    if not CONTEXT_FILE.exists():
        return "*Context file not found*"

    try:
        content = CONTEXT_FILE.read_text(encoding="utf-8")

        # Truncate if necessary
        if len(content) > MAX_CONTEXT_LENGTH:
            # We want to clearly indicate it was truncated
            truncated_indicator = "\n...[TRUNCATED: Additional PR context hidden to prevent context overflow]..."
            content = content[:MAX_CONTEXT_LENGTH - len(truncated_indicator)] + truncated_indicator

        return content
    except Exception as e:
        return f"*Failed to read active context: {e}*"

def generate_plan(prompt: str) -> str:
    """
    Simulates the agent's planning phase by injecting the active context.
    This demonstrates how the context is used by the LLM planner.
    """
    active_context = _get_active_context()

    # Inject context into the payload for the LLM
    payload = f"""
SYSTEM: You are an AI agent planning your next task.

Active Context (DO NOT DUPLICATE WORK IN THESE FILES):
------------------------------------------------------
{active_context}
------------------------------------------------------

USER REQUEST:
{prompt}
"""
    # In a real system, this payload would be sent to the LLM.
    # We return it here for demonstration and testing purposes.
    return payload

if __name__ == "__main__":
    # Test local run
    print(_get_active_context())
    print("\n\n---\n\n")
    print(generate_plan("Improve the CLI tool's argument parsing."))
