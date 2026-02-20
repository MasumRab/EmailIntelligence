#!/usr/bin/env pwsh
<#
.SYNOPSIS
CLI interface for the Speckit Workflow Wrapper

.DESCRIPTION
Provides command-line access to modular Speckit workflow components.
Allows selective execution of workflow parts as needed.

.PARAMETER Action
The workflow action to execute (Validate, SetupPlan, UpdateContext, FullWorkflow, MinimalSetup)

.PARAMETER AgentTypes
Comma-separated list of agent types to update (claude,qwen,cursor-agent,etc.)

.PARAMETER Variables
Hashtable of template variables in format "key1=value1,key2=value2"

.PARAMETER RepoRoot
Repository root path (defaults to current directory)

.EXAMPLE
./SpeckitWorkflowCLI.ps1 -Action Validate

.EXAMPLE
./SpeckitWorkflowCLI.ps1 -Action SetupPlan -Variables "PROJECT NAME=MyFeature,DATE=2025-01-15"

.EXAMPLE
./SpeckitWorkflowCLI.ps1 -Action UpdateContext -AgentTypes "claude,qwen"

.EXAMPLE
./SpeckitWorkflowCLI.ps1 -Action FullWorkflow -AgentTypes "claude,qwen,cursor-agent"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('Validate', 'SetupPlan', 'UpdateContext', 'ExecuteHandoffs', 'FullWorkflow', 'MinimalSetup')]
    [string]$Action,
    
    [string]$AgentTypes = "",
    
    [string]$Variables = "",
    
    [string]$RepoRoot = "",
    
    [string]$CommandName = "",
    
    [switch]$Json,
    
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Output "Speckit Workflow CLI - Modular execution of Speckit orchestration components"
    Write-Output ""
    Write-Output "Actions:"
    Write-Output "  Validate        - Validate environment (git branch, paths)"
    Write-Output "  SetupPlan       - Setup implementation plan from template"
    Write-Output "  UpdateContext   - Update agent context files"
    Write-Output "  ExecuteHandoffs - Execute workflow handoffs"
    Write-Output "  FullWorkflow    - Execute complete plan workflow"
    Write-Output "  MinimalSetup    - Execute minimal plan setup only"
    Write-Output ""
    Write-Output "Parameters:"
    Write-Output "  -AgentTypes     Comma-separated agent types (claude,qwen,cursor-agent,etc.)"
    Write-Output "  -Variables      Template variables (key1=value1,key2=value2)"
    Write-Output "  -RepoRoot       Repository root path (default: current directory)"
    Write-Output "  -CommandName    Command name for handoff execution"
    Write-Output "  -Json           Output results in JSON format"
    Write-Output "  -Help           Show this help message"
    Write-Output ""
    Write-Output "Examples:"
    Write-Output "  ./SpeckitWorkflowCLI.ps1 -Action Validate"
    Write-Output "  ./SpeckitWorkflowCLI.ps1 -Action SetupPlan -Variables 'PROJECT NAME=MyFeature'"
    Write-Output "  ./SpeckitWorkflowCLI.ps1 -Action UpdateContext -AgentTypes 'claude,qwen'"
    Write-Output "  ./SpeckitWorkflowCLI.ps1 -Action FullWorkflow -AgentTypes 'claude,qwen'"
    exit 0
}

# Import the workflow wrapper
$wrapperPath = Join-Path $PSScriptRoot 'SpeckitWorkflowWrapper.ps1'
. $wrapperPath

# Parse parameters
$parsedAgentTypes = @()
if ($AgentTypes) {
    $parsedAgentTypes = $AgentTypes -split ',' | ForEach-Object { $_.Trim() }
}

$parsedVariables = @{}
if ($Variables) {
    $Variables -split ',' | ForEach-Object {
        $parts = $_ -split '=', 2
        if ($parts.Count -eq 2) {
            $parsedVariables[$parts[0].Trim()] = $parts[1].Trim()
        }
    }
}

# Initialize wrapper
$wrapper = [SpeckitWorkflowWrapper]::new($RepoRoot)

# Execute requested action
$result = $false
$outputData = @{}

try {
    switch ($Action) {
        'Validate' {
            $result = $wrapper.ExecuteEnvironmentValidation()
            $outputData['Validated'] = $result
            $outputData['Message'] = if ($result) { "Environment validation passed" } else { "Environment validation failed" }
        }
        
        'SetupPlan' {
            $result = $wrapper.ExecutePlanSetup($parsedVariables)
            $outputData['PlanSetup'] = $result
            $outputData['VariablesUsed'] = $parsedVariables.Keys -join ', '
            $outputData['Message'] = if ($result) { "Plan setup completed" } else { "Plan setup failed" }
        }
        
        'UpdateContext' {
            if ($parsedAgentTypes.Count -eq 0) {
                $parsedAgentTypes = @('claude') # Default
            }
            $result = $wrapper.ExecuteAgentContextUpdate($parsedAgentTypes)
            $outputData['ContextUpdated'] = $result
            $outputData['AgentTypes'] = $parsedAgentTypes -join ', '
            $outputData['Message'] = if ($result) { "Agent context updated" } else { "Agent context update failed" }
        }
        
        'ExecuteHandoffs' {
            if (-not $CommandName) {
                throw "CommandName is required for ExecuteHandoffs action"
            }
            $result = $wrapper.ExecuteHandoffs($CommandName, $parsedVariables)
            $outputData['HandoffsExecuted'] = $result
            $outputData['CommandName'] = $CommandName
            $outputData['Message'] = if ($result) { "Handoffs executed" } else { "Handoff execution failed" }
        }
        
        'FullWorkflow' {
            if ($parsedAgentTypes.Count -eq 0) {
                $parsedAgentTypes = @('claude', 'qwen', 'cursor-agent')
            }
            $result = $wrapper.ExecuteFullPlanWorkflow($parsedAgentTypes)
            $outputData['WorkflowCompleted'] = $result
            $outputData['AgentTypes'] = $parsedAgentTypes -join ', '
            $outputData['Message'] = if ($result) { "Full workflow completed" } else { "Full workflow failed" }
        }
        
        'MinimalSetup' {
            $result = $wrapper.ExecuteMinimalPlanSetup()
            $outputData['MinimalSetup'] = $result
            $outputData['Message'] = if ($result) { "Minimal setup completed" } else { "Minimal setup failed" }
        }
    }
    
    # Output results
    if ($Json) {
        $outputData['Success'] = $result
        $outputData['Timestamp'] = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
        $outputData | ConvertTo-Json -Depth 10
    } else {
        Write-Output "Action: $Action"
        Write-Output "Result: $result"
        Write-Output "Message: $($outputData['Message'])"
        
        if ($parsedAgentTypes.Count -gt 0) {
            Write-Output "Agent Types: $($parsedAgentTypes -join ', ')"
        }
        
        if ($parsedVariables.Count -gt 0) {
            Write-Output "Variables Used: $($parsedVariables.Keys -join ', ')"
        }
        
        if ($CommandName) {
            Write-Output "Command: $CommandName"
        }
        
        exit (if ($result) { 0 } else { 1 })
    }
    
} catch {
    $errorData = @{
        Success = $false
        Action = $Action
        Error = $_.Exception.Message
        Timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    }
    
    if ($Json) {
        $errorData | ConvertTo-Json -Depth 10
    } else {
        Write-Error "Error executing $Action`: $($_.Exception.Message)"
    }
    exit 1
}
