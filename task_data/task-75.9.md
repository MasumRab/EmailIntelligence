# Task 75.9: FrameworkIntegration

## Purpose
Finalize the Branch Clustering System and integrate it into the main framework. This Stage Three task completes Task 75 by creating production-ready code, establishing bridges to downstream orchestration tasks (79, 80, 83, 101), and providing comprehensive documentation for deployment.

**Scope:** Framework integration and production deployment  
**Effort:** 16-24 hours | **Complexity:** 6/10  
**Status:** Ready when 75.6, 75.7, 75.8 complete  
**Unblocks:** Tasks 79, 80, 83, 100, 101
**Dependencies:** Tasks 75.1-75.8

---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Success Criteria](#success-criteria)
- [Core Deliverables](#core-deliverables)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Integration Points](#integration-points)
- [Configuration & Defaults](#configuration-parameters)
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Performance Targets](#performance-targets)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Success Criteria

Task 75.9 is complete when:

**Code Integration:**
- [ ] All Task 75.1-75.6 modules consolidated into branch_clustering_framework.py
- [ ] Production-ready code with no technical debt
- [ ] All imports and dependencies properly managed
- [ ] Configuration externalized and validated
- [ ] Error handling comprehensive and logged
- [ ] No deprecated code or warnings

**API & Interfaces:**
- [ ] Clean public API defined for framework
- [ ] BranchClusteringEngine as primary entry point
- [ ] Input schema documented and validated
- [ ] Output schema documented and validated
- [ ] Type hints throughout codebase
- [ ] API documentation complete

**Downstream Integration:**
- [ ] Bridge to Task 79 (ExecutionContext) established
- [ ] Bridge to Task 80 (ValidationIntensity) established
- [ ] Bridge to Task 83 (TestSuiteSelection) established
- [ ] Bridge to Task 101 (OrchestrationTools) established
- [ ] Data contracts clearly specified
- [ ] Orchestration sequence defined

**Documentation:**
- [ ] Complete API documentation (docstrings, examples)
- [ ] Architecture documentation explaining design decisions
- [ ] Deployment guide with step-by-step instructions
- [ ] Configuration reference document
- [ ] Integration guide for downstream tasks
- [ ] Troubleshooting guide
- [ ] Performance tuning guide

**Quality & Testing:**
- [ ] All tests from 75.8 passing
- [ ] Integration tests with downstream adapters
- [ ] Documentation validated with examples
- [ ] Code review checklist completed
- [ ] Backward compatibility verified

**Framework Readiness:**
- [ ] Framework can be imported into main project
- [ ] Framework properly packaged
- [ ] Dependencies listed in requirements.txt
- [ ] Version number assigned
- [ ] Ready for Task 100 (Framework Deployment)

---

## Core Deliverables

### 1. branch_clustering_framework.py
Production-ready consolidated framework module

**Includes:**
- CommitHistoryAnalyzer (from 75.1)
- CodebaseStructureAnalyzer (from 75.2)
- DiffDistanceCalculator (from 75.3)
- BranchClusterer (from 75.4)
- IntegrationTargetAssigner (from 75.5)
- BranchClusteringEngine (from 75.6)
- Configuration management
- Comprehensive error handling
- Logging and monitoring hooks

**Key Features:**
```python
class BranchClusteringFramework:
    """
    Production-ready Branch Clustering System.
    
    Provides:
    - Multi-dimensional branch analysis
    - Intelligent clustering
    - Integration target assignment
    - Performance optimization
    - Complete error handling
    - Extensible architecture
    """
    
    def __init__(self, config: Dict):
        """Initialize framework with configuration."""
        pass
    
    def analyze_branches(self, branches: List[BranchInfo]) -> FrameworkOutput:
        """
        Analyze branches and produce clustering results.
        
        Returns structured output ready for downstream tasks.
        """
        pass
    
    # Methods for downstream tasks
    def get_execution_context(self, branch: str) -> ExecutionContext:
        """Bridge to Task 79 - ExecutionContext."""
        pass
    
    def get_validation_intensity(self, branch: str) -> ValidationIntensity:
        """Bridge to Task 80 - ValidationIntensity."""
        pass
    
    def get_test_suite_selection(self, branch: str) -> TestSuiteSelection:
        """Bridge to Task 83 - TestSuiteSelection."""
        pass
    
    def get_orchestration_strategy(self, branch: str) -> OrchestrationStrategy:
        """Bridge to Task 101 - OrchestrationTools."""
        pass
```

### 2. framework_configuration.yaml
Externalized configuration for production deployment

```yaml
framework:
  version: "1.0.0"
  name: "Branch Clustering Framework"

analyzers:
  commit_history:
    enabled: true
    lookback_days: 30
    max_commits: 1000
  
  codebase_structure:
    enabled: true
    include_extensions: [.py, .js, .ts, .java]
    exclude_patterns: ["__pycache__", "node_modules"]
  
  diff_distance:
    enabled: true
    normalization_method: "minmax"
    similarity_threshold: 0.5

clustering:
  algorithm: "kmeans"
  n_clusters: 3
  random_state: 42

orchestration:
  enable_parallelization: true
  num_workers: 3
  timeout_seconds: 300

output:
  format: "json"
  pretty_print: true
  export_dir: "./output"
```

### 3. API_REFERENCE.md
Complete API documentation for framework

**Sections:**
- Framework overview and concepts
- Installation and setup
- Configuration guide
- API reference with examples
- Data structures and schemas
- Error handling
- Performance tuning
- Troubleshooting

### 4. INTEGRATION_GUIDE.md
Guide for downstream tasks to use the framework

**Sections:**
- Overview of framework outputs
- How to integrate into Task 79 (ExecutionContext)
- How to integrate into Task 80 (ValidationIntensity)
- How to integrate into Task 83 (TestSuiteSelection)
- How to integrate into Task 101 (OrchestrationTools)
- Data contract specifications
- Error handling strategies

### 5. DEPLOYMENT_GUIDE.md
Step-by-step deployment instructions

**Sections:**
- Prerequisites and environment setup
- Installation steps
- Configuration deployment
- Verification procedures
- Troubleshooting deployment issues
- Rollback procedures
- Performance monitoring

### 6. requirements.txt
Python dependencies for framework

```
# Core dependencies
numpy>=1.20.0
pandas>=1.2.0
scikit-learn>=0.24.0

# Optional dependencies for visualization
matplotlib>=3.3.0
seaborn>=0.11.0

# Testing
pytest>=6.0.0
pytest-cov>=2.12.0
pytest-benchmark>=3.4.0

# Code quality
black>=21.0
flake8>=3.9.0
mypy>=0.900
```

---

## Subtasks Overview

### Dependency Flow Diagram

```
75.9.1 (2-3h)
[Design Integration]
    │
    ├─→ 75.9.2 (3-4h) ────────┐
    │   [Consolidate Code]     │
    │                          ├─→ 75.9.3 (3-4h) ─────────┐
    ├─→ 75.9.4 (3-4h) ────────┤  [API Design]             │
    │   [Error Handling]       │                          ├─→ 75.9.6 (2-3h) ──┐
    │                          ├─→ 75.9.5 (4-5h) ────────┤  [Integration]      │
    ├─→ 75.9.7 (4-5h) ────────┤  [Documentation]         │                    ├─→ 75.9.8 (3-4h)
    │   [Downstream Bridges]   │                          │  [Deployment]      │
    │                          │                          │                    │
    │                          └──────────────────────────┘                    │
    │                                                                          │
    └──────────────────────────────────────────────────────────────────────────┘

Critical Path: 75.9.1 → 75.9.2 → 75.9.3-75.9.7 (partial parallel) → 75.9.6 → 75.9.8
Minimum Duration: 16-24 hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after 75.9.2):**
- 75.9.3: API design (3-4 hours)
- 75.9.4: Error handling (3-4 hours)
- 75.9.5: Documentation (4-5 hours)
- 75.9.7: Downstream bridges (4-5 hours)

These tasks depend on consolidated code (75.9.2) and are independent of each other. **Estimated parallel execution saves 8-12 hours.**

**Must be sequential:**
- 75.9.1 → 75.9.2 (design before consolidation)
- 75.9.2 → 75.9.3-75.9.7 (need code first)
- 75.9.3-75.9.7 → 75.9.6 (need API + docs + bridges)
- 75.9.6 → 75.9.8 (need integration before deployment)

### Timeline with Parallelization

**Days 1: Design (75.9.1)**
- Review framework architecture
- Document integration strategy
- Plan deployment process

**Days 1-2: Code Consolidation (75.9.2)**
- Merge all 75.1-75.6 modules
- Unified configuration management
- Remove duplicate code

**Days 2-4: Parallel Implementation (75.9.3-75.9.7)**
- **75.9.3 (Person A, Days 2-3):** API design & type hints
- **75.9.4 (Person B, Days 2-3):** Comprehensive error handling
- **75.9.5 (Person C, Days 2-4):** Complete documentation
- **75.9.7 (Person D, Days 3-4):** Downstream bridges
- Merge results end of Day 3

**Days 4-5: Integration & Deployment (75.9.6-75.9.8)**
- Day 4: Package and validate framework
- Day 5: Create deployment guide, version release

---

## Subtasks

### 75.9.1: Consolidate All Modules
**Purpose:** Merge all Task 75.1-75.6 modules into framework  
**Effort:** 2-3 hours

**Steps:**
1. Create branch_clustering_framework.py
2. Import all analyzer classes
3. Import clustering and assignment logic
4. Import engine orchestrator
5. Resolve any import conflicts

**Success Criteria:**
- [ ] Framework file created and complete
- [ ] All components imported correctly
- [ ] No import errors
- [ ] Code compiles without warnings


### Implementation Checklist (From HANDOFF)
- [ ] Create branch_clustering_framework.py module
- [ ] Import all analyzer classes (75.1-75.3)
- [ ] Import clustering and assignment logic (75.4-75.5)
- [ ] Import engine orchestrator (75.6)
- [ ] Resolve any import conflicts
---

### 75.9.2: Refine Public API
**Purpose:** Define clean, documented API  
**Effort:** 2-3 hours

**Steps:**
1. Define framework public interface
2. Create BranchClusteringFramework wrapper class
3. Add input validation
4. Add output validation
5. Document all public methods

**Success Criteria:**
- [ ] Clean public API defined
- [ ] All methods documented
- [ ] Type hints added
- [ ] Input/output validation working


### Implementation Checklist (From HANDOFF)
- [ ] Define clean public API
- [ ] Create BranchClusteringFramework as primary entry point
- [ ] Add type hints throughout codebase
- [ ] Implement input/output validation
- [ ] Document all public methods
---

### 75.9.3: Create Downstream Bridges
**Purpose:** Establish integration points for Tasks 79, 80, 83, 101  
**Effort:** 3-4 hours

**Steps:**
1. Create adapter methods for Task 79 (ExecutionContext)
2. Create adapter methods for Task 80 (ValidationIntensity)
3. Create adapter methods for Task 83 (TestSuiteSelection)
4. Create adapter methods for Task 101 (OrchestrationTools)
5. Document data contracts

**Success Criteria:**
- [ ] All 4 bridges implemented
- [ ] Data contracts specified
- [ ] Example usage provided
- [ ] Integration points tested


### Implementation Checklist (From HANDOFF)
- [ ] Create adapter methods for Task 79 (ExecutionContext)
- [ ] Create adapter methods for Task 80 (ValidationIntensity)
- [ ] Create adapter methods for Task 83 (TestSuiteSelection)
- [ ] Create adapter methods for Task 101 (OrchestrationTools)
- [ ] Document data contracts
---

### 75.9.4: Implement Production Configuration
**Purpose:** Externalize and validate all configuration  
**Effort:** 2-3 hours

**Steps:**
1. Create framework_configuration.yaml
2. Implement configuration loader
3. Implement configuration validator
4. Add environment variable overrides
5. Document all configuration options

**Success Criteria:**
- [ ] Configuration file created
- [ ] Config loading working
- [ ] Config validation working
- [ ] All options documented


### Implementation Checklist (From HANDOFF)
- [ ] Create framework_configuration.yaml
- [ ] Implement configuration loader
- [ ] Implement configuration validator
- [ ] Add environment variable overrides
- [ ] Document all configuration options
---

### 75.9.5: Write Complete API Documentation
**Purpose:** Document framework API and usage  
**Effort:** 3-4 hours

**Steps:**
1. Create API_REFERENCE.md with full documentation
2. Document all classes and methods
3. Provide usage examples
4. Document data structures
5. Document error codes

**Success Criteria:**
- [ ] Complete API documentation
- [ ] All methods documented with examples
- [ ] Data structures clearly explained
- [ ] Error handling documented


### Implementation Checklist (From HANDOFF)
- [ ] Create API_REFERENCE.md with full documentation
- [ ] Document all classes and methods
- [ ] Provide usage examples
- [ ] Document data structures
- [ ] Document error codes
---

### 75.9.6: Create Integration Guides
**Purpose:** Guide for downstream tasks  
**Effort:** 2-3 hours

**Steps:**
1. Create INTEGRATION_GUIDE.md
2. Document Task 79 integration
3. Document Task 80 integration
4. Document Task 83 integration
5. Document Task 101 integration

**Success Criteria:**
- [ ] Integration guide complete
- [ ] All downstream tasks documented
- [ ] Data contracts specified
- [ ] Example integration code provided


### Implementation Checklist (From HANDOFF)
- [ ] Create INTEGRATION_GUIDE.md
- [ ] Document Task 79 integration
- [ ] Document Task 80 integration
- [ ] Document Task 83 integration
- [ ] Document Task 101 integration
---

### 75.9.7: Create Deployment Documentation
**Purpose:** Deployment and troubleshooting guides  
**Effort:** 2-3 hours

**Steps:**
1. Create DEPLOYMENT_GUIDE.md
2. Document prerequisites
3. Document installation steps
4. Document configuration steps
5. Document verification and troubleshooting

**Success Criteria:**
- [ ] Deployment guide complete
- [ ] Step-by-step instructions clear
- [ ] Troubleshooting section helpful
- [ ] Verification procedures included


### Implementation Checklist (From HANDOFF)
- [ ] Create DEPLOYMENT_GUIDE.md
- [ ] Document prerequisites
- [ ] Document installation steps
- [ ] Document configuration steps
- [ ] Document verification and troubleshooting
---

### 75.9.8: Code Review & Finalization
**Purpose:** Final review, testing, and preparation for deployment  
**Effort:** 2-3 hours

**Steps:**
1. Run complete test suite (75.8)
2. Verify all documentation complete
3. Code quality review (style, naming, patterns)
4. Create requirements.txt
5. Final integration testing

**Success Criteria:**
- [ ] All tests passing
- [ ] Code quality verified
- [ ] Documentation complete
- [ ] Ready for Task 100 (Framework Deployment)


### Implementation Checklist (From HANDOFF)
- [ ] Run complete test suite (75.8)
- [ ] Verify all documentation complete
- [ ] Code quality review
- [ ] Create requirements.txt
- [ ] Final integration testing
---

## Integration Points

### Bridge to Task 79: ExecutionContext

**Purpose:** Determine execution strategy (parallel/serial)

**Data Flow:**
```
Branch info from 75.6 output
    ↓
Framework.get_execution_context(branch_name)
    ↓
ExecutionContext (parallel/serial decision)
    ↓
Task 79 uses for orchestration decisions
```

### Bridge to Task 80: ValidationIntensity

**Purpose:** Determine test intensity level

**Data Flow:**
```
Cluster analysis from 75.4
    ↓
Framework.get_validation_intensity(branch_name)
    ↓
ValidationIntensity (light/medium/heavy)
    ↓
Task 80 uses for test planning
```

### Bridge to Task 83: TestSuiteSelection

**Purpose:** Select appropriate test suites

**Data Flow:**
```
Target assignment from 75.5
    ↓
Framework.get_test_suite_selection(branch_name)
    ↓
TestSuiteSelection (which tests to run)
    ↓
Task 83 uses for test execution
```

### Bridge to Task 101: OrchestrationTools

**Purpose:** Special handling for orchestration branches

**Data Flow:**
```
Enhanced orchestration data from 75.6
    ↓
Framework.get_orchestration_strategy(branch_name)
    ↓
OrchestrationStrategy (core/extension handling)
    ↓
Task 101 uses for special processing
```

---

## Configuration Parameters

- `FRAMEWORK_VERSION` = "1.0.0"
- `ENABLE_VALIDATION` = true
- `ENABLE_LOGGING` = true
- `LOG_LEVEL` = "INFO"
- `CACHE_ENABLED` = true
- `PERFORMANCE_TIMEOUT_SECONDS` = 300

---


## Technical Reference (From HANDOFF)

### Framework Architecture

**Primary Entry Point Class**
```python
class BranchClusteringFramework:
    # Production-ready branch clustering system
    
    def __init__(self, config: Dict):
        # Initialize with configuration
    
    def analyze_branches(self, branches: List[str]):
        # Analyze branches and produce clustering results
    
    def get_execution_context(self, branch: str):
        # Bridge to Task 79 - ExecutionContext
    
    def get_validation_intensity(self, branch: str):
        # Bridge to Task 80 - ValidationIntensity
    
    def get_test_suite_selection(self, branch: str):
        # Bridge to Task 83 - TestSuiteSelection
    
    def get_orchestration_strategy(self, branch: str):
        # Bridge to Task 101 - OrchestrationTools
```

### Downstream Integration Paths

**Task 79: ExecutionContext**
Branch info from 75.6 → get_execution_context() → ExecutionContext

**Task 80: ValidationIntensity**
Cluster analysis from 75.4 → get_validation_intensity() → ValidationIntensity

**Task 83: TestSuiteSelection**
Target assignment from 75.5 → get_test_suite_selection() → TestSuiteSelection

**Task 101: OrchestrationTools**
Enhanced orchestration data from 75.6 → get_orchestration_strategy() → OrchestrationStrategy

### Framework Output Deliverables

**1. branch_clustering_framework.py**
- Consolidated module with all components
- ~2000-3000 lines of production code
- Full type hints and documentation

**2. framework_configuration.yaml**
- Externalized configuration
- All parameters adjustable
- Environment variable support

**3. Documentation (API, Integration, Deployment)**
- API_REFERENCE.md
- INTEGRATION_GUIDE.md
- DEPLOYMENT_GUIDE.md
- requirements.txt

### Performance & Quality Targets

- Framework initialization: <1 second
- API call latency: <100ms
- Complete analysis: <120 seconds (13+ branches)
- Memory footprint: <100MB
- Code coverage: >95%
- Test suite: 40+ tests, all passing

### Dependencies & Integration

- Consolidates: Tasks 75.1-75.6
- Enables: Tasks 75.7-75.9 and downstream Tasks 79, 80, 83, 101
- External: scipy, scikit-learn, pandas, gitpython

---

## Typical Development Workflow

```bash
git checkout -b feat/framework-integration
mkdir -p src/framework docs/api

# Step 1: Design integration (75.9.1)
cat > FRAMEWORK_INTEGRATION_PLAN.md << 'EOF'
# Integration Architecture
- Consolidate Tasks 75.1-75.6
- Clean API with 4 entry points
- Downstream bridges (79, 80, 83, 101)
- Production-ready packaging
EOF

# Step 2: Consolidate modules (75.9.2)
cat > src/framework/branch_clustering_framework.py << 'EOF'
from src.analyzers import CommitHistoryAnalyzer
from src.analyzers import CodebaseStructureAnalyzer
from src.analyzers import DiffDistanceCalculator
from src.clustering import BranchClusterer
from src.assignment import IntegrationTargetAssigner
from src.engine import BranchClusteringEngine

class BranchClusteringFramework:
    """Production-ready consolidated framework."""
    def __init__(self, repo_path: str, config_path: str = None):
        self.engine = BranchClusteringEngine(repo_path, config_path)
    
    def analyze_branches(self, branch_names: List[str]) -> dict:
        """Main analysis pipeline."""
        return self.engine.execute(branch_names)
    
    def get_execution_context(self, branch: str) -> dict:
        """Bridge to Task 79."""
        results = self.engine.get_results(branch)
        return self._convert_to_execution_context(results)
    
    def get_validation_intensity(self, branch: str) -> dict:
        """Bridge to Task 80."""
        pass
    
    def get_test_suite_selection(self, branch: str) -> dict:
        """Bridge to Task 83."""
        pass
    
    def get_orchestration_strategy(self, branch: str) -> dict:
        """Bridge to Task 101."""
        pass

git add src/framework/branch_clustering_framework.py
git commit -m "feat: consolidate Tasks 75.1-75.6 (75.9.2)"
```

# Step 3: API design (75.9.3)
```bash
cat > docs/api/API_REFERENCE.md << 'EOF'
# Branch Clustering Framework API

## Primary Classes

### BranchClusteringFramework
Main entry point for all clustering operations.

**Methods:**
- `analyze_branches(branch_names: List[str]) -> dict`
- `get_execution_context(branch: str) -> ExecutionContext`
- `get_validation_intensity(branch: str) -> ValidationIntensity`
- `get_test_suite_selection(branch: str) -> TestSuiteSelection`
- `get_orchestration_strategy(branch: str) -> OrchestrationStrategy`

**Configuration:** externalized in framework_configuration.yaml
EOF

git add docs/api/
git commit -m "docs: API reference and type hints (75.9.3)"
```

# Step 4: Error handling (75.9.4)
```bash
# Add comprehensive error handling with logging
git add src/framework/error_handling.py
git commit -m "feat: comprehensive error handling (75.9.4)"
```

# Step 5: Complete documentation (75.9.5)
```bash
cat > DEPLOYMENT_GUIDE.md << 'EOF'
# Deployment Guide

## Installation
1. Extract framework files
2. Install dependencies: `pip install -r requirements.txt`
3. Configure framework_configuration.yaml
4. Run tests: `pytest tests/ -v`

## Usage
See API_REFERENCE.md for complete API documentation.
EOF

git add docs/ DEPLOYMENT_GUIDE.md
git commit -m "docs: complete deployment guide (75.9.5)"
```

# Step 6: Downstream bridges (75.9.7)
```bash
cat > src/framework/bridges.py << 'EOF'
# Task 79, 80, 83, 101 bridges
class ExecutionContextBridge:
    def convert(self, framework_output): pass

class ValidationIntensityBridge:
    def convert(self, framework_output): pass

# ... more bridges
EOF

git add src/framework/bridges.py tests/test_bridges.py
git commit -m "feat: downstream task bridges (75.9.7)"
```

# Step 7: Package framework (75.9.6)
```bash
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='branch-clustering-framework',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[...],
    python_requires='>=3.8',
)
EOF

git add setup.py requirements.txt
git commit -m "feat: framework packaging and versioning (75.9.6)"

# Run final tests
pytest tests/ -v --cov=src --cov-report=html
git add tests/
git commit -m "test: comprehensive test suite (75.9.8)"

# Create release
git tag v1.0.0
git push origin feat/framework-integration --tags
```

---

## Integration Handoff

**Task 75.8 Outputs → Task 75.9:**
- All passing unit tests from 75.8
- Test coverage reports (>90%)
- Test data fixtures

**Task 75.9 Outputs → Task 100 (Framework Deployment):**
- branch_clustering_framework.py (consolidated module)
- framework_configuration.yaml (configuration)
- API_REFERENCE.md (API documentation)
- INTEGRATION_GUIDE.md (integration with downstream tasks)
- DEPLOYMENT_GUIDE.md (deployment instructions)
- setup.py (packaging metadata)
- requirements.txt (dependencies)
- Bridge implementations (Tasks 79, 80, 83, 101)

**Task 75.9 Outputs → Downstream Tasks (79, 80, 83, 101):**
- Clean public API methods
- Data contracts and schemas
- Integration examples
- Bridge adapters

---

## Common Gotchas & Solutions

### Gotcha 1: Circular Imports When Consolidating Modules ⚠️

**Problem:** Importing all Task 75.1-75.6 modules creates circular import chains
**Symptom:** `ImportError: cannot import name...` or `ModuleNotFoundError`
**Root Cause:** Tasks have interdependencies; consolidation creates cycles

**Solution:**
```python
# Use lazy imports and module-level imports
class BranchClusteringFramework:
    def __init__(self, repo_path: str):
        # Import only when needed, not at module level
        from src.analyzers import CommitHistoryAnalyzer
        from src.clustering import BranchClusterer
        self.analyzer = CommitHistoryAnalyzer(repo_path)
        self.clusterer = BranchClusterer(repo_path)
```

**Test:**
```bash
python -c "from src.framework import BranchClusteringFramework; print('OK')"
```

---

### Gotcha 2: Configuration Not Cascading to Sub-Components ⚠️

**Problem:** Framework config not passed to Task 75.1-75.6 components
**Symptom:** Components use hardcoded defaults instead of config
**Root Cause:** Not propagating config through initialization chain

**Solution:**
```python
class BranchClusteringFramework:
    def __init__(self, repo_path: str, config_path: str):
        self.config = load_config(config_path)
        
        # Pass config to each component
        self.commit_analyzer = CommitHistoryAnalyzer(
            repo_path,
            config=self.config.get('commit_history')
        )
        self.structure_analyzer = CodebaseStructureAnalyzer(
            repo_path,
            config=self.config.get('codebase_structure')
        )
```

**Test:**
```python
def test_config_propagation():
    config_path = 'config/test.yaml'
    framework = BranchClusteringFramework('.', config_path)
    
    # Verify each component got config
    assert framework.commit_analyzer.config == expected_config
```

---

### Gotcha 3: Type Hints Missing or Inconsistent ⚠️

**Problem:** Code without type hints fails type checking and doc generation
**Symptom:** mypy errors, IDE warnings, documentation incomplete
**Root Cause:** Consolidated modules have different type hint styles

**Solution:**
```python
from typing import Dict, List, Optional, Tuple

class BranchClusteringFramework:
    def __init__(
        self, 
        repo_path: str, 
        config_path: Optional[str] = None
    ) -> None:
        """Initialize framework."""
        pass
    
    def analyze_branches(self, branches: List[str]) -> Dict[str, any]:
        """Analyze branches and return clustering results."""
        pass
```

**Test:**
```bash
mypy src/framework/ --strict
```

---

### Gotcha 4: Downstream Bridges Incomplete or Wrong Schema ⚠️

**Problem:** Bridge methods return wrong data structure for Task 79/80/83/101
**Symptom:** Downstream tasks fail to parse framework output
**Root Cause:** Bridge conversion logic doesn't match downstream input schema

**Solution:**
```python
def get_execution_context(self, branch: str) -> ExecutionContext:
    """Convert framework output to Task 79 schema."""
    framework_result = self.engine.get_results(branch)
    
    # Validate framework result has required fields
    assert 'cluster_id' in framework_result
    assert 'target_assignment' in framework_result
    
    # Map to ExecutionContext schema
    execution_context = {
        'branch': branch,
        'cluster_id': framework_result['cluster_id'],
        'target': framework_result['target_assignment'],
        'confidence': framework_result['confidence_score'],
        # ... other required fields
    }
    
    # Validate against schema
    assert validate_execution_context_schema(execution_context)
    return execution_context
```

**Test:**
```python
def test_bridge_to_task_79():
    framework = BranchClusteringFramework('.')
    exec_context = framework.get_execution_context('feature/test')
    
    # Verify schema
    assert 'cluster_id' in exec_context
    assert 'target' in exec_context
    assert 0 <= exec_context['confidence'] <= 1
```

---

### Gotcha 5: Documentation Examples Don't Work ⚠️

**Problem:** Code examples in API_REFERENCE.md have syntax errors
**Symptom:** Copy-pasting examples fails with `ImportError` or `AttributeError`
**Root Cause:** Examples not tested against actual code

**Solution:**
```python
# Test all examples from documentation
def test_api_example_basic_usage():
    """Test example from API_REFERENCE.md"""
    from src.framework import BranchClusteringFramework
    
    framework = BranchClusteringFramework('.')
    results = framework.analyze_branches(['feature/test'])
    
    assert 'clusters' in results
    assert 'assignments' in results

def test_api_example_get_execution_context():
    """Test bridge example from INTEGRATION_GUIDE.md"""
    from src.framework import BranchClusteringFramework
    
    framework = BranchClusteringFramework('.')
    exec_context = framework.get_execution_context('feature/test')
    
    assert 'branch' in exec_context
    assert 'target' in exec_context
```

---

### Gotcha 6: Performance Degradation After Consolidation ⚠️

**Problem:** Consolidated framework is slower than individual components
**Symptom:** Analysis time exceeds targets (<120 seconds for 13 branches)
**Root Cause:** Additional overhead from framework layers, or redundant computation

**Solution:**
```python
class BranchClusteringFramework:
    def __init__(self, repo_path: str, config_path: str = None):
        self.config = load_config(config_path)
        
        # Enable caching to avoid redundant computation
        self.cache_enabled = self.config.get('cache_enabled', True)
        self._results_cache = {} if self.cache_enabled else None
    
    def analyze_branches(self, branches: List[str]) -> Dict:
        """Analyze with caching."""
        cache_key = tuple(sorted(branches))
        
        if cache_key in self._results_cache:
            return self._results_cache[cache_key]
        
        results = self.engine.execute(branches)
        
        if self.cache_enabled:
            self._results_cache[cache_key] = results
        
        return results
```

**Benchmark:**
```bash
python -m pytest tests/test_performance.py -v
# Verify: analysis time < 120 seconds for 13 branches
```

---

### Gotcha 7: Dependency Conflicts or Version Incompatibilities ⚠️

**Problem:** requirements.txt has conflicting versions or incompatible packages
**Symptom:** `pip install` fails or runtime `ImportError`
**Root Cause:** Tasks 75.1-75.6 have different dependency versions

**Solution:**
```python
# requirements.txt - use compatible versions
numpy>=1.20.0,<2.0.0
scipy>=1.6.0,<2.0.0
scikit-learn>=0.24.0,<1.5.0
pandas>=1.2.0,<2.0.0
gitpython>=3.1.0

# Optional visualization
plotly>=5.0.0
matplotlib>=3.3.0
```

**Test:**
```bash
# Test installation in clean environment
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python -c "import src.framework; print('OK')"
```

---

### Gotcha 8: Missing Bridge Implementation for Downstream Task ⚠️

**Problem:** Bridge method for Task 79/80/83/101 not implemented (just `pass`)
**Symptom:** Downstream task receives `None` instead of expected data
**Root Cause:** Bridge stubbed out but not completed

**Solution:**
```python
def get_test_suite_selection(self, branch: str) -> Dict:
    """Bridge to Task 83 - TestSuiteSelection."""
    # MUST be implemented, not just `pass`
    framework_result = self.engine.get_results(branch)
    
    # Extract relevant metrics for test suite selection
    complexity = framework_result['metrics'].get('diff_complexity', 0.5)
    test_changes = 'tag:test_changes' in framework_result.get('tags', [])
    
    # Map to TestSuiteSelection schema
    test_selection = {
        'branch': branch,
        'requires_e2e': complexity > 0.7 or test_changes,
        'requires_unit': True,
        'requires_integration': complexity > 0.5,
        'requires_performance': 'tag:performance_critical' in framework_result.get('tags', []),
    }
    
    return test_selection
```

**Verification:**
```python
def test_all_bridges_implemented():
    framework = BranchClusteringFramework('.')
    
    # Verify all bridge methods return non-None
    exec_ctx = framework.get_execution_context('feature/test')
    assert exec_ctx is not None
    
    val_intensity = framework.get_validation_intensity('feature/test')
    assert val_intensity is not None
    
    test_suite = framework.get_test_suite_selection('feature/test')
    assert test_suite is not None
    
    orch_strategy = framework.get_orchestration_strategy('feature/test')
    assert orch_strategy is not None
```

---

## Integration Checkpoint

**When to move to Task 100 (Framework Deployment):**
- [ ] All 8 subtasks complete
- [ ] Framework consolidated and tested
- [ ] Public API clean and documented
- [ ] Downstream bridges implemented and tested
- [ ] All documentation complete
- [ ] Code review passed
- [ ] Ready for deployment

---

## Performance Targets

- **Framework initialization:** <1 second
- **API call latency:** <100ms
- **Complete analysis:** <120 seconds for 13+ branches
- **Memory footprint:** <100MB

---

## Done Definition

Task 75.9 is done when:
1. All 8 subtasks marked complete
2. Framework consolidated and production-ready
3. Clean public API with documentation
4. All downstream bridges implemented
5. Complete documentation (API, integration, deployment)
6. All tests passing
7. Code review completed
8. Ready for Task 100 (Framework Deployment)

---

## Next Steps (Task 100 and Beyond)

**Task 100: Framework Deployment**
- Final validation of framework in main project
- Integration with existing systems
- Performance verification in production
- Deployment to production environment

**Downstream Orchestration Tasks (79, 80, 83, 101)**
- Implement decision logic using framework outputs
- Create specialized processing pipelines
- Integrate with main test orchestration system
- Coordinate execution strategies
