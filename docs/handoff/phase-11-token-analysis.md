# Phase 11: Token Usage Analysis

**Purpose:** Analyze and optimize token usage across agent rule files.
**Steps:** 5
**Dependencies:** Phase 6 complete (deduplication should run first)

---

## Why This Phase?

Agent rules are loaded into context every session. Excessive tokens:
- Slow down AI reasoning
- Dilute important instructions
- Waste context window budget (140k tokens for Letta Code)

**Best practice:** Keep rules under 80-150 lines each.

---

## Step 11.1 — Calculate Token Usage per File

**Run:**
```bash
echo "=== TOKEN USAGE BY FILE ==="

# Root agent files
for file in AGENTS.md CLAUDE.md GEMINI.md QWEN.md IFLOW.md; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    tokens=$((lines * 5))  # rough estimate: 5 tokens per line
    status=""
    if [ "$lines" -gt 150 ]; then
      status="⚠️ LONG"
    elif [ "$lines" -lt 20 ]; then
      status="⚠️ BRIEF"
    else
      status="✅ OK"
    fi
    echo "$file: $lines lines (~$tokens tokens) $status"
  fi
done

# Rule directories
for dir in .cursor/rules .claude/rules .roo/rules .windsurf/rules .trae/rules .kiro/steering .clinerules; do
  if [ -d "$dir" ]; then
    lines=$(find "$dir" -name "*.md" -exec cat {} \; 2>/dev/null | wc -l)
    tokens=$((lines * 5))
    echo "$dir: $lines lines (~$tokens tokens)"
  fi
done
```

---

## Step 11.2 — Identify Token Hotspots

**Run:**
```bash
echo "=== TOKEN HOTSPOTS (files over 100 lines) ==="

find . -name "*.md" \
  \( -path "./.cursor/*" -o -path "./.claude/*" -o -path "./.roo/*" \
  -o -path "./.windsurf/*" -o -path "./.trae/*" -o -path "./.kiro/*" \
  -o -path "./.clinerules/*" -o -path "./.github/*" \) \
  -exec sh -c 'lines=$(wc -l < "$1" 2>/dev/null || echo 0); if [ "$lines" -gt 100 ]; then echo "$1: $lines lines ⚠️"; fi' _ {} \;
```

---

## Step 11.3 — Analyze Content Duplication (Token Waste)

**Run:**
```bash
echo "=== DUPLICATION ANALYSIS ==="

# Count duplicate sections
echo "Checking for 'Code Style' sections across files:"
grep -rl "Code Style" .cursor .claude .roo .windsurf .trae .kiro .clinerules 2>/dev/null | wc -l
echo "files have duplicate 'Code Style' sections"

echo ""
echo "Checking for 'Build Commands' sections:"
grep -rl "Build Commands\|pytest\|npm run" .cursor .claude .roo .windsurf .trae .kiro .clinerules 2>/dev/null | wc -l
echo "files have duplicate build command sections"
```

---

## Step 11.4 — Calculate Total Token Load

**Run:**
```bash
echo "=== TOTAL TOKEN LOAD ==="

# Sum all lines in agent rule files
total_lines=0

# Root files
for file in AGENTS.md CLAUDE.md GEMINI.md QWEN.md; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    total_lines=$((total_lines + lines))
  fi
done

# Rule directories  
for dir in .cursor/rules .claude/rules .roo/rules .windsurf/rules .trae/rules .kiro/steering .clinerules; do
  if [ -d "$dir" ]; then
    lines=$(find "$dir" -name "*.md" -exec cat {} \; 2>/dev/null | wc -l)
    total_lines=$((total_lines + lines))
  fi
done

total_tokens=$((total_lines * 5))

echo "Total lines: $total_lines"
echo "Estimated tokens: $total_tokens"
echo ""

if [ "$total_tokens" -gt 10000 ]; then
  echo "⚠️ HIGH TOKEN LOAD — consider deduplication"
elif [ "$total_tokens" -gt 5000 ]; then
  echo "✅ MODERATE TOKEN LOAD"
else
  echo "✅ LOW TOKEN LOAD — optimal"
fi
```

---

## Step 11.5 — Token Optimization Recommendations

**Based on analysis, output recommendations:**

```bash
echo "=== TOKEN OPTIMIZATION RECOMMENDATIONS ==="

# Check for long files
long_files=$(find . -name "*.md" \
  \( -path "./.cursor/*" -o -path "./.claude/*" -o -path "./.roo/*" \
  -o -path "./.windsurf/*" -o -path "./.trae/*" -o -path "./.kiro/*" \
  -o -path "./.clinerules/*" \) \
  -exec sh -c 'lines=$(wc -l < "$1" 2>/dev/null || echo 0); test "$lines" -gt 150 && echo "$1"' _ {} \; | wc -l)

if [ "$long_files" -gt 0 ]; then
  echo "1. Split $long_files files over 150 lines into focused, smaller files"
fi

# Check for duplicate content
dup_sections=$(grep -rl "Code Style\|Architecture\|Testing" .cursor .claude .roo .windsurf .trae .kiro .clinerules 2>/dev/null | wc -l)

if [ "$dup_sections" -gt 3 ]; then
  echo "2. Deduplicate common sections — move to AGENTS.md, reference from tool files"
fi

# Check for .claude/rules
if [ ! -d ".claude/rules" ] || [ -z "$(ls -A .claude/rules 2>/dev/null)" ]; then
  echo "3. Consolidate .claude/ context into CLAUDE.md (no .claude/rules needed)"
fi

echo ""
echo "TARGET: Under 5,000 total tokens for optimal performance"
echo "CURRENT: Run Step 11.4 to check"
```

---

## Gate Check

```bash
echo "=== PHASE 11 GATE CHECK ==="
echo "1. Token load calculated: RUN Step 11.4"
echo "2. Optimization plan: RUN Step 11.5"
echo "3. Execute remediation if needed"
```

---

## Token Budget Guidelines

| Category | Recommended | Max |
|----------|-------------|-----|
| Single rule file | 80-150 lines | 200 lines |
| All root files combined | 300 lines | 500 lines |
| All rule directories | 500 lines | 1000 lines |
| **Total context load** | **< 5,000 tokens** | **10,000 tokens** |

---

## Optimization Strategies

| Strategy | Token Savings | Trade-off |
|----------|---------------|-----------|
| **Split long files** | 50-70% | More files to manage |
| **Use AGENTS.md as single source** | 80% | Tools must import |
| **Path-scoped rules** | 30-50% | Complex frontmatter |
| **Remove duplicates** | 20-40% | None (best ROI) |
| **Use @imports** | 60-80% | Requires tool support |

---

## Notes

- Token estimates are rough (5 tokens per line average)
- Actual context usage depends on tool implementation
- Some tools (Kiro, Windsurf) use file-level scoping to reduce load
- Phase 6 (Deduplication) should run before token optimization
