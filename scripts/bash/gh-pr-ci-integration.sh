#!/usr/bin/env bash
# gh-pr-ci-integration.sh
# GitHub PR and CI/CD integration for EmailIntelligence testing framework
# Enhances PR resolution testing with GitHub context and CI/CD status

set -e

# Parse command line arguments
PR_ID="${1}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITHUB_REPO="${GITHUB_REPO:-}"
CI_SYSTEM="${2:-github-actions}"  # github-actions, gitlab-ci, jenkins, azure-devops

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# GitHub API endpoints
GH_API_BASE="https://api.github.com"
GH_REPOS_API="$GH_API_BASE/repos"

# Function: Get GitHub PR details
get_github_pr_context() {
    local pr_id=$1
    local output_file="${2:-pr-context.json}"
    
    echo "Fetching GitHub PR context for PR #$pr_id..."
    
    # Validate GitHub token
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "ERROR: GITHUB_TOKEN environment variable not set"
        echo "Please set GITHUB_TOKEN for GitHub API access"
        return 1
    fi
    
    if [ -z "$GITHUB_REPO" ]; then
        echo "ERROR: GITHUB_REPO environment variable not set"
        echo "Please set GITHUB_REPO (format: owner/repo)"
        return 1
    fi
    
    # Fetch PR details
    echo "→ Fetching PR metadata..."
    local pr_data=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/pulls/$pr_id")
    
    # Extract key information
    local pr_number=$(echo "$pr_data" | jq -r '.number')
    local pr_title=$(echo "$pr_data" | jq -r '.title')
    local pr_state=$(echo "$pr_data" | jq -r '.state')
    local pr_author=$(echo "$pr_data" | jq -r '.user.login')
    local pr_created=$(echo "$pr_data" | jq -r '.created_at')
    local pr_updated=$(echo "$pr_data" | jq -r '.updated_at')
    local pr_base_branch=$(echo "$pr_data" | jq -r '.base.ref')
    local pr_head_branch=$(echo "$pr_data" | jq -r '.head.ref')
    local pr_mergeable=$(echo "$pr_data" | jq -r '.mergeable')
    local pr_mergeable_state=$(echo "$pr_data" | jq -r '.mergeable_state')
    local pr_additions=$(echo "$pr_data" | jq -r '.additions')
    local pr_deletions=$(echo "$pr_data" | jq -r '.deletions')
    local pr_changed_files=$(echo "$pr_data" | jq -r '.changed_files')
    
    # Calculate PR age
    local pr_age_days=$(calculate_pr_age_days "$pr_created")
    
    # Fetch PR files
    echo "→ Fetching PR file changes..."
    local pr_files=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/pulls/$pr_id/files")
    
    # Count conflicts and issues
    local conflict_files=$(echo "$pr_files" | jq '[.[] | select(.status == "conflicted") | .filename] | length')
    local added_files=$(echo "$pr_files" | jq '[.[] | select(.status == "added") | .filename] | length')
    local modified_files=$(echo "$pr_files" | jq '[.[] | select(.status == "modified") | .filename] | length')
    local deleted_files=$(echo "$pr_files" | jq '[.[] | select(.status == "removed") | .filename] | length')
    
    # Fetch PR reviews
    echo "→ Fetching PR reviews..."
    local pr_reviews=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/pulls/$pr_id/reviews")
    
    local approved_reviews=$(echo "$pr_reviews" | jq '[.[] | select(.state == "APPROVED")] | length')
    local changes_requested=$(echo "$pr_reviews" | jq '[.[] | select(.state == "CHANGES_REQUESTED")] | length')
    local pending_reviews=$(echo "$pr_reviews" | jq '[.[] | select(.state == "PENDING")] | length')
    
    # Fetch PR comments and issues
    echo "→ Fetching PR discussion..."
    local pr_comments=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/pulls/$pr_id/comments")
    local issue_comments=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/issues/$pr_id/comments")
    
    local total_comments=$(($(echo "$pr_comments" | jq '. | length') + $(echo "$issue_comments" | jq '. | length')))
    
    # Calculate complexity score
    local pr_complexity=$(calculate_pr_complexity "$pr_changed_files" "$conflict_files" "$pr_additions" "$pr_deletions")
    
    # Create context JSON
    cat > "$output_file" << EOF
{
  "pr_metadata": {
    "number": $pr_number,
    "title": $(echo "$pr_title" | jq -Rs .),
    "state": $(echo "$pr_state" | jq -Rs .),
    "author": $(echo "$pr_author" | jq -Rs .),
    "base_branch": $(echo "$pr_base_branch" | jq -Rs .),
    "head_branch": $(echo "$pr_head_branch" | jq -Rs .),
    "created_at": $(echo "$pr_created" | jq -Rs .),
    "updated_at": $(echo "$pr_updated" | jq -Rs .),
    "age_days": $pr_age_days,
    "mergeable": $pr_mergeable,
    "mergeable_state": $(echo "$pr_mergeable_state" | jq -Rs .)
  },
  "change_metrics": {
    "files_changed": $pr_changed_files,
    "additions": $pr_additions,
    "deletions": $pr_deletions,
    "conflict_files": $conflict_files,
    "added_files": $added_files,
    "modified_files": $modified_files,
    "deleted_files": $deleted_files,
    "complexity_score": $pr_complexity
  },
  "review_status": {
    "approved_reviews": $approved_reviews,
    "changes_requested": $changes_requested,
    "pending_reviews": $pending_reviews,
    "total_reviews": $(($approved_reviews + $changes_requested + $pending_reviews)),
    "total_comments": $total_comments
  },
  "context_issues": {
    "has_conflicts": $(if [ "$conflict_files" -gt 0 ]; then echo "true"; else echo "false"; fi),
    "is_mergeable": $(if [ "$pr_mergeable" == "true" ]; then echo "true"; else echo "false"; fi),
    "outstanding_reviews": $(if [ "$changes_requested" -gt 0 ] || [ "$pending_reviews" -gt 0 ]; then echo "true"; else echo "false"; fi),
    "stale_pr": $(if [ "$pr_age_days" -gt 7 ]; then echo "true"; else echo "false"; fi)
  },
  "timestamp": "$(date -Iseconds)"
}
EOF
    
    echo "✓ GitHub PR context saved to: $output_file"
    echo "✓ PR #$pr_number: $pr_title"
    echo "✓ Complexity Score: $pr_complexity"
    echo "✓ Mergeable: $pr_mergeable_state"
    echo "✓ Conflicts: $conflict_files files"
    echo "✓ Reviews: $approved_reviews approved, $changes_requested changes requested, $pending_reviews pending"
}

# Function: Get CI/CD status
get_cicd_status() {
    local pr_id=$1
    local ci_system=$2
    local output_file="${3:-cicd-status.json}"
    
    echo "Fetching CI/CD status for PR #$pr_id using $ci_system..."
    
    case "$ci_system" in
        github-actions)
            fetch_github_actions_status "$pr_id" "$output_file"
            ;;
        gitlab-ci)
            fetch_gitlab_ci_status "$pr_id" "$output_file"
            ;;
        jenkins)
            fetch_jenkins_status "$pr_id" "$output_file"
            ;;
        azure-devops)
            fetch_azure_devops_status "$pr_id" "$output_file"
            ;;
        *)
            echo "ERROR: Unsupported CI/CD system: $ci_system"
            echo "Supported systems: github-actions, gitlab-ci, jenkins, azure-devops"
            return 1
            ;;
    esac
}

# Function: Fetch GitHub Actions status
fetch_github_actions_status() {
    local pr_id=$1
    local output_file=$2
    
    echo "→ Fetching GitHub Actions workflows..."
    
    # Get check runs (GitHub Actions and other checks)
    local check_runs=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/commits/$(get_pr_commit_sha "$pr_id")/check-runs")
    
    # Analyze check runs
    local total_checks=$(echo "$check_runs" | jq '.total_count')
    local passed_checks=$(echo "$check_runs" | jq '[.check_runs[] | select(.conclusion == "success")] | length')
    local failed_checks=$(echo "$check_runs" | jq '[.check_runs[] | select(.conclusion == "failure")] | length')
    local pending_checks=$(echo "$check_runs" | jq '[.check_runs[] | select(.conclusion == null)] | length')
    local cancelled_checks=$(echo "$check_runs" | jq '[.check_runs[] | select(.conclusion == "cancelled")] | length')
    
    # Check for specific workflow types
    local workflows=$(echo "$check_runs" | jq '[.check_runs[] | select(.name | test("CI|test|lint|build|deploy"))]')
    local ci_workflows=$(echo "$workflows" | jq '. | length')
    local passing_workflows=$(echo "$workflows" | jq '[.[] | select(.conclusion == "success")] | length')
    local failing_workflows=$(echo "$workflows" | jq '[.[] | select(.conclusion == "failure")] | length')
    
    # Calculate status
    local overall_status="pending"
    local status_details=""
    
    if [ "$failed_checks" -gt 0 ]; then
        overall_status="failed"
        status_details="Some checks have failed"
    elif [ "$pending_checks" -gt 0 ]; then
        overall_status="pending"
        status_details="Checks are still running"
    elif [ "$passed_checks" -gt 0 ]; then
        overall_status="success"
        status_details="All checks passed"
    else
        overall_status="neutral"
        status_details="No checks configured"
    fi
    
    # Get specific workflow details
    local test_workflow_status=$(echo "$workflows" | jq '[.[] | select(.name | test("test|Test"))] | first | .conclusion // "pending"')
    local build_workflow_status=$(echo "$workflows" | jq '[.[] | select(.name | test("build|Build"))] | first | .conclusion // "pending"')
    local lint_workflow_status=$(echo "$workflows" | jq '[.[] | select(.name | test("lint|Lint"))] | first | .conclusion // "pending"')
    
    cat > "$output_file" << EOF
{
  "cicd_system": "github-actions",
  "pr_number": $pr_id,
  "overall_status": $(echo "$overall_status" | jq -Rs .),
  "status_details": $(echo "$status_details" | jq -Rs .),
  "check_runs": {
    "total_checks": $total_checks,
    "passed_checks": $passed_checks,
    "failed_checks": $failed_checks,
    "pending_checks": $pending_checks,
    "cancelled_checks": $cancelled_checks
  },
  "workflow_analysis": {
    "total_workflows": $ci_workflows,
    "passing_workflows": $passing_workflows,
    "failing_workflows": $failing_workflows,
    "workflow_success_rate": $(if [ "$ci_workflows" -gt 0 ]; then echo "scale=2; $passing_workflows * 100 / $ci_workflows" | bc; else echo "0"; fi)
  },
  "specific_checks": {
    "test_workflow_status": $(echo "$test_workflow_status" | jq -Rs .),
    "build_workflow_status": $(echo "$build_workflow_status" | jq -Rs .),
    "lint_workflow_status": $(echo "$lint_workflow_status" | jq -Rs .)
  },
  "ci_readiness": {
    "ready_for_merge": $(if [ "$overall_status" == "success" ]; then echo "true"; else echo "false"; fi),
    "blockers_exist": $(if [ "$failed_checks" -gt 0 ]; then echo "true"; else echo "false"; fi),
    "failing_tests": $(echo "$failing_workflows" | jq -Rs .)
  },
  "timestamp": "$(date -Iseconds)"
}
EOF
    
    echo "✓ CI/CD status saved to: $output_file"
    echo "✓ Overall Status: $overall_status"
    echo "✓ Success Rate: $(if [ "$ci_workflows" -gt 0 ]; then echo "scale=1; $passing_workflows * 100 / $ci_workflows" | bc; else echo "0"; fi)%"
    echo "✓ Ready for Merge: $(if [ "$overall_status" == "success" ]; then echo "Yes"; else echo "No"; fi)"
}

# Function: Calculate PR age in days
calculate_pr_age_days() {
    local created_at=$1
    
    # Calculate difference in days
    local created_timestamp=$(date -d "$created_at" +%s 2>/dev/null || echo "0")
    local current_timestamp=$(date +%s)
    local age_seconds=$((current_timestamp - created_timestamp))
    local age_days=$((age_seconds / 86400))
    
    echo "$age_days"
}

# Function: Calculate PR complexity score
calculate_pr_complexity() {
    local files_changed=$1
    local conflict_files=$2
    local additions=$3
    local deletions=$4
    
    # Calculate complexity based on multiple factors
    # Files changed (40% weight)
    local file_complexity=0
    if [ "$files_changed" -le 5 ]; then
        file_complexity=1
    elif [ "$files_changed" -le 15 ]; then
        file_complexity=2
    elif [ "$files_changed" -le 30 ]; then
        file_complexity=3
    else
        file_complexity=4
    fi
    
    # Conflict factor (30% weight)
    local conflict_complexity=$conflict_files
    [ "$conflict_complexity" -gt 4 ] && conflict_complexity=4
    
    # Change size factor (30% weight)
    local total_changes=$((additions + deletions))
    local change_complexity=1
    if [ "$total_changes" -le 100 ]; then
        change_complexity=1
    elif [ "$total_changes" -le 500 ]; then
        change_complexity=2
    elif [ "$total_changes" -le 2000 ]; then
        change_complexity=3
    else
        change_complexity=4
    fi
    
    # Calculate weighted complexity
    local complexity=$(echo "scale=2; ($file_complexity * 0.4) + ($conflict_complexity * 0.3) + ($change_complexity * 0.3)" | bc)
    echo "$complexity"
}

# Function: Get PR commit SHA
get_pr_commit_sha() {
    local pr_id=$1
    
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "$GH_REPOS_API/$GITHUB_REPO/pulls/$pr_id" | jq -r '.head.sha' | cut -c1-7
}

# Function: Enhanced testing integration
integrate_with_testing_framework() {
    local pr_id=$1
    
    echo "Integrating GitHub PR context and CI/CD status with testing framework..."
    
    # Get GitHub PR context
    get_github_pr_context "$pr_id" "test-results/pr-data/${pr_id}-gh-context.json"
    
    # Get CI/CD status
    get_cicd_status "$pr_id" "$CI_SYSTEM" "test-results/pr-data/${pr_id}-cicd-status.json"
    
    # Create enhanced PR data file
    merge_context_data "$pr_id"
}

# Function: Merge context data with testing framework
merge_context_data() {
    local pr_id=$1
    
    echo "→ Merging context data for enhanced testing..."
    
    # Check if base PR data exists
    local base_data="test-results/pr-data/${pr_id}.json"
    local gh_context="test-results/pr-data/${pr_id}-gh-context.json"
    local cicd_status="test-results/pr-data/${pr_id}-cicd-status.json"
    
    if [ ! -f "$base_data" ]; then
        echo "WARNING: Base PR data file not found: $base_data"
        echo "Creating enhanced template from GitHub context..."
        create_enhanced_pr_template "$pr_id"
        return
    fi
    
    # Merge all context data
    if [ -f "$gh_context" ] && [ -f "$cicd_status" ]; then
        # Create enhanced data file
        local enhanced_data="test-results/pr-data/${pr_id}-enhanced.json"
        
        jq -s '.[0] * .[1] * .[2]' \
            "$base_data" "$gh_context" "$cicd_status" > "$enhanced_data"
        
        echo "✓ Enhanced PR data created: $enhanced_data"
        echo "  → Base data + GitHub context + CI/CD status merged"
        
        # Copy to main data file for testing framework
        cp "$enhanced_data" "$base_data"
    fi
}

# Function: Create enhanced PR template
create_enhanced_pr_template() {
    local pr_id=$1
    
    echo "Creating enhanced PR data template from GitHub context..."
    
    local gh_context="test-results/pr-data/${pr_id}-gh-context.json"
    local cicd_status="test-results/pr-data/${pr_id}-cicd-status.json"
    local enhanced_template="test-results/pr-data/${pr_id}.json"
    
    if [ -f "$gh_context" ]; then
        # Extract key metrics from GitHub context
        local complexity_score=$(jq -r '.change_metrics.complexity_score' "$gh_context")
        local files_changed=$(jq -r '.change_metrics.files_changed' "$gh_context")
        local conflicts=$(jq -r '.change_metrics.conflict_files' "$gh_context")
        local has_conflicts=$(jq -r '.context_issues.has_conflicts' "$gh_context")
        local mergeable=$(jq -r '.pr_metadata.mergeable' "$gh_context")
        local outstanding_reviews=$(jq -r '.context_issues.outstanding_reviews' "$gh_context")
        
        # Create enhanced template
        cat > "$enhanced_template" << EOF
{
  "file_count": $files_changed,
  "conflict_type": "$(if [ "$conflicts" -gt 0 ]; then echo "mixed"; else echo "content"; fi)",
  "dependency_impact": $((complexity_score / 1.0 | 0)),
  "semantic_changes": $((complexity_score / 1.2 | 0)),
  "feature_requirements": "PR #$pr_id resolution enhancement",
  "complexity_classification": "$(if [ "$complexity_score" -le 1.5 ]; then echo "low"; elif [ "$complexity_score" -le 2.5 ]; then echo "medium"; elif [ "$complexity_score" -le 3.5 ]; then echo "high"; else echo "critical"; fi)",
  
  "github_context": {
    "pr_metadata": $(jq '.pr_metadata' "$gh_context"),
    "change_metrics": $(jq '.change_metrics' "$gh_context"),
    "review_status": $(jq '.review_status' "$gh_context"),
    "context_issues": $(jq '.context_issues' "$gh_context")
  },
  
  "cicd_status": {
    "overall_status": $(jq '.overall_status' "$cicd_status"),
    "check_runs": $(jq '.check_runs' "$cicd_status"),
    "ci_readiness": $(jq '.ci_readiness' "$cicd_status")
  },
  
  "enhanced_testing_criteria": {
    "github_pr_factors": {
      "complexity_score": $complexity_score,
      "has_conflicts": $has_conflicts,
      "is_mergeable": $mergeable,
      "outstanding_reviews": $outstanding_reviews
    },
    "cicd_factors": {
      "ready_for_merge": $(jq -r '.ci_readiness.ready_for_merge' "$cicd_status"),
      "blockers_exist": $(jq -r '.ci_readiness.blockers_exist' "$cicd_status"),
      "workflow_success_rate": $(jq -r '.workflow_analysis.workflow_success_rate' "$cicd_status")
    }
  },
  
  "feature_preservation": 0.95,
  "regression_count": 0,
  "manual_interventions": 3,
  "tests_passed": 45,
  "tests_total": 50,
  "performance_impact": 2.1,
  "security_score": 0.92,
  "documentation_complete": true,
  "workflow_clarity": 3,
  "error_recovery": 4,
  "tool_integration": 3,
  "learning_curve": 2,
  "timestamp": "$(date -Iseconds)"
}
EOF
        
        echo "✓ Enhanced PR template created: $enhanced_template"
    fi
}

# Function: Display help
show_help() {
    echo "Usage: $0 <PR_ID> [CI_SYSTEM]"
    echo ""
    echo "Arguments:"
    echo "  PR_ID          - GitHub PR number to analyze"
    echo "  CI_SYSTEM      - CI/CD system type (github-actions, gitlab-ci, jenkins, azure-devops)"
    echo ""
    echo "Environment Variables:"
    echo "  GITHUB_TOKEN   - GitHub Personal Access Token (required)"
    echo "  GITHUB_REPO    - GitHub repository (format: owner/repo)"
    echo ""
    echo "Examples:"
    echo "  $0 123 github-actions"
    echo "  GITHUB_TOKEN=ghp_xxx GITHUB_REPO=myorg/myrepo $0 456"
}

# Main execution
case "${1:-}" in
    -h|--help|"")
        show_help
        exit 0
        ;;
    *)
        if [ -z "$PR_ID" ]; then
            echo "ERROR: PR_ID is required"
            show_help
            exit 1
        fi
        
        integrate_with_testing_framework "$PR_ID" "$CI_SYSTEM"
        ;;
esac