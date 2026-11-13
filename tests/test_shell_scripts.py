"""Guards for the repository's shell scripts.

Two defects motivated this module, both found by hand and both invisible to the
rest of the suite because nothing parses a ``.sh`` file except the shell that
runs it:

* ``backup.sh`` ended with two lines of leaked model output — ``esac</content>``
  and a stray ``</xai:function_call: …``. The file was published in that state
  on ``main``, and ``bash -n`` rejects the whole script, so the backup tool the
  repository ships could not execute at all. No Python test noticed.
* the same class of artifact can land in any file, so the scan below is
  repository-wide rather than limited to the script that was broken.

These are cheap, deterministic checks on committed files; they never run the
scripts (several of them touch backups and worktrees).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Substrings that only appear in a shell script when an assistant's tool-call
#: markup was pasted into it. None is valid bash, but a script that is never
#: parsed can carry them indefinitely, which is exactly what happened.
LEAKED_SCAFFOLDING = ("</content>", "<xai:", "function_call", "</parameter>")


def _shell_scripts() -> list[Path]:
    """Every tracked shell script, so an untracked scratch file cannot fail CI."""
    listed = subprocess.run(
        ["git", "ls-files", "*.sh", "*.bash"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if listed.returncode == 0 and listed.stdout.strip():
        return sorted(REPO_ROOT / line for line in listed.stdout.splitlines() if line.strip())
    return sorted(p for p in REPO_ROOT.rglob("*.sh") if ".git" not in p.parts)


SCRIPTS = _shell_scripts()


def test_the_survey_found_shell_scripts() -> None:
    """A scan that finds nothing is a broken scan, not a clean repository."""
    assert SCRIPTS, "no shell scripts discovered; the survey itself is broken"


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_every_shell_script_parses(script: Path) -> None:
    """``bash -n`` is the shell's own parser; it rejects a file bash cannot run."""
    completed = subprocess.run(
        ["bash", "-n", str(script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, f"{script.name} does not parse:\n{completed.stderr}"


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_no_shell_script_carries_leaked_tool_output(script: Path) -> None:
    """Markup from an assistant's tool call is never part of a shell script."""
    text = script.read_text(errors="replace")
    found = [marker for marker in LEAKED_SCAFFOLDING if marker in text]
    assert not found, f"{script.name} carries leaked tool-call markup: {found}"
