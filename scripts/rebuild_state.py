import os
import json
import urllib.request
import re
import subprocess
import time

token = os.environ.get("GITHUB_TOKEN")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
url = "https://api.github.com/graphql"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

print("Fetching commented PRs...")
commented_raw = run_cmd('gh pr list --search "in:comments @jules" --state open --limit 500 --json number')
commented_prs = set(pr['number'] for pr in json.loads(commented_raw)) if commented_raw else set()

query = """
query($cursor: String) {
  repository(owner: "MasumRab", name: "EmailIntelligence") {
    pullRequests(states: OPEN, first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { number title additions deletions }
    }
  }
}
"""

all_prs = []
has_next = True
cursor = None

print("Fetching all open PRs via GraphQL...")
while has_next:
    variables = {"cursor": cursor} if cursor else {}
    req_body = json.dumps({"query": query, "variables": variables}).encode('utf-8')
    req = urllib.request.Request(url, data=req_body, headers=headers, method='POST')

    retries = 10
    data = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                break
        except urllib.error.HTTPError as e:
            if e.code == 502:
                print(f"502 Bad Gateway. Retrying in 5 seconds (Attempt {attempt+1}/{retries})...")
                time.sleep(5)
            else:
                raise

    if not data:
        print("Failed to fetch data after retries.")
        break

    if "errors" in data:
        print("GraphQL Error:", data["errors"])
        break

    page = data["data"]["repository"]["pullRequests"]
    all_prs.extend(page["nodes"])

    has_next = page["pageInfo"]["hasNextPage"]
    cursor = page["pageInfo"]["endCursor"]
    print(f"Fetched {len(all_prs)} PRs...")

state = []
print(f"Processing {len(all_prs)} PRs for dependencies...")
for pr in all_prs:
    num = pr['number']
    additions = pr.get('additions', 0)
    deletions = pr.get('deletions', 0)

    category = "Feature"
    if additions > 5000 or deletions > 5000:
        category = "High-Volume"
    else:
        title = pr['title'].lower()
        if any(x in title for x in ['refactor', 'config', 'schema', 'ci', 'bump', 'sentinel', 'fix', 'chore', 'docs']):
            category = "Tooling/Schema"

    blocked_by = []
    if num in commented_prs:
        comments_raw = run_cmd(f'gh pr view {num} --json comments')
        if comments_raw:
            try:
                comments = json.loads(comments_raw).get('comments', [])
                for c in comments:
                    body = c.get('body', '')
                    if "@jules Blocked by PR" in body:
                        matches = re.findall(r'#(\d+)', body)
                        blocked_by.extend([int(m) for m in matches])
            except Exception:
                pass

    state.append({
        "pr": num,
        "title": pr['title'],
        "type": category,
        "blocked_by": list(set(blocked_by))
    })

with open('/tmp/merge_tree_state.json', 'w') as f:
    json.dump(state, f, indent=2)

print(f"Successfully rebuilt JSON state for {len(state)} PRs.")
