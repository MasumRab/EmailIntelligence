#!/bin/bash
# Branch Analysis and Verification Script
# Executes the preliminary checks required before core alignment can proceed safely

echo "=== STARTING BRANCH ANALYSIS AND VERIFICATION ==="
echo "Date: $(date)"
echo ""

echo "1. IDENTIFYING ORCHESTRATION BRANCHES..."
echo "---------------------------------------"
ORCHESTRATION_BRANCHES=$(git branch -a | grep -i orchestration)
if [ -z "$ORCHESTRATION_BRANCHES" ]; then
    echo "No orchestration branches found"
else
    echo "Found orchestration branches:"
    echo "$ORCHESTRATION_BRANCHES"
fi
echo ""

echo "2. CHECKING FOR MIGRATION ISSUES (backend → src/backend)..."
echo "----------------------------------------------------------"
echo "Checking for import statements with old 'backend' path..."
BACKEND_IMPORTS=$(find . -name "*.py" -exec grep -l "from backend\|import backend" {} \; 2>/dev/null | head -10)
if [ -z "$BACKEND_IMPORTS" ]; then
    echo "No obvious backend import issues found"
else
    echo "Files with potential old import statements:"
    echo "$BACKEND_IMPORTS"
    echo ""
    grep -n "from backend\|import backend" $BACKEND_IMPORTS 2>/dev/null | head -20
fi
echo ""

echo "3. IDENTIFYING OUTDATED DIRECTORIES..."
echo "-------------------------------------"
echo "Looking for temporary/backlog directories..."
TEMP_DIRS=$(find . -name "temp*" -o -name "backlog*" -o -name "*backup*" -type d | grep -v "\.git" | head -20)
if [ -z "$TEMP_DIRS" ]; then
    echo "No obvious temporary directories found"
else
    echo "Potential temporary/outdated directories:"
    echo "$TEMP_DIRS"
fi
echo ""

echo "4. CHECKING LAUNCH.PY FILES..."
echo "------------------------------"
LAUNCH_SCRIPTS=$(find . -name "launch.py" -type f)
if [ -z "$LAUNCH_SCRIPTS" ]; then
    echo "No launch.py files found"
else
    echo "Found launch.py files:"
    echo "$LAUNCH_SCRIPTS"
    echo ""
    for launch_script in $LAUNCH_SCRIPTS; do
        echo "Checking $launch_script:"
        if [ -f "$launch_script" ]; then
            echo "  - Size: $(wc -c < "$launch_script") bytes"
            HAS_ORCHESTRATION=$(grep -c "orchestration\|command.*pattern\|container\|services" "$launch_script" 2>/dev/null || echo 0)
            if [ "$HAS_ORCHESTRATION" -gt 0 ]; then
                echo "  - Contains orchestration features"
            else
                echo "  - Basic launch functionality"
            fi
        fi
        echo ""
    done
fi
echo ""

echo "5. CHECKING FOR DUPLICATE DOCUMENTATION FILES..."
echo "-----------------------------------------------"
DUPLICATE_MD=$(find . -name "*.md" -not -path "./docs/*" -not -path "./.git/*" -not -path "./venv/*" -not -path "./.taskmaster/*" | xargs grep -l "Documentation\|Overview\|Introduction" 2>/dev/null | head -10)
if [ -z "$DUPLICATE_MD" ]; then
    echo "No obvious duplicate documentation files found outside docs/"
else
    echo "Possible duplicate documentation files in wrong locations:"
    echo "$DUPLICATE_MD"
fi
echo ""

echo "6. IDENTIFYING SIMILAR BRANCHES..."
echo "----------------------------------"
SIMILAR_BRANCHES=$(git branch -a | grep -E "(notmuch|tagging|search|merge|align)" | head -15)
if [ -z "$SIMILAR_BRANCHES" ]; then
    echo "No similar named branches detected"
else
    echo "Branches with potentially similar functionality:"
    echo "$SIMILAR_BRANCHES"
fi
echo ""

echo "=== BRANCH ANALYSIS COMPLETE ==="
echo "Review the findings above before proceeding with core alignment tasks"
echo ""
echo "Next steps:"
echo "1. Address any orchestration branch issues identified above"
echo "2. Fix any migration issues (backend → src) before alignment"
echo "3. Clean up any temporary/duplicate directories if needed"
echo "4. Verify launch.py functionality on critical branches"
echo "5. Address any similar branches that may have conflicting content"
echo "6. Then proceed with core alignment tasks (74-83)"