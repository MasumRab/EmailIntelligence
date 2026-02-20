#!/bin/bash
# Master Audit Script - Runs all audit tools for branch preparation
# Usage: ./master_audit.sh <repo_root> <report_prefix>

set -e

REPO_ROOT="${1:-.}"
REPORT_PREFIX="${2:-audit}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================"
echo "Master Audit Script"
echo "========================================"
echo "Repo: $REPO_ROOT"
echo "Prefix: $REPORT_PREFIX"
echo "Timestamp: $TIMESTAMP"
echo "========================================"

cd "$REPO_ROOT"

# Define report files
REPORT_DIR="$REPO_ROOT/audit-reports"
mkdir -p "$REPORT_DIR"

echo ""
echo "[1/4] Running Path Change Detection..."
echo "----------------------------------------"
python3 scripts/path_change_detector.py HEAD origin/main 2>&1 | tee "$REPORT_DIR/${REPORT_PREFIX}-path-changes-${TIMESTAMP}.md"
echo "Path change report saved to: $REPORT_DIR/${REPORT_PREFIX}-path-changes-${TIMESTAMP}.md"

echo ""
echo "[2/4] Running Import Audit..."
echo "----------------------------------------"
python3 scripts/import_audit.py "$REPO_ROOT" 2>&1 | tee "$REPORT_DIR/${REPORT_PREFIX}-import-audit-${TIMESTAMP}.md"
echo "Import audit report saved to: $REPORT_DIR/${REPORT_PREFIX}-import-audit-${TIMESTAMP}.md"

echo ""
echo "[3/4] Running Conflict Prediction..."
echo "----------------------------------------"
python3 scripts/conflict_predictor.py HEAD origin/main 2>&1 | tee "$REPORT_DIR/${REPORT_PREFIX}-conflict-prediction-${TIMESTAMP}.md"
echo "Conflict prediction report saved to: $REPORT_DIR/${REPORT_PREFIX}-conflict-prediction-${TIMESTAMP}.md"

echo ""
echo "[4/4] Generating Summary Report..."
echo "----------------------------------------"

# Generate summary
cat > "$REPORT_DIR/${REPORT_PREFIX}-summary-${TIMESTAMP}.md" << EOF
# Master Audit Summary Report

**Timestamp:** $TIMESTAMP  
**Repository:** $REPO_ROOT  
**Report Prefix:** $REPORT_PREFIX

## Reports Generated

| Tool | File |
|------|------|
| Path Change Detector | ${REPORT_PREFIX}-path-changes-${TIMESTAMP}.md |
| Import Audit | ${REPORT_PREFIX}-import-audit-${TIMESTAMP}.md |
| Conflict Predictor | ${REPORT_PREFIX}-conflict-prediction-${TIMESTAMP}.md |

## Quick Links

- [Path Changes](./${REPORT_PREFIX}-path-changes-${TIMESTAMP}.md)
- [Import Issues](./${REPORT_PREFIX}-import-audit-${TIMESTAMP}.md)
- [Conflict Predictions](./${REPORT_PREFIX}-conflict-prediction-${TIMESTAMP}.md)

## Next Steps

1. Review path changes and update imports using \`update_references.py\`
2. Fix import issues using \`import_audit.py --auto-fix\`
3. Analyze conflict predictions and prepare resolution strategies
4. Run \`intelligent_merge_analyzer.py\` for detailed change overlap analysis

## Notes

- All reports are located in: $REPORT_DIR
- Auto-fix logs are in: $REPORT_DIR/auto-fix-*.log
EOF

echo "Summary report saved to: $REPORT_DIR/${REPORT_PREFIX}-summary-${TIMESTAMP}.md"

echo ""
echo "========================================"
echo "Master Audit Complete!"
echo "========================================"
echo "Reports directory: $REPORT_DIR"
echo "Summary: $REPORT_DIR/${REPORT_PREFIX}-summary-${TIMESTAMP}.md"
echo "========================================"
