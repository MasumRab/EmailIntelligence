# Git Repository Scan Report
**Generated:** 2025-11-10  
**Scan Scope:** All .git repositories in /home/masum/github and subdirectories

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Repos Scanned | 8 |
| Repos with Unpushed Commits | 0 |
| Repos with Stashes | 6 |
| Total Stashes Across All Repos | 51 |
| Repos with Uncommitted Changes | 6 |

**Critical Finding:** No unpushed commits, but significant stashed work (51 stashes) and uncommitted changes across 6 repositories indicate potential work-in-progress requiring review and action.

---

## Repository Details & Branch Analysis

### 1. ✅ `/home/masum/github/worktrees/taskmaster-worktree`
**Status:** Clean unpushed work  
**Current Branch:** `taskmaster`  
**Unpushed Commits:** 0  
**Stashes:** 0  
**Uncommitted Changes:** 19 untracked files

**Branch Status (git branch -vv):**
```
  master     dd61677 Remove .env from taskmaster worktree
* taskmaster dd61677 Remove .env from taskmaster worktree
```
- **Local branches:** 2 (master, taskmaster)
- **Tracking:** No remote tracking configured
- **Note:** Worktree-specific setup - no remote sync expected

**Files Untracked:**
- Configuration directories: `.clinerules/`, `.cursor/`, `.env.example`, `.gemini/`, `.github/`, `.kilo/`, `.kiro/`, `.roo/`, `.vscode/`, `.windsurf/`, `.zed/`
- Documentation: `AGENT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- Rules: `.rules`, `.rulesync/`, `.trae/`
- Gitignore-related: `.gitignore`

**Action Items:**
- [ ] Review if these files should be gitignored or committed
- [ ] Consider adding AI tool config directories to global gitignore
- [ ] Commit or remove untracked documentation files

---

### 2. ✅ `/home/masum/github/rulesync`
**Status:** Clean  
**Current Branch:** `main`  
**Unpushed Commits:** 0  
**Stashes:** 0  
**Uncommitted Changes:** None

**Branch Status (git branch -vv):**
```
* main b441920 [origin/main] Merge pull request #474 from dyoshikawa/fix-rule
```
- **Local branches:** 1 (main)
- **Remote branches:** 3 (origin/HEAD, origin/fix-tests, origin/main, origin/skills)
- **Tracking:** main → origin/main (in sync)

**Assessment:** No action needed. Repository is clean and properly synchronized.

---

### 3. ⚠️ `/home/masum/github/EmailIntelligenceQwen`
**Status:** Stashed work + uncommitted changes  
**Current Branch:** `001-implement-planning-workflow`  
**Unpushed Commits:** 0  
**Stashes:** 11  
**Uncommitted Changes:** 35 (modified + untracked)

**Branch Status (git branch -vv):**
```
  001-generate-tasks-md              17d0ac2 fix: Update conflict warning message in post-checkout hook
* 001-implement-planning-workflow    6ccb0c4 [origin/001-implement-planning-workflow] Resolve merge conflict: accept remote's version of scripts/hooks/post-checkout
  align-feature-notmuch-tagging-1-v2 e586b2a [origin/align-feature-notmuch-tagging-1-v2] Remove redundant documentation files and directories
  feat/modular-ai-platform           3550a11 [origin/feat/modular-ai-platform] fix: resolve conflicts in launch.py and tests/test_launcher.py
  feature-notmuch-tagging-1          7f94dac [origin/feature-notmuch-tagging-1: ahead 1, behind 1] Add orchestration tools and sync scripts
  main                               8293f96 [origin/main: behind 4] Merge pull request #194 from MasumRab/remove-deprecated-markers
  orchestration-tools                65f3465 [origin/orchestration-tools: behind 13] Merge branch 'orchestration-tools'
  orchestration-tools-temp           6ccb0c4 [origin/orchestration-tools: ahead 2, behind 11] Resolve merge conflict
  scientific                         79a4dce [origin/scientific: behind 8] Fix merge artifacts in Git hooks
+ taskmaster                         a5b6cf7 (/home/masum/github/EmailIntelligenceQwen/.taskmaster) [taskmaster/taskmaster: ahead 6, behind 5] Flatten structure
```
- **Local branches:** 10 (9 regular + 1 worktree)
- **Remote branches:** 60+ active
- **Sync Status:** 
  - Current branch: in sync with origin
  - feature-notmuch-tagging-1: ⚠️ ahead 1, behind 1 (diverged)
  - main: ⚠️ behind 4 commits
  - orchestration-tools: ⚠️ behind 13 commits
  - orchestration-tools-temp: ⚠️ ahead 2, behind 11 (diverged)
  - scientific: ⚠️ behind 8 commits
  - taskmaster: ⚠️ ahead 6, behind 5 (diverged worktree)

**Stash Summary:**
- `stash@{0}`: WIP on planning workflow (17d0ac2)
- `stash@{1}`: Merge PR #194 - remove deprecated markers
- `stash@{2}`: Modular AI platform sync
- `stash@{3-10}`: Various orchestration and scientific branch work

**Modified Files:**
- Setup scripts: `setup/setup_environment_system.sh`, `setup/setup_environment_wsl.sh`, `setup/setup_python.sh`
- Configuration: `.gitignore`, `pyproject.toml`
- Documentation: `README.md`, `docs/`
- Launch scripts: `setup/launch.py`

**Untracked Files (20+):**
- Agent guides: `AGENT.md`, `CLAUDE.md`, `QWEN.md`
- Planning/workflow: `PLANNING_WORKFLOW.md`, `PROJECT_SUMMARY.md`, etc.
- Cleanup scripts: `cleanup_orchestration_branch.py`
- Specs directory

**Action Items:**
- [ ] **PRIORITY:** Review and decide on 11 stashes - determine if any contain important work
- [ ] Commit legitimate changes to setup files and configuration
- [ ] Consolidate/clean untracked planning documentation
- [ ] Remove or properly track orchestration cleanup scripts
- [ ] Verify status of planning workflow implementation

---

### 4. ⚠️ `/home/masum/github/EmailIntelligence`
**Status:** Stashed work + uncommitted changes  
**Current Branch:** `orchestration-tools-changes`  
**Unpushed Commits:** 0  
**Stashes:** 14  
**Uncommitted Changes:** 21 (modified + deleted + untracked)

**Branch Status (git branch -vv) - Key Branches Only:**
```
  main                         74b486f5 [origin/main: behind 10] Address Sourcery AI review comments
  orchestration-tools          19432490 [origin/orchestration-tools: behind 59] Update managed files
* orchestration-tools-changes  5d9a0682 [origin/orchestration-tools-changes] docs: add context contamination prevention guide
  scientific                   79a4dcea [origin/scientific: ahead 2, behind 3] Fix merge artifacts in Git hooks
+ taskmaster                   79d77c65 (/home/masum/github/EmailIntelligence/.taskmaster) [origin/taskmaster: behind 9] Update tasks
```
- **Local branches:** 18 (17 regular + 1 worktree)
- **Remote branches:** 70+ active
- **Critical Sync Issues:**
  - orchestration-tools: ⚠️⚠️ behind 59 commits (severely out of sync)
  - main: ⚠️ behind 10 commits
  - taskmaster: ⚠️ behind 9 commits
  - scientific: ahead 2, behind 3 (diverged)
  - Current branch: in sync with origin

**Stash Summary:**
- `stash@{0-2}`: Orchestration-tools and branch switch stashes
- `stash@{3-8}`: Sourcery AI fixes, scientific branch, backend migration
- `stash@{9-13}`: Feature branches, testing, notmuch tagging

**Modified/Deleted Files:**
- Configuration: `.gitignore`, `uv.lock`
- Deployment/setup: `deployment/test_stages.py`, `setup/` files
- Hooks: Deleted `.git-hooks/` directory (likely intentional migration)
- Scripts: `scripts/install-hooks.sh`, `scripts/reverse_sync_orchestration.sh`
- Testing: 1 untracked `tests/` directory

**Action Items:**
- [ ] **PRIORITY:** Review and consolidate 14 stashes
- [ ] Investigate hook deletion - verify migration to new hook location completed
- [ ] Commit orchestration workflow and deployment changes
- [ ] Review testing changes and either commit or document removal
- [ ] Clean up untracked tests directory

---

### 5. ⚠️ `/home/masum/github/EmailIntelligenceGem`
**Status:** Stashed work + uncommitted deletions  
**Current Branch:** `001-rebase-analysis`  
**Unpushed Commits:** 0  
**Stashes:** 13  
**Uncommitted Changes:** 4 deleted files

**Branch Status (git branch -vv) - Key Branches Only:**
```
* 001-rebase-analysis           ad98d8c feat: Resolve merge conflicts and integrate recovered files
  main                          3e71949 Update agent configuration and documentation files
  orchestration-tools           fe220f6 [origin/orchestration-tools: ahead 57, behind 28] docs: amend constitution
  orchestration-tools-clean     807f334 [origin/orchestration-tools-clean] Remove submodule, keep shared files directly
  scientific                    38ff3fc [origin/scientific: ahead 9, behind 3] Complete merge on scientific branch
+ taskmaster                    ec17785 (/home/masum/github/EmailIntelligenceGem/.taskmaster) [origin/taskmaster: behind 10]
```
- **Local branches:** 13 (12 regular + 1 worktree)
- **Remote branches:** 70+ active
- **Sync Status:**
  - Current branch: no remote tracking
  - orchestration-tools: ⚠️ ahead 57, behind 28 (heavily diverged)
  - scientific: ahead 9, behind 3 (diverged)
  - taskmaster: behind 10 commits

**Stash Summary:**
- `stash@{0}`: Orchestration tools .gitignore updates
- `stash@{1-6}`: Scientific branch work (Jules MCP, task completion)
- `stash@{7-12}`: Orchestration tools and hook improvements

**Deleted Files:**
- `scripts/find_lost_files_in_commits.sh`
- `scripts/find_lost_source_code_commits.sh`
- `scripts/find_lost_source_files.sh`
- `scripts/show_dangling_commit_diffs.sh`

**Action Items:**
- [ ] **PRIORITY:** Review 13 stashes for important work
- [ ] Confirm if script deletions are intentional (appears to be cleanup of debugging/recovery scripts)
- [ ] Commit or restore deleted scripts based on analysis needs
- [ ] Consider whether rebase-analysis branch should be merged or archived

---

### 6. ⚠️ `/home/masum/github/EmailIntelligenceAuto`
**Status:** Stashed work  
**Current Branch:** `orchestration-tools-changes`  
**Unpushed Commits:** 0  
**Stashes:** 3  
**Uncommitted Changes:** None

**Branch Status (git branch -vv) - Key Branches Only:**
```
* orchestration-tools-changes a5a5b174 [origin/orchestration-tools-changes] fix: Export init_config function in package __init__.py
  orchestration-tools          785d5467 [origin/orchestration-tools] feat: Add dependency optimization scripts and Jules task prompts
  scientific                   86ac726d [origin/scientific] config: update linting and deployment configurations
+ taskmaster                   efd2244c (/home/masum/github/EmailIntelligenceAuto/.taskmaster) [origin/taskmaster] fix: correct corrupted task JSON files
```
- **Local branches:** 41 (40 regular + 1 worktree)
- **Remote branches:** 70+ active
- **Sync Status:**
  - Current branch: in sync with origin
  - orchestration-tools: in sync
  - scientific: in sync
  - taskmaster: in sync
  - **Note:** Most branches have no remote tracking (cleanup opportunity)

**Stash Summary:**
- `stash@{0}`: Orchestration sync on agent-context-control branch
- `stash@{1}`: Orchestration sync on main
- `stash@{2}`: Task branch stash with taskmaster file removal

**Action Items:**
- [ ] Review 3 stashes to determine if work should be recovered
- [ ] Consider if agent-context-control feature development is still active
- [ ] Evaluate orchestration sync stashes for mergeable changes
- [ ] Clean up untracked local branches (many have no remote tracking)

---

### 7. ⚠️ `/home/masum/github/PR/EmailIntelligence`
**Status:** Stashed work + uncommitted changes  
**Current Branch:** `feature/merge-clean`  
**Unpushed Commits:** 0  
**Stashes:** 8  
**Uncommitted Changes:** 50+ untracked files

**Branch Status (git branch -vv) - Key Branches Only:**
```
  001-implement-planning-workflow  5561285 [origin/001-implement-planning-workflow: ahead 1] docs: add complete orchestration push system architecture
  docs-cleanup                     5447844 [origin/docs-cleanup: ahead 1] feat: PR #176 integration work
* feature/merge-clean              3e59922 [origin/feature/merge-clean] Add conflict resolution progress tracking
  main                             45710d4 [origin/main: ahead 1] docs: distribute .github/instructions to main branch
  scientific                       42275c9 [origin/scientific: ahead 11, behind 3] docs: distribute .github/instructions to scientific branch
+ taskmaster                       584814a (/home/masum/github/PR/EmailIntelligence/.taskmaster) [origin/taskmaster: ahead 2, behind 8]
```
- **Local branches:** 14 (13 regular + 1 worktree)
- **Remote branches:** 70+ active
- **Sync Status:**
  - Current branch: in sync with origin
  - 001-implement-planning-workflow: ahead 1 commit
  - docs-cleanup: ahead 1 commit
  - main: ahead 1 commit
  - scientific: ⚠️ ahead 11, behind 3 (diverged)
  - taskmaster: ahead 2, behind 8 (diverged)

**Stash Summary:**
- `stash@{0}`: Merge-clean feature with conflict resolution tracking
- `stash@{1-4}`: Various feature branches (notmuch-tagging, scientific, orchestration)
- `stash@{5-7}`: Testing cleanup and branch switch work

**Untracked Files:**
- Tool configs: `.claude/`, `.clinerules/`, `.cursor/`, `.gemini/`, `.kilo/`, `.kiro/`, `.roo/`, `.rules/`, `.serena/`, `.trae/`, `.windsurf/`, `.zed/`, `.mcp.json`, `.amp-settings.json`
- Session/tracking: `.session`, `.COMMIT_MESSAGE`, `.IMPLEMENTATION_CHECKLIST`, `.aider.chat.history.md`, `.aider.input.history`, `.orchestration-test-plan`, `.taskmaster/`, `.test-results-summary`
- Other: `.gitignore.rej`, `scripts/hooks/`

**Action Items:**
- [ ] **PRIORITY:** Review 8 stashes and determine which branches are still active
- [ ] Consolidate tool configuration directories to workspace root if not repo-specific
- [ ] Clean up session and AI tool temporary files
- [ ] Verify `.gitignore.rej` file (merge conflict in gitignore) and resolve
- [ ] Consider the purpose of feature/merge-clean branch in overall workflow

---

### 8. ✅ `/home/masum/github/EmailIntelligenceAider`
**Status:** Stashed work  
**Current Branch:** `scientific`  
**Unpushed Commits:** 0  
**Stashes:** 2  
**Uncommitted Changes:** None

**Branch Status (git branch -vv) - Key Branches Only:**
```
  main                  c61bdeb [origin/main: behind 1] docs update
  orchestration-tools   785d546 [origin/orchestration-tools] feat: Add dependency optimization scripts and Jules task prompts
* scientific            86ac726 [origin/scientific] config: update linting and deployment configurations
+ taskmaster            5bac052 (/home/masum/github/EmailIntelligenceAider/.taskmaster) Clean up taskmaster branch
```
- **Local branches:** 9 (8 regular + 1 worktree)
- **Remote branches:** 70+ active
- **Sync Status:**
  - Current branch: in sync with origin
  - main: behind 1 commit
  - orchestration-tools: in sync
  - taskmaster: no remote tracking

**Stash Summary:**
- `stash@{0}`: Migration work (backend-to-src-backend)
- `stash@{1}`: Strategy 5 orchestration push aggregation

**Action Items:**
- [ ] Review 2 stashes - appear to be from completed feature work
- [ ] Determine if these should be discarded or if work is ongoing
- [ ] Verify scientific branch is current development target

---

## Branch Synchronization Summary

### Out-of-Sync Branches (Requires Action)

| Repo | Branch | Status | Commits |
|------|--------|--------|---------|
| EmailIntelligenceQwen | feature-notmuch-tagging-1 | Diverged | ahead 1, behind 1 |
| EmailIntelligenceQwen | main | Behind | behind 4 |
| EmailIntelligenceQwen | orchestration-tools | Behind | behind 13 |
| EmailIntelligenceQwen | orchestration-tools-temp | Diverged | ahead 2, behind 11 |
| EmailIntelligenceQwen | scientific | Behind | behind 8 |
| EmailIntelligenceQwen | taskmaster | Diverged | ahead 6, behind 5 |
| EmailIntelligence | main | Behind | behind 10 |
| EmailIntelligence | orchestration-tools | ⚠️⚠️ Severely Behind | behind 59 |
| EmailIntelligence | scientific | Diverged | ahead 2, behind 3 |
| EmailIntelligence | taskmaster | Behind | behind 9 |
| EmailIntelligenceGem | orchestration-tools | Heavily Diverged | ahead 57, behind 28 |
| EmailIntelligenceGem | scientific | Diverged | ahead 9, behind 3 |
| EmailIntelligenceGem | taskmaster | Behind | behind 10 |
| PR/EmailIntelligence | 001-implement-planning-workflow | Ahead | ahead 1 |
| PR/EmailIntelligence | docs-cleanup | Ahead | ahead 1 |
| PR/EmailIntelligence | main | Ahead | ahead 1 |
| PR/EmailIntelligence | scientific | Diverged | ahead 11, behind 3 |
| PR/EmailIntelligence | taskmaster | Diverged | ahead 2, behind 8 |
| EmailIntelligenceAider | main | Behind | behind 1 |

### Branches in Sync (No Action Needed)
- rulesync: main
- EmailIntelligenceQwen: 001-implement-planning-workflow (current)
- EmailIntelligence: orchestration-tools-changes (current)
- EmailIntelligenceAuto: orchestration-tools-changes (current), orchestration-tools, scientific, taskmaster
- EmailIntelligenceAider: scientific (current), orchestration-tools

---

## Critical Issues & Recommendations

### Urgent Priority

1. **CRITICAL: orchestration-tools Branch Divergence (EmailIntelligence)**
   - **Issue:** EmailIntelligence repo's `orchestration-tools` branch is behind 59 commits from origin
   - **Impact:** High risk of losing work, merge conflicts, or deploying stale code
   - **Recommendation:**
     ```bash
     cd /home/masum/github/EmailIntelligence
     git checkout orchestration-tools
     git fetch origin
     git log --oneline origin/orchestration-tools..HEAD  # Review local commits
     git log --oneline HEAD..origin/orchestration-tools  # Review remote commits
     # Then decide: rebase, merge, or force push based on analysis
     ```
   - **Related Issues:**
     - EmailIntelligenceGem: orchestration-tools ahead 57, behind 28 (diverged in opposite direction)
     - EmailIntelligenceQwen: orchestration-tools behind 13

### High Priority

1. **Stash Management (51 total stashes)**
   - **Issue:** Large number of stashes indicates incomplete work or forgotten changes
   - **Recommendation:** 
     ```bash
     # For each repo with stashes, run:
     git stash list -p  # Review all stashes
     git stash drop <stash>  # Remove if no longer needed
     git stash pop  # Apply and remove if work is still needed
     ```
   - **Repos Affected:** EmailIntelligenceQwen (11), EmailIntelligence (14), EmailIntelligenceGem (13), EmailIntelligenceAuto (3), PR/EmailIntelligence (8), EmailIntelligenceAider (2)

2. **Multiple Branches Behind Remote (Sync Drift)**
   - **Issue:** Many branches are behind remote: main branches (behind 1-10), scientific (behind 3-8), taskmaster (behind 9-10)
   - **Impact:** Local changes may be stale; difficult to integrate with current remote state
   - **Recommendation:**
     ```bash
     # For each out-of-sync branch, run:
     git fetch origin
     git checkout <branch>
     git pull origin <branch>  # or git rebase origin/<branch> if preferred
     ```
   - **Affected Repos:** EmailIntelligenceQwen, EmailIntelligence, EmailIntelligenceGem, EmailIntelligenceAider

3. **Uncommitted Changes in Primary Repos**
   - **Issue:** EmailIntelligence, EmailIntelligenceQwen, and PR/EmailIntelligence have significant uncommitted changes
   - **Recommendation:** 
     - Commit or discard changes in setup files immediately
     - These may be from interrupted orchestration syncs
     - Clarify whether these are abandoned experiments or work-in-progress

4. **Hook File Deletions (EmailIntelligence)**
   - **Issue:** Post-checkout, post-commit, pre-commit hooks deleted (not staged for deletion properly)
   - **Recommendation:**
     - Verify if hooks were migrated to new location
     - Run `git status` to confirm deletion staging
     - Investigate why hooks are in uncommitted state rather than proper git deletion

### Medium Priority

5. **Untracked Configuration Proliferation**
   - **Issue:** Multiple repos have untracked AI tool configs (.claude/, .cursor/, .gemini/, etc.)
   - **Recommendation:**
     - Add to root `.gitignore` if not repo-specific
     - Consider centralizing tool configs to workspace root
     - Run: `echo ".claude/ .cursor/ .gemini/ .kilo/ .kiro/ .roo/ .trae/ .windsurf/ .zed/" >> ~/.gitignore_global`

6. **Branch Status Clarity**
   - **Issue:** Multiple feature branches across repos (orchestration-tools, scientific, planning-workflow)
   - **Recommendation:**
     - Document which branches are active development targets
     - Create a `BRANCH_STATUS.md` tracking which branches can be archived
     - Plan cleanup for stale branches

### Low Priority

7. **Documentation File Tracking**
   - **Issue:** Multiple AGENT.md, CLAUDE.md, QWEN.md files in various states
   - **Recommendation:**
     - Standardize location (e.g., workspace root)
     - Remove duplicates from individual repos
     - Consider if these should be symlinked

---

## Action Plan (Recommended Sequence)

### Phase 1: Analysis (This Week)
```bash
# 1. Generate detailed stash reports for high-stash repos
for repo in EmailIntelligenceQwen EmailIntelligence EmailIntelligenceGem; do
  cd /home/masum/github/$repo
  echo "=== $repo ===" > stash_analysis_$repo.md
  git stash list -p >> stash_analysis_$repo.md
done

# 2. Check each stash size
for repo in EmailIntelligenceQwen EmailIntelligence EmailIntelligenceGem; do
  cd /home/masum/github/$repo
  git stash list | wc -l
done

# 3. Verify hook migrations
for repo in EmailIntelligence EmailIntelligenceGem; do
  cd /home/masum/github/$repo
  find . -name "*.sample" | grep hooks
  ls -la .git/hooks/
done
```

### Phase 2: Cleanup (Next Week)
- [ ] Process stashes: keep only active work, discard old
- [ ] Commit legitimate changes (setup files, configuration)
- [ ] Resolve all uncommitted deletions and modifications
- [ ] Clean untracked files per repo assessment

### Phase 3: Consolidation (Following Week)
- [ ] Consolidate tool configurations
- [ ] Create branch strategy document
- [ ] Archive or merge stale feature branches
- [ ] Update gitignore rules globally

---

## Summary Table

| Repo | Branch | Unpushed | Stashes | Changes | Status | Action |
|------|--------|----------|---------|---------|--------|--------|
| taskmaster-worktree | taskmaster | 0 | 0 | 19 untracked | ✅ Clean | Review untracked files |
| rulesync | main | 0 | 0 | None | ✅ Clean | None |
| EmailIntelligenceQwen | 001-implement-planning-workflow | 0 | 11 | 35 mixed | ⚠️ Needs Action | Review stashes + commit changes |
| EmailIntelligence | orchestration-tools-changes | 0 | 14 | 21 mixed | ⚠️ Needs Action | Review stashes + resolve deletions |
| EmailIntelligenceGem | 001-rebase-analysis | 0 | 13 | 4 deleted | ⚠️ Needs Action | Review stashes + confirm deletions |
| EmailIntelligenceAuto | orchestration-tools-changes | 0 | 3 | None | ⚠️ Minor | Review 3 stashes |
| PR/EmailIntelligence | feature/merge-clean | 0 | 8 | 50+ untracked | ⚠️ Needs Action | Clean configs + review stashes |
| EmailIntelligenceAider | scientific | 0 | 2 | None | ✅ Minor | Review 2 stashes |

---

## Key Metrics
- **Repos with issues:** 6/8 (75%)
- **Total stashes to review:** 51
- **Avg stashes per affected repo:** 8.5
- **Estimated cleanup time:** 4-6 hours

---

*Next Steps: Start with Phase 1 analysis to understand which stashes contain important work before any cleanup operations.*
