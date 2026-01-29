# Task 75.7: Visualization & Reporting Module

## Quick Summary
Implement visualization and reporting tools that present clustering results through interactive dashboards, dendrograms, and summary reports. This is a Stage Three component—depends on Tasks 75.1-75.6.

**Effort:** 20-28 hours | **Complexity:** 6/10 | **Parallelizable:** No (depends on 75.6)

---

## What to Build

A Python module `ClusteringVisualizer` that:
1. Generates interactive dendrogram visualization
2. Creates clustering quality metric dashboards
3. Produces static HTML reports
4. Exports summary statistics and insights
5. Generates tag distribution charts

### Class Signature
```python
class ClusteringVisualizer:
    def __init__(self, pipeline_results: dict)
    def generate_dendrogram(self, output_path: str = None) -> str
    def generate_dashboard(self, output_path: str = None) -> str
    def generate_report(self, output_path: str = None) -> str
    def export_summary_stats(self, output_path: str = None) -> dict
```

---

## Visualization 1: Interactive Dendrogram

### Purpose
Display hierarchical clustering structure with branch names and cluster cuts.

### Features
- Interactive hover tooltips showing branch details
- Color-coded clusters (different color per cluster)
- Configurable threshold line showing where dendrogram was cut
- Zoom/pan controls
- Export as SVG or PNG

### Output Format
HTML file with embedded Plotly visualization:
- File: `dendrogram_<timestamp>.html`
- Size: ~500 KB
- Interactive: Yes (zoom, pan, hover)

### Implementation
```python
def generate_dendrogram(self, output_path: str = None) -> str:
    """
    Generate interactive dendrogram from linkage matrix.
    
    Args:
        output_path: Path to save HTML file
        
    Returns:
        Path to generated file
    """
    # Use scipy.cluster.hierarchy.dendrogram to extract data
    # Use plotly.graph_objects to render interactive visualization
    # Add threshold line at clustering_threshold
    # Color branches by cluster assignment
    # Return file path
```

---

## Visualization 2: Clustering Quality Dashboard

### Purpose
Display clustering quality metrics and distribution of branches across clusters.

### Charts Included

1. **Silhouette Score Distribution** (bar chart)
   - X-axis: Cluster ID
   - Y-axis: Average silhouette score per cluster
   - Interpretation: >0.5 good, >0.7 excellent

2. **Cluster Size Distribution** (pie chart)
   - Slices: One per cluster
   - Label: Cluster ID and branch count
   - Interpretation: Balanced vs. imbalanced clustering

3. **Integration Target Distribution** (stacked bar)
   - X-axis: Integration target (main, scientific, orchestration-tools)
   - Y-axis: Number of branches
   - Stacked by risk level

4. **Risk Level Distribution** (horizontal bar)
   - X-axis: Number of branches
   - Y-axis: Risk level (low, medium, high)
   - Color-coded

5. **Metrics Correlation Matrix** (heatmap)
   - Rows/columns: Commit history, codebase structure, diff distance
   - Values: Correlation coefficients [-1, 1]
   - Color scale: Red (positive) to blue (negative)

6. **Quality Metrics Summary** (text box)
   - Silhouette score: X.XX (range: [-1, 1])
   - Davies-Bouldin index: X.XX (lower is better)
   - Calinski-Harabasz index: X.XX (higher is better)
   - Interpretation: Good/fair/poor

### Output Format
HTML file with embedded Plotly dashboard:
- File: `dashboard_<timestamp>.html`
- Size: ~600 KB
- Interactive: Yes (hover details, click to filter)

---

## Visualization 3: Static HTML Report

### Purpose
Comprehensive one-page summary report with key findings and recommendations.

### Report Sections

#### Header
- Title: "Branch Clustering Analysis Report"
- Generated: Timestamp
- Repository: Repo path
- Summary: X branches, Y clusters, Z integration targets

#### Executive Summary
- Key findings (3-5 bullet points)
- Overall clustering quality assessment
- Recommendations (2-3 bullet points)

#### Clustering Overview
- Total branches: X
- Total clusters: Y
- Average cluster size: Z
- Clustering method: Hierarchical agglomerative (Ward)
- Distance metric: Euclidean

#### Quality Assessment
Table with metrics:
| Metric | Value | Interpretation |
|--------|-------|-----------------|
| Silhouette Score | 0.71 | Excellent |
| Davies-Bouldin Index | 0.85 | Good |
| Calinski-Harabasz Index | 15.3 | Good |

#### Integration Target Distribution
Table:
| Target | Count | Avg Confidence | Key Tags |
|--------|-------|-----------------|----------|
| main | 8 | 0.89 | core-feature, stable |
| scientific | 3 | 0.76 | experiment, research |
| orchestration-tools | 2 | 0.81 | orchestration, devops |

#### Top Insights
- Highest confidence assignment: [branch, confidence, target]
- Lowest confidence assignment: [branch, confidence, target]
- Largest cluster: [cluster_id, size, description]
- Riskiest branch: [branch, risk_score, tags]
- Most stable branch: [branch, stability_score, tags]

#### Detailed Branch Listing
Table with columns:
| Branch | Target | Cluster | Confidence | Risk | Tags | Metrics |
|--------|--------|---------|------------|------|------|---------|

#### Recommendations
- Action items for high-risk branches
- Suggested test strategies for each target
- Potential optimizations for clustering
- Downstream task integration notes

### Output Format
HTML file with CSS styling:
- File: `report_<timestamp>.html`
- Size: ~400 KB
- Interactive: Limited (no JavaScript)
- Printable: Yes

---

## Visualization 4: Tag Distribution Analysis

### Purpose
Show distribution of tags across branches and identify patterns.

### Charts Included

1. **Tag Frequency Chart** (horizontal bar)
   - X-axis: Number of branches with tag
   - Y-axis: Tag name (top 20)
   - Sorted by frequency

2. **Tag Categories Distribution** (grouped bar)
   - X-axis: Tag category (scope, risk, complexity, etc.)
   - Y-axis: Number of unique tags
   - Stacked by category

3. **Tag Co-occurrence Matrix** (heatmap)
   - Rows/columns: Top 15 tags
   - Values: Count of branches with both tags
   - Color scale: Frequency

### Output Format
Embedded in dashboard HTML or separate file.

---

## Summary Statistics Export

### Output Format
JSON file with aggregated statistics:

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

---

## Implementation Checklist

- [ ] Create `ClusteringVisualizer` class
- [ ] Initialize with pipeline_results dict
- [ ] Extract linkage matrix and branch assignments from input
- [ ] Implement `generate_dendrogram()` using scipy and plotly
- [ ] Add color-coding by cluster
- [ ] Add threshold line visualization
- [ ] Implement `generate_dashboard()` with 6+ charts
- [ ] Create silhouette distribution chart
- [ ] Create cluster size pie chart
- [ ] Create integration target distribution chart
- [ ] Create risk level distribution chart
- [ ] Create metrics correlation heatmap
- [ ] Add quality metrics summary text
- [ ] Implement `generate_report()` with HTML formatting
- [ ] Include all report sections listed above
- [ ] Add CSS styling (clean, professional)
- [ ] Implement `export_summary_stats()` with JSON output
- [ ] Generate tag distribution analysis
- [ ] Create tag frequency chart
- [ ] Create tag co-occurrence analysis
- [ ] Add recommendation engine logic
- [ ] Implement error handling for missing/invalid data
- [ ] Add docstrings (Google style)
- [ ] Return file paths for all generated outputs

---

## Technology Stack

- `plotly` (interactive visualizations)
- `scipy.cluster.hierarchy` (dendrogram data extraction)
- `pandas` (data aggregation)
- `jinja2` (HTML report templating)
- Python built-in: `json`, `html`, `datetime`

---

## Test Cases

1. **Standard results**: 13 branches, 3 clusters, normal metrics
2. **Single cluster**: All branches in one cluster (quality check)
3. **Many small clusters**: Each branch separate (quality check)
4. **Quality metrics edge cases**: Extreme values in metrics
5. **Empty/missing data**: Graceful handling of incomplete data

---

## Dependencies

- Outputs from **Task 75.6 (BranchClusteringPipeline)** (required)
- Python built-in modules
- External: `plotly`, `scipy`, `pandas`, `jinja2`
- Feeds into **Task 75.8 (Testing Suite)**

---

## Configuration

Accept these parameters in `__init__` or config file:

```python
VISUALIZATION_CONFIG = {
    "theme": "plotly_white",  # or "plotly_dark"
    "color_palette": "Set3",  # Plotly colorscale
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

---

## Output Files Summary

| File | Format | Size | Purpose |
|------|--------|------|---------|
| dendrogram_*.html | HTML + Plotly | ~500 KB | Interactive clustering visualization |
| dashboard_*.html | HTML + Plotly | ~600 KB | Quality metrics and distributions |
| report_*.html | HTML + CSS | ~400 KB | Comprehensive summary report |
| summary_stats_*.json | JSON | ~50 KB | Aggregated statistics and recommendations |

---

## Next Steps After Completion

1. Unit test with sample pipeline results
2. Validate HTML output renders correctly (in browser)
3. Test with different data sizes (5 to 100 branches)
4. Verify all charts render without errors
5. Pass results to Task 75.8 (Testing Suite)

**Blocked by:** 75.6 (must complete first)
**Enables:** 75.8, 75.9 (Stage Three)
