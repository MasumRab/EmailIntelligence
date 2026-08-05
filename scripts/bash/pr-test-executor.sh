#!/usr/bin/env bash
# pr-test-executor.sh
# Comprehensive test execution framework for EmailIntelligence PR resolution improvements
# Executes the two-phase testing methodology with automated data collection

set -e

# Parse command line arguments
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Configuration
TEST_PHASE="${1:-baseline}"  # baseline or improved
PR_LIST_FILE="${2:-pr-test-list.txt}"
OUTPUT_DIR="test-results/$(date +%Y%m%d-%H%M%S)"

# Test categories and weights
declare -A COMPLEXITY_WEIGHTS=([low]=1 [medium]=2 [high]=3 [critical]=4)
declare -A QUALITY_THRESHOLDS=(min_tests_pass 0.8 performance_max_degrade 5.0 security_min_score 0.9)

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/pr-data"
mkdir -p "$OUTPUT_DIR/metrics"
mkdir -p "$OUTPUT_DIR/reports"

# Test configuration
EMAILINTELLIGENCE_VERSION="${EMAILINTELLIGENCE_VERSION:-latest}"
GIT_TEST_REPO="${GIT_TEST_REPO:-test-repo}"

echo "=== EmailIntelligence PR Resolution Testing Framework ==="
echo "Phase: $TEST_PHASE"
echo "Output: $OUTPUT_DIR"
echo "Configuration: $EMAILINTELLIGENCE_VERSION"
echo

# Function: Calculate complexity score
calculate_complexity_score() {
    local file_count=$1
    local conflict_type=$2
    local dependency_impact=$3
    local semantic_changes=$4
    
    # Normalize inputs
    local file_weight
    case $file_count in
        1-5) file_weight=1 ;;
        6-15) file_weight=2 ;;
        16-30) file_weight=3 ;;
        31-50) file_weight=4 ;;
        *) file_weight=4 ;;
    esac
    
    local conflict_weight
    case $conflict_type in
        content) conflict_weight=1 ;;
        structural) conflict_weight=2 ;;
        architectural) conflict_weight=3 ;;
        mixed) conflict_weight=4 ;;
    esac
    
    local dep_weight=$dependency_impact  # 1-4 scale
    local semantic_weight=$semantic_changes  # 1-4 scale
    
    # Calculate weighted score (0.0-4.0)
    local complexity_score=$(echo "scale=2; ($file_weight * 0.3) + ($conflict_weight * 0.25) + ($dep_weight * 0.25) + ($semantic_weight * 0.2)" | bc)
    echo "$complexity_score"
}

# Function: Calculate effectiveness score
calculate_effectiveness_score() {
    local feature_preservation=$1
    local regressions=$2
    local resolution_time=$3
    local manual_interventions=$4
    
    # Feature preservation (0.0-1.0)
    local preservation_score=$(echo "scale=3; $feature_preservation" | bc)
    
    # Regression penalty (0.0-1.0, subtract from 1.0)
    local regression_score=$(echo "scale=3; (10 - $regressions) / 10" | bc)
    [ $(echo "$regression_score < 0" | bc) -eq 1 ] && regression_score=0
    
    # Time efficiency (0.0-1.0, assuming max 240 minutes)
    local time_score=$(echo "scale=3; if (240 - $resolution_time < 0) 0 else (240 - $resolution_time) / 240" | bc)
    
    # Manual intervention score (0.0-1.0, subtract from 1.0)
    local intervention_score=$(echo "scale=3; (10 - $manual_interventions) / 10" | bc)
    [ $(echo "$intervention_score < 0" | bc) -eq 1 ] && intervention_score=0
    
    # Calculate weighted effectiveness score
    local effectiveness_score=$(echo "scale=3; ($preservation_score * 0.4) + ($regression_score * 0.2) + ($time_score * 0.2) + ($intervention_score * 0.2)" | bc)
    echo "$effectiveness_score"
}

# Function: Calculate quality score
calculate_quality_score() {
    local tests_passed=$1
    local tests_total=$2
    local performance_degrade=$3
    local security_score=$4
    local documentation_complete=$5
    
    # Test coverage (0.0-1.0)
    local test_score=$(echo "scale=3; $tests_passed / $tests_total" | bc)
    
    # Performance impact (0.0 or 1.0)
    local perf_score=1
    if [ $(echo "$performance_degrade > 5.0" | bc) -eq 1 ]; then
        perf_score=0
    fi
    
    # Security compliance (0.0-1.0)
    local security_score_norm=$(echo "scale=3; $security_score" | bc)
    
    # Documentation (0.0 or 1.0)
    local doc_score=0
    if [ "$documentation_complete" = "true" ]; then
        doc_score=1
    fi
    
    # Calculate weighted quality score
    local quality_score=$(echo "scale=3; ($test_score * 0.3) + ($perf_score * 0.25) + ($security_score_norm * 0.25) + ($doc_score * 0.2)" | bc)
    echo "$quality_score"
}

# Function: Calculate user experience score
calculate_ux_score() {
    local workflow_clarity=$1
    local error_recovery=$2
    local tool_integration=$3
    local learning_curve=$4
    
    # Normalize to 0.0-1.0 scale
    local clarity_score=$(echo "scale=3; $workflow_clarity / 5" | bc)
    local recovery_score=$(echo "scale=3; $error_recovery / 5" | bc)
    local integration_score=$(echo "scale=3; $tool_integration / 5" | bc)
    local curve_score=$(echo "scale=3; $learning_curve / 5" | bc)
    
    # Calculate weighted UX score
    local ux_score=$(echo "scale=3; ($clarity_score * 0.3) + ($recovery_score * 0.25) + ($integration_score * 0.25) + ($curve_score * 0.2)" | bc)
    echo "$ux_score"
}

# Function: Test individual PR
test_pr() {
    local pr_id=$1
    local pr_data_file="$OUTPUT_DIR/pr-data/${pr_id}.json"
    local pr_metrics_file="$OUTPUT_DIR/metrics/${pr_id}-metrics.json"
    
    echo "Testing PR: $pr_id"
    
    # Validate PR data file exists
    if [ ! -f "$pr_data_file" ]; then
        echo "ERROR: PR data file not found: $pr_data_file"
        return 1
    fi
    
    # Extract PR data
    local file_count=$(jq -r '.file_count' "$pr_data_file")
    local conflict_type=$(jq -r '.conflict_type' "$pr_data_file")
    local dependency_impact=$(jq -r '.dependency_impact' "$pr_data_file")
    local semantic_changes=$(jq -r '.semantic_changes' "$pr_data_file")
    
    local feature_requirements=$(jq -r '.feature_requirements' "$pr_data_file")
    local complexity_classification=$(jq -r '.complexity_classification' "$pr_data_file")
    
    # Execute resolution process
    echo "  → Executing resolution process..."
    local start_time=$(date +%s)
    
    # Simulate resolution execution based on EmailIntelligence version
    case $EMAILINTELLIGENCE_VERSION in
        baseline)
            # Use current EmailIntelligence version
            simulate_baseline_resolution "$pr_id"
            ;;
        improved)
            # Use enhanced EmailIntelligence version
            simulate_improved_resolution "$pr_id"
            ;;
    esac
    
    local end_time=$(date +%s)
    local resolution_time=$((end_time - start_time))
    
    # Collect resolution metrics
    echo "  → Collecting metrics..."
    local feature_preservation=$(jq -r '.feature_preservation' "$pr_data_file")
    local regressions=$(jq -r '.regression_count' "$pr_data_file")
    local manual_interventions=$(jq -r '.manual_interventions' "$pr_data_file")
    
    local tests_passed=$(jq -r '.tests_passed' "$pr_data_file")
    local tests_total=$(jq -r '.tests_total' "$pr_data_file")
    local performance_degrade=$(jq -r '.performance_impact' "$pr_data_file")
    local security_score=$(jq -r '.security_score' "$pr_data_file")
    local documentation_complete=$(jq -r '.documentation_complete' "$pr_data_file")
    
    local workflow_clarity=$(jq -r '.workflow_clarity' "$pr_data_file")
    local error_recovery=$(jq -r '.error_recovery' "$pr_data_file")
    local tool_integration=$(jq -r '.tool_integration' "$pr_data_file")
    local learning_curve=$(jq -r '.learning_curve' "$pr_data_file")
    
    # Calculate scores
    local complexity_score=$(calculate_complexity_score "$file_count" "$conflict_type" "$dependency_impact" "$semantic_changes")
    local effectiveness_score=$(calculate_effectiveness_score "$feature_preservation" "$regressions" "$resolution_time" "$manual_interventions")
    local quality_score=$(calculate_quality_score "$tests_passed" "$tests_total" "$performance_degrade" "$security_score" "$documentation_complete")
    local ux_score=$(calculate_ux_score "$workflow_clarity" "$error_recovery" "$tool_integration" "$learning_curve")
    
    # Overall score (weighted average)
    local overall_score=$(echo "scale=3; ($complexity_score * 0.2) + ($effectiveness_score * 0.3) + ($quality_score * 0.3) + ($ux_score * 0.2)" | bc)
    
    # Generate metrics report
    cat > "$pr_metrics_file" << EOF
{
  "pr_id": "$pr_id",
  "test_phase": "$TEST_PHASE",
  "timestamp": "$(date -Iseconds)",
  "complexity_score": $complexity_score,
  "effectiveness_score": $effectiveness_score,
  "quality_score": $quality_score,
  "ux_score": $ux_score,
  "overall_score": $overall_score,
  "resolution_time_minutes": $resolution_time,
  "resolution_data": {
    "file_count": $file_count,
    "conflict_type": "$conflict_type",
    "dependency_impact": $dependency_impact,
    "semantic_changes": $semantic_changes,
    "complexity_classification": "$complexity_classification",
    "feature_preservation_rate": $feature_preservation,
    "regression_count": $regressions,
    "manual_interventions": $manual_interventions,
    "tests_passed": $tests_passed,
    "tests_total": $tests_total,
    "performance_degrade_percent": $performance_degrade,
    "security_score": $security_score,
    "documentation_complete": $documentation_complete,
    "workflow_clarity": $workflow_clarity,
    "error_recovery": $error_recovery,
    "tool_integration": $tool_integration,
    "learning_curve": $learning_curve
  }
}
EOF
    
    echo "  ✓ Completed - Overall Score: $overall_score"
    echo "  ✓ Metrics saved to: $pr_metrics_file"
}

# Function: Simulate baseline resolution
simulate_baseline_resolution() {
    local pr_id=$1
    # Simulate baseline performance
    echo "  → Applying baseline EmailIntelligence resolution approach"
    sleep 2  # Simulate processing time
}

# Function: simulate improved resolution
simulate_improved_resolution() {
    local pr_id=$1
    # Simulate improved performance
    echo "  → Applying enhanced EmailIntelligence resolution approach"
    sleep 1  # Simulate faster processing time
}

# Function: Run complete test suite
run_test_suite() {
    echo "Starting test suite execution..."
    
    # Check PR list file
    if [ ! -f "$PR_LIST_FILE" ]; then
        echo "ERROR: PR list file not found: $PR_LIST_FILE"
        echo "Please create a PR list file with PR IDs to test"
        return 1
    fi
    
    # Read PR IDs
    local pr_ids=()
    while IFS= read -r line; do
        # Skip empty lines and comments
        if [[ $line =~ ^#.*$ ]] || [[ -z $line ]]; then
            continue
        fi
        pr_ids+=("$line")
    done < "$PR_LIST_FILE"
    
    if [ ${#pr_ids[@]} -eq 0 ]; then
        echo "ERROR: No PR IDs found in $PR_LIST_FILE"
        return 1
    fi
    
    echo "Testing ${#pr_ids[@]} PRs: ${pr_ids[*]}"
    echo
    
    # Test each PR
    for pr_id in "${pr_ids[@]}"; do
        test_pr "$pr_id"
        echo
    done
    
    # Generate summary report
    generate_summary_report "${pr_ids[@]}"
}

# Function: Generate summary report
generate_summary_report() {
    local pr_ids=("$@")
    local summary_file="$OUTPUT_DIR/reports/test-summary.json"
    
    echo "Generating summary report..."
    
    # Calculate aggregate metrics
    local complexity_sum=0
    local effectiveness_sum=0
    local quality_sum=0
    local ux_sum=0
    local overall_sum=0
    local resolution_time_sum=0
    
    for pr_id in "${pr_ids[@]}"; do
        local metrics_file="$OUTPUT_DIR/metrics/${pr_id}-metrics.json"
        if [ -f "$metrics_file" ]; then
            local complexity=$(jq -r '.complexity_score' "$metrics_file")
            local effectiveness=$(jq -r '.effectiveness_score' "$metrics_file")
            local quality=$(jq -r '.quality_score' "$metrics_file")
            local ux=$(jq -r '.ux_score' "$metrics_file")
            local overall=$(jq -r '.overall_score' "$metrics_file")
            local time=$(jq -r '.resolution_time_minutes' "$metrics_file")
            
            complexity_sum=$(echo "$complexity_sum + $complexity" | bc)
            effectiveness_sum=$(echo "$effectiveness_sum + $effectiveness" | bc)
            quality_sum=$(echo "$quality_sum + $quality" | bc)
            ux_sum=$(echo "$ux_sum + $ux" | bc)
            overall_sum=$(echo "$overall_sum + $overall" | bc)
            resolution_time_sum=$(echo "$resolution_time_sum + $time" | bc)
        fi
    done
    
    local pr_count=${#pr_ids[@]}
    local avg_complexity=$(echo "scale=3; $complexity_sum / $pr_count" | bc)
    local avg_effectiveness=$(echo "scale=3; $effectiveness_sum / $pr_count" | bc)
    local avg_quality=$(echo "scale=3; $quality_sum / $pr_count" | bc)
    local avg_ux=$(echo "scale=3; $ux_sum / $pr_count" | bc)
    local avg_overall=$(echo "scale=3; $overall_sum / $pr_count" | bc)
    local avg_resolution_time=$(echo "scale=2; $resolution_time_sum / $pr_count" | bc)
    
    # Create summary report
    cat > "$summary_file" << EOF
{
  "test_phase": "$TEST_PHASE",
  "test_timestamp": "$(date -Iseconds)",
  "emailintelligence_version": "$EMAILINTELLIGENCE_VERSION",
  "pr_count": $pr_count,
  "pr_tested": $(printf '%s\n' "${pr_ids[@]}" | jq -R . | jq -s .),
  "aggregate_metrics": {
    "average_complexity_score": $avg_complexity,
    "average_effectiveness_score": $avg_effectiveness,
    "average_quality_score": $avg_quality,
    "average_ux_score": $avg_ux,
    "average_overall_score": $avg_overall,
    "average_resolution_time_minutes": $avg_resolution_time
  },
  "performance_benchmarks": {
    "complexity_threshold": 3.0,
    "effectiveness_minimum": 0.7,
    "quality_minimum": 0.8,
    "ux_minimum": 0.6,
    "resolution_time_maximum": 120
  },
  "success_criteria": {
    "overall_score_target": 0.75,
    "resolution_efficiency_target": "< 120 minutes",
    "feature_preservation_target": "> 0.95",
    "quality_threshold": "> 0.8"
  }
}
EOF
    
    echo "Summary report generated: $summary_file"
    echo "=== Test Suite Complete ==="
    echo "Results: $OUTPUT_DIR"
}

# Function: Display help
show_help() {
    echo "Usage: $0 [phase] [pr-list-file]"
    echo ""
    echo "Arguments:"
    echo "  phase           - 'baseline' or 'improved' (default: baseline)"
    echo "  pr-list-file    - File containing PR IDs to test (default: pr-test-list.txt)"
    echo ""
    echo "Environment Variables:"
    echo "  EMAILINTELLIGENCE_VERSION - Version to test (baseline/improved, default: latest)"
    echo "  GIT_TEST_REPO         - Test repository path (default: test-repo)"
    echo ""
    echo "Example:"
    echo "  $0 baseline pr-baseline-list.txt"
    echo "  EMAILINTELLIGENCE_VERSION=improved $0 improved pr-improved-list.txt"
}

# Main execution
case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    baseline|improved)
        run_test_suite
        ;;
    *)
        echo "ERROR: Invalid phase '$1'. Use 'baseline' or 'improved'"
        echo "Use --help for usage information"
        exit 1
        ;;
esac