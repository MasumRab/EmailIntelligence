#!/bin/bash
# Validate setup files to prevent system-breaking changes

echo "Validating setup files..."

# 1. Syntax check for Python files
for file in setup/*.py; do
  if [[ -f "$file" ]]; then
    echo "Checking syntax: $file"
    python -m py_compile "$file" || { echo "Syntax error in $file"; exit 1; }
  fi
done

# 2. Requirements check (dry-run)
if [[ -f "setup/requirements.txt" ]]; then
  echo "Checking requirements..."
  pip install --dry-run -r setup/requirements.txt >/dev/null 2>&1 || { echo "Requirements conflict"; exit 1; }
fi

# 3. Config validation (JSON)
for file in setup/*.json setup/*.yaml setup/*.yml; do
  if [[ -f "$file" ]]; then
    echo "Validating config: $file"
    if [[ "$file" == *.json ]]; then
      python -c "import json; json.load(open('$file'))" || { echo "Invalid JSON in $file"; exit 1; }
    fi
    # Add YAML validation if needed
  fi
done

# 4. Script execution test (--help)
for file in setup/*.sh setup/*.py; do
  if [[ -f "$file" && -x "$file" ]]; then
    echo "Testing script: $file"
    timeout 5s "$file" --help >/dev/null 2>&1 || { echo "Script test failed: $file"; exit 1; }
  fi
done

echo "All setup validations passed."
