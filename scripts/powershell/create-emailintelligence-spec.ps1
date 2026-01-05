# create-emailintelligence-spec.ps1
# Create comprehensive EmailIntelligence testing framework specifications with GitHub context and branch analysis
# This tool integrates with GitHub API to collect PR metadata, review status, CI/CD context, and testing framework requirements
#
# Usage: .\create-emailintelligence-spec.ps1 [OPTIONS]
#
# OPTIONS:
#   -Interactive          Interactive mode with GitHub integration (default)
#   -PrNumber <num>       Use specific PR number for GitHub data collection
#   -Baseline            Create specification for baseline testing phase
#   -Improved            Create specification for improved testing phase
#   -Template            Show only the specification template
#   -CollectGitHub       Collect GitHub PR context and metadata
#   -AnalyzeBranches     Perform comprehensive branch analysis
#   -PrepareTesting      Prepare for testing framework integration
#   -Help                Show help message

[CmdletBinding()]
param(
    [switch]$Interactive = $true,
    [string]$PrNumber = "",
    [ValidateSet("baseline", "improved")]
    [string]$PhaseType = "",
    [switch]$Template = $false,
    [switch]$CollectGitHub = $false,
    [switch]$AnalyzeBranches = $false,
    [switch]$PrepareTesting = $false,
    [switch]$Help = $false
)

if ($Help) {
    @"
Usage: create-emailintelligence-spec.ps1 [OPTIONS]

Create comprehensive EmailIntelligence testing framework specifications with GitHub context and branch analysis.

OPTIONS:
  -Interactive          Interactive mode with GitHub integration (default)
  -PrNumber <num>       Use specific PR number for GitHub data collection
  -Baseline            Create specification for baseline testing phase
  -Improved            Create specification for improved testing phase
  -Template            Show only the specification template
  -CollectGitHub       Collect GitHub PR context and metadata
  -AnalyzeBranches     Perform comprehensive branch analysis
  -PrepareTesting      Prepare for testing framework integration
  -Help                Show this help message

EXAMPLES:
  # Interactive specification with GitHub integration
  .\create-emailintelligence-spec.ps1 -CollectGitHub -AnalyzeBranches
  
  # Create specification for specific PR in baseline phase
  .\create-emailintelligence-spec.ps1 -PrNumber 123 -Baseline -CollectGitHub
  
  # Create improved phase specification with testing preparation
  .\create-emailintelligence-spec.ps1 -Improved -PrepareTesting
  
  # Show complete template
  .\create-emailintelligence-spec.ps1 -Template

INTEGRATION WITH TESTING FRAMEWORK:
  This tool creates specifications that integrate with the EmailIntelligence testing framework:
  - Phase 1: Baseline testing with current methodology
  - Phase 2: Improved testing with EmailIntelligence enhancements
  - GitHub API integration for PR context and CI/CD status
  - Branch analysis for conflict resolution strategy
  - Statistical preparation for comparison analysis
"@
    exit 0
}

# Check GitHub configuration
function Test-GitHubConfig {
    if ([string]::IsNullOrEmpty($env:GITHUB_TOKEN)) {
        Write-Host "❌ ERROR: GITHUB_TOKEN not set. Please configure your GitHub token." -ForegroundColor Red
        Write-Host "   `$env:GITHUB_TOKEN='ghp_your_token_here'" -ForegroundColor Yellow
        return $false
    }
    
    if ([string]::IsNullOrEmpty($env:GITHUB_REPO)) {
        Write-Host "❌ ERROR: GITHUB_REPO not set. Please configure your repository." -ForegroundColor Red
        Write-Host "   `$env:GITHUB_REPO='owner/repository-name'" -ForegroundColor Yellow
        return $false
    }
    
    Write-Host "✅ GitHub configuration validated" -ForegroundColor Green
    return $true
}

# Collect GitHub PR context and metadata
function Get-GitHubPRContext {
    param(
        [string]$PrNumber
    )
    
    if ([string]::IsNullOrEmpty($PrNumber)) {
        Write-Host "❌ PR number required for GitHub context collection" -ForegroundColor Red
        return $null
    }
    
    Write-Host "🔍 Collecting GitHub PR context for PR #$PrNumber..." -ForegroundColor Cyan
    
    try {
        # Collect basic PR information
        $prUri = "https://api.github.com/repos/$env:GITHUB_REPO/pulls/$PrNumber"
        $headers = @{ Authorization = "token $env:GITHUB_TOKEN"; Accept = "application/vnd.github.v3+json" }
        $prData = Invoke-RestMethod -Uri $prUri -Headers $headers -UseBasicParsing
        
        if ($prData.message) {
            Write-Host "❌ ERROR: PR #$PrNumber not found or inaccessible" -ForegroundColor Red
            return $null
        }
        
        # Extract key information
        $title = $prData.title
        $author = $prData.user.login
        $state = $prData.state
        $mergeable = $prData.mergeable
        $createdAt = $prData.created_at
        $updatedAt = $prData.updated_at
        $additions = $prData.additions
        $deletions = $prData.deletions
        $changedFiles = $prData.changed_files
        $headSha = $prData.head.sha
        $baseSha = $prData.base.sha
        $headBranch = $prData.head.ref
        $baseBranch = $prData.base.ref
        
        # Calculate PR age
        $createdDate = [datetime]::Parse($createdAt)
        $updatedDate = [datetime]::Parse($updatedAt)
        $prAgeDays = [int](($updatedDate - $createdDate).TotalDays)
        
        # Collect review status
        $reviewsUri = "https://api.github.com/repos/$env:GITHUB_REPO/pulls/$PrNumber/reviews"
        $reviewsData = Invoke-RestMethod -Uri $reviewsUri -Headers $headers -UseBasicParsing
        $approvedReviews = ($reviewsData | Where-Object { $_.state -eq "APPROVED" }).Count
        $changesRequested = ($reviewsData | Where-Object { $_.state -eq "CHANGES_REQUESTED" }).Count
        $commentedReviews = ($reviewsData | Where-Object { $_.state -eq "COMMENTED" }).Count
        
        # Collect CI/CD status if available
        $checksUri = "https://api.github.com/repos/$env:GITHUB_REPO/commits/$headSha/check-runs"
        $checksData = Invoke-RestMethod -Uri $checksUri -Headers $headers -UseBasicParsing
        $checkRuns = $checksData.total_count
        $successfulChecks = ($checksData.check_runs | Where-Object { $_.conclusion -eq "success" }).Count
        $failedChecks = ($checksData.check_runs | Where-Object { $_.conclusion -eq "failure" }).Count
        $pendingChecks = ($checksData.check_runs | Where-Object { $_.conclusion -eq $null }).Count
        
        # Calculate CI/CD success rate
        $cicdSuccessRate = if ($checkRuns -gt 0) { [math]::Round(($successfulChecks * 100) / $checkRuns) } else { 0 }
        
        # Determine complexity
        $changeVolume = if ($changedFiles -gt 20) { "High" } elseif ($changedFiles -gt 5) { "Medium" } else { "Low" }
        $stalenessRisk = if ($prAgeDays -gt 7) { "High" } elseif ($prAgeDays -gt 3) { "Medium" } else { "Low" }
        $mergeReadiness = if ($mergeable -and $failedChecks -eq 0) { "Ready" } else { "Not Ready" }
        
        # Output collected data
        $output = @"

## GitHub PR Context Analysis

### Basic PR Information
- **PR Number**: #$PrNumber
- **Title**: $title
- **Author**: $author
- **State**: $state
- **Created**: $createdAt
- **Last Updated**: $updatedAt
- **Age**: $prAgeDays days
- **Mergeable**: $mergeable

### Branch Analysis
- **Source Branch**: $headBranch ($headSha)
- **Target Branch**: $baseBranch ($baseSha)
- **Source Repository**: $($prData.head.repo.full_name ?? "same-repo")

### Change Metrics
- **Files Changed**: $changedFiles
- **Lines Added**: $additions
- **Lines Deleted**: $deletions
- **Net Changes**: $($additions - $deletions)

### Review Status
- **Approved Reviews**: $approvedReviews
- **Changes Requested**: $changesRequested
- **Comments**: $commentedReviews
- **Total Reviews**: $($reviewsData.Count)

### CI/CD Status
- **Total Check Runs**: $checkRuns
- **Successful Checks**: $successfulChecks
- **Failed Checks**: $failedChecks
- **Pending Checks**: $pendingChecks
- **CI/CD Success Rate**: $cicdSuccessRate%

### Complexity Assessment
- **Change Volume**: $changeVolume
- **Staleness Risk**: $stalenessRisk
- **Merge Readiness**: $mergeReadiness

"@
        
        # Store data for further processing
        $prData | ConvertTo-Json -Depth 10 | Out-File -FilePath "pr-${PrNumber}-data.json" -Encoding UTF8
        
        return $output
    }
    catch {
        Write-Host "❌ ERROR: Failed to collect GitHub data - $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Analyze branch conflicts and characteristics
function Start-BranchAnalysis {
    param(
        [string]$SourceBranch,
        [string]$TargetBranch
    )
    
    Write-Host "🌿 Analyzing branch conflicts between '$SourceBranch' and '$TargetBranch'..." -ForegroundColor Cyan
    
    try {
        # Get merge base
        $mergeBase = git merge-base $SourceBranch $TargetBranch 2>$null
        if ([string]::IsNullOrEmpty($mergeBase)) {
            $mergeBase = "unknown"
        }
        
        # Analyze files that differ
        $conflictFiles = git diff --name-only $mergeBase $SourceBranch $TargetBranch 2>$null | Measure-Object | Select-Object -ExpandProperty Count
        
        # Check for actual conflicts
        $actualConflicts = 0
        try {
            $mergeTreeResult = git merge-tree $(git mktree < $(git ls-tree $mergeBase | ForEach-Object { "100644 $_" })) `
                                        $(git mktree < $(git ls-tree $SourceBranch | ForEach-Object { "100644 $_" })) `
                                        $(git mktree < $(git ls-tree $TargetBranch | ForEach-Object { "100644 $_" })) 2>$null
            if ($mergeTreeResult -match "^<<<<<<<") {
                $actualConflicts = ($mergeTreeResult | Select-String "^<<<<<<<").Count
            }
        } catch {
            # Fallback to manual conflict detection
            $diffFiles = git diff $mergeBase $SourceBranch $TargetBranch 2>$null | Select-String "^<<<<<<<\s"
            $actualConflicts = $diffFiles.Count
        }
        
        # Analyze file types
        $diffFilesList = git diff --name-only $mergeBase $SourceBranch $TargetBranch 2>$null
        $codeFiles = ($diffFilesList | Where-Object { $_ -match '\.(js|ts|py|java|go|rs|cpp|c|h)$' }).Count
        $configFiles = ($diffFilesList | Where-Object { $_ -match '\.(json|yaml|yml|toml|ini|conf)$' }).Count
        $docFiles = ($diffFilesList | Where-Object { $_ -match '\.(md|txt|rst)$' }).Count
        
        # Determine complexity
        $complexity = "Low"
        if ($conflictFiles -gt 50 -or $codeFiles -gt 20) {
            $complexity = "Critical"
        } elseif ($conflictFiles -gt 20 -or $codeFiles -gt 10) {
            $complexity = "High"
        } elseif ($conflictFiles -gt 5 -or $codeFiles -gt 3) {
            $complexity = "Medium"
        }
        
        # Analysis output
        $otherFiles = $conflictFiles - $codeFiles - $configFiles - $docFiles
        if ($otherFiles -lt 0) { $otherFiles = 0 }
        
        $output = @"

## Branch Conflict Analysis

### Merge Characteristics
- **Merge Base**: $mergeBase
- **Files with Differences**: $conflictFiles
- **Actual Merge Conflicts**: $actualConflicts
- **Overall Complexity**: $complexity

### File Type Distribution
- **Code Files**: $codeFiles
- **Configuration Files**: $configFiles  
- **Documentation Files**: $docFiles
- **Other Files**: $otherFiles

### Resolution Strategy Recommendation
"@
        
        # Provide recommendations
        if ($actualConflicts -eq 0) {
            $output += @"
✅ **No conflicts detected** - Clean merge possible
- **Recommended Strategy**: Fast-forward merge or simple merge
- **Risk Level**: Low
- **Testing Required**: Standard validation only
"@
        } elseif ($complexity -eq "Low") {
            $output += @"
🔧 **Simple conflicts** - Manual resolution required
- **Recommended Strategy**: Conservative merge with manual conflict resolution
- **Risk Level**: Low-Medium
- **Testing Required**: Enhanced validation
"@
        } elseif ($complexity -eq "Medium") {
            $output += @"
⚠️ **Moderate conflicts** - Strategic resolution needed
- **Recommended Strategy**: Feature preservation with worktree isolation
- **Risk Level**: Medium
- **Testing Required**: Comprehensive validation
"@
        } else {
            $output += @"
🚨 **Complex conflicts** - Advanced resolution required
- **Recommended Strategy**: Refactoring merge with EmailIntelligence enhancement
- **Risk Level**: High
- **Testing Required**: Full testing framework validation
"@
        }
        
        return $output
    }
    catch {
        Write-Host "❌ ERROR: Failed to analyze branches - $($_.Exception.Message)" -ForegroundColor Red
        return @"

## Branch Conflict Analysis

### Analysis Error
- **Error**: Failed to analyze branch conflicts
- **Fallback**: Manual conflict detection required
- **Recommendation**: Review conflicts manually using git diff and status

"@
    }
}

# Create comprehensive specification template
function New-ComprehensiveTemplate {
    param(
        [string]$PrNumber = "[PR_NUMBER]",
        [string]$PhaseType = "baseline"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $template = @"
# EmailIntelligence Testing Framework Specification

*Generated: $timestamp*
*Phase Type: $PhaseType*
*PR Number: #$PrNumber*

## Executive Summary

This specification defines the testing approach for PR #${PrNumber} using the EmailIntelligence Testing Framework ${PhaseType} phase methodology.

### Testing Framework Integration
- **Phase**: ${PhaseType} (Baseline vs Improved comparison)
- **GitHub Integration**: Full API context and CI/CD status collection
- **Branch Analysis**: Comprehensive conflict detection and resolution strategy
- **Statistical Validation**: Industry-standard statistical analysis for improvement measurement

## GitHub PR Context Analysis

### Basic Information
- **PR Number**: #${PrNumber}
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

### ${PhaseType} Phase Specifics
"@
    
    if ($PhaseType -eq "baseline") {
        $template += @"

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
"@
    } else {
        $template += @"

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
"@
    }
    
    $template += @"

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
- [ ] Complete ${PhaseType} phase testing execution
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
*Generated by create-emailintelligence-spec.ps1 on $timestamp*
*Framework Version: EmailIntelligence v2.0*
*Phase: $PhaseType*
"@
    
    return $template
}

# Interactive specification creation with GitHub integration
function Start-InteractiveSpecification {
    Write-Host "🚀 EmailIntelligence Testing Framework Specification Creator" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host
    Write-Host "This tool creates comprehensive specifications for EmailIntelligence testing framework" -ForegroundColor White
    Write-Host "with GitHub context collection, branch analysis, and testing phase preparation." -ForegroundColor White
    Write-Host
    
    # Phase selection
    Write-Host "📊 Testing Phase Configuration" -ForegroundColor Yellow
    Write-Host "==============================" -ForegroundColor Yellow
    if ([string]::IsNullOrEmpty($PhaseType)) {
        Write-Host "Select testing phase:"
        Write-Host "1) Baseline Phase - Current methodology measurement"
        Write-Host "2) Improved Phase - EmailIntelligence enhancement testing"
        $phaseChoice = Read-Host "Enter choice (1-2)"
        
        switch ($phaseChoice) {
            "1" { $PhaseType = "baseline" }
            "2" { $PhaseType = "improved" }
            default { $PhaseType = "baseline"; Write-Host "Invalid choice. Defaulting to baseline." -ForegroundColor Yellow }
        }
    }
    
    Write-Host "Selected Phase: $PhaseType" -ForegroundColor Green
    Write-Host
    
    # GitHub integration setup
    Write-Host "🔧 GitHub Integration Setup" -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Yellow
    if (-not (Test-GitHubConfig)) {
        Write-Host "Please configure GitHub integration before continuing." -ForegroundColor Red
        exit 1
    }
    
    # PR number collection
    Write-Host
    Write-Host "📋 PR Analysis Configuration" -ForegroundColor Yellow
    Write-Host "============================" -ForegroundColor Yellow
    $prInput = Read-Host "PR Number for analysis (leave empty to analyze current branch)"
    
    if (-not [string]::IsNullOrEmpty($prInput)) {
        $PrNumber = $prInput
        $CollectGitHub = $true
        $AnalyzeBranches = $true
        
        Write-Host "Collecting GitHub context for PR #$PrNumber..." -ForegroundColor Cyan
        $githubContext = Get-GitHubPRContext -PrNumber $PrNumber
        if ($null -eq $githubContext) {
            Write-Host "❌ Failed to collect GitHub context. Continuing with available information." -ForegroundColor Yellow
        } else {
            Write-Host $githubContext
        }
    }
    
    # Branch analysis
    if ([string]::IsNullOrEmpty($PrNumber)) {
        $sourceBranch = Read-Host "Source branch"
        $targetBranch = Read-Host "Target branch"
        
        if (-not [string]::IsNullOrEmpty($sourceBranch) -and -not [string]::IsNullOrEmpty($targetBranch)) {
            $branchAnalysis = Start-BranchAnalysis -SourceBranch $sourceBranch -TargetBranch $targetBranch
            Write-Host $branchAnalysis
        }
    }
    
    # Testing framework preparation
    Write-Host
    Write-Host "🎯 Testing Framework Integration" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Yellow
    $enableScoring = Read-Host "Enable 6-dimensional scoring framework? (Y/n)"
    if ($enableScoring -notmatch "^[Nn]$") {
        $PrepareTesting = $true
        Write-Host "✅ 6-dimensional scoring framework enabled" -ForegroundColor Green
    }
    
    $enableStats = Read-Host "Prepare for statistical comparison analysis? (Y/n)"
    if ($enableStats -notmatch "^[Nn]$") {
        Write-Host "✅ Statistical analysis preparation enabled" -ForegroundColor Green
    }
    
    # Generate specification
    Write-Host
    Write-Host "📝 Generating Comprehensive Specification..." -ForegroundColor Cyan
    Write-Host "===========================================" -ForegroundColor Cyan
    
    $specification = New-ComprehensiveTemplate -PrNumber $PrNumber -PhaseType $PhaseType
    Write-Host $specification
    
    Write-Host
    Write-Host "🎉 Specification Generated Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host
    Write-Host "Next Steps:" -ForegroundColor White
    Write-Host "1. Review and customize the specification above" -ForegroundColor Gray
    Write-Host "2. Use with EmailIntelligence CLI for guided execution:" -ForegroundColor Gray
    if (-not [string]::IsNullOrEmpty($PrNumber)) {
        Write-Host "   python emailintelligence_cli.py setup-resolution --pr $PrNumber --phase $PhaseType" -ForegroundColor Cyan
    } else {
        Write-Host "   python emailintelligence_cli.py setup-resolution --source-branch $sourceBranch --target-branch $targetBranch --phase $PhaseType" -ForegroundColor Cyan
    }
    Write-Host "3. Execute testing framework with comprehensive validation" -ForegroundColor Gray
    Write-Host "4. Collect metrics for statistical analysis and improvement measurement" -ForegroundColor Gray
}

# Main execution logic
function Main {
    if ($Template) {
        New-ComprehensiveTemplate -PrNumber $PrNumber -PhaseType $PhaseType
        exit 0
    }
    
    if ($Interactive) {
        Start-InteractiveSpecification
    } else {
        New-ComprehensiveTemplate -PrNumber $PrNumber -PhaseType $PhaseType
    }
}

# Execute main function
Main