import argparse
import json
import subprocess
import os
import datetime

BACKUP_FILE_DEFAULT = ".branch_backup.json"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nError: {result.stderr.strip()}")
    return result.stdout.strip()

def get_current_branch():
    return run_cmd("git rev-parse --abbrev-ref HEAD")

def get_current_sha():
    return run_cmd("git rev-parse HEAD")

def snapshot(backup_file=BACKUP_FILE_DEFAULT):
    branch_name = get_current_branch()
    sha = get_current_sha()

    timestamp = datetime.datetime.now().isoformat()
    backup_data = {
        "branch": branch_name,
        "sha": sha,
        "timestamp": timestamp
    }

    with open(backup_file, "w") as f:
        json.dump(backup_data, f, indent=4)

    print(f"Backup created: {branch_name} at {sha} saved to {backup_file}")
    return backup_data

def restore(backup_file=BACKUP_FILE_DEFAULT):
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found: {backup_file}")

    with open(backup_file, "r") as f:
        backup_data = json.load(f)

    target_sha = backup_data.get("sha")
    target_branch = backup_data.get("branch")

    if not target_sha or not target_branch:
        raise ValueError(f"Invalid backup data in {backup_file}")

    current_branch = get_current_branch()
    if current_branch != target_branch and current_branch != "HEAD":
        print(f"Warning: Current branch '{current_branch}' differs from backed up branch '{target_branch}'.")
        print(f"Checking out '{target_branch}' before restoring.")
        run_cmd(f"git checkout {target_branch}")

    run_cmd(f"git reset --hard {target_sha}")
    print(f"Restored {target_branch} to {target_sha}")
    return backup_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup and restore git branch ref.")
    parser.add_argument("action", choices=["snapshot", "restore"], help="Action to perform")
    parser.add_argument("--file", default=BACKUP_FILE_DEFAULT, help="Backup file path")

    args = parser.parse_args()

    try:
        if args.action == "snapshot":
            snapshot(args.file)
        elif args.action == "restore":
            restore(args.file)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
