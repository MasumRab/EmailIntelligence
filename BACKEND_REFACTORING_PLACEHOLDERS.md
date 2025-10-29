# Backend References - Refactoring Placeholders

This document catalogs key references to "backend" in the codebase to facilitate future refactoring or module restructuring.

## Critical File Paths (launch.py)
```python
# PLACEHOLDER: Update these paths if backend directory is renamed/restructured
critical_files = [
    "backend/python_backend/main.py",              # Main FastAPI app
    "backend/python_nlp/nlp_engine.py",           # NLP processing engine
    "backend/python_backend/database.py",         # Database management
    # ... 10+ more backend files
]
```

## Import Statements
```python
# PLACEHOLDER: Update relative imports if backend structure changes
from ..python_backend.ai_engine import AdvancedAIEngine  # gmail_service.py
from backend.node_engine.email_nodes import (...)        # node_engine files
```

## Module Paths
```python
# PLACEHOLDER: Update uvicorn module path if backend.python_backend.main is renamed
uvicorn.run("backend.python_backend.main:app", ...)      # run.py

# PLACEHOLDER: Update module mappings for import checking
"backend.python_backend.database",                       # error_checking_prompt.py
"backend/python_backend": "src/main:create_app() ..."    # architecture mapping
```

## Path Calculations
```python
# PLACEHOLDER: Update path assumptions if script location changes
project_root = script_dir.parent.parent  # backend/node_engine/test_sanitization.py
```

## Refactoring Checklist
- [ ] Update all file paths in launch.py critical_files list
- [ ] Update all import statements using `from backend.` or `backend.`
- [ ] Update uvicorn.run() module path in run.py
- [ ] Update path calculations in test files
- [ ] Update documentation strings
- [ ] Test: `python launch.py --system-info`, `pytest`, `python run.py`

## Total References Found: 2800+ (focus on project files, exclude venv)
