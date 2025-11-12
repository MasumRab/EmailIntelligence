"""
TODO: Deprecate and remove this module.

This module provides a basic, blocking progress bar implementation.
It has been superseded by the use of `tqdm` for progress indicators
in the new unified CLI (`src/cli/main.py`).

This module (along with other modules in `src/cli/` like `analyze.py`, `ci.py`,
`identify.py`, `install.py`, `verify.py`) should be deprecated and removed.
"""
import time
import sys

def progress_bar(duration, task_name):
    """
    Displays a progress bar for a given duration.
    """
    print(f"Running {task_name}...")
    for i in range(duration + 1):
        time.sleep(1)
        percent = int((i / duration) * 100)
        sys.stdout.write("\r")
        sys.stdout.write("[%-20s] %d%%" % ('=' * int(percent / 5), percent))
        sys.stdout.flush()
    sys.stdout.write("\n")