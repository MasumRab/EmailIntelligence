# Command Centralization & Propagation System

## Overview
A comprehensive system for centralizing tool installation commands and automatically propagating them to new project folders.

## Files Created

### 1. `setup_command_registry.md`
- Complete architectural documentation
- Implementation details
- Integration patterns

### 2. `command_registry_tools.json`
- JSON registry of all requested tools
- Platform-specific installation commands
- Environment variable configurations

### 3. `install_tools.sh`
- Executable installation script
- Cross-platform support
- Dependency checking and verification

## Available Tools & Installation Commands

### Qwen (AI Assistant)
```bash
./install_tools.sh qwen
# Installs: pip install qwen-code
# Requires: QWEN_API_KEY
```

### Gemini (Google AI)
```bash
./install_tools.sh gemini
# Installs: pip install google-genai gemini-cli
# Requires: GOOGLE_API_KEY
```

### AMP (AI Assistant)
```bash
./install_tools.sh amp
# Installs: npm install -g @amperka/amp-cli
# No API keys required
```

### Cursor (AI IDE)
```bash
./install_tools.sh cursor
# Linux: Downloads .deb package
# macOS: brew install cursor
# Windows: winget install cursor.cursor
```

### IFLOW (Workflow System)
```bash
./install_tools.sh iflow
# Installs: pip install iflow-workflow
# Local documentation: IFLOW.md
```

### Aider (AI Coding Assistant)
```bash
./install_tools.sh aider
# Installs: pip install aider-chat
# Supports: ANTHROPIC_API_KEY, OPENAI_API_KEY
```

### LLXPRT (Export Tool)
```bash
./install_tools.sh llxprt
# Installs: pip install llxprt
# Local documentation: LLXPRT.md
```

### CRUSH (Compression Tool)
```bash
./install_tools.sh crush
# Installs: pip install crush-toolkit
# Local documentation: CRUSH.md
```

## Usage Examples

### Install Single Tool
```bash
./install_tools.sh qwen
```

### Install Multiple Tools
```bash
./install_tools.sh qwen gemini aider
```

### Install All Tools
```bash
./install_tools.sh --all
```

### List Available Tools
```bash
./install_tools.sh --list
```

### Check Tool Information
```bash
# View all available tools
jq '.tools | keys[]' command_registry_tools.json

# Get specific tool details
jq '.tools.qwen' command_registry_tools.json
```

## Propagation Methods

### 1. Copy to New Projects
```bash
# When creating a new project
mkdir new-project
cd new-project
cp ../install_tools.sh .
cp ../command_registry_tools.json .

# Install required tools
./install_tools.sh qwen gemini
```

### 2. Git Submodule Approach
```bash
# Add as submodule to existing repos
git submodule add <this-repo> .tool-registry

# Propagate to new projects
./.tool-registry/install_tools.sh <tools...>
```

### 3. Template Integration
```bash
# Integrate with project templates
create-project() {
    local name=$1
    local tools=("${@:2}")

    mkdir "$name"
    cd "$name"

    # Copy tool registry
    cp /path/to/registry/* .

    # Install tools
    ./install_tools.sh "${tools[@]}"
}

# Usage
create-project "my-ai-app" qwen aider cursor
```

## System Benefits

### ✅ Centralized Management
- Single source of truth for all installation commands
- Easy updates and maintenance
- Version tracking for tool definitions

### ✅ Cross-Platform Support
- Automatic platform detection (Linux/macOS/Windows)
- Platform-specific installation commands
- Dependency checking per platform

### ✅ Automated Verification
- Post-installation verification commands
- Environment variable setup
- Dependency validation

### ✅ Easy Propagation
- Copy files to new projects
- Git submodule integration
- Template-based project creation

### ✅ Error Handling
- Comprehensive error checking
- Clear error messages
- Graceful failure handling

## Integration with Existing Systems

### Task Master AI Integration
```bash
# Task Master can now include tool installation tasks
task-master add-task "Install development tools" --prompt="
Install qwen, gemini, and aider for AI-assisted development
"
```

### Specify Integration
```bash
# Specify projects can include tool setup
specify init my-project --ai claude
cd my-project
../install_tools.sh qwen aider
```

### Worktree Propagation
```bash
# Automatically propagate to all worktrees
find . -name ".git" -type d -exec dirname {} \; | while read dir; do
    if [ "$dir" != "." ]; then
        cp install_tools.sh command_registry_tools.json "$dir/"
        echo "Propagated tools to $dir"
    fi
done
```

## Maintenance

### Adding New Tools
```bash
# Add new tool to JSON registry
jq '.tools.newtool = {
    "name": "newtool",
    "description": "New Tool Description",
    "install_commands": {
        "linux": ["command1", "command2"],
        "macos": ["command1", "command2"],
        "windows": ["command1", "command2"]
    }
}' command_registry_tools.json > temp.json && mv temp.json command_registry_tools.json
```

### Updating Tool Versions
```bash
# Update tool version
jq '.tools.qwen.version = "2.0.0"' command_registry_tools.json > temp.json && mv temp.json command_registry_tools.json
```

### Platform-Specific Commands
```bash
# Add Windows-specific commands
jq '.tools.newtool.install_commands.windows = ["windows-command"]' command_registry_tools.json > temp.json && mv temp.json command_registry_tools.json
```

This system provides a robust, scalable solution for managing tool installations across multiple projects and environments.