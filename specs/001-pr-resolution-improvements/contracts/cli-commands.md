# CLI Command Specifications

## EmailIntelligence CLI Integration Commands

### create-specification

**Purpose**: Generate detailed specifications for PR conflicts through guided prompts

```yaml
command: "emailintelligence-cli create-specification"
arguments:
  --branch: "Target branch name (required)"
  --base: "Base branch or commit SHA (required)"
  --output: "Output file path (default: spec-<timestamp>.md)"
  --template: "Specification template type (basic|detailed|enterprise)"
  --interactive: "Enable interactive prompting (default: true)"
  
returns:
  status: "success|error"
  specification_path: "string"
  conflicts_detected: "integer"
  analysis_time: "float"  # seconds
  complexity_score: "float"  # 0.0-1.0
```

### validate-constitution

**Purpose**: Check specification compliance against constitutional rules

```yaml
command: "emailintelligence-cli validate-constitution"
arguments:
  --spec: "Specification file path (required)"
  --rules-path: "Constitutional rules directory (default: ./constitutions)"
  --severity-filter: "Minimum severity level (info|warning|error|critical)"
  --auto-fix: "Attempt automatic fixes where possible"
  
returns:
  status: "success|error"
  compliance_score: "float"  # 0.0-1.0
  violations: 
    - rule_id: "string"
      severity: "string"
      description: "string"
      location: "string"
      auto_fixable: "boolean"
  execution_time: "float"  # seconds
```

### generate-strategy

**Purpose**: Create multi-phase resolution strategies with risk assessment

```yaml
command: "emailintelligence-cli generate-strategy"
arguments:
  --spec: "Specification file path (required)"
  --strategy-type: "Strategy type (conservative|balanced|aggressive)"
  --risk-tolerance: "Risk level (low|medium|high)"
  --include-rollback: "Include rollback procedures (default: true)"
  --task-export: "Export to TaskMaster (default: true)"
  
returns:
  status: "success|error"
  strategies:
    - strategy_id: "string"
      name: "string"
      risk_score: "float"
      phases:
        - phase_id: "string"
          name: "string"
          estimated_duration: "integer"
          rollback_procedure: "string"
          dependencies: "array"
  execution_time: "float"
  recommended_strategy: "string"
```

### execute-resolution

**Purpose**: Execute resolution strategy with worktree isolation

```yaml
command: "emailintelligence-cli execute-resolution"
arguments:
  --spec: "Specification file path (required)"
  --strategy: "Strategy ID to execute (required)"
  --dry-run: "Preview changes without executing"
  --worktree-pool: "Number of concurrent worktrees (default: 3)"
  --cleanup: "Auto-cleanup worktrees on completion (default: true)"
  
returns:
  status: "success|partial_success|error"
  execution_log:
    - phase: "string"
      status: "started|completed|failed"
      timestamp: "datetime"
      details: "string"
  preserved_features: "array"
  rollback_performed: "boolean"
  final_repository_state: "string"
  execution_time: "float"
```

### export-tasks

**Purpose**: Export specifications to TaskMaster with dependency analysis

```yaml
command: "emailintelligence-cli export-tasks"
arguments:
  --spec: "Specification file path (required)"
  --strategy: "Strategy ID (optional, exports all if not specified)"
  --project-root: "Project root directory (required)"
  --priority-default: "Default task priority (low|medium|high)"
  --dependencies: "Generate dependency relationships (default: true)"
  
returns:
  status: "success|warning|error"
  exported_tasks: 
    - task_id: "string"
      title: "string"
      description: "string"
      priority: "string"
      dependencies: "array"
  taskmaster_urls: "array"  # Links to created tasks
  dependency_graph: "object"  # Visual representation
```

## Configuration Commands

### setup-constitution

**Purpose**: Initialize constitutional rule repository

```yaml
command: "emailintelligence-cli setup-constitution"
arguments:
  --init: "Initialize new constitution repository"
  --template: "Constitution template (organizational|project|custom)"
  --rules-path: "Directory for constitutional rules"
  --validate: "Validate existing constitution setup"
  
returns:
  status: "success|error"
  constitution_path: "string"
  rules_count: "integer"
  template_applied: "string"
```

### performance-benchmark

**Purpose**: Measure and track resolution performance

```yaml
command: "emailintelligence-cli performance-benchmark"
arguments:
  --baseline: "Establish new performance baseline"
  --compare: "Compare against existing baseline"
  --conflict-type: "Specific conflict type (text|binary|structural|all)"
  --iterations: "Number of benchmark iterations (default: 10)"
  
returns:
  status: "success|error"
  baseline_established: "boolean"
  metrics:
    - conflict_type: "string"
      average_time: "float"
      median_time: "float"
      improvement_percentage: "float"
      confidence_score: "float"
  performance_report_path: "string"
```

## Structured Output Formats

### Specification Output Format

```json
{
  "specification": {
    "spec_id": "uuid",
    "version": "1.0.0",
    "title": "string",
    "metadata": {
      "created_at": "2025-11-12T19:29:00Z",
      "author": "string",
      "branch": "string",
      "complexity_score": 0.75
    },
    "conflicts": [
      {
        "conflict_id": "uuid",
        "type": "text|binary|structural",
        "file_path": "string",
        "severity": "low|medium|high|critical",
        "description": "string",
        "analysis": {}
      }
    ],
    "constitutional_compliance": {
      "score": 0.85,
      "violations": [],
      "recommendations": []
    }
  }
}
```

### Strategy Output Format

```json
{
  "strategy": {
    "strategy_id": "uuid",
    "name": "Conservative Resolution Strategy",
    "risk_assessment": {
      "overall_risk": 0.25,
      "technical_risk": "low",
      "organizational_risk": "low",
      "timeline_risk": "medium"
    },
    "phases": [
      {
        "phase_id": "uuid",
        "name": "Pre-resolution Validation",
        "description": "string",
        "estimated_duration": 30,
        "rollback_procedure": "string",
        "tasks": [
          {
            "task_id": "uuid",
            "title": "string",
            "priority": "high",
            "dependencies": []
          }
        ]
      }
    ],
    "preservation_strategies": [
      {
        "feature": "string",
        "method": "string",
        "validation_steps": []
      }
    ]
  }
}
```

### Performance Metrics Format

```json
{
  "performance_metrics": {
    "measurement_timestamp": "2025-11-12T19:29:00Z",
    "baseline_established": true,
    "metrics": {
      "text_conflicts": {
        "average_resolution_time": 45.2,
        "success_rate": 0.95,
        "improvement_vs_manual": 0.65
      },
      "binary_conflicts": {
        "average_resolution_time": 120.5,
        "success_rate": 0.88,
        "improvement_vs_manual": 0.52
      },
      "structural_conflicts": {
        "average_resolution_time": 300.8,
        "success_rate": 0.82,
        "improvement_vs_manual": 0.58
      }
    },
    "overall_improvement": 0.58,
    "confidence_score": 0.92
  }
}
```

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "status": "error",
    "error_code": "VALIDATION_FAILED|CONFLICT_DETECTION_ERROR|CONSTITUTIONAL_VIOLATION",
    "message": "Human-readable error description",
    "details": {
      "conflicts": [],
      "violations": [],
      "suggestions": []
    },
    "exit_code": 1
  }
}
```

### Validation Error Details

```json
{
  "validation_error": {
    "rule_id": "FILE_PERMISSIONS_RESTRICTED",
    "severity": "critical",
    "location": "src/config/database.yml:45",
    "expected": "User should not have write permissions",
    "actual": "File permissions: 755",
    "auto_fix_available": true,
    "fix_suggestion": "Run: chmod 644 src/config/database.yml"
  }
}
```

---

**CLI Contract Status**: ✅ Complete
**Next Step**: Create quickstart guide for implementation