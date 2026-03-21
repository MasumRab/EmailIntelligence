"""
Import Audit Command Module (Industrial Edition)

High-fidelity import refactoring using LibCST and AST.
Provides a 'Robust' mode for zero-loss structural changes.
"""

import ast
import json
import subprocess
import logging
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

try:
    import libcst as cst
    from libcst import matchers as m
    LIBCST_AVAILABLE = True
except ImportError:
    LIBCST_AVAILABLE = False

from ..interface import Command

logger = logging.getLogger(__name__)


class ImportTransformer(cst.CSTTransformer):
    """LibCST Transformer for surgical import remapping."""
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
        self.modified = False

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.Import:
        new_names = []
        for alias in updated_node.names:
            parts = alias.name.value.split('.')
            if parts[0] in self.mapping:
                new_root = self.mapping[parts[0]]
                new_name = alias.with_changes(
                    name=cst.parse_expression("{}.{}".format(new_root, ".".join(parts[1:])) if len(parts) > 1 else new_root)
                )
                new_names.append(new_name)
                self.modified = True
            else:
                new_names.append(alias)
        return updated_node.with_changes(names=new_names)

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        if updated_node.module and isinstance(updated_node.module, cst.Name):
            root = updated_node.module.value.split('.')[0]
            if root in self.mapping:
                new_root = self.mapping[root]
                new_module = cst.parse_expression(updated_node.module.value.replace(root, new_root, 1))
                self.modified = True
                return updated_node.with_changes(module=new_module)
        return updated_node


class ImportAuditCommand(Command):
    """
    Command for high-fidelity import refactoring and standardization.
    
    Modes:
    - AST (Fast): Default method for standard remapping.
    - LibCST (Robust): Zero-loss transformation preserving comments/formatting.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "import-audit"

    @property
    def description(self) -> str:
        return "Audit, normalize, and surgically standardize repository imports"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--fix", action="store_true", help="Apply fixes")
        parser.add_argument("--robust", action="store_true", help="Use LibCST for high-fidelity fixing")
        parser.add_argument("--standardize", action="store_true", help="Run ruff and isort (Review required)")
        parser.add_argument("--path", default=".", help="Directory to scan")
        parser.add_argument("--map", help="Path to JSON refactor map")
        parser.add_argument("--legacy-roots", default="backend,core,utils")
        parser.add_argument("--new-prefix", default="src")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        root_dir = Path(args.path)
        refactor_map = self._build_refactor_map(args)
        
        mode = "LibCST" if (args.robust and LIBCST_AVAILABLE) else "AST"
        print("🧬 Starting {} Refactor in '{}'".format(mode, root_dir.absolute()))
        
        py_files = list(root_dir.rglob("*.py"))
        fixed_count = 0
        for py_file in py_files:
            if "venv" in str(py_file):
                continue
            
            if args.robust and LIBCST_AVAILABLE:
                if self._process_file_libcst(py_file, refactor_map, args.fix):
                    fixed_count += 1
            else:
                if self._process_file_ast(py_file, refactor_map, args.fix):
                    fixed_count += 1

        print("✅ Refactor Complete. Files Modified: {}".format(fixed_count))
        return 0

    def _process_file_libcst(self, file_path: Path, mapping: Dict[str, str], apply_fix: bool) -> bool:
        """Robust refactoring using LibCST."""
        try:
            source = file_path.read_text(encoding='utf-8')
            wrapper = cst.MetadataWrapper(cst.parse_module(source))
            transformer = ImportTransformer(mapping)
            modified_tree = wrapper.visit(transformer)
            
            if transformer.modified:
                if apply_fix:
                    file_path.write_text(modified_tree.code, encoding='utf-8')
                    print("  [ROBUST FIXED] {}".format(file_path.name))
                    return True
                else:
                    print("  [!] {}: Legacy imports detected (Robust Mode)".format(file_path.name))
            return False
        except Exception as e:
            print("  [ERROR] LibCST failed on {}: {}".format(file_path.name, e))
            return False

    def _process_file_ast(self, file_path: Path, mapping: Dict[str, str], apply_fix: bool) -> bool:
        """Standard refactoring using AST."""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            changes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split('.')[0] in mapping:
                            changes.append((node.lineno, alias.name, self._map_name(alias.name, mapping)))
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split('.')[0]
                    if root in mapping:
                        changes.append((node.lineno, node.module, self._map_name(node.module, mapping)))
            if not changes: return False
            if apply_fix: return self._apply_ast_changes(file_path, content, changes)
            return False
        except Exception: return False

    def _map_name(self, original: str, mapping: Dict[str, str]) -> str:
        root = original.split('.')[0]
        suffix = original[len(root):]
        return mapping[root] + suffix

    def _apply_ast_changes(self, file_path: Path, content: str, changes: List[Tuple[int, str, str]]) -> bool:
        lines = content.splitlines()
        modified = False
        for lineno, old, new in sorted(changes, key=lambda x: x[0], reverse=True):
            idx = lineno - 1
            if idx < len(lines) and old in lines[idx]:
                lines[idx] = lines[idx].replace(old, new)
                modified = True
        if modified:
            file_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
            print("  [FIXED] {}".format(file_path.name))
            return True
        return False

    def _build_refactor_map(self, args: Namespace) -> Dict[str, str]:
        if args.map and Path(args.map).exists():
            with open(args.map) as f: return json.load(f)
        return {r.strip(): r.strip() if "." in r else "{}.{}".format(args.new_prefix, r.strip()) for r in args.legacy_roots.split(",")}
