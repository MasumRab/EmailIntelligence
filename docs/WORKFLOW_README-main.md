# 📚 Documentation Branch Workflow System

## Overview

The Documentation Branch Workflow System automatically manages documentation across `main` and `scientific` branches, intelligently determining when content should be shared versus kept branch-specific.

### Agent Context Control Integration

This workflow integrates with the Agent Context Control system to ensure documentation changes respect branch-specific access boundaries. The context control system automatically detects the current branch and applies appropriate access controls, preventing AI agents from working outside their designated scope.

**Context Profiles:**
- **main**: Focus on production-ready documentation, user guides, and deployment procedures
- **scientific**: Emphasis on research methodologies, experimental features, and technical analysis
- **orchestration-tools**: Full access to infrastructure and tooling documentation

## 🏗️ System Architecture

### Core Components

1. **Branch Versioning Engine** (`scripts/docs_branch_versioning.py`)
   - Creates branch-specific documentation versions
   - Manages file naming and organization
   - Handles cleanup of orphaned versions

2. **Content Analyzer** (`scripts/docs_content_analyzer.py`)
   - Compares documentation between branches
   - Analyzes goals, audience, and technical depth
   - Generates sharing recommendations

3. **Merge Strategist** (`scripts/docs_merge_strategist.py`)
   - Determines optimal sharing strategy
   - Executes automated merge decisions
   - Creates review requests for complex cases

4. **Review Manager** (`scripts/docs_review_manager.py`)
   - Manages review workflow and queue
   - Provides dashboard interface
   - Tracks approval and decision history

5. **Workflow Trigger** (`scripts/docs_workflow_trigger.py`)
   - Orchestrates the complete workflow
   - Triggers analysis and strategy determination
   - Provides status reporting

## 🔄 Workflow Process

### 1. Documentation Edit
```bash
# Edit documentation normally
vim docs/api/API_REFERENCE.md
git add docs/api/API_REFERENCE.md
git commit -m "docs: update API authentication section"
```

### 2. Automatic Branch Versioning (Pre-commit)
- System detects documentation changes
- Creates branch-specific versions (e.g., `API_REFERENCE-main.md`)
- Maintains unified base versions

### 3. Content Analysis (Post-commit)
- Analyzes content differences between branches
- Evaluates goal similarity, audience overlap, technical depth
- Generates intelligent sharing recommendations

### 4. Strategy Determination
- **SHARE**: High similarity, merge to both branches
- **BRANCH_SPECIFIC**: Significant differences, keep separate
- **MANUAL_REVIEW**: Complex cases requiring human decision

### 5. Review & Execution
- Automated decisions execute immediately
- Manual reviews create structured review requests
- Reviewers approve/reject sharing decisions

## 🎯 Decision Criteria

### Share Content When:
- **Goal Similarity** > 80%
- **Audience Overlap** > Audience Differences
- **Technical Depth Difference** < 2.0
- Content serves similar purposes across branches

### Keep Branch-Specific When:
- **Goal Similarity** < 30%
- **Audience Differences** > Audience Overlap × 2
- **Technical Depth Difference** > 5.0
- Content serves fundamentally different purposes

### Manual Review When:
- Mixed criteria, unclear best approach
- High business impact decisions
- Complex stakeholder considerations

## 📋 Usage Guide

### Check Review Status
```bash
python scripts/docs_review_manager.py --dashboard
```

### Review Specific Document
```bash
python scripts/docs_review_manager.py --details REVIEW_ID
```

### Approve Review Decision
```bash
python scripts/docs_review_manager.py --approve "review_123:SHARE:reviewer_name:High similarity in goals"
```

### Manual Analysis
```bash
python scripts/docs_content_analyzer.py docs/api/API_REFERENCE.md --save
```

### Force Strategy Determination
```bash
python scripts/docs_merge_strategist.py --analyze docs/api/API_REFERENCE.md
```

## 📁 File Organization

```
docs/
├── .branch-config.json          # Branch-specific rules and settings
├── .review-queue.json           # Active review requests
├── .merge-history.json          # Decision audit trail
├── reviews/                     # Manual review files
│   └── review_{id}.md
├── WORKFLOW_README.md           # This documentation
└── [existing docs structure]
```

## ⚙️ Configuration

### Branch Configuration (`docs/.branch-config.json`)
```json
{
  "branches": {
    "main": {
      "purpose": "production-ready implementations",
      "audience": ["end-users", "administrators"],
      "content_focus": ["deployment", "user-guides"]
    },
    "scientific": {
      "purpose": "research and experimental features",
      "audience": ["researchers", "scientists"],
      "content_focus": ["methodologies", "algorithms"]
    }
  },
  "sharing_rules": {
    "high_overlap_threshold": 0.8,
    "manual_review_threshold": 0.6
  }
}
```

### Git Hooks Integration
- **Pre-commit**: Creates branch-specific versions
- **Post-commit**: Triggers analysis workflow
- **Post-checkout**: Syncs documentation on branch switches

## 📊 Monitoring & Analytics

### Review Dashboard Metrics
- **Pending Reviews**: Currently awaiting decisions
- **Completion Rate**: Percentage of reviews completed
- **Average Review Time**: Time from creation to decision
- **Strategy Distribution**: SHARE vs BRANCH_SPECIFIC ratios

### Quality Metrics
- **Accuracy Rate**: Percentage of automated decisions accepted
- **Override Rate**: Manual corrections of automated decisions
- **Consistency Score**: Documentation parity between branches

## 🔧 Maintenance

### Regular Tasks
```bash
# Clean up old reviews (older than 30 days)
python scripts/docs_review_manager.py --cleanup 30

# Audit merge decisions
python scripts/docs_merge_strategist.py --status

# Update branch configuration
vim docs/.branch-config.json
```

### Troubleshooting
- **Hook not triggering**: Check file permissions and Python path
- **Analysis failing**: Verify git repository state and file access
- **Review queue corrupted**: Reset with empty JSON structure

## 🎯 Best Practices

### For Contributors
1. **Write clear commit messages** with "docs:" prefix
2. **Test changes** on both branches when possible
3. **Review automated decisions** for complex changes
4. **Provide context** in review decisions

### For Reviewers
1. **Consider business impact** of sharing decisions
2. **Review goal alignment** carefully
3. **Document reasoning** for non-obvious decisions
4. **Monitor patterns** for process improvements

### For Maintainers
1. **Regular configuration updates** based on team feedback
2. **Monitor quality metrics** for system improvements
3. **Review audit trails** for process optimization
4. **Update documentation** as workflow evolves

## 🚀 Advanced Features

### Custom Analysis Rules
Extend `docs_content_analyzer.py` with domain-specific analysis logic.

### Integration APIs
All components provide programmatic APIs for integration with other tools.

### Batch Processing
Process multiple documents simultaneously for bulk operations.

---

## 📞 Support

For issues with the documentation workflow:
1. Check this guide for configuration issues
2. Review error logs in workflow scripts
3. Create issue with "documentation-workflow" label
4. Contact the development team for complex issues

**Version**: 1.0
**Last Updated**: November 2, 2025</content>
</xai:function_call">Create workflow documentation
