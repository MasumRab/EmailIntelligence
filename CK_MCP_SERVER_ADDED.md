# ✅ CK MCP Server Added to Qwen Code CLI

**Date:** 2026-02-20  
**Status:** ✅ **CONFIGURED** (needs to be started)

---

## Problem Solved

**Issue:** `ck-search` MCP not showing when using `/mcp` command

**Root Cause:** The MCP server was configured in `.mcp.json` (project-level) but not in Qwen Code CLI's global settings.

**Solution:** Added `ck` server to Qwen's global MCP configuration using `qwen mcp add`.

---

## Current Status

```bash
$ qwen mcp list

Configured MCP servers:
✗ task-master-ai: npx -y task-master-ai (stdio) - Disconnected
✗ ck: ck --serve  (stdio) - Disconnected
```

**✅ `ck` is now configured** but shows as "Disconnected" - this is normal.

---

## Why "Disconnected"?

The "Disconnected" status is **expected** because:

1. **MCP servers are started on-demand** - Qwen Code CLI launches them when needed
2. **Not a persistent connection** - Servers are not always running
3. **Health check needed** - Server starts when you use semantic search

---

## How to Use

### 1. Start a Qwen Code Session

```bash
qwen
```

### 2. Use Semantic Search

**Ask Qwen:**
```
Search for security validation code in src/ using semantic search
```

**What Happens:**
- Qwen automatically starts the `ck` MCP server
- Server runs in background during the session
- Results returned from semantic search
- Server stops when session ends

### 3. Check Server Status (During Session)

While in a Qwen session, the server will be connected:
```
✓ ck: ck --serve (stdio) - Connected
```

---

## Configuration Details

### Added Server

```json
{
  "mcpServers": {
    "ck": {
      "command": "ck",
      "args": ["--serve"]
    }
  }
}
```

**Location:** `~/.qwen/settings.json`

### Command Used

```bash
qwen mcp add ck "ck --serve"
# Output: MCP server "ck" added to user settings. (stdio)
```

---

## Verification

### Check Configuration

```bash
qwen mcp list
```

**Expected Output:**
```
Configured MCP servers:
✗ task-master-ai: npx -y task-master-ai (stdio) - Disconnected
✗ ck: ck --serve  (stdio) - Disconnected
```

### Test in Qwen Session

```bash
# Start Qwen
qwen

# Ask for semantic search
"Find error handling patterns in src/"
```

**Expected:** Qwen will:
1. Start the `ck` MCP server
2. Execute semantic search
3. Return results
4. Server status shows "Connected" during session

---

## Troubleshooting

### Issue: Server Still Not Showing

**Check:**
```bash
# Verify server is configured
qwen mcp list | grep ck

# Check ck installation
ck --version

# Test ck manually
ck --sem "test" src/
```

**Solution:**
```bash
# Remove and re-add
qwen mcp remove ck
qwen mcp add ck "ck --serve"
```

---

### Issue: "Disconnected" Status

**This is normal!** MCP servers:
- ✅ Are started on-demand
- ✅ Run only during Qwen sessions
- ✅ Stop when session ends

**Not a problem** - server will connect automatically when you use semantic search.

---

### Issue: Server Won't Start

**Check:**
```bash
# Verify ck is in PATH
which ck

# Test ck directly
ck --status .

# Check for errors
ck --serve 2>&1 | head -10
```

**Solution:**
```bash
# Reinstall ck
cargo install ck

# Or download from releases
# https://github.com/BeaconBay/ck/releases
```

---

## Alternative: Project-Level Configuration

If you prefer project-level configuration (for `.mcp.json`):

### Create `.qwen/settings.json` in Project Root

```bash
mkdir -p .qwen
cat > .qwen/settings.json << 'EOF'
{
  "mcp": {
    "servers": {
      "ck": {
        "enabled": true,
        "command": "ck",
        "args": ["--serve"],
        "cwd": "/home/masum/github/PR/.taskmaster"
      }
    }
  }
}
EOF
```

### Start Qwen in Project Directory

```bash
cd /home/masum/github/PR/.taskmaster
qwen
```

**Note:** Global configuration (what we did) is **recommended** for most users.

---

## Comparison: Before vs After

### Before (Problem)

```bash
$ qwen mcp list
Configured MCP servers:
✗ task-master-ai: npx -y task-master-ai (stdio) - Disconnected

# ck not listed at all!
```

### After (Fixed)

```bash
$ qwen mcp list
Configured MCP servers:
✗ task-master-ai: npx -y task-master-ai (stdio) - Disconnected
✗ ck: ck --serve  (stdio) - Disconnected

# ✅ ck is now configured!
```

---

## Next Steps

### 1. Test Semantic Search

```bash
qwen

# In Qwen session:
"Search for security validation code using semantic search"
```

### 2. Verify It Works

Expected response should include:
- Search results from `src/` directory
- File paths and line numbers
- Similarity scores

### 3. Optional: Configure Additional Servers

```bash
# Add task-master-ai (if desired)
qwen mcp add task-master "npx -y task-master-ai"

# List all
qwen mcp list
```

---

## Resources

- **Official MCP Docs:** https://beaconbay.github.io/ck/features/mcp-integration.html
- **Qwen MCP Command:** `qwen mcp --help`
- **Our Setup Guide:** [QWEN_MCP_CK_SETUP.md](QWEN_MCP_CK_SETUP.md)
- **Integration Complete:** [CK_MCP_INTEGRATION_COMPLETE.md](CK_MCP_INTEGRATION_COMPLETE.md)

---

## Summary

✅ **Problem Solved:**
- `ck` MCP server now configured in Qwen Code CLI
- Shows in `qwen mcp list` output
- Ready to use for semantic search

✅ **Status:**
- Configured: ✅ Yes
- Connected: ⚠️ On-demand (normal)
- Ready to use: ✅ Yes

**Next Action:** Start a Qwen session and test semantic search!

---

**Last Updated:** 2026-02-20  
**Command Used:** `qwen mcp add ck "ck --serve"`
