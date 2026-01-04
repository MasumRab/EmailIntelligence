# Progress Tracking & Roadblock Recovery Guide

**Purpose**: Quick commands and workflows to track progress and recover from roadblocks  
**Last Updated**: November 12, 2025

---

## 🚀 Session Start Checklist

Run these commands when starting a development session:

```bash
# 1. Check current branch and status
git branch -v
git status

# 2. Review recent commits
git log -5 --oneline --graph

# 3. Check active/recent tasks
backlog task list --plain | head -20

# 4. Read latest session log
cat backlog/sessions/IFLOW-$(date +%Y%m%d)-*.md | tail -30

# 5. Check current blockers
backlog search "blocker" --plain
backlog search "roadblock" --plain
```

---

## 🔍 Dependency Diagnosis (Roadblock #1)

### Quick Health Check
```bash
# 1. Check Python environment
python --version
pip --version
which python

# 2. List all installed packages (verbose)
pip list
pip show notmuch
pip show gradio

# 3. Check dependency file consistency
echo "=== requirements.txt ==="
cat requirements.txt | grep -E "notmuch|gradio|pytorch"

echo "=== pyproject.toml ==="
cat pyproject.toml | grep -A 10 "dependencies"

echo "=== uv.lock (first 20 lines of conflicts) ==="
cat uv.lock | head -20
```

### Deep Dependency Analysis
```bash
# Check for circular dependencies
pip install pipdeptree 2>/dev/null && pipdeptree

# Analyze package conflicts
pip check

# Show dependency tree for problem packages
pipdeptree -p notmuch
pipdeptree -p gradio
pipdeptree -p pytorch

# Check version mismatches
pip install --dry-run -r requirements.txt 2>&1 | grep -i "conflict\|version\|incompatible"
```

### Dependency Resolution Actions
```bash
# Option 1: Use uv to resolve
python launch.py --setup

# Option 2: Use poetry
python launch.py --use-poetry --setup

# Option 3: Update dependencies
python launch.py --update-deps

# Option 4: Clean and fresh install
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Testing & Validation

### Run Full Test Suite
```bash
# Python backend tests
cd /home/masum/github/EmailIntelligenceAuto
pytest -v
pytest tests/ -v --tb=short

# Specific test file
pytest tests/test_category_service.py -v

# Specific test function
pytest tests/test_category_service.py::TestCategoryService::test_update_category -v

# With coverage
pytest --cov=backend --cov=modules tests/

# Linting
flake8 backend/ modules/ src/
black --check backend/ modules/ src/
mypy backend/ modules/ src/
pylint src/ modules/
```

### TypeScript/Frontend Testing
```bash
# From client directory
cd client

# Lint
npm run lint

# Type check
npm run type-check  # If available

# Build
npm run build

# Dev server
npm run dev
```

### End-to-End Validation
```bash
# 1. Start backend
python launch.py &

# 2. Wait for backend startup
sleep 5

# 3. Test API endpoints
curl -X GET http://localhost:8000/api/health
curl -X GET http://localhost:8000/api/workflows

# 4. Test workflow selection
curl -X POST http://localhost:8000/api/email/process \
  -H "Content-Type: application/json" \
  -d '{"email_id": "test-123"}'

# 5. Test category operations
curl -X GET http://localhost:8000/api/categories

# 6. Kill backend
kill %1
```

---

## 📊 Progress Tracking Commands

### Create Progress Update Task
```bash
# Create task to track progress
backlog task create "Progress Update Session" \
  -d "Track session progress and update dashboards" \
  --ac "Review roadblocks" \
  --ac "Test implementations" \
  --ac "Update dashboards" \
  --ac "Document findings"

# Then when starting
backlog task edit <id> -s "In Progress" -a @myself
```

### Update Achievement Tracking
```bash
# When completing a feature
backlog task create "COMPLETED: Workflow Selection" \
  -s Done \
  -d "Implemented dynamic workflow selection in email routes"

# Search for completed items
backlog task list -s Done --plain
```

### Roadblock Management
```bash
# Create roadblock task
backlog task create "ROADBLOCK: Dependency Conflicts" \
  -d "Resolve notmuch and gradio package conflicts" \
  -s "In Progress" \
  --priority high

# Track roadblock status
backlog search "roadblock" --plain

# Mark roadblock as resolved
backlog task edit <id> -s Done --notes "Dependencies resolved, tests passing"
```

---

## 📈 Generate Progress Report

### Automated Progress Script
```bash
#!/bin/bash
# save as: scripts/progress_report.sh

echo "=== EMAILINTELLIGENCE PROJECT PROGRESS REPORT ==="
echo "Generated: $(date)"
echo ""

echo "=== Git Status ==="
git log -1 --oneline
git status --short

echo ""
echo "=== Task Summary ==="
backlog task list --plain | wc -l
echo "Tasks in backlog:"
backlog task list -s "To Do" --plain | wc -l
echo "Tasks in progress:"
backlog task list -s "In Progress" --plain | wc -l
echo "Tasks completed:"
backlog task list -s Done --plain | wc -l

echo ""
echo "=== Test Status ==="
pytest --collect-only 2>/dev/null | grep "test session" || echo "Tests: Unable to run"

echo ""
echo "=== Build Status ==="
cd client && npm run build > /dev/null 2>&1 && echo "Frontend build: ✅ PASS" || echo "Frontend build: ❌ FAIL"
cd ..

echo ""
echo "=== Dependency Status ==="
pip check 2>/dev/null && echo "Dependencies: ✅ OK" || echo "Dependencies: ⚠️  CONFLICTS"

echo ""
echo "=== Latest Session Logs ==="
ls -t backlog/sessions/*.md | head -3
```

### Run Report Generation
```bash
bash scripts/progress_report.sh
```

---

## 🔄 Recovery Workflows

### When Stuck on Roadblock #1 (Dependencies)

**Step 1**: Capture current state
```bash
pip list > /tmp/pip_list.txt
cat requirements.txt > /tmp/requirements_backup.txt
cat pyproject.toml > /tmp/pyproject_backup.txt
```

**Step 2**: Try resolution strategy
```bash
# Strategy A: Update all packages
pip install --upgrade pip setuptools wheel
pip install --upgrade -r requirements.txt

# Strategy B: Use compatibility solver
pip install pipdeptree
pipdeptree | grep -E "notmuch|gradio"

# Strategy C: Isolate problem packages
pip uninstall -y notmuch gradio
pip install notmuch  # Install alone to see what it needs
pip install gradio   # Install alone to see what it needs
```

**Step 3**: Document findings
```bash
cat > /tmp/dependency_resolution.md << 'EOF'
# Dependency Resolution Attempt
Date: $(date)

## Issue
notmuch and gradio conflicts

## Analysis
$(pipdeptree 2>/dev/null)

## Resolution
$(pip check)

## Status
Resolved: YES/NO
EOF

backlog task edit <roadblock-id> --notes "$(cat /tmp/dependency_resolution.md)"
```

### When Tests Keep Failing

**Step 1**: Clear cache and rebuild
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache

# Clear Node cache
rm -rf node_modules/ package-lock.json
npm install
```

**Step 2**: Run minimal test
```bash
# Single small test to verify setup
pytest tests/test_database.py -v -s

# If fails, capture output
pytest tests/test_database.py -v --tb=long > /tmp/test_output.txt
cat /tmp/test_output.txt
```

**Step 3**: Document issue
```bash
backlog task create "Debug: Test Suite Failures" \
  -d "Diagnose and resolve test failures" \
  --ac "Identify root cause" \
  --ac "Implement fix" \
  --ac "Verify tests pass"
```

---

## 📝 Session Documentation Pattern

### Create Session Log Entry
```bash
# Create new session log
cat > backlog/sessions/IFLOW-$(date +%Y%m%d)-001.md << 'EOF'
# Development Session

Date: $(date)
Session ID: IFLOW-$(date +%Y%m%d)-001
Status: In Progress

## Session Goals
1. [Goal 1]
2. [Goal 2]

## Progress

### Accomplished
- [ ] Task 1
- [ ] Task 2

### In Progress
- [ ] Current task

### Roadblocks
- Roadblock description

## Next Steps
1. Step 1
2. Step 2
EOF

# Edit the template
vim backlog/sessions/IFLOW-$(date +%Y%m%d)-001.md
```

### Update Progress Dashboard
```bash
# After significant progress
cat >> PROGRESS_DASHBOARD.md << 'EOF'

## Latest Update
Date: $(date)
Session: [Session ID]

### Completed
- [Item completed]

### Blockers Resolved
- [Blocker resolved]

### Current Focus
- [Current work]
EOF
```

---

## 🎯 Quick Win Opportunities

If blocked on major issues, these quick wins restore momentum:

### 1. Documentation (30 mins)
```bash
# Update API documentation
# Update README.md with current status
# Create architecture diagrams
```

### 2. Code Quality (1 hour)
```bash
# Format code
black backend/ modules/ src/

# Sort imports
isort backend/ modules/ src/

# Lint check
flake8 backend/ --max-line-length=100
```

### 3. Environment Improvements (1-2 hours)
```bash
# Improve launch.py
# Add better error messages
# Implement graceful shutdown
# Add port cleanup logic
```

### 4. Testing Infrastructure (2 hours)
```bash
# Create test fixtures
# Improve test organization
# Add conftest.py patterns
# Document test procedures
```

---

## 🔗 Key Files to Monitor

```bash
# Check these regularly
watch -n 5 git status                    # File changes
cat requirements.txt                      # Dependencies
cat SESSION_LOG.md                        # Last session
cat PROGRESS_DASHBOARD.md                 # Overall status
backlog task list --plain                # Active tasks
```

---

## 📌 Commands by Frequency

### Daily
- `git status` - Check file changes
- `backlog task list --plain` - Review tasks
- `PROGRESS_DASHBOARD.md` - Check status

### When Blocked
- Run dependency diagnosis (Roadblock #1 section)
- Check test failures
- Review roadblock tracking doc

### When Done
- Update session log
- Update PROGRESS_DASHBOARD.md
- Mark tasks complete in backlog
- Create new tasks for unblocked work

### Weekly
- Generate progress report
- Review sidelined tasks
- Plan next week's work

---

## Emergency Commands

```bash
# If everything broken
git stash save "Emergency backup"
git pull origin main
python launch.py --setup
pytest

# If port stuck
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# If environment corrupted
rm -rf venv/ .venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

