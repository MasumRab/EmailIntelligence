#!/usr/bin/env bash

# create-pr-resolution-spec.sh
# Create a PR resolution specification based on merge scenarios and architectural branch conflicts
# This script helps users create proper specifications for complex PR resolution scenarios
#
# Usage: ./create-pr-resolution-spec.sh [OPTIONS]
#
# OPTIONS:
#   --interactive    Interactive mode with guided prompts (default)
#   --template       Show only the specification template
#   --merge-info     Display merge conflict information first
#   --help, -h       Show help message

set -e

# Parse command line arguments
INTERACTIVE_MODE=true
SHOW_TEMPLATE=false
SHOW_MERGE_INFO=false

for arg in "$@"; do
    case "$arg" in
        --interactive)
            INTERACTIVE_MODE=true
            ;;
        --template)
            SHOW_TEMPLATE=true
            INTERACTIVE_MODE=false
            ;;
        --merge-info)
            SHOW_MERGE_INFO=true
            ;;
        --help|-h)
            cat << 'EOF'
Usage: create-pr-resolution-spec.sh [OPTIONS]

Create a PR resolution specification based on merge scenarios and architectural branch conflicts.
This script provides a guided template to help create proper specifications for complex PR resolution scenarios.

OPTIONS:
  --interactive    Interactive mode with guided prompts (default)
  --template       Show only the specification template
  --merge-info     Display current merge conflict information
  --help, -h       Show this help message

EXAMPLES:
  # Interactive guided specification creation
  ./create-pr-resolution-spec.sh
  
  # Show specification template only
  ./create-pr-resolution-spec.sh --template
  
  # Check current merge conflicts
  ./create-pr-resolution-spec.sh --merge-info

EOF
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Get repository and merge information
eval $(get_feature_paths)

# Function to get current merge status
get_merge_status() {
    echo "=== Current Merge Status ==="
    
    # Check if we're in a merge conflict
    if git status --porcelain | grep -q "^UU"; then
        echo "STATUS: In merge conflict"
        
        # Show conflicted files
        echo "CONFlicted files:"
        git status --porcelain | grep "^UU" | awk '{print "  " $2}'
        
        # Show merge base information
        echo "MERGE base: $(git merge-base HEAD $(git branch --show-current))"
        
    elif git status --porcelain | grep -q "^.M"; then
        echo "STATUS: Changes detected (not in conflict)"
        git status --porcelain | grep "^.M" | head -5 | awk '{print "  " $2 " (" $1 ")"}'
        echo "  ... and more"
        
    else
        echo "STATUS: Clean working directory"
    fi
    
    echo
    echo "CURRENT BRANCH: $(git branch --show-current)"
    echo "REMOTES:"
    git remote -v 2>/dev/null || echo "  No remotes configured"
    
    echo
    echo "RECENT COMMITS:"
    git log --oneline -3
}

# Function to show merge conflict information
show_merge_info() {
    echo "🔍 Merge Conflict Analysis"
    echo "=========================="
    
    get_merge_status
    
    echo "⚡ Resolution Recommendations:"
    echo "1. Use 'git status' to see exact conflict files"
    echo "2. Use 'git diff' to see conflict differences"
    echo "3. Consider using 'git mergetool' for visual resolution"
    echo "4. Document resolution approach in specification"
    echo
}

# Function to create specification template
create_specification_template() {
    cat << 'EOF'
# PR Resolution Specification Template

## Merge Scenario Information

### Branch Details
- **Source Branch**: [branch-name]
- **Target Branch**: [branch-name] 
- **Merge Type**: [fast-forward/three-way/conflicted]
- **Architecture Impact**: [breaking/non-breaking/enhancement]

### Conflict Characteristics
- **Conflict Type**: [content/structural/architectural]
- **Complexity Level**: [simple/moderate/complex/critical]
- **Affected Areas**: [files/modules/components]

## Resolution Requirements

### Primary Objectives
1. **Primary Goal**: [What must be achieved]
2. **Constraints**: [Limitations or requirements]
3. **Success Criteria**: [How to measure success]

### Resolution Strategy Options

#### Option A: Conservative Merge
**Approach**: Minimal changes, preserve existing functionality
- **Pros**: Safe, minimal risk
- **Cons**: May lose new features
- **Risk Level**: Low
- **Effort**: Low

#### Option B: Feature Preservation
**Approach**: Integrate both branch features intelligently
- **Pros**: Preserves functionality from both branches
- **Cons**: More complex resolution
- **Risk Level**: Medium
- **Effort**: Medium

#### Option C: Refactoring Merge
**Approach**: Restructure to accommodate both approaches
- **Pros**: Cleanest final result
- **Cons**: High effort, potential for new bugs
- **Risk Level**: High
- **Effort**: High

### Recommended Resolution Plan

#### Phase 1: Analysis
- [ ] Analyze conflict patterns
- [ ] Identify architectural implications
- [ ] Assess enhancement preservation needs
- [ ] Document constitutional compliance requirements

#### Phase 2: Strategy Development
- [ ] Select resolution approach
- [ ] Plan worktree isolation strategy
- [ ] Define rollback procedures
- [ ] Create test validation plan

#### Phase 3: Execution
- [ ] Create isolated worktree environment
- [ ] Apply constitutional validation
- [ ] Execute resolution strategy
- [ ] Validate with test suite

#### Phase 4: Validation
- [ ] Verify all conflicts resolved
- [ ] Confirm constitutional compliance
- [ ] Run enhancement validation
- [ ] Document resolution approach

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| [Risk 1] | [Low/Med/High] | [Low/Med/High] | [Mitigation strategy] |
| [Risk 2] | [Low/Med/High] | [Low/Med/High] | [Mitigation strategy] |

### Resource Requirements
- **Development Time**: [X hours/days]
- **Testing Effort**: [X hours/days] 
- **Review Required**: [Yes/No - Who]
- **Rollback Complexity**: [Simple/Complex]

## Acceptance Criteria

### Functional Requirements
- [ ] All merge conflicts resolved
- [ ] No regression in existing functionality
- [ ] New features from both branches preserved
- [ ] Constitutional requirements met

### Quality Requirements
- [ ] Test suite passes completely
- [ ] Performance impact assessed and acceptable
- [ ] Documentation updated
- [ ] Team review completed

### Success Metrics
- **Resolution Time**: Target < [X] hours
- **Bug Rate**: < [X] new bugs introduced
- **Feature Preservation**: > [X]% of intended features
- **Review Score**: > [X]% positive feedback

## Notes and Assumptions

### Assumptions
- [Assumption 1]: [Description]
- [Assumption 2]: [Description]

### Dependencies
- [Dependency 1]: [Description and impact]
- [Dependency 2]: [Description and impact]

### Open Questions
- [Question 1]: [Description]
- [Question 2]: [Description]

---
*Generated by create-pr-resolution-spec.sh on $(date)*
EOF
}

# Function to run interactive mode
run_interactive_mode() {
    echo "🚀 PR Resolution Specification Creator"
    echo "======================================="
    echo
    echo "This tool helps you create detailed specifications for complex PR resolution scenarios."
    echo "It guides you through analyzing merge conflicts and defining resolution strategies."
    echo
    
    # Get basic information
    read -p "📋 What is the main objective for this PR resolution? (e.g., 'Merge feature/auth to main'): " OBJECTIVE
    echo
    
    read -p "🌿 Source branch: " SOURCE_BRANCH
    read -p "🎯 Target branch: " TARGET_BRANCH
    echo
    
    echo "📊 Conflict Analysis"
    echo "==================="
    read -p "How many files have conflicts? (or 'unknown'): " CONFLICT_COUNT
    read -p "What type of conflicts? (content/structural/architectural): " CONFLICT_TYPE
    read -p "Estimated complexity? (simple/moderate/complex/critical): " COMPLEXITY
    echo
    
    echo "🎨 Resolution Strategy"
    echo "====================="
    read -p "Preferred approach? (conservative/feature-preservation/refactoring): " APPROACH
    echo
    
    echo "⏱️ Planning"
    echo "==========="
    read -p "Estimated resolution time? (e.g., '2 hours', '1 day'): " TIME_ESTIMATE
    read -p "Who needs to review this? (names/roles): " REVIEWERS
    echo
    
    # Generate personalized template
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    cat << EOF
# PR Resolution Specification: $OBJECTIVE

*Generated: $timestamp*

## Merge Scenario Information

### Branch Details
- **Source Branch**: ${SOURCE_BRANCH:-"[NOT SPECIFIED]"}
- **Target Branch**: ${TARGET_BRANCH:-"[NOT SPECIFIED]"}
- **Merge Type**: [fast-forward/three-way/conflicted]
- **Architecture Impact**: [breaking/non-breaking/enhancement]

### Conflict Characteristics
- **Conflict Count**: ${CONFLICT_COUNT:-"[NOT SPECIFIED]"}
- **Conflict Type**: ${CONFLICT_TYPE:-"[NOT SPECIFIED]"}
- **Complexity Level**: ${COMPLEXITY:-"[NOT SPECIFIED]"}
- **Affected Areas**: [files/modules/components]

## Resolution Requirements

### Primary Objectives
1. **Primary Goal**: ${OBJECTIVE:-"[NOT SPECIFIED]"}
2. **Constraints**: [Technical/organizational constraints]
3. **Success Criteria**: [How to measure success]

### Selected Strategy
**Approach**: ${APPROACH:-"[NOT SPECIFIED]"}
- **Pros**: [Benefits of this approach]
- **Cons**: [Risks and challenges]
- **Risk Level**: [Low/Medium/High]
- **Effort**: [Low/Medium/High]

### Resource Requirements
- **Development Time**: ${TIME_ESTIMATE:-"[NOT SPECIFIED]"}
- **Review Required**: ${REVIEWERS:-"[NOT SPECIFIED]"}
- **Rollback Complexity**: [Simple/Complex]

---

## Next Steps

1. **Complete the template** above with detailed information
2. **Use this specification** with the EmailIntelligence CLI:
   \`\`\`bash
   eai setup-resolution --pr [PR_NUMBER] --source-branch ${SOURCE_BRANCH:-"SOURCE"} --target-branch ${TARGET_BRANCH:-"TARGET"}
   \`\`\`

3. **Follow the resolution workflow** with constitutional validation and enhancement preservation

---
*Template generated by create-pr-resolution-spec.sh*
EOF
    
    echo
    echo "💡 Tip: Copy the specification above to your resolution planning document"
    echo "🔧 Use the EmailIntelligence CLI with this specification for guided resolution"
}

# Main execution logic
main() {
    if $SHOW_MERGE_INFO; then
        show_merge_info
        exit 0
    fi
    
    if $SHOW_TEMPLATE; then
        create_specification_template
        exit 0
    fi
    
    if $INTERACTIVE_MODE; then
        run_interactive_mode
    else
        create_specification_template
    fi
}

# Execute main function
main "$@"