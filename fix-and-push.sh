#!/bin/bash
git config --global user.email "jules@example.com"
git config --global user.name "Jules"
git add src/validation/quick_validator.py src/validation/standard_validator.py src/validation/comprehensive_validator.py src/validation/quality_checker.py src/cli/commands/resolve_command.py src/resolution/auto_resolver.py src/backend/python_backend/workflow_editor_ui.py
git commit -m "Fix sonar issues"
