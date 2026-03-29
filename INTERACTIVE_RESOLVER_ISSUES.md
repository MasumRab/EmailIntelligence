# interactive_stash_resolver.sh - Issues Report

## Critical Issues

### 1. **`set -e` Prevents Proper Error Handling (Line 5)**
**Problem:** Script exits on ANY error, including expected failures
```bash
set -e  # This causes script to exit on:
# - User choosing "Skip this file" (return 1)
# - Failed git operations (expected in some cases)
```

**Impact:** 
- If user skips a file (choice 5), script exits instead of continuing
- Function returns fail with "set -e", terminating execution
- Cannot gracefully handle partial conflicts

**Fix:** Remove `set -e` and add explicit error checking

---

### 2. **Missing Stash Reference Validation (Line 155)**
**Problem:** No validation that stash exists before attempting to use it
```bash
STASH_REF="$1"  # Could be invalid, empty, or non-existent
show_stash_info "$STASH_REF"  # Fails silently or with confusing error
```

**Impact:**
- User won't know stash is invalid until deep in execution
- `git stash show` commands will fail cryptically

**Fix:** Validate stash exists with `git rev-parse "$STASH_REF" > /dev/null 2>&1`

---

### 3. **Incomplete Conflict Marker Cleanup (Line 62)**
**Problem:** `sed` command only removes marker lines, not conflict content
```bash
sed -i '/^<<<<<<< /d; /^=======/d; /^>>>>>>> /d' "$file"
# Removes: <<<<<<< HEAD
#          =======
#          >>>>>>> branch
# BUT: Keeps both conflicting sections, just without markers
```

**Impact:** Keeps both versions of conflicting code without markers, creating broken file

**Fix:** Need to keep content between markers, not just remove markers

---

### 4. **Unquoted Variable in Loop (Line 125)**
**Problem:** `git add $modified_files` expands unquoted, fails with spaces
```bash
modified_files=$(git diff --name-only --diff-filter=AM)
git add $modified_files  # Breaks if filenames have spaces
```

**Impact:** Files with spaces in names won't be added

**Fix:** Use `git add $modified_files` with proper quoting or array

---

### 5. **No Validation of Editor Exit Status (Line 67-70)**
**Problem:** User exits editor with error code, script doesn't check
```bash
${EDITOR:-vi} "$file"  # User might exit with error
echo "Please resolve the conflicts and press Enter..."
read -r _  # Always continues regardless of editor success
git add "$file"  # Might add unresolved conflicts
```

**Impact:** Unresolved conflicts get added without warning

**Fix:** Check editor exit status: `${EDITOR:-vi} "$file" || return 1`

---

### 6. **Misleading "Accept All Ours" Message (Lines 54-57)**
**Problem:** Comment says "current branch" but behavior is opposite
```bash
2)
    echo "Accepting all 'ours' changes (current branch)"
    git checkout --ours "$file"  # Actually takes working tree version
```

**Impact:** User confused about which version they're choosing

**Fix:** Clarify in message what --ours and --theirs actually mean

---

### 7. **No Handling for Files Already Staged (Line 101)**
**Problem:** `git add -A` adds everything, including unresolved conflicts
```bash
if git stash apply "$stash_ref" 2>/dev/null; then
    git add -A  # Stages everything, including conflicts
    return 0
```

**Impact:** Conflicts can be staged and committed without user noticing

**Fix:** Run `git status` check before staging

---

### 8. **Interactive Resolver Path in Other Scripts**
**Problem:** `stash_manager_optimized.sh` calls this with --preview flag that doesn't exist
```bash
# Line 224 in handle_stashes_optimized.sh:
"$interactive_script" --preview "stash@{$stash_index}"  # --preview not implemented
```

**Impact:** Script fails with unrecognized argument

**Fix:** Remove --preview or implement it

---

## Summary of Errors

| Error | Severity | Type | Location |
|-------|----------|------|----------|
| `set -e` interference | Critical | Logic | Line 5 |
| Missing stash validation | Critical | Validation | Line 155 |
| Incomplete conflict cleanup | High | Logic | Line 62 |
| Unquoted variable expansion | High | Syntax | Line 125 |
| No editor validation | Medium | Logic | Line 67-70 |
| Misleading messages | Medium | UX | Line 54-57 |
| Premature staging | High | Logic | Line 101 |
| Invalid flag in caller | Critical | Compatibility | External |

---

## Files Affected

1. `scripts/interactive_stash_resolver.sh` - All 8 issues
2. `scripts/handle_stashes_optimized.sh` - Calls with invalid --preview flag (line 224)

## Recommended Actions

1. **Immediate:** Remove `set -e`, add proper error handling
2. **High Priority:** Fix conflict marker cleanup logic
3. **High Priority:** Add stash validation at startup
4. **Medium Priority:** Fix unquoted variables and editor validation
5. **Medium Priority:** Update messages for clarity
6. **Low Priority:** Remove --preview flag from callers
