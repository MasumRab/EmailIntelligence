import os
import sys
import subprocess
import shutil
import requests
import re
from pathlib import Path

# Constants
DOCS_DIR = Path("docs")
CONTEXT_FILE = DOCS_DIR / "ACTIVE_CONTEXT.md"
DEGRADED_MESSAGE = "*GitHub Token missing - Context unavailable*"
API_ERROR_MESSAGE = "*GitHub API Error - Context unavailable*"
TIMEOUT = 10
API_BASE_URL = "https://api.github.com"

def get_repository():
    """Gets the repository string ('owner/repo') from env or git config."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo:
        return repo

    try:
        # Fallback to git config safely
        result = subprocess.run(
            [shutil.which("git") or "git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()

        # Parse SSH or HTTPS urls
        # SSH: git@github.com:owner/repo.git
        # HTTPS: https://github.com/owner/repo.git

        # HTTPS matching
        https_match = re.match(r"https://github\.com/(.+?)/(.+?)(\.git)?$", url)
        if https_match:
            return f"{https_match.group(1)}/{https_match.group(2)}"

        # SSH matching
        ssh_match = re.match(r"git@github\.com:(.+?)/(.+?)(\.git)?$", url)
        if ssh_match:
            return f"{ssh_match.group(1)}/{ssh_match.group(2)}"

    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return None

def fetch_paginated(url, headers):
    """Fetches all items across all pages using the Link header."""
    items = []
    current_url = url

    while current_url:
        response = requests.get(current_url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, list):
            items.extend(data)
        else:
            items.append(data)

        # Check for pagination in Link header
        link_header = response.headers.get("Link")
        current_url = None
        if link_header:
            # Look for rel="next"
            links = link_header.split(",")
            for link in links:
                parts = link.split(";")
                if len(parts) >= 2 and 'rel="next"' in parts[1]:
                    # Extract URL from <url>
                    match = re.search(r"<(.*?)>", parts[0])
                    if match:
                        current_url = match.group(1)
                        break

    return items

def generate_context():
    """Generates the ACTIVE_CONTEXT.md content."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN missing. Using degraded mode.")
        write_context(DEGRADED_MESSAGE)
        return

    repo = get_repository()
    if not repo:
        print("Could not determine repository. Using degraded mode.")
        write_context(DEGRADED_MESSAGE)
        return

    print(f"Fetching active context for {repo}...")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        # Fetch open PRs
        prs_url = f"{API_BASE_URL}/repos/{repo}/pulls?state=open&per_page=100"
        prs = fetch_paginated(prs_url, headers)

        if not prs:
            write_context("No active Pull Requests found.\n")
            return

        content = ["# Active GitHub Context\n",
                   "This file contains currently open Pull Requests and their modified files to prevent work duplication.\n\n"]

        for pr in prs:
            pr_number = pr.get("number")
            pr_title = pr.get("title")
            pr_url = pr.get("html_url")
            pr_author = pr.get("user", {}).get("login", "Unknown")

            content.append(f"## [PR #{pr_number}]({pr_url}) - {pr_title} (by @{pr_author})\n")
            content.append("**Locked Files:**\n")

            # Fetch files for this PR
            files_url = f"{API_BASE_URL}/repos/{repo}/pulls/{pr_number}/files?per_page=100"
            files = fetch_paginated(files_url, headers)

            if files:
                for f in files:
                    filename = f.get("filename")
                    status = f.get("status")
                    content.append(f"- `{filename}` ({status})\n")
            else:
                content.append("- *No files modified*\n")

            content.append("\n")

        write_context("".join(content))
        print("Context updated successfully.")

    except requests.RequestException as e:
        print(f"GitHub API Error: {e}")
        write_context(API_ERROR_MESSAGE)
    except Exception as e:
        print(f"Unexpected error: {e}")
        write_context(API_ERROR_MESSAGE)

def write_context(content):
    """Writes the content to the context file."""
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_context()
