# Exact Subtasks for Branch Analysis: Identification, Classification, Investigation, and Semantic Understanding

## Overview
This document identifies the exact subtasks associated with branch identification, classification, investigation, and semantic understanding that maximize architectural choices understanding for future alignment tasks. These subtasks ensure that future alignment tasks are completely specified regarding refactoring and any changes required.

## Primary Branch Analysis Tasks

### Task 001: Framework Definition for Branch Alignment
- **Purpose**: Establish strategic framework and decision criteria for aligning feature branches
- **Focus**: Defines HOW branches should be aligned rather than performing alignment

#### Subtasks:
1. **001.1**: Identify All Active Feature Branches
2. **001.2**: Analyze Git History and Codebase Similarity
3. **001.3**: Define Target Selection Criteria
4. **001.4**: Propose Optimal Targets with Justifications
5. **001.5**: Create ALIGNMENT_CHECKLIST.md
6. **001.6**: Define Merge vs Rebase Strategy
7. **001.7**: Create Architectural Prioritization Guidelines
8. **001.8**: Define Safety and Validation Procedures

### Task 002: Branch Clustering System (Advanced Analysis)
- **Purpose**: Intelligent branch clustering and target assignment system
- **Focus**: Data-driven analysis to automatically determine optimal integration targets

#### Subtasks:
1. **002.1**: CommitHistoryAnalyzer
   - Analyze Git commit history for each feature branch
   - Extract metrics like commit frequency, author patterns, merge points, divergence dates
   - Calculate divergence metrics from main/scientific/orchestration-tools
   - Identify shared history points and merge bases

2. **002.2**: CodebaseStructureAnalyzer
   - Analyze file structure and code organization of each feature branch
   - Fingerprint architectural characteristics
   - Map directory structure and file counts per branch
   - Identify language distribution and module boundaries
   - Generate structural fingerprints for comparison

3. **002.3**: DiffDistanceCalculator
   - Calculate code distance metrics between feature branches and targets
   - Compute file-level diffs using various algorithms
   - Calculate similarity scores (Jaccard, edit distance, etc.)
   - Identify changed files and weight changes by significance
   - Generate distance vectors for clustering

4. **002.4**: BranchClusterer
   - Cluster feature branches by similarity using analysis outputs
   - Combine metrics from CommitHistoryAnalyzer, CodebaseStructureAnalyzer, DiffDistanceCalculator
   - Apply clustering algorithm (K-means, hierarchical, or DBSCAN)
   - Group branches targeting the same integration point
   - Assign confidence scores to cluster assignments

5. **002.5**: IntegrationTargetAssigner
   - Assign optimal integration targets (main, scientific, orchestration-tools) to each branch
   - Take clustered branches and metrics as input
   - Apply Task 001 framework criteria to refine assignments
   - Calculate confidence scores for each target assignment
   - Generate justification for recommendations

6. **002.6**: PipelineIntegration
   - Integrate clustering system with alignment pipeline (Tasks 016-017)
   - Read categorized_branches.json from Task 002.5 output
   - Feed branch assignments to Task 016 orchestrator
   - Handle Task 007 as execution mode

7. **002.7**: VisualizationReporting
   - Generate visualizations and reports from clustering analysis
   - Create branch similarity heatmaps
   - Generate cluster assignment visualizations
   - Produce target distribution charts and confidence score distributions

8. **002.8**: TestingSuite
   - Develop comprehensive test suite for all Task 002 components
   - Unit tests for all modules (002.1-002.7)
   - Integration tests between components
   - Performance benchmarks and end-to-end workflow tests

9. **002.9**: FrameworkIntegration
   - Final integration of Task 002 with Task 001 framework
   - Finalize Task 001 + Task 002 data flow
   - Document usage and workflows
   - Create onboarding guide

### Task 007: Feature Branch Identification and Categorization Tool
- **Purpose**: Automatically identify active feature branches and suggest optimal targets
- **Focus**: Command-line tool for branch analysis and categorization

#### Subtasks:
1. **007.1**: Implement Destructive Merge Artifact Detection
   - Extend branch analysis to identify merge conflict markers
   - Detect '<<<<<<<', '=======', '>>>>>>>', patterns in feature branches
   - Flag branches with artifacts in output
   - Contribute to lower confidence scores for affected branches

2. **007.2**: Develop Logic for Detecting Content Mismatches
   - Compare feature branches to proposed primary targets
   - Identify significant content differences beyond typical divergence
   - Detect cases where branch named for one target shows higher similarity to another
   - Generate 'content_mismatch_alert' in output

3. **007.3**: Integrate Backend-to-Src Migration Status Analysis
   - Evaluate backend→src migration status within each feature branch
   - Check for presence/absence/modification patterns of migration-related files
   - Assess if migration is complete, incomplete, or inconsistent
   - Categorize branches as 'migrated', 'partially_migrated', 'not_migrated', or 'inconsistent'

## Architectural Choices Focus

### For Maximum Understanding in Future Alignment Tasks

#### 1. Architectural Prioritization Guidelines (Task 001.7)
- **Purpose**: Define how to handle architectural differences between branches
- **Focus**: When to prefer advanced architectural patterns from feature branches over target branches
- **Impact**: Guides refactoring decisions in alignment tasks
- **Specification for Future Tasks**: 
  - Framework for preferring advanced architectures from feature branches
  - Guidelines for documenting partial updates to target branch architecture
  - Criteria for architectural compatibility assessment
  - Decision points for prioritizing feature branch vs target branch patterns

#### 2. Merge vs Rebase Strategy (Task 001.6)
- **Purpose**: Document when to use merge versus rebase for alignment
- **Focus**: Strategic decision-making for branch integration
- **Impact**: Affects refactoring approach in alignment tasks
- **Specification for Future Tasks**:
  - Conditions for merge (preserve history, large teams)
  - Conditions for rebase (clean linear history, small teams)
  - Conflict resolution procedures
  - When to use visual merge tools

#### 3. Safety and Validation Procedures (Task 001.8)
- **Purpose**: Define backup, validation, and rollback procedures
- **Focus**: Safe alignment operations without data loss
- **Impact**: Critical for refactoring and change operations
- **Specification for Future Tasks**:
  - Backup procedures (branch-backup-pre-align naming)
  - Pre/post-alignment validation (test suite baselines)
  - Regression testing approach
  - Rollback procedures

## Semantic Understanding Components

### 1. Codebase Similarity Analysis (Task 002.2 & 002.3)
- **Semantic Focus**: Understanding what code does and how it relates to other branches
- **Analysis**: Structural fingerprinting, language distribution, module boundaries
- **Output**: Quantified similarity scores between branches and targets

### 2. Git History Analysis (Task 002.1)
- **Semantic Focus**: Understanding development patterns and evolution
- **Analysis**: Commit frequency, author patterns, merge points, divergence dates
- **Output**: Historical context for each branch

### 3. Content Mismatch Detection (Task 007.2)
- **Semantic Focus**: Understanding when branch content doesn't match its naming/conceptual target
- **Analysis**: Enhanced diff analysis, file hash comparisons, structural comparisons
- **Output**: Mismatch alerts with specific rationales

## Classification and Investigation Components

### 1. Branch Classification (Task 002.4 & 002.5)
- **Classification Focus**: Grouping branches by similarity and assigning targets
- **Investigation**: Combining multiple analysis dimensions to make informed decisions
- **Output**: Categorized branches with confidence scores

### 2. Feature Branch Identification (Task 001.1 & Task 007)
- **Identification Focus**: Cataloging all active feature branches that need analysis
- **Investigation**: Using git commands to list and analyze remote branches
- **Output**: Complete list of branches for further analysis

### 3. Migration Status Analysis (Task 007.3)
- **Classification Focus**: Categorizing branches by migration status
- **Investigation**: Checking directory structures and file contents for migration indicators
- **Output**: Migration status (migrated, partially_migrated, not_migrated, inconsistent)

## Integration with Future Alignment Tasks

### How These Subtasks Maximize Architectural Understanding for Alignment

1. **Pre-Alignment Analysis**: These subtasks provide comprehensive understanding of branch content, history, and architecture before any alignment begins

2. **Decision Framework**: Task 001 provides the strategic framework for making alignment decisions

3. **Data-Driven Insights**: Task 002 provides quantitative analysis to support alignment decisions

4. **Risk Assessment**: Task 007 identifies potential issues (merge artifacts, content mismatches) that could complicate alignment

5. **Specification Completeness**: All subtasks ensure that when alignment tasks are created, they have complete information about:
   - What needs to be refactored
   - Why specific approaches should be taken
   - What architectural patterns should be preserved or adopted
   - What risks are associated with the alignment
   - What validation is needed

## Expected Output Format

All these subtasks contribute to generating `categorized_branches.json` with:
- Branch names and metadata
- Target assignments with confidence scores
- Justifications for each assignment
- Migration status
- Content mismatch alerts
- Merge artifact detections
- Architectural prioritization recommendations

This output provides complete specifications for future alignment tasks, ensuring they are completely specified regarding refactoring and any changes required.