#!/bin/bash

echo "=== Scientific Branch AST Analysis ==="
echo ""

echo "1. Checking for Merge Conflicts..."
grep -r "<<<<<<<\|=======\|>>>>>>>>" src.scientific 2>/dev/null && echo "FOUND" || echo "✓ Clean - No conflicts"

echo ""
echo "2. Checking TODO/FIXME markers..."
grep -r "TODO\|FIXME\|XXX\|HACK" src.scientific 2>/dev/null | head -10 || echo "✓ None found"

echo ""
echo "3. Finding CLI patterns..."
grep -r "def cli_\|@click.command\|@click.option" src.scientific 2>/dev/null | head -20 || echo "No CLI patterns found"

echo ""
echo "4. Checking for subprocess calls..."
grep -r "subprocess\." src.scientific 2>/dev/null | grep -v "test" | head -15 || echo "No subprocess calls"

echo ""
echo "5. Current scientific branch status:"
git log --oneline -5 scientific-integration
echo ""
git status --short scientific-integration
echo ""
echo "=== Analysis Complete ==="
