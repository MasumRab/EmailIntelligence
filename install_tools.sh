#!/bin/bash
set -e

# Centralized Tool Installation Script
# Usage: ./install_tools.sh [tool1] [tool2] ...

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGISTRY_FILE="$SCRIPT_DIR/command_registry_tools.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

detect_platform() {
    case "$(uname -s)" in
        Linux*)  PLATFORM="linux" ;;
        Darwin*) PLATFORM="macos" ;;
        CYGWIN*|MINGW*) PLATFORM="windows" ;;
        *) PLATFORM="unknown" ;;
    esac
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    local tool_name=$1

    # Check if jq is available
    if ! command -v jq >/dev/null 2>&1; then
        log_error "jq is required but not installed. Please install jq first."
        return 1
    fi

    # Check if tool exists in registry
    if ! jq -e ".tools.$tool_name" "$REGISTRY_FILE" >/dev/null 2>&1; then
        log_error "Tool '$tool_name' not found in registry"
        return 1
    fi

    # Check tool dependencies
    local deps=$(jq -r ".tools.$tool_name.dependencies[]" "$REGISTRY_FILE" 2>/dev/null)
    for dep in $deps; do
        if [ "$dep" != "null" ] && [ -n "$dep" ]; then
            if ! command -v "$dep" >/dev/null 2>&1; then
                log_error "Missing dependency: $dep (required for $tool_name)"
                log_info "Please install $dep first, then re-run this script"
                return 1
            fi
        fi
    done
}

install_tool() {
    local tool_name=$1

    log_info "Installing $tool_name..."

    # Get installation commands for current platform
    local commands=$(jq -r ".tools.$tool_name.install_commands.$PLATFORM[]" "$REGISTRY_FILE" 2>/dev/null)

    if [ "$commands" = "null" ] || [ -z "$commands" ]; then
        log_error "No installation commands found for $tool_name on $PLATFORM"
        return 1
    fi

    # Execute each command
    echo "$commands" | while IFS= read -r cmd; do
        if [ "$cmd" != "null" ] && [ -n "$cmd" ]; then
            log_info "Running: $cmd"
            if eval "$cmd"; then
                log_success "Command completed successfully"
            else
                log_error "Failed to execute: $cmd"
                return 1
            fi
        fi
    done

    # Set up environment variables if any
    setup_environment "$tool_name"

    # Verify installation
    verify_installation "$tool_name"

    log_success "$tool_name installed successfully"
}

setup_environment() {
    local tool_name=$1

    # Get environment variables
    local env_vars=$(jq -r ".tools.$tool_name.environment_variables | to_entries[] | select(.value != \"\") | \"export \(.key)=\\\"\(.value)\\\"\"" "$REGISTRY_FILE" 2>/dev/null)

    if [ -n "$env_vars" ]; then
        log_info "Setting up environment variables for $tool_name..."
        echo "$env_vars" | while IFS= read -r env_cmd; do
            if [ "$env_cmd" != "null" ] && [ -n "$env_cmd" ]; then
                eval "$env_cmd"
                log_success "Set: $env_cmd"
            fi
        done

        # Suggest adding to shell profile
        log_warning "Consider adding these environment variables to your shell profile (~/.bashrc, ~/.zshrc, etc.)"
    fi
}

verify_installation() {
    local tool_name=$1

    # Get verification commands
    local verify_cmds=$(jq -r ".tools.$tool_name.verify_commands[]" "$REGISTRY_FILE" 2>/dev/null)

    if [ -n "$verify_cmds" ] && [ "$verify_cmds" != "null" ]; then
        log_info "Verifying $tool_name installation..."
        echo "$verify_cmds" | while IFS= read -r cmd; do
            if [ "$cmd" != "null" ] && [ -n "$cmd" ]; then
                if eval "$cmd" >/dev/null 2>&1; then
                    log_success "Verification passed: $cmd"
                else
                    log_warning "Verification failed: $cmd"
                fi
            fi
        done
    fi
}

show_available_tools() {
    echo -e "${BLUE}Available tools:${NC}"
    jq -r '.tools | keys[]' "$REGISTRY_FILE" 2>/dev/null | while read -r tool; do
        local desc=$(jq -r ".tools.$tool.description" "$REGISTRY_FILE" 2>/dev/null)
        local category=$(jq -r ".tools.$tool.category" "$REGISTRY_FILE" 2>/dev/null)
        echo -e "  ${GREEN}$tool${NC} - $desc (${category})"
    done
}

show_usage() {
    echo "Centralized Tool Installation Script"
    echo ""
    echo "Usage: $0 [tool1] [tool2] ..."
    echo ""
    echo "Options:"
    echo "  --list, -l    Show available tools"
    echo "  --help, -h    Show this help message"
    echo "  --all         Install all available tools"
    echo ""
    echo "Examples:"
    echo "  $0 qwen                    # Install Qwen"
    echo "  $0 qwen gemini aider      # Install multiple tools"
    echo "  $0 --all                   # Install all tools"
    echo "  $0 --list                  # Show available tools"
    echo ""
    show_available_tools
}

main() {
    detect_platform
    log_info "Detected platform: $PLATFORM"

    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi

    case "$1" in
        --help|-h)
            show_usage
            exit 0
            ;;
        --list|-l)
            show_available_tools
            exit 0
            ;;
        --all)
            # Get all tool names
            local all_tools=$(jq -r '.tools | keys[]' "$REGISTRY_FILE" 2>/dev/null)
            set -- $all_tools
            ;;
    esac

    for tool in "$@"; do
        if [[ "$tool" == --* ]]; then
            continue
        fi

        if check_dependencies "$tool"; then
            install_tool "$tool" || log_error "Failed to install $tool"
        fi
    done

    log_success "Installation process completed"
}

main "$@"