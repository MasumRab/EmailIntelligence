#!/bin/bash
# CLI Integration Script
# Safely integrates CLI features into other branches without interfering with existing files

set -e  # Exit on any error

# Configuration
CONFIG_FILE=".cli_framework/config.json"
BACKUP_DIR=".cli_backups"
LOG_FILE=".cli_framework/installation.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
    log "INFO: $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    log "WARNING: $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    log "ERROR: $1"
}

# Check if jq is installed
check_jq() {
    if ! command -v jq &> /dev/null; then
        print_error "jq is required but not installed. Please install jq first."
        exit 1
    fi
}

# Create backup of a file
backup_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local backup_path="${BACKUP_DIR}/$(dirname "$file" | sed 's|/|_|g')_$(basename "$file")_$(date +%s)"
        mkdir -p "$(dirname "$backup_path")"
        cp "$file" "$backup_path"
        print_status "Backed up $file to $backup_path"
    fi
}

# Install CLI components based on mode
install_cli_components() {
    local mode="${1:-minimal}"
    print_status "Installing CLI components in '$mode' mode..."
    
    case "$mode" in
        "full")
            install_full_mode
            ;;
        "minimal")
            install_minimal_mode
            ;;
        *)
            print_error "Unknown installation mode: $mode"
            exit 1
            ;;
    esac
}

# Full installation mode
install_full_mode() {
    print_status "Installing in full mode..."
    
    # Create directories if they don't exist
    mkdir -p src/analysis/constitutional
    mkdir -p src/core
    mkdir -p src/git
    mkdir -p src/resolution
    mkdir -p src/strategy
    mkdir -p src/validation
    mkdir -p src/utils
    
    # Copy all components
    copy_component "emailintelligence_cli.py" "." "CLI main entry point"
    copy_component "src/resolution/__init__.py" "src/resolution/" "Constitutional engine"
    copy_component "src/git/conflict_detector.py" "src/git/" "Git conflict detection"
    copy_component "src/analysis/conflict_analyzer.py" "src/analysis/" "Conflict analysis"
    copy_component "src/core/conflict_models.py" "src/core/" "Conflict models"
    copy_component "src/analysis/constitutional/analyzer.py" "src/analysis/constitutional/" "Constitutional analyzer"
    copy_component "src/core/interfaces.py" "src/core/" "Core interfaces"
    copy_component "src/core/exceptions.py" "src/core/" "Core exceptions"
    copy_component "src/git/repository.py" "src/git/" "Repository operations"
    copy_component "src/resolution/auto_resolver.py" "src/resolution/" "Auto resolver"
    copy_component "src/resolution/semantic_merger.py" "src/resolution/" "Semantic merger"
    copy_component "src/strategy/generator.py" "src/strategy/" "Strategy generator"
    copy_component "src/strategy/risk_assessor.py" "src/strategy/" "Risk assessor"
    copy_component "src/validation/validator.py" "src/validation/" "Validator"
    copy_component "src/utils/logger.py" "src/utils/" "Logger utilities"
    
    print_status "Full installation completed!"
}

# Minimal installation mode
install_minimal_mode() {
    print_status "Installing in minimal mode..."
    
    # Create directories if they don't exist
    mkdir -p src/resolution
    mkdir -p src/git
    mkdir -p src/analysis
    mkdir -p src/core
    
    # Copy only essential components
    copy_component "emailintelligence_cli.py" "." "CLI main entry point"
    copy_component "src/resolution/__init__.py" "src/resolution/" "Constitutional engine"
    copy_component "src/git/conflict_detector.py" "src/git/" "Git conflict detection"
    copy_component "src/analysis/conflict_analyzer.py" "src/analysis/" "Conflict analysis"
    copy_component "src/core/conflict_models.py" "src/core/" "Conflict models"
    
    print_status "Minimal installation completed!"
}

# Copy a component with backup
copy_component() {
    local source="$1"
    local dest_dir="$2"
    local description="$3"
    
    if [[ -f "$source" ]]; then
        local dest_file="$dest_dir$(basename "$source")"
        backup_file "$dest_file"
        cp "$source" "$dest_file"
        print_status "Installed $description: $dest_file"
    else
        print_warning "Component file does not exist: $source"
    fi
}

# Check for conflicts with existing files
check_conflicts() {
    print_status "Checking for potential conflicts..."
    
    # This is a simplified check - in a real implementation, you'd want more sophisticated conflict detection
    if [[ -f "emailintelligence_cli.py" ]] && [[ ! -f ".original_emailintelligence_cli.py" ]]; then
        print_warning "emailintelligence_cli.py already exists. It will be backed up during installation."
    fi
}

# Main function
main() {
    print_status "Starting EmailIntelligence CLI Framework installation..."
    
    # Initialize
    mkdir -p "$BACKUP_DIR"
    touch "$LOG_FILE"
    
    # Check prerequisites
    check_jq
    
    # Parse arguments
    local mode="minimal"
    if [[ $# -gt 0 ]]; then
        mode="$1"
    fi
    
    # Check for conflicts
    check_conflicts
    
    # Install components
    install_cli_components "$mode"
    
    print_status "Installation completed successfully!"
    print_status "Log file: $LOG_FILE"
    print_status "Backups are stored in: $BACKUP_DIR"
}

# Run main function with arguments
main "$@"