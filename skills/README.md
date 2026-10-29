# Jules AI Agent Skills

This directory contains skills for working with Google Jules — an AI coding agent that autonomously implements features and fixes bugs.

---

## Skills Overview

| Skill | Package | Purpose |
|-------|---------|---------|
| **jules-cli** | `jules-cli.skill` | CLI commands with repo-specific examples |
| **jules-api** | `jules-api.skill` | REST API endpoints, authentication, SDK |
| **jules-sessions** | `jules-sessions.skill` | Analyze local session JSON files |
| **jules-workflows** | `jules-workflows.skill` | Common workflow patterns |

---

## Installation

### Letta Code

```bash
# Copy to Letta Code skills directory
cp *.skill ~/.letta/skills/
cd ~/.letta/skills
unzip jules-cli.skill
unzip jules-api.skill
unzip jules-sessions.skill
unzip jules-workflows.skill
```

### OpenCode

```bash
cp -r jules-* ~/.config/opencode/skill/
```

### Kilo (Kilocode)

```bash
cp -r jules-* ~/.kilo/skills/
```

### Vibe (Mistral)

```bash
cp -r jules-* ~/.vibe/skills/
```

---

## Quick Reference

### jules-cli — CLI Commands

```bash
jules                                          # Launch TUI
jules new "Fix the bug"                        # Create session
jules new --repo owner/repo "Task"             # Specific repo
jules new --parallel 3 "Task"                  # 3 parallel agents
jules remote list --session                    # List sessions
jules remote pull --session ID                 # Get result
jules teleport ID                              # Clone + apply
```

### jules-api — REST API

```bash
# Create session
curl -X POST "https://jules.googleapis.com/v1alpha/sessions" \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Task", "source": {"github": "owner/repo"}}'

# Get session status
curl "https://jules.googleapis.com/v1alpha/sessions/ID" \
  -H "x-goog-api-key: $JULES_API_KEY"
```

### jules-sessions — Local Analysis

```bash
# Using the included scripts
~/.letta/skills/jules-sessions/scripts/analyze_sessions.sh --status
~/.letta/skills/jules-sessions/scripts/analyze_sessions.sh --pr-links
~/.letta/skills/jules-sessions/scripts/analyze_sessions.sh --stats

# Manual queries
jq '.outputs[].pullRequest.url' jules_sessions/*_session.json
```

### jules-workflows — Patterns

```bash
# Fire and forget
jules new --repo owner/repo --auto-pr "Task"

# Interactive with approval
jules new "Task"
# API: POST /sessions/{id}:approve

# From analysis to follow-up
jules new "Continue work from PR #437"
```

---

## Scripts Included

### `analyze_sessions.sh`

Query and analyze local Jules session files.

```bash
./analyze_sessions.sh --status        # All sessions with state
./analyze_sessions.sh --pr-links       # PR URLs only
./analyze_sessions.sh --pending        # Sessions needing action
./analyze_sessions.sh --stats          # Count by status
./analyze_sessions.sh --extract-patch  # Extract git patches
./analyze_sessions.sh --by-branch NAME # Filter by branch
```

### `sync_session.sh`

Pull session data from Jules API to local JSON.

```bash
# Requires JULES_API_KEY
export JULES_API_KEY="your-key"
./sync_session.sh SESSION_ID PR_NUMBER
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `JULES_API_KEY` | Google AI Studio API key |
| `JULES_SESSIONS_DIR` | Override sessions directory (default: `./jules_sessions`) |

---

## Documentation

Each skill contains comprehensive documentation:

- **jules-cli**: Installation, quick commands, repo examples, troubleshooting
- **jules-api**: All endpoints, request/response schemas, error codes, SDK usage
- **jules-sessions**: File schema, query commands, analysis patterns
- **jules-workflows**: 8 workflow patterns, error recovery

---

## Integration with EmailIntelligence

These skills are pre-configured with examples for `MasumRab/EmailIntelligence`:

```bash
jules new --repo MasumRab/EmailIntelligence "Add API rate limiting"
jules new --repo MasumRab/EmailIntelligence --branch scientific "Optimize ML model"
```

---

## References

- [Jules Website](https://jules.google.com)
- [Jules API Docs](https://developers.google.com/jules/api)
- [Jules SDK GitHub](https://github.com/google-labs-code/jules-sdk)
- `../jules_sessions/README.md` — Local session tracking docs

---

## Updates

To update skills from the source:

```bash
# From project root
./scripts/sync_skills.sh  # If script exists

# Or manually
cp -r ~/.letta/skills/jules-* ./skills/
```

---

## jules-scheduling

Task orchestration and scheduling for complex multi-task workflows.

**Package:** `jules-scheduling.skill`

**Features:**
- Schedule JSON schema with phases, dependencies, quality gates
- Parallel execution rules (max concurrent tasks, fail modes)
- Task template with validation criteria
- Progress monitoring queries

**Usage:**
```bash
jules new --schedule jules_sessions/task_schedule.json
```

**See:** [[jules-scheduling]] skill for full reference.
