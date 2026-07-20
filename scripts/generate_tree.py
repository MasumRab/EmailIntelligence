import json
import subprocess
import re
import time

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_prs():
    print("Fetching PR metadata via gh cli...")
    retries = 10
    for attempt in range(retries):
        result = subprocess.run(
            ['gh', 'pr', 'list', '--state', 'open', '--limit', '1000',
             '--json', 'number,title,baseRefName,headRefName,body,additions,deletions'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        elif "502" in result.stderr or "Bad Gateway" in result.stderr:
            print(f"502 Bad Gateway. Retrying in 5 seconds (Attempt {attempt+1}/{retries})...")
            time.sleep(5)
        else:
            print(f"Error fetching PRs: {result.stderr}")
            result.check_returncode()

    raise Exception("Failed to fetch PRs after retries.")

def build_tree():
    raw_prs = get_prs()
    pr_map = {pr['number']: pr for pr in raw_prs}
    branch_to_pr = {pr['headRefName']: pr['number'] for pr in raw_prs}
    children_map = {pr['number']: [] for pr in raw_prs}
    roots = set(pr_map.keys())

    # Fetch comments where we left directives
    print("Fetching commented PRs...")
    commented_raw = run_cmd('gh pr list --search \'in:comments "Blocked by PR"\' --state open --limit 500 --json number')
    commented_prs = set(pr['number'] for pr in json.loads(commented_raw)) if commented_raw else set()

    print("Mapping verifiable dependencies...")
    for pr_id, pr in pr_map.items():
        pr['blocked_by'] = set()

        # 1. VERIFIED GIT NESTING
        base_branch = pr['baseRefName']
        if base_branch in branch_to_pr and branch_to_pr[base_branch] != pr_id:
            pr['blocked_by'].add(branch_to_pr[base_branch])

        # 2. VERIFIED TEXT NESTING in Body
        body = pr.get('body', '')
        if body:
            matches = re.findall(r'(?i)(?:depends on|blocked by).*?#(\d+)', body)
            for match in matches:
                parent_id = int(match)
                if parent_id in pr_map:
                    pr['blocked_by'].add(parent_id)

        # 3. VERIFIED TEXT NESTING in Comments
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

    # Build parent/child map
    for pr_id, pr in pr_map.items():
        pr['blocked_by'] = list(pr['blocked_by'])
        for parent_id in pr['blocked_by']:
            if parent_id in children_map:
                children_map[parent_id].append(pr_id)
                if pr_id in roots:
                    roots.remove(pr_id)

    # 3. PRIORITY SORTING: High-Volume roots first
    def get_priority(pr_id):
        node = pr_map[pr_id]
        total_changes = node.get('additions', 0) + node.get('deletions', 0)
        # Sort key: True if > 5000 changes (High Volume), then by total changes descending
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
