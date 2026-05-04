#!/usr/bin/env bash
# execution-journal.sh — Auto-captures context, decisions, and changes for each phase
# Usage: source context-guard.sh && source execution-journal.sh
# Then call: start_phase "5" "File Cleanup"

# Append a structured phase entry to STATE.md with full context capture
start_phase() {
    local phase_num="$1"
    local phase_name="$2"
    local timestamp
    timestamp="$(date -u +%Y-%m-%dT%H:%M:%S%z)"
    local commit_sha
    commit_sha="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"

    cat >> "$PROJECT_ROOT/docs/handoff/STATE.md" << EOF

### Phase ${phase_num}: ${phase_name}
- **Status:** IN_PROGRESS
- **Agent:** \${AGENT_NAME:-unknown}
- **Agent Model:** \${AGENT_MODEL:-unknown}
- **Session ID:** \${SESSION_ID:-unknown}
- **Started:** ${timestamp}
- **Completed:** [NOT STARTED]
- **Context:**
  - Branch: ${CURRENT_BRANCH}
  - Commit: ${commit_sha}
  - CWD: \$(pwd)
  - Project Root: ${PROJECT_ROOT}
  - Discovered Tools: ${AGENT_TOOLS}
  - Tool Count: \$(echo "${AGENT_TOOLS}" | wc -w)
- **Decision Log:**
  | # | Decision | Rationale | Alternatives Considered | Outcome |
  |---|----------|-----------|------------------------|---------|
- **Changes:**
  | File | Action | Before | After | Commit SHA |
  |------|--------|--------|-------|------------|
- **Gate Check:** [NOT RUN]
- **Files Modified:** none
- **Issues:** none
- **Verification Evidence:** [Captured after gate check]

EOF

    echo "Phase ${phase_num} entry created at ${timestamp}"
    echo "Branch: ${CURRENT_BRANCH} | Commit: ${commit_sha} | Tools: \$(echo "${AGENT_TOOLS}" | wc -w) discovered"
}

# Log a decision during phase execution
log_decision() {
    local phase_num="$1"
    local decision_num="$2"
    local decision="$3"
    local rationale="$4"
    local alternatives="$5"
    local outcome="$6"

    echo "Decision ${phase_num}.${decision_num}: ${decision}"
    echo "  Rationale: ${rationale}"
    echo "  Alternatives: ${alternatives}"
    echo "  Outcome: ${outcome}"
}

# Log a file change during phase execution
log_change() {
    local file="$1"
    local action="$2"
    local before="$3"
    local after="$4"
    local commit="${5:-pending}"

    echo "Change: ${file} → ${action}"
    echo "  Before: ${before}"
    echo "  After: ${after}"
    echo "  Commit: ${commit}"
}

# Complete a phase with gate check results
complete_phase() {
    local phase_num="$1"
    local gate_result="$2"  # PASS or FAIL
    local gate_output="$3"  # Full gate check output
    local timestamp
    timestamp="$(date -u +%Y-%m-%dT%H:%M:%S%z)"
    local commit_sha
    commit_sha="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"

    echo "Phase ${phase_num} completed at ${timestamp}"
    echo "Gate Check: ${gate_result}"
    echo "Final Commit: ${commit_sha}"
}

# Generate a diff summary between two commits
diff_summary() {
    local from_commit="$1"
    local to_commit="${2:-HEAD}"

    echo "=== Changes between ${from_commit} and ${to_commit} ==="
    git diff --stat "${from_commit}" "${to_commit}" 2>/dev/null || echo "No diff available"
    echo ""
    echo "Files changed: $(git diff --name-only "${from_commit}" "${to_commit}" 2>/dev/null | wc -l)"
    echo "Lines added: $(git diff --stat "${from_commit}" "${to_commit}" 2>/dev/null | tail -1 | grep -o '[0-9]* insertion' || echo '0')"
    echo "Lines deleted: $(git diff --stat "${from_commit}" "${to_commit}" 2>/dev/null | tail -1 | grep -o '[0-9]* deletion' || echo '0')"
}
