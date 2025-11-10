# Central Command Registry & Propagation System

## Overview
This document outlines a centralized system for managing installation/setup commands that can be automatically propagated to new project folders.

## Architecture

### 1. Central Command Registry
```
.command-registry/
├── tools/
│   ├── qwen.json
│   ├── gemini.json
│   ├── amp.json
│   ├── cursor.json
│   ├── iflow.json
│   ├── aider.json
│   ├── llxprt.json
│   └── crush.json
├── scripts/
│   ├── propagate-commands.sh
│   ├── update-registry.sh
│   └── validate-commands.sh
└── templates/
    ├── project-init.sh
    └── command-runner.sh
```

### 2. Command Definition Format
Each tool gets a JSON configuration:

```json
{
  "name": "qwen",
  "description": "Qwen Code AI Assistant",
  "category": "ai-assistant",
  "platforms": ["linux", "macos", "windows"],
  "dependencies": ["python", "pip"],
  "install_commands": {
    "linux": [
      "pip install qwen-code",
      "qwen --setup"
    ],
    "macos": [
      "brew install qwen-code",
      "qwen --configure"
    ]
  },
  "verify_commands": [
    "qwen --version"
  ],
  "environment_variables": {
    "QWEN_API_KEY": "your_key_here"
  },
  "version": "1.0.0",
  "last_updated": "2024-12-01"
}
```

## Propagation Methods

### Method 1: Git Submodules/Hooks
```bash
# In new project directory
git submodule add <registry-repo> .command-registry
git submodule update --init --recursive

# Post-commit hook automatically propagates
#!/bin/bash
.command-registry/scripts/propagate-commands.sh
```

### Method 2: Template-Based Initialization
```bash
# Project creation script
create-new-project() {
    local project_name=$1
    local tools=("${@:2}")

    mkdir "$project_name"
    cd "$project_name"

    # Copy central registry
    cp -r /path/to/central/registry .command-registry

    # Install specified tools
    for tool in "${tools[@]}"; do
        .command-registry/scripts/install-tool.sh "$tool"
    done
}

# Usage
create-new-project "my-ai-project" qwen gemini aider
```

### Method 3: Environment-Based Auto-Propagation
```bash
# .bashrc or .zshrc addition
propagate_commands() {
    if [ -f ".command-registry/manifest.json" ]; then
        .command-registry/scripts/check-updates.sh
        .command-registry/scripts/install-missing.sh
    fi
}

# Auto-run on directory change
chpwd_functions=(${chpwd_functions[@]} propagate_commands)
```

## Implementation

### 1. Registry Management Script
```bash
#!/bin/bash
# update-registry.sh

update_tool_definition() {
    local tool_name=$1
    local new_definition=$2

    # Validate JSON
    echo "$new_definition" | jq . >/dev/null || {
        echo "Invalid JSON for $tool_name"
        return 1
    }

    # Backup old version
    cp ".command-registry/tools/${tool_name}.json" \
       ".command-registry/backup/${tool_name}.$(date +%Y%m%d_%H%M%S).json"

    # Update definition
    echo "$new_definition" > ".command-registry/tools/${tool_name}.json"

    # Update manifest
    update_manifest "$tool_name"

    echo "Updated $tool_name definition"
}

update_manifest() {
    local tool_name=$1

    # Regenerate manifest with versions
    jq -n '{
        registry_version: "1.0.0",
        last_updated: now | strftime("%Y-%m-%dT%H:%M:%SZ"),
        tools: {}
    }' > .command-registry/manifest.json

    for tool_file in .command-registry/tools/*.json; do
        tool_name=$(basename "$tool_file" .json)
        version=$(jq -r '.version' "$tool_file")
        jq --arg name "$tool_name" --arg ver "$version" \
           '.tools[$name] = $ver' .command-registry/manifest.json > tmp.json
        mv tmp.json .command-registry/manifest.json
    done
}
```

### 2. Propagation Script
```bash
#!/bin/bash
# propagate-commands.sh

propagate_to_directory() {
    local target_dir=$1

    if [ ! -d "$target_dir" ]; then
        echo "Target directory $target_dir does not exist"
        return 1
    fi

    cd "$target_dir"

    # Check if registry exists
    if [ ! -d ".command-registry" ]; then
        echo "Initializing command registry in $target_dir"
        mkdir -p .command-registry
    fi

    # Copy latest definitions
    cp -r /path/to/central/registry/tools .command-registry/
    cp -r /path/to/central/registry/scripts .command-registry/

    # Update manifest
    .command-registry/scripts/update-registry.sh

    echo "Propagated commands to $target_dir"
}

# Propagate to all subdirectories
propagate_to_all() {
    find . -maxdepth 2 -name ".git" -type d | while read -r git_dir; do
        project_dir=$(dirname "$git_dir")
        if [ "$project_dir" != "." ]; then
            propagate_to_directory "$project_dir"
        fi
    done
}
```

### 3. Auto-Installation Script
```bash
#!/bin/bash
# install-tool.sh

install_tool() {
    local tool_name=$1
    local tool_config=".command-registry/tools/${tool_name}.json"

    if [ ! -f "$tool_config" ]; then
        echo "Tool $tool_name not found in registry"
        return 1
    fi

    # Detect platform
    detect_platform

    # Check dependencies
    check_dependencies "$tool_config"

    # Install tool
    install_commands=$(jq -r ".install_commands.$PLATFORM[]" "$tool_config")

    echo "Installing $tool_name for $PLATFORM..."
    while IFS= read -r cmd; do
        if [ "$cmd" != "null" ]; then
            echo "Running: $cmd"
            eval "$cmd" || {
                echo "Failed to install $tool_name"
                return 1
            }
        fi
    done <<< "$install_commands"

    # Set environment variables
    setup_environment "$tool_config"

    # Verify installation
    verify_installation "$tool_config"

    echo "$tool_name installed successfully"
}

detect_platform() {
    case "$(uname -s)" in
        Linux*)  PLATFORM="linux" ;;
        Darwin*) PLATFORM="macos" ;;
        CYGWIN*|MINGW*) PLATFORM="windows" ;;
        *) PLATFORM="unknown" ;;
    esac
}

check_dependencies() {
    local config_file=$1
    local deps=$(jq -r '.dependencies[]' "$config_file" 2>/dev/null)

    for dep in $deps; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            echo "Missing dependency: $dep"
            echo "Please install $dep first"
            return 1
        fi
    done
}
```

## Usage Examples

### 1. Initialize New Project with Tools
```bash
# Create project with specific tools
new-project my-ai-app qwen gemini aider

# This would:
# 1. Create my-ai-app/ directory
# 2. Copy command registry
# 3. Install qwen, gemini, aider
# 4. Set up environment variables
```

### 2. Update All Projects
```bash
# Update all projects with latest commands
update-all-projects

# This would:
# 1. Find all project directories
# 2. Update their command registries
# 3. Install any new tools
```

### 3. Check Tool Versions
```bash
# Verify all tools are up to date
check-tool-versions

# This would:
# 1. Check installed versions
# 2. Compare with registry versions
# 3. Report outdated tools
```

## Benefits

1. **Centralized Management**: Single source of truth for all commands
2. **Automatic Propagation**: New projects get latest commands automatically
3. **Version Control**: Track changes to installation procedures
4. **Platform Support**: Different commands for different operating systems
5. **Dependency Management**: Automatic prerequisite checking
6. **Environment Setup**: Automatic environment variable configuration
7. **Verification**: Built-in checks to ensure successful installation

## Integration with Existing Tools

### With Task Master AI
```json
{
  "integration": {
    "task-master": {
      "auto_tasks": [
        "install-tool qwen",
        "verify-tool qwen",
        "configure-tool qwen"
      ]
    }
  }
}
```

### With Specify
```json
{
  "integration": {
    "specify": {
      "post_init_commands": [
        "propagate-commands",
        "install-required-tools"
      ]
    }
  }
}
```

This system provides a robust, scalable way to manage and distribute tool installation commands across multiple projects and environments.