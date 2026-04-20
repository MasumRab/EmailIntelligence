#!/usr/bin/env bash
# context-agnostic-gates.sh — Executable gate checks for any branch/folder
# Usage: source context-guard.sh && source context-agnostic-gates.sh
#
# Each gate function returns 0 (pass) or 1 (fail) so agents can
# programmatically determine results. "NOT PRESENT" is NOT a failure —
# it documents that the branch doesn't configure that tool.

set -uo pipefail

# --- Phase 1: Emergency Fixes ---
phase1_gate() {
    local failures=0
    echo "=== PHASE 1 GATE CHECK (context-agnostic) ==="
    echo "Branch: $CURRENT_BRANCH | Root: $PROJECT_ROOT"

    check_file_content "CLAUDE.md" '<<<<<<' "Merge conflicts" || failures=$((failures + 1))
    check_json ".roo/mcp.json" "Roo MCP" || failures=$((failures + 1))
    check_json ".cursor/mcp.json" "Cursor MCP" || failures=$((failures + 1))
    check_json ".claude/mcp.json" "Claude MCP" || failures=$((failures + 1))
    check_file_content ".windsurf/mcp.json" "YOUR_" "Windsurf placeholders" || failures=$((failures + 1))
    check_json ".trae/mcp.json" "Trae MCP" || failures=$((failures + 1))
    check_json ".kiro/mcp.json" "Kiro MCP" || failures=$((failures + 1))
    check_json ".kilo/mcp.json" "Kilo MCP" || failures=$((failures + 1))
    check_file ".rules" ".rules file (should be deleted)" || failures=$((failures + 1))

    echo ""
    echo "=== DISCOVERED AGENT TOOLS ==="
    echo "$AGENT_TOOLS" | tr ' ' '\n' | nl
    echo ""
    echo "=== PHASE 1 RESULT ==="
    echo "Files checked: $(echo "$AGENT_TOOLS" | wc -w)"
    echo "Branch: $CURRENT_BRANCH"
    return $failures
}

# --- Phase 2: Content Fixes ---
phase2_gate() {
    local failures=0
    echo "=== PHASE 2 GATE CHECK (context-agnostic) ==="

    check_file_content ".windsurf/rules/dev_workflow.md" "windsurf,windsurf" "Duplicate flag" || failures=$((failures + 1))

    local prisma_count=0
    for dir in .clinerules .windsurf/rules .roo/rules .trae/rules .kiro/steering .kilo/rules; do
        if [ -d "$PROJECT_ROOT/$dir" ]; then
            local count
            count=$(grep -rl "prisma" "$PROJECT_ROOT/$dir" 2>/dev/null | wc -l)
            echo "🔍 Prisma refs in $dir: $count"
            prisma_count=$((prisma_count + count))
        else
            echo "⚪ Prisma refs in $dir: NOT PRESENT (branch doesn't configure this tool)"
        fi
    done
    echo "Total Prisma refs: $prisma_count"
    [ "$prisma_count" -gt 0 ] && failures=$((failures + 1))

    check_json "rulesync.jsonc" "Rulesync config" || failures=$((failures + 1))
    echo ""
    echo "=== PHASE 2 RESULT ==="
    echo "Total Prisma refs: $prisma_count"
    return $failures
}

# --- Phase 3: Ruler Setup ---
phase3_gate() {
    local failures=0
    echo "=== PHASE 3 GATE CHECK (context-agnostic) ==="

    check_file ".ruler/AGENTS.md" "Ruler AGENTS.md" || failures=$((failures + 1))
    check_file ".ruler/ruler.toml" "Ruler config" || failures=$((failures + 1))

    if command -v ruler &>/dev/null; then
        echo "🔍 Ruler dry-run: $(ruler apply --dry-run 2>&1 | head -1)"
    else
        echo "⚪ Ruler: NOT INSTALLED (branch doesn't require ruler)"
    fi

    check_file_content "CLAUDE.md" "EmailIntelligence" "Project name reference" || failures=$((failures + 1))
    check_file_content "AGENTS.md" "EmailIntelligence" "Project name reference" || failures=$((failures + 1))
    echo ""
    echo "=== PHASE 3 RESULT ==="
    return $failures
}

# --- Phase 4: Agent RuleZ ---
phase4_gate() {
    local failures=0
    echo "=== PHASE 4 GATE CHECK (context-agnostic) ==="

    if command -v rulez &>/dev/null; then
        echo "✅ rulez: $(rulez --version 2>/dev/null || echo 'INSTALLED')"
    else
        echo "⚪ rulez: NOT INSTALLED (branch doesn't require rulez)"
    fi

    check_file ".claude/hooks.yaml" "Agent RuleZ hooks" || failures=$((failures + 1))

    if command -v rulez &>/dev/null && [ -f "$PROJECT_ROOT/.claude/hooks.yaml" ]; then
        echo "🔍 rulez validate: $(rulez validate 2>&1 | grep -c 'validated successfully') passed"
        echo "🔍 rulez lint: $(rulez lint 2>&1 | grep -c 'No issues found') clean"
    fi
    echo ""
    echo "=== PHASE 4 RESULT ==="
    return $failures
}

# --- Phase 5: File Cleanup ---
phase5_gate() {
    local failures=0
    echo "=== PHASE 5 GATE CHECK (context-agnostic) ==="

    check_file "GEMINI.md" "Gemini CLI instructions" || failures=$((failures + 1))
    check_file "QWEN.md" "Qwen CLI instructions" || failures=$((failures + 1))
    check_file "IFLOW.md" "iFlow instructions" || failures=$((failures + 1))
    check_file "CRUSH.md" "Crush instructions" || failures=$((failures + 1))
    check_file "LLXPRT.md" "LLxPRT instructions" || failures=$((failures + 1))
    check_file ".gemini/JULES_TEMPLATE.md" "Jules template extraction" || failures=$((failures + 1))

    echo ""
    local tier2_count=0
    for f in GEMINI.md QWEN.md IFLOW.md CRUSH.md LLXPRT.md; do
        [ -f "$PROJECT_ROOT/$f" ] && tier2_count=$((tier2_count + 1))
    done
    echo "=== PHASE 5 RESULT ==="
    echo "Tier 2 files present: $tier2_count/5"
    return $failures
}

# --- Phase 6: Deduplication ---
phase6_gate() {
    local failures=0
    echo "=== PHASE 6 GATE CHECK (context-agnostic) ==="

    check_file_content ".clinerules/cline_rules.md" "prisma" "Prisma refs in cline" || failures=$((failures + 1))
    check_file_content ".windsurf/rules/dev_workflow.md" "windsurf,windsurf" "Windsurf duplicate flag" || failures=$((failures + 1))
    check_file ".qwen/PROJECT_SUMMARY.md" "Qwen project summary" || failures=$((failures + 1))
    check_file "GEMINI.md" "Gemini root file" || failures=$((failures + 1))

    echo ""
    echo "=== PHASE 6 RESULT ==="
    return $failures
}

# --- Phase 7: Hierarchy ---
phase7_gate() {
    local failures=0
    echo "=== PHASE 7 GATE CHECK (context-agnostic) ==="

    check_file "src/core/AGENTS.md" "src/core AGENTS.md" || failures=$((failures + 1))
    check_file "src/backend/AGENTS.md" "src/backend AGENTS.md" || failures=$((failures + 1))
    check_file "client/AGENTS.md" "client AGENTS.md" || failures=$((failures + 1))

    echo ""
    echo "=== PHASE 7 RESULT ==="
    return $failures
}

# --- Phase 8: Orchestration ---
phase8_gate() {
    local failures=0
    echo "=== PHASE 8 GATE CHECK (context-agnostic) ==="

    check_file "modules/config.sh" "Config module" || failures=$((failures + 1))
    check_file "modules/branch.sh" "Branch module" || failures=$((failures + 1))
    check_file "modules/distribute.sh" "Distribute module" || failures=$((failures + 1))
    check_file "modules/safety.sh" "Safety module" || failures=$((failures + 1))
    check_file "modules/validate.sh" "Validate module" || failures=$((failures + 1))
    check_file "modules/utils.sh" "Utils module" || failures=$((failures + 1))
    check_file "modules/logging.sh" "Logging module" || failures=$((failures + 1))
    check_file "scripts/distribute-orchestration-files.sh" "Distribution script" || failures=$((failures + 1))

    echo ""
    echo "=== PHASE 8 RESULT ==="
    return $failures
}

# --- Phase 9: Verification (aggregates all prior gates) ---
phase9_gate() {
    local failures=0
    echo "=== PHASE 9 GATE CHECK — FULL VERIFICATION ==="

    phase1_gate || failures=$((failures + 1))
    echo ""
    phase2_gate || failures=$((failures + 1))
    echo ""
    phase3_gate || failures=$((failures + 1))
    echo ""
    phase4_gate || failures=$((failures + 1))
    echo ""
    phase5_gate || failures=$((failures + 1))
    echo ""
    phase6_gate || failures=$((failures + 1))
    echo ""
    phase7_gate || failures=$((failures + 1))
    echo ""
    phase8_gate || failures=$((failures + 1))

    echo ""
    if [ "$failures" -eq 0 ]; then
        echo "============================================"
        echo "✅ PHASE 9 — ALL VERIFICATION CHECKS PASSED"
        echo "============================================"
    else
        echo "============================================"
        echo "❌ PHASE 9 — $failures SUB-GATE(S) FAILED — see above"
        echo "============================================"
    fi
    return $failures
}

# --- Phase 10: Agent Rules Quality Evaluation ---
phase10_gate() {
    local failures=0
    echo "=== PHASE 10 GATE CHECK (context-agnostic) ==="

    # 1. Stack detection
    if [ -f "$PROJECT_ROOT/scripts/detect-branch-stack.sh" ]; then
        echo "🔍 Stack detection:"
        bash "$PROJECT_ROOT/scripts/detect-branch-stack.sh" 2>/dev/null | grep -E "^  (✅|⚠️|⚪)" | head -10
    else
        echo "⚪ detect-branch-stack.sh: NOT FOUND"
        failures=$((failures + 1))
    fi

    # 2. Structural accuracy
    if [ -f "$PROJECT_ROOT/scripts/verify-agent-content.sh" ]; then
        local verify_result
        verify_result=$(bash "$PROJECT_ROOT/scripts/verify-agent-content.sh" 2>/dev/null | tail -1)
        echo "🔍 Structural: $verify_result"
        echo "$verify_result" | grep -q "aligned" || failures=$((failures + 1))
    else
        echo "⚪ verify-agent-content.sh: NOT FOUND"
        failures=$((failures + 1))
    fi

    # 3. Content size
    if [ -f "$PROJECT_ROOT/.ruler/AGENTS.md" ]; then
        local lines
        lines=$(wc -l < "$PROJECT_ROOT/.ruler/AGENTS.md")
        echo "📏 .ruler/AGENTS.md: $lines lines"
        [ "$lines" -gt 80 ] && echo "⚠️  Over 80 lines — consider trimming redundant rules"
    fi

    # 4. Redundancy patterns
    local redundant=0
    for f in .ruler/AGENTS.md GEMINI.md QWEN.md; do
        if [ -f "$PROJECT_ROOT/$f" ]; then
            local r
            r=$(grep -ci "clean code\|best practices\|write.*maintainable\|follow.*conventions" "$PROJECT_ROOT/$f" 2>/dev/null)
            r="${r:-0}"
            if [ "$r" -gt 0 ] 2>/dev/null; then
                echo "⚠️  $f: $r vague/redundant rules"
                redundant=$((redundant + r))
            fi
        fi
    done
    [ "$redundant" -gt 0 ] && failures=$((failures + 1))

    # 5. Distribution sync
    if [ -f "$PROJECT_ROOT/.ruler/AGENTS.md" ] && [ -f "$PROJECT_ROOT/AGENTS.md" ]; then
        if diff <(sed -n '/^# EmailIntelligence/,$p' "$PROJECT_ROOT/AGENTS.md") "$PROJECT_ROOT/.ruler/AGENTS.md" > /dev/null 2>&1; then
            echo "✅ AGENTS.md distribution in sync"
        else
            echo "❌ AGENTS.md drifted from .ruler/AGENTS.md"
            failures=$((failures + 1))
        fi
    fi

    # 6. Stack evaluation exists
    if [ -f "$PROJECT_ROOT/docs/handoff/phase-10-stack-evaluation.md" ]; then
        echo "✅ Stack evaluation document exists"
    else
        echo "⚠️  No stack evaluation document — create one for this branch"
    fi

    echo ""
    echo "=== PHASE 10 RESULT ==="
    echo "ℹ️  Manual step: paste .ruler/AGENTS.md into agentrulegen.com/analyze and record quality score"
    return $failures
}

# --- Phase 11: Smart Workflow Remediation ---
phase11_gate() {
    local failures=0
    echo "=== PHASE 11 GATE CHECK (context-agnostic) ==="

    # Prisma references — use grep -rl for directories
    if [ -d "$PROJECT_ROOT/.kilo/rules" ]; then
        local kilo_count
        kilo_count=$(grep -rl "prisma" "$PROJECT_ROOT/.kilo/rules" 2>/dev/null | wc -l)
        echo "🔍 Prisma in .kilo/rules: $kilo_count"
        [ "$kilo_count" -gt 0 ] && failures=$((failures + 1))
    else
        echo "⚪ Prisma in .kilo/rules: NOT PRESENT"
    fi
    if [ -d "$PROJECT_ROOT/.github/instructions" ]; then
        local gh_count
        gh_count=$(grep -rl "prisma" "$PROJECT_ROOT/.github/instructions" 2>/dev/null | wc -l)
        echo "🔍 Prisma in .github/instructions: $gh_count"
        [ "$gh_count" -gt 0 ] && failures=$((failures + 1))
    else
        echo "⚪ Prisma in .github/instructions: NOT PRESENT"
    fi

    # Variable quoting in git commands
    check_file_content "modules/branch.sh" 'git .* \$' "Unquoted vars in branch.sh" || failures=$((failures + 1))
    check_file_content "modules/distribute.sh" 'git .* \$' "Unquoted vars in distribute.sh" || failures=$((failures + 1))

    # Branch name validation
    if type validate_branch_name_format &>/dev/null; then
        echo "✅ Branch name validation function exists"
    else
        echo "⚪ Branch name validation function: NOT FOUND"
        failures=$((failures + 1))
    fi

    # Tier 2 files
    check_file "GEMINI.md" "GEMINI.md" || failures=$((failures + 1))
    check_file "QWEN.md" "QWEN.md" || failures=$((failures + 1))

    echo ""
    echo "=== PHASE 11 RESULT ==="
    return $failures
}

# --- Phase 12: Deep Agent Handoff (documentary only) ---
phase12_gate() {
    local failures=0
    echo "=== PHASE 12 GATE CHECK (context-agnostic) ==="

    check_file "docs/handoff/phase-12-deep-agent-handoff.md" "Phase 12 document" || failures=$((failures + 1))
    check_file "docs/handoff/STATE.md" "State index" || failures=$((failures + 1))
    check_file ".github/instructions/tools-manifest.json" "Tools manifest" || failures=$((failures + 1))
    check_file ".gemini/settings.json" "Gemini runtime config" || failures=$((failures + 1))
    check_file ".qwen/settings.json" "Qwen runtime config" || failures=$((failures + 1))

    echo ""
    echo "=== PHASE 12 RESULT ==="
    echo "ℹ️  Phase 12 is documentation only — no file modifications expected"
    return $failures
}

# --- Final Verification (summary gate) ---
final_gate() {
    local failures=0
    echo "============================================"
    echo "FINAL VERIFICATION — ALL ISSUES"
    echo "Branch: $CURRENT_BRANCH | Root: $PROJECT_ROOT"
    echo "============================================"

    echo ""
    echo "--- CRITICAL ISSUES ---"
    check_file_content "CLAUDE.md" '<<<<<<' "Merge conflicts" || failures=$((failures + 1))
    check_file ".roo/mcp.json" "Roo MCP populated" || failures=$((failures + 1))
    check_file ".cursor/mcp.json" "Cursor MCP populated" || failures=$((failures + 1))
    check_file ".trae/mcp.json" "Trae MCP exists" || failures=$((failures + 1))
    check_file_content ".windsurf/mcp.json" "YOUR_" "Windsurf placeholders" || failures=$((failures + 1))

    echo ""
    echo "--- MAJOR ISSUES ---"
    local prisma_total=0
    for dir in .clinerules .windsurf/rules .roo/rules .trae/rules .kiro/steering; do
        if [ -d "$PROJECT_ROOT/$dir" ]; then
            local c
            c=$(grep -rl "prisma" "$PROJECT_ROOT/$dir" 2>/dev/null | wc -l)
            echo "🔍 Prisma in $dir: $c"
            prisma_total=$((prisma_total + c))
        fi
    done
    echo "Total Prisma refs: $prisma_total"
    [ "$prisma_total" -gt 0 ] && failures=$((failures + 1))

    echo ""
    echo "--- INFRASTRUCTURE ---"
    [ -d "$PROJECT_ROOT/.ruler" ] && echo "✅ Ruler: CONFIGURED" || echo "⚪ Ruler: NOT CONFIGURED"
    command -v ruler &>/dev/null && echo "✅ Ruler: INSTALLED" || echo "⚪ Ruler: NOT INSTALLED"
    [ -f "$PROJECT_ROOT/.ruler/ruler.toml" ] && echo "✅ Ruler config: EXISTS" || echo "⚪ Ruler config: MISSING"
    [ "$PROJECT_ROOT/.ruler/ruler.toml" != "$(pwd)/.ruler/ruler.toml" ] || failures=$((failures + 1))

    [ -f "$PROJECT_ROOT/.claude/hooks.yaml" ] && echo "✅ Agent RuleZ: CONFIGURED" || echo "⚪ Agent RuleZ: NOT CONFIGURED"
    command -v rulez &>/dev/null && echo "✅ Agent RuleZ: INSTALLED" || echo "⚪ Agent RuleZ: NOT INSTALLED"

    check_json "rulesync.jsonc" "RuleSync config" || failures=$((failures + 1))

    echo ""
    echo "--- TIER 2 ROOT FILES ---"
    local tier2=0
    for f in GEMINI.md QWEN.md IFLOW.md CRUSH.md LLXPRT.md; do
        if [ -f "$PROJECT_ROOT/$f" ]; then
            echo "✅ $f: EXISTS"
            tier2=$((tier2 + 1))
        else
            echo "⚪ $f: NOT PRESENT"
        fi
    done
    echo "Tier 2 files: $tier2/5"

    echo ""
    if [ "$failures" -eq 0 ]; then
        echo "============================================"
        echo "✅ CONTEXT-AGNOSTIC CHECKS COMPLETE"
        echo "============================================"
    else
        echo "============================================"
        echo "❌ CONTEXT-AGNOSTIC CHECKS — $failures ISSUE(S) FOUND"
        echo "============================================"
    fi
    return $failures
}

# Run all phases if sourced directly
if [ "${1:-all}" = "all" ]; then
    total_failures=0
    phase1_gate || total_failures=$((total_failures + $?))
    echo ""
    phase2_gate || total_failures=$((total_failures + $?))
    echo ""
    phase3_gate || total_failures=$((total_failures + $?))
    echo ""
    phase4_gate || total_failures=$((total_failures + $?))
    echo ""
    phase5_gate || total_failures=$((total_failures + $?))
    echo ""
    phase6_gate || total_failures=$((total_failures + $?))
    echo ""
    phase7_gate || total_failures=$((total_failures + $?))
    echo ""
    phase8_gate || total_failures=$((total_failures + $?))
    echo ""
    phase9_gate || total_failures=$((total_failures + $?))
    echo ""
    phase10_gate || total_failures=$((total_failures + $?))
    echo ""
    phase11_gate || total_failures=$((total_failures + $?))
    echo ""
    phase12_gate || total_failures=$((total_failures + $?))
    echo ""
    final_gate || total_failures=$((total_failures + $?))
    echo ""
    echo "TOTAL FAILURES: $total_failures"
    exit $total_failures
fi
