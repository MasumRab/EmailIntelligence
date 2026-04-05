"""
Compare Command Module

Implements a sophisticated command for comparing logic DNA and functional patterns.
Uses AST normalization, logic hashing, and high-level aspect detection.
"""

import ast
import hashlib
import json
from argparse import Namespace
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..interface import Command


class CompareCommand(Command):
    """
    Command for identifying functional regressions during consolidation.
    
    Combines high-level pattern detection (Macro) with function-level 
    logic signatures (Micro) to verify implementation parity.
    """

    @property
    def name(self) -> str:
        return "logic-compare"

    @property
    def description(self) -> str:
        return "Compare logic signatures and functional patterns across script versions"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("scripts", nargs="+", help="Scripts to compare")
        parser.add_argument("--json", action="store_true", help="Output as JSON")
        parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold")

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    async def execute(self, args: Namespace) -> int:
        script_files = args.scripts
        if len(script_files) < 2:
            print("Error: Need at least 2 scripts to compare.")
            return 1

        print("🧬 Performing Forensic Logic Analysis on {} scripts...".format(len(script_files)))
        
        results = self._analyze_logic_chain(script_files)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            self._print_forensic_report(results, args.threshold)
            
        return 0

    def _analyze_logic_chain(self, files: List[str]) -> Dict:
        chain = []
        for f in files:
            path = Path(f)
            dna = self._extract_logical_dna(path)
            patterns = self._detect_patterns(path)
            chain.append({"file": f, "dna": dna, "patterns": patterns})
        
        comparisons = []
        for i in range(len(chain) - 1):
            comparisons.append(self._compare_dna(chain[i], chain[i+1]))
            
        return {"files": [c["file"] for c in chain], "comparisons": comparisons}

    def _extract_logical_dna(self, path: Path) -> Dict[str, Dict]:
        """Extract normalized logic signatures for every function."""
        dna = {}
        try:
            content = path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 1. Normalize logic (strip comments/whitespace)
                    logic_body = ast.get_source_segment(content, node) or ""
                    normalized = self._normalize_logic(logic_body)
                    
                    # 2. Generate Logical Signature
                    sig = hashlib.sha256(normalized.encode()).hexdigest()[:12]
                    
                    dna[node.name] = {
                        "sig": sig,
                        "complexity": len(node.body),
                        "body": normalized
                    }
        except Exception as e:
            print("Error extracting DNA from {}: {}".format(path.name, e))
        return dna

    def _detect_patterns(self, path: Path) -> Dict[str, bool]:
        """Detect critical high-level functionality patterns."""
        patterns = {
            'dynamic_improvement': False,
            'adaptive_thresholding': False,
            'layer_organization': False,
            'robust_parsing': False,
            'table_extraction': False,
            'iteration_tracking': False,
            'dependency_validation': False,
            'self_healing': False
        }
        try:
            content = path.read_text(encoding='utf-8')
            patterns['dynamic_improvement'] = 'iteration > 1' in content and 'prev_results' in content
            patterns['adaptive_thresholding'] = 'similarity < 0.7' in content or 'threshold.*0.7' in content
            patterns['layer_organization'] = 'foundation' in content and 'layer' in content
            patterns['robust_parsing'] = 're.split' in content and 're.sub' in content
            patterns['table_extraction'] = 'table' in content and 'row' in content and '|' in content
            patterns['iteration_tracking'] = 'iteration_history' in content or 'best_results' in content
            patterns['dependency_validation'] = 'dep_id' in content and 'validate' in content
            patterns['self_healing'] = 'improvement' in content and 'threshold' in content
        except Exception:
            pass
        return patterns

    def _normalize_logic(self, source: str) -> str:
        """Remove comments and normalize whitespace."""
        lines = [line.strip() for line in source.splitlines() 
                 if line.strip() and not line.strip().startswith("#")]
        return "".join(lines)

    def _compare_dna(self, old: Dict, new: Dict) -> Dict:
        """Deep comparison of logical signatures and patterns."""
        old_dna = old["dna"]
        new_dna = new["dna"]
        
        matches = []
        drifts = []
        missing = []

        # Function-level comparison
        for fn_name, old_data in old_dna.items():
            if fn_name in new_dna:
                new_data = new_dna[fn_name]
                if old_data["sig"] == new_data["sig"]:
                    matches.append(fn_name)
                else:
                    similarity = SequenceMatcher(None, old_data["body"], new_data["body"]).ratio()
                    drifts.append({
                        "name": fn_name,
                        "similarity": similarity,
                        "complexity_delta": new_data["complexity"] - old_data["complexity"]
                    })
            else:
                missing.append(fn_name)

        # Pattern-level comparison
        missing_patterns = [p for p, val in old["patterns"].items() if val and not new["patterns"][p]]

        return {
            "from": old["file"],
            "to": new["file"],
            "parity_score": len(matches) / len(old_dna) if old_dna else 1.0,
            "matches": matches,
            "drifts": drifts,
            "missing": missing,
            "missing_patterns": missing_patterns
        }

    def _print_forensic_report(self, results: Dict, threshold: float):
        for comp in results["comparisons"]:
            print("\n--- {} -> {} ---".format(comp['from'], comp['to']))
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

            if comp["missing_patterns"]:
                print("🚨 MISSING FUNCTIONAL ASPECTS: {}".format(", ".join(comp['missing_patterns'])))
