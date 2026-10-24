import subprocess
import os

# Use GraphQL API to push commits directly
branch_name = "jules/4928457512359891241"
head_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()

try:
    print(f"Creating branch {branch_name}...")
    subprocess.run(["gh", "api", "repos/MasumRab/EmailIntelligence/git/refs",
                   "-X", "POST",
                   "-F", f"ref=refs/heads/{branch_name}",
                   "-F", f"sha={head_sha}"], check=True)
except subprocess.CalledProcessError:
    print("Branch may already exist, updating...")
    subprocess.run(["gh", "api", f"repos/MasumRab/EmailIntelligence/git/refs/heads/{branch_name}",
                   "-X", "PATCH",
                   "-F", f"sha={head_sha}",
                   "-F", "force=true"], check=True)

print("Creating PR...")
result = subprocess.run([
    "gh", "pr", "create",
    "--base", "main",
    "--head", branch_name,
    "--title", "Fix NameError in verify_password and extract dummy hash",
    "--body", "Fixes a NameError that occurs when handling invalid hashes or mismatched passwords in the verify_password function due to a missing argon2.exceptions import. It also extracts a hardcoded dummy hash to a module-level constant DUMMY_PASSWORD_HASH for reuse and better timing attack mitigation. Regression tests are included to ensure these exceptions are safely caught and return False."
], capture_output=True, text=True)

if result.returncode != 0:
    print(result.stderr)
else:
    print(result.stdout)
