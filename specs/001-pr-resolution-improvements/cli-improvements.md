# CLI Improvements for PR Analysis & Worktree Alignment

## Command Structure Improvements

### Proposed Command Structure
```bash
# Primary namespace for PR resolution
emailintelligence-cli pr-resolve [subcommand] [options]

# Subcommands
emailintelligence-cli pr-resolve init           # Initialize resolution environment
emailintelligence-cli pr-resolve analyze        # Analyze conflicts and create specification
emailintelligence-cli pr-resolve validate       # Validate against constitutional rules
emailintelligence-cli pr-resolve strategy       # Generate resolution strategy
emailintelligence-cli pr-resolve execute        # Execute resolution with worktree isolation
emailintelligenti-cli pr-resolve tasks          # Export to TaskMaster
emailintelligence-cli pr-resolve status         # Show resolution status
emailintelligence-cli pr-resolve cleanup        # Cleanup worktrees and temporary files
```

### Enhanced Worktree Management
```python
class EnhancedGitWorktreeManager:
    def __init__(self, repository_path: str):
        self.repo = Repo(repository_path)
        self.worktree_pool = WorktreePool(max_size=5)
        self.session_manager = WorktreeSessionManager()
        self.recovery_manager = WorktreeRecoveryManager()
    
    def create_resolution_worktree(self, branch: str, base: str, session_id: str) -> str:
        """Create isolated worktree for conflict resolution"""
        # Validate Git version compatibility
        self._validate_git_version()
        
        # Create unique worktree path
        worktree_path = self._generate_worktree_path(session_id, branch)
        
        try:
            # Create worktree with proper isolation
            worktree = self.repo.git.worktree('add', worktree_path, branch)
            
            # Initialize session tracking
            self.session_manager.register_session(session_id, {
                'worktree_path': worktree_path,
                'branch': branch,
                'base': base,
                'created_at': datetime.now()
            })
            
            return worktree_path
            
        except GitCommandError as e:
            # Attempt recovery
            return self.recovery_manager.handle_worktree_failure(
                worktree_path, e, branch, base
            )
    
    def _validate_git_version(self):
        """Ensure Git version supports worktree operations"""
        git_version = self.repo.git.version()
        if not self._supports_worktrees(git_version):
            raise CLIError(
                f"Git {self.MIN_GIT_VERSION}+ required. "
                f"Current version: {git_version}"
            )
    
    def cleanup_all_worktrees(self, session_id: str = None):
        """Cleanup worktrees with proper error handling"""
        if session_id:
            self.session_manager.cleanup_session(session_id)
        else:
            self.worktree_pool.cleanup_all()
```

### Enhanced CLI Error Handling
```python
class ResolutionCLIErrorHandler:
    def handle_error(self, error: Exception, context: dict):
        error_type = type(error).__name__
        
        if isinstance(error, GitCommandError):
            return self._handle_git_error(error, context)
        elif isinstance(error, WorktreeError):
            return self._handle_worktree_error(error, context)
        elif isinstance(error, ConstitutionalRuleError):
            return self._handle_constitutional_error(error, context)
        else:
            return self._handle_generic_error(error, context)
    
    def _handle_worktree_error(self, error: WorktreeError, context: dict):
        """Handle worktree-specific errors with recovery"""
        logger.error(f"Worktree error in {context.get('operation')}: {error}")
        
        # Attempt recovery based on error type
        if "corrupt" in str(error).lower():
            return self._recover_corrupt_worktree(context)
        elif "permission" in str(error).lower():
            return self._fix_worktree_permissions(context)
        else:
            return self._cleanup_and_retry(context)
```

### Parallel Worktree Coordination
```python
class WorktreeSessionCoordinator:
    def __init__(self):
        self.active_sessions = {}
        self.worktree_locks = {}
        self.conflict_detector = WorktreeConflictDetector()
    
    def start_parallel_resolution(self, sessions: List[dict]):
        """Coordinate multiple resolution sessions"""
        # Detect potential conflicts between sessions
        conflicts = self.conflict_detector.detect_conflicts(sessions)
        if conflicts:
            return self._resolve_conflicts(sessions, conflicts)
        
        # Start all sessions with coordination
        results = []
        for session in sessions:
            try:
                result = self._execute_session_coordinated(session)
                results.append(result)
            except Exception as e:
                logger.error(f"Session {session['id']} failed: {e}")
                results.append(self._handle_session_failure(session, e))
        
        return results
    
    def _execute_session_coordinated(self, session: dict):
        """Execute session with coordination"""
        # Acquire worktree lock
        with self._acquire_worktree_lock(session['branch']):
            # Execute resolution in isolated worktree
            return self._run_resolution_workflow(session)
```

### Local Repository Alignment
```python
class LocalRepositoryAlignment:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
        self.conflict_analyzer = ConflictAnalyzer()
        self.alignment_validator = AlignmentValidator()
    
    def analyze_pr_alignment(self, branch: str, base: str) -> dict:
        """Analyze PR alignment with local repository state"""
        # Get actual conflict information
        conflicts = self._get_real_conflicts(branch, base)
        
        # Analyze local repository state
        repo_state = self._analyze_repository_state()
        
        # Validate alignment
        alignment = self.alignment_validator.validate_alignment(
            conflicts, repo_state
        )
        
        return {
            'conflicts': conflicts,
            'repo_state': repo_state,
            'alignment_score': alignment.score,
            'recommendations': alignment.recommendations
        }
    
    def _get_real_conflicts(self, branch: str, base: str) -> List[dict]:
        """Get actual Git conflicts using real repository analysis"""
        try:
            # Create temporary worktree for analysis
            with self._create_analysis_worktree(branch, base) as worktree:
                # Use actual Git commands to detect conflicts
                conflict_files = self._detect_conflict_files(worktree.path)
                conflict_details = []
                
                for file_path in conflict_files:
                    detail = self._analyze_file_conflict(worktree.path, file_path)
                    conflict_details.append(detail)
                
                return conflict_details
                
        except Exception as e:
            logger.error(f"Failed to analyze conflicts: {e}")
            raise ResolutionError(f"Conflict analysis failed: {e}")
```

### Performance Optimization
```python
class WorktreePerformanceOptimizer:
    def __init__(self):
        self.cache = LRUCache(maxsize=100)
        self.metrics = PerformanceMetrics()
    
    def optimize_worktree_operations(self):
        """Optimize worktree operations based on usage patterns"""
        # Cache frequently accessed worktrees
        # Reuse worktrees for similar operations
        # Pre-warm worktree pool during idle time
        # Monitor and adjust pool size based on load
    
    def get_worktree_performance_metrics(self):
        """Get real performance metrics for optimization"""
        return {
            'average_creation_time': self.metrics.avg_creation_time(),
            'reuse_efficiency': self.metrics.reuse_efficiency(),
            'cache_hit_rate': self.metrics.cache_hit_rate(),
            'pool_utilization': self.metrics.pool_utilization()
        }
```

## Implementation Priorities

### Phase 1: Core CLI Structure
1. Implement pr-resolve namespace commands
2. Add Git version validation
3. Enhanced error handling framework

### Phase 2: Worktree Management
1. Session coordination system
2. Worktree recovery mechanisms
3. Performance optimization

### Phase 3: Local Alignment
1. Real conflict analysis with Git
2. Repository state alignment validation
3. Performance monitoring integration

### Phase 4: Advanced Features
1. Parallel worktree coordination
2. Automated recovery procedures
3. Performance tuning and optimization