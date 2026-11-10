import re
import subprocess
import sys

_SAFE_REF = re.compile(r'^[A-Za-z0-9][A-Za-z0-9/_.-]*$')


_TREE_OID = re.compile(r'^[0-9a-f]{40,64}$')


def _safe_ref(name: str) -> str:
    """Return the regex-matched branch name. A bool check leaves the raw argv value tainted."""
    match = _SAFE_REF.match(name or "")
    if not match:
        raise ValueError("Invalid branch name")
    return match.group(0)


def check_branch_status(branch):
    """Report whether ``branch`` merges cleanly into ``main``.

    Uses ``git merge-tree --write-tree`` (git >= 2.38), which performs the
    merge in memory without touching the working tree. Its exit status is the
    verdict: 0 means clean, 1 means conflicts, anything else is a failure to
    compute (bad ref, missing object), which is not the same as a conflict.

    Exit status 1 alone is ambiguous: a branch that does not exist also exits 1
    ("not something we can merge"). A conflict leaves the merged tree id as the
    first line of stdout, so that is what confirms the conflict reading.
    """
    try:
        branch = _safe_ref(branch)
    except ValueError:
        return "error"

    try:
        result = subprocess.run(
            ['git', 'merge-tree', '--write-tree', 'main', branch],
            capture_output=True,
            text=True,
        )
    except OSError:
        return "error"

    if result.returncode == 0:
        return "clean"
    first_line = (result.stdout or "").strip().splitlines()[:1]
    if result.returncode == 1 and first_line and _TREE_OID.match(first_line[0]):
        return "conflicting"
    return "error"


def process_branches(branches):
    results = {}
    for branch in branches:
        results[branch] = check_branch_status(branch)
        print(f"{branch}: {results[branch]}")
    return results


if __name__ == '__main__':
    process_branches(sys.argv[1:])
