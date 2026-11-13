"""Regression tests for terminal escape-sequence injection in the shell loggers.

``backup.sh``, ``scripts/setup_automation.sh``, ``scripts/sync-common-docs.sh``
and ``scripts/test_orchestration.sh`` each print status lines built from a
message that can carry untrusted text — a file name, a git branch name, a line
of captured output. Two properties have to hold at once, and the two attempts
made so far each got one:

* a **raw** ESC byte in the message must not reach the terminal. ``ESC ] 0 ; …
  BEL`` is an OSC sequence: it rewrites the window title, and the payload is
  attacker-chosen.
* an **ordinary** message must print unchanged. ``printf %q`` neutralises the
  escape but turns ``Backup complete for 3 files`` into
  ``Backup\\ complete\\ for\\ 3\\ files``, which is unreadable on every line of
  every script.

These tests execute the helpers and inspect the bytes they write, rather than
comparing against one particular escaping scheme. A different-but-correct
sanitisation still passes; the earlier test compared against the exact ``%q``
rendering, so it pinned the implementation instead of the property.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

#: script → the logging helpers it defines, in declaration order.
SCRIPTS: dict[str, tuple[str, ...]] = {
    "backup.sh": ("log_info", "log_success", "log_warning", "log_error"),
    "scripts/setup_automation.sh": ("print_status", "print_success", "print_warning", "print_error"),
    "scripts/sync-common-docs.sh": ("print_status", "print_success", "print_warning", "print_error"),
    "scripts/test_orchestration.sh": ("log_info", "log_success", "log_warning", "log_error"),
}

CASES = [(rel, fn) for rel, functions in SCRIPTS.items() for fn in functions]

#: The variables each script sets before defining its helpers. Supplied here
#: rather than by sourcing the script, because every one of them runs work at
#: top level and would touch the repository.
COLOURS = (
    "BLUE='\\033[0;34m'\n"
    "GREEN='\\033[0;32m'\n"
    "YELLOW='\\033[1;33m'\n"
    "RED='\\033[0;31m'\n"
    "NC='\\033[0m'\n"
)

ESC = "\x1b"
BEL = "\x07"
OSC_TITLE = f"{ESC}]0;"


def _function_source(rel: str, name: str) -> str:
    """Return the text of ``name() { … }`` exactly as the script defines it."""
    text = (REPO_ROOT / rel).read_text()
    match = re.search(rf"^{name}\(\) \{{.*?^\}}$", text, re.MULTILINE | re.DOTALL)
    assert match is not None, f"{name}() is no longer defined in {rel}"
    return match.group(0)


def _run(rel: str, name: str, message: str) -> bytes:
    """Invoke one helper with ``message`` as ``$1`` and return its raw stdout."""
    script = COLOURS + _function_source(rel, name) + f'\n{name} "$1"\n'
    completed = subprocess.run(
        ["bash", "-c", script, "bash", message],
        capture_output=True,
        check=True,
    )
    return completed.stdout


@pytest.mark.parametrize(("rel", "name"), CASES)
def test_a_raw_escape_byte_never_reaches_the_terminal(rel: str, name: str) -> None:
    """The escape byte is already in the argument; %s alone does not stop it."""
    output = _run(rel, name, f"{OSC_TITLE}pwned{BEL}")

    assert OSC_TITLE.encode() not in output, f"{rel}:{name} emitted an OSC title sequence"
    assert BEL.encode() not in output, f"{rel}:{name} emitted a raw BEL"


@pytest.mark.parametrize(("rel", "name"), CASES)
def test_a_literal_backslash_escape_is_not_interpreted(rel: str, name: str) -> None:
    """A caller writing ``\\x1b`` as text must not have it expanded by printf %b."""
    output = _run(rel, name, r"\x1b]0;pwned\x07")

    assert OSC_TITLE.encode() not in output
    assert BEL.encode() not in output


@pytest.mark.parametrize(("rel", "name"), CASES)
def test_an_ordinary_message_prints_unchanged(rel: str, name: str) -> None:
    """Sanitising must not quote, escape or otherwise mangle a normal message."""
    assert b"Backup complete for 3 files" in _run(rel, name, "Backup complete for 3 files")
