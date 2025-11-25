# LLM Documentation Discovery & Processing Flow

**For**: Understanding how AI agents (Claude, GPT, etc.) discover and use project documentation  
**Purpose**: Map the information retrieval pipeline so docs are findable and actionable  
**Date**: November 9, 2025

---

## 🔍 Documentation Discovery Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│         HOW LLM AGENTS FIND AND USE YOUR DOCS              │
└─────────────────────────────────────────────────────────────┘

PHASE 1: INITIAL CONTEXT LOADING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ↓
  Agent starts (e.g., `amp`, `claude`, `cline`)
  ↓
  Agent loads PROJECT DISCOVERY FILES (in priority order):
  
  1️⃣ README.md (root)
     ├─ Project overview
     ├─ Links to key documentation
     └─ Quick start guide
  
  2️⃣ AGENTS.md (root) ← CRITICAL
     ├─ Task Master commands
     ├─ Workflow patterns
     ├─ Tool allowlist
     └─ Essential commands
  
  3️⃣ .amp-settings.json (root)
     ├─ Amp tool configuration
     ├─ Permissions rules
     ├─ Guarded files list
     └─ Safe operating mode
  
  4️⃣ CLAUDE.md (if using Claude Code)
     ├─ Claude-specific setup
     ├─ Custom slash commands
     └─ Context prefill
  
  5️⃣ .taskmaster/config.json
     ├─ AI model settings
     ├─ Research modes
     └─ Fallback models


PHASE 2: DISCOVERY OF SPECIALIZED DOCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ↓
  Agent needs to understand specific subsystem
  ↓
  Discovers docs via multiple paths:

  PATH A: Search-based discovery
  ┌─ Agent searches repo for topic
  ├─ `grep` or `finder` tool finds relevant docs
  ├─ Returns doc path + line numbers
  └─ Agent loads full doc

  PATH B: README/top-doc cross-references
  ┌─ Main docs link to specialized docs
  ├─ README.md → links to Architecture, Setup, Workflows
  ├─ AGENTS.md → links to Task Master guide
  └─ docs/INDEX.md → master reference (if created)

  PATH C: Directory structure scanning
  ┌─ Agent explores docs/ directory
  ├─ Reads file listing
  ├─ Identifies doc categories (ci-cd/, architecture/, etc.)
  └─ Loads relevant docs by filename pattern

  PATH D: User explicit requests
  ┌─ User: "Show me the orchestration setup"
  ├─ Agent searches for "orchestration"
  ├─ Finds: ORCHESTRATION_SYSTEM.md, ORCHESTRATION.md, etc.
  └─ Loads in priority order


PHASE 3: SPECIALIZED CONTEXT LOADING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ↓
  Agent determines task type, loads relevant docs:

  For GIT/BRANCH OPERATIONS:
  ├─ ORCHESTRATION_SYSTEM.md (machine-readable spec)
  ├─ AGENT_ORCHESTRATION_CHECKLIST.md (pre-op validation)
  ├─ ORCHESTRATION.md (quick ref)
  └─ SAFE_ACTION_PLAN.md (safety rules)

  For FILE MODIFICATIONS:
  ├─ ORCHESTRATION_SYSTEM.md (what syncs)
  ├─ AGENT_ORCHESTRATION_CHECKLIST.md (safety checks)
  └─ .amp-settings.json (guarded files)

  For TASK MANAGEMENT:
  ├─ AGENTS.md (Task Master commands)
  ├─ .taskmaster/config.json (model settings)
  └─ .taskmaster/tasks/tasks.json (current tasks)

  For WORKFLOW IMPLEMENTATION:
  ├─ GITHUB_WORKFLOWS_ROADMAP.md (P0/P1/P2 priorities)
  ├─ .github/workflows/ (existing workflow examples)
  └─ docs/ci-cd/ (if created)


PHASE 4: CONTEXT FILTERING & PRIORITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ↓
  Agent has 5-10 relevant docs, which to use?
  ↓
  Filtering happens by:

  1. DOCUMENT SIZE (token budget)
  ├─ Prioritize short docs (checklists > long narratives)
  ├─ Load decision trees before examples
  └─ Load full docs only if needed

  2. SPECIFICITY TO TASK
  ├─ Task = "modify setup file"
  ├─ Prioritize: AGENT_ORCHESTRATION_CHECKLIST.md
  ├─ Then: ORCHESTRATION_SYSTEM.md
  └─ Finally: ORCHESTRATION.md (if time)

  3. EXECUTION PHASE
  ├─ BEFORE action: Load CHECKLIST (validation)
  ├─ DURING action: Reference SYSTEM (decision tree)
  ├─ AFTER action: Verify against CHECKLIST (confirmation)
  └─ ON ERROR: Consult ORCHESTRATION.md (troubleshooting)


PHASE 5: DECISION MAKING WITH LOADED CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ↓
  Agent references loaded docs during reasoning:

  Example reasoning with AGENT_ORCHESTRATION_CHECKLIST.md:
  ┌─ Task: "Modify setup/setup_environment_system.sh"
  ├─ Step 1: Load AGENT_ORCHESTRATION_CHECKLIST.md
  ├─ Check: "Before modifying ANY file"
  ├─ Read: "1. What files will I modify?"
  ├─ Answer: "setup/setup_environment_system.sh"
  ├─ Check: "2. Are any of these MANAGED FILES?"
  ├─ Answer: "Yes, setup/* is in MANAGED_FILES"
  ├─ Check: "3. If YES to managed files, check BRANCH"
  ├─ Command: $ git branch
  ├─ Result: orchestration-tools ✓
  └─ Decision: ✅ SAFE TO PROCEED

  Example reasoning with ORCHESTRATION_SYSTEM.md:
  ┌─ Task: "I pushed to orchestration-tools, what happens?"
  ├─ Load: "📊 Sync Propagation Model"
  ├─ Find: "SCENARIO 2: Developer commits on orchestration-tools"
  ├─ Read: Step-by-step flow
  ├─ Understand: "Commit succeeds, stays local"
  ├─ Understand: "Developer pushes: git push origin orchestration-tools"
  ├─ Understand: "Remote receives commit on orchestration-tools"
  └─ Decision: Next sync will propagate to all branches ✓
```

---

## 📂 Documentation Hierarchy & Discovery

### What agents see when exploring `/docs`:

```
docs/
├─ INDEX.md (if created - master reference)
│  └─ Links to all major topics
│
├─ ORCHESTRATION_SYSTEM.md ⭐ MACHINE-READABLE SPEC
│  ├─ For: Understanding sync behavior
│  ├─ Use: Decision trees, constraint lists
│  ├─ Agents: Load for git operations involving setup files
│  └─ Size: ~1000 lines (token-efficient with sections)
│
├─ AGENT_ORCHESTRATION_CHECKLIST.md ⭐ PRE-OP VALIDATION
│  ├─ For: Validation before every operation
│  ├─ Use: Checklists, quick reference, green/yellow/red
│  ├─ Agents: Load FIRST before any file operation
│  └─ Size: ~400 lines (highly scannable)
│
├─ ORCHESTRATION.md (Quick Start)
│  ├─ For: Quick reference guide
│  ├─ Use: Common workflows, disable/enable hooks
│  ├─ Agents: Load as fallback if full spec needed
│  └─ Size: ~60 lines (very concise)
│
├─ orchestration-push-workflow.md (Detailed Workflows)
│  ├─ For: Step-by-step procedural guides
│  ├─ Use: When implementing complex orchestration tasks
│  ├─ Agents: Load if checklist insufficient
│  └─ Size: ~200 lines
│
├─ GITHUB_WORKFLOWS_ROADMAP.md (CI/CD Strategy)
│  ├─ For: Understanding workflow priorities
│  ├─ Use: Planning CI/CD work
│  ├─ Agents: Load when working on .github/workflows/
│  └─ Size: ~445 lines (prioritized sections)
│
├─ SYNC-FRAMEWORK.md (Technical Deep-Dive)
│  ├─ For: Understanding sync mechanism
│  ├─ Use: Troubleshooting sync issues
│  ├─ Agents: Load if sync behavior unclear
│  └─ Size: ~150 lines
│
├─ GIT_HOOKS_REFERENCE.md (Hook Behavior)
│  ├─ For: Understanding git hook behavior
│  ├─ Use: When hooks misbehave
│  ├─ Agents: Load if post-checkout/post-merge issues
│  └─ Size: ~100 lines
│
└─ ci-cd/
   ├─ WORKFLOWS.md (P0/P1/P2 implementation)
   └─ VALIDATION_CRITERIA.md (merge validation)
```

---

## 🔎 How Agents Discover These Docs

### Scenario 1: Agent searches for "orchestration"

```
User: "I need to modify setup files"
       ↓
Agent searches: grep -r "orchestration" docs/
       ↓
Results found:
  ✓ docs/ORCHESTRATION_SYSTEM.md (line 1: "# Orchestration System")
  ✓ docs/ORCHESTRATION.md (line 1: "# Orchestration System Guide")
  ✓ docs/AGENT_ORCHESTRATION_CHECKLIST.md (found early)
  ✓ ORCHESTRATION_DOCS_SCRIPTS_REVIEW.md (root level)
       ↓
Agent prioritizes by:
  1. AGENT_ORCHESTRATION_CHECKLIST.md (most actionable)
  2. ORCHESTRATION_SYSTEM.md (most comprehensive)
  3. ORCHESTRATION.md (quickest ref)
       ↓
Agent loads TOP 2-3 into context
       ↓
Proceeds with safe modification pattern from checklist
```

### Scenario 2: Agent encounters "managed file" in .amp-settings.json

```
Agent reads: .amp-settings.json
       ↓
Sees: "amp.guardedFiles.allowlist": [".amp-settings.json", ".mcp.json", ...]
       ↓
Agent realizes: "These files are protected, need special handling"
       ↓
Agent searches: "guard" or "protected" in docs
       ↓
Finds: AGENT_ORCHESTRATION_CHECKLIST.md
       ↓
Reads: "🔒 Safety Rules (Non-negotiable)"
       ↓
Learns: Never force-push, never commit app code, etc.
```

### Scenario 3: Agent performs git operation

```
Agent needs to: $ git push origin orchestration-tools
       ↓
Agent is safety-conscious, checks: .amp-settings.json
       ↓
Sees: "git push origin" requires 'action: ask'
       ↓
Agent searches: "git push" in docs
       ↓
Loads: AGENT_ORCHESTRATION_CHECKLIST.md → "Before git push"
       ↓
Checklist shows:
  [ ] git log -1 shows your commit message
  [ ] git diff origin/orchestration-tools..HEAD shows expected
  [ ] Only pushing to orchestration-tools
  [ ] Changes are tested and reviewed
       ↓
Agent validates each checkbox before proceeding
```

### Scenario 4: Agent doesn't know if file syncs

```
Agent wants to edit: .flake8 file
       ↓
Agent asks: "Does this file sync from orchestration-tools?"
       ↓
Agent searches: "flake8" in ORCHESTRATION_SYSTEM.md
       ↓
Finds: "MANAGED FILES list" includes ".flake8"
       ↓
Agent decides: "This is a managed file, must edit on orchestration-tools"
       ↓
Agent checks branch, proceeds safely
```

---

## 📊 Agent Processing Flow (Detailed)

### Step-by-Step: How an agent modifies a managed file

```
┌─ USER REQUEST: "Update setup script to fix timeout issue"

├─ STEP 1: LOAD DISCOVERY FILES
│  ├─ Read: README.md (context on project)
│  ├─ Read: AGENTS.md (safe workflow)
│  ├─ Read: .amp-settings.json (permissions)
│  └─ Decision: What doc tree to follow?

├─ STEP 2: IDENTIFY TASK CATEGORY
│  └─ Task = "Modify setup file"
│      Decision: Load AGENT_ORCHESTRATION_CHECKLIST.md

├─ STEP 3: PRE-OPERATION VALIDATION
│  └─ Load: AGENT_ORCHESTRATION_CHECKLIST.md
│     └─ Section: "🔴 CRITICAL CHECKS (Do these FIRST)"
│        ├─ Check 1: What files will I modify?
│        │  Answer: setup/setup_environment_system.sh
│        │
│        ├─ Check 2: Are any of these MANAGED FILES?
│        │  Answer: YES (in MANAGED_FILES list)
│        │
│        └─ Check 3: If YES, check BRANCH
│           Answer: $ git branch
│           Result: orchestration-tools ✓

├─ STEP 4: LOAD OPERATIONAL SPEC
│  └─ Load: ORCHESTRATION_SYSTEM.md
│     └─ Find: "Decision Tree for Agents"
│        └─ Find: "I want to modify a setup file"
│           └─ Read: Safe modification pattern
│              ├─ Branch check: orchestration-tools ✓
│              ├─ Modification allowed: YES ✓
│              └─ Next steps: Proceed with modification

├─ STEP 5: EXECUTE MODIFICATION
│  ├─ Read file: setup/setup_environment_system.sh
│  ├─ Make change: Fix timeout logic
│  ├─ Validate: Bash syntax check
│  └─ Test: Local test run

├─ STEP 6: PRE-COMMIT VALIDATION
│  └─ Load: AGENT_ORCHESTRATION_CHECKLIST.md
│     └─ Section: "Before `git commit`"
│        ├─ Validate: git branch shows orchestration-tools ✓
│        ├─ Validate: git diff --stat shows MANAGED_FILES only ✓
│        ├─ Validate: No app code ✓
│        ├─ Validate: No .env files ✓
│        └─ Decision: ✅ SAFE TO COMMIT

├─ STEP 7: COMMIT
│  └─ $ git commit -m "fix: resolve setup script timeout issue"
│     └─ Verified: Commit message is clear ✓

├─ STEP 8: PRE-PUSH VALIDATION
│  └─ Load: AGENT_ORCHESTRATION_CHECKLIST.md
│     └─ Section: "Before `git push`"
│        ├─ Validate: git log -1 shows commit message ✓
│        ├─ Validate: git diff shows expected changes ✓
│        ├─ Validate: Only pushing to orchestration-tools ✓
│        └─ Decision: ✅ SAFE TO PUSH

├─ STEP 9: PUSH
│  └─ $ git push origin orchestration-tools
│     └─ Verified: Push successful ✓

├─ STEP 10: POST-PUSH DOCUMENTATION
│  └─ Load: ORCHESTRATION_SYSTEM.md
│     └─ Section: "Sync Propagation Model"
│        └─ Find: "SCENARIO 2: Developer commits on orchestration-tools"
│           └─ Understand: Change will sync to all branches on next post-checkout/post-merge
│              └─ Document: "Updated setup script; will propagate to main/scientific on next sync"

└─ RESULT: ✅ Modification complete, safe, propagation planned
```

---

## 🎯 Context Window Optimization

### How agents load docs efficiently (limited tokens)

```
TOTAL CONTEXT BUDGET: ~100k tokens (for large models)
Breakdown:
  ├─ Codebase/files being edited: ~40k tokens
  ├─ Discovery + navigation docs: ~10k tokens
  ├─ Safety/constraints docs: ~5k tokens
  ├─ Task-specific reference: ~15k tokens
  └─ Working memory/response: ~30k tokens

DISCOVERY DOCS PRIORITY (tokens-efficient):

Tier 1 (ALWAYS LOAD - ~2k tokens):
  ├─ .amp-settings.json (300 tokens)
  ├─ AGENT_ORCHESTRATION_CHECKLIST.md first 200 lines (400 tokens)
  └─ AGENTS.md (1300 tokens)

Tier 2 (IF RELEVANT - ~3k tokens):
  ├─ ORCHESTRATION_SYSTEM.md sections only (2k tokens)
  │  ├─ Load: "Core Concepts"
  │  ├─ Load: "Decision Tree for Agents"
  │  └─ Load: "Safety Guardrails"
  │
  └─ .github/workflows/test.yml (1k tokens)

Tier 3 (ON DEMAND - ~5k tokens):
  ├─ Full ORCHESTRATION_SYSTEM.md
  ├─ ORCHESTRATION.md (quick ref)
  └─ Relevant troubleshooting section

EXAMPLE: Agent modifying setup file

Context budget allocation:
  1. Load: .amp-settings.json (300 tokens)
  2. Load: AGENT_ORCHESTRATION_CHECKLIST.md TOP SECTION (400 tokens)
  3. Load: ORCHESTRATION_SYSTEM.md → "Decision Tree" section (600 tokens)
  4. Load: ORCHESTRATION_SYSTEM.md → "Safety Guardrails" section (400 tokens)
  Total for safety context: ~1700 tokens
  Remaining for: File content, reasoning, response (~40k tokens)
```

---

## 🔗 Inter-Document References

### How docs link to each other (for agent discovery)

```
README.md
  ├─ "For orchestration system details, see docs/ORCHESTRATION_SYSTEM.md"
  ├─ "For AI agent operations, see docs/AGENT_ORCHESTRATION_CHECKLIST.md"
  └─ "For Task Master workflow, see AGENTS.md"

AGENTS.md
  ├─ "Tasks use .taskmaster/ structure, see Task Master guide"
  ├─ "For branch safety, see SAFE_ACTION_PLAN.md"
  └─ "For orchestration details, see docs/ORCHESTRATION_SYSTEM.md"

ORCHESTRATION_SYSTEM.md
  ├─ "For quick reference, see docs/ORCHESTRATION.md"
  ├─ "For detailed workflows, see docs/orchestration-push-workflow.md"
  ├─ "For hook details, see docs/GIT_HOOKS_REFERENCE.md"
  └─ "For agent checklists, see docs/AGENT_ORCHESTRATION_CHECKLIST.md"

AGENT_ORCHESTRATION_CHECKLIST.md
  ├─ "For detailed spec, see docs/ORCHESTRATION_SYSTEM.md"
  ├─ "For quick start, see docs/ORCHESTRATION.md"
  └─ "For emergency recovery, see troubleshooting sections"

.amp-settings.json (comments)
  └─ "For guarded files rationale, see docs/AGENT_ORCHESTRATION_CHECKLIST.md"
```

---

## 🤖 LLM-Specific Discovery Patterns

### Claude (via Claude Code)

```
Claude's discovery sequence:
1. Loads: .claude/settings.json (Claude Code config)
2. Loads: CLAUDE.md (auto-loaded context)
3. Loads: README.md (project overview)
4. Searches: For topic-specific docs
5. Uses: file paths from custom slash commands

Example:
  User: "/taskmaster-next"
  ↓
  Claude loads: .claude/commands/taskmaster-next.md
  ↓
  Claude executes: task-master next
  ↓
  Claude reads: .taskmaster/tasks/tasks.json
  ↓
  Claude references: AGENTS.md for command syntax
```

### Amp

```
Amp's discovery sequence:
1. Loads: .amp-settings.json (Amp configuration)
2. Loads: AGENTS.md (essential context)
3. Searches: Using finder/grep tools
4. Loads: Discovered docs on-demand
5. Uses: Tool allowlist for safety

Example:
  User: "Modify setup file"
  ↓
  Amp reads: .amp-settings.json → guarded files
  ↓
  Amp determines: "File is managed, need orchestration docs"
  ↓
  Amp searches: grep -r "setup" docs/
  ↓
  Amp loads: AGENT_ORCHESTRATION_CHECKLIST.md (priority)
  ↓
  Amp executes: Safe modification pattern
```

### OpenAI/GPT

```
GPT's discovery sequence:
1. User provides: Project context in system prompt
2. System prompt includes: Key file paths
3. GPT searches: Using file reading tools
4. GPT finds: Discovery docs mentioned in context
5. GPT loads: Full docs as needed

Example:
  System prompt: "Project has orchestration system, see docs/ORCHESTRATION_SYSTEM.md"
  ↓
  GPT reads: docs/ORCHESTRATION_SYSTEM.md
  ↓
  GPT understands: Sync behavior, constraints
  ↓
  GPT can: Make informed decisions about branch operations
```

---

## 📋 Checklist for Documentation Discoverability

```
✅ Documentation Structure:

  [ ] README.md exists and links to key docs
  [ ] AGENTS.md exists with essential commands
  [ ] docs/ directory has organized structure
  [ ] Each major subsystem has dedicated doc file
  [ ] Cross-references between related docs
  [ ] Machine-readable specs (decision trees, checklists)
  [ ] Quick-reference guides for common tasks
  [ ] Troubleshooting sections indexed
  [ ] Safety constraints clearly marked (🔴 RED, ⚠️ YELLOW)
  [ ] Examples showing safe vs unsafe patterns

✅ Agent Configuration:

  [ ] .amp-settings.json exists
  [ ] CLAUDE.md exists (if using Claude)
  [ ] Custom slash commands documented
  [ ] Tool allowlist configured
  [ ] Guarded files list specific
  [ ] Permissions clear (action: ask vs allow)

✅ Integration Docs:

  [ ] MCP server configuration documented
  [ ] API keys/auth documented (without exposing secrets)
  [ ] Integration patterns for each tool
  [ ] Example workflows for common tasks
  [ ] Troubleshooting for tool failures

✅ Version Control:

  [ ] Docs tracked in git
  [ ] Versioning strategy clear
  [ ] Changelog maintained
  [ ] Links always point to HEAD (not specific commits)
  [ ] Docs updated with code changes
```

---

## 🚀 How to Improve Discovery

### For current EmailIntelligence project:

```
1. CREATE docs/INDEX.md (master reference)
   └─ Links to all major topics
   └─ Organized by user type (developer, AI agent, DevOps)
   └─ Quick search guide

2. UPDATE README.md
   └─ Link to ORCHESTRATION_SYSTEM.md in intro
   └─ Link to AGENT_ORCHESTRATION_CHECKLIST.md in safety section
   └─ Link to AGENTS.md in workflow section

3. ADD comments to .amp-settings.json
   └─ Explain why files are guarded
   └─ Reference safety docs
   └─ Link to orchestration system

4. CREATE doc header template
   ```
   # [Topic]
   
   **For**: [Target audience]
   **Size**: [~XXX lines] (for token budget)
   **Priority**: [Critical/High/Medium/Low]
   **Related Docs**: [Links to related docs]
   **Quick Answer**: [1-2 sentence summary]
   ```

5. ADD semantic tags to docs
   ```
   <!-- Agent-Friendly: True -->
   <!-- Token-Efficient: True -->
   <!-- Decision-Trees: Yes -->
   <!-- Keywords: orchestration, git, sync -->
   ```

6. CREATE docs/DISCOVERY_GUIDE.md
   └─ Map of all docs
   └─ How agents find them
   └─ What each is for
   └─ When to use which
```

---

## Example: Complete Discovery Journey

```
USER REQUEST: "Help me safely modify the Python setup script"

AGENT DISCOVERY JOURNEY:
═══════════════════════════════════════════════════════════════

1️⃣ INITIAL LOAD
   Agent reads: README.md
   Finds: "See ORCHESTRATION_SYSTEM.md for setup file guidelines"
   Action: Make note

2️⃣ TASK RECOGNITION
   Agent determines: "Task = modify setup file"
   Decision: Need safety docs
   Searches: finder("orchestration")

3️⃣ SEARCH RESULTS
   Agent finds:
   ✓ docs/ORCHESTRATION_SYSTEM.md
   ✓ docs/AGENT_ORCHESTRATION_CHECKLIST.md
   ✓ docs/ORCHESTRATION.md
   ✓ ORCHESTRATION_DOCS_SCRIPTS_REVIEW.md
   
   Priority ranking:
   1. AGENT_ORCHESTRATION_CHECKLIST.md (most actionable)
   2. ORCHESTRATION_SYSTEM.md (comprehensive spec)
   3. ORCHESTRATION.md (quick ref if needed)

4️⃣ LOAD CHECKLIST
   Agent reads: AGENT_ORCHESTRATION_CHECKLIST.md
   Section: "🔴 CRITICAL CHECKS (Do these FIRST)"
   
   Executes:
   ✅ Check 1: Identify file type → setup/ file
   ✅ Check 2: Check MANAGED_FILES list → YES, in list
   ✅ Check 3: Verify branch → orchestration-tools ✓

5️⃣ LOAD DECISION TREE
   Agent reads: ORCHESTRATION_SYSTEM.md
   Section: "📊 Decision Tree for Agents"
   Subsection: "I want to modify a setup file"
   
   Follows tree:
   ✓ File is managed? YES
   ✓ Branch is orchestration-tools? YES
   ✓ Decision: Safe to modify ✓

6️⃣ EXECUTE MODIFICATION
   Agent:
   ├─ Reads file
   ├─ Makes change
   ├─ Validates syntax
   └─ Prepares commit

7️⃣ PRE-COMMIT VALIDATION
   Agent loads: AGENT_ORCHESTRATION_CHECKLIST.md
   Section: "Before `git commit`"
   
   Validates:
   ✅ Branch check
   ✅ File scope check
   ✅ No app code
   ✅ No local files
   ✅ Commit message clarity

8️⃣ COMMIT & PUSH
   Agent:
   ├─ Commits with clear message
   ├─ Validates pre-push checklist
   ├─ Pushes to orchestration-tools
   └─ Documents: "Change will sync to all branches"

9️⃣ POST-ACTION UNDERSTANDING
   Agent reads: ORCHESTRATION_SYSTEM.md
   Section: "Sync Propagation Model"
   Scenario: "Developer commits on orchestration-tools"
   
   Understands: Change will sync to other branches on next merge/checkout

🔟 COMPLETION
   Agent summarizes:
   ✓ Modification complete
   ✓ All safety checks passed
   ✓ Propagation planned
   ✓ No risks identified

═══════════════════════════════════════════════════════════════

KEY SUCCESS FACTORS:
✅ Multiple entry points to docs (README, search, cross-refs)
✅ Actionable checklists (not just narrative)
✅ Decision trees (step-by-step reasoning)
✅ Clear organization (by task type)
✅ Safety constraints highlighted (🔴 RED sections)
✅ Examples of safe vs unsafe patterns
✅ Token-efficient docs (multiple sizes available)
```

---

## Summary: Documentation for LLM Efficiency

```
PROBLEM: "LLMs don't understand workflow configuration efficiently"

ROOT CAUSE:
  ├─ Prose-based documentation (narratives)
  ├─ No clear decision trees
  ├─ No machine-readable structure
  ├─ Long context to extract small facts
  └─ No checklists for validation

SOLUTION: Three-Tier Documentation

  TIER 1: CHECKLISTS (Pre-operation validation)
  └─ AGENT_ORCHESTRATION_CHECKLIST.md
     ├─ ~400 lines, highly scannable
     ├─ Checkboxes before each operation
     ├─ Quick yes/no answers
     └─ Agents load FIRST

  TIER 2: DECISION TREES (Step-by-step reasoning)
  └─ ORCHESTRATION_SYSTEM.md
     ├─ ~1000 lines, organized by scenarios
     ├─ Step-by-step flows
     ├─ Constraint lists
     └─ Agents load SECOND for detailed reasoning

  TIER 3: NARRATIVE (Complete understanding)
  └─ ORCHESTRATION.md, orchestration-push-workflow.md
     ├─ Quick ref and detailed procedures
     ├─ Agents load ON DEMAND
     └─ For edge cases and troubleshooting

RESULT: LLM agents can efficiently:
  ✅ Discover relevant docs (multiple entry points)
  ✅ Load context selectively (checklists first, specs second)
  ✅ Validate before action (checklist approach)
  ✅ Reason about constraints (decision trees)
  ✅ Troubleshoot on error (reference docs)
  ✅ Propagate understanding (sync flow diagrams)
```

---

**Last Updated**: November 9, 2025  
**Audience**: Developers, AI agents, DevOps engineers  
**Version**: 1.0
