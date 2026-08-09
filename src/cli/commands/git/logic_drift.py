"""
Logic Drift Command Module

Implements a command for comparing logic DNA between branches to detect functional
drift or regressions during merge conflict resolution.
"""

import ast
import hashlib
import json
import subprocess
from argparse import Namespace
from difflib import SequenceMatcher
from typing import Any, Dict, List, Tuple

from ..interface import Command

class LogicDriftAnalyzerCommand(Command):
    """
    Command for identifying functional regressions across branches.
    """

    @property
    def name(self) -> str:
        return "git-logic-drift"

    @property
    def description(self) -> str:
        return "Compare logic signatures across git branches"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("file", help="File to analyze across branches")
        parser.add_argument("--base", default="origin/main", help="Base branch")
        parser.add_argument("--head", default="HEAD", help="Head branch")
        parser.add_argument("--json", action="store_true", help="Output as JSON")
        parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold")

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    async def execute(self, args: Namespace) -> int:
        print(f"🧬 Performing Logic Drift Analysis for {args.file} ({args.base} vs {args.head})...")
        
        base_content = self._get_file_content(args.base, args.file)
        head_content = self._get_file_content(args.head, args.file)
        
        if base_content is None or head_content is None:
            print("❌ Error: Could not read file from one or both branches.")
            return 1
            
        base_dna = self._extract_logical_dna(base_content)
        head_dna = self._extract_logical_dna(head_content)
        
        comp = self._compare_dna(base_dna, head_dna)
        
        if args.json:
            print(json.dumps(comp, indent=2))
        else:
            self._print_forensic_report(comp, args.threshold)
            
        return 0

    def _get_file_content(self, ref: str, file_path: str) -> str:
        try:
            return subprocess.check_output(["git", "show", f"{ref}:{file_path}"], text=True, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return None

    def _extract_logical_dna(self, content: str) -> Dict[str, Dict]:
        import tempfile
        import os
        from pathlib import Path
        from src.cli.commands.analysis.compare import CompareCommand

        # Reuse CompareCommand's exact DNA extractor to satisfy DRY principles
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as tf:
            tf.write(content)
            temp_path = tf.name

        try:
            cmd = CompareCommand()
            dna = cmd._extract_logical_dna(Path(temp_path))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return dna

    def _normalize_logic(self, source: str) -> str:
        lines = [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]
        return "".join(lines)

    def _compare_dna(self, old_dna: Dict, new_dna: Dict) -> Dict:
        from src.cli.commands.analysis.compare import CompareCommand
        cmd = CompareCommand()
        # Mock the wrapper dictionaries used by CompareCommand
        old_wrapper = {"dna": old_dna, "patterns": {}, "file": "base"}
        new_wrapper = {"dna": new_dna, "patterns": {}, "file": "head"}
        return cmd._compare_dna(old_wrapper, new_wrapper)

    def _print_forensic_report(self, comp: Dict, threshold: float):
        print("Parity Score: {:.2f}%".format(comp['parity_score'] * 100))
        if comp["matches"]:
            print("✅ Identical Logic ({}): {}".format(len(comp['matches']), ", ".join(comp['matches'][:5])))
        if comp["drifts"]:
            print("⚠️  Logic Drift Detected ({}):".format(len(comp['drifts'])))
            for d in comp["drifts"]:
                status = "Fuzzy Match" if d["similarity"] >= threshold else "MAJOR DRIFT"
                print("  - {}: {:.1f}% similarity ({})".format(d['name'], d['similarity'] * 100, status))
        if comp["missing"]:
            print("❌ Dropped Functions ({}): {}".format(len(comp['missing']), ", ".join(comp['missing'])))
