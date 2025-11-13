# Data Model: Enhanced PR Resolution with Spec Kit Methodology

## Core Entities

### Conflict Entity

#### TextConflict
```yaml
text_conflict:
  file_path: string
  conflict_markers: array
  original_content: string
  incoming_content: string
  common_ancestor: string
  merge_base_sha: string
  conflict_type: "text"
  line_numbers:
    start: integer
    end: integer
  severity_level: "low" | "medium" | "high" | "critical"
  resolution_suggestions: array
```

#### BinaryConflict
```yaml
binary_conflict:
  file_path: string
  original_hash: string
  incoming_hash: string
  file_size: integer
  conflict_type: "binary"
  mime_type: string
  detection_method: "hash_mismatch" | "extension_change" | "permission_change"
  preservation_strategy: "original" | "incoming" | "manual_merge"
  rename_detection:
    similarity_score: float
    suggested_name: string
```

#### StructuralConflict
```yaml
structural_conflict:
  affected_paths: array
  conflict_type: "structural"
  change_types:
    - "directory_moved"
    - "file_deleted"
    - "permission_changed"
    - "directory_deleted"
  resolution_strategies:
    - "preserve_both"
    - "merge_hierarchies"
    - "restore_deleted"
  impact_assessment:
    scope: "local" | "project" | "global"
    risk_level: "low" | "medium" | "high"
```

### ConstitutionalRule Entity

```yaml
constitutional_rule:
  rule_id: string
  name: string
  description: string
  rule_type: "pattern" | "validation" | "policy" | "constraint"
  severity: "info" | "warning" | "error" | "critical"
  pattern: string  # Markdown pattern for matching
  auto_fixable: boolean
  fix_description: string
  dependencies: array  # Other rule IDs
  last_updated: datetime
  rule_source: string  # Git SHA or version
```

### ResolutionStrategy Entity

```yaml
resolution_strategy:
  strategy_id: string
  name: string
  description: string
  target_conflicts: array  # Array of conflict entities
  risk_assessment:
    technical_risk: "low" | "medium" | "high"
    organizational_risk: "low" | "medium" | "high"
    timeline_risk: "low" | "medium" | "high"
    overall_risk_score: float (0.0-1.0)
  phases:
    - phase_name: string
      description: string
      estimated_duration: integer  # seconds
      rollback_procedure: string
      dependencies: array  # Phase IDs
      task_generation:
        enabled: boolean
        template: string
  success_criteria:
    - criterion: string
      measurable: boolean
  preservation_strategies:
    - feature_name: string
      preservation_method: string
      validation_steps: array
```

### Specification Entity

```yaml
specification:
  spec_id: string
  version: string
  title: string
  description: string
  metadata:  # YAML frontmatter
    created_at: datetime
    updated_at: datetime
    author: string
    branch: string
    base_sha: string
    head_sha: string
    conflict_count: integer
    estimated_complexity: "low" | "medium" | "high"
  conflicts: array  # Array of conflict entities
  constitutional_compliance:
    rules_applied: array
    violations: array
    compliance_score: float (0.0-1.0)
  generated_tasks: array  # TaskMaster task references
  performance_baseline:
    manual_resolution_time: integer  # seconds
    automated_prediction: integer  # seconds
    confidence_score: float (0.0-1.0)
```

## Entity Relationships

### Conflict Resolution Flow
```
Specification → Conflicts (1:N)
├── TextConflict → ConstitutionalRule (N:M)
├── BinaryConflict → ResolutionStrategy (1:N)
└── StructuralConflict → ResolutionStrategy (1:N)

ResolutionStrategy → Phases (1:N)
├── Phase → TaskGeneration (1:1)
└── Phase → Dependencies (N:M)

Specification → Tasks (1:N) via TaskMaster Integration
```

### Constitutional Validation Flow
```
Conflict → ConstitutionalRule Matching
├── Pattern Evaluation (regex-based)
├── Severity Assessment
└── Compliance Scoring

ConstitutionalRule → Dependencies
├── Rule Chaining
├── Priority Resolution
└── Validation Order
```

## State Transitions

### Conflict States
```yaml
conflict_lifecycle:
  states:
    - "detected"
    - "categorized" 
    - "analyzed"
    - "validated"
    - "strategized"
    - "resolved"
    - "verified"
  transitions:
    detected → categorized: "conflict_classification"
    categorized → analyzed: "detailed_analysis"
    analyzed → validated: "constitutional_check"
    validated → strategized: "resolution_planning"
    strategized → resolved: "implementation"
    resolved → verified: "validation_complete"
```

### Resolution Strategy States
```yaml
strategy_lifecycle:
  states:
    - "generated"
    - "analyzed"
    - "approved"
    - "executing"
    - "completed"
    - "rolled_back"
  transitions:
    generated → analyzed: "risk_assessment"
    analyzed → approved: "human_validation"
    approved → executing: "phase_start"
    executing → completed: "all_phases_complete"
    executing → rolled_back: "failure_detected"
```

## Data Validation Rules

### Conflict Validation
- File paths must be absolute and within repository bounds
- Conflict markers must match Git conflict pattern `<<<<<<<`, `=======`, `>>>>>>>`
- Hash values must be valid SHA-1 hashes
- Severity levels must be from approved enum

### Constitutional Rule Validation
- Rule patterns must be valid regex expressions
- Severity levels must map to approved risk classifications
- Dependencies must form acyclic graph
- Rule IDs must be unique across all rules

### Specification Validation
- YAML frontmatter must be parseable
- Git SHAs must exist in repository
- Conflict count must match actual detected conflicts
- Performance baseline must be realistic (>0 seconds)

## Performance Considerations

### Caching Strategy
- Constitutional rules cached by rule source SHA
- Conflict analysis results cached by file path + Git SHA
- Resolution strategies cached by conflict pattern
- Performance benchmarks cached by conflict type

### Database Design (if needed)
```sql
-- Core tables for file-based storage fallback
CREATE TABLE conflicts (
    id INTEGER PRIMARY KEY,
    spec_id TEXT NOT NULL,
    conflict_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    metadata TEXT NOT NULL,  -- JSON
    created_at DATETIME NOT NULL
);

CREATE TABLE constitutional_rules (
    id INTEGER PRIMARY KEY,
    rule_id TEXT UNIQUE NOT NULL,
    pattern TEXT NOT NULL,
    severity TEXT NOT NULL,
    metadata TEXT NOT NULL,  -- JSON
    created_at DATETIME NOT NULL
);

CREATE INDEX idx_conflicts_spec_id ON conflicts(spec_id);
CREATE INDEX idx_rules_pattern ON constitutional_rules(pattern);
```

---

**Data Model Status**: ✅ Complete
**Next Step**: Generate API contracts and CLI command specifications