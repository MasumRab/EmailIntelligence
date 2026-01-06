# Task 079: Develop Modular Framework for Parallel Alignment Task Execution

**Status:** Ready for Implementation  
**Priority:** High  
**Effort:** 24-32 hours  
**Complexity:** 8/10  
**Dependencies:** Task 007 (branch alignment strategy framework complete)  
**Blocks:** Task 080 (Validation Framework Integration), Task 083 (E2E Testing and Reporting)

---

## Purpose

Develop a modular Python orchestration framework that executes branch alignment tasks in parallel, grouped by their target primary branch (main, scientific, orchestration-tools). This is an **ALIGNMENT PROCESS TASK** - a tool for the alignment workflow, not a feature branch requiring independent development.

**Scope:** Orchestrator framework only  
**Focus:** Safe parallel execution with error handling and monitoring  
**Blocks:** Validation integration (Task 080) and E2E testing (Task 083)

---

## Success Criteria

Task 079 is complete when:

### Core Functionality
- [ ] `BranchAlignmentOrchestrator` class implemented and tested
- [ ] Reads categorized branches from Task 007 output (categorized_branches.json)
- [ ] Groups branches by primary target (main, scientific, orchestration-tools)
- [ ] Executes branch alignment tasks in parallel within each target group
- [ ] Integrates primary changes (calls to Task 077 logic)
- [ ] Detects errors (integrates Task 076 error detection)
- [ ] Generates changes documentation (integrates Task 078 logic)
- [ ] Returns structured results dict with per-branch status
- [ ] Handles all edge cases: empty branch lists, single branches, large branch counts
- [ ] Output matches specification exactly

### Safety & Resilience
- [ ] Parallel execution prevents race conditions (isolated working directories or temporary clones)
- [ ] Rollback procedures implemented for failed branch alignments
- [ ] Resource management enforced (max_workers limits, memory bounds)
- [ ] Circuit breaker pattern prevents cascading failures
- [ ] Graceful degradation on partial failures
- [ ] No data loss on error

### Quality Assurance
- [ ] Unit tests pass (minimum 8 test cases with >95% coverage)
- [ ] No exceptions raised for valid inputs (comprehensive error handling)
- [ ] Performance: <30 seconds per target group (50 branches total)
- [ ] Memory: <200 MB peak usage
- [ ] Code quality: PEP 8 compliant, comprehensive docstrings
- [ ] Concurrent logging works without corruption
- [ ] Thread/process safety verified in tests

### Integration Readiness
- [ ] Compatible with Task 080 (Validation Framework) input requirements
- [ ] Output format matches specification exactly
- [ ] Configuration externalized and validated
- [ ] Documentation complete and accurate
- [ ] Clear error reporting for downstream tasks

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 007 (branch alignment framework) complete with ALIGNMENT_CHECKLIST.md
- [ ] categorized_branches.json output from Task 007 available
- [ ] Python 3.8+ with concurrent.futures module
- [ ] Git installed and accessible via subprocess
- [ ] Test infrastructure in place
- [ ] Understanding of Task 076 (error detection), 077 (integration), 078 (documentation)

### Blocks (What This Task Unblocks)
- Task 080 (Validation Framework Integration) - requires orchestrator framework
- Task 083 (E2E Testing and Reporting) - requires working orchestrator
- All alignment execution work depends on this framework

### External Dependencies
- Python subprocess (built-in)
- concurrent.futures (built-in)
- Standard library: json, logging, typing, threading
- Task 076 error detection module (assumed available)
- Task 077 integration utility (assumed available)
- Task 078 documentation generator (assumed available)

---

## Sub-subtasks

### 079.1: Design Orchestrator Architecture
**Effort:** 2-3 hours  
**Depends on:** None

**Steps:**
1. Design high-level orchestrator class structure
2. Document target group isolation strategy (sequential vs parallel groups)
3. Design parallel execution within groups (ThreadPoolExecutor approach)
4. Define branch processing pipeline (integrate → error-detect → document)
5. Document rollback and recovery strategy

**Success Criteria:**
- [ ] Architecture documented with flow diagrams
- [ ] Target group handling specified
- [ ] Parallel execution strategy clear
- [ ] Integration points with Tasks 076, 077, 078 defined
- [ ] Rollback strategy documented

---

### 079.2: Implement Branch Loading & Grouping
**Effort:** 3-4 hours  
**Depends on:** 079.1

**Steps:**
1. Implement JSON file loading for categorized_branches.json
2. Validate branch data structure (required fields)
3. Implement grouping by target branch (main/scientific/orchestration-tools)
4. Implement branch sorting/ordering within groups
5. Add comprehensive error handling for missing/invalid data

**Success Criteria:**
- [ ] Loads categorized_branches.json without errors
- [ ] Groups branches by target correctly
- [ ] Handles missing/empty branch lists gracefully
- [ ] Validates all required fields present
- [ ] Clear error messages for invalid data

---

### 079.3: Implement Parallel Execution Engine
**Effort:** 4-5 hours  
**Depends on:** 079.2

**Steps:**
1. Implement ThreadPoolExecutor setup with configurable max_workers
2. Implement run_alignment_for_branch function signature
3. Implement group-by-group execution loop
4. Implement task submission and future handling
5. Implement exception handling per branch

**Success Criteria:**
- [ ] Executes branches in parallel within target groups
- [ ] All branches process to completion (successful or failed)
- [ ] Individual branch failures don't stop other branches
- [ ] Thread/process safety verified
- [ ] Performance: <30s for 50 branches

---

### 079.4: Integrate Primary Change Logic (Task 077)
**Effort:** 3-4 hours  
**Depends on:** 079.3

**Steps:**
1. Define integration interface with Task 077 module
2. Implement call to integrate_primary_changes function
3. Handle integration success/failure return values
4. Implement state tracking (pre/post integration)
5. Add logging for integration operations

**Success Criteria:**
- [ ] Calls Task 077 logic correctly for each branch
- [ ] Captures integration success/failure status
- [ ] Logs integration operations
- [ ] Handles integration exceptions gracefully
- [ ] State changes tracked properly

---

### 079.5: Implement Error Detection (Task 076)
**Effort:** 3-4 hours  
**Depends on:** 079.4

**Steps:**
1. Define error detection interface with Task 076 module
2. Implement call to run_error_detection function
3. Parse and classify detected errors
4. Create error report structure
5. Add error logging and context preservation

**Success Criteria:**
- [ ] Calls Task 076 error detection after integration
- [ ] Classifies errors by severity
- [ ] Creates detailed error reports
- [ ] Preserves error context for downstream tasks
- [ ] Error information useful for Task 080

---

### 079.6: Implement Rollback & Recovery
**Effort:** 3-4 hours  
**Depends on:** 079.5

**Steps:**
1. Implement backup branch creation before alignment
2. Implement rollback on integration failure
3. Implement rollback on error detection failure
4. Test rollback procedures with mock failures
5. Document recovery procedures

**Success Criteria:**
- [ ] Creates backup branches (backup-<branch>-pre-align naming)
- [ ] Rolls back successfully on integration failure
- [ ] Rolls back on error detection issues
- [ ] No data loss on rollback
- [ ] Recovery procedures clear and tested

---

### 079.7: Implement Monitoring, Logging & Circuit Breaker
**Effort:** 3-4 hours  
**Depends on:** 079.6

**Steps:**
1. Implement comprehensive logging throughout pipeline
2. Implement progress tracking (X of Y branches processed)
3. Implement status reporting per branch and per target group
4. Implement circuit breaker (stop on N% failure rate)
5. Implement audit trail (start/end times, outcomes)

**Success Criteria:**
- [ ] Logs all operations with context (branch, target, action)
- [ ] Progress tracking visible and helpful
- [ ] Status reports accurate and up-to-date
- [ ] Circuit breaker stops cascade failures
- [ ] Audit trail complete for debugging

---

### 079.8: Write Unit Tests & Validate Output
**Effort:** 3-4 hours  
**Depends on:** 079.7

**Steps:**
1. Create test fixtures with mock branch data
2. Implement 8+ unit test cases
3. Mock external dependencies (Task 076, 077, 078)
4. Test parallel execution safety
5. Test error handling and recovery
6. Generate coverage report (>95%)
7. Validate output against specification

**Success Criteria:**
- [ ] 8+ comprehensive test cases
- [ ] All tests pass consistently
- [ ] Code coverage >95%
- [ ] Parallel safety verified
- [ ] Output matches specification

---

## Specification

### Input Format

Reads from `categorized_branches.json` (output from Task 007):

```json
{
  "branches": [
    {
      "branch_name": "feature/auth",
      "assigned_target": "main",
      "confidence": 0.87,
      "tags": ["tag:main_branch", "tag:parallel_safe"],
      "cluster_id": 0
    },
    {
      "branch_name": "feature/research",
      "assigned_target": "scientific",
      "confidence": 0.72,
      "tags": ["tag:scientific_branch"],
      "cluster_id": 1
    }
  ]
}
```

### Output Format

```json
{
  "orchestration_results": {
    "main": {
      "target_branch": "main",
      "processed_branches": 4,
      "successful": 3,
      "failed": 1,
      "branches": [
        {
          "branch_name": "feature/auth",
          "status": "completed",
          "integration_time_seconds": 12.5,
          "errors_detected": [],
          "changes_summary": "string reference to generated doc"
        },
        {
          "branch_name": "feature/security-fix",
          "status": "failed_integration",
          "integration_time_seconds": 8.2,
          "error_message": "Merge conflict in src/auth.py (unresolvable)",
          "errors_detected": ["merge_conflict_unresolvable"]
        }
      ]
    },
    "scientific": {
      "target_branch": "scientific",
      "processed_branches": 2,
      "successful": 2,
      "failed": 0,
      "branches": [...]
    },
    "orchestration-tools": {
      "target_branch": "orchestration-tools",
      "processed_branches": 1,
      "successful": 1,
      "failed": 0,
      "branches": [...]
    }
  },
  "overall_summary": {
    "total_branches_processed": 7,
    "total_successful": 6,
    "total_failed": 1,
    "total_time_seconds": 45.3,
    "circuit_breaker_triggered": false,
    "execution_timestamp": "2025-12-22T14:30:00Z"
  }
}
```

### run_alignment_for_branch Function Signature

```python
def run_alignment_for_branch(
    branch_name: str,
    target_branch: str,
    repo_path: str,
    integration_utility: object,  # Task 077
    error_detector: object,       # Task 076
    doc_generator: object         # Task 078
) -> dict:
    """
    Execute alignment for a single branch.
    
    Returns:
        {
            'branch_name': str,
            'status': 'completed|failed_integration|failed_error_detection|exception',
            'integration_time_seconds': float,
            'errors_detected': [str],  # Error codes from Task 076
            'error_message': str (if failed),
            'changes_summary': str (if successful)
        }
    """
```

### Configuration Parameters

```yaml
orchestration:
  # Parallel execution settings
  enable_parallelization: true
  max_workers_per_target: 4
  
  # Timeout settings
  branch_alignment_timeout_seconds: 300
  integration_timeout_seconds: 60
  error_detection_timeout_seconds: 30
  
  # Rollback settings
  enable_backup_branches: true
  backup_branch_prefix: "backup"
  auto_cleanup_backups: false
  
  # Circuit breaker settings
  enable_circuit_breaker: true
  failure_threshold_percent: 50
  failure_threshold_count: 5
  
  # Logging settings
  log_level: "INFO"
  log_per_branch: true
  audit_trail_enabled: true
  
  # Resource management
  max_memory_mb: 500
  max_concurrent_git_ops: 8
```

---

## Performance Targets

### Per Component
- Branch alignment: <10 seconds (small branches)
- Integration (Task 077): <30 seconds
- Error detection (Task 076): <15 seconds
- Documentation (Task 078): <5 seconds

### Full Pipeline
- 7 branches (mixed targets): <60 seconds
- 50 branches: <300 seconds
- 100 branches: <600 seconds

### Resource Usage
- Memory: <200 MB peak
- CPU: Efficient parallelization (3-4x speedup for 4 workers)
- Disk: Backup branches <100 MB

---

## Testing Strategy

### Unit Tests

Minimum 8 test cases:

```python
def test_load_categorized_branches():
    """Load and parse categorized_branches.json"""
    
def test_group_branches_by_target():
    """Branches grouped correctly by target"""
    
def test_parallel_execution_within_group():
    """All branches in target group execute in parallel"""
    
def test_sequential_execution_between_groups():
    """Target groups process sequentially or isolated"""
    
def test_rollback_on_integration_failure():
    """Rollback succeeds when integration fails"""
    
def test_error_detection_integration():
    """Error detection runs and results captured"""
    
def test_circuit_breaker_stops_cascade():
    """Circuit breaker stops on failure threshold"""
    
def test_output_schema_validation():
    """Output matches specification exactly"""
```

### Integration Tests

```python
def test_full_orchestration_mixed_targets():
    """Full workflow with branches for all three targets"""
    
def test_error_handling_and_recovery():
    """Error conditions handled gracefully"""
    
def test_parallel_safety_no_race_conditions():
    """No race conditions in concurrent execution"""
```

### Coverage Target
- Code coverage: >95%
- All error paths tested
- All edge cases (empty, single branch, large counts)

---

## Common Gotchas & Solutions

**Gotcha 1: Race conditions in git operations**
```python
# WRONG: Multiple threads modifying same working directory
for branch_info in branches:
    executor.submit(run_alignment_for_branch, branch_info)

# RIGHT: Each thread operates on isolated clone or unique branch
def run_alignment_for_branch(branch_info, isolated_workdir):
    # Each thread has its own git working directory
    subprocess.run(['git', 'fetch'], cwd=isolated_workdir)
```

**Gotcha 2: Logging corruption from concurrent threads**
```python
# WRONG: Multiple threads writing to same file
open('alignment.log', 'a').write(message)

# RIGHT: Use thread-safe logging
import logging
logger = logging.getLogger(__name__)
# Logging module handles thread safety
logger.info(message)
```

**Gotcha 3: Resource exhaustion with too many workers**
```python
# WRONG: Unbounded thread pool
with ThreadPoolExecutor() as executor:  # defaults to too many
    for branch in branches:
        executor.submit(heavy_operation, branch)

# RIGHT: Bound number of workers
with ThreadPoolExecutor(max_workers=4) as executor:
    for branch in branches:
        executor.submit(heavy_operation, branch)
```

**Gotcha 4: Rollback branch left behind on crash**
```python
# WRONG: Create backup, then crash before cleanup
git checkout -b backup-branch feature-branch
# ... crash happens ...

# RIGHT: Always clean up with try/finally
try:
    git checkout -b backup-branch feature-branch
    # ... work ...
finally:
    git branch -D backup-branch  # Clean up on success or failure
```

**Gotcha 5: Circuit breaker threshold too sensitive**
```python
# WRONG: Circuit breaker triggers on any failure
if failure_count >= 1:
    stop_all_tasks()  # Too aggressive

# RIGHT: Trigger only on significant failure rate
if failure_count >= 5 and failure_rate >= 0.50:
    stop_all_tasks()  # Reasonable threshold
```

---

## CLI Integration and Factory Pattern Guidance

This section incorporates proven CLI integration and factory pattern strategies from the guidance/ directory, based on successful implementation of modular frameworks for safe feature adoption.

### Factory Pattern for Service Compatibility

#### Why Factory Pattern is Critical for Orchestration

The factory pattern enables the orchestrator to work with branches that have different service startup patterns:

**Benefits for Orchestration:**
1. **Service Startup Compatibility**: Works with both `uvicorn src.main:create_app --factory` and direct instantiation
2. **Flexibility**: Allows gradual migration between architectures
3. **Preservation**: Maintains all existing functionality during alignment
4. **Testing**: Enables testing of both startup patterns

#### Factory Pattern Implementation Template

```python
# src/main.py
from fastapi import FastAPI
from typing import Optional

def create_app(
    config: Optional[dict] = None,
    enable_context_control: bool = True
) -> FastAPI:
    """
    Factory function compatible with both architectural approaches.
    
    This function bridges different service startup patterns:
    - Remote branch expects: uvicorn src.main:create_app --factory
    - Local branch uses: uvicorn src.main:app (direct instantiation)
    
    Args:
        config: Optional configuration dictionary
        enable_context_control: Whether to enable context control patterns
        
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="EmailIntelligence CLI",
        description="Advanced CLI with constitutional analysis and conflict resolution",
        version="1.0.0"
    )
    
    # Register routes
    register_routes(app)
    
    # Configure middleware
    configure_middleware(app)
    
    # Enable context control if requested
    if enable_context_control:
        enable_context_control_patterns(app)
    
    # Configure error handlers
    configure_error_handlers(app)
    
    return app

def register_routes(app: FastAPI) -> None:
    """Register all application routes"""
    from src.api.routes import (
        conflict_routes,
        analysis_routes,
        resolution_routes
    )
    
    app.include_router(conflict_routes.router, prefix="/api/conflicts")
    app.include_router(analysis_routes.router, prefix="/api/analysis")
    app.include_router(resolution_routes.router, prefix="/api/resolution")

def configure_middleware(app: FastAPI) -> None:
    """Configure application middleware"""
    from fastapi.middleware.cors import CORSMiddleware
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

def enable_context_control_patterns(app: FastAPI) -> None:
    """Enable context control patterns from remote branch"""
    from src.context.control import ContextManager
    
    context_manager = ContextManager()
    app.state.context_manager = context_manager
    
    @app.on_event("startup")
    async def startup_context():
        await context_manager.initialize()

def configure_error_handlers(app: FastAPI) -> None:
    """Configure error handlers"""
    from src.core.exceptions import (
        ConflictDetectionError,
        AnalysisError,
        ResolutionError
    )
    
    @app.exception_handler(ConflictDetectionError)
    async def conflict_detection_handler(request, exc):
        return {"error": "Conflict detection failed", "details": str(exc)}

    @app.exception_handler(AnalysisError)
    async def analysis_error_handler(request, exc):
        return {"error": "Analysis failed", "details": str(exc)}

    @app.exception_handler(ResolutionError)
    async def resolution_error_handler(request, exc):
        return {"error": "Resolution failed", "details": str(exc)}
```

#### Integration with Orchestrator

When the orchestrator processes branches with different architectures:

```python
# In orchestrator.py
def run_alignment_for_branch(branch_name: str, target_branch: str):
    """
    Execute alignment for a branch with factory pattern support.
    """
    # Check if branch uses factory pattern
    uses_factory = check_factory_pattern_support(branch_name)
    
    if uses_factory:
        # Use factory pattern for service startup
        startup_cmd = ["uvicorn", "src.main:create_app", "--factory"]
    else:
        # Use direct instantiation
        startup_cmd = ["uvicorn", "src.main:app"]
    
    # Execute alignment with appropriate startup pattern
    result = execute_alignment(
        branch_name=branch_name,
        target_branch=target_branch,
        startup_cmd=startup_cmd
    )
    
    return result

def check_factory_pattern_support(branch_name: str) -> bool:
    """
    Check if branch supports factory pattern.
    
    Returns True if src/main.py contains create_app() function.
    """
    import subprocess
    
    try:
        # Check for create_app function in src/main.py
        result = subprocess.run(
            ["git", "show", f"{branch_name}:src/main.py"],
            capture_output=True,
            text=True
        )
        
        return "def create_app" in result.stdout
    except subprocess.CalledProcessError:
        return False
```

### CLI Integration Framework

#### Framework Components

The CLI integration framework provides modular, non-interfering feature adoption:

```
.cli_framework/
├── install.sh              # Installation script with multiple modes
├── merge_to_branch.sh      # Safe merge script for other branches
├── config.json             # Framework configuration
└── modules/
    ├── conflict_detector.py
    ├── constitutional_analyzer.py
    └── resolution_engine.py
```

#### Installation Modes

**1. Minimal Mode**
```bash
./install.sh --mode minimal
```
- Core CLI functionality only
- Essential conflict detection
- Basic resolution capabilities

**2. Full Mode**
```bash
./install.sh --mode full
```
- All CLI features with dependencies
- Advanced constitutional analysis
- Complete resolution engine
- Performance optimizations

**3. Custom Mode**
```bash
./install.sh --mode custom --modules conflict_detector,constitutional_analyzer
```
- Selected components only
- Flexible dependency management
- Modular installation approach

#### Non-Interference Policy

The framework follows strict non-interference policies:

1. **Preserve Existing Files**
   - Never overwrite existing files without backup
   - Create automatic backups before modifications
   - Use versioned file names for new files

2. **Modular Installation**
   - Each component is independent
   - Can install/uninstall modules individually
   - No tight coupling between modules

3. **Rollback Capability**
   - Every installation creates rollback script
   - Can revert to previous state
   - No permanent changes without confirmation

#### Integration with Orchestrator

```python
# In orchestrator.py
class BranchAlignmentOrchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.cli_framework = None
        
    def initialize_cli_framework(self, mode: str = "minimal"):
        """
        Initialize CLI integration framework.
        
        Args:
            mode: Installation mode (minimal, full, custom)
        """
        from cli_framework.installer import CLIInstaller
        
        installer = CLIInstaller(mode=mode)
        self.cli_framework = installer.install()
        
        # Validate installation
        self._validate_cli_installation()
    
    def _validate_cli_installation(self):
        """Validate CLI framework installation"""
        required_modules = [
            "conflict_detector",
            "constitutional_analyzer",
            "resolution_engine"
        ]
        
        for module in required_modules:
            if not self.cli_framework.has_module(module):
                raise RuntimeError(
                    f"Required module {module} not installed"
                )
```

### Interface-Based Architecture

#### Core Interfaces

Define interfaces for key components to enable flexibility:

```python
# src/core/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.core.conflict_models import Conflict

class IConflictDetector(ABC):
    """Interface for conflict detection"""
    
    @abstractmethod
    async def detect_conflicts(
        self,
        pr_id: str,
        target_branch: str
    ) -> List[Conflict]:
        """Detect conflicts in a pull request"""
        pass
    
    @abstractmethod
    def get_conflict_summary(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """Generate summary of detected conflicts"""
        pass

class IConstitutionalAnalyzer(ABC):
    """Interface for constitutional analysis"""
    
    @abstractmethod
    async def analyze_constitutional_compliance(
        self,
        pr_id: str,
        target_branch: str
    ) -> Dict[str, Any]:
        """Analyze constitutional compliance"""
        pass
    
    @abstractmethod
    def get_compliance_report(self, analysis: Dict[str, Any]) -> str:
        """Generate compliance report"""
        pass

class IResolver(ABC):
    """Interface for conflict resolution"""
    
    @abstractmethod
    async def resolve_conflict(
        self,
        conflict: Conflict,
        strategy: str
    ) -> bool:
        """Resolve a specific conflict"""
        pass
    
    @abstractmethod
    def get_resolution_summary(self) -> Dict[str, Any]:
        """Get summary of resolutions performed"""
        pass
```

#### Implementation Example

```python
# src/analysis/conflict_analyzer.py
from src.core.interfaces import IConflictDetector
from src.core.conflict_models import Conflict
from src.git.repository import RepositoryOperations

class ConflictDetector(IConflictDetector):
    """Implementation of conflict detection interface"""
    
    def __init__(self, repo_path: str):
        self.repo_ops = RepositoryOperations(repo_path)
    
    async def detect_conflicts(
        self,
        pr_id: str,
        target_branch: str
    ) -> List[Conflict]:
        """Detect conflicts in a pull request"""
        # Fetch PR information
        pr_info = await self._get_pr_info(pr_id)
        
        # Analyze conflicts
        conflicts = []
        for file_path in pr_info['changed_files']:
            file_conflicts = await self._analyze_file_conflicts(
                file_path,
                target_branch
            )
            conflicts.extend(file_conflicts)
        
        return conflicts
    
    async def get_conflict_summary(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """Generate summary of detected conflicts"""
        return {
            'total_conflicts': len(conflicts),
            'by_severity': self._group_by_severity(conflicts),
            'by_type': self._group_by_type(conflicts),
            'files_affected': len(set(c.file_path for c in conflicts))
        }
```

### Repository Operations for Orchestration

#### Git Operations Module

```python
# src/git/repository.py
from pathlib import Path
from typing import List, Tuple, Optional
import subprocess

class RepositoryOperations:
    """Git repository operations for orchestration"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
    
    async def run_command(
        self,
        cmd: List[str],
        cwd: Optional[str] = None
    ) -> Tuple[str, str, int]:
        """
        Execute git command with error handling.
        
        Returns:
            Tuple of (stdout, stderr, exit_code)
        """
        working_dir = cwd or str(self.repo_path)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Command failed: {' '.join(cmd)}\n"
                f"Error: {e.stderr}"
            )
    
    async def create_backup_branch(
        self,
        source_branch: str,
        backup_name: str
    ) -> bool:
        """Create backup branch before alignment"""
        try:
            # Checkout source branch
            await self.run_command(
                ['git', 'checkout', source_branch]
            )
            
            # Create backup branch
            await self.run_command(
                ['git', 'checkout', '-b', backup_name]
            )
            
            return True
            
        except Exception as e:
            raise RuntimeError(
                f"Failed to create backup branch: {str(e)}"
            )
    
    async def rollback_to_backup(
        self,
        backup_branch: str,
        target_branch: str
    ) -> bool:
        """Rollback to backup branch"""
        try:
            # Checkout backup branch
            await self.run_command(
                ['git', 'checkout', backup_branch]
            )
            
            # Force reset target branch
            await self.run_command(
                ['git', 'checkout', target_branch]
            )
            await self.run_command(
                ['git', 'reset', '--hard', backup_branch]
            )
            
            return True
            
        except Exception as e:
            raise RuntimeError(
                f"Failed to rollback: {str(e)}"
            )
```

### Context Control Integration

#### What is Context Control?

Context control is a pattern from the remote branch for managing execution context:

- **Isolation**: Separate execution contexts for different operations
- **Performance Optimization**: Efficient resource management
- **Error Handling**: Comprehensive error detection and recovery

#### Integration Strategy

```python
# src/context/control.py
from typing import Dict, Any, Optional

class ContextManager:
    """Manages execution context for operations"""
    
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.active_context: Optional[str] = None
    
    async def initialize(self):
        """Initialize context manager"""
        # Load configuration
        self.config = await self._load_config()
        
        # Initialize default context
        await self.create_context("default")
    
    async def create_context(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new execution context"""
        context = {
            'name': name,
            'config': config or {},
            'state': {},
            'isolation_level': 'process',
            'performance_mode': 'balanced'
        }
        
        self.contexts[name] = context
        return context
    
    async def activate_context(self, name: str):
        """Activate a specific context"""
        if name not in self.contexts:
            raise ValueError(f"Context {name} not found")
        
        self.active_context = name
    
    async def get_active_context(self) -> Dict[str, Any]:
        """Get currently active context"""
        if not self.active_context:
            raise ValueError("No active context")
        
        return self.contexts[self.active_context]
```

#### Integration with Orchestrator

```python
# In orchestrator.py
class BranchAlignmentOrchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.context_manager = None
        
    async def initialize_context_control(self):
        """Initialize context control for orchestration"""
        from src.context.control import ContextManager
        
        self.context_manager = ContextManager()
        await self.context_manager.initialize()
        
        # Create context for each target group
        for target in ['main', 'scientific', 'orchestration-tools']:
            await self.context_manager.create_context(
                name=f"target_{target}",
                config={
                    'isolation_level': 'process',
                    'performance_mode': 'optimized'
                }
            )
    
    async def execute_with_context(
        self,
        branch_name: str,
        target_branch: str,
        operation: callable
    ):
        """Execute operation with appropriate context"""
        context_name = f"target_{target_branch}"
        
        # Activate target-specific context
        await self.context_manager.activate_context(context_name)
        
        # Execute operation
        try:
            result = await operation(branch_name, target_branch)
            return result
        finally:
            # Cleanup context
            await self.context_manager.cleanup_context(context_name)
```

### Best Practices for Orchestration

#### 1. Always Use Factory Pattern for Service Compatibility

**When to Use:**
- Branches have different service startup patterns
- Need to support multiple architectures
- Want flexibility in deployment

**Implementation:**
```python
# Always check for factory pattern support
if has_factory_pattern(branch):
    startup_cmd = ["uvicorn", "src.main:create_app", "--factory"]
else:
    startup_cmd = ["uvicorn", "src.main:app"]
```

#### 2. Use Interface-Based Architecture

**Benefits:**
- Enables testing with mocks
- Facilitates multiple implementations
- Supports dependency injection
- Improves code maintainability

**Example:**
```python
# Define interface
class IConflictDetector(ABC):
    @abstractmethod
    async def detect_conflicts(self, pr_id: str) -> List[Conflict]:
        pass

# Implement interface
class ConflictDetector(IConflictDetector):
    async def detect_conflicts(self, pr_id: str) -> List[Conflict]:
        # Implementation
        pass

# Use interface in orchestrator
detector: IConflictDetector = ConflictDetector()
conflicts = await detector.detect_conflicts(pr_id)
```

#### 3. Implement Comprehensive Error Handling

**Pattern:**
```python
try:
    result = await operation()
except SpecificException as e:
    # Handle specific error
    logger.error(f"Specific error: {str(e)}")
    await rollback()
    raise
except Exception as e:
    # Handle unexpected error
    logger.error(f"Unexpected error: {str(e)}")
    await rollback()
    raise
finally:
    # Cleanup
    await cleanup()
```

#### 4. Use Non-Interference Policies

**Principles:**
- Never overwrite without backup
- Create automatic backups
- Use versioned file names
- Enable rollback capability

**Implementation:**
```python
def safe_modify_file(file_path: str, modifications: callable):
    """Safely modify file with backup"""
    # Create backup
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    
    try:
        # Apply modifications
        modifications(file_path)
    except Exception as e:
        # Restore from backup
        shutil.copy2(backup_path, file_path)
        raise
```

#### 5. Validate After Each Step

**Checklist:**
```python
async def validate_after_step(step_name: str):
    """Validate after each orchestration step"""
    checks = [
        check_service_startup,
        check_import_paths,
        check_functionality,
        check_performance
    ]
    
    for check in checks:
        result = await check()
        if not result['passed']:
            raise ValidationError(
                f"{step_name} validation failed: {result['message']}"
            )
```

---

## Helper Tools (Optional)

The following tools are available to accelerate work or provide validation. **None are required** - every task is completable using only the steps in this file.

### Progress Logging

After completing each sub-subtask, optionally log progress for multi-session continuity:

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()

# After completing sub-subtask 079.4
memory.add_work_log(
    action="Completed Task 079.4: Integrate Primary Change Logic",
    details="integrate_primary_changes integration complete, state tracking implemented, 12 test cases passing"
)
memory.update_todo("task_079_4", "completed")
memory.save_session()
```

**What this does:** Maintains session state across work sessions, enables agent handoffs, documents progress.  
**Required?** No - git commits are sufficient.  
**See:** MEMORY_API_FOR_TASKS.md for full usage patterns and examples.

### Performance Profiling

After completing sub-subtask 079.7, optionally profile execution:

```bash
python -m cProfile -s cumulative src/orchestration/orchestrator.py \
  --input categorized_branches.json \
  --output-stats stats.prof
```

**What this does:** Identifies performance bottlenecks in orchestrator.  
**Required?** No - performance testing sufficient.  
**See:** SCRIPTS_IN_TASK_WORKFLOW.md for profiling utilities.

---

## Tools Reference

| Tool | Purpose | When to Use | Required? |
|------|---------|-----------|----------|
| Memory API | Progress logging | After each sub-subtask | No |
| cProfile | Performance profiling | After 079.7 | No |
| next_task.py | Find next task | After completion | No |

**For detailed usage and troubleshooting:** See SCRIPTS_IN_TASK_WORKFLOW.md (all optional tools documented there)

---

## Integration Checkpoint

**When to move to Task 080 (Validation Framework Integration):**

- [ ] All 8 sub-subtasks complete
- [ ] Unit tests passing (>90% coverage)
- [ ] Orchestrator accepts categorized_branches.json from Task 007
- [ ] Output matches specification exactly
- [ ] Parallel execution verified and tested
- [ ] Error handling robust (no crashes)
- [ ] Rollback procedures tested and working
- [ ] Performance meets targets (<30s per target group)
- [ ] Code review approved
- [ ] Ready for Task 080 to integrate validation

---

## Done Definition

Task 079 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage) on CI/CD
3. ✅ Code review approved
4. ✅ Orchestrator functional and tested
5. ✅ Output matches specification exactly
6. ✅ Parallel execution safe and efficient
7. ✅ Error handling comprehensive and graceful
8. ✅ Documentation complete and accurate
9. ✅ Ready for hand-off to Task 080
10. ✅ Commit: "feat: complete Task 079 Modular Parallel Alignment Framework"
11. ✅ All success criteria checkboxes marked complete

---

## Next Steps

1. **Immediate:** Implement sub-subtask 079.1 (Design Orchestrator Architecture)
2. **Days 1-2:** Complete all 8 sub-subtasks
3. **Day 3:** Write and test unit tests (target: >95% coverage)
4. **Day 4:** Code review and refinement
5. **Day 5:** Ready for Task 080 (Validation Framework Integration)

**Reference:** This framework enables Task 080 (validation) and Task 083 (testing) - all alignment execution depends on this orchestrator.

---

## Downstream Impact

After Task 079 completion, the following are unblocked:
- **Task 080:** Validation Framework Integration (integrates pre-merge and comprehensive validation)
- **Task 083:** E2E Testing and Reporting (tests full alignment workflow)
- **Phase 2 Alignment Execution:** Actual branch alignments can begin

---

**Last Updated:** January 6, 2026  
**Structure:** TASK_STRUCTURE_STANDARD.md  
**Phase:** Retrofit - Legacy task format to complete standard format
