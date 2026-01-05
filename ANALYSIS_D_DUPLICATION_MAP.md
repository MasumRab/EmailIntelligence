# EmailIntelligence - Duplication vs Unique Functionality Map

**Analysis Date**: 2025-11-22  
**Purpose**: Exact mapping of what's duplicated vs unique

---

## D. Duplication Map: Monolith vs Modules

### Summary Table

| Functionality | Monolith Lines | Module Lines | Duplication % | Winner |
|---------------|----------------|--------------|---------------|--------|
| Constitutional Analysis | 213 | 759 | 100% (mock vs real) | Module ✅ |
| Strategy Generation | 251 | 957 | 90% (mock vs real) | Module ✅ |
| Validation | 163 | 962 | 100% (mock vs real) | Module ✅ |
| Git Worktree Ops | 156 | 0 | 0% | Monolith ✅ |
| CLI Argument Parsing | 87 | 0 | 0% | Monolith ✅ |
| File Metadata Storage | 120 | 0 | 0% | Monolith ✅ |
| Interactive Prompts | 61 | 0 | 0% | Monolith ✅ |
| User Output Formatting | 94 | Minimal logging | 20% | Monolith ✅ |
| Alignment Execution | 262 | ??? | Unknown | Need analysis |

---

## 1. Constitutional Analysis

### Monolith (Lines 277-489, 213 lines)

**What it does**:
```python
def analyze_constitutional(self, pr_number, constitution_files, interactive):
    ├── Load metadata from JSON
    ├── Load constitutions (YAML/JSON)
    ├── Perform constitutional analysis (MOCK - hash-based)
    ├── Assess compliance (MOCK - hash-based)
    ├── Display results (MOCK data)
    └── Save results to metadata.json
```

**Unique functionality**:
- ✅ Metadata file loading (`_load_metadata()`)
- ✅ Constitution file selection (multi-file support)
- ✅ Interactive constitution selection
- ✅ Results display formatting (user-friendly output)
- ✅ Results saving to metadata.json

**Duplicated functionality (mock)**:
- ❌ Constitution parsing
- ❌ Compliance checking
- ❌ Violation detection
- ❌ Scoring

### Module: `ConstitutionalEngine` (759 lines)

**What it does**:
```python
class ConstitutionalEngine:
    ├── Load constitutional rules from JSON files
    ├── Compile regex patterns for validation
    ├── Validate specification templates (REAL)
    ├── Validate resolution strategies (REAL)
    ├── Validate execution phases (REAL)
    ├── Generate constitutional scoring
    ├── Track compliance history
    └── Generate recommendations
```

**Unique functionality**:
- ✅ Regex-based pattern matching
- ✅ Multi-level violation types (CRITICAL, MAJOR, MINOR, WARNING, INFO)
- ✅ Compliance level determination
- ✅ Remediation guidance
- ✅ Auto-fix detection
- ✅ Context extraction around violations
- ✅ Location tracking (line numbers)
- ✅ Confidence scoring based on match frequency
- ✅ Violation statistics and history
- ✅ Weighted scoring with customizable weights

**Missing functionality**:
- ❌ No metadata file handling
- ❌ No user-friendly output formatting
- ❌ Uses logging (not print statements)

### Integration Plan

**Keep from Monolith**:
- Metadata loading/saving
- User output formatting
- Interactive selection
- Multi-file constitution support

**Replace with Module**:
- All compliance checking logic
- All violation detection
- All scoring calculations

**Duplication**: **100%** of core logic (but monolith is mock)

---

## 2. Strategy Generation

### Monolith (Lines 575-826, 251 lines)

**What it does**:
```python
def develop_spec_kit_strategy(self, pr_number, interactive):
    ├── Load metadata
    ├── Build alignment config
    ├── Generate strategy (MOCK - hardcoded values)
    │   ├── Mock conflict count (first 5 only)
    │   ├── Mock alignment scores (hash-based)
    │   ├── Mock enhancement analysis (hardcoded 3 & 2)
    │   ├── Mock risk assessment (hardcoded "Medium")
    │   └── Mock phases with random strategy options
    ├── Interactive strategy development
    └── Save strategy to JSON
```

**Unique functionality**:
- ✅ Metadata loading
- ✅ Strategy file saving to JSON
- ✅ Interactive strategy modification
- ✅ User-friendly strategy display
- ✅ Default alignment config generation

**Duplicated functionality (mock)**:
- ❌ Strategy type selection
- ❌ Risk assessment
- ❌ Enhancement analysis
- ❌ Phase generation
- ❌ Time estimation

### Module: `MultiPhaseStrategyGenerator` (957 lines)

**What it does**:
```python
class MultiPhaseStrategyGenerator:
    ├── Initialize 6 strategy types with configs
    ├── Initialize enhancement preservation patterns
    ├── Initialize risk templates (5 categories)
    ├── Initialize execution checkpoint templates
    ├── Generate multiple strategies
    ├── Select strategy types based on context
    ├── Generate single strategy with:
    │   ├── Real time estimation
    │   ├── Real risk factor generation
    │   ├── Real enhancement preservation
    │   ├── Real execution phases
    │   └── Real confidence calculation
    ├── Generate hybrid strategies
    └── Rank strategies by confidence/risk/time
```

**Unique functionality**:
- ✅ 6 strategy types (vs 4 hardcoded options)
- ✅ Context-aware strategy selection
- ✅ 5 risk categories with real calculation
- ✅ Enhancement preservation patterns (4 types)
- ✅ Execution checkpoint templates
- ✅ Hybrid strategy synthesis
- ✅ Strategy ranking algorithm
- ✅ Parallel execution detection
- ✅ Risk mitigation planning
- ✅ Dynamic time estimation

**Missing functionality**:
- ❌ No JSON file I/O
- ❌ No interactive modification
- ❌ Minimal user-facing output

### Integration Plan

**Keep from Monolith**:
- metadata loading/saving
- Strategy file JSON I/O
- Interactive modification UI
- User output formatting

**Replace with Module**:
- All strategy generation logic
- All risk assessment
- All time estimation
- All enhancement analysis

**Duplication**: **90%** of core logic (10% unique is I/O)

---

## 3. Validation

### Monolith (Lines 1093-1258, 166 lines)

**What it does**:
```python
def validate_resolution(self, pr_number, level, test_suites):
    ├── Load metadata
    ├── Perform validation (MOCK - hash-based pass/fail)
    │   ├── Quick: 2 mock checks
    │   ├── Standard: 4 mock checks
    │   └── Comprehensive: 7 mock checks
    ├── Display results
    └── Save results
```

**Unique functionality**:
- ✅ Metadata loading
- ✅ Validation level selection (quick/standard/comprehensive)
- ✅ Results display formatting
- ✅ Results saving to JSON

**Duplicated functionality (mock)**:
- ❌ All test execution
- ❌ All validation checks
- ❌ All scoring

### Module: `ComprehensiveValidator` (962 lines)

**What it does**:
```python
class ComprehensiveValidator:
    ├── Initialize 6 quality gates
    ├── Comprehensive validation workflow:
    │   ├── Standard validation (inherited)
    │   ├── Full workflow validation
    │   ├── Performance benchmarking
    │   ├── Advanced quality metrics (7 dimensions)
    │   ├── Risk assessment (5 categories)
    │   ├── Quality gate assessment
    │   ├── Critical issue identification
    │   ├── Recommendation generation
    │   └── Deployment readiness scoring
    ├── Workflow validation (5 components)
    ├── Performance benchmarking (3 areas)
    ├── Quality metrics:
    │   ├── Complexity
    │   ├── Maintainability
    │   ├── Testability
    │   ├── Security
    │   ├── Reliability
    │   ├── Performance
    │   └── Documentation
    └── Risk assessment:
        ├── Technical
        ├── Business
        ├── Resource
        ├── Timeline
        └── Quality
```

**Unique functionality**:
- ✅ 6 quality gates with thresholds
- ✅ 7-dimensional quality metrics
- ✅ 5-category risk assessment
- ✅ Real performance benchmarking
- ✅ Workflow component validation
- ✅ Execution readiness scoring
- ✅ Deployment readiness scoring
- ✅ Critical issue detection
- ✅ Time-based performance tracking

**Also exists** (not analyzed yet):
- `quick_validator.py` (18.4 KB)
- `standard_validator.py` (25.2 KB)
- `reporting_engine.py` (40.4 KB)

**Missing functionality**:
- ❌ No simple output formatting
- ❌ No JSON file I/O
- ❌ Uses logging (not print)

### Integration Plan

**Keep from Monolith**:
- Metadata loading/saving
- Validation level selection UI
- Results display formatting
- Results saving to JSON

**Replace with Module**:
- ALL validation logic
- Use `quick_validator.py` for `--level quick`
- Use `standard_validator.py` for `--level standard`
- Use `comprehensive_validator.py` for `--level comprehensive`

**Duplication**: **100%** of validation logic (monolith is all mock)

---

## 4. Git Worktree Operations

### Monolith (Lines 120-275, 156 lines)

**What it does**:
```python
def setup_resolution(self, pr_number, source_branch, target_branch, ...):
    ├── Create worktree names
    ├── Create worktree paths
    ├── Run git worktree add (subprocess)
    ├── Detect conflicts (basic git diff)
    ├── Store metadata
    └── Create initial spec template
```

**Functionality**:
- ✅ Git worktree creation via subprocess
- ✅ Worktree path management
- ✅ Basic conflict detection (file-level only)
- ✅ Metadata initialization
- ✅ Spec template creation (placeholder)

### Modules: **NONE**

No module handles git operations directly.

**But**: `src/graph/` might have conflict detection logic?

**Graph modules**:
- `graph/__init__.py`
- `graph/conflicts/detection.py` ← **This likely has real conflict detection!**

### Integration Plan

**Keep from Monolith**:
- Git worktree management (it's already real)
- Worktree path creation
- Subprocess calls

**Potentially Add from Modules**:
- Use `graph/conflicts/detection.py` for sophisticated conflict detection
- Replace simple `git diff` with graph-based analysis

**Duplication**: **0%** - Monolith is unique here!

---

## 5. CLI Argument Parsing

### Monolith (Lines 1280-1418, 138 lines, but only ~87 for parsing)

**What it does**:
```python
def main():
    parser = argparse.ArgumentParser(...)
    subparsers = parser.add_subparsers(...)
    
    # Setup-resolution command
    setup_parser = subparsers.add_parser('setup-resolution', ...)
    setup_parser.add_argument('--pr-number', ...)

    # ... etc for 5 commands
    
    args = parser.parse_args()
    cli = EmailIntelligenceCLI()
    
    # Dispatch to command methods
    if args.command == 'setup-resolution':
        cli.setup_resolution(...)

    # ... etc
```

**Functionality**:
- ✅ Argument parsing with argparse
- ✅ Command dispatching
- ✅ Help text generation
- ✅ Argument validation

### Modules: **NONE**

No module has CLI parsing (they're libraries).

**Duplication**: **0%** - Monolith is unique!

---

## 6. File Metadata Storage

### Monolith (Scattered, ~120 lines total)

**What it does**:
```python
def _load_metadata(self, pr_number):
    metadata_file = resolution_branches_dir / f"pr-{pr_number}" / "metadata.json"
    with open(metadata_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_metadata(self, pr_number, metadata):
    metadata_file = resolution_branches_dir / f"pr-{pr_number}" / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

# Used in:

# - setup_resolution

# - analyze_constitutional

# - develop_spec_kit_strategy

# - align_content

# - validate_resolution
```

**Functionality**:
- ✅ JSON file-based metadata storage
- ✅ PR-specific metadata organization
- ✅ Metadata schema management

### Modules: **NONE**

Modules use database (`src/database/`) not JSON files!

**But**: Database module exists for Neo4j graph storage.

### Integration Question

**Current**: File-based metadata (JSON)  
**Available**: Neo4j database

**Options**:
1. **Keep files**: Simple, works, no migration needed
2. **Migrate to Neo4j**: More powerful, graph queries, but requires migration
3. **Hybrid**: Files for CLI, database for modules

**Recommendation**: **Keep files** for MVP, optionally migrate later.

**Duplication**: **0%** - Monolith is unique!

---

## 7. Interactive Prompts

### Monolith (Scattered, ~61 lines)

**What it does**:
```python

# In analyze_constitutional:
if interactive:
    selected = self._interactive_constitution_selection(constitutions)

# In develop_spec_kit_strategy:
if interactive:
    strategy_dict = self._interactive_strategy_development(strategy)

# In align_content:
if interactive:
    result = self._execute_phase_interactive(phase, metadata)
```

**Funct ionality**:
- ✅ User input prompts
- ✅ Menu selection
- ✅ Interactive modification
- ✅ Confirmation prompts

### Modules: **NONE**

Modules are non-interactive libraries.

**Duplication**: **0%** - Monolith is unique!

---

## 8. User Output Formatting

### Monolith (~94 lines)

**What it does**:
```python
def _info(self, message: str) -> None:
    print(f"INFO: {message}")

def _success(self, message: str) -> None:
    print(f"SUCCESS: {message}")

def _warn(self, message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)

def _error(self, message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)

# Plus formatted output in each command:

# - Tables

# - Progress bars (simulated with "...")

# - Section headers ("=" * 80)

# - Color-coded status
```

**Functionality**:
- ✅ Formatted console output
- ✅ Color-coded messages
- ✅ Tables and sections
- ✅ User-friendly formatting

### Modules: **Minimal**

Modules use `structlog` for logging:
```python
logger = structlog.get_logger()
logger.info("Message", key=value)
```

**This is different**:
- Logging → for developers/debugging
- Print formatting → for end users

**Duplication**: **~20%** - Both output info, but different purposes

**Integration**: Keep monolith's user-facing output, modules keep logging.

---

## 9. Alignment Execution

### Monolith (Lines 828-1090, 262 lines)

**What it does**:
```python
def align_content(self, pr_number, strategy_file, dry_run, interactive, checkpoint_each_step):
    ├── Load metadata & strategy
    ├── Execute phases:
    │   ├── dry_run: Display what would happen (MOCK)
    │   ├── interactive: Prompt user for each step (MOCK)
    │   └── normal: Execute resolution (MOCK - simulated)
    └── Save alignment results

def _execute_phase(self, phase, metadata):
    ├── Iterate through steps
    ├── Simulate conflict resolution (MOCK)
    ├── Simulate alignment score improvement (MOCK)
    └── Calculate phase-level score (MOCK)
```

**Functionality**:
- ✅ Strategy loading
- ✅ Phase execution orchestration
- ✅ Dry-run mode
- ✅ Interactive mode
- ✅ Checkpoint support
- ❌ **ALL EXECUTION IS SIMULATED** (no real file merging!)

### Modules: **???**

Need to check:
- `src/resolution/execution.py` (ExecutionEngine) - mentioned in `__init__.py` but not analyzed
- `src/resolution/workflows.py` (WorkflowOrchestrator) - mentioned in `__init__.py`
- `src/resolution/engine.py` (ResolutionEngine) - mentioned in `__init__.py`

**Unknown if these exist!**

### Analysis Needed

**TODO**: Check if these files exist and what they do:
1. `src/resolution/execution.py`
2. `src/resolution/workflows.py`
3. `src/resolution/engine.py`
4. `src/resolution/generation.py` (CodeChangeGenerator)

**If they exist**: Likely have real execution logic!  
**If they don't**: Need to implement or keep dry-run only.

**Duplication**: **Unknown** - Need to analyze mentioned modules.

---

## Summary: What's Unique vs Duplicated

### Monolith-Only (Keep, 424 lines)

1. **Git Worktree Operations** (156 lines) - Real, working
2. **CLI Argument Parsing** (87 lines) - Essential
3. **File Metadata Storage** (120 lines) - Simple, works
4. **Interactive Prompts** (61 lines) - User experience

**Total unique value**: ~29% of monolith

### Module-Only (Use, 2,678+ lines)

1. **Real Constitutional Analysis** (759 lines)
2. **Real Strategy Generation** (957 lines)
3. **Real Validation** (962 lines)
4. **Plus**: Quick/Standard validators, Reporting engine (~84 KB more!)

**Total unique value**: Massive (modules are vastly superior)

### Duplicated (Replace, 627 lines)

1. **Constitutional Analysis Logic** (213 lines) - Mock → replace with module
2. **Strategy Generation Logic** (251 lines) - Mock → replace with module
3. **Validation Logic** (163 lines) - Mock → replace with module

**Duplication**: ~43% of monolith (all mock implementations)

### Unknown (Need Analysis, 262 lines)

1. **Alignment Execution** (262 lines) - Check if modules exist

**Unknown**: ~18% of monolith

### User Experience (Keep, 94 lines)

1. **Output Formatting** (94 lines) - User-facing

**Overlap**: ~6% (both do output, different purposes)

---

## Final Duplication Map

```
Monolith (1,464 lines total):

├── Unique & Keep (424 lines, 29%)
│   ├── Git Worktree Ops (156)
│   ├── CLI Parsing (87)
│   ├── Metadata I/O (120)
│   └── Interactive Prompts (61)
│
├── User Experience (94 lines, 6%)
│   └── Output Formatting
│
├── Duplicated & Replace (627 lines, 43%)
│   ├── Constitutional (213) → ConstitutionalEngine
│   ├── Strategy (251) → MultiPhaseStrategyGenerator
│   └── Validation (163) → ComprehensiveValidator
│
├── Unknown (262 lines, 18%)
│   └── Alignment Execution → Check if modules exist
│
└── Overhead (57 lines, 4%)
    ├── Imports
    ├── Class definition
    └── Config loading
```

---

## Refactoring Strategy Summary

### Replace (43%)
Mock implementations → Real module methods

### Keep (35%)
- Git operations (working)
- CLI interface (good UX)
- Metadata storage (simple, works)
- Interactive prompts (user experience)
- Output formatting (user-facing)

### Investigate (18%)
- Alignment execution modules
- Resolution engine modules
- Check if they exist

### Remove (4%)
- Unused imports
- Duplicate config

---

## Effort Estimate by Category

| Category | Lines to Change | Estimated Hours |
|----------|-----------------|-----------------|
| Replace constitutional | 213 | 16-20 |
| Replace strategy | 251 | 20-24 |
| Replace validation | 163 | 12-16 |
| Wire imports & init | ~50 | 8-12 |
| Update CLI commands | ~100 | 12-16 |
| Testing | - | 20-30 |
| **Total** | **~777** | **88-118 hours** |

Add Phase 0 audit (8h) + Polish (40h) = **136-166 hours total**

**Timeline**: 3.5-4 weeks at 40h/week

**Previous estimate**: 208-248 hours (included more contingency and advanced features)

---

## Next Action

1. ✅ Create `ANALYSIS_A_MONOLITH_RELATIONSHIPS.md`
2. ✅ Create `ANALYSIS_B_MODULE_DEEP_DIVE.md`
3. ✅ Create `ANALYSIS_C_REAL_REFACTORING_PLAN.md`
4. ✅ Create `ANALYSIS_D_DUPLICATION_MAP.md`
5. **TODO**: Check if execution modules exist:
   - `src/resolution/execution.py`
   - `src/resolution/workflows.py`
   - `src/resolution/engine.py`
   - `src/resolution/generation.py`
6. **TODO**: Update task.md and implementation_plan.md with real findings
