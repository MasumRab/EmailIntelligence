import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

def find_files_with_wildcard(pattern: str, root_dir: Path = Path('.')) -> List[Path]:
    """
    Finds files matching a given glob pattern within a root directory.

    Args:
        pattern: The glob pattern to match (e.g., "**/*.py", "src/**/*.md").
        root_dir: The root directory to start the search from. Defaults to the current directory.

    Returns:
        A list of Path objects for files matching the pattern.
    """
    if not root_dir.is_dir():
        logger.error(f"Root directory '{root_dir}' does not exist or is not a directory.")
        return []

    found_files = list(root_dir.rglob(pattern))
    logger.debug(f"Found {len(found_files)} files matching pattern '{pattern}' in '{root_dir}'")
    return found_files

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example usage:
    print("Searching for all Python files:")
    python_files = find_files_with_wildcard("**/*.py")
    for f in python_files:
        print(f)

    print("\nSearching for markdown files in docs directory:")
    markdown_files = find_files_with_wildcard("*.md", root_dir=Path("docs"))
    for f in markdown_files:
        print(f)
