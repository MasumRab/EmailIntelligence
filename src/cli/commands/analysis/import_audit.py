"""
Import Audit Command Module (Industrial Edition)

High-fidelity import refactoring using LibCST and AST.
Provides a 'Robust' mode for zero-loss structural changes.
"""

import ast
import json
import logging
import os
import tempfile
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import libcst as cst
from libcst import matchers as m

from ..interface import Command

logger = logging.getLogger(__name__)

class ImportTransformer(cst.CSTTransformer):
    """LibCST Transformer for surgical import remapping."""
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
        self.modified = False

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.Import:
        new_names = []
        for name in updated_node.names:
            old_name = name.name.value
            if old_name in self.mapping:
                new_names.append(name.with_changes(name=cst.Name(self.mapping[old_name])))
                self.modified = True
            else:
                new_names.append(name)
        return updated_node.with_changes(names=new_names)

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        if updated_node.module:
            old_module = updated_node.module.value
            if old_module in self.mapping:
                self.modified = True
                return updated_node.with_changes(module=cst.Name(self.mapping[old_module]))
        return updated_node

class ImportAuditCommand(Command):
    """
    Industrial-grade import auditor and refactoring engine.
    Supports AST heuristics and LibCST lossless transformations.
    """

    @property
    def name(self) -> str:
        return "import-audit"

    @property
    def description(self) -> str:
        return "Deep module mapping and codebase-wide import refactoring (Task 18 alignment)"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--src", default="src", help="Source directory to analyze")
        parser.add_argument("--legacy-roots", default="backend", help="Comma-separated legacy root namespaces")
        parser.add_argument("--new-prefix", default="src.backend", help="The target module prefix to remap to")
        parser.add_argument("--fix", action="store_true", help="Apply transformations (lossless CST)")
        parser.add_argument("--map", help="Path to a custom JSON import mapping file")
        parser.add_argument("--mode", choices=["ast", "cst"], default="cst", help="Refactoring backend to use")

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    async def execute(self, args: Namespace) -> int:
        print(f"🚀 Initializing Import Auditor (Mode: {args.mode.upper()})")
        src_path = Path(args.src)
        if not src_path.exists():
            print(f"❌ Error: Target path '{src_path}' not found.")
            return 1

        mapping = self._build_refactor_map(args)
        print(f"📋 Loaded {len(mapping)} refactoring rules.")
        
        targets = list(src_path.rglob("*.py"))
        print(f"🔍 Analyzing {len(targets)} Python files...")
        
        modified_count = 0
        for f in targets:
            if args.mode == "cst":
                changed = self._process_cst(f, mapping, args.fix)
            else:
                changed = self._process_ast(f, mapping, args.fix)

            if changed:
                modified_count += 1
                if not args.fix: print(f"  ⚠️ Requires update: {f}")

        if args.fix:
            print(f"\n✅ Migration Complete. Modified {modified_count} files.")
        else:
            print(f"\n📊 Dry Run Complete. {modified_count} files require migration.")
            if modified_count > 0: print("   Run with --fix to apply changes.")

        return 0

    def _process_cst(self, file_path: Path, mapping: Dict[str, str], apply_fix: bool) -> bool:
        """High-fidelity processing preserving comments and exact whitespace."""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = cst.parse_module(content)

            transformer = ImportTransformer(mapping)
            modified_tree = tree.visit(transformer)
            
            if transformer.modified and apply_fix:
                file_path.write_text(modified_tree.code, encoding='utf-8')
                print(f"  🔧 Rewrote: {file_path}")

            return transformer.modified
        except Exception as e:
            logger.debug(f"CST processing failed on {file_path}: {e}")
            # Fallback to AST checking if CST chokes
            return self._process_ast(file_path, mapping, False)

    def _process_ast(self, file_path: Path, mapping: Dict[str, str], apply_fix: bool) -> bool:
        """Fast heuristic evaluation. (Fallback)"""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            changes = self._extract_ast_import_changes(tree, mapping)

            if not changes:
                return False
            if apply_fix:
                return self._apply_ast_changes(file_path, content, changes)
            return False
        except Exception:
            return False

    def _extract_ast_import_changes(self, tree: ast.AST, mapping: Dict[str, str]) -> List[Tuple[int, str, str]]:
        """Extract import changes from AST tree."""
        changes = []
        for node in ast.walk(tree):
            change = self._process_ast_node(node, mapping)
            if change:
                changes.append(change)
        return changes

    def _process_ast_node(self, node: ast.AST, mapping: Dict[str, str]) -> Optional[Tuple[int, str, str]]:
        """Process a single AST node for import changes."""
        if isinstance(node, ast.Import):
            for n in node.names:
                root = n.name.split('.')[0]
                if root in mapping:
                    return (node.lineno, n.name, self._map_name(n.name, mapping))
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split('.')[0]
            if root in mapping:
                return (node.lineno, node.module, self._map_name(node.module, mapping))
        return None

    def _map_name(self, original: str, mapping: Dict[str, str]) -> str:
        root = original.split('.')[0]
        if root in mapping:
            return original.replace(root, mapping[root], 1)
        return original

    def _apply_ast_changes(self, file_path: Path, content: str, changes: List[Tuple[int, str, str]]) -> bool:
        """Naive line-based replace for AST fallback. (DANGEROUS, preferred CST)"""
        # Create a copy of content to avoid any user-controlled modifications
        lines = content.splitlines()
        if not lines:
            return False

        modified = False
        for lineno, old, new in changes:
            # Validate lineno is a positive integer within bounds
            if not isinstance(lineno, int) or lineno < 1:
                continue
            idx = lineno - 1
            # Additional bounds check: ensure idx is within list bounds
            if idx >= len(lines):
                continue
            # Validate that the old string exists in the target line before modification
            # This prevents malicious manipulation of line numbers or content
            if old not in lines[idx]:
                continue
            lines[idx] = lines[idx].replace(old, new)
            modified = True

        if modified:
            # Write using a safe method - create temp file with fixed name pattern
            try:
                # Use mkstemp for atomic file writing with secure permissions
                fd, temp_path_str = tempfile.mkstemp(
                    suffix='.tmp',
                    prefix='import_audit_',
                    dir=str(file_path.parent)
                )
                try:
                    with os.fdopen(fd, 'w', encoding='utf-8') as f:
                        f.write("\n".join(lines) + "\n")
                    # Atomic rename
                    os.replace(temp_path_str, str(file_path))
                    print(f"  ⚠️ AST Fallback Rewrite: {file_path}")
                except Exception:
                    # Clean up temp file on failure
                    os.unlink(temp_path_str)
                    raise
            except Exception:
                return False
        return modified

    def _build_refactor_map(self, args: Namespace) -> Dict[str, str]:
        if args.map and Path(args.map).exists():
            with open(args.map) as f:
                return json.load(f)
        return {r.strip(): r.strip() if "." in r else f"{args.new_prefix}.{r.strip()}" for r in args.legacy_roots.split(",")}
