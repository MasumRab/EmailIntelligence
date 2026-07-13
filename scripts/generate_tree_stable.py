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

def get_prs_paginated():
    print("Fetching all open PRs via GraphQL...")
    query = """
    query($cursor: String) {
      repository(owner: "MasumRab", name: "EmailIntelligence") {
        pullRequests(states: OPEN, first: 100, after: $cursor) {
          pageInfo { hasNextPage endCursor }
          nodes { number title baseRefName headRefName body additions deletions }
        }
      }
    }
    """

    all_prs = []
    has_next = True
    cursor = None

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
                if e.code in [502, 504]:
                    print(f"{e.code} Bad Gateway/Timeout. Retrying in 5 seconds (Attempt {attempt+1}/{retries})...")
                    time.sleep(5)
                else:
                    raise

        if not data or "errors" in data:
            print("Failed to fetch data or GraphQL error occurred.")
            break

        page = data["data"]["repository"]["pullRequests"]
        all_prs.extend(page["nodes"])

        has_next = page["pageInfo"]["hasNextPage"]
        cursor = page["pageInfo"]["endCursor"]
        print(f"Fetched {len(all_prs)} PRs...")

    return all_prs

def build_tree():
    raw_prs = get_prs_paginated()
    pr_map = {pr['number']: pr for pr in raw_prs}
    branch_to_pr = {pr['headRefName']: pr['number'] for pr in raw_prs}
    children_map = {pr['number']: [] for pr in raw_prs}
    roots = set(pr_map.keys())

    print("Fetching commented PRs...")
    commented_raw = run_cmd('gh pr list --search \'in:comments "Blocked by PR"\' --state open --limit 500 --json number')
    commented_prs = set(pr['number'] for pr in json.loads(commented_raw)) if commented_raw else set()

    print("Mapping verifiable dependencies...")
    for pr_id, pr in pr_map.items():
        pr['blocked_by'] = set()

        base_branch = pr['baseRefName']
        if base_branch in branch_to_pr and branch_to_pr[base_branch] != pr_id:
            pr['blocked_by'].add(branch_to_pr[base_branch])

        body = pr.get('body', '')
        if body:
            matches = re.findall(r'(?i)(?:depends on|blocked by).*?#(\d+)', body)
            for match in matches:
                parent_id = int(match)
                if parent_id in pr_map:
                    pr['blocked_by'].add(parent_id)

        if pr_id in commented_prs:
            comments_raw = run_cmd(f'gh pr view {pr_id} --json comments')
            if comments_raw:
                try:
                    comments = json.loads(comments_raw).get('comments', [])
                    for c in comments:
                        cbody = c.get('body', '')
                        if "blocked by pr" in cbody.lower():
                            matches = re.findall(r'#(\d+)', cbody)
                            for match in matches:
                                parent_id = int(match)
                                if parent_id in pr_map:
                                    pr['blocked_by'].add(parent_id)
                except Exception:
                    pass

    for pr_id, pr in pr_map.items():
        pr['blocked_by'] = list(pr['blocked_by'])
        for parent_id in pr['blocked_by']:
            if parent_id in children_map:
                children_map[parent_id].append(pr_id)
                if pr_id in roots:
                    roots.remove(pr_id)

    def get_priority(pr_id):
        node = pr_map[pr_id]
        total_changes = node.get('additions', 0) + node.get('deletions', 0)
        return (total_changes > 5000, total_changes)

    sorted_roots = sorted(list(roots), key=get_priority, reverse=True)

    print("Generating nested markdown with cycle protection...")
    def render_node(node_id, indent_level=0, path=None):
        if path is None:
            path = set()

        if node_id in path:
            indent = "  " * indent_level
            return f"{indent}- [ ] ⚠️ **PR #{node_id}**: [CIRCULAR DEPENDENCY DETECTED]\n"

        node = pr_map.get(node_id)
        if not node: return ""

        current_path = path.copy()
        current_path.add(node_id)

        indent = "  " * indent_level
        title = node['title'].replace('\n', ' ').strip()

        changes = node.get('additions', 0) + node.get('deletions', 0)
        tag = " 🚨 [HIGH-VOLUME]" if changes > 5000 else ""

        out = f"{indent}- [ ] **PR #{node_id}**{tag}: {title}\n"
        children = sorted(children_map.get(node_id, []))
        for child_id in children:
            out += render_node(child_id, indent_level + 1, current_path)
        return out

    markdown_output = "# Verified Global Nested Merge Tree\n\n"
    for root in sorted_roots:
        markdown_output += render_node(root)

    with open('merge_tree_report.md', 'w') as f:
        f.write(markdown_output)

    with open('/tmp/merge_tree_state.json', 'w') as f:
        json.dump(raw_prs, f, indent=2)

if __name__ == '__main__':
    build_tree()
    print("SUCCESS: merge_tree_report.md and /tmp/merge_tree_state.json generated.")
