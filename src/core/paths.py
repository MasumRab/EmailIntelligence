"""Locate the repository root from any module, without counting parent levels.

The previous convention derived the project root by counting ``os.path.dirname``
calls from ``__file__`` (``parent.parent.parent`` and friends).  That is exactly
what rotted when modules moved from ``backend/python_nlp/`` to
``src/backend/python_nlp/``: every constant silently shifted one level down and
started pointing at ``src/`` instead of the repository root, so ``data/`` -- which
is gitignored and absent from a fresh checkout -- was never found.

Counting parents encodes each module's depth into a path, so every future move
breaks it again.  Walking up until a stable marker file is found is
depth-independent: the marker, not the module's location, defines the root.
"""

from pathlib import Path
from typing import Optional

# A tracked file that only exists at the repository root.
ROOT_MARKER = "pyproject.toml"


def project_root(start: Optional[Path] = None) -> Path:
    """Return the repository root: the nearest directory holding the marker.

    Args:
        start: File or directory to start the walk from.  Defaults to this
            module's own ``__file__``.

    Returns:
        The resolved repository root directory.

    Raises:
        FileNotFoundError: If no ancestor directory contains the marker.
    """
    current = Path(start if start is not None else __file__).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / ROOT_MARKER).is_file():
            return candidate

    raise FileNotFoundError(
        f"Could not locate {ROOT_MARKER!r} in any parent of {current}; "
        "cannot determine the repository root."
    )
