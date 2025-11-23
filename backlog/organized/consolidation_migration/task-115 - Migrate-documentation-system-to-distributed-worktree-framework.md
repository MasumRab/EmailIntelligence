---
id: task-115
title: Migrate documentation system to distributed worktree framework
status: To Do
assignee: []
created_date: '2025-11-02 01:27'
updated_date: '2025-11-03 18:37'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Migrate the current documentation workflow and shared setup file management to a distributed worktree framework, leveraging a centralized `orchestration-tools` remote branch for all orchestration tools and canonical setup files, with automated distribution via `post-merge` hooks and enhanced cross-worktree synchronization.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Phase 1: Foundation & Assessment completed - New worktree architecture (orchestration-tools branch, post-merge hook) defined, risks and mitigation strategies documented.
- [ ] #2 Phase 2: Orchestration Tools & Setup Files Centralization completed -  remote branch created and populated with all orchestration scripts, Git hooks, and canonical setup files.
- [ ] #3 Phase 3: Automated Distribution & Local Update completed -  hook implemented and tested for automatic distribution;  repurposed and tested for mass local worktree updates.
- [ ] #4 Phase 4: Integration & Deprecation completed - All worktrees successfully updated via new system; old usage: git subtree add   --prefix=<prefix> <commit>
   or: git subtree add   --prefix=<prefix> <repository> <ref>
   or: git subtree merge --prefix=<prefix> <commit>
   or: git subtree split --prefix=<prefix> [<commit>]
   or: git subtree pull  --prefix=<prefix> <repository> <ref>
   or: git subtree push  --prefix=<prefix> <repository> <refspec>

    -h, --help            show the help
    -q, --quiet           quiet
    -d, --debug           show debug messages
    -P, --[no-]prefix ... the name of the subdir to split out

options for 'split' (also: 'push')
    --[no-]annotate ...   add a prefix to commit message of new commits
    -b, --branch ...      create a new branch from the split subtree
    --[no-]ignore-joins   ignore prior --rejoin commits
    --[no-]onto ...       try connecting new tree to an existing one
    --[no-]rejoin         merge the new branch back into HEAD

options for 'add' and 'merge' (also: 'pull', 'split --rejoin', and 'push --rejoin')
    --[no-]squash         merge subtree changes as a single commit
    -m, --message ...     use the given message as the commit message for the merge commit methodology and  references removed from documentation.
- [ ] #5 Phase 5: Validation & Go-Live completed - Comprehensive testing of new system passed, documentation updated, and team trained on new workflow.

- [ ] #6 Phase 1: Foundation & Assessment completed - New worktree architecture (`orchestration-tools` branch, `post-merge` hook) defined, risks and mitigation strategies documented.
- [ ] #7 Phase 2: Orchestration Tools & Setup Files Centralization completed - `orchestration-tools` remote branch created and populated with all orchestration scripts, Git hooks, and canonical setup files.
- [ ] #8 Phase 3: Automated Distribution & Local Update completed - `post-merge` hook implemented and tested for automatic distribution; `sync_setup_worktrees.sh` repurposed and tested for mass local worktree updates.
- [ ] #9 Phase 4: Integration & Deprecation completed - All worktrees successfully updated via new system; old `git subtree` methodology and `launch-setup-fixes` references removed from documentation.
- [ ] #10 Phase 5: Validation & Go-Live completed - Comprehensive testing of new system passed, documentation updated, and team trained on new workflow.
<!-- AC:END -->
