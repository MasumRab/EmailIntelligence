#!/bin/bash
# Patch must be in repo root and committed
PATCH="pr-179.patch"

# Dry-run only
if git apply --check "$PATCH" > /tmp/bisect.log 2>&1; then
  # Patch applies → GOOD
  exit 0
else
  # Patch fails → BAD
  echo "BAD: patch failed on $(git rev-parse --short HEAD)"
  cat /tmp/bisect.log
  exit 1
fi
