# Qwen MCP Server Setup Guide with `ck`

**Last Updated:** 2026-02-20  
**Purpose:** Configure Qwen Code to use `ck` semantic search via MCP protocol

---

## Overview

This guide shows how to integrate the `ck` (seek) semantic search tool with Qwen Code using the Model Context Protocol (MCP). This enables Qwen agents to:

- 🔍 Search code by **meaning** (not just keywords)
- 🎯 Find related concepts and patterns
- ⚡ Use hybrid search (regex + semantic)
- 🤖 Get AI-powered code navigation

---

## Prerequisites

### 1. Verify `ck` Installation

```bash
# Check if ck is installed
ck --version

# If not installed, install from:
# https://github.com/BeaconBay/ck
```

**Current Status:** ✅ Installed at `/home/masum/.cargo/bin/ck`

### 2. Verify Qwen Code MCP Support

Qwen Code supports MCP integration via configuration files.

---

## Setup Options

### Option 1: Project-Level Configuration (Recommended)

Configure MCP servers for this specific project.

#### Step 1: Create `.mcp.json`

Create file at project root: `/home/masum/github/PR/.taskmaster/.mcp.json`

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": ["--serve"],
      "cwd": "/home/masum/github/PR/.taskmaster"
    }
  }
}
```

**Configuration Options:**

| Field | Purpose | Example |
|-------|---------|---------|
| `command` | Executable to run | `"ck"` |
| `args` | Command arguments | `["--serve"]` |
| `cwd` | Working directory | `"/path/to/project"` |
| `env` | Environment variables | `{"KEY": "value"}` |

#### Step 2: Restart Qwen Code

After creating the config file, restart Qwen Code to load the MCP server.

---

### Option 2: Global Qwen Configuration

Configure MCP servers globally for all Qwen sessions.

#### Step 1: Locate Qwen Config

```bash
# Qwen global config location
~/.qwen/settings.json
```

#### Step 2: Add MCP Server Configuration

Edit `~/.qwen/settings.json`:

```json
{
  "mcp": {
    "servers": {
      "ck": {
        "enabled": true,
        "command": "ck",
        "args": ["--serve"],
        "cwd": "/home/masum/github/PR/.taskmaster"
      },
      "task-master-ai": {
        "enabled": true,
        "command": "npx",
        "args": ["-y", "task-master-ai"],
        "env": {
          "TASK_MASTER_TOOLS": "core"
        }
      }
    }
  }
}
```

#### Step 3: Reload Qwen

```bash
# Reload Qwen configuration
# (Restart Qwen Code or use reload command if available)
```

---

### Option 3: Manual MCP Server Start

Start the MCP server manually and connect Qwen to it.

#### Step 1: Start ck MCP Server

```bash
cd /home/masum/github/PR/.taskmaster
ck --serve
```

**Output:**
```
MCP server started on localhost:PORT
Available tools: semantic_search, regex_search, hybrid_search, index_status, reindex, health_check
```

#### Step 2: Connect Qwen to Running Server

Configure Qwen to connect to the running MCP server via socket or HTTP.

---

## MCP Server Configuration Details

### ck MCP Server

**Command:** `ck --serve`

**Available Tools:**

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `semantic_search` | Find code by meaning | "error handling patterns" |
| `regex_search` | Classic grep-style search | "fn.*main" |
| `hybrid_search` | Combine regex + semantic | "async database operations" |
| `index_status` | Check index health | View indexed files count |
| `reindex` | Rebuild index | After major code changes |
| `health_check` | Verify server status | Connection test |

**Configuration:**

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": [
        "--serve",
        "--model", "bge-small",
        "--threshold", "0.6",
        "--limit", "10"
      ],
      "cwd": "/home/masum/github/PR/.taskmaster",
      "env": {}
    }
  }
}
```

**Advanced Options:**

| Argument | Purpose | Default |
|----------|---------|---------|
| `--model` | Embedding model | `bge-small` |
| `--threshold` | Min similarity score | `0.6` |
| `--limit` | Max results | `10` |
| `--rerank` | Enable reranking | `false` |

---

### Taskmaster MCP Server (Optional)

If you also want Taskmaster AI integration:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "TASK_MASTER_TOOLS": "core",
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Tool Tiers:**

| Tier | Tools | Purpose |
|------|-------|---------|
| `core` | 7 | Basic task management |
| `standard` | 14 | + Analysis & complexity |
| `all` | 44+ | Full feature set |

---

## Complete Configuration Example

### Combined Setup (ck + Taskmaster)

Create `.mcp.json` at project root:

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": ["--serve"],
      "cwd": "/home/masum/github/PR/.taskmaster"
    },
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "TASK_MASTER_TOOLS": "core",
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PERPLEXITY_API_KEY": "pplx-..."
      }
    }
  }
}
```

**Benefits:**
- 🔍 `ck` for semantic code search
- 📋 `task-master-ai` for task management
- 🤖 Both available to Qwen agents

---

## Testing the Setup

### Test 1: Verify MCP Server Connection

```bash
# Start ck server
cd /home/masum/github/PR/.taskmaster
ck --serve
```

**Expected Output:**
```
MCP server started
Index status: 758 files, 15330 chunks
Model: BAAI/bge-small-en-v1.5
```

### Test 2: Check Index Status

In Qwen, ask:
```
Check the ck index status
```

**Expected Response:**
```
Index location: /home/masum/github/PR/.taskmaster/.ck/
Files indexed: 758
Total chunks: 15330
Model: BAAI/bge-small-en-v1.5 (384 dims)
```

### Test 3: Semantic Search

In Qwen, ask:
```
Find security validation code in src/
```

**Expected Response:**
```
Found 10 relevant results:

1. src/core/security.py: SecurityValidator class
2. src/validation/validator.py: Validator module
3. src/analysis/constitutional/requirement_checker.py: SecurityChecker
...
```

### Test 4: Hybrid Search

In Qwen, ask:
```
Search for async git operations using hybrid search
```

**Expected Response:**
```
Hybrid search results (regex + semantic):

1. src/git/repository.py: async def run_command()
2. src/git/repository.py: async def has_uncommitted_changes()
3. src/core/git_operations.py: GitOperations class
...
```

---

## Usage Examples

### Example 1: Code Exploration

**User:** "Show me how error handling works in this codebase"

**Qwen with ck MCP:**
```
Searching semantically for "error handling patterns"...

Found 8 relevant results:

1. src/core/exceptions.py (Score: 0.92)
   - EmailIntelligenceException base class
   - GitOperationError, ValidationError subclasses

2. src/resolution/auto_resolver.py (Score: 0.88)
   - try/except blocks in _resolve_conflict()
   - Error logging and recovery

3. src/git/repository.py (Score: 0.85)
   - Exception handling in run_command()
   - Timeout error handling
...
```

---

### Example 2: Finding Anti-Patterns

**User:** "Find blocking code in async methods"

**Qwen with ck MCP:**
```
Searching for "blocking subprocess async"...

Found potential issue:

src/git/repository.py:30-65
async def run_command(self, cmd: List[str], cwd: Optional[Path] = None):
    result = subprocess.run(  # ← Blocking call!
        cmd,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

Recommendation: Replace subprocess.run() with asyncio.create_subprocess_exec()
```

---

### Example 3: Code Review

**User:** "Review security-related code before merge"

**Qwen with ck MCP:**
```
Searching for "security authentication validation"...

Security-related code found:

1. src/core/security.py
   - SecurityValidator.validate_branch_name()
   - SecurityValidator.is_safe_path()
   - Directory traversal prevention

2. src/core/config.py
   - API key validation
   - Secret management

3. src/validation/validator.py
   - Input validation
   - Type checking

No critical security issues detected.
```

---

## Troubleshooting

### Issue 1: MCP Server Not Starting

**Symptoms:** Qwen reports "MCP server connection failed"

**Solutions:**
```bash
# 1. Verify ck is installed
ck --version

# 2. Check if port is available
lsof -i :PORT  # Replace PORT with actual port

# 3. Start server manually to test
ck --serve

# 4. Check .mcp.json syntax
cat .mcp.json | jq .
```

---

### Issue 2: Index Not Found

**Symptoms:** "Index not found" or "0 files indexed"

**Solutions:**
```bash
# 1. Check index location
ck --status .

# 2. Build index if missing
ck --index .

# 3. Verify index directory exists
ls -la .ck/

# 4. Rebuild index
ck --clean . && ck --index .
```

---

### Issue 3: Slow Search Performance

**Symptoms:** Semantic search takes >5 seconds

**Solutions:**
```bash
# 1. Check index size
ck --status-verbose .

# 2. Use smaller model
ck --serve --model bge-small

# 3. Reduce result limit
ck --sem "query" --limit 5

# 4. Increase threshold for fewer results
ck --sem "query" --threshold 0.8
```

---

### Issue 4: No Results Returned

**Symptoms:** Search returns 0 results

**Solutions:**
```bash
# 1. Lower threshold
ck --sem "query" --threshold 0.4

# 2. Increase limit
ck --sem "query" --limit 50

# 3. Try hybrid search instead
ck --hybrid "query"

# 4. Verify files are indexed
ck --status .
```

---

## Best Practices

### 1. Start with Hybrid Search

```json
{
  "default_search_mode": "hybrid",
  "threshold": 0.6,
  "limit": 10
}
```

**Why:** Best balance of precision and recall.

### 2. Configure Appropriate Limits

```json
{
  "args": [
    "--serve",
    "--limit", "10",
    "--threshold", "0.6"
  ]
}
```

**Why:** Prevents overwhelming responses.

### 3. Use Project-Specific Config

```json
{
  "mcpServers": {
    "ck": {
      "cwd": "/path/to/this/project"
    }
  }
}
```

**Why:** Each project has different codebase.

### 4. Monitor Index Health

```bash
# Check weekly
ck --status .

# Clean orphans monthly
ck --clean-orphans .
```

---

## Security Considerations

### API Keys

**Never hardcode API keys in `.mcp.json`:**

❌ Bad:
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-actual-key-here"
  }
}
```

✅ Good:
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
  }
}
```

**Use environment variables or `.env` files:**

```bash
# .env file (gitignored)
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...
```

### Local Execution

**ck MCP server runs 100% locally:**
- ✅ No external API calls
- ✅ No telemetry
- ✅ No data leaves your machine
- ✅ Index stored locally in `.ck/`

---

## Advanced Configuration

### Custom Embedding Model

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": [
        "--serve",
        "--model", "nomic-v1.5"
      ]
    }
  }
}
```

**Available Models:**
- `bge-small` (default, fast, 384 dims)
- `bge-large` (better quality, slower)
- `nomic-v1.5` (8k context, highest quality)
- `jina-code` (code-specialized)

### Enable Reranking

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": [
        "--serve",
        "--rerank",
        "--rerank-model", "bge-reranker"
      ]
    }
  }
}
```

**Benefits:** Better relevance ranking for results.

---

## Resources

- **ck Documentation:** https://beaconbay.github.io/ck/
- **ck GitHub:** https://github.com/BeaconBay/ck
- **MCP Protocol:** https://modelcontextprotocol.io/
- **Qwen Code:** See `.qwen/settings.json` for configuration

---

## Quick Reference

### Start MCP Server
```bash
ck --serve
```

### Configuration File
```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": ["--serve"],
      "cwd": "/path/to/project"
    }
  }
}
```

### Test Connection
```bash
ck --status .
ck --sem "test query" src/
```

### Common Commands
```bash
# Check status
ck --status .

# Rebuild index
ck --clean . && ck --index .

# Search
ck --sem "query" src/
ck --hybrid "query" src/
```

---

**Next Steps:**
1. Create `.mcp.json` at project root
2. Restart Qwen Code
3. Test with: "Search for security code using semantic search"
4. Enjoy AI-powered code navigation! 🚀
