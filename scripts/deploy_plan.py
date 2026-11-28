import argparse
import json
import subprocess
import sys

def get_deploy_plan(target_ref: str) -> dict:
    """
    Retrieves the deploy plan (staged files and target ref).
    """
    try:
        # Get staged files
        result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        staged_files = [f for f in result.stdout.split('\n') if f]
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}", file=sys.stderr)
        staged_files = []

    return {
        "target_ref": target_ref,
        "staged_files": staged_files
    }

def main():
    parser = argparse.ArgumentParser(description="Print deploy plan without executing")
    parser.add_argument(
        "--target-ref", 
        required=True, 
        help="Target branch, commit, or tag for deployment"
    )
    args = parser.parse_args()

    plan = get_deploy_plan(args.target_ref)
    
    print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()
