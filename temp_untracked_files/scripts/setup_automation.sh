#!/bin/bash
# Setup script for automated documentation synchronization

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the project root
if [[ ! -d "$PROJECT_ROOT/.git" ]]; then
    print_error "Not in project root directory"
    exit 1
fi

print_status "Setting up automated documentation synchronization..."

# Create necessary directories
print_status "Creating log and metrics directories..."
mkdir -p "$PROJECT_ROOT/logs"

# Install git hooks
print_status "Installing git hooks..."
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
POST_COMMIT_HOOK="$HOOKS_DIR/post-commit"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"

if [[ -f "$POST_COMMIT_HOOK" ]]; then
    print_warning "Post-commit hook already exists, backing up..."
    cp "$POST_COMMIT_HOOK" "$POST_COMMIT_HOOK.backup.$(date +%Y%m%d_%H%M%S)"
fi

if [[ -f "$PRE_COMMIT_HOOK" ]]; then
    print_warning "Pre-commit hook already exists, backing up..."
    cp "$PRE_COMMIT_HOOK" "$PRE_COMMIT_HOOK.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create the post-commit hook
cat > "$POST_COMMIT_HOOK" << EOF
#!/bin/bash
# Git post-commit hook for documentation synchronization

SCRIPT_DIR="$SCRIPT_DIR"
PROJECT_ROOT="$PROJECT_ROOT"

# Check if this is a documentation-related commit
if git diff-tree --no-commit-id --name-only HEAD | grep -q "^docs/\|^backlog/"; then
    echo "Documentation changes detected, running sync..."

    # Run the sync script
    if python "\$SCRIPT_DIR/auto_sync_docs.py" --run-once; then
        echo "Documentation sync completed successfully"
    else
        echo "Warning: Documentation sync failed"
    fi
else
    echo "No documentation changes detected, skipping sync"
fi
EOF

chmod +x "$POST_COMMIT_HOOK"
print_success "Installed post-commit git hook"

# Create the pre-commit hook
cat > "$PRE_COMMIT_HOOK" << EOF
#!/bin/bash
# Pre-commit hook to check for misplaced documentation files

SCRIPT_DIR="$SCRIPT_DIR"
PROJECT_ROOT="$PROJECT_ROOT"

# Run the pre-commit check script
"\$SCRIPT_DIR/pre-commit-docs-check"
EOF

chmod +x "$PRE_COMMIT_HOOK"
print_success "Installed pre-commit git hook"

# Create systemd service file (optional)
if command -v systemctl &> /dev/null; then
    print_status "Creating systemd service for scheduled sync..."

    SERVICE_FILE="/etc/systemd/system/docs-sync.service"
    TIMER_FILE="/etc/systemd/system/docs-sync.timer"

    # Create service file
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Automated Documentation Sync
After=network.target

[Service]
Type=oneshot
User=$(whoami)
WorkingDirectory=$PROJECT_ROOT
ExecStart=$SCRIPT_DIR/auto_sync_docs.py --run-once
EOF

    # Create timer file
    sudo tee "$TIMER_FILE" > /dev/null << EOF
[Unit]
Description=Run documentation sync daily
Requires=docs-sync.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

    sudo systemctl daemon-reload
    print_success "Created systemd service and timer"
    print_status "To enable: sudo systemctl enable docs-sync.timer"
    print_status "To start: sudo systemctl start docs-sync.timer"
fi

# Create cron job as alternative
print_status "Setting up cron job for scheduled sync..."
CRON_JOB="0 2 * * * cd $PROJECT_ROOT && $SCRIPT_DIR/auto_sync_docs.py --run-once"

if ! crontab -l 2>/dev/null | grep -q "auto_sync_docs.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    print_success "Added cron job for daily sync at 2:00 AM"
else
    print_warning "Cron job already exists"
fi

# Test the setup
print_status "Testing setup..."
if python "$SCRIPT_DIR/auto_sync_docs.py" --run-once; then
    print_success "Setup test passed"
else
    print_error "Setup test failed"
    exit 1
fi

print_success "Automated documentation synchronization setup complete!"
echo ""
echo "What's been set up:"
echo "  - Git post-commit hook for automatic sync on documentation changes"
echo "  - Cron job for daily sync at 2:00 AM"
if command -v systemctl &> /dev/null; then
    echo "  - Systemd service and timer (enable with: sudo systemctl enable docs-sync.timer)"
fi
echo "  - Log files in logs/docs_sync.log"
echo "  - Metrics in logs/docs_sync_metrics.json"
echo ""
echo "To run manual sync: python scripts/auto_sync_docs.py --run-once"
echo "To start scheduler: python scripts/auto_sync_docs.py --schedule"