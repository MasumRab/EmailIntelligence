import argparse
import subprocess
import sys

def run_git_command(command, check=True):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip(), result.returncode

def is_divergent(branch, base):
    _, returncode = run_git_command(["git", "merge-base", "--is-ancestor", base, branch], check=False)
    # If base is not an ancestor of branch, they are divergent
    return returncode != 0

def get_merge_commit_count(branch, base):
    stdout, _ = run_git_command(["git", "rev-list", "--merges", f"{base}..{branch}", "--count"])
    return int(stdout) if stdout.isdigit() else 0

def get_commit_count(branch, base):
    stdout, _ = run_git_command(["git", "rev-list", f"{base}..{branch}", "--count"])
    return int(stdout) if stdout.isdigit() else 0

def get_changed_files_count(branch, base):
    # Using ... to get changes in branch since it diverged from base
    stdout, _ = run_git_command(["git", "diff", f"{base}...{branch}", "--name-only"])
    return len([line for line in stdout.split('\n') if line.strip()])

def analyze_branch(branch, base, threshold_commits=50, threshold_files=100):
    divergent = is_divergent(branch, base)
    merges = get_merge_commit_count(branch, base)
    commits = get_commit_count(branch, base)
    files = get_changed_files_count(branch, base)

    print(f"Branch Analysis: {branch} (Base: {base})")
    print(f"- Divergent from base: {'Yes' if divergent else 'No'}")
    print(f"- Merge commits: {merges}")
    print(f"- Total commits: {commits}")
    print(f"- Changed files: {files}")

    is_complex = (
        merges > 0 or
        commits >= threshold_commits or
        files >= threshold_files
    )

    print("\nComplexity Classification:")
    if is_complex:
        print("COMPLEX")
        print("\nRecommended Alignment Strategy: MULTILEVEL ITERATIVE REBASE")
        print("1. Semantic Level: Review architectural changes and decouple modules if possible.")
        print("2. Git Level: Perform iterative rebasing in small batches (e.g., 10 commits).")
        print("   Resolve conflicts incrementally.")
        print("3. Testing Level: Run targeted test subsets after each rebase batch.")
    else:
        print("SIMPLE")
        if divergent:
            print("\nRecommended Alignment Strategy: STANDARD REBASE")
            print("1. Perform a standard rebase: git rebase " + base)
        else:
            print("\nRecommended Alignment Strategy: FAST-FORWARD MERGE")
            print("1. Branch is up-to-date with base. Fast-forward merge is possible.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a Git branch for complexity.")
    parser.add_argument("branch", help="The branch to analyze")
    parser.add_argument("--base", default="main", help="The base branch to compare against (default: main)")
    args = parser.parse_args()

    analyze_branch(args.branch, args.base)
