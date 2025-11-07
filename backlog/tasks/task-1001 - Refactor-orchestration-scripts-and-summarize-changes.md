---
id: task-1001
title: Refactor orchestration scripts and summarize changes
status: To Do
assignee: []
created_date: '2025-11-06 03:28'
updated_date: '2025-11-06 03:32'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
This task is to summarize the changes from three recent commits and then drop them. The changes include:
- Refactoring the `cleanup_orchestration.sh` script to simplify it.
- Implementing a more robust "remote-first" hook installation in `install-hooks.sh`.
- A large documentation update to `orchestration-workflow.md`.
- A significant refactoring of the `setup/launch.py` script to improve its structure and maintainability.

**Details of changes:**

**Commit 1: refactor: Remove redundant hook cleanup from cleanup_orchestration.sh**
```diff
diff --git a/scripts/cleanup_orchestration.sh b/scripts/cleanup_orchestration.sh
index 40c2558a..b1c3f946 100755
--- a/scripts/cleanup_orchestration.sh
+++ b/scripts/cleanup_orchestration.sh
@@ -19,14 +19,6 @@ if [ "$current_branch" != "orchestration-tools" ]; then
             echo "Removed scripts/currently_disabled/ from git and working directory"
         fi
 
-        # Remove all orchestration-managed hooks to prevent mixup
-        HOOKS_TO_REMOVE=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")
-        for hook in "${HOOKS_TO_REMOVE[@]}"; do
-            if [ -f ".git/hooks/$hook" ]; then
-                rm ".git/hooks/$hook"
-                echo "Removed .git/hooks/$hook"
-            fi
-        done
-
         echo "Cleanup completed."
     else
```

**Commit 2: feat: Implement remote-first hook installation in install-hooks.sh**
```diff
diff --git a/scripts/install-hooks.sh b/scripts/install-hooks.sh
index 064678f1..08b45c77 100755
--- a/scripts/install-hooks.sh
+++ b/scripts/install-hooks.sh
@@ -26,7 +26,7 @@ source "$SCRIPT_DIR/lib/common.sh"
 
 # Configuration
 ORCHESTRATION_BRANCH="${ORCHESTRATION_BRANCH:-orchestration-tools}"
-HOOKS_DIR="scripts/hooks"
+HOOKS_RELATIVE_PATH="scripts/hooks"
 REQUIRED_HOOKS=(
     "pre-commit"
     "post-commit"
@@ -67,25 +67,35 @@ parse_install_args() {
 # Install a single hook from orchestration-tools branch
 install_hook_from_remote() {
     local hook_name=$1
-    local hook_path="$HOOKS_DIR/$hook_name"
+    local hook_path="$HOOKS_RELATIVE_PATH/$hook_name"
     local git_hook_path=".git/hooks/$hook_name"
 
     log_info "Installing hook: $hook_name"
 
-    # Check if hook exists in remote orchestration-tools
+    # Create .git/hooks directory if it doesn't exist
+    mkdir -p .git/hooks/
+
+    # Check if remote branch exists
     if ! git ls-remote --exit-code --heads origin "$ORCHESTRATION_BRANCH" >/dev/null 2>&1; then
-        log_error "Remote branch $ORCHESTRATION_BRANCH not found"
+        log_error "Remote branch $ORCHESTRATION_BRANCH not found. Cannot install hook $hook_name."
         return 1
     fi
 
     # Fetch latest from remote
     if ! git fetch origin "$ORCHESTRATION_BRANCH" --quiet 2>/dev/null; then
-        log_warn "Failed to fetch from remote $ORCHESTRATION_BRANCH"
+        log_warn "Failed to fetch from remote $ORCHESTRATION_BRANCH. May be using stale version for $hook_name."
     fi
 
     # Check if hook exists in remote branch
     if ! git ls-tree -r "origin/$ORCHESTRATION_BRANCH" --name-only | grep -q "^$hook_path$"; then
-        log_debug "Hook $hook_name not found in remote $ORCHESTRATION_BRANCH"
+        log_debug "Hook $hook_name not found in remote $ORCHESTRATION_BRANCH. Skipping."
+        return 1
+    fi
+
+    # Get remote hook content
+    local remote_hook_content=$(git show "origin/$ORCHESTRATION_BRANCH:$hook_path" 2>/dev/null)
+    if [[ -z "$remote_hook_content" ]]; then
+        log_error "Remote hook $hook_name content is empty. Skipping installation."
         return 1
     fi
 
@@ -93,7 +103,7 @@ install_hook_from_remote() {
     local needs_update=true
     if [[ -f "$git_hook_path" ]] && ! $FORCE; then
         # Compare local installed hook with remote version
-        if git diff --quiet "origin/$ORCHESTRATION_BRANCH:$hook_path" "$git_hook_path" 2>/dev/null; then
+        if [[ "$remote_hook_content" == "$(cat "$git_hook_path")" ]]; then
             log_debug "Hook $hook_name is already up to date"
             needs_update=false
         fi
@@ -102,15 +112,11 @@ install_hook_from_remote() {
     if $needs_update; then
         log_info "Updating hook: $hook_name"
 
-        # Checkout from remote branch
-        if git show "origin/$ORCHESTRATION_BRANCH:$hook_path" > "$git_hook_path" 2>/dev/null; then
-            chmod +x "$git_hook_path"
-            log_info "Successfully installed hook: $hook_name"
-            return 0
-        else
-            log_error "Failed to install hook: $hook_name"
-            return 1
-        fi
+        # Write remote hook content to local .git/hooks/
+        echo "$remote_hook_content" > "$git_hook_path" || { log_error "Failed to write hook $hook_name"; return 1; }
+        chmod +x "$git_hook_path"
+        log_info "Successfully installed hook: $hook_name"
+        return 0
     else
         log_debug "Skipping hook (up to date): $hook_name"
         return 0
@@ -119,9 +125,24 @@ install_hook_from_remote() {
 
 # Main installation function
 main() {
-    # Initialize logging manually to avoid common.sh issues
+    # Initialize logging manually to avoid common.sh issues before common.sh is sourced
+    # This part must be kept in sync with common.sh's logging setup
     LOG_LEVEL=${LOG_LEVEL:-INFO}
-    CURRENT_LOG_LEVEL=${LOG_LEVEL}
+    # Capture current log level set before potential common.sh sourcing
+    CURRENT_LOG_LEVEL_SET=$LOG_LEVEL
+
+    # Attempt to source common.sh, but only if it exists
+    if [[ -f "$SCRIPT_DIR/lib/common.sh" ]]; then
+        source "$SCRIPT_DIR/lib/common.sh"
+    else
+        # Define basic logging functions if common.sh is not available
+        log_error() { echo "[ERROR] $@" >&2; }
+        log_warn() { echo "[WARN] $@"; }
+        log_info() { if [[ "$LOG_LEVEL" == "INFO" || "$LOG_LEVEL" == "DEBUG" ]]; then echo "[INFO] $@"; fi; }
+        log_debug() { if [[ "$LOG_LEVEL" == "DEBUG" ]]; then echo "[DEBUG] $@"; fi; }
+
+        log_warn "common.sh not found. Using basic logging."
+    fi
 
     parse_install_args "$@"
 
@@ -136,6 +157,9 @@ main() {
     local installed=0
     local failed=0
 
+    # Create .git/hooks directory if it doesn't exist
+    mkdir -p .git/hooks/
+
     # Install each required hook
     for hook_name in "${REQUIRED_HOOKS[@]}"; do
         if install_hook_from_remote "$hook_name"; then
@@ -156,12 +180,12 @@ main() {
 }
 
 # Run main function
-main "$@"
+main "$@"
 \ No newline at end of file
```

**Commit 3: op**
This commit includes a large documentation update to `docs/orchestration-workflow.md` and a significant refactoring of the `setup/launch.py` script to improve its structure and maintainability. Due to the size of the diff, it is not included here.

**Changed Files:**
- `scripts/cleanup_orchestration.sh`
- `scripts/install-hooks.sh`
- `docs/orchestration-workflow.md`
- `setup/launch.py`
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Review the refactoring of the `cleanup_orchestration.sh` script.
- [ ] #2 Review the implementation of the "remote-first" hook installation in `install-hooks.sh`.

- [ ] #3 Review the documentation update to `orchestration-workflow.md`.
- [ ] #4 Review the refactoring of the `setup/launch.py` script.
<!-- AC:END -->
