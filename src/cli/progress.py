"""
Module for a basic, blocking progress bar implementation.

TODO: Assess the necessity of this module and either remove it or refactor it
for specific, limited use cases.

This module's `progress_bar` function has largely been superseded by the use
of `tqdm` for progress indicators in the new unified CLI (`src/cli/main.py`).

To adhere to SOLID principles, specifically the Single Responsibility Principle (SRP)
and the Open/Closed Principle (OCP), consider the following:

1.  **Remove if Obsolete:** If this `progress_bar` function is no longer used
    anywhere in the project (e.g., after migrating all calls to `tqdm`), it
    should be removed to reduce codebase clutter and improve maintainability.
2.  **Refactor for Reusability (if needed):** If a specific, simple, blocking
    progress bar is still genuinely required (e.g., for very short, non-async
    operations where `tqdm` might be overkill), refactor this function to be
    a standalone, reusable utility that adheres to SRP. Ensure it doesn't block
    the main thread unnecessarily if used in a larger application.
3.  **Consistency:** For consistency across the CLI, `tqdm` is the preferred
    progress indicator. Any new progress indication should leverage `tqdm`.
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