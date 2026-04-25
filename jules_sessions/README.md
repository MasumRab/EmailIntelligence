# Jules Sessions — AI Agent Session Tracking

This directory contains session data from [Google Jules](https://jules.google.com), an AI coding agent that autonomously implements features and fixes bugs.

---

## Directory Structure

```
jules_sessions/
├── pr437_session.json      # Jules session metadata for PR #437
├── pr437_activities.json   # Step-by-step actions for PR #437
├── pr464_session.json      # Session for PR #464
├── pr464_activities.json   # Activities for PR #464
└── ... (one pair per PR)
```

---

## File Types

### Session Files (`pr*_session.json`)

Contains complete session metadata:

| Field | Description |
|-------|-------------|
| `id` | Jules session ID |
| `title` | Session title (e.g., "Bolt: Performance Optimization Agent") |
| `createTime` | ISO timestamp when session started |
| `updateTime` | ISO timestamp of last update |
| `state` | Session state (`COMPLETED`, `FAILED`, `RUNNING`) |
| `sourceContext.source` | GitHub repo path |
| `sourceContext.githubRepoContext.startingBranch` | Branch Jules worked on |
| `prompt` | Full system prompt given to Jules |
| `url` | Link to Jules session dashboard |
| `outputs[]` | Array of outputs (changes, PRs) |
| `outputs[].changeSet.gitPatch` | The actual diff (unified format) |
| `outputs[].pullRequest` | PR details (URL, title, description, refs) |

### Activities Files (`pr*_activities.json`)

Contains step-by-step actions:

| Field | Description |
|-------|-------------|
| Tool calls | File reads, writes, bash commands |
| Reasoning | Agent's thought process |
| Iterations | Number of steps taken |
| Errors | Any failures encountered |

---

## How Files Are Created

### Automatic Creation (Jules Native)

When Jules completes a session, it:
1. Creates a PR on GitHub
2. Generates session metadata (accessible via Jules dashboard)

To capture these files locally:

```bash
# After Jules completes a session, export via Jules CLI or API
# (Method varies based on Jules API availability)

# Example: Manual export from Jules dashboard
# 1. Open https://jules.google.com/session/<session-id>
# 2. Export session data as JSON
# 3. Save to this directory
```

### Manual Creation

If you need to manually log a Jules session:

```python
# scripts/capture_jules_session.py

import json
from datetime import datetime
from pathlib import Path

def create_session_manifest(pr_number: int, session_id: str, 
                            title: str, branch: str, prompt: str,
                            patch: str, pr_url: str):
    """Create session and activities files for a Jules run."""
    
    session = {
        "name": f"sessions/{session_id}",
        "title": title,
        "createTime": datetime.utcnow().isoformat() + "Z",
        "state": "COMPLETED",
        "sourceContext": {
            "source": "sources/github/MasumRab/EmailIntelligence",
            "githubRepoContext": {"startingBranch": branch}
        },
        "prompt": prompt,
        "url": f"https://jules.google.com/session/{session_id}",
        "id": session_id,
        "outputs": [{
            "changeSet": {
                "source": "sources/github/MasumRab/EmailIntelligence",
                "gitPatch": patch
            },
            "pullRequest": {
                "url": pr_url,
                "title": title,
                "baseRef": branch
            }
        }]
    }
    
    # Write session file
    session_path = Path("jules_sessions") / f"pr{pr_number}_session.json"
    session_path.write_text(json.dumps(session, indent=2))
    print(f"Created: {session_path}")

# Usage:
# create_session_manifest(
#     pr_number=437,
#     session_id="15863163327149061241",
#     title="⚡ Bolt: Optimize Database Search",
#     branch="scientific",
#     prompt="...",
#     patch="diff --git a/...",
#     pr_url="https://github.com/MasumRab/EmailIntelligence/pull/437"
# )
```

---

## Updating Session Files

### After PR Merge

When a PR is merged, update the session file:

```bash
# Add merge information to session
jq '.outputs[0].pullRequest.mergedAt = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
   jules_sessions/pr437_session.json > tmp.json && mv tmp.json jules_sessions/pr437_session.json

# Add merge commit
jq '.outputs[0].pullRequest.mergeCommit = "abc1234"' \
   jules_sessions/pr437_session.json > tmp.json && mv tmp.json jules_sessions/pr437_session.json
```

### Adding Review Notes

```bash
# Add human review notes
jq '.humanReview = {"reviewer": "@MasumRab", "approved": true, "notes": "Good optimization"}' \
   jules_sessions/pr437_session.json > tmp.json && mv tmp.json jules_sessions/pr437_session.json
```

---

## Querying Session Data

### Find All Completed Sessions

```bash
# List completed sessions
jq -r 'select(.state == "COMPLETED") | "\(.id) \(.title)"' jules_sessions/*_session.json
```

### Extract All PR URLs

```bash
# Get all PR links
jq -r '.outputs[]?.pullRequest?.url // empty' jules_sessions/*_session.json
```

### Find Sessions by Branch

```bash
# Sessions on 'scientific' branch
jq -r 'select(.sourceContext.githubRepoContext.startingBranch == "scientific") | .title' \
    jules_sessions/*_session.json
```

### Session Statistics

```bash
# Count by state
jq -s 'group_by(.state) | map({state: .[0].state, count: length})' \
    jules_sessions/*_session.json
```

---

## Data Retention

| Data Type | Retention | Reason |
|-----------|-----------|--------|
| Session metadata | Permanent | Audit trail |
| Activities logs | Permanent | Behavioral analysis |
| Git patches | Permanent | Code history |
| PR descriptions | Permanent | Documentation |

---

## Size Management

Sessions can be large (pr571 = 171 MB total). To reduce storage:

```bash
# Compress old sessions
gzip jules_sessions/pr*_activities.json

# Or extract just key metrics
jq '{id, title, state, pr: .outputs[0].pullRequest.url}' \
   jules_sessions/pr571_session.json > jules_sessions/pr571_summary.json
```

---

## Privacy & Security

⚠️ **Sensitive Data**: Session files may contain:
- Environment variable names
- Internal URLs
- Code snippets with business logic

**Do NOT commit if sessions contain:**
- API keys or secrets
- Production credentials
- Customer data

---

## Future Extensions

### Planned Features

- [ ] Automated session capture via Jules webhook
- [ ] Session comparison tool (diff between Jules runs)
- [ ] Success rate analytics by prompt type
- [ ] Integration with CI/CD for automated reviews
- [ ] Prompt optimization based on session outcomes

### Contributing

When adding new session capture methods:
1. Follow the schema above
2. Include all required fields
3. Add timestamp in ISO 8601 format
4. Validate JSON before committing

---

## References

- [Jules Documentation](https://jules.google.com/docs)
- [Jules Dashboard](https://jules.google.com/)
- Session files schema: see `pr437_session.json` as example
