#!/usr/bin/env bash

# create-emailintelligence-spec.sh
# Enhanced EmailIntelligence testing framework specifications with Constitutional Framework Integration
# This tool provides guided specification creation with AI-powered template generation and constitutional compliance
#
# Usage: ./create-emailintelligence-spec.sh [OPTIONS]
#
# OPTIONS:
#   --interactive          Interactive mode with guided prompts (default)
#   --pr-number <num>      Use specific PR number for GitHub data collection
#   --baseline             Create specification for baseline testing phase
#   --improved             Create specification for improved testing phase
#   --template            Show only the specification template
#   --guided              Enable guided prompt system with AI assistance
#   --constitutional       Include constitutional compliance validation
#   --parallel             Enable parallel execution planning
#   --collect-github      Collect GitHub PR context and metadata
#   --analyze-branches    Perform comprehensive branch analysis
#   --prepare-testing     Prepare for testing framework integration
#   --help, -h            Show help message

set -e

# Parse command line arguments
INTERACTIVE_MODE=true
PR_NUMBER=""
PHASE_TYPE=""
SHOW_TEMPLATE=false
GUIDED_MODE=false
CONSTITUTIONAL_MODE=false
PARALLEL_MODE=false
COLLECT_GITHUB=false
ANALYZE_BRANCHES=false
PREPARE_TESTING=false

for arg in "$@"; do
    case "$arg" in
        --interactive)
            INTERACTIVE_MODE=true
            ;;
        --pr-number)
            if [[ -z "${!OPTIND:-}" || "${!OPTIND:-}" == --* ]]; then
                echo "ERROR: --pr-number requires a PR number argument" >&2
                exit 1
            fi
            PR_NUMBER="${!OPTIND}"
            OPTIND=$((OPTIND + 1))
            ;;
        --baseline)
            PHASE_TYPE="baseline"
            ;;
        --improved)
            PHASE_TYPE="improved"
            ;;
        --template)
            SHOW_TEMPLATE=true
            INTERACTIVE_MODE=false
            ;;
        --guided)
            GUIDED_MODE=true
            ;;
        --constitutional)
            CONSTITUTIONAL_MODE=true
            ;;
        --parallel)
            PARALLEL_MODE=true
            ;;
        --collect-github)
            COLLECT_GITHUB=true
            ;;
        --analyze-branches)
            ANALYZE_BRANCHES=true
            ;;
        --prepare-testing)
            PREPARE_TESTING=true
            ;;
        --help|-h)
            cat << 'EOF'
Usage: create-emailintelligence-spec.sh [OPTIONS]

Enhanced EmailIntelligence specification creation with Constitutional Framework Integration

OPTIONS:
  --interactive          Interactive mode with guided prompts (default)
  --pr-number <num>      Use specific PR number for GitHub data collection
  --baseline             Create specification for baseline testing phase
  --improved             Create specification for improved testing phase
  --template            Show only the specification template
  --guided              Enable guided prompt system with AI assistance
  --constitutional       Include constitutional compliance validation
  --parallel             Enable parallel execution planning
  --collect-github      Collect GitHub PR context and metadata
  --analyze-branches    Perform comprehensive branch analysis
  --prepare-testing     Prepare for testing framework integration
  --help, -h            Show this help message

ENHANCED FEATURES:
  🧠 Guided AI-powered prompt system
  ⚖️ Constitutional compliance validation
  🚀 Parallel execution planning
  📊 Quality scoring and recommendations
  🔧 Template generation for various conflict types

EXAMPLES:
  # Guided specification creation with constitutional validation
  ./create-emailintelligence-spec.sh --guided --constitutional
  
  # Create specification for specific PR with parallel planning
  ./create-emailintelligence-spec.sh --pr-number 123 --baseline --parallel
  
  # Enhanced improved phase specification
  ./create-emailintelligence-spec.sh --improved --guided --constitutional
  
  # Show complete template
  ./create-emailintelligence-spec.sh --template

CONSTITUTIONAL FRAMEWORK INTEGRATION:
  This tool integrates with EmailIntelligence Constitutional Framework:
  - Real-time compliance validation during specification creation
  - Constitutional scoring and quality assessment
  - Automated quality gates and compliance checking
  - Template generation with constitutional rule integration

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

# Get repository and environment information
eval $(get_feature_paths)

# Check GitHub configuration
check_github_config() {
    if [[ -z "${GITHUB_TOKEN:-}" ]]; then
        echo "❌ ERROR: GITHUB_TOKEN not set. Please configure your GitHub token."
        echo "   export GITHUB_TOKEN='ghp_your_token_here'"
        return 1
    fi
    
    if [[ -z "${GITHUB_REPO:-}" ]]; then
        echo "❌ ERROR: GITHUB_REPO not set. Please configure your repository."
        echo "   export GITHUB_REPO='owner/repository-name'"
        return 1
    fi
    
    echo "✅ GitHub configuration validated"
    return 0
}

# Collect GitHub PR context and metadata
collect_github_context() {
    local pr_number="$1"
    
    if [[ -z "$pr_number" ]]; then
        echo "❌ PR number required for GitHub context collection"
        return 1
    fi
    
    echo "🔍 Collecting GitHub PR context for PR #$pr_number..."
    
    # Collect basic PR information
    local pr_data=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                        "https://api.github.com/repos/$GITHUB_REPO/pulls/$pr_number")
    
    if echo "$pr_data" | jq -e '.message' > /dev/null 2>&1; then
        echo "❌ ERROR: PR #$pr_number not found or inaccessible"
        return 1
    fi
    
    # Extract key information
    local title=$(echo "$pr_data" | jq -r '.title')
    local author=$(echo "$pr_data" | jq -r '.user.login')
    local state=$(echo "$pr_data" | jq -r '.state')
    local mergeable=$(echo "$pr_data" | jq -r '.mergeable')
    local created_at=$(echo "$pr_data" | jq -r '.created_at')
    local updated_at=$(echo "$pr_data" | jq -r '.updated_at')
    local additions=$(echo "$pr_data" | jq -r '.additions')
    local deletions=$(echo "$pr_data" | jq -r '.deletions')
    local changed_files=$(echo "$pr_data" | jq -r '.changed_files')
    local head_sha=$(echo "$pr_data" | jq -r '.head.sha')
    local base_sha=$(echo "$pr_data" | jq -r '.base.sha')
    local head_branch=$(echo "$pr_data" | jq -r '.head.ref')
    local base_branch=$(echo "$pr_data" | jq -r '.base.ref')
    
    # Calculate PR age
    local pr_age_days=$(($(date -d "$updated_at" +%s) - $(date -d "$created_at" +%s)) / 86400)
    
    # Collect review status
    local reviews_data=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                             "https://api.github.com/repos/$GITHUB_REPO/pulls/$pr_number/reviews")
    local approved_reviews=$(echo "$reviews_data" | jq '[.[] | select(.state == "APPROVED")] | length')
    local changes_requested=$(echo "$reviews_data" | jq '[.[] | select(.state == "CHANGES_REQUESTED")] | length')
    local commented_reviews=$(echo "$reviews_data" | jq '[.[] | select(.state == "COMMENTED")] | length')
    
    # Collect CI/CD status if available
    local checks_data=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                            "https://api.github.com/repos/$GITHUB_REPO/commits/$head_sha/check-runs")
    local check_runs=$(echo "$checks_data" | jq '.total_count')
    local successful_checks=$(echo "$checks_data" | jq '[.check_runs[] | select(.conclusion == "success")] | length')
    local failed_checks=$(echo "$checks_data" | jq '[.check_runs[] | select(.conclusion == "failure")] | length')
    local pending_checks=$(echo "$checks_data" | jq '[.check_runs[] | select(.conclusion == null)] | length')
    
    # Output collected data
    cat << EOF
## GitHub PR Context Analysis

### Basic PR Information
- **PR Number**: #$pr_number
- **Title**: $title
- **Author**: $author
- **State**: $state
- **Created**: $created_at
- **Last Updated**: $updated_at
- **Age**: ${pr_age_days} days
- **Mergeable**: $mergeable

### Branch Analysis
- **Source Branch**: $head_branch ($head_sha)
- **Target Branch**: $base_branch ($base_sha)
- **Source Repository**: $(echo "$pr_data" | jq -r '.head.repo.full_name // "same-repo"')

### Change Metrics
- **Files Changed**: $changed_files
- **Lines Added**: $additionals
- **Lines Deleted**: $deletions
- **Net Changes**: $((additions - deletions))

### Review Status
- **Approved Reviews**: $approved_reviews
- **Changes Requested**: $changes_requested
- **Comments**: $commented_reviews
- **Total Reviews**: $(echo "$reviews_data" | jq '. | length')

### CI/CD Status
- **Total Check Runs**: $check_runs
- **Successful Checks**: $successful_checks
- **Failed Checks**: $failed_checks
- **Pending Checks**: $pending_checks
- **CI/CD Success Rate**: $(( check_runs > 0 ? successful_checks * 100 / check_runs : 0 ))%

### Complexity Assessment
- **Change Volume**: $((changed_files > 20 ? "High" : changed_files > 5 ? "Medium" : "Low"))
- **Staleness Risk**: $((pr_age_days > 7 ? "High" : pr_age_days > 3 ? "Medium" : "Low"))
- **Merge Readiness**: $((mergeable == "true" && failed_checks == 0 ? "Ready" : "Not Ready"))
EOF
    
    # Return extracted data for further processing
    echo "$pr_data" > "/tmp/pr-${pr_number}-data.json"
    return 0
}

# Analyze branch conflicts and characteristics
analyze_branch_conflicts() {
    local source_branch="$1"
    local target_branch="$2"
    
    echo "🌿 Analyzing branch conflicts between '$source_branch' and '$target_branch'..."
    
    # Get merge base
    local merge_base=$(git merge-base "$source_branch" "$target_branch" 2>/dev/null || echo "unknown")
    
    # Analyze files that differ
    local conflict_files=$(git diff --name-only "$merge_base" "$source_branch" "$target_branch" 2>/dev/null | wc -l)
    local total_diffs=$(git diff --stat "$merge_base" "$source_branch" "$target_branch" 2>/dev/null | tail -1)
    
    # Check for actual conflicts
    local actual_conflicts=0
    if git merge-tree $(git merge-tree $(git mktree < <(git ls-tree "$merge_base" | sed 's/^/100644 /')) \
                                       $(git mktree < <(git ls-tree "$source_branch" | sed 's/^/100644 /')) \
                                       $(git mktree < <(git ls-tree "$target_branch" | sed 's/^/100644 /')) 2>/dev/null | \
        grep -c "^<<<<<<<" || echo "0") > /dev/null 2>&1; then
        actual_conflicts=1
    fi
    
    # Analyze file types
    local code_files=$(git diff --name-only "$merge_base" "$source_branch" "$target_branch" 2>/dev/null | \
                      grep -E '\.(js|ts|py|java|go|rs|cpp|c|h)$' | wc -l)
    local config_files=$(git diff --name-only "$merge_base" "$source_branch" "$target_branch" 2>/dev/null | \
                        grep -E '\.(json|yaml|yml|toml|ini|conf)$' | wc -l)
    local doc_files=$(git diff --name-only "$merge_base" "$source_branch" "$target_branch" 2>/dev/null | \
                     grep -E '\.(md|txt|rst)$' | wc -l)
    
    # Determine conflict complexity
    local complexity="Low"
    if [[ $conflict_files -gt 50 || $code_files -gt 20 ]]; then
        complexity="Critical"
    elif [[ $conflict_files -gt 20 || $code_files -gt 10 ]]; then
        complexity="High"
    elif [[ $conflict_files -gt 5 || $code_files -gt 3 ]]; then
        complexity="Medium"
    fi
    
    # Analysis output
    cat << EOF

## Branch Conflict Analysis

### Merge Characteristics
- **Merge Base**: $merge_base
- **Files with Differences**: $conflict_files
- **Actual Merge Conflicts**: $actual_conflicts
- **Overall Complexity**: $complexity

### File Type Distribution
- **Code Files**: $code_files
- **Configuration Files**: $config_files  
- **Documentation Files**: $doc_files
- **Other Files**: $((conflict_files - code_files - config_files - doc_files))

### Resolution Strategy Recommendation
EOF
    
    # Provide recommendations based on analysis
    if [[ $actual_conflicts -eq 0 ]]; then
        echo "✅ **No conflicts detected** - Clean merge possible"
        echo "- **Recommended Strategy**: Fast-forward merge or simple merge"
        echo "- **Risk Level**: Low"
        echo "- **Testing Required**: Standard validation only"
    elif [[ $complexity == "Low" ]]; then
        echo "🔧 **Simple conflicts** - Manual resolution required"
        echo "- **Recommended Strategy**: Conservative merge with manual conflict resolution"
        echo "- **Risk Level**: Low-Medium"
        echo "- **Testing Required**: Enhanced validation"
    elif [[ $complexity == "Medium" ]]; then
        echo "⚠️ **Moderate conflicts** - Strategic resolution needed"
        echo "- **Recommended Strategy**: Feature preservation with worktree isolation"
        echo "- **Risk Level**: Medium"
        echo "- **Testing Required**: Comprehensive validation"
    else
        echo "🚨 **Complex conflicts** - Advanced resolution required"
        echo "- **Recommended Strategy**: Refactoring merge with EmailIntelligence enhancement"
        echo "- **Risk Level**: High"
        echo "- **Testing Required**: Full testing framework validation"
    fi
    
    echo
}

# Create comprehensive specification template
create_comprehensive_template() {
    local pr_number="${1:-[PR_NUMBER]}"
    local phase_type="${2:-baseline}"
    
    cat << EOF
# EmailIntelligence Testing Framework Specification

*Generated: $(date)*
*Phase Type: ${phase_type}*
*PR Number: #${pr_number}*

## Executive Summary

This specification defines the testing approach for PR #${pr_number} using the EmailIntelligence Testing Framework ${phase_type} phase methodology.

### Testing Framework Integration
- **Phase**: ${phase_type} (Baseline vs Improved comparison)
- **GitHub Integration**: Full API context and CI/CD status collection
- **Branch Analysis**: Comprehensive conflict detection and resolution strategy
- **Statistical Validation**: Industry-standard statistical analysis for improvement measurement

## GitHub PR Context Analysis

### Basic Information
- **PR Number**: #${pr_number}
- **Title**: [To be filled from GitHub API]
- **Author**: [To be collected from GitHub]
- **Source Branch**: [From GitHub API]
- **Target Branch**: [From GitHub API]
- **Creation Date**: [From GitHub API]
- **Last Update**: [From GitHub API]
- **PR Age**: [Calculated from dates]

### Change Metrics (GitHub API)
- **Files Changed**: [From GitHub API]
- **Lines Added**: [From GitHub API]
- **Lines Deleted**: [From GitHub API]
- **Net Change Impact**: [Calculated]
- **Change Complexity**: [Derived from metrics]

### Review Status Analysis
- **Approved Reviews**: [From GitHub API]
- **Changes Requested**: [From GitHub API]
- **Comments**: [From GitHub API]
- **Review Saturation**: [Calculated]
- **Merge Readiness**: [From GitHub mergeable status]

### CI/CD Integration Status
- **Total Check Runs**: [From GitHub Checks API]
- **Successful Checks**: [From GitHub Checks API]
- **Failed Checks**: [From GitHub Checks API]
- **Pending Checks**: [From GitHub Checks API]
- **CI/CD Success Rate**: [Calculated percentage]
- **Pipeline Health**: [Derived from check results]

## Branch Analysis and Conflict Assessment

### Merge Characteristics
- **Merge Base**: [From git analysis]
- **Files with Differences**: [From git diff analysis]
- **Actual Merge Conflicts**: [From conflict detection]
- **Conflict Complexity**: [Simple/Medium/High/Critical]
- **Resolution Complexity**: [Assessment based on analysis]

### File Type Impact Analysis
- **Code Files**: [Count and impact assessment]
- **Configuration Files**: [Change impact]
- **Documentation Files**: [Update requirements]
- **Test Files**: [Coverage implications]
- **Build/Deploy Files**: [CI/CD impact]

### Architecture Impact Assessment
- **Breaking Changes**: [Risk assessment]
- **API Changes**: [Compatibility impact]
- **Database Changes**: [Migration requirements]
- **Infrastructure Changes**: [Deployment impact]

## 6-Dimensional Scoring Framework

### Dimension 1: Conflict Complexity Assessment (0.0-4.0)
- **File Complexity Score**: [1.0 = Simple, 2.0 = Moderate, 3.0 = Complex, 4.0 = Critical]
- **Change Type Complexity**: [Semantic vs syntactic changes]
- **Dependency Impact**: [Cascading effect assessment]
- **Overall Complexity**: [Weighted average]

### Dimension 2: Resolution Effectiveness Measurement (0.0-1.0)
- **Feature Preservation Rate**: [Target >95%]
- **Regression Count**: [Target <2 per PR]
- **Resolution Time**: [Target <4 hours]
- **Manual Intervention Rate**: [Target <20%]

### Dimension 3: Quality Assurance Validation (0.0-1.0)
- **Code Quality Metrics**: [Linting, complexity, maintainability]
- **Performance Impact**: [Benchmark vs baseline]
- **Security Compliance**: [Vulnerability assessment]
- **Documentation Quality**: [Update completeness]

### Dimension 4: User Experience Assessment (0.0-1.0)
- **Workflow Clarity**: [Developer experience rating]
- **Error Recovery**: [Rollback effectiveness]
- **Tool Integration**: [Development workflow integration]
- **Learning Curve**: [Adoption difficulty assessment]

### Dimension 5: GitHub PR Context Assessment (0.0-1.0)
- **Mergeability Score**: [Based on GitHub API mergeable status]
- **Review Status Score**: [Review completion and quality]
- **Context Issues Score**: [Staleness, outdated PRs]
- **CI/CD Integration Score**: [Status check and pipeline health]

### Dimension 6: CI/CD Integration Assessment (0.0-1.0)
- **Workflow Success Rate**: [Percentage of successful CI/CD workflows]
- **Merge Readiness Score**: [CI/CD gates satisfaction]
- **Test Coverage Score**: [Automated testing coverage]
- **Pipeline Reliability Score**: [Consistency and failure patterns]

## Testing Phase Configuration

### ${phase_type} Phase Specifics
EOF
    
    if [[ "$phase_type" == "baseline" ]]; then
        cat << EOF
#### Baseline Testing Characteristics
- **Methodology**: Current manual/resolution approach
- **Tool Version**: Pre-EmailIntelligence enhancement
- **Comparison Baseline**: Industry standard manual processes
- **Success Metrics**: Current baseline performance levels
- **Data Collection**: Establish current state metrics
- **Validation Focus**: Accurate baseline measurement for comparison

#### Baseline Testing Protocol
1. **Pre-Resolution Analysis**: Current conflict detection and analysis
2. **Manual Resolution**: Existing team resolution methodology
3. **Quality Validation**: Current testing and validation approaches
4. **Performance Measurement**: Current resolution time and effectiveness
5. **Data Collection**: Comprehensive metrics for improvement comparison

#### Baseline Success Criteria
- **Resolution Time**: Current average resolution time documented
- **Quality Rate**: Current bug rate and regression percentage
- **User Satisfaction**: Current developer experience ratings
- **Resource Usage**: Current time and effort requirements
EOF
    else
        cat << EOF
#### Improved Testing Characteristics
- **Methodology**: EmailIntelligence enhanced resolution approach
- **Tool Version**: EmailIntelligence v2.0+ with all enhancements
- **Improvement Target**: >30% efficiency improvement over baseline
- **Success Metrics**: Measurable improvement in all 6 dimensions
- **Data Collection**: Enhanced metrics for statistical validation
- **Validation Focus**: Quantified improvement measurement

#### Improved Testing Protocol
1. **Enhanced Analysis**: EmailIntelligence automated conflict detection
2. **AI-Assisted Resolution**: Worktree-based isolation and constitutional analysis
3. **Constitutional Validation**: Automated compliance checking
4. **Performance Optimization**: Caching and API optimization benefits
5. **Statistical Validation**: Advanced statistical analysis and significance testing

#### Improved Success Criteria
- **Resolution Time**: >30% reduction from baseline measurement
- **Quality Rate**: >95% feature preservation, <1% regression rate
- **User Satisfaction**: >4.5/5 developer experience rating
- **Statistical Significance**: p<0.05 for improvement measurements
EOF
    fi
    
    cat << EOF

## Implementation Strategy

### Worktree-Based Resolution Approach
1. **Isolated Environment Setup**
   - Create dedicated worktree for conflict analysis
   - Configure clean testing environment
   - Establish rollback mechanisms

2. **Constitutional Framework Application**
   - Load organizational constitution requirements
   - Validate resolution against constitutional principles
   - Document compliance violations and mitigations

3. **Enhanced Resolution Execution**
   - Apply EmailIntelligence resolution algorithms
   - Preserve features from both branches intelligently
   - Minimize regression risk through careful integration

4. **Comprehensive Validation**
   - Run enhanced test suite with coverage analysis
   - Validate constitutional compliance
   - Measure performance impact and user experience

### Data Collection and Analysis

#### Metrics Collection Points
- **Resolution Time**: Start to completion timestamp tracking
- **Quality Metrics**: Bug detection, regression tracking, feature preservation
- **User Experience**: Developer workflow satisfaction and efficiency
- **GitHub Context**: Automated PR metadata and status collection
- **CI/CD Status**: Real-time pipeline status and success rate monitoring

#### Statistical Analysis Preparation
- **Sample Size**: 5 PRs per phase for statistical validity
- **Comparison Method**: Paired t-test for before/after comparison
- **Effect Size**: Cohen's d for practical significance measurement
- **Confidence Intervals**: 95% CI for all improvement metrics
- **Power Analysis**: Ensure adequate statistical power (>80%)

## Risk Assessment and Mitigation

### High-Risk Factors
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|---------|-------------------|
| **GitHub API Rate Limiting** | Medium | High | Implement caching and exponential backoff |
| **Complex Conflict Scenarios** | Medium | High | Enhanced resolution algorithms and rollback |
| **CI/CD Integration Failures** | Low | Medium | Multi-system fallback and graceful degradation |
| **Statistical Insignificance** | Medium | Medium | Adequate sample size and power analysis |

### Quality Assurance Gates
- **Pre-Resolution**: Constitutional validation and risk assessment
- **During Resolution**: Real-time monitoring and checkpoint validation
- **Post-Resolution**: Comprehensive testing and statistical analysis
- **Final Validation**: Success criteria verification and documentation

## Success Metrics and Validation

### Primary Success Metrics
- **Efficiency Improvement**: >30% reduction in resolution time
- **Quality Enhancement**: >95% feature preservation rate
- **Statistical Validity**: p<0.05 significance with >95% confidence
- **User Experience**: >4.5/5 satisfaction rating
- **Performance**: <15 minutes average resolution time
- **Automation**: >75% reduction in manual intervention

### Validation Protocol
1. **Data Collection**: Automated metrics collection during resolution
2. **Statistical Analysis**: Industry-standard significance testing
3. **Comparative Analysis**: Baseline vs. improved phase comparison
4. **Quality Assurance**: Multi-dimensional validation criteria
5. **Stakeholder Review**: Executive and technical validation

## Integration with Testing Framework

### GitHub Actions Integration
- **Automatic Triggers**: PR opened, synchronized, updated events
- **Context Collection**: Automated GitHub API data gathering
- **CI/CD Monitoring**: Real-time status check collection
- **Result Reporting**: Automated statistical analysis and reporting

### EmailIntelligence CLI Integration
- **Worktree Management**: Automated isolated environment creation
- **Constitutional Analysis**: Automated compliance checking
- **Enhanced Resolution**: AI-assisted conflict resolution
- **Performance Monitoring**: Real-time metrics collection

### Continuous Monitoring
- **Performance Benchmarking**: Industry-standard performance tracking
- **Quality Metrics**: Comprehensive quality assessment automation
- **User Feedback**: Automated satisfaction and usability tracking
- **Optimization Opportunities**: Data-driven improvement identification

## Next Steps and Action Items

### Immediate Actions (Day 1-2)
- [ ] GitHub API configuration and token validation
- [ ] Branch analysis and conflict detection completion
- [ ] Testing environment setup and validation
- [ ] Baseline measurement collection initiation

### Short-term Actions (Week 1)
- [ ] Complete ${phase_type} phase testing execution
- [ ] Collect comprehensive metrics for all 6 dimensions
- [ ] Perform initial statistical analysis
- [ ] Document lessons learned and optimization opportunities

### Medium-term Actions (Weeks 2-4)
- [ ] Complete comparative analysis between phases
- [ ] Validate statistical significance of improvements
- [ ] Generate executive summary and recommendations
- [ ] Plan optimization and enhancement roadmap

---

## Appendices

### A. Technical Implementation Details
- GitHub API integration specifications
- Statistical analysis methodology
- Performance benchmarking protocols

### B. Constitutional Framework
- Organizational principles and requirements
- Compliance checking algorithms
- Exception handling and documentation

### C. Quality Assurance Protocols
- Testing methodology and validation criteria
- Regression detection and prevention
- Performance impact assessment

---
*Generated by create-emailintelligence-spec.sh on $(date)*
*Framework Version: EmailIntelligence v2.0*
*Phase: ${phase_type}*
EOF
}

# Enhanced interactive specification creation with guided prompts
run_enhanced_interactive_specification() {
    echo "🚀 EmailIntelligence Enhanced Specification Creator"
    echo "==================================================="
    echo "Constitutional Framework Integration • AI-Powered Guidance • Quality Scoring"
    echo
    
    # Display enhanced capabilities
    echo "✨ Enhanced Capabilities:"
    echo "- 🧠 AI-powered guided prompt system"
    echo "- ⚖️ Constitutional compliance validation"
    echo "- 📊 Quality scoring and recommendations"
    echo "- 🚀 Parallel execution planning"
    echo "- 🔧 Template generation for various conflict types"
    echo
    
    # Feature configuration
    echo "⚙️ Feature Configuration"
    echo "========================"
    
    # Phase selection
    echo "📊 Testing Phase Configuration"
    echo "=============================="
    if [[ -z "$PHASE_TYPE" ]]; then
        echo "Select testing phase:"
        echo "1) Baseline Phase - Current methodology measurement"
        echo "2) Improved Phase - EmailIntelligence enhancement testing"
        read -p "Enter choice (1-2) [Default: 1]: " PHASE_CHOICE
        
        case "$PHASE_CHOICE" in
            2) PHASE_TYPE="improved" ;;
            1|"") PHASE_TYPE="baseline" ;;
            *) echo "Invalid choice. Defaulting to baseline."; PHASE_TYPE="baseline" ;;
        esac
    fi
    
    echo "Selected Phase: $PHASE_TYPE"
    echo
    
    # Enhanced feature selection
    echo "🎯 Enhanced Features"
    echo "==================="
    
    # Guided mode
    if [[ -z "$GUIDED_MODE" ]]; then
        read -p "Enable AI-guided prompt system? (Y/n) [Default: Y]: " ENABLE_GUIDED
        if [[ "$ENABLE_GUIDED" =~ ^[Nn]$ ]]; then
            GUIDED_MODE=false
        else
            GUIDED_MODE=true
        fi
    fi
    
    # Constitutional validation
    if [[ -z "$CONSTITUTIONAL_MODE" ]]; then
        read -p "Enable constitutional compliance validation? (Y/n) [Default: Y]: " ENABLE_CONST
        if [[ "$ENABLE_CONST" =~ ^[Nn]$ ]]; then
            CONSTITUTIONAL_MODE=false
        else
            CONSTITUTIONAL_MODE=true
        fi
    fi
    
    # Parallel execution
    if [[ -z "$PARALLEL_MODE" ]]; then
        read -p "Enable parallel execution planning? (Y/n) [Default: Y]: " ENABLE_PARALLEL
        if [[ "$ENABLE_PARALLEL" =~ ^[Nn]$ ]]; then
            PARALLEL_MODE=false
        else
            PARALLEL_MODE=true
        fi
    fi
    
    echo "Enabled Features:"
    echo "- Guided Mode: $( [[ "$GUIDED_MODE" == true ]] && echo "✅" || echo "❌" )"
    echo "- Constitutional Validation: $( [[ "$CONSTITUTIONAL_MODE" == true ]] && echo "✅" || echo "❌" )"
    echo "- Parallel Planning: $( [[ "$PARALLEL_MODE" == true ]] && echo "✅" || echo "❌" )"
    echo
    
    # Conflict information collection
    echo "🔍 Conflict Information Collection"
    echo "=================================="
    
    if [[ -n "$PR_NUMBER" ]]; then
        echo "Using PR #$PR_NUMBER for context"
        COLLECT_GITHUB=true
        ANALYZE_BRANCHES=true
    else
        read -p "PR Number for analysis (leave empty for manual input): " PR_INPUT
        
        if [[ -n "$PR_INPUT" ]]; then
            PR_NUMBER="$PR_INPUT"
            COLLECT_GITHUB=true
            ANALYZE_BRANCHES=true
            
            # GitHub integration
            echo
            echo "🔧 GitHub Integration Setup"
            echo "==========================="
            if ! check_github_config; then
                echo "⚠️ GitHub configuration not available. Continuing with manual input."
            else
                echo "✅ GitHub integration available"
                echo "Collecting GitHub context for PR #$PR_NUMBER..."
                if ! collect_github_context "$PR_NUMBER"; then
                    echo "❌ Failed to collect GitHub context. Continuing with available information."
                fi
            fi
        else
            # Manual conflict input
            echo
            echo "📝 Manual Conflict Information"
            echo "==============================="
            read -p "Source branch: " SOURCE_BRANCH
            read -p "Target branch: " TARGET_BRANCH
            read -p "Conflict description: " CONFLICT_DESC
            read -p "Affected files (comma-separated): " AFFECTED_FILES
            
            # Convert to structured data for template generator
            export CONFLICT_METADATA='{
                "source_branch": "'$SOURCE_BRANCH'",
                "target_branch": "'$TARGET_BRANCH'",
                "description": "'$CONFLICT_DESC'",
                "affected_files": "'$AFFECTED_FILES'"
            }'
            
            echo "✅ Conflict information collected"
        fi
    fi
    
    # Testing framework preparation
    echo
    echo "🎯 Testing Framework Integration"
    echo "================================"
    read -p "Enable 6-dimensional scoring framework? (Y/n) [Default: Y]: " ENABLE_SCORING
    if [[ ! "$ENABLE_SCORING" =~ ^[Nn]$ ]]; then
        PREPARE_TESTING=true
        echo "✅ 6-dimensional scoring framework enabled"
    fi
    
    read -p "Prepare for statistical comparison analysis? (Y/n) [Default: Y]: " ENABLE_STATS
    if [[ ! "$ENABLE_STATS" =~ ^[Nn]$ ]]; then
        echo "✅ Statistical analysis preparation enabled"
    fi
    
    # Python integration for enhanced template generation
    echo
    echo "🤖 Python Template Generation Integration"
    echo "=========================================="
    echo "Generating enhanced specification template with constitutional compliance..."
    
    if command -v python3 >/dev/null 2>&1; then
        # Try to use Python template generator
        PYTHON_SCRIPT="
import sys
sys.path.append('$SCRIPT_DIR/../src')

from specification.template_generator import (
    SpecificationTemplateGenerator, ConflictType, SpecificationPhase,
    ConflictMetadata, TemplateGenerationContext
)

import json
from datetime import datetime

# Create conflict metadata
conflict_metadata = ConflictMetadata(
    conflict_type=ConflictType.CONTENT,
    file_paths=['$AFFECTED_FILES'.split(',') if '$AFFECTED_FILES' else []],
    pr_numbers=['$PR_NUMBER'] if '$PR_NUMBER' else [],
    branches=['$SOURCE_BRANCH', '$TARGET_BRANCH'] if '$SOURCE_BRANCH' and '$TARGET_BRANCH' else [],
    complexity_score=5.0,  # Default complexity
    affected_components=['Code Resolution'],  # Default
    estimated_resolution_time=30,  # Default 30 minutes
    risk_level='MEDIUM',
    stakeholder_impact='moderate'
)

# Create project context
project_context = {
    'organization': {'name': 'EmailIntelligence Team'},
    'technology_stack': {'language': 'Python', 'framework': 'FastAPI'},
    'deployment_environment': {'type': 'Development'},
    'testing_phase': '$PHASE_TYPE'
}

# Create team context
team_context = {
    'roles': ['Developer', 'Technical Lead', 'QA Engineer'],
    'skills': ['Git', 'Constitutional Framework', 'Quality Assurance'],
    'experience_level': 'Medium'
}

# Select specification phase
spec_phase = SpecificationPhase.BASELINE if '$PHASE_TYPE' == 'baseline' else SpecificationPhase.IMPROVED

# Create template generation context
template_context = TemplateGenerationContext(
    conflict_metadata=conflict_metadata,
    project_context=project_context,
    team_context=team_context,
    constitutional_requirements={'enabled': '$CONSTITUTIONAL_MODE' == 'true'},
    specification_phase=spec_phase,
    template_options={
        'guided_mode': '$GUIDED_MODE' == 'true',
        'parallel_planning': '$PARALLEL_MODE' == 'true',
        'quality_scoring': True
    }
)

# Generate template
generator = SpecificationTemplateGenerator()
try:
    result = generator.generate_specification_template(conflict_metadata, project_context, team_context, spec_phase)
    print(json.dumps(result, indent=2, default=str))
except Exception as e:
    print(f'Error: {str(e)}', file=sys.stderr)
    sys.exit(1)
"
        
        echo "$PYTHON_SCRIPT" > /tmp/generate_template.py
        
        if python3 /tmp/generate_template.py > /tmp/spec_template.json 2>/tmp/spec_errors.log; then
            echo "✅ Enhanced template generated successfully"
            
            # Display template summary
            echo
            echo "📋 Template Summary"
            echo "==================="
            python3 -c "
import json
with open('/tmp/spec_template.json', 'r') as f:
    data = json.load(f)
    
print(f'Template Type: {data.get(\"template_metadata\", {}).get(\"template_type\", \"Unknown\")}')
print(f'Quality Score: {data.get(\"template_metadata\", {}).get(\"quality_score\", \"N/A\")}')
print(f'Constitutional Compliance: {data.get(\"constitutional_validation\", {}).get(\"overall_score\", \"N/A\")}')
print(f'Completeness: {len(data.get(\"template_content\", {}))} sections generated')
"
            
            # Save template
            TEMPLATE_DIR="specs/$(date +%Y%m%d_%H%M%S)_$PHASE_TYPE"
            mkdir -p "$TEMPLATE_DIR"
            cp /tmp/spec_template.json "$TEMPLATE_DIR/enhanced_specification.json"
            
            echo "✅ Template saved to: $TEMPLATE_DIR"
        else
            echo "❌ Python template generation failed. Using fallback template."
            cat /tmp/spec_errors.log >&2
        fi
        
        rm -f /tmp/generate_template.py /tmp/spec_template.json /tmp/spec_errors.log
    else
        echo "❌ Python3 not available. Using bash template generation."
    fi
    
    # Generate comprehensive specification
    echo
    echo "📝 Generating Comprehensive Specification..."
    echo "==========================================="
    
    create_comprehensive_template "$PR_NUMBER" "$PHASE_TYPE"
    
    echo
    echo "🎉 Enhanced Specification Generated Successfully!"
    echo "=================================================="
    echo
    echo "Next Steps:"
    echo "1. Review the enhanced specification with constitutional compliance"
    echo "2. Use with EmailIntelligence CLI for guided execution:"
    if [[ -n "$PR_NUMBER" ]]; then
        echo "   python emailintelligence_cli.py setup-resolution --pr $PR_NUMBER --phase $PHASE_TYPE"
    else
        echo "   python emailintelligence_cli.py setup-resolution --source-branch $SOURCE_BRANCH --target-branch $TARGET_BRANCH --phase $PHASE_TYPE"
    fi
    echo "3. Execute testing framework with comprehensive validation"
    echo "4. Collect metrics for statistical analysis and improvement measurement"
    echo
    echo "🆕 Enhanced Features Used:"
    echo "- Constitutional compliance validation"
    echo "- AI-powered guided prompts"
    echo "- Quality scoring and recommendations"
    echo "- Parallel execution planning"
    echo "- Template generation for various conflict types"
}

# Original interactive mode for backward compatibility
run_interactive_specification() {
    run_enhanced_interactive_specification
}

# Main execution logic
main() {
    if $SHOW_TEMPLATE; then
        create_comprehensive_template "$PR_NUMBER" "${PHASE_TYPE:-baseline}"
        exit 0
    fi
    
    if $INTERACTIVE_MODE; then
        run_interactive_specification
    else
        create_comprehensive_template "$PR_NUMBER" "${PHASE_TYPE:-baseline}"
    fi
}

# Execute main function
main "$@"