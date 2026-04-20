#!/usr/bin/env bash
# context-guard.sh — Branch and folder agnostic context detection
# Usage: source context-guard.sh  (from any directory, any branch)
#
# This script:
# 1. Auto-detects project root from any CWD
# 2. Detects current branch
# 3. Discovers which agent tools are configured
# 4. Sets PROJECT_ROOT for all subsequent operations

set -euo pipefail

# --- Step 1: Detect project root ---
detect_project_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/.git/HEAD" ] || [ -f "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "ERROR: No git repository found in path hierarchy" >&2
    return 1
}

PROJECT_ROOT="$(detect_project_root)"
export PROJECT_ROOT
# NOTE: We do NOT cd to PROJECT_ROOT — keep user's CWD intact
# All file operations will use $PROJECT_ROOT prefix

# --- Step 2: Detect branch ---
CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || echo 'detached')"
CURRENT_COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
export CURRENT_BRANCH CURRENT_COMMIT

# --- Step 3: Discover configured agent tools ---
# Scans for known agent tool directories and files
discover_agents() {
    local tools=()
    local r="$PROJECT_ROOT"

    # Agent config directories
    [ -d "$r/.roo" ]           && tools+=("roo")
    [ -d "$r/.cursor" ]        && tools+=("cursor")
    [ -d "$r/.claude" ]        && tools+=("claude")
    [ -d "$r/.windsurf" ]      && tools+=("windsurf")
    [ -d "$r/.trae" ]          && tools+=("trae")
    [ -d "$r/.kiro" ]          && tools+=("kiro")
    [ -d "$r/.kilo" ]          && tools+=("kilo")
    [ -d "$r/.clinerules" ]    && tools+=("cline")
    [ -d "$r/.zed" ]           && tools+=("zed")
    [ -d "$r/.continue" ]      && tools+=("continue")
    [ -d "$r/.gemini" ]        && tools+=("gemini")
    [ -d "$r/.qwen" ]          && tools+=("qwen")
    [ -d "$r/.agent" ]         && tools+=("agent")
    [ -d "$r/.agents" ]        && tools+=("agents")
    [ -d "$r/.iflow" ]         && tools+=("iflow")
    [ -d "$r/.ruler" ]         && tools+=("ruler")

    # Root-level agent files
    [ -f "$r/CLAUDE.md" ]      && tools+=("CLAUDE.md")
    [ -f "$r/AGENTS.md" ]      && tools+=("AGENTS.md")
    [ -f "$r/GEMINI.md" ]      && tools+=("GEMINI.md")
    [ -f "$r/QWEN.md" ]        && tools+=("QWEN.md")
    [ -f "$r/IFLOW.md" ]       && tools+=("IFLOW.md")
    [ -f "$r/CRUSH.md" ]       && tools+=("CRUSH.md")
    [ -f "$r/LLXPRT.md" ]      && tools+=("LLXPRT.md")
    [ -f "$r/.rules" ]         && tools+=(".rules")

    # Config files
    [ -f "$r/.mcp.json" ]      && tools+=("mcp.json(root)")
    [ -f "$r/rulesync.jsonc" ] && tools+=("rulesync")
    [ -f "$r/opencode.json" ]  && tools+=("opencode")

    echo "${tools[@]}"
}

AGENT_TOOLS="$(discover_agents)"
export AGENT_TOOLS

# --- Step 6: Determine branch-specific state file ---
# Sanitize branch name for filename (replace / with _)
SAFE_BRANCH="$(echo "$CURRENT_BRANCH" | sed 's|/|_|g')"
STATE_FILE="$PROJECT_ROOT/docs/handoff/STATE_${SAFE_BRANCH}.md"
export STATE_FILE SAFE_BRANCH

# --- Step 7: Print context summary ---
echo "=== EXECUTION CONTEXT ==="
echo "Project Root:   $PROJECT_ROOT"
echo "Branch:         $CURRENT_BRANCH ($CURRENT_COMMIT)"
echo "CWD:            $PWD"
echo "Agent Tools:    $AGENT_TOOLS"
echo "Tool Count:     $(echo "$AGENT_TOOLS" | wc -w)"
echo "State File:     $STATE_FILE"
if [ -f "$STATE_FILE" ]; then
    echo "State Exists:   YES ($(wc -l < "$STATE_FILE") lines)"
else
    echo "State Exists:   NO — run: cp docs/handoff/STATE_TEMPLATE.md \"$STATE_FILE\""
fi
echo "========================="

# --- Step 5: Helper functions for gate checks ---
# These replace all hardcoded relative-path checks

# Check if file exists, report status
# NOTE: "NOT PRESENT" is a valid check result — it documents the branch's configuration
check_file() {
    local file="$1"
    local desc="$2"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "✅ $desc ($file): EXISTS"
        return 0
    else
        # This is NOT a skip — it's a documented finding: this branch doesn't have this file
        echo "⚪ $desc ($file): NOT PRESENT (branch doesn't configure this tool)"
        return 0  # Not a failure — just not configured on this branch
    fi
}

# Check file content with grep, only if file exists
check_file_content() {
    local file="$1"
    local pattern="$2"
    local desc="$3"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        local count
        count=$(grep -c "$pattern" "$PROJECT_ROOT/$file" 2>/dev/null || echo "0")
        echo "🔍 $desc ($file): $count matches"
        echo "$count"
    else
        echo "⚪ $desc ($file): NOT PRESENT (branch doesn't configure this tool)"
        echo "0"
    fi
}

# Validate JSON file, only if it exists
check_json() {
    local file="$1"
    local desc="$2"
    if [ -f "$PROJECT_ROOT/$file" ]; then
        if python3 -c "import json,sys; json.load(open(sys.argv[1])); print('VALID')" "$PROJECT_ROOT/$file" 2>/dev/null; then
            echo "✅ $desc ($file): VALID JSON"
            return 0
        else
            echo "❌ $desc ($file): INVALID JSON"
            return 1
        fi
    else
        echo "⚪ $desc ($file): NOT PRESENT (branch doesn't configure this tool)"
        return 0
    fi
}

# Check if directory exists
check_dir() {
    local dir="$1"
    local desc="$2"
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        echo "✅ $desc ($dir): EXISTS"
        return 0
    else
        echo "⚪ $desc ($dir): NOT PRESENT"
        return 0
    fi
}

# Count files matching pattern in directory
count_files() {
    local dir="$1"
    local pattern="$2"
    local desc="$3"
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        local count
        count=$(find "$PROJECT_ROOT/$dir" -name "$pattern" 2>/dev/null | wc -l)
        echo "📁 $desc ($dir/$pattern): $count files"
        echo "$count"
    else
        echo "⚪ $desc ($dir): NOT PRESENT (skipped)"
        echo "0"
    fi
}
