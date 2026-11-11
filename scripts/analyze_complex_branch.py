import argparse
import subprocess
import sys
import re

# Stricter SAFE_ARG regex - prevents leading dash, double dots, and restricts special chars
_SAFE_ARG = re.compile(r"^(?!-)(?!.*\.\.)[A-Za-z0-9_./~=-]*$")


def _clean_arg(argument):
    """Return the git argument, or raise. The matched text is what reaches argv."""
    match = _SAFE_ARG.fullmatch(argument)
    if not match:
        raise ValueError(f"Invalid git argument: {argument!r}")
    return match.group(0)


def run_git_command(command, check=True):
    # SonarCloud pythonsecurity:S8705 follows the caller-supplied strings into
    # subprocess.run; only the regex-matched values drop the taint.
    command = [_clean_arg(argument) for argument in command]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Git command failed: {' '.join(command)}", file=sys.stderr)
            print(f"Error: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        return e.stdout.strip(), e.returncode


def is_divergent(branch, base):
    # Use -- separator to prevent argument injection
    _, returncode = run_git_command(["git", "merge-base", "--is-ancestor", "--", base, branch], check=False)
    # If base is not an ancestor of branch, they are divergent
    return returncode != 0


def get_merge_commit_count(branch, base):
    stdout, _ = run_git_command(["git", "rev-list", "--merges", "--count", "--", f"{base}..{branch}"])
    return int(stdout) if stdout.isdigit() else 0


def get_commit_count(branch, base):
    stdout, _ = run_git_command(["git", "rev-list", "--count", "--", f"{base}..{branch}"])
    return int(stdout) if stdout.isdigit() else 0


def get_changed_files_count(branch, base):
    # Using ... to get changes in branch since it diverged from base
    # Use -- separator for safety
    stdout, _ = run_git_command(["git", "diff", "--name-only", "--", f"{base}...{branch}"])
    return len([line for line in stdout.split('\n') if line.strip()])


def is_valid_git_ref(ref):
    if not ref or ref.startswith('-'):
        return False
    return bool(re.match(r'^[a-zA-Z0-9_/\.-]+$', ref))


def analyze_branch(branch, base, threshold_commits=50, threshold_files=100):
    if not is_valid_git_ref(branch) or not is_valid_git_ref(base):
        print(f"Error: Invalid git reference: branch={branch}, base={base}", file=sys.stderr)
        sys.exit(1)

    if is_divergent(branch, base):
        merge_commits = get_merge_commit_count(branch, base)
        commit_count = get_commit_count(branch, base)
        changed_files = get_changed_files_count(branch, base)

        print(f"Branch: {branch}")
        print(f"Base: {base}")
        print("Status: DIVERGENT")
        print(f"Commits since divergence: {commit_count}")
        print(f"Merge commits: {merge_commits}")
        print(f"Changed files: {changed_files}")

        if merge_commits > 0:
            print(f"\n⚠️  COMPLEX: Branch has {merge_commits} merge commit(s).")
            print("   Recommended: REBASE with conflict resolution")
        elif commit_count > threshold_commits or changed_files > threshold_files:
            print(f"\n⚠️  COMPLEX: High commit count ({commit_count}) or file count ({changed_files}).")
            print("   Recommended: REBASE with conflict resolution")
        else:
            print("\nSIMPLE: Standard rebase recommended.")
    else:
        commit_count = get_commit_count(branch, base)
        print(f"Branch: {branch}")
        print(f"Base: {base}")
        print(f"Status: UP-TO-DATE")
        print(f"Commits ahead: {commit_count}")
        print("1. Branch is up-to-date with base. Fast-forward merge is possible.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a Git branch for complexity.")
    parser.add_argument("branch", help="Branch to analyze")
    parser.add_argument("base", help="Base branch to compare against")
    parser.add_argument("--threshold-commits", type=int, default=50, help="Commit threshold for complexity")
    parser.add_argument("--threshold-files", type=int, default=100, help="File threshold for complexity")
    args = parser.parse_args()

    analyze_branch(args.branch, args.base, args.threshold_commits, args.threshold_files)