import subprocess
import argparse
import sys
import re

def is_valid_branch_name(name):
    if not name or name.startswith('-'):
        return False
    return re.match(r'^[a-zA-Z0-9/\-_\.]+$', name) is not None

_SAFE_ARG = re.compile(r"[A-Za-z0-9/_.=^@:+-]*")


def _clean_arg(argument: str) -> str:
    """Return the argument, or raise if any character falls outside the allowlist."""
    match = _SAFE_ARG.fullmatch(argument)
    if not match:
        raise ValueError(f"Invalid argument format: {argument}")
    return match.group(0)


def run_cmd(cmd):
    if not isinstance(cmd, list) or not all(isinstance(x, str) for x in cmd):
        raise ValueError("Command must be a list of strings")

    for i, arg in enumerate(cmd):
        if i > 0 and arg.startswith('-') and arg not in ('--',):
            raise ValueError(f"Argument starts with '-': {arg}")

    # Pass the regex-matched values, not the originals: SonarCloud drops the taint only
    # when the value reaching subprocess.run is the one the regex produced.
    safe_cmd = [_clean_arg(argument) for argument in cmd]

    try:
        result = subprocess.run(safe_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running '{' '.join(safe_cmd)}': {e.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Check if a feature branch is up-to-date with its primary branch.")
    parser.add_argument("feature_branch", help="The feature branch to check")
    parser.add_argument("primary_branch", help="The primary target branch (e.g., main)")
    
    args = parser.parse_args()
    
    if not is_valid_branch_name(args.feature_branch):
        print(f"Error: Invalid feature branch name '{args.feature_branch}'", file=sys.stderr)
        sys.exit(1)
        
    if not is_valid_branch_name(args.primary_branch):
        print(f"Error: Invalid primary branch name '{args.primary_branch}'", file=sys.stderr)
        sys.exit(1)
    
    p_branch = args.primary_branch
    f_branch = args.feature_branch

    primary_commit = run_cmd(["git", "rev-parse", f"refs/heads/{p_branch}"])
    if not primary_commit:
        sys.exit(1)
        
    feature_commit = run_cmd(["git", "rev-parse", f"refs/heads/{f_branch}"])
    if not feature_commit:
        sys.exit(1)

    merge_base = run_cmd(["git", "merge-base", f"refs/heads/{p_branch}", f"refs/heads/{f_branch}"])
    if not merge_base:
        sys.exit(1)
        
    is_up_to_date = merge_base == primary_commit
    
    print(f"Feature branch: {f_branch}")
    print(f"Primary branch: {p_branch}")
    print(f"Merge base: {merge_base}")
    print(f"Primary latest: {primary_commit}")
    
    if is_up_to_date:
        print("Status: UP-TO-DATE")
        sys.exit(0)
    else:
        print("Status: OUT-OF-DATE")
        sys.exit(1)

if __name__ == "__main__":
    main()
