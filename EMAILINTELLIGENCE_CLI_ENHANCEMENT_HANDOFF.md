# EmailIntelligence CLI Enhancement - Comprehensive Handoff Document

**Session Date:** 2026-02-28  
**Target Branch:** `orchestration-tools`  
**Primary Objectives:** Refactor conflict detection with git merge-tree, implement direct branch push workflow, add all-branches scanning capability

---

## 1. Git-Related Work

### 1.1 Primary Refactoring: `_detect_conflicts` with `git merge-tree`

**Current Implementation Location:** `emailintelligence_cli.py` lines 231-258

**Current Code:**
```python
def _detect_conflicts(self, worktree_a_path: Path, worktree_b_path: Path) -> List[Dict[str, Any]]:
    """Detect conflicts between worktrees"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=worktree_a_path,
            check=True, capture_output=True, text=True
        )
        conflicts = []
        for file_path in result.stdout.strip().split('\n'):
            if file_path and not file_path.startswith('.'):
                conflict_info = {
                    'file': file_path,
                    'path_a': str(worktree_a_path / file_path),
                    'path_b': str(worktree_b_path / file_path),
                    'detected_at': datetime.now().isoformat()
                }
                conflicts.append(conflict_info)
        self._info(f"🔍 Detected {len(conflicts)} potential conflicts")
        return conflicts
    except subprocess.CalledProcessError:
        return []
```

**Issue:** Uses `git diff --name-only` which only shows files that differ between branches - NOT actual merge conflict markers. This is a LOW-ACCURACY git command that needs replacement.

---

### 1.2 Complete New Implementation

Add these imports at the top of the file:
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from pathlib import Path
import subprocess
```

Add these new classes BEFORE the EmailIntelligenceCLI class:
```python
class ConflictType(Enum):
    """Types of merge conflicts detected by git merge-tree"""
    CHANGED_IN_BOTH = "changed_in_both"
    ADDED_IN_BOTH = "added_in_both"
    REMOVED_IN_SOURCE = "removed_in_source"
    REMOVED_IN_TARGET = "removed_in_target"
    MODIFIED_DELETED = "modified_deleted"


class ConflictSeverity(Enum):
    """Severity assessment for conflicts"""
    HIGH = "high"      # Both branches modified same areas
    MEDIUM = "medium"  # One branch deleted/modified
    LOW = "low"        # Minor conflicts


@dataclass
class ConflictRegion:
    """Represents a specific conflict region within a file"""
    start_line: int
    end_line: int
    content_ours: str
    content_theirs: str
    content_base: Optional[str] = None


@dataclass
class ConflictFile:
    """Structured conflict information for a single file"""
    file_path: str
    conflict_type: ConflictType
    conflict_regions: List[ConflictRegion] = field(default_factory=list)
    resolution_status: str = "unresolved"  # "unresolved", "resolved_ours", "resolved_theirs", "resolved_manual"
    severity: ConflictSeverity = ConflictSeverity.MEDIUM
    lines_affected: int = 0


@dataclass
class ConflictReport:
    """Complete conflict detection result"""
    source_branch: str
    target_branch: str
    base_branch: str
    conflicts: List[ConflictFile]
    merge_base_commit: str
    detection_method: str = "git merge-tree"
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def total_conflicts(self) -> int:
        return len(self.conflicts)
    
    @property
    def files_requiring_resolution(self) -> List[str]:
        return [c.file_path for c in self.conflicts if c.resolution_status == "unresolved"]
    
    @property
    def severity_summary(self) -> Dict[str, int]:
        summary = {"high": 0, "medium": 0, "low": 0}
        for c in self.conflicts:
            summary[c.severity.value] += 1
        return summary


# Custom Exception Classes
class GitOperationError(Exception):
    """Base exception for git operation failures"""
    pass


class MergeTreeError(GitOperationError):
    """Raised when git merge-tree command fails"""
    pass


class BranchNotFoundError(GitOperationError):
    """Raised when specified branch doesn't exist"""
    pass


class WorktreeUnavailableError(GitOperationError):
    """Raised when worktree operations fail"""
    pass
```

Add these new methods to the EmailIntelligenceCLI class (after line 258):
```python
def detect_conflicts_with_merge_tree(
    self,
    base: str,
    branch_a: str,
    branch_b: str
) -> ConflictReport:
    """
    Detect actual merge conflicts using git merge-tree.
    
    This method replaces the inadequate git diff --name-only approach
    with accurate three-way merge conflict detection.
    
    Args:
        base: Base/common ancestor branch or commit
        branch_a: First branch to compare (source)
        branch_b: Second branch to compare (target)
    
    Returns:
        ConflictReport containing list of ConflictFile objects
    
    Raises:
        MergeTreeError: If git merge-tree command fails
        BranchNotFoundError: If specified branches don't exist
    """
    self._info(f"🔍 Running merge-tree analysis: {branch_a} vs {branch_b}")
    
    # Validate branches exist
    self._validate_branch_exists(branch_a)
    self._validate_branch_exists(branch_b)
    
    # Get merge base for context
    merge_base = self._get_merge_base(branch_a, branch_b)
    
    # Execute merge-tree
    try:
        result = subprocess.run(
            ["git", "merge-tree", "--name-only", base, branch_a, branch_b],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise MergeTreeError(f"git merge-tree failed: {e.stderr}")
    
    # Parse output into ConflictFile objects
    conflicts = self._parse_merge_tree_output(result.stdout, branch_a, branch_b)
    
    return ConflictReport(
        source_branch=branch_a,
        target_branch=branch_b,
        base_branch=base,
        conflicts=conflicts,
        merge_base_commit=merge_base
    )


def _validate_branch_exists(self, branch: str) -> None:
    """Validate that a branch exists"""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        cwd=self.repo_root,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise BranchNotFoundError(f"Branch '{branch}' does not exist")


def _get_merge_base(self, branch_a: str, branch_b: str) -> str:
    """Get the merge base commit between two branches"""
    result = subprocess.run(
        ["git", "merge-base", branch_a, branch_b],
        cwd=self.repo_root,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def _parse_merge_tree_output(
    self,
    output: str,
    branch_a: str,
    branch_b: str
) -> List[ConflictFile]:
    """
    Parse git merge-tree output into structured ConflictFile objects.
    
    Output format:
    - changed in both:  <path>
    - removed in one:   <path>
    - added in both:    <path>
    """
    conflicts = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Parse conflict type and file path
        if line.startswith('changed in both:'):
            file_path = line.split(':', 1)[1].strip()
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=ConflictType.CHANGED_IN_BOTH,
                severity=ConflictSeverity.HIGH  # Both modified = high severity
            ))
            
        elif line.startswith('added in both:'):
            file_path = line.split(':', 1)[1].strip()
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=ConflictType.ADDED_IN_BOTH,
                severity=ConflictSeverity.HIGH
            ))
            
        elif line.startswith('removed in '):
            file_path = line.split(':', 1)[1].strip()
            # Determine which branch removed the file
            if branch_a in line:
                conflict_type = ConflictType.REMOVED_IN_SOURCE
            else:
                conflict_type = ConflictType.REMOVED_IN_TARGET
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=conflict_type,
                severity=ConflictSeverity.MEDIUM
            ))
    
    return conflicts
```

---

### 1.3 Setup-Resolution Modification

**Goal:** Push resolved changes directly to existing branches without creating new branches.

**Current Workflow:**
1. Create pr-{pr}-resolution branch
2. Create worktree-a (source branch)
3. Create worktree-b (target branch)
4. Resolve conflicts
5. Create PR from resolution branch

**New Workflow:**
1. Use existing source branch (no new branch)
2. Use existing target branch (no new branch)
3. Create worktrees pointing to existing branches
4. Resolve conflicts
5. Push directly to source branch via git push --force-with-lease

**New Method to add:**
```python
def setup_resolution_direct(
    self,
    pr_number: int,
    source_branch: str,
    target_branch: str,
    constitution_files: List[str] = None,
    spec_files: List[str] = None,
    dry_run: bool = False,
    direct_push: bool = True
) -> Dict[str, Any]:
    """
    Setup resolution workspace with direct branch push capability.
    
    Key changes:
    - NO pr-{pr}-resolution branch created
    - Works directly with existing source/target branches
    - After resolution, pushes directly to source branch
    """
    
    # Validate branches exist remotely
    self._validate_branches_exist([source_branch, target_branch])
    
    worktree_a_path = self.worktrees_dir / f"pr-{pr_number}-branch-a"
    worktree_b_path = self.worktrees_dir / f"pr-{pr_number}-branch-b"
    
    if not dry_run:
        # Create worktrees pointing to EXISTING branches
        self._create_worktree(worktree_a_path, source_branch)
        self._create_worktree(worktree_b_path, target_branch)
    
    # Use new merge-tree detection
    conflict_report = self.detect_conflicts_with_merge_tree(
        base=target_branch,
        branch_a=source_branch,
        branch_b=target_branch
    )
    
    # Metadata WITHOUT resolution branch reference
    resolution_metadata = {
        'pr_number': pr_number,
        'source_branch': source_branch,
        'target_branch': target_branch,
        'worktree_a_path': str(worktree_a_path),
        'worktree_b_path': str(worktree_b_path),
        'direct_push_enabled': direct_push,
        'modified_branches': [],
        'conflicts': conflict_report.__dict__,
        'resolution_method': 'direct_push',
        'push_operations_log': [],
        'created_at': datetime.now().isoformat(),
        'status': 'ready_for_resolution'
    }
    
    # Save metadata
    metadata_file = self.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(resolution_metadata, f, indent=2)
    
    return resolution_metadata


def push_resolution(
    self,
    pr_number: int,
    confirmed: bool = False,
    branches: List[str] = None,
    force: bool = False
) -> Dict[str, Any]:
    """
    Push resolved changes directly to source branch.
    
    Args:
        pr_number: PR identifier
        confirmed: User must explicitly confirm (required=True)
        branches: List of branches to push to
        force: Use force push
    
    Returns:
        Dict with success status and logs
    """
    # Load metadata
    metadata_file = self.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    source_branch = metadata['source_branch']
    branches = branches or [source_branch]
    
    # Display confirmation prompt if not confirmed
    if not confirmed:
        print(f"⚠️  WARNING: This will force-push to: {branches}")
        print(f"⚠️  This will OVERWRITE existing commits on remote!")
        response = input("Type 'yes' to confirm: ")
        if response.lower() != 'yes':
            return {'success': False, 'reason': 'user_cancelled'}
    
    # Build push command
    push_cmd = ["git", "push"]
    if force:
        push_cmd.append("--force-with-lease")  # Safer than -f
    push_cmd.extend(["origin", f"{metadata['worktree_a_path']}:refs/heads/{source_branch}"])
    
    # Log operation
    operation = {
        'timestamp': datetime.now().isoformat(),
        'branches': branches,
        'command': ' '.join(push_cmd),
        'source_branch': source_branch
    }
    metadata['push_operations_log'].append(operation)
    
    # Execute push
    try:
        subprocess.run(push_cmd, check=True, cwd=metadata['worktree_a_path'])
        metadata['modified_branches'].extend(branches)
        metadata['status'] = 'resolution_pushed'
        
        # Save updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self._success(f"✅ Pushed resolution to {source_branch}")
        return {'success': True, 'branches': branches, 'operation': operation}
        
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': str(e)}


def _validate_branches_exist(self, branches: List[str]) -> None:
    """Validate that all specified branches exist"""
    for branch in branches:
        self._validate_branch_exists(branch)


def _create_worktree(self, path: Path, branch: str) -> None:
    """Create a git worktree at the specified path"""
    subprocess.run(
        ["git", "worktree", "add", str(path), branch],
        cwd=self.repo_root,
        check=True
    )
```

---

### 1.4 All-Branches Scanning Capability

```python
@dataclass
class BranchPairResult:
    """Result for a single branch pair scan"""
    source: str
    target: str
    conflict_count: int
    conflict_files: List[str]
    severity: str
    scan_duration_ms: float


@dataclass
class ConflictMatrix:
    """Complete conflict matrix for all branch pairs"""
    scanned_at: str
    branches: List[str]
    target_branches: List[str]
    total_pairs: int
    pairs_with_conflicts: int
    results: List[BranchPairResult]


def scan_all_branches(
    self,
    include_remotes: bool = True,
    target_branches: List[str] = None,
    concurrency: int = 4,
    exclude_patterns: List[str] = None
) -> ConflictMatrix:
    """
    Scan conflicts across all branch pairs.
    
    Args:
        include_remotes: Include remote branches in scan
        target_branches: Specific target branches (default: ['main'])
        concurrency: Number of parallel scans
        exclude_patterns: Branch patterns to exclude
    
    Returns:
        ConflictMatrix with all results
    """
    import concurrent.futures
    import time
    
    target_branches = target_branches or ['main']
    exclude_patterns = exclude_patterns or ['main', 'develop', 'HEAD']
    
    # Enumerate branches
    branches = self._enumerate_branches(include_remotes, exclude_patterns)
    
    self._info(f"Scanning {len(branches)} branches against {len(target_branches)} targets...")
    
    # Generate branch pairs
    pairs = []
    for source in branches:
        for target in target_branches:
            if source != target:
                pairs.append((source, target))
    
    self._info(f"Scanning {len(pairs)} branch pairs...")
    
    # Scan in parallel
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(self._scan_branch_pair, src, tgt): (src, tgt) 
            for src, tgt in pairs
        }
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            completed += 1
            if completed % 10 == 0:
                self._info(f"Progress: {completed}/{len(pairs)} pairs scanned")
    
    duration_ms = (time.time() - start_time) * 1000
    
    return ConflictMatrix(
        scanned_at=datetime.now().isoformat(),
        branches=branches,
        target_branches=target_branches,
        total_pairs=len(pairs),
        pairs_with_conflicts=sum(1 for r in results if r.conflict_count > 0),
        results=results
    )


def _enumerate_branches(
    self,
    include_remotes: bool = True,
    exclude_patterns: List[str] = None
) -> List[str]:
    """Enumerate all local and remote branches"""
    
    # Get local branches
    result = subprocess.run(
        ["git", "branch", "--format=%(refname:short)"],
        cwd=self.repo_root,
        capture_output=True,
        text=True,
        check=True
    )
    local_branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
    
    # Get remote branches
    if include_remotes:
        result = subprocess.run(
            ["git", "branch", "-r", "--format=%(refname:short)"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        remote_branches = [
            b.strip().replace('origin/', '') 
            for b in result.stdout.split('\n')
            if b.strip() and 'origin/HEAD' not in b
        ]
        local_branches = list(set(local_branches + remote_branches))
    
    # Apply exclusions
    if exclude_patterns:
        local_branches = [
            b for b in local_branches 
            if not any(self._matches_pattern(b, p) for p in exclude_patterns)
        ]
    
    return sorted(local_branches)


def _matches_pattern(self, branch: str, pattern: str) -> bool:
    """Check if branch matches pattern (supports wildcards)"""
    import fnmatch
    return fnmatch.fnmatch(branch, pattern)


def _scan_branch_pair(self, source: str, target: str) -> BranchPairResult:
    """Scan a single branch pair for conflicts"""
    import time
    start = time.time()
    
    try:
        report = self.detect_conflicts_with_merge_tree(target, source, target)
        duration_ms = (time.time() - start) * 1000
        
        # Determine severity
        severity = "low"
        if any(c.severity == ConflictSeverity.HIGH for c in report.conflicts):
            severity = "high"
        elif any(c.severity == ConflictSeverity.MEDIUM for c in report.conflicts):
            severity = "medium"
        
        return BranchPairResult(
            source=source,
            target=target,
            conflict_count=len(report.conflicts),
            conflict_files=[c.file_path for c in report.conflicts],
            severity=severity,
            scan_duration_ms=duration_ms
        )
    except Exception as e:
        return BranchPairResult(
            source=source,
            target=target,
            conflict_count=0,
            conflict_files=[],
            severity="error",
            scan_duration_ms=0
        )
```

---

### 1.5 Worktree Fallback Mechanism

```python
class GitWorkspaceManager:
    """Enhanced workspace manager with fallback support"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.fallback_mode = False
        self.fallback_reason = None
    
    def initialize(self) -> bool:
        """Initialize with automatic fallback detection"""
        try:
            # Check git available
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            
            # Check in repo
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            
            # Verify worktree support
            self._verify_worktree_support()
            
            return True
            
        except FileNotFoundError:
            self._enable_fallback("git_not_installed", "Git is not installed")
            return False
        except subprocess.CalledProcessError:
            self._enable_fallback("not_a_repo", "Not in a git repository")
            return False
        except PermissionError as e:
            self._enable_fallback("permission_denied", str(e))
            return False
    
    def _enable_fallback(self, reason: str, details: str):
        """Enable fallback mode"""
        self.fallback_mode = True
        self.fallback_reason = {
            'reason': reason, 
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        print(f"⚠️  Falling back to single-branch mode: {reason}")
        print(f"   Details: {details}")
    
    def _verify_worktree_support(self):
        """Verify git worktree is supported"""
        result = subprocess.run(
            ["git", "worktree", "--help"],
            capture_output=True
        )
        if result.returncode != 0:
            raise WorktreeUnavailableError("Git worktree not supported")
    
    def create_workspace(
        self, 
        name: str, 
        branch: str,
        use_worktree: bool = True
    ) -> Path:
        """Create workspace with automatic fallback"""
        
        if use_worktree and not self.fallback_mode:
            try:
                return self._create_git_worktree(name, branch)
            except (WorktreeUnavailableError, PermissionError) as e:
                self._enable_fallback("worktree_creation_failed", str(e))
        
        # Fallback: use regular directory
        return self._create_fallback_workspace(name, branch)
    
    def _create_fallback_workspace(self, name: str, branch: str) -> Path:
        """Create workspace without git worktree"""
        
        workspace_dir = self.repo_root / ".emailintelligence" / "workspaces" / name
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Clone at specific branch
        subprocess.run(
            ["git", "clone", "--branch", branch, ".", str(workspace_dir)],
            cwd=self.repo_root,
            capture_output=True,
            check=True
        )
        
        return workspace_dir
```

---

## 2. EmailIntelligence CLI Enhancements

### 2.1 File Analysis: emailintelligence_cli.py

**Location:** Root directory of EmailIntelligence repository  
**Size:** 59,317 characters  
**Key Methods:**

| Method | Line | Purpose |
|--------|------|---------|
| `_detect_conflicts` | 231-258 | NEEDS REFACTORING - uses git diff |
| `setup_resolution` | 103-214 | Creates resolution workspace |
| `analyze_constitutional` | 260-379 | Analyzes conflicts against constitutions |
| `develop_spec_kit_strategy` | 558-623 | Creates resolution strategy |
| `align_content` | 887-967 | Executes content alignment |
| `validate_resolution` | 1069-1118 | Validates resolution |
| argparse setup | 1282-1410 | CLI argument parsing |

**Current Worktree Configuration (from __init__):**
```python
self.repo_root = Path.cwd()
self.worktrees_dir = self.repo_root / ".git" / "worktrees"
self.resolution_branches_dir = self.repo_root / "resolution-workspace"
self.config_file = self.repo_root / ".emailintelligence" / "config.yaml"
self.constitutions_dir = self.repo_root / ".emailintelligence" / "constitutions"
self.strategies_dir = self.repo_root / ".emailintelligence" / "strategies"
```

---

### 2.2 Configuration: .emailintelligence/config.yaml

**Full Content:**
```yaml
analysis_settings:
  detailed_reporting: true
  enable_ai_analysis: false

constitutional_framework:
  compliance_threshold: 0.8
  default_constitutions: []

worktree_settings:
  cleanup_on_completion: true
  max_worktrees: 10
```

---

### 2.3 CLI Commands (from argparse)

| Command | Purpose |
|---------|---------|
| `setup-resolution` | Setup resolution workspace for PR |
| `analyze-constitutional` | Analyze conflicts against constitution |
| `develop-spec-kit-strategy` | Develop resolution strategy |
| `align-content` | Execute content alignment |
| `validate-resolution` | Validate completed resolution |
| `version` | Show version information |

---

## 3. Orchestration-Tools Consolidation

### 3.1 Branches Involved

From `implement/orchestration_tools_consolidation_summary.md`:
- `orchestration-tools` (main consolidation target)
- `orchestration-tools-changes` (aggregation branch)
- `orchestration-tools-changes-2`
- `orchestration-tools-changes-4`
- `orchestration-tools-changes-emailintelligence-cli-20251112`
- `orchestration-tools-changes-recovery-framework`

### 3.2 Files on orchestration-tools

**Scripts:**
- `scripts/hooks/post-push`
- `scripts/hooks/pre-commit`
- `scripts/hooks/post-commit`
- `scripts/hooks/post-merge`
- `scripts/lib/orchestration-approval.sh`

**Setup:**
- `setup/launch.py`
- `setup/setup_environment_system.sh`

**Configuration:**
- `.flake8`
- `.pylintrc`
- `.gitignore`

### 3.3 Current Repository Status

**From git status:**
```
Current Branch: gitbutler/workspace
Main Worktree: C:/Users/masum/Documents/EmailIntelligence
Secondary Worktree: .worktrees/pr481 (prunable)
Remote: origin https://github.com/MasumRab/EmailIntelligence.git
```

### 3.4 Branch Naming Convention

Branches found in repository:
- `bolt-smart-filter-opt-7251234506607923073`
- `bolt/smart-filter-cache-optimization-7932786554965032055`
- `gitbutler/workspace` (current)
- `main`
- `mr-branch-2`, `mr-branch-3`, `mr-branch-4`
- `orchestration-tools`
- `pr-481`
- `scientific`
- `sentinel-fix-xss-fallback-12723436363458782184`

---

## 4. Branch/Merge/Conflict Improvements

### 4.1 Conflict Detection Methods Evaluated

| Method | Accuracy | Worktree Required | Use Case |
|--------|----------|-------------------|----------|
| `git diff --name-only` (CURRENT) | LOW ❌ | Yes | Only shows different files |
| `git merge-tree` | **HIGH ✅** | No | Actual merge conflicts |
| `git ls-files -u` | HIGH | Only during merge | Unmerged files |
| `git diff --merge-base` | MEDIUM | No | Potential conflicts |

**RECOMMENDATION:** Use `git merge-tree` as primary method.

### 4.2 Git Commands to Refactor

| Current (Inadequate) | Replace With |
|---------------------|--------------|
| `git diff --name-only` | `git merge-tree --name-only` |
| `git diff --stat` | `git merge-tree` |
| `git diff HEAD` | `git merge-tree` |

### 4.3 TASKMASTER_ISOLATION_FIX.md Findings

**Issue:** Attempted to whitelist `.taskmaster/**` in orchestration-tools `.gitignore`

**Result:** 
- ❌ Would have tracked taskmaster files in orchestration-tools branch
- ❌ Would have contaminated branch history

**Correct Approach:**
- ✅ Use `.git/info/exclude` alone (not propagated to other branches)

---

## 5. Complete Todo List

| # | Item | Status |
|---|------|--------|
| 1 | Analyze current _detect_conflicts implementation | ✅ Completed |
| 2 | Create comprehensive enhancement plan | ✅ Completed |
| 3 | Refactor _detect_conflicts with git merge-tree | ⏳ Pending |
| 4 | Audit codebase for low-accuracy git commands | ⏳ Pending |
| 5 | Modify setup-resolution for direct push | ⏳ Pending |
| 6 | Implement all-branches scanning capability | ⏳ Pending |
| 7 | Evaluate CodeRabbit integration | ⏳ Pending |
| 8 | Add worktree fallback mechanism | ⏳ Pending |
| 9 | Document technical implementation details | ⏳ Pending |

---

## 6. File Analysis Results

### 6.1 analyze_repo.py

**Location:** Root directory  
**Size:** 10,054 characters

**Functions:**
```python
def get_file_category(filepath):
    """Categorizes a file based on its path and extension."""
    # Categories: Testing, Documentation, Configuration, Scripting, 
    # Core Logic, Frontend, Notebook, Data, Containerization, CI/CD, Assets

def analyze_file(filepath):
    """Analyzes a single file for metrics using AST."""
    # Returns: loc, imports, functions, classes, imports_list

def resolve_import_path(import_name, current_file_path, root_dir):
    """Resolves an import name to a file path."""
    # Supports absolute and relative imports
```

### 6.2 agent-config.json

```json
{
  "api_keys": {
    "google": "YOUR_GOOGLE_API_KEY_HERE_OR_LEAVE_EMPTY",
    "anthropic": "YOUR_ANTHROPIC_API_KEY_HERE_OR_LEAVE_EMPTY",
    "perplexity": "YOUR_PERPLEXITY_API_KEY_HERE_OR_LEAVE_EMPTY",
    "openai": "YOUR_OPENAI_API_KEY_HERE_OR_LEAVE_EMPTY"
  },
  "models": {
    "main": "claude-3-5-sonnet-20241022",
    "research": "perplexity-llama-3.1-sonar-large-128k-online",
    "fallback": "gpt-4o-mini"
  },
  "agents": {...},
  "mcp_servers": {...}
}
```

---

## 7. All Search Findings

### 7.1 emailintelligence_cli.py References

| File | Line | Finding |
|------|------|---------|
| `scripts/hooks/post-push` | 33-34 | `REQUIRED_FILES=("emailintelligence_cli.py", "scripts/bash/create-pr-resolution-spec.sh")` |
| `implement/orchestration_tools_consolidation_summary.md` | 13 | `"emailintelligence_cli.py - Complete EmailIntelligence CLI v2.0 implementation"` |

### 7.2 orchestration-tools References

Found in 300+ docs files including:
- `TASKMASTER_ISOLATION_FIX.md`
- `TASKMASTER_BRANCH_CONVENTIONS.md`
- `docs/ORCHESTRATION_SYSTEM.md`
- `docs/ORCHESTRATION_WORKFLOW.md`
- `docs/ORCHESTRATION_BRANCH_SCOPE.md`
- `docs/AGENT_ORCHESTRATION_CHECKLIST.md`
- `docs/ORCHESTRATION.md`
- `docs/ORCHESTRATION_GITHUB_PROTECTION_SUMMARY.md`

### 7.3 CodeRabbit References

Found in `scripts/branch_rename_migration.py` line 77:
```python
'coderabbitai/utg/f31e8bd',  # Branch name only, NOT integration
```

---

## 8. Conclusions & Decisions

### 8.1 Branch Determination

**DECISION:** `orchestration-tools` is the correct branch for emailintelligence_cli.py  
**RATIONALE:** CLI is a Git-oriented orchestration tool, not application code  
**DATE:** 2026-02-28

### 8.2 Conflict Detection Method

**DECISION:** Use `git merge-tree` as primary conflict detection method  
**RATIONALE:** Provides accurate three-way merge conflict detection without requiring worktrees  
**DATE:** 2026-02-28

### 8.3 Workflow Modification

**DECISION:** Push resolved changes directly to existing source branch  
**RATIONALE:** Eliminates need for pr-{pr}-resolution branch creation, reduces PR count  
**DATE:** 2026-02-28

### 8.4 External Tool Integration

**DECISION:** Keep native implementation, do NOT integrate CodeRabbit  
**RATIONALE:** 
- Adds external dependency
- Limited API access
- Privacy implications (data sent to external service)
- Additional cost (subscription-based)
**DATE:** 2026-02-28

### 8.5 Fallback Mechanism

**DECISION:** Implement graceful fallback for worktree unavailability  
**RATIONALE:** Core functionality should work even without worktree support  
**DATE:** 2026-02-28

---

## 9. Implementation Guide

### 9.1 Starting Commands

```bash
# Checkout orchestration-tools branch
git checkout orchestration-tools
git pull origin orchestration-tools
```

### 9.2 Implementation Order

1. Add new dataclasses and exception classes (lines ~70-100)
2. Add `detect_conflicts_with_merge_tree` method (~line 260)
3. Add helper methods `_validate_branch_exists`, `_get_merge_base`, `_parse_merge_tree_output`
4. Add `setup_resolution_direct` method
5. Add `push_resolution` method with confirmations
6. Add `scan_all_branches` method
7. Add `_enumerate_branches`, `_scan_branch_pair` helpers
8. Add GitWorkspaceManager class for fallback
9. Update argparse to add new commands
10. Write tests
11. Commit and push

### 9.3 Estimated Effort

| Task | Days |
|------|------|
| Refactor conflict detection | 1.0 |
| Audit git commands | 0.5 |
| Modify setup-resolution | 1.0 |
| All-branches scan | 1.5 |
| Worktree fallback | 1.0 |
| Tests | 2.0 |
| Documentation | 1.0 |
| **TOTAL** | **8.0** |

---

## 10. Key Code Locations

| Item | Line Numbers | Notes |
|------|---------------|-------|
| `_detect_conflicts` | 231-258 | NEEDS REFACTORING |
| `setup_resolution` | 103-214 | Modify for direct push |
| `analyze_constitutional` | 260-379 | Works with new conflict detection |
| `develop_spec_kit_strategy` | 558-623 | Uses metadata |
| `align_content` | 887-967 | Uses worktrees |
| `validate_resolution` | 1069-1118 | Final validation |
| argparse | 1282-1410 | Add new commands |

---

*End of Comprehensive Handoff Document*
*Last Updated: 2026-02-28*
*Target Branch: orchestration-tools*
