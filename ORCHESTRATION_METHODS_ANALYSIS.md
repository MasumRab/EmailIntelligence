# Agent File Orchestration: Alternative Methods to Git Hooks

## Overview
Instead of relying on client-side git hooks (which can be disabled, forgotten, or inconsistently configured), there are several server-side and automated alternatives for orchestrating agent file synchronization across branches.

---

## Method Comparison Matrix

| Method | Setup | Reliability | Enforcement | Centralized | Cost | Best For |
|--------|-------|-------------|-------------|------------|------|----------|
| **GitHub Actions** | Medium | ⭐⭐⭐⭐⭐ | Strong | ✅ | Free | Primary sync & validation |
| **Branch Protection Rules** | Low | ⭐⭐⭐⭐⭐ | Very Strong | ✅ | Free | Blocking invalid changes |
| **CODEOWNERS** | Low | ⭐⭐⭐⭐ | Medium | ✅ | Free | Review enforcement |
| **Pull Request Templates** | Low | ⭐⭐⭐ | Weak | ✅ | Free | Process guidance |
| **GitHub Bot (Dependabot-style)** | Medium | ⭐⭐⭐⭐⭐ | Strong | ✅ | Free | Automated PR creation |
| **Scheduled Workflows** | Medium | ⭐⭐⭐⭐ | Medium | ✅ | Free | Periodic reconciliation |
| **Merge Queue** | Low | ⭐⭐⭐⭐ | Strong | ✅ | Paid | Sequential merge control |
| **Manual Checklist** | Very Low | ⭐⭐ | Very Weak | ❌ | Free | Documentation only |
| **Server Hooks** | High | ⭐⭐⭐⭐⭐ | Very Strong | ✅ | Infrastructure | Enterprise-grade |
| **Monorepo Tools** | High | ⭐⭐⭐⭐⭐ | Strong | ✅ | Varies | Large-scale mono-repos |

---

## Detailed Methods

### 1. **GitHub Actions (Recommended Primary Method)**

#### How It Works
- Trigger on push/pull_request events
- Detect agent file changes automatically
- Run validation, sync, or enforcement logic
- Create PRs, comments, or status checks

#### Advantages
✅ Centralized enforcement (no client config needed)
✅ Guaranteed to run (server-side)
✅ Transparent to developers (visible in CI checks)
✅ Can create automated PRs
✅ Free and already in use (ci.yml exists)
✅ Works across all branches automatically

#### Disadvantages
❌ Requires workflow YAML setup
❌ Subject to GitHub API rate limits
❌ Debugging requires checking logs

#### Implementation for Agent Files
```yaml
# .github/workflows/orchestrate-agent-files.yml
name: Orchestrate Agent Files

on:
  push:
    paths:
      - 'AGENTS.md'
      - 'AGENT.md'
      - 'CLAUDE.md'
      - 'GEMINI.md'
      - 'QWEN.md'
      - 'LLXPRT.md'
      - 'CONTRIBUTING.md'
      - 'AGENT_GUIDANCE_PLAN.md'
    branches-ignore:
      - orchestration-tools

jobs:
  sync-to-orchestration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Check if on feature branch
        if: github.ref != 'refs/heads/orchestration-tools'
        run: |
          echo "Agent files changed on non-canonical branch"
          echo "Creating PR to orchestration-tools..."
      
      - name: Create sync PR
        if: github.ref != 'refs/heads/orchestration-tools'
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: 'chore: sync agent files from ${{ github.ref_name }}'
          title: '[AUTO] Sync agent files to orchestration-tools'
          body: |
            Agent instruction files were modified on `${{ github.ref_name }}`.
            This PR syncs them to the canonical orchestration-tools branch.
          branch: sync/agent-files-${{ github.ref_name }}
          base: orchestration-tools
```

#### Use Cases
- Auto-create PRs when agent files change on feature branches
- Validate agent file consistency
- Sync approved changes to all branches
- Block merges with invalid agent file state

---

### 2. **Branch Protection Rules + CODEOWNERS**

#### How It Works
- Define CODEOWNERS file pointing to maintainers
- Require PR reviews for agent files
- GitHub enforces reviews before merge
- Can dismiss stale reviews, require updates

#### Advantages
✅ GitHub-native, no config complexity
✅ Automatic review requirement
✅ Works with any PR workflow
✅ Status checks integrate naturally
✅ Simple to understand

#### Disadvantages
❌ Passive (requires developer to create PR)
❌ Doesn't auto-sync
❌ Only blocks merges, doesn't create PRs

#### Example CODEOWNERS
```
# .github/CODEOWNERS
AGENTS.md @orchestration-maintainers
AGENT.md @orchestration-maintainers
CLAUDE.md @orchestration-maintainers
GEMINI.md @orchestration-maintainers
QWEN.md @orchestration-maintainers
LLXPRT.md @orchestration-maintainers
CONTRIBUTING.md @orchestration-maintainers
AGENT_GUIDANCE_PLAN.md @orchestration-maintainers
```

#### Implementation
1. Create CODEOWNERS file (shown above)
2. Add branch protection rule:
   - Require PR reviews for these files
   - Dismiss stale reviews
   - Require review from code owners
   - Require status checks to pass

---

### 3. **Scheduled Reconciliation Workflow**

#### How It Works
- Run on schedule (e.g., daily/weekly)
- Compare orchestration-tools to other branches
- Detect drift/inconsistencies
- Create PRs to fix misalignment

#### Advantages
✅ Catches drifts that might be missed
✅ Periodic validation even if no changes
✅ Can aggregate multiple fixes in one PR
✅ Non-blocking (doesn't prevent merges)

#### Disadvantages
❌ Not real-time
❌ May create unnecessary PRs
❌ Requires tuning to avoid spam

#### Example Workflow
```yaml
name: Weekly Agent File Reconciliation

on:
  schedule:
    - cron: '0 9 * * MON'  # Monday mornings
  workflow_dispatch:

jobs:
  reconcile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Compare agent files across branches
        run: |
          AGENT_FILES=(AGENTS.md AGENT.md CLAUDE.md GEMINI.md QWEN.md LLXPRT.md CONTRIBUTING.md AGENT_GUIDANCE_PLAN.md)
          
          for branch in main scientific; do
            for file in "${AGENT_FILES[@]}"; do
              orchestration=$(git show orchestration-tools:$file 2>/dev/null || echo "")
              branch_version=$(git show $branch:$file 2>/dev/null || echo "")
              
              if [ "$orchestration" != "$branch_version" ]; then
                echo "DRIFT: $file differs on $branch"
              fi
            done
          done
      
      - name: Create reconciliation PR if needed
        # Only create PR if drift detected
        # ...
```

---

### 4. **Automated Bot (Like Dependabot)**

#### How It Works
- Custom bot monitors agent file changes
- Creates PRs with proposed changes
- Can apply transformations or sync logic
- Similar pattern to Dependabot

#### Advantages
✅ Fully automated
✅ Creates visible, reviewable PRs
✅ Can transform/validate before PR
✅ Highly customizable

#### Disadvantages
❌ Requires bot infrastructure/GitHub App setup
❌ More complex to implement
❌ Need proper authentication

#### Tools Available
- **Peter Evans Create PR Action** - Easy PR creation
- **GitHub Bot SDKs** - Full bot capability
- **Probot** - Framework for GitHub Apps

---

### 5. **Validation Workflow (Pre-merge Gate)**

#### How It Works
- Runs on every push/PR
- Validates agent file consistency
- Blocks merge if validation fails
- Clear error messages for developers

#### Advantages
✅ Catches problems immediately
✅ Prevents bad state from merging
✅ Developer feedback is instant
✅ No manual review needed

#### Disadvantages
❌ Only blocks, doesn't fix
❌ Requires developer action to fix

#### Example Validation
```yaml
name: Validate Agent Files

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check required agent files exist
        run: |
          REQUIRED_FILES=(
            AGENTS.md
            AGENT.md
            CLAUDE.md
            GEMINI.md
            QWEN.md
            LLXPRT.md
            CONTRIBUTING.md
          )
          
          MISSING=()
          for file in "${REQUIRED_FILES[@]}"; do
            if [ ! -f "$file" ]; then
              MISSING+=("$file")
            fi
          done
          
          if [ ${#MISSING[@]} -gt 0 ]; then
            echo "❌ Missing required agent files:"
            printf '%s\n' "${MISSING[@]}"
            exit 1
          fi
          echo "✅ All required agent files present"
      
      - name: Validate AGENTS.md structure
        run: |
          # Check for key sections
          grep -q "## Architecture Principles" AGENTS.md || exit 1
          grep -q "## Code Style" AGENTS.md || exit 1
          echo "✅ AGENTS.md has required sections"
```

---

## Recommended Hybrid Approach

### Tier 1: Prevention (Branch Protection)
```
├─ CODEOWNERS enforcement
├─ Required PR reviews for agent files
└─ Require status checks (validation workflow)
```

### Tier 2: Validation (GitHub Actions)
```
├─ Validate on every push
├─ Check file existence, format, structure
└─ Provide clear error messages
```

### Tier 3: Synchronization (GitHub Actions)
```
├─ Auto-create PRs for feature branch changes
├─ Sync approved changes to all branches
└─ Post-merge auto-sync orchestration-tools → other branches
```

### Tier 4: Reconciliation (Scheduled Workflow)
```
├─ Weekly drift detection
├─ Alert on inconsistencies
└─ Create PRs if manual intervention needed
```

---

## Implementation Roadmap

### Week 1: Setup Prevention & Validation
1. Create `.github/CODEOWNERS` file
2. Add branch protection rules
3. Create validation workflow (`validate-agent-files.yml`)
4. Document in AGENTS.md

### Week 2: Setup Automation
1. Create sync workflow (`sync-agent-files.yml`)
2. Configure to create PRs for feature branch changes
3. Test on a feature branch
4. Document sync expectations

### Week 3: Setup Reconciliation
1. Create scheduled workflow (`reconcile-agent-files.yml`)
2. Set to run weekly
3. Add notification logic
4. Monitor for false positives

### Week 4: Decommission Hooks
1. Archive local git hooks documentation
2. Update AGENTS.md to remove hook references
3. Switch to GitHub Actions-based approach
4. Validate all workflows functioning

---

## Comparison: Hooks vs. GitHub Actions

### Git Hooks (Current)
```
Reliability:    ⭐⭐⭐ (depends on dev setup)
Enforcement:    ⭐⭐ (can be disabled)
Visibility:     ⭐⭐ (hidden from team)
Maintenance:    ⭐⭐ (scattered across machines)
Consistency:    ⭐⭐ (varies by developer)
```

### GitHub Actions (Recommended)
```
Reliability:    ⭐⭐⭐⭐⭐ (server-side, always runs)
Enforcement:    ⭐⭐⭐⭐⭐ (block merges via protection rules)
Visibility:     ⭐⭐⭐⭐⭐ (transparent in CI checks)
Maintenance:    ⭐⭐⭐⭐⭐ (single source of truth)
Consistency:    ⭐⭐⭐⭐⭐ (identical for all developers)
```

---

## Questions for Implementation Decision

1. **Synchronization Strategy:**
   - Should all branches auto-sync from orchestration-tools?
   - Or should changes go TO orchestration-tools via PR?
   - Or bidirectional with conflict resolution?

2. **Approval Process:**
   - Who approves agent file PRs?
   - Does sync require approval or auto-merge?

3. **Scientific/Taskmaster Branches:**
   - Can they have specialized overrides?
   - How are overrides validated?

4. **Frequency:**
   - Real-time sync or daily reconciliation?
   - Scheduled validation intervals?

5. **Failure Handling:**
   - Block merges on inconsistency?
   - Just warn and log?
   - Create notification issues?

---

## Success Metrics

- ✅ Agent files automatically synchronized across branches
- ✅ No manual intervention needed for standard sync
- ✅ Drift detected within 24 hours
- ✅ Invalid changes blocked before merge
- ✅ All developers aware of enforcement (via PR checks)
- ✅ Zero failed syncs due to configuration issues
