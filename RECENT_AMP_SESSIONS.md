# Most Recent Amp Sessions

**Retrieved:** 2026-02-26 02:00  
**Source:** `~/.local/share/amp/threads/`  
**Total Indexed:** 294 Amp sessions

---

## Top 10 Most Recent Amp Sessions

| # | Session ID | Modified | Size | Topic (from filename) |
|---|------------|----------|------|----------------------|
| **1** | `T-019c9548` | Feb 26 01:55 | 330 KB | Continue cross-task deduplication cleanup |
| **2** | `T-019c7e1c` | Feb 26 01:51 | 1.5 MB | Large session (likely complex task) |
| **3** | `T-019c935d` | Feb 25 20:40 | 655 KB | Evening session |
| **4** | `T-019c8d82` | Feb 24 23:44 | 358 KB | Late night session |
| **5** | `T-019c8973` | Feb 23 18:47 | 196 KB | Evening session |
| **6** | `T-019c85ef` | Feb 23 02:20 | 5 KB | Short session |
| **7** | `T-019c85cb` | Feb 23 01:40 | 5 KB | Short session |
| **8** | `T-019c85bf` | Feb 23 01:27 | 4 KB | Short session |
| **9** | `T-019c78ff` | Feb 21 13:52 | 396 KB | Afternoon session |
| **10** | `T-019c78fd` | Feb 20 14:04 | 438 KB | Afternoon session |

---

## Session Details (Most Recent)

### Session 1: T-019c9548 (Most Recent)

**Modified:** Feb 26 01:55  
**Size:** 330 KB (329,899 bytes)  
**Messages:** 21  
**Title:** "Continue cross-task deduplication cleanup"

**View with cass:**
```bash
cass view ~/.local/share/amp/threads/T-019c9548-f290-724a-9be0-52b00db7169e.json -n 1
```

---

### Session 2: T-019c7e1c (Largest Recent)

**Modified:** Feb 26 01:51  
**Size:** 1.5 MB (1,500,511 bytes)  
**Likely:** Complex multi-step task with extensive conversation

---

## How to Access Amp Sessions

### Method 1: Direct File Access

```bash
# List all sessions by date
ls -lt ~/.local/share/amp/threads/*.json

# View specific session
cat ~/.local/share/amp/threads/T-019c9548-f290-724a-9be0-52b00db7169e.json | jq .
```

---

### Method 2: Using Cass

```bash
# Search Amp sessions
cass search "your query" --agent amp --robot

# View session at line
cass view ~/.local/share/amp/threads/T-019c9548-....json -n 42

# Get session stats
cass stats --json | jq '.by_agent[] | select(.agent == "amp")'
```

---

### Method 3: Using Cass Search

```bash
# Search for specific topic in Amp sessions
cass search "branch alignment" --agent amp --week --robot

# Get all Amp sessions from today
cass search "" --agent amp --today --robot --limit 50
```

---

## Session Statistics

### By Agent (All Indexed Sessions)

```json
{
  "amp": 294,
  "claude_code": 408,
  "gemini": 342,
  "opencode": 196,
  "codex": 5
}
```

### Recent Activity (Last 7 Days)

Based on file modification times:
- **Feb 26:** 2 sessions (most active)
- **Feb 25:** 1 session
- **Feb 24:** 1 session
- **Feb 23:** 4 sessions
- **Feb 21:** 1 session
- **Feb 20:** 1 session

---

## Finding Specific Sessions

### By Topic

```bash
# Search for branch alignment discussions
cass search "branch alignment" --agent amp --robot

# Search for task-related sessions
cass search "taskmaster" --agent amp --robot
```

### By Date Range

```bash
# Today's sessions
cass search "" --agent amp --today --robot

# This week
cass search "" --agent amp --week --robot --limit 100

# Specific date range
cass search "" --agent amp --since 2026-02-20 --until 2026-02-26 --robot
```

### By Size (Complexity)

```bash
# Large sessions (> 500KB) - likely complex tasks
ls -lhS ~/.local/share/amp/threads/*.json | head -10

# Small sessions (< 10KB) - likely quick questions
ls -lh ~/.local/share/amp/threads/*.json | awk '$5 < 10000'
```

---

## Session File Structure

Amp session files are JSON with this structure:

```json
{
  "v": 2349,
  "id": "T-019c9548-f290-724a-9be0-52b00db7169e",
  "created": 1772031111833,
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "..."
    },
    {
      "role": "assistant",
      "content": "...",
      "timestamp": "..."
    }
  ]
}
```

---

## Tips for Finding Sessions

### 1. Use Cass Search (Recommended)

```bash
# Best for finding specific topics
cass search "your query" --agent amp --robot
```

### 2. Sort by File Size

```bash
# Large sessions = complex tasks
ls -lhS ~/.local/share/amp/threads/*.json | head -5
```

### 3. Sort by Modification Time

```bash
# Most recent first
ls -lt ~/.local/share/amp/threads/*.json | head -10
```

### 4. Search Session Content

```bash
# Grep through all sessions
grep -l "branch alignment" ~/.local/share/amp/threads/*.json
```

---

## Next Steps

### To View a Specific Session:

```bash
# Replace SESSION_ID with the actual ID
cass view ~/.local/share/amp/threads/SESSION_ID.json -n 1

# Or with context
cass view ~/.local/share/amp/threads/SESSION_ID.json -n 42 -C 10
```

### To Search Across All Sessions:

```bash
# Find all sessions about a topic
cass search "branch alignment" --agent amp --robot --limit 20

# Get session list
cass search "" --agent amp --week --fields minimal --robot
```

---

**Last Updated:** 2026-02-26 02:00  
**Total Amp Sessions:** 294  
**Most Recent:** T-019c9548 (Feb 26 01:55)
