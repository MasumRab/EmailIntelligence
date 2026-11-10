"""installing Node dependencies must never hand the command to a shell.

`install_nodejs_dependencies` used to pass `shell=(os.name == "nt")` and a bare
`"npm"` argv entry. On Windows that re-parses the list through cmd.exe, so a
PATH entry or a directory name containing shell metacharacters could run an
arbitrary command. These checks fail on the pre-fix code.
"""

import shutil
import types
from pathlib import Path

import setup.launch as launch


def _prepare(monkeypatch, tmp_path: Path) -> dict:
    """Point the launcher at a throwaway root and capture the run_command call."""
    calls: dict = {}

    def fake_run(cmd, desc, cwd=None, shell=False):
        calls.update(cmd=cmd, desc=desc, cwd=cwd, shell=shell)
        return True

    (tmp_path / "client").mkdir()
    (tmp_path / "client" / "package.json").write_text("{}")
    monkeypatch.setattr(launch, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(launch, "run_command", fake_run)
    monkeypatch.setattr(launch, "check_node_npm_installed", lambda: True)
    return calls


def test_npm_is_never_run_through_a_shell_on_windows(monkeypatch, tmp_path):
    """The defect only armed itself on Windows, so the test must say nt."""
    calls = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(launch, "os", types.SimpleNamespace(name="nt"))

    assert launch.install_nodejs_dependencies("client") is True

    assert calls["shell"] is False, f"shell={calls['shell']!r} re-opens the injection sink"


def test_npm_binary_is_resolved_to_an_explicit_path(monkeypatch, tmp_path):
    calls = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(launch.shutil, "which", lambda name: "/opt/node/bin/npm" if name == "npm" else None)

    launch.install_nodejs_dependencies("client", update=True)

    assert calls["cmd"] == ["/opt/node/bin/npm", "update"]


def test_falls_back_to_the_name_when_npm_is_not_on_path(monkeypatch, tmp_path):
    calls = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(launch.shutil, "which", lambda name: None)

    launch.install_nodejs_dependencies("client")

    assert calls["cmd"] == ["npm", "install"]
    assert calls["shell"] is False


def test_shutil_is_the_module_actually_used():
    """Guard against a rename: the module must import the stdlib it calls."""
    assert launch.shutil is shutil
