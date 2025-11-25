#!/bin/bash
# Orchestration Files Change Monitoring Script
# This script monitors key orchestration files during the alignment process

echo "=== ORCHESTRATION FILES MONITORING SCRIPT ==="
echo "Running pre-alignment safety checks..."
echo ""

# Define critical orchestration files to monitor
CRITICAL_FILES=(
    "setup/launch.py"
    "launch.py"
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    "src/agents/"
    "src/core/context_control/"
    "src/context_control/"
    "src/core/database.py"
    ".env"
    "config/"
    ".taskmaster/"
    "scripts/"
)

# Function to check for missing critical files
check_missing_files() {
    echo "Checking for missing critical orchestration files/directories..."
    local missing_files=()
    
    for file in "${CRITICAL_FILES[@]}"; do
        if [[ -n "$file" ]]; then
            if [[ -f "$file" && ! -e "$file" ]]; then
                missing_files+=("$file")
            elif [[ -d "$file" && ! -d "${file%/}" ]]; then
                missing_files+=("$file")
            fi
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo "❌ CRITICAL: Missing orchestration files/directories detected:"
        for missing in "${missing_files[@]}"; do
            echo "   - $missing"
        done
        echo ""
        echo "ACTION REQUIRED: These critical orchestration files are missing!"
        return 1
    else
        echo "✅ No critical orchestration files are missing"
        echo ""
        return 0
    fi
}

# Function to check for import statement integrity
check_import_statements() {
    echo "Checking for critical import statement integrity..."
    
    local import_issues=()
    
    if [[ -f "setup/launch.py" ]]; then
        # Check if launch.py has critical imports
        if ! grep -q "import.*config\|from.*config" "setup/launch.py" 2>/dev/null && ! grep -q "import.*environment\|from.*environment" "setup/launch.py" 2>/dev/null; then
            import_issues+=("setup/launch.py may be missing critical config/environment imports")
        fi
    fi
    
    if [[ -f "launch.py" ]]; then
        # Check if wrapper has proper forwarding
        if ! grep -q "setup.launch\|setup/launch" "launch.py" 2>/dev/null; then
            import_issues+=("launch.py may be missing proper forwarding to setup/launch.py")
        fi
    fi
    
    if [ ${#import_issues[@]} -gt 0 ]; then
        echo "⚠️  Potential import statement issues detected:"
        for issue in "${import_issues[@]}"; do
            echo "   - $issue"
        done
        echo ""
    else
        echo "✅ Import statements appear intact in orchestration files"
        echo ""
    fi
}

# Function to check launch functionality
check_launch_functionality() {
    echo "Testing basic launch functionality..."
    
    if [[ -f "launch.py" ]]; then
        echo "Found launch.py, testing basic import..."
        python -c "import sys; sys.path.insert(0, '.'); import launch; print('Launch module imports successfully')" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Launch module imports successfully"
        else
            echo "❌ CRITICAL: Launch module fails to import - orchestration functionality broken"
            echo ""
            return 1
        fi
    else
        echo "⚠️  launch.py not found, checking for launch in setup/"
        if [[ -f "setup/launch.py" ]]; then
            python -c "import sys; sys.path.insert(0, './setup'); import launch; print('Setup launch module imports successfully')" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "✅ Setup launch module imports successfully"
            else
                echo "❌ CRITICAL: Setup launch module fails to import - orchestration functionality broken"
                echo ""
                return 1
            fi
        else
            echo "❌ CRITICAL: No launch.py found in either root or setup/ - orchestration system may be broken"
            echo ""
            return 1
        fi
    fi
    echo ""
    return 0
}

# Function to check for critical configuration files
check_config_files() {
    echo "Checking for critical configuration files..."
    
    local config_issues=()
    
    # Check for project configuration
    if [[ ! -f "pyproject.toml" ]]; then
        config_issues+=("pyproject.toml missing - project configuration incomplete")
    fi
    
    # Check for environment configuration
    if [[ ! -f ".env" ]] && [[ ! -f ".env.example" ]] && [[ ! -f ".env.template" ]]; then
        config_issues+=(".env or template missing - environment configuration incomplete")
    fi
    
    # Check for database configuration
    if [[ ! -f "src/core/database.py" ]]; then
        config_issues+=("src/core/database.py missing - database orchestration broken")
    fi
    
    if [ ${#config_issues[@]} -gt 0 ]; then
        echo "❌ Configuration issues detected:"
        for issue in "${config_issues[@]}"; do
            echo "   - $issue"
        done
        echo ""
        return 1
    else
        echo "✅ Critical configuration files present"
        echo ""
        return 0
    fi
}

# Function to check agent directory integrity
check_agents_directory() {
    echo "Checking agent directory integrity..."
    
    local agent_issues=()
    
    if [[ -d "src/agents" ]]; then
        # Check if agents directory has expected structure
        if [[ ! -f "src/agents/__init__.py" ]]; then
            agent_issues+=("src/agents/__init__.py missing - agents module broken")
        fi
        
        if [[ ! -d "src/agents/core" ]] && [[ ! -f "src/agents/core.py" ]]; then
            # Look for any core agent functionality
            agent_core_found=$(find "src/agents" -name "*.py" -exec grep -l "class.*Agent\|def.*agent\|Agent.*=" {} \; 2>/dev/null | head -1)
            if [ -z "$agent_core_found" ]; then
                agent_issues+=("No core agent functionality found in src/agents - critical functionality may be missing")
            fi
        fi
    else
        echo "⚠️  src/agents directory not found"
    fi
    
    if [ ${#agent_issues[@]} -gt 0 ]; then
        echo "❌ Agent directory issues detected:"
        for issue in "${agent_issues[@]}"; do
            echo "   - $issue"
        done
        echo ""
        return 1
    else
        echo "✅ Agent directory appears intact"
        echo ""
        return 0
    fi
}

# Function to check context control integrity
check_context_control() {
    echo "Checking context control integrity..."
    
    local context_issues=()
    
    if [[ -d "src/core/context_control" ]]; then
        local context_dir="src/core/context_control"
        
        if [[ -n "$context_dir" ]]; then
            if [[ ! -f "$context_dir/__init__.py" ]]; then
                context_issues+=("$context_dir/__init__.py missing - context control module broken")
            fi
            
            # Look for key context control functionality
            local controller_file=$(find "$context_dir" -name "*.py" -exec grep -l "ContextController\|context.*control\|isolation" {} \; 2>/dev/null | head -1)
            if [ -z "$controller_file" ]; then
                context_issues+=("No context controller functionality found in $context_dir - context isolation may be broken")
            fi
        fi
    elif [[ -d "src/context_control" ]]; then
        local context_dir="src/context_control"
        
        if [[ -n "$context_dir" ]]; then
            if [[ ! -f "$context_dir/__init__.py" ]]; then
                context_issues+=("$context_dir/__init__.py missing - context control module broken")
            fi
            
            # Look for key context control functionality
            local controller_file=$(find "$context_dir" -name "*.py" -exec grep -l "ContextController\|context.*control\|isolation" {} \; 2>/dev/null | head -1)
            if [ -z "$controller_file" ]; then
                context_issues+=("No context controller functionality found in $context_dir - context isolation may be broken")
            fi
        fi
    else
        echo "⚠️  No context control directory found"
    fi
    
    if [ ${#context_issues[@]} -gt 0 ]; then
        echo "❌ Context control issues detected:"
        for issue in "${context_issues[@]}"; do
            echo "   - $issue"
        done
        echo ""
        return 1
    else
        echo "✅ Context control appears intact"
        echo ""
        return 0
    fi
}

# Run all checks
echo "Running orchestration files safety checks..."
echo "============================================"

overall_status=0

if ! check_missing_files; then
    overall_status=1
fi

check_import_statements

if ! check_launch_functionality; then
    overall_status=1
fi

if ! check_config_files; then
    overall_status=1
fi

if ! check_agents_directory; then
    overall_status=1
fi

if ! check_context_control; then
    overall_status=1
fi

echo "============================================"
if [ $overall_status -eq 0 ]; then
    echo "✅ All orchestration safety checks PASSED"
    echo "Proceeding with alignment process..."
else
    echo "❌ CRITICAL ORCHESTRATION ISSUES DETECTED"
    echo "STOPPING alignment process until issues are resolved!"
    echo "Please verify the orchestration system before continuing."
    exit 1
fi

echo ""
echo "=== MONITORING CHECKLIST FOR ALIGNMENT PROCESS ==="
echo ""
echo "BEFORE EACH MAJOR ALIGNMENT OPERATION:"
echo "- [ ] Verify this script passes without errors"
echo "- [ ] Confirm launch.py functionality works"
echo "- [ ] Check that agents directory is intact"
echo "- [ ] Validate context control functionality"
echo ""
echo "DURING CONFLICT RESOLUTION:"
echo "- [ ] Never remove orchestration functionality during conflict resolution"
echo "- [ ] When resolving conflicts, favor keeping orchestration code"
echo "- [ ] Test orchestration functionality after resolving conflicts"
echo ""
echo "AFTER EACH MAJOR OPERATION:"
echo "- [ ] Re-run this script to verify integrity"
echo "- [ ] Test launch functionality"
echo "- [ ] Verify agent and context control still work"
echo ""