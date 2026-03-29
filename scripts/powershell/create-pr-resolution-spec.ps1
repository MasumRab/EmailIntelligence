# create-pr-resolution-spec.ps1
# Create a PR resolution specification based on merge scenarios and architectural branch conflicts
# This script helps users create proper specifications for complex PR resolution scenarios
#
# Usage: .\create-pr-resolution-spec.ps1 [OPTIONS]
#
# OPTIONS:
#   -Interactive    Interactive mode with guided prompts (default)
#   -Template       Show only the specification template
#   -MergeInfo      Display merge conflict information first
#   -Help           Show help message

param(
    [switch]$Interactive,
    [switch]$Template,
    [switch]$MergeInfo,
    [switch]$Help
)

function Show-Help {
    @"
Usage: create-pr-resolution-spec.ps1 [OPTIONS]

Create a PR resolution specification based on merge scenarios and architectural branch conflicts.
This script provides a guided template to help create proper specifications for complex PR resolution scenarios.

OPTIONS:
  -Interactive    Interactive mode with guided prompts (default)
  -Template       Show only the specification template
  -MergeInfo      Display current merge conflict information
  -Help           Show this help message

EXAMPLES:
  # Interactive guided specification creation
  .\create-pr-resolution-spec.ps1
  
  # Show specification template only
  .\create-pr-resolution-spec.ps1 -Template
  
  # Check current merge conflicts
  .\create-pr-resolution-spec.ps1 -MergeInfo

"@
}

function Get-MergeStatus {
    Write-Host "=== Current Merge Status ===" -ForegroundColor Cyan
    
    # Check git status
    try {
        $gitStatus = git status --porcelain
        $currentBranch = git branch --show-current
        
        # Check for merge conflicts
        $conflictedFiles = $gitStatus | Where-Object { $_ -match "^UU" }
        
        if ($conflictedFiles) {
            Write-Host "STATUS: In merge conflict" -ForegroundColor Red
            
            Write-Host "CONFLICTed files:"
            foreach ($file in $conflictedFiles) {
                $fileName = $file -replace "^UU\s+", ""
                Write-Host "  $fileName" -ForegroundColor Yellow
            }
            
            # Show merge base
            $mergeBase = git merge-base HEAD $currentBranch
            Write-Host "MERGE base: $mergeBase"
        }
        elseif ($gitStatus | Where-Object { $_ -match "^\.\M" }) {
            Write-Host "STATUS: Changes detected (not in conflict)" -ForegroundColor Yellow
            
            $modifiedFiles = $gitStatus | Where-Object { $_ -match "^\.\M" } | Select-Object -First 5
            foreach ($file in $modifiedFiles) {
                $fileName = $file -replace "^\.\M\s+", ""
                Write-Host "  $fileName ($file.Substring(0,2))" -ForegroundColor Yellow
            }
            if (($gitStatus | Where-Object { $_ -match "^\.\M" }).Count -gt 5) {
                Write-Host "  ... and more" -ForegroundColor Gray
            }
        }
        else {
            Write-Host "STATUS: Clean working directory" -ForegroundColor Green
        }
        
        Write-Host
        Write-Host "CURRENT BRANCH: $currentBranch"
        
        # Show remotes
        $remotes = git remote -v
        if ($remotes) {
            Write-Host "REMOTES:"
            $remotes | ForEach-Object { Write-Host "  $_" }
        } else {
            Write-Host "  No remotes configured"
        }
        
        Write-Host
        Write-Host "RECENT COMMITS:"
        git log --oneline -3 | ForEach-Object { Write-Host "  $_" }
    }
    catch {
        Write-Host "Error getting git status: $_" -ForegroundColor Red
    }
}

function Show-MergeInfo {
    Write-Host "🔍 Merge Conflict Analysis" -ForegroundColor Cyan
    Write-Host "=========================="
    
    Get-MergeStatus
    
    Write-Host "⚡ Resolution Recommendations:" -ForegroundColor Yellow
    Write-Host "1. Use 'git status' to see exact conflict files"
    Write-Host "2. Use 'git diff' to see conflict differences"
    Write-Host "3. Consider using 'git mergetool' for visual resolution"
    Write-Host "4. Document resolution approach in specification"
    Write-Host
}

function Create-SpecificationTemplate {
    @"
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
*Generated by create-pr-resolution-spec.ps1 on $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")*
"@
}

function Run-InteractiveMode {
    Write-Host "🚀 PR Resolution Specification Creator" -ForegroundColor Cyan
    Write-Host "======================================="
    Write-Host
    Write-Host "This tool helps you create detailed specifications for complex PR resolution scenarios."
    Write-Host "It guides you through analyzing merge conflicts and defining resolution strategies."
    Write-Host
    
    # Get basic information
    $objective = Read-Host "📋 What is the main objective for this PR resolution? (e.g., 'Merge feature/auth to main')"
    Write-Host
    
    $sourceBranch = Read-Host "🌿 Source branch"
    $targetBranch = Read-Host "🎯 Target branch"
    Write-Host
    
    Write-Host "📊 Conflict Analysis" -ForegroundColor Yellow
    Write-Host "==================="
    $conflictCount = Read-Host "How many files have conflicts? (or 'unknown')"
    $conflictType = Read-Host "What type of conflicts? (content/structural/architectural)"
    $complexity = Read-Host "Estimated complexity? (simple/moderate/complex/critical)"
    Write-Host
    
    Write-Host "🎨 Resolution Strategy" -ForegroundColor Yellow
    Write-Host "====================="
    $approach = Read-Host "Preferred approach? (conservative/feature-preservation/refactoring)"
    Write-Host
    
    Write-Host "⏱️ Planning" -ForegroundColor Yellow
    Write-Host "==========="
    $timeEstimate = Read-Host "Estimated resolution time? (e.g., '2 hours', '1 day')"
    $reviewers = Read-Host "Who needs to review this? (names/roles)"
    Write-Host
    
    # Generate personalized template
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    @"
# PR Resolution Specification: $objective

*Generated: $timestamp*

## Merge Scenario Information

### Branch Details
- **Source Branch**: $sourceBranch
- **Target Branch**: $targetBranch
- **Merge Type**: [fast-forward/three-way/conflicted]
- **Architecture Impact**: [breaking/non-breaking/enhancement]

### Conflict Characteristics
- **Conflict Count**: $conflictCount
- **Conflict Type**: $conflictType
- **Complexity Level**: $complexity
- **Affected Areas**: [files/modules/components]

## Resolution Requirements

### Primary Objectives
1. **Primary Goal**: $objective
2. **Constraints**: [Technical/organizational constraints]
3. **Success Criteria**: [How to measure success]

### Selected Strategy
**Approach**: $approach
- **Pros**: [Benefits of this approach]
- **Cons**: [Risks and challenges]
- **Risk Level**: [Low/Medium/High]
- **Effort**: [Low/Medium/High]

### Resource Requirements
- **Development Time**: $timeEstimate
- **Review Required**: $reviewers
- **Rollback Complexity**: [Simple/Complex]

---

## Next Steps

1. **Complete the template** above with detailed information
2. **Use this specification** with the EmailIntelligence CLI:
   ```
   eai setup-resolution --pr [PR_NUMBER] --source-branch $sourceBranch --target-branch $targetBranch
   ```

3. **Follow the resolution workflow** with constitutional validation and enhancement preservation

---
*Template generated by create-pr-resolution-spec.ps1*
"@
    
    Write-Host
    Write-Host "💡 Tip: Copy the specification above to your resolution planning document" -ForegroundColor Green
    Write-Host "🔧 Use the EmailIntelligence CLI with this specification for guided resolution" -ForegroundColor Green
}

# Main execution logic
function Main {
    if ($Help) {
        Show-Help
        exit 0
    }
    
    if ($MergeInfo) {
        Show-MergeInfo
        exit 0
    }
    
    if ($Template) {
        Create-SpecificationTemplate
        exit 0
    }
    
    if ($Interactive) {
        Run-InteractiveMode
    } else {
        Create-SpecificationTemplate
    }
}

# Execute main function
Main