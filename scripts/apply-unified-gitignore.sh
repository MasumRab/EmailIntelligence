#!/usr/bin/env bash
# apply-unified-gitignore.sh
#
# Applies scripts/unified.gitignore to one or more branches, with a per-branch
# audit that detects already-tracked files which the new ignore would hide.
#
# Usage:
#   bash scripts/apply-unified-gitignore.sh --audit               # audit all branches
#   bash scripts/apply-unified-gitignore.sh --audit BRANCH...     # audit specific branches
#   bash scripts/apply-unified-gitignore.sh --apply BRANCH...     # commit on specific branches
#   bash scripts/apply-unified-gitignore.sh --apply-main-set      # main, scientific, orchestration-tools, taskmaster
#
# Safety:
#   * Never force-pushes.
#   * Audit mode is read-only.
#   * Apply mode commits locally; you must `git push` yourself.
#   * If the working tree is dirty on a target branch, that branch is skipped.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
UNIFIED="$REPO_ROOT/scripts/unified.gitignore"
MAIN_SET=(main scientific orchestration-tools taskmaster)

[ -f "$UNIFIED" ] || { echo "ERROR: $UNIFIED not found"; exit 1; }

usage() { sed -n '2,18p' "$0"; exit 1; }

mode=""
declare -a branches=()
case "${1:-}" in
  --audit)            mode="audit"; shift; branches=("$@") ;;
  --apply)            mode="apply"; shift; branches=("$@") ;;
  --apply-main-set)   mode="apply"; branches=("${MAIN_SET[@]}") ;;
  *) usage ;;
esac

# Default: all local + remote branches for audit
if [ "$mode" = "audit" ] && [ ${#branches[@]} -eq 0 ]; then
  mapfile -t branches < <(git -C "$REPO_ROOT" for-each-ref --format='%(refname:short)' refs/heads refs/remotes/origin \
                          | grep -v '^origin/HEAD$' | sort -u)
fi

ORIG_BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
if [ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]; then
  echo "ERROR: working tree is dirty. Commit or stash first." >&2
  exit 1
fi

audit_branch() {
  local b="$1"
  echo ""
  echo "=== AUDIT: $b ==="
  # List tracked files on this branch that the unified ignore would match.
  local tracked
  tracked="$(git -C "$REPO_ROOT" ls-tree -r --name-only "$b" 2>/dev/null || true)"
  [ -z "$tracked" ] && { echo "  (branch not found or empty)"; return; }
  # Use git check-ignore against unified file via temp index.
  local tmpdir; tmpdir="$(mktemp -d)"
  cp "$UNIFIED" "$tmpdir/.gitignore"
  cd "$tmpdir"
  git init -q
  local conflicts
  conflicts="$(echo "$tracked" | git check-ignore --stdin --no-index 2>/dev/null || true)"
  cd "$REPO_ROOT"
  rm -rf "$tmpdir"
  if [ -n "$conflicts" ]; then
    echo "  ⚠ The following currently-tracked files would be IGNORED by the unified .gitignore:"
    echo "$conflicts" | sed 's/^/    /'
    echo "  → Decide: (a) git rm --cached them, or (b) add a branch-specific !pattern."
  else
    echo "  ✓ No tracked files conflict with the unified .gitignore."
  fi
}

apply_branch() {
  local b="$1"
  echo ""
  echo "=== APPLY: $b ==="
  if ! git -C "$REPO_ROOT" rev-parse --verify --quiet "$b" >/dev/null; then
    echo "  skip: branch $b does not exist locally"
    return
  fi
  git -C "$REPO_ROOT" checkout -q "$b"
  cp "$UNIFIED" "$REPO_ROOT/.gitignore"
  if git -C "$REPO_ROOT" diff --quiet -- .gitignore; then
    echo "  ✓ already up to date"
    return
  fi
  git -C "$REPO_ROOT" add .gitignore
  git -C "$REPO_ROOT" commit -q -m "chore: adopt unified .gitignore baseline"
  echo "  ✓ committed (push manually when ready)"
}

for b in "${branches[@]}"; do
  case "$mode" in
    audit) audit_branch "$b" ;;
    apply) apply_branch "$b" ;;
  esac
done

git -C "$REPO_ROOT" checkout -q "$ORIG_BRANCH"
echo ""
echo "Done. Restored to: $ORIG_BRANCH"
