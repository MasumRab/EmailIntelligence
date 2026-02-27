# `ck` (Seek) - Quick Reference Card

**Drop-in grep replacement with semantic search**

---

## Quick Start

### Basic Search (grep-compatible)

```bash
# Simple search (no index needed)
ck "SecurityValidator" src/

# Case-insensitive
ck -i "todo" .

# Recursive
ck -r "import" .

# Line numbers
ck -n "TODO" file.py
```

---

## Semantic Search (Game Changer)

```bash
# Find by meaning (auto-indexes)
ck --sem "error handling" src/

# Limit results
ck --sem "authentication" --limit 5

# Higher precision
ck --sem "auth" --threshold 0.8

# Show scores
ck --sem "security" --scores
```

**Finds:** Related concepts, not just keywords

---

## Hybrid Search (Best Default)

```bash
# Combine regex + semantic
ck --hybrid "async git operations" src/

# With filtering
ck --hybrid "bug" --limit 10
ck --hybrid "error" --threshold 0.02
```

**Best for:** Most production searches

---

## Lexical Search (BM25)

```bash
# Full-text search with ranking
ck --lex "user authentication token" src/
```

**Better than:** Regex for multi-word phrases

---

## Index Management

```bash
# Check status
ck --status .

# Detailed status
ck --status-verbose .

# Clean orphans
ck --clean-orphans .

# Remove index
ck --clean .

# Switch model
ck --switch-model nomic-v1.5

# Add file
ck --add file.rs

# Pre-build (for CI)
ck --index .
```

---

## Output Options

```bash
# Context lines
ck -C 2 "error" src/        # 2 lines context
ck -A 3 "TODO" src/         # 3 lines after
ck -B 1 "FIXME" src/        # 1 line before

# JSON (for tools)
ck --json --sem "bug" src/

# JSONL (for AI agents)
ck --jsonl --sem "error" src/
ck --jsonl --topk 5 "func"
```

---

## Advanced Features

```bash
# MCP server (AI integration)
ck --serve

# Reranking (better relevance)
ck --sem "auth" --rerank
ck --sem "login" --rerank-model bge

# Different models
ck --index --model nomic-v1.5
ck --index --model jina-code
```

---

## grep → ck Cheat Sheet

| grep | ck | Notes |
|------|-----|-------|
| `grep "pat" file` | `ck "pat" file` | Same |
| `grep -i "pat"` | `ck -i "pat"` | Same |
| `grep -r "pat" dir` | `ck -r "pat" dir` | Same |
| `grep -n "pat"` | `ck -n "pat"` | Same |
| `grep -C 3 "pat"` | `ck -C 3 "pat"` | Same |
| `grep -A 2 "pat"` | `ck -A 2 "pat"` | Same |
| `grep -B 2 "pat"` | `ck -B 2 "pat"` | Same |
| `grep -w "pat"` | `ck -w "pat"` | Same |
| `grep -F "pat"` | `ck -F "pat"` | Same |
| `grep -v "pat"` | `ck --invert "pat"` | |
| `grep -c "pat"` | `ck --count "pat"` | |
| `grep -l "pat"` | `ck --files "pat"` | |
| (none) | `ck --sem "concept"` | **NEW** |
| (none) | `ck --hybrid "concept"` | **NEW** |
| (none) | `ck --lex "phrase"` | **NEW** |

---

## When to Use Each

| Search Type | Command | Best For |
|-------------|---------|----------|
| **Exact string** | `ck "pattern"` | Finding specific text |
| **Regex** | `ck -r "fn.*main"` | Pattern matching |
| **Concept** | `ck --sem "error handling"` | Exploration, discovery |
| **Multi-concept** | `ck --hybrid "async git"` | Most searches |
| **Phrase** | `ck --lex "user auth token"` | Better than regex |

---

## Pro Tips

### 1. Default to Hybrid

```bash
# Start here for most searches
ck --hybrid "your query" src/
```

### 2. Tune Thresholds

```bash
# Too many results → increase threshold
ck --sem "auth" --threshold 0.8

# Too few → decrease threshold
ck --sem "auth" --threshold 0.4
```

### 3. Use for Code Review

```bash
# Find all security code
ck --hybrid "security authentication" src/

# Find error handling
ck --sem "error handling retry" src/
```

### 4. Explore Codebases

```bash
# Learn how X works
ck --sem "authentication flow" src/
ck --sem "request handling" src/
```

### 5. Find Anti-Patterns

```bash
# Blocking async code
ck --sem "blocking subprocess async" src/

# Memory leaks
ck --sem "memory leak" src/
```

---

## Performance

| Mode | Speed | Index |
|------|-------|-------|
| **Regex** | ⚡ Instant | ❌ No |
| **Lexical** | ⚡ Fast (0.1-0.5s) | ✅ Yes |
| **Semantic** | 🐌 Medium (0.5-2s) | ✅ Yes |
| **Hybrid** | 🐌 Medium (0.5-2s) | ✅ Yes |

**Index:** One-time build (2-5 min), incremental updates (seconds)

---

## Common Workflows

### Code Review

```bash
# Find security-related code
ck --hybrid "security auth" src/

# Find error handling
ck --sem "error handling" src/
```

### Debugging

```bash
# Find related code
ck --sem "null check validation" src/

# Find usages
ck --hybrid "database connection" src/
```

### Refactoring

```bash
# Find all usages of concept
ck --sem "logging" src/

# Find potential issues
ck --sem "race condition" src/
```

### Learning

```bash
# Explore by concept
ck --sem "how auth works" src/
ck --sem "request flow" src/
```

---

## AI Agent Integration

```bash
# Start MCP server
ck --serve

# Use with:
# - Claude Desktop
# - Cursor
# - Any MCP client

# Provides tools:
# - semantic_search
# - regex_search
# - hybrid_search
# - index_status
# - reindex
# - health_check
```

---

## Troubleshooting

### No Results?

```bash
# Lower threshold
ck --sem "query" --threshold 0.4

# Increase limit
ck --sem "query" --limit 50

# Try hybrid instead
ck --hybrid "query"
```

### Too Many Results?

```bash
# Increase threshold
ck --sem "query" --threshold 0.8

# Decrease limit
ck --sem "query" --limit 5
```

### Index Issues?

```bash
# Check status
ck --status .

# Rebuild
ck --clean . && ck --index .

# Switch model
ck --switch-model nomic-v1.5
```

---

## Resources

- **Help:** `ck --help`
- **GitHub:** https://github.com/ck-tool/ck
- **Models:** BAAI/bge-small (default), nomic-v1.5, jina-code

---

**Bottom Line:** Use `ck --hybrid` as your default search. It's like grep but understands meaning.
