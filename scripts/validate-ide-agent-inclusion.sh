#!/bin/bash

# Validate IDE Agent File Inclusion in orchestration-tools
# This script ensures all IDE agent files and configurations are properly tracked

set -e

REPO_ROOT="${REPO_ROOT:-.}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
ERRORS=0
WARNINGS=0

echo "=========================================="
echo "IDE Agent File Inclusion Validation"
echo "=========================================="
echo "Repository: $REPO_ROOT"
echo "Branch: $BRANCH"
echo ""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check primary agent instruction files
echo "1. Checking Primary Agent Instruction Files..."
AGENT_FILES=(
  "AGENTS.md"
  "CRUSH.md"
  "LLXPRT.md"
  "IFLOW.md"
  "QWEN.md"
  "CLAUDE.md"
)

for file in "${AGENT_FILES[@]}"; do
  if [ -f "$REPO_ROOT/$file" ]; then
    if git ls-files | grep -q "^$file$"; then
      echo -e "  ${GREEN}✅${NC} $file - tracked"
    else
      echo -e "  ${RED}❌${NC} $file - EXISTS but NOT tracked"
      ((ERRORS++))
    fi
  else
    echo -e "  ${YELLOW}⚠️${NC} $file - file not found"
    ((WARNINGS++))
  fi
done
echo ""

# 2. Check IDE configuration directories
echo "2. Checking IDE Configuration Directories..."
IDE_DIRS=(
  ".claude"
  ".cursor"
  ".windsurf"
  ".roo"
  ".kilo"
  ".clinerules"
  ".opencode"
  ".specify"
)

for dir in "${IDE_DIRS[@]}"; do
  if [ -d "$REPO_ROOT/$dir" ]; then
    file_count=$(git ls-files | grep "^$dir/" | wc -l)
    if [ "$file_count" -gt 0 ]; then
      echo -e "  ${GREEN}✅${NC} $dir/ - $file_count files tracked"
    else
      echo -e "  ${RED}❌${NC} $dir/ - EXISTS but files NOT tracked"
      ((ERRORS++))
    fi
  else
    echo -e "  ${YELLOW}⚠️${NC} $dir/ - directory not found"
    ((WARNINGS++))
  fi
done
echo ""

# 3. Check GitHub instructions
echo "3. Checking GitHub Instructions..."
GITHUB_FILES=(
  ".github/instructions/dev_workflow.instructions.md"
  ".github/instructions/taskmaster.instructions.md"
  ".github/instructions/self_improve.instructions.md"
  ".github/instructions/vscode_rules.instructions.md"
  ".github/instructions/tools-manifest.json"
)

for file in "${GITHUB_FILES[@]}"; do
  if [ -f "$REPO_ROOT/$file" ]; then
    if git ls-files | grep -q "^${file#./}$"; then
      echo -e "  ${GREEN}✅${NC} ${file#./} - tracked"
    else
      echo -e "  ${RED}❌${NC} ${file#./} - EXISTS but NOT tracked"
      ((ERRORS++))
    fi
  else
    echo -e "  ${YELLOW}⚠️${NC} ${file#./} - file not found"
    ((WARNINGS++))
  fi
done
echo ""

# 4. Check MCP configuration
echo "4. Checking MCP Configuration..."
if [ -f "$REPO_ROOT/.mcp.json" ]; then
  if git ls-files | grep -q "^\.mcp\.json$"; then
    echo -e "  ${GREEN}✅${NC} .mcp.json - tracked"
  else
    echo -e "  ${RED}❌${NC} .mcp.json - EXISTS but NOT tracked"
    ((ERRORS++))
  fi
else
  echo -e "  ${YELLOW}⚠️${NC} .mcp.json - file not found"
  ((WARNINGS++))
fi
echo ""

# 5. Check supporting documentation
echo "5. Checking Supporting Documentation..."
SUPPORT_FILES=(
  "TASKMASTER_INTEGRATION_README.md"
  "MODEL_CONTEXT_STRATEGY.md"
  "ORCHESTRATION_CONTROL_MODULE.md"
  "ORCHESTRATION_IDE_AGENT_INCLUSION.md"
)

for file in "${SUPPORT_FILES[@]}"; do
  if [ -f "$REPO_ROOT/$file" ]; then
    if git ls-files | grep -q "^$file$"; then
      echo -e "  ${GREEN}✅${NC} $file - tracked"
    else
      echo -e "  ${RED}❌${NC} $file - EXISTS but NOT tracked"
      ((ERRORS++))
    fi
  else
    echo -e "  ${YELLOW}⚠️${NC} $file - file not found"
    ((WARNINGS++))
  fi
done
echo ""

# 6. Check .env.example
echo "6. Checking Environment Configuration..."
if [ -f "$REPO_ROOT/.env.example" ]; then
  if git ls-files | grep -q "^\.env\.example$"; then
    echo -e "  ${GREEN}✅${NC} .env.example - tracked"
  else
    echo -e "  ${RED}❌${NC} .env.example - EXISTS but NOT tracked"
    ((ERRORS++))
  fi
else
  echo -e "  ${YELLOW}⚠️${NC} .env.example - file not found"
  ((WARNINGS++))
fi
echo ""

# Summary
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✅ All IDE agent files are properly included!${NC}"
  exit 0
else
  echo -e "${RED}❌ Please add missing files to git:${NC}"
  echo ""
  echo "To fix, run:"
  echo "  git add AGENT_FILES..."
  echo "  git add .claude/ .cursor/ .windsurf/ .roo/ .kilo/"
  echo "  git commit -m 'chore: ensure IDE agent files included in orchestration-tools'"
  exit 1
fi
