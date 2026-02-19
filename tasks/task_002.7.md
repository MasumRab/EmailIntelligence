# Task 002.7: VisualizationReporting

**Status:** Ready for Implementation
**Priority:** Medium
**Effort:** 20-28 hours
**Complexity:** 6/10
**Dependencies:** 002.6

---

## Overview/Purpose

Implement visualization and reporting tools that present clustering results through interactive dashboards, dendrograms, and summary reports. This is a Stage Three component that transforms raw pipeline output from Task 002.6 into human-readable artifacts for developer review, decision support, and downstream integration verification.

**Scope:** `ClusteringVisualizer` class and all output generation
**Tech Stack:** plotly, scipy, pandas, jinja2

---

## Success Criteria

Task 002.7 is complete when:

### Core Functionality
- [ ] `ClusteringVisualizer` class accepts `pipeline_results` dict from Task 002.6 output
- [ ] `generate_dendrogram()` produces interactive HTML with hover, zoom, pan, cluster colors, and threshold line
- [ ] `generate_dashboard()` produces HTML with all 6 charts (Silhouette, Cluster Size, Integration Target, Risk, Correlation, Quality Summary)
- [ ] `generate_report()` produces static HTML with all 8 sections (Header, Executive Summary, Clustering Overview, Quality Assessment, Integration Target Distribution, Top Insights, Detailed Branch Listing, Recommendations)
- [ ] `export_summary_stats()` returns dict matching JSON schema and writes to file
- [ ] Tag distribution analysis generates 3 charts (frequency, categories, co-occurrence)
- [ ] All output files generated with correct naming: `dendrogram_*.html`, `dashboard_*.html`, `report_*.html`, `summary_stats_*.json`

### Quality Assurance
- [ ] Unit tests pass with standard results (13 branches, 3 clusters)
- [ ] Edge cases handled: single cluster, many small clusters, extreme metric values, empty/missing data
- [ ] All HTML outputs render correctly in browser
- [ ] No exceptions on valid pipeline_results input
- [ ] Google-style docstrings on all public methods
- [ ] PEP 8 compliant code

### Integration Readiness
- [ ] Compatible with Task 002.6 pipeline output format
- [ ] Summary stats JSON consumable by downstream tasks
- [ ] Configuration externalized via VISUALIZATION_CONFIG dict
- [ ] File paths returned from all generation methods

---

## Prerequisites & Dependencies

### Required Before Starting
- [ ] Task 002.6 (BranchClusteringPipeline) complete and producing valid output
- [ ] Development environment with plotly, scipy, pandas, jinja2 installed
- [ ] Test infrastructure in place

### Blocks (What This Task Unblocks)
- Task 002.8 (TestingSuite) — visualization outputs needed for validation tests
- Task 002.9 (FrameworkIntegration) — visualizer integrated into framework API

### External Dependencies
- Python 3.8+
- `plotly` (interactive visualizations)
- `scipy.cluster.hierarchy` (dendrogram data extraction)
- `pandas` (data aggregation)
- `jinja2` (HTML report templating)
- Python built-in: `json`, `html`, `datetime`

---

## Sub-subtasks Breakdown

### 002.7.1: ClusteringVisualizer Class Setup
**Effort:** 2-3 hours
**Depends on:** None

**Steps:**
1. Create `ClusteringVisualizer` class with `__init__(self, pipeline_results: dict)`
2. Extract linkage matrix and branch assignments from pipeline_results
3. Validate input structure (raise ValueError for missing fields)
4. Initialize output path management
5. Add configuration loading from VISUALIZATION_CONFIG

**Success Criteria:**
- [ ] Class instantiates with valid pipeline_results
- [ ] Raises ValueError for invalid/missing data
- [ ] Configuration loaded and validated

---

### 002.7.2: Interactive Dendrogram
**Effort:** 4-5 hours
**Depends on:** 002.7.1

**Steps:**
1. Use `scipy.cluster.hierarchy.dendrogram` to extract plot data
2. Render with `plotly.graph_objects` for interactivity
3. Add color-coding by cluster assignment
4. Add configurable threshold line at clustering cut point
5. Add hover tooltips showing branch name, cluster ID, metrics
6. Enable zoom/pan controls
7. Support SVG/PNG export
8. Save as `dendrogram_<timestamp>.html` (~500KB)

**Success Criteria:**
- [ ] HTML file renders interactive dendrogram
- [ ] Clusters visually distinct by color
- [ ] Threshold line visible at correct height
- [ ] Hover shows branch details

---

### 002.7.3: Clustering Quality Dashboard (6 Charts)
**Effort:** 6-8 hours
**Depends on:** 002.7.1

**Steps:**
1. Create Silhouette Score Distribution bar chart (X: cluster ID, Y: avg score)
2. Create Cluster Size Distribution pie chart (slices per cluster with branch count)
3. Create Integration Target Distribution stacked bar (X: target, Y: count, stacked by risk)
4. Create Risk Level Distribution horizontal bar (X: count, Y: risk level, color-coded)
5. Create Metrics Correlation Matrix heatmap (commit history, codebase structure, diff distance)
6. Create Quality Metrics Summary text box (silhouette, Davies-Bouldin, Calinski-Harabasz with interpretation)
7. Arrange in dashboard layout
8. Save as `dashboard_<timestamp>.html` (~600KB)

**Success Criteria:**
- [ ] All 6 charts render without errors
- [ ] Interactive hover details on all charts
- [ ] Dashboard layout clean and responsive

---

### 002.7.4: Static HTML Report (8 Sections)
**Effort:** 4-6 hours
**Depends on:** 002.7.1

**Steps:**
1. Create jinja2 template with CSS styling (clean, professional, printable)
2. Render Header section (title, timestamp, repo path, branch/cluster/target counts)
3. Render Executive Summary (3-5 key findings, quality assessment, 2-3 recommendations)
4. Render Clustering Overview (total branches, clusters, avg size, method, distance metric)
5. Render Quality Assessment table (silhouette, Davies-Bouldin, Calinski-Harabasz with interpretations)
6. Render Integration Target Distribution table (target, count, avg confidence, key tags)
7. Render Top Insights (highest/lowest confidence, largest cluster, riskiest/most stable branch)
8. Render Detailed Branch Listing table (branch, target, cluster, confidence, risk, tags, metrics)
9. Render Recommendations (action items for high-risk, test strategies, optimization suggestions)
10. Save as `report_<timestamp>.html` (~400KB)

**Success Criteria:**
- [ ] All 8 sections present and populated
- [ ] CSS styling professional and printable
- [ ] No JavaScript required (static HTML)

---

### 002.7.5: Tag Distribution Analysis (3 Charts)
**Effort:** 3-4 hours
**Depends on:** 002.7.1

**Steps:**
1. Create Tag Frequency Chart horizontal bar (X: branch count, Y: tag name, top 20, sorted)
2. Create Tag Categories Distribution grouped bar (X: category, Y: unique tags, stacked)
3. Create Tag Co-occurrence Matrix heatmap (top 15 tags, values: branch count with both tags)
4. Embed in dashboard or generate separate file

**Success Criteria:**
- [ ] Tag frequency limited to max_tags_in_chart (default 20)
- [ ] Co-occurrence matrix symmetric and readable
- [ ] Categories correctly grouped

---

### 002.7.6: Summary Statistics JSON Export
**Effort:** 2-3 hours
**Depends on:** 002.7.1

**Steps:**
1. Aggregate clustering_summary (total_branches, total_clusters, avg/max/min cluster_size)
2. Aggregate quality_metrics (silhouette, davies_bouldin, calinski_harabasz, quality_assessment)
3. Aggregate integration_targets (per-target count, avg_confidence, tags)
4. Aggregate risk_distribution (low/medium/high counts)
5. Compute top_tags (tag, count pairs sorted by frequency)
6. Generate recommendations list (actionable strings)
7. Save as `summary_stats_<timestamp>.json` (~50KB)

**Success Criteria:**
- [ ] JSON matches schema exactly
- [ ] No NaN or Inf values
- [ ] All fields populated

---

### 002.7.7: Error Handling and Edge Cases
**Effort:** 2-3 hours
**Depends on:** 002.7.2, 002.7.3, 002.7.4, 002.7.5, 002.7.6

**Steps:**
1. Handle single-cluster input (degenerate dendrogram)
2. Handle many-small-clusters input (chart scaling)
3. Handle missing/None values in pipeline_results
4. Handle extreme metric values (all zeros, all ones)
5. Add graceful fallbacks for empty data
6. Add recommendation engine logic for edge cases

**Success Criteria:**
- [ ] No exceptions on any valid pipeline_results variant
- [ ] Meaningful output even with degenerate inputs

---

## Specification Details

### Class Interface

```python
class ClusteringVisualizer:
    def __init__(self, pipeline_results: dict)
    def generate_dendrogram(self, output_path: str = None) -> str
    def generate_dashboard(self, output_path: str = None) -> str
    def generate_report(self, output_path: str = None) -> str
    def export_summary_stats(self, output_path: str = None) -> dict
```

### Summary Stats JSON Schema

```json
{
  "clustering_summary": {
    "total_branches": 13,
    "total_clusters": 3,
    "average_cluster_size": 4.3,
    "max_cluster_size": 8,
    "min_cluster_size": 2
  },
  "quality_metrics": {
    "silhouette_score": 0.71,
    "davies_bouldin_index": 0.85,
    "calinski_harabasz_index": 15.3,
    "quality_assessment": "Good"
  },
  "integration_targets": {
    "main": {
      "count": 8,
      "avg_confidence": 0.89,
      "tags": ["core-feature", "stable", "low-risk"]
    },
    "scientific": {
      "count": 3,
      "avg_confidence": 0.76,
      "tags": ["experiment", "research", "medium-risk"]
    },
    "orchestration-tools": {
      "count": 2,
      "avg_confidence": 0.81,
      "tags": ["orchestration", "devops", "moderate-impact"]
    }
  },
  "risk_distribution": {
    "low-risk": 7,
    "medium-risk": 5,
    "high-risk": 1
  },
  "top_tags": [
    {"tag": "active-development", "count": 11},
    {"tag": "low-risk", "count": 7},
    {"tag": "testing-required-medium", "count": 6}
  ],
  "recommendations": [
    "Cluster 2 has low silhouette score (0.45) - consider adjusting threshold",
    "2 branches tagged 'high-risk' require enhanced testing",
    "Orchestration-tools cluster is small - monitor for stability"
  ]
}
```

### Dashboard Chart Descriptions

| Chart | Type | X-Axis | Y-Axis | Notes |
|-------|------|--------|--------|-------|
| Silhouette Score | Bar | Cluster ID | Avg silhouette | >0.5 good, >0.7 excellent |
| Cluster Size | Pie | — | — | Slices per cluster with branch count |
| Integration Target | Stacked Bar | Target name | Branch count | Stacked by risk level |
| Risk Level | Horizontal Bar | Branch count | Risk level | Color-coded low/medium/high |
| Correlation | Heatmap | Metric name | Metric name | Values in [-1, 1], red-blue scale |
| Quality Summary | Text Box | — | — | Score, index, interpretation |

### Report Sections

| Section | Content |
|---------|---------|
| Header | Title, timestamp, repo path, summary counts |
| Executive Summary | 3-5 key findings, quality assessment, 2-3 recommendations |
| Clustering Overview | Total branches/clusters, avg size, method (Ward), metric (Euclidean) |
| Quality Assessment | Table: metric, value, interpretation |
| Integration Target Distribution | Table: target, count, avg confidence, key tags |
| Top Insights | Highest/lowest confidence, largest cluster, riskiest/most stable branch |
| Detailed Branch Listing | Table: branch, target, cluster, confidence, risk, tags, metrics |
| Recommendations | Action items, test strategies, optimizations, downstream notes |

### Output Files

| File | Format | Size | Purpose |
|------|--------|------|---------|
| `dendrogram_*.html` | HTML + Plotly | ~500 KB | Interactive clustering visualization |
| `dashboard_*.html` | HTML + Plotly | ~600 KB | Quality metrics and distributions |
| `report_*.html` | HTML + CSS | ~400 KB | Comprehensive summary report |
| `summary_stats_*.json` | JSON | ~50 KB | Aggregated statistics and recommendations |

---

## Implementation Guide

### Step 1: Class Initialization
```python
class ClusteringVisualizer:
    def __init__(self, pipeline_results: dict):
        self._validate_input(pipeline_results)
        self.results = pipeline_results
        self.linkage_matrix = pipeline_results.get('linkage_matrix')
        self.branch_assignments = pipeline_results.get('branch_assignments')
        self.quality_metrics = pipeline_results.get('quality_metrics')
        self.config = VISUALIZATION_CONFIG.copy()
```

### Step 2: Dendrogram Generation
```python
def generate_dendrogram(self, output_path: str = None) -> str:
    from scipy.cluster.hierarchy import dendrogram as scipy_dendro
    import plotly.graph_objects as go

    dendro_data = scipy_dendro(self.linkage_matrix, no_plot=True,
                                labels=[b['name'] for b in self.branch_assignments])
    fig = go.Figure()
    # Add icoord/dcoord traces with cluster color mapping
    # Add threshold horizontal line
    # Add hover tooltips
    fig.update_layout(title="Branch Clustering Dendrogram",
                      template=self.config['theme'])
    path = output_path or f"dendrogram_{datetime.now():%Y%m%d_%H%M%S}.html"
    fig.write_html(path)
    return path
```

### Step 3: Dashboard Generation
```python
def generate_dashboard(self, output_path: str = None) -> str:
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=3, cols=2, subplot_titles=[...])
    # Row 1: Silhouette bar + Cluster size pie
    # Row 2: Integration target stacked bar + Risk horizontal bar
    # Row 3: Correlation heatmap + Quality text annotation
    path = output_path or f"dashboard_{datetime.now():%Y%m%d_%H%M%S}.html"
    fig.write_html(path)
    return path
```

### Step 4: Report Generation with Jinja2
```python
def generate_report(self, output_path: str = None) -> str:
    from jinja2 import Template
    template = Template(REPORT_HTML_TEMPLATE)
    html = template.render(
        title="Branch Clustering Analysis Report",
        timestamp=datetime.now().isoformat(),
        repo_path=self.results.get('repo_path', 'unknown'),
        summary=self._compute_summary(),
        quality=self.quality_metrics,
        targets=self._compute_target_distribution(),
        insights=self._compute_top_insights(),
        branches=self.branch_assignments,
        recommendations=self._compute_recommendations()
    )
    path = output_path or f"report_{datetime.now():%Y%m%d_%H%M%S}.html"
    with open(path, 'w') as f:
        f.write(html)
    return path
```

---

## Configuration & Defaults

```python
VISUALIZATION_CONFIG = {
    "theme": "plotly_white",
    "color_palette": "Set3",
    "figure_width": 1000,
    "figure_height": 600,
    "font_family": "Arial",
    "font_size": 12,
    "include_dendrogram": True,
    "include_dashboard": True,
    "include_report": True,
    "include_stats": True,
    "max_tags_in_chart": 20
}
```

All parameters configurable via `__init__` kwargs or external config file. Theme options: `plotly_white`, `plotly_dark`. Color palette options: any valid Plotly colorscale name.

---

## Typical Development Workflow

1. Implement `ClusteringVisualizer.__init__()` with input validation
2. Implement `generate_dendrogram()` — test with sample linkage matrix
3. Implement `generate_dashboard()` — build each chart individually, then combine
4. Implement `generate_report()` — create jinja2 template, then render
5. Implement `export_summary_stats()` — aggregate and serialize
6. Add tag distribution analysis charts
7. Add error handling for edge cases (single cluster, empty data)
8. Add docstrings (Google style) to all public methods
9. Test with sample pipeline results (13 branches, 3 clusters)
10. Validate all HTML renders in browser
11. Run with different data sizes (5 to 100 branches)
12. Verify file sizes match expectations

---

## Integration Handoff

### For Task 002.8 (TestingSuite)
- Provide 5 test scenarios: standard results, single cluster, many small clusters, extreme metrics, empty/missing data
- All generation methods return file paths for assertion

### For Task 002.9 (FrameworkIntegration)
- `ClusteringVisualizer` is imported and called via `framework.get_visualization_paths()`
- Summary stats JSON consumed by `validate_downstream_compatibility()`
- All output files referenced in `export_outputs()` return dict

---

## Common Gotchas & Solutions

**Gotcha 1: Plotly figure size exceeding memory with many branches**
```python
# WRONG: Rendering 100+ branch labels in dendrogram without truncation
# RIGHT: Truncate labels to 30 chars, limit leaf nodes displayed
labels = [name[:30] for name in branch_names]
```

**Gotcha 2: NaN values in correlation matrix**
```python
# WRONG: pandas.DataFrame.corr() on columns with zero variance
# RIGHT: Check for zero variance columns first, replace NaN with 0
corr_matrix = df.corr().fillna(0)
```

**Gotcha 3: Jinja2 template escaping HTML in branch names**
```python
# WRONG: Using {{ branch_name }} without escaping
# RIGHT: Use |e filter or Markup for safe rendering
{{ branch_name | e }}
```

**Gotcha 4: Timestamp collision in output filenames**
```python
# WRONG: Using seconds-only timestamp (collisions in batch mode)
# RIGHT: Include microseconds
f"dendrogram_{datetime.now():%Y%m%d_%H%M%S_%f}.html"
```

---

## Integration Checkpoint

**When to move to Task 002.8 (TestingSuite):**

- [ ] All 7 sub-subtasks complete
- [ ] All 4 output types generated successfully (dendrogram, dashboard, report, stats JSON)
- [ ] All 6 dashboard charts render without errors
- [ ] All 8 report sections populated
- [ ] Summary stats JSON validates against schema
- [ ] Tag distribution analysis produces 3 charts
- [ ] 5 test scenarios verified (standard, single cluster, many clusters, extreme values, empty data)
- [ ] All HTML renders correctly in browser
- [ ] Performance acceptable (generation < 30 seconds for 13 branches)
- [ ] Code review approved
- [ ] Commit message: "feat: complete Task 002.7 VisualizationReporting"

---

## Done Definition

Task 002.7 is done when:

1. All 7 sub-subtasks marked complete
2. `generate_dendrogram()` produces interactive HTML with cluster colors and threshold line
3. `generate_dashboard()` produces HTML with all 6 charts
4. `generate_report()` produces static HTML with all 8 sections
5. `export_summary_stats()` returns valid JSON matching schema
6. Tag distribution analysis produces 3 charts
7. All edge cases handled (single cluster, empty data, extreme values)
8. All output files match expected sizes (~500KB, ~600KB, ~400KB, ~50KB)
9. Code review approved
10. Ready for hand-off to Task 002.8

---

## Provenance

**Source:** HANDOFF_75.7_VisualizationReporting
**Original Task ID:** 75.7
**Migrated To:** 002.7
**Migration Date:** 2026-01-29
**Consolidation:** All content from HANDOFF preserved in 14-section standard format

---

## Next Steps

1. **Immediate:** Begin with sub-subtask 002.7.1 (Design Visualization Architecture and Dashboard Layout)
2. **Week 1:** Complete all 7 sub-subtasks with proper visualization components
3. **Week 1-2:** Implement interactive HTML dashboard with all 6 chart types
4. **Week 2:** Create PDF report generation with key metrics and visualizations
5. **Week 2:** Write comprehensive tests for all 5 visualization scenarios
6. **Week 2-3:** Performance validation and responsiveness optimization
7. **Week 3:** Code review and documentation completion
8. **Upon completion:** Ready for hand-off to Task 002.8 (TestingSuite)
9. **Parallel tasks:** Task 002.8 (TestingSuite), Task 002.9 (FrameworkIntegration) can proceed in parallel
