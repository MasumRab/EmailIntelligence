"""The legacy data-directory constant must honour the DATA_DIR environment variable.

`DatabaseConfig.__init__` already reads `DATA_DIR`, and `tests/conftest.py` sets it,
but the module-level constant that the legacy (config-less) path uses did not — so the
two paths could point at different directories. The constant is bound at import time,
so this is checked in a subprocess rather than by monkeypatching a live module.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_module_data_dir_honours_env():
    env = dict(os.environ, DATA_DIR="/tmp/ei-data-dir-probe")
    proc = subprocess.run(
        [sys.executable, "-c", "import src.core.database as d; print(d.DATA_DIR)"],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "/tmp/ei-data-dir-probe"


def test_module_data_dir_defaults_to_data():
    env = {k: v for k, v in os.environ.items() if k != "DATA_DIR"}
    proc = subprocess.run(
        [sys.executable, "-c", "import src.core.database as d; print(d.DATA_DIR)"],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "data"
