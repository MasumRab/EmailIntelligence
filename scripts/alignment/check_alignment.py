import subprocess
import argparse
import sys

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running '{' '.join(cmd)}': {e.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Check if a feature branch is up-to-date with its primary branch.")
    parser.add_argument("feature_branch", help="The feature branch to check")
    parser.add_argument("primary_branch", help="The primary target branch (e.g., main)")

    args = parser.parse_args()

    # Ensure branches are available locally (we assume they are for this script context)

    # Get the latest commit of the primary branch
    primary_commit = run_cmd(["git", "rev-parse", args.primary_branch])
    if not primary_commit:
        sys.exit(1)

    # Get the latest commit of the feature branch
    feature_commit = run_cmd(["git", "rev-parse", args.feature_branch])
    if not feature_commit:
        sys.exit(1)

    # Find the merge base
    merge_base = run_cmd(["git", "merge-base", args.primary_branch, args.feature_branch])
    if not merge_base:
        sys.exit(1)

    # Check if the feature branch is up-to-date
    # It is up-to-date if the merge base is exactly the latest commit of the primary branch
    is_up_to_date = merge_base == primary_commit

    print(f"Feature branch: {args.feature_branch}")
    print(f"Primary branch: {args.primary_branch}")
    print(f"Merge base: {merge_base}")
    print(f"Primary latest: {primary_commit}")

    if is_up_to_date:
        print("Status: UP-TO-DATE")
        sys.exit(0)
    else:
        print("Status: OUT-OF-DATE")
        sys.exit(0)

if __name__ == "__main__":
    main()
