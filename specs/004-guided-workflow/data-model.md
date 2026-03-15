# Data Model: Orchestration & Scientific Core

**Version**: 1.3.0 (Aligned with Branch Analysis Features)

---

## 1. Session (`src.core.models.orchestration.Session`)

Tracks the state of a long-running developer workflow (CLI side).

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique session identifier |
| `workflow` | Enum | `rebase`, `analyze`, `sync`, `scientific_resolution` |
| `status` | Enum | `active`, `paused`, `completed`, `failed` |
| `context` | Dict | Arbitrary workflow data |

---

## 2. Conflict (`src.core.conflict_models.Conflict`)

Represents a merge conflict with semantic understanding.

| Field | Type | Description |
|-------|------|-------------|
| `file_path` | str | Relative file path |
| `conflict_type` | Enum | `content`, `structural`, `semantic` |
| `severity` | Enum | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `resolution_strategy` | str | Suggested fix strategy |

---

## 3. ResolutionPlan (`src.core.conflict_models.ResolutionPlan`)

A structured plan for resolving complex conflicts.

| Field | Type | Description |
|-------|------|-------------|
| `conflicts` | List[Conflict] | Detected conflicts |
| `strategy` | Dict | Generated resolution strategy |
| `validation_result` | ValidationResult | Outcome of pre-merge checks |

---

## 4. ConstitutionalRule (`src.core.models.analysis.Rule`)

Config-driven rule definition.

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique Rule ID |
| `requirements` | List[Req] | Normative statements (MUST/SHOULD) |
| `compliance_score` | float | 0.0 to 1.0 score |

---

## 5. CLICommand

Interface for all CLI commands.

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Command trigger |
| `args` | Namespace | Parsed arguments |
| `execute()` | Method | Main logic |

---

# New Data Structures (v1.3.0)

## 6. Commit Topology Analysis (FR-043, FR-044)

### CommitNode
```python
class CommitNode(BaseModel):
    hash: str                           # SHA-1
    parents: List[str] = []             # Parent SHA hashes
    author: str
    author_email: str
    date: datetime
    message: str
    files_changed: List[str] = []
    insertions: int = 0
    deletions: int = 0
    is_merge: bool = False
    is_revert: bool = False
```

### TopologyGraph
```python
class TopologyGraph(BaseModel):
    nodes: Dict[str, CommitNode]        # hash -> CommitNode
    edges: Dict[str, List[str]]         # hash -> [parent_hashes]
    root: str                          # oldest common ancestor SHA
```

### RiskAssessment
```python
class RiskFactor(str, Enum):
    WIP = "wip_commit"
    LARGE_DIFF = "large_diff"
    MANY_FILES = "many_files"
    MERGE_COMMIT = "merge_commit"
    REVERT = "revert_commit"
    BREAKING_CHANGE = "breaking_change"

class RiskAssessment(BaseModel):
    commit_hash: str
    risk_score: int = Field(ge=0, le=25)
    risk_factors: List[RiskFactor] = []
    is_problematic: bool = False
```

### TopologyRiskReport (FR-045)
```python
class TopologyRiskReport(BaseModel):
    total_commits: int
    problematic_commits: int
    risk_distribution: Dict[RiskFactor, int]  # factor -> count
    conflict_probability: float = Field(ge=0.0, le=1.0)
    estimated_rebase_complexity: str  # "low", "medium", "high", "extreme"
    recommendations: List[str] = []
```

---

## 7. Branch Categorization (NEW)

### BranchCategory
```python
class BranchCategory(str, Enum):
    FEATURE = "feature"
    FIX = "fix"
    HOTFIX = "hotfix"
    DOCS = "docs"
    REFACTOR = "refactor"
    RELEASE = "release"
    MAINLINE = "mainline"
    EXPERIMENTAL = "experimental"
    UNKNOWN = "unknown"

class BranchCategoryResult(BaseModel):
    branch_name: str
    category: BranchCategory
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    evidence: List[str] = []           # Why this category was chosen
    heuristics_used: List[str] = []    # "name_pattern", "commit_analysis"
```

---

## 8. Branch Alignment (FR-028 to FR-035)

### AlignmentReport
```python
class StructuralDiff(BaseModel):
    added_dirs: List[str] = []
    removed_dirs: List[str] = []
    modified_files: List[str] = []
    renamed_files: Dict[str, str] = {}  # old -> new
    similarity_by_name: Dict[str, float] = {}  # filename -> 0.0-1.0

class AlignmentReport(BaseModel):
    source_branch: str
    target_branch: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    
    # Commit overlap analysis
    shared_commits: List[str] = []
    unique_to_source: List[str] = []
    unique_to_target: List[str] = []
    
    # Structure analysis
    structural_diff: StructuralDiff
    
    # Risk assessment
    topology_risk: TopologyRiskReport
    conflict_probability: float = Field(ge=0.0, le=1.0)
    
    recommendations: List[str] = []
```

---

## 9. Analysis Cache (FR-047)

### BranchAnalysisCache
```python
class BranchAnalysisCache(BaseModel):
    branch_name: str
    commit_sha: str                    # Cache key - invalidates if branch moves
    analyzed_at: datetime
    
    # Cached data (fast compare without re-analysis)
    topology: TopologyGraph
    risk_assessment: List[RiskAssessment] = []
    category: BranchCategoryResult
    
    # Quick stats
    commit_count: int
    last_modified: datetime
    analysis_duration_ms: int
```

---

## 10. Unified Analysis Output (per Constitution Section XII)

### AnalysisResult (ALL COMMANDS RETURN THIS)
```python
from typing import Union, Optional

class AnalysisResult(BaseModel):
    success: bool
    command: str                       # Which command generated this
    
    # Data variants - one of these is populated
    data: Optional[Union[
        AlignmentReport,
        TopologyGraph,
        TopologyRiskReport,
        List[Conflict],
        BranchCategoryResult,
        BranchAnalysisCache
    ]] = None
    
    metadata: AnalysisMetadata
    error: Optional[ErrorDetail] = None

class AnalysisMetadata(BaseModel):
    execution_time_ms: int
    branches_analyzed: List[str]
    commits_analyzed: int
    tool_used: str                     # "pydriller", "git-networkx", "subprocess"
    schema_version: str = "1.3.0"
    cache_hit: bool = False           # True if returned cached data

class ErrorDetail(BaseModel):
    code: str                          # e.g., "GIT_CONFLICT_DETECTED"
    message: str
    details: Dict                      # e.g., {file: "auth.py", hunks: 3}
    hint: str                          # e.g., "Run dev.py resolve auth.py"
```

---

## Feature to Data Model Coverage

| Feature | FR | Primary Data Structure | Status |
|---------|-----|----------------------|--------|
| Conflict Analysis | FR-029 | `Conflict`, `ResolutionPlan` | ✅ In model |
| Commit History | FR-028 | `CommitNode`, `TopologyGraph` | ✅ Added |
| Rebase Planning | FR-030 | `TopologyGraph`, `RiskAssessment` | ✅ Added |
| Directory Comparison | FR-031 | `StructuralDiff` | ✅ Added |
| Filename Matching | FR-032 | `StructuralDiff.similarity_by_name` | ✅ Added |
| Content Diff | FR-033 | `CommitNode.insertions/deletions` | ✅ Added |
| AST Similarity | FR-034 | External (pyastsim) | N/A |
| Code Structure | FR-035 | External (gkg) | N/A |
| Commit Topology | FR-043 | `TopologyGraph` | ✅ Added |
| Problem Detection | FR-044 | `RiskAssessment`, `RiskFactor` | ✅ Added |
| Risk Report | FR-045 | `TopologyRiskReport` | ✅ Added |
| Hygiene Analysis | FR-046 | Uses `TopologyRiskReport` | ✅ Covered |
| Analysis Cache | FR-047 | `BranchAnalysisCache` | ✅ Added |
| Branch Category | NEW | `BranchCategoryResult` | ✅ Added |
| Alignment Report | FR-028 | `AlignmentReport` | ✅ Added |

---

## JSON Output Example

```json
{
  "success": true,
  "command": "dev.py align",
  "data": {
    "source_branch": "feature/auth",
    "target_branch": "main",
    "similarity_score": 0.73,
    "shared_commits": ["abc123", "def456", ...],
    "unique_to_source": ["ghi789"],
    "unique_to_target": ["jkl012"],
    "structural_diff": {
      "added_dirs": ["src/auth/"],
      "modified_files": ["auth.py", "models.py"]
    },
    "topology_risk": {
      "total_commits": 50,
      "problematic_commits": 3,
      "conflict_probability": 0.25,
      "estimated_rebase_complexity": "medium"
    }
  },
  "metadata": {
    "execution_time_ms": 1234,
    "branches_analyzed": ["feature/auth", "main"],
    "commits_analyzed": 150,
    "tool_used": "pydriller",
    "schema_version": "1.3.0",
    "cache_hit": false
  }
}
```
