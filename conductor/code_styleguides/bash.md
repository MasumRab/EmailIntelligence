# Bash Shell Scripting Style Guide

## General Principles
- **Root-Relative Execution**: All scripts should be designed to run from the project root.
- **Strict Error Handling**: Use `set -e` to exit on error and `set -u` to exit on unset variables.
- **Portability**: Prefer standard `sh` syntax where possible, but use `bash` for advanced features like arrays and local variables.

## Formatting
- **Indentation**: Use 2 spaces for indentation.
- **Shebang**: Always include a shebang line (e.g., `#!/usr/bin/env bash`).
- **Comments**: Include a header comment explaining the purpose, usage, and any dependencies.

## Naming
- **Files**: Use `snake_case` for filenames (e.g., `clean_install.sh`).
- **Variables**: Use `UPPER_CASE` for constants and `lower_case` for local variables.

## Functions
- Define functions using the `function_name() { ... }` syntax.
- Use `local` for variables within functions to prevent namespace pollution.

## Documentation
- Document all flags and arguments.
- Provide examples of common usage patterns.
