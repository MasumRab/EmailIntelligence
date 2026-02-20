#!/usr/bin/env pwsh
<#
.SYNOPSIS
SOLID, modular wrapper for Speckit Orchestration Command System components

.DESCRIPTION
Provides a flexible interface to execute parts of the Speckit workflow as needed,
following SOLID principles with clear separation of concerns and dependency injection.
#>

# Interface definitions for SOLID architecture
interface IWorkflowValidator {
    [bool] ValidateEnvironment()
    [PSCustomObject] GetEnvironmentContext()
}

interface ITemplateProcessor {
    [bool] ProcessTemplate([string]$TemplatePath, [string]$OutputPath, [hashtable]$Variables)
    [bool] TemplateExists([string]$TemplatePath)
}

interface IAgentContextManager {
    [bool] UpdateAgentContext([string]$AgentType, [PSCustomObject]$PlanData)
    [PSCustomObject] ExtractPlanData([string]$PlanPath)
}

interface IWorkflowOrchestrator {
    [bool] ExecuteHandoff([string]$CommandName, [hashtable]$Context)
    [array] GetAvailableHandoffs([string]$CommandName)
}

# Single Responsibility: Environment validation
class SpeckitEnvironmentValidator : IWorkflowValidator {
    [PSCustomObject]$Paths
    [bool]$HasGit
    
    SpeckitEnvironmentValidator() {
        $this.LoadCommonFunctions()
        $this.Paths = Get-FeaturePathsEnv
        $this.HasGit = Test-HasGit
    }
    
    [void] LoadCommonFunctions() {
        . "$PSScriptRoot/common.ps1"
    }
    
    [bool] ValidateEnvironment() {
        return Test-FeatureBranch -Branch $this.Paths.CURRENT_BRANCH -HasGit $this.HasGit
    }
    
    [PSCustomObject] GetEnvironmentContext() {
        return $this.Paths
    }
}

# Single Responsibility: Template processing
class SpeckitTemplateProcessor : ITemplateProcessor {
    [string]$RepoRoot
    
    SpeckitTemplateProcessor([string]$RepoRoot) {
        $this.RepoRoot = $RepoRoot
    }
    
    [bool] TemplateExists([string]$TemplatePath) {
        return Test-Path $TemplatePath
    }
    
    [bool] ProcessTemplate([string]$TemplatePath, [string]$OutputPath, [hashtable]$Variables) {
        if (-not $this.TemplateExists($TemplatePath)) {
            Write-Warning "Template not found: $TemplatePath"
            return $false
        }
        
        # Ensure output directory exists
        $parent = Split-Path -Parent $OutputPath
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        
        # Copy template
        Copy-Item $TemplatePath $OutputPath -Force
        
        # Replace variables if provided
        if ($Variables.Count -gt 0) {
            $content = Get-Content -LiteralPath $OutputPath -Raw -Encoding utf8
            foreach ($key in $Variables.Keys) {
                $content = $content -replace "\[$($key)\]", $Variables[$key]
            }
            Set-Content -LiteralPath $OutputPath -Value $content -NoNewline -Encoding utf8
        }
        
        return $true
    }
}

# Single Responsibility: Agent context management
class SpeckitAgentContextManager : IAgentContextManager {
    [string]$RepoRoot
    
    SpeckitAgentContextManager([string]$RepoRoot) {
        $this.RepoRoot = $RepoRoot
        $this.LoadCommonFunctions()
    }
    
    [void] LoadCommonFunctions() {
        . "$PSScriptRoot/common.ps1"
    }
    
    [PSCustomObject] ExtractPlanData([string]$PlanPath) {
        if (-not (Test-Path $PlanPath)) {
            throw "Plan file not found: $PlanPath"
        }
        
        $planContent = Get-Content -LiteralPath $PlanPath -Raw -Encoding utf8
        
        return [PSCustomObject]@{
            Language = $this.ExtractField($planContent, 'Language/Version')
            Framework = $this.ExtractField($planContent, 'Primary Dependencies')
            Storage = $this.ExtractField($planContent, 'Storage')
            Content = $planContent
        }
    }
    
    [string] ExtractField([string]$Content, [string]$FieldPattern) {
        $pattern = "\*\*$FieldPattern\*\*:\s*([^\n]+)"
        if ($Content -match $pattern) {
            return $matches[1].Trim()
        }
        return "NEEDS CLARIFICATION"
    }
    
    [bool] UpdateAgentContext([string]$AgentType, [PSCustomObject]$PlanData) {
        $agentFiles = $this.GetAgentFilePaths()
        $targetFile = $agentFiles[$AgentType]
        
        if (-not $targetFile) {
            Write-Warning "Unknown agent type: $AgentType"
            return $false
        }
        
        # Create/update agent file with plan data
        $templatePath = Join-Path $this.RepoRoot '.specify/templates/agent-file-template.md'
        $processor = [SpeckitTemplateProcessor]::new($this.RepoRoot)
        
        $variables = @{
            'PROJECT NAME' = (Get-CurrentBranch)
            'DATE' = (Get-Date).ToString('yyyy-MM-dd')
            'TECH_STACK' = $this.BuildTechStack($PlanData)
        }
        
        return $processor.ProcessTemplate($templatePath, $targetFile, $variables)
    }
    
    [hashtable] GetAgentFilePaths() {
        return @{
            'claude' = Join-Path $this.RepoRoot 'CLAUDE.md'
            'qwen' = Join-Path $this.RepoRoot '.qwen/commands/speckit.implementation.toml'
            'cursor-agent' = Join-Path $this.RepoRoot '.cursor/rules/specify-rules.mdc'
            'copilot' = Join-Path $this.RepoRoot '.github/agents/copilot-instructions.md'
            # Add other agent types as needed
        }
    }
    
    [string] BuildTechStack([PSCustomObject]$PlanData) {
        $stack = @()
        if ($PlanData.Language -and $PlanData.Language -ne "NEEDS CLARIFICATION") {
            $stack += $PlanData.Language
        }
        if ($PlanData.Framework -and $PlanData.Framework -ne "NEEDS CLARIFICATION") {
            $stack += $PlanData.Framework
        }
        if ($PlanData.Storage -and $PlanData.Storage -ne "NEEDS CLARIFICATION" -and $PlanData.Storage -ne "N/A") {
            $stack += $PlanData.Storage
        }
        return $stack -join ', '
    }
}

# Single Responsibility: Workflow orchestration
class SpeckitWorkflowOrchestrator : IWorkflowOrchestrator {
    [string]$RepoRoot
    
    SpeckitWorkflowOrchestrator([string]$RepoRoot) {
        $this.RepoRoot = $RepoRoot
    }
    
    [bool] ExecuteHandoff([string]$CommandName, [hashtable]$Context) {
        $handoffs = $this.GetAvailableHandoffs($CommandName)
        
        foreach ($handoff in $handoffs) {
            Write-Output "Executing handoff: $($handoff.label) -> $($handoff.agent)"
            # In a real implementation, this would trigger the next agent/command
        }
        
        return $true
    }
    
    [array] GetAvailableHandoffs([string]$CommandName) {
        # Parse TOML command files to get handoff configuration
        $commandPath = Join-Path $this.RepoRoot ".qwen/commands/$CommandName.toml"
        
        if (-not (Test-Path $commandPath)) {
            return @()
        }
        
        # Simplified TOML parsing - in production, use a proper TOML parser
        $content = Get-Content $commandPath -Raw
        $handoffs = @()
        
        if ($content -match 'handoffs:\s*\[(.*?)\]') {
            $handoffSection = $matches[1]
            # Extract handoff information (simplified)
            $handoffs += @{
                label = "Create Tasks"
                agent = "speckit.tasks"
            }
        }
        
        return $handoffs
    }
}

# Open/Closed: Workflow composer that can be extended
class SpeckitWorkflowComposer {
    [IWorkflowValidator]$Validator
    [ITemplateProcessor]$TemplateProcessor
    [IAgentContextManager]$AgentManager
    [IWorkflowOrchestrator]$Orchestrator
    
    SpeckitWorkflowComposer(
        [IWorkflowValidator]$Validator,
        [ITemplateProcessor]$TemplateProcessor,
        [IAgentContextManager]$AgentManager,
        [IWorkflowOrchestrator]$Orchestrator
    ) {
        $this.Validator = $Validator
        $this.TemplateProcessor = $TemplateProcessor
        $this.AgentManager = $AgentManager
        $this.Orchestrator = $Orchestrator
    }
    
    # Dependency Inversion: Execute specific workflow steps
    [bool] ExecuteStep([string]$StepName, [hashtable]$Parameters) {
        switch ($StepName) {
            'ValidateEnvironment' {
                return $this.Validator.ValidateEnvironment()
            }
            'SetupPlan' {
                return $this.SetupPlanStep($Parameters)
            }
            'UpdateAgentContext' {
                return $this.UpdateAgentContextStep($Parameters)
            }
            'ExecuteHandoffs' {
                return $this.Orchestrator.ExecuteHandoff($Parameters.CommandName, $Parameters.Context)
            }
            default {
                Write-Warning "Unknown workflow step: $StepName"
                return $false
            }
        }
    }
    
    [bool] SetupPlanStep([hashtable]$Parameters) {
        $context = $this.Validator.GetEnvironmentContext()
        $templatePath = Join-Path $context.REPO_ROOT '.specify/templates/plan-template.md'
        
        $variables = @{}
        if ($Parameters.ContainsKey('Variables')) {
            $variables = $Parameters.Variables
        }
        
        return $this.TemplateProcessor.ProcessTemplate($templatePath, $context.IMPL_PLAN, $variables)
    }
    
    [bool] UpdateAgentContextStep([hashtable]$Parameters) {
        $context = $this.Validator.GetEnvironmentContext()
        $planData = $this.AgentManager.ExtractPlanData($context.IMPL_PLAN)
        
        $agentTypes = @()
        if ($Parameters.ContainsKey('AgentTypes')) {
            $agentTypes = $Parameters.AgentTypes
        } else {
            $agentTypes = @('claude') # Default agent
        }
        
        $success = $true
        foreach ($agentType in $agentTypes) {
            $success = $success -and $this.AgentManager.UpdateAgentContext($agentType, $planData)
        }
        
        return $success
    }
}

# Factory for creating workflow components (Dependency Injection)
class SpeckitWorkflowFactory {
    static [SpeckitWorkflowComposer] CreateComposer([string]$RepoRoot = $null) {
        if (-not $RepoRoot) {
            $RepoRoot = (Get-Location).Path
        }
        
        $validator = [SpeckitEnvironmentValidator]::new()
        $templateProcessor = [SpeckitTemplateProcessor]::new($RepoRoot)
        $agentManager = [SpeckitAgentContextManager]::new($RepoRoot)
        $orchestrator = [SpeckitWorkflowOrchestrator]::new($RepoRoot)
        
        return [SpeckitWorkflowComposer]::new($validator, $templateProcessor, $agentManager, $orchestrator)
    }
}

# Public API - Flexible wrapper interface
class SpeckitWorkflowWrapper {
    [SpeckitWorkflowComposer]$Composer
    
    SpeckitWorkflowWrapper([string]$RepoRoot = $null) {
        $this.Composer = [SpeckitWorkflowFactory]::CreateComposer($RepoRoot)
    }
    
    # Execute individual workflow steps
    [bool] ExecuteEnvironmentValidation() {
        return $this.Composer.ExecuteStep('ValidateEnvironment', @{})
    }
    
    [bool] ExecutePlanSetup([hashtable]$Variables = @{}) {
        return $this.Composer.ExecuteStep('SetupPlan', @{ Variables = $Variables })
    }
    
    [bool] ExecuteAgentContextUpdate([array]$AgentTypes = @()) {
        return $this.Composer.ExecuteStep('UpdateAgentContext', @{ AgentTypes = $AgentTypes })
    }
    
    [bool] ExecuteHandoffs([string]$CommandName, [hashtable]$Context = @{}) {
        return $this.Composer.ExecuteStep('ExecuteHandoffs', @{ 
            CommandName = $CommandName 
            Context = $Context 
        })
    }
    
    # Execute predefined workflow combinations
    [bool] ExecutePlanWorkflow([hashtable]$Variables = @{}, [array]$AgentTypes = @('claude')) {
        if (-not $this.ExecuteEnvironmentValidation()) {
            return $false
        }
        
        if (-not $this.ExecutePlanSetup($Variables)) {
            return $false
        }
        
        if (-not $this.ExecuteAgentContextUpdate($AgentTypes)) {
            return $false
        }
        
        return $true
    }
    
    [bool] ExecuteMinimalPlanSetup() {
        return $this.ExecutePlanWorkflow(@{}, @())
    }
    
    [bool] ExecuteFullPlanWorkflow([array]$AgentTypes = @('claude', 'qwen', 'cursor-agent')) {
        return $this.ExecutePlanWorkflow(@{}, $AgentTypes)
    }
}
