# RTK-Subagent Integration Design

**Date:** 2026-02-27  
**Status:** Proposal  
**Risk Level:** Low (non-breaking, opt-in enhancement)

---

## Executive Summary

This document proposes integrating RTK (token optimization CLI) capabilities into specialized subagent workflows. The integration is **opt-in** and **non-breaking**, adding token-efficient operations to existing agent capabilities without modifying core agent behavior.

**Key Benefits:**
- 60-80% token reduction for agent reconnaissance operations
- Faster agent execution (reduced I/O and context building)
- Consistent token optimization across all agent types
- No breaking changes to existing workflows

---

## Current Agent Framework Analysis

### Available Agent Types (from MULTI_AGENT_COORDINATION.md)

**Core Workflow Agents:**
- `architect-reviewer` - Architecture review and validation
- `backend-architect` - Backend architecture design
- `code-reviewer` - Code quality and production-readiness
- `error-detective` - Bug detection and root cause analysis
- `git-error-detective` - Git conflicts and version control
- `security-auditor` - Security vulnerability assessment
- `security-error-detective` - Security-specific error detection
- `performance-engineer` - Performance optimization
- `test-automator` - Test suite creation

**Specialist Agents:**
- `python-pro`, `javascript-pro`, `typescript-pro`, `rust-pro`, `golang-pro`, `php-pro`
- `ai-engineer`, `ml-engineer`, `data-engineer`
- `docs-architect`, `api-documenter`, `reference-builder`
- `cloud-architect`, `network-engineer`, `devops-troubleshooter`
- And 20+ more specialized agents

### Agent Invocation Pattern

Agents are invoked via the `task` tool:

```python
task(description="Review code structure",
     prompt="Please perform a comprehensive code review...",
     subagent_type="code-reviewer")
```

**Current Agent Workflow:**
1. Agent receives task description and prompt
2. Agent explores codebase using native commands (`ls`, `grep`, `read_file`, etc.)
3. Agent analyzes findings
4. Agent returns comprehensive report

**Token Cost:** High - exploration phase uses verbose native commands

---

## RTK Integration Architecture

### Design Principle: Opt-In Enhancement

RTK integration is **additive**, not replacement. Agents continue to work without RTK, but can leverage RTK when:
1. RTK is available in the environment
2. Task context indicates token optimization is appropriate
3. User explicitly requests RTK usage

### Integration Strategy: Three Tiers

#### Tier 1: RTK-Aware Agents (Low Risk)
Agents receive RTK usage guidance and can choose to use RTK commands when appropriate.

**Implementation:**
- Add RTK section to agent-specific instructions
- Agent decides when to use RTK vs native commands
- No code changes required

**Example Agents:**
- `code-reviewer` - Use `rtk grep` for initial code search
- `architect-reviewer` - Use `rtk tree` for structure exploration
- `security-auditor` - Use `rtk ls` for file discovery

#### Tier 2: RTK-Enhanced Agents (Medium Risk)
Specialized agent variants with RTK commands built into their workflow.

**Naming Convention:** `{agent}-rtk`

**Example Variants:**
- `code-reviewer-rtk` - Code review with token-optimized exploration
- `architect-reviewer-rtk` - Architecture review with RTK reconnaissance
- `security-auditor-rtk` - Security audit with RTK file discovery
- `performance-engineer-rtk` - Performance analysis with RTK profiling

**Implementation:**
- Create agent variant instruction files
- Pre-configure RTK usage patterns
- Fallback to native commands if RTK unavailable

#### Tier 3: RTK-Specialist Agents (Higher Risk, Higher Reward)
New agent types specifically for RTK operations.

**New Agent Types:**
- `rtk-explorer` - Specialized in token-optimized codebase exploration
- `rtk-summarizer` - Generates compact summaries using RTK tools
- `rtk-diff-analyzer` - Specialized in change analysis using `rtk diff`

**Implementation:**
- Define new agent types in agent registry
- Create dedicated instruction files
- Integrate with existing agent coordination

---

## Recommended Approach: Tier 1 + Selective Tier 2

**Phase 1 (Low Risk):** Add RTK guidance to existing agents  
**Phase 2 (Medium Risk):** Create RTK variants for high-token agents  
**Phase 3 (Optional):** Evaluate need for RTK-specialist agents

---

## Agent-Specific RTK Integration Patterns

### 1. architect-reviewer

**Current Workflow:**
```bash
ls -la
tree src/
find . -name "*.py" | head -20
cat architecture.md
```

**RTK-Enhanced Workflow:**
```bash
rtk ls -la                    # 70% token savings
rtk tree src/                 # 80% token savings
rtk find "src/"               # Compact tree output
rtk read architecture.md      # Intelligent filtering
```

**Instruction Addition:**
```markdown
## RTK Usage for Architecture Review

**Recommended RTK Commands:**
- `rtk tree -L 2` - High-level project structure
- `rtk ls -la` - Directory contents (token-optimized)
- `rtk read <file>` - Architecture documents with filtering
- `rtk smart <file>` - 2-line technical summaries

**When to Avoid RTK:**
- Detailed architectural analysis (use `read_file` tool)
- Security-critical architecture review
- Compliance documentation review
```

---

### 2. code-reviewer

**Current Workflow:**
```bash
grep -r "TODO\|FIXME" src/
cat src/main.py
git diff HEAD~5
```

**RTK-Enhanced Workflow:**
```bash
rtk grep "TODO|FIXME" src/    # Compact grep, grouped by file
rtk read src/main.py          # Smart filtering
rtk diff                      # Only changed lines
```

**Instruction Addition:**
```markdown
## RTK Usage for Code Review

**Recommended RTK Commands:**
- `rtk grep "pattern" src/` - Code search (grouped, compact)
- `rtk read <file>` - Initial code reconnaissance
- `rtk diff` - Change summary
- `rtk test` - Test run (failures only)

**When to Avoid RTK:**
- Line-by-line code review (use `read_file` tool)
- Debugging test failures (use native `pytest -v`)
- Security vulnerability analysis
```

---

### 3. security-auditor

**Current Workflow:**
```bash
find . -name "*.py" -exec grep -l "eval\|exec" {} \;
cat src/auth.py
grep -r "password\|secret" .
```

**RTK-Enhanced Workflow:**
```bash
rtk find "src/"                        # Compact file discovery
rtk grep "eval|exec" src/              # Pattern search (compact)
rtk read src/auth.py                   # Initial reconnaissance
```

**Instruction Addition:**
```markdown
## RTK Usage for Security Audits

**⚠️ CRITICAL: Security audits require full fidelity**

**Safe RTK Usage:**
- `rtk ls` - File discovery
- `rtk find` - Locate files by pattern
- `rtk grep` - Initial pattern search (then verify with native)

**NEVER Use RTK For:**
- Reading security-critical code (use `read_file` tool)
- Analyzing authentication logic
- Reviewing encryption implementations
- Compliance-related code review
- Vulnerability verification
```

---

### 4. performance-engineer

**Current Workflow:**
```bash
pytest --profile
cat profile_output.txt
time python script.py
```

**RTK-Enhanced Workflow:**
```bash
rtk pytest --profile        # Compact test output
rtk read profile_output.txt # Filtered reading
rtk err python script.py    # Only errors/warnings
```

**Instruction Addition:**
```markdown
## RTK Usage for Performance Analysis

**Recommended RTK Commands:**
- `rtk test` - Test runs (passing = minimal output)
- `rtk err <command>` - Run and show only errors
- `rtk read <profile>` - Profile output with filtering

**When to Avoid RTK:**
- Detailed performance profiling (need full metrics)
- Benchmark analysis (need exact numbers)
- Memory profiling (need complete heap dumps)
```

---

### 5. error-detective

**Current Workflow:**
```bash
cat error.log
grep -A 10 "Traceback" logs/
git log --oneline -20
```

**RTK-Enhanced Workflow:**
```bash
rtk log error.log            # Filter and deduplicate
rtk grep "Traceback" logs/   # Compact grep
rtk git log --oneline -20    # Compact history
```

**Instruction Addition:**
```markdown
## RTK Usage for Error Detection

**Recommended RTK Commands:**
- `rtk log <file>` - Filter and deduplicate logs
- `rtk err <command>` - Run and show only errors
- `rtk grep "pattern"` - Error pattern search
- `rtk git log` - Compact history

**When to Avoid RTK:**
- Analyzing stack traces (need full context)
- Debugging complex failures
- Root cause analysis (need complete error details)
```

---

### 6. docs-architect

**Current Workflow:**
```bash
find . -name "*.md"
cat docs/architecture.md
grep -r "TODO" docs/
```

**RTK-Enhanced Workflow:**
```bash
rtk find "docs/"             # Compact tree output
rtk read docs/architecture.md # Smart filtering
rtk grep "TODO" docs/        # Compact grep
```

**Instruction Addition:**
```markdown
## RTK Usage for Documentation

**Recommended RTK Commands:**
- `rtk tree docs/` - Documentation structure
- `rtk read <file>` - Documentation with filtering
- `rtk grep "pattern" docs/` - Content search
- `rtk smart <file>` - Quick document summaries

**When to Avoid RTK:**
- Final documentation review (need exact wording)
- Technical accuracy verification
- API documentation generation
```

---

## Implementation Plan

### Phase 1: RTK-Aware Agents (Week 1-2)

**Task 1.1:** Create RTK usage sections in agent instruction files
- Target: Top 10 most-used agent types
- Files: `.qwen/agents/*.md` or equivalent
- Risk: **Low** - Documentation only, no code changes

**Task 1.2:** Update RTK_USAGE_GUIDE.md with agent-specific examples
- Add "RTK for Different Agent Types" section
- Include before/after token comparisons
- Risk: **Low** - Documentation enhancement

**Task 1.3:** Test RTK usage with each agent type
- Verify agents correctly use RTK when available
- Verify graceful fallback when RTK unavailable
- Risk: **Low** - Testing only

---

### Phase 2: RTK-Enhanced Agent Variants (Week 3-4)

**Task 2.1:** Create RTK variant instruction files
- `architect-reviewer-rtk.md`
- `code-reviewer-rtk.md`
- `security-auditor-rtk.md`
- `performance-engineer-rtk.md`
- `error-detective-rtk.md`

**Task 2.2:** Register RTK variant agents
- Add to agent registry/configuration
- Ensure proper routing when `subagent_type="*-rtk"` requested

**Task 2.3:** Create RTK variant quick reference
- Side-by-side comparison: standard vs RTK variant
- Token savings estimates
- When to use which variant

**Risk:** **Medium** - New agent variants require testing

---

### Phase 3: Evaluation (Week 5-6)

**Task 3.1:** Measure token savings
- Compare token usage: standard agents vs RTK variants
- Collect data from real usage scenarios

**Task 3.2:** Gather user feedback
- Survey users on RTK variant effectiveness
- Identify pain points and improvement areas

**Task 3.3:** Decide on Tier 3 (RTK-specialist agents)
- Evaluate if specialist agents provide additional value
- Cost-benefit analysis of new agent types

---

## Configuration Examples

### Agent Configuration with RTK

**Option A: Environment Variable**
```bash
# Enable RTK for all agents
export AGENT_RTK_MODE=1

# Or per-agent
export CODE_REVIEWER_RTK=1
export ARCHITECT_REVIEWER_RTK=1
```

**Option B: Agent Instruction**
```markdown
## RTK Configuration

This agent is RTK-aware. When RTK is available in your environment,
I will use RTK commands for exploration and reconnaissance tasks.

To disable RTK: Set `AGENT_RTK_MODE=0` in your environment.
```

**Option C: Explicit Agent Variant**
```python
# Use RTK-enhanced agent
task(description="Review architecture",
     subagent_type="architect-reviewer-rtk")

# Use standard agent (no RTK)
task(description="Review architecture",
     subagent_type="architect-reviewer")
```

---

## Risk Mitigation

### Risk 1: Agent Confusion About When to Use RTK

**Mitigation:**
- Clear decision framework in agent instructions
- Examples of appropriate vs inappropriate RTK usage
- "Golden Rule": When in doubt, prefer native commands

### Risk 2: RTK Unavailable in Environment

**Mitigation:**
- Agents check for RTK availability before use
- Graceful fallback to native commands
- No errors if RTK not installed

### Risk 3: Information Loss from RTK Filtering

**Mitigation:**
- Conservative RTK usage (reconnaissance only)
- Escalation path: RTK → RTK verbose → native
- Agent training on recognizing when RTK is insufficient

### Risk 4: Breaking Existing Workflows

**Mitigation:**
- **Opt-in only** - agents don't use RTK unless explicitly configured
- No changes to default agent behavior
- RTK variants are separate agent types, not replacements

---

## Token Savings Estimates

### Agent Reconnaissance Phase (Typical)

| Operation | Native Tokens | RTK Tokens | Savings |
|-----------|---------------|------------|---------|
| `ls -la` (3 levels) | 1,500 | 450 | 70% |
| `tree src/` | 2,000 | 400 | 80% |
| `grep "pattern" src/` | 1,200 | 300 | 75% |
| `read file.py` | 800 | 400 | 50% |
| `git log --oneline -20` | 800 | 200 | 75% |
| **Total** | **6,300** | **1,750** | **72%** |

### Full Agent Session (Estimated)

| Agent Type | Standard Tokens | RTK Tokens | Savings |
|------------|-----------------|------------|---------|
| `architect-reviewer` | 15,000 | 6,000 | 60% |
| `code-reviewer` | 12,000 | 4,500 | 62% |
| `security-auditor` | 18,000 | 9,000 | 50% (conservative RTK usage) |
| `performance-engineer` | 10,000 | 4,000 | 60% |
| `error-detective` | 8,000 | 3,200 | 60% |

**Overall Estimated Savings:** 60-70% for reconnaissance-heavy agents

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ RTK guidance added to 10+ agent instruction files
- ✅ Agents successfully use RTK when available
- ✅ No breaking changes to existing workflows
- ✅ User feedback positive on token savings

### Phase 2 Success Criteria
- ✅ 5 RTK variant agents created and tested
- ✅ Token savings match estimates (60-70%)
- ✅ Users can easily select RTK variants
- ✅ Clear documentation on when to use which variant

### Phase 3 Success Criteria
- ✅ Data-driven decision on Tier 3 agents
- ✅ Comprehensive token savings report
- ✅ User satisfaction with RTK integration
- ✅ Roadmap for continued RTK enhancement

---

## Recommendation

**Proceed with Phase 1 immediately** (low risk, high reward):
1. Add RTK guidance to top 10 agent instruction files
2. Update RTK_USAGE_GUIDE.md with agent-specific examples
3. Test with real usage scenarios

**Evaluate Phase 2 after Phase 1 completion:**
- If Phase 1 successful → proceed with RTK variants
- If Phase 1 shows issues → address before expanding

**Phase 3 optional:**
- Only if data shows specialist agents provide unique value
- Consider opportunity cost vs other enhancements

---

## Appendix: Agent Instruction Template

### Template for Adding RTK to Agent Instructions

```markdown
## RTK (Token Optimization) Usage

**This agent is RTK-aware.** When RTK is available in your environment, use RTK commands for exploration and reconnaissance to reduce token usage by 60-70%.

### Quick Decision Framework

**✅ Use RTK for:**
- [Agent-specific exploration task 1]
- [Agent-specific exploration task 2]
- Initial reconnaissance and discovery

**❌ Avoid RTK for:**
- [Agent-specific critical task 1]
- [Agent-specific critical task 2]
- Detailed analysis requiring full fidelity

**⚠️ Escalate verbosity if output is unclear:**
```bash
rtk -v command     # More verbose
rtk -vv command    # Even more
rtk -vvv command   # Maximum detail before going native
```

**Golden Rule:** When in doubt about information loss, prefer native commands or `read_file` tool.

### Recommended RTK Commands for [Agent Type]

```bash
# Exploration
rtk ls -la                    # Directory listing
rtk tree <dir>/               # Tree view
rtk find "<pattern>"          # Find files

# Code Search
rtk grep "pattern" <dir>/     # Compact grep, grouped by file

# File Reading
rtk read <file>               # Smart filtering
rtk smart <file>              # 2-line technical summary

# [Agent-specific commands]
```

**See:** [`RTK_USAGE_GUIDE.md`](../../RTK_USAGE_GUIDE.md) for complete documentation.
```

---

**Document Status:** Ready for Review  
**Next Steps:** Create todos for Phase 1 implementation  
**Owner:** Agent coordination team
