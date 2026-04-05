import subprocess
import ast
import hashlib
import re
from typing import Dict, List, Any

try:
    import libcst as cst
    HAVE_LIBCST = True
except ImportError:
    HAVE_LIBCST = False

class GitAnalysisError(Exception):
    """Raised when git commands fail due to bad refs or fetching errors."""
    pass

def hash_content(code: str) -> str:
    return hashlib.md5(code.encode()).hexdigest()

class BranchAnalyzer:
    """Analyzes a branch using ast and libcst to extract semantic features."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_changed_files(self, branch: str, base_branch: str) -> List[str]:
        """Gets all files changed between branches."""
        try:
            cmd = ["git", "diff", "--name-only", f"{base_branch}...{branch}"]
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True)
            files = [f for f in result.stdout.strip().split("\n") if f]
            return files
        except subprocess.CalledProcessError as e:
            if any(err in e.stderr for err in ["bad revision", "unknown revision", "ambiguous argument", "fatal: bad object"]):
                raise GitAnalysisError(f"Git diff failed due to invalid ref: {e.stderr}")
            return []

    def get_file_content(self, branch: str, filepath: str) -> str:
        """Gets the content of a file at a specific branch."""
        try:
            cmd = ["git", "show", f"{branch}:{filepath}"]
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if "does not exist" in e.stderr or "fatal: Path" in e.stderr:
                return "" # Missing path is fine, handle naturally
            raise GitAnalysisError(f"Git show failed: {e.stderr}")

    def analyze_file(self, content: str) -> Dict[str, Any]:
        """Extracts features from Python code using ast and libcst."""
        result = {
            "functions": [],
            "classes": [],
            "imports": [],
            "docstrings": [],
            "comments": [],
            "structural_hash": "",
            "content_hash": hash_content(content)
        }

        if not content:
            return result

        # Fast AST structural pass
        self._extract_ast_features(content, result)

        # LibCST for deep semantic extraction (comments)
        if HAVE_LIBCST:
            self._extract_cst_comments(content, result)

        return result

    def _extract_ast_features(self, content: str, result: Dict[str, Any]) -> None:
        """Extract features using AST."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                self._process_ast_node(node, result)

            result["structural_hash"] = hash_content(
                ast.dump(
                    tree,
                    annotate_fields=False,
                    include_attributes=False))
        except SyntaxError:
            pass  # Invalid python file, skip AST

    def _process_ast_node(self, node: ast.AST, result: Dict[str, Any]) -> None:
        """Process a single AST node and extract features."""
        if isinstance(node, (ast.FunctionDef, getattr(ast, 'AsyncFunctionDef', type(None)))):
            result["functions"].append(node.name)
            doc = ast.get_docstring(node)
            if doc:
                result["docstrings"].append(doc)
        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)
            doc = ast.get_docstring(node)
            if doc:
                result["docstrings"].append(doc)
        elif isinstance(node, ast.Import):
            for name in node.names:
                result["imports"].append(name.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for name in node.names:
                result["imports"].append(f"{mod}.{name.name}")

    def _extract_cst_comments(self, content: str, result: Dict[str, Any]) -> None:
        """Extract comments using LibCST."""
        try:
            cst_tree = cst.parse_module(content)

            class CommentVisitor(cst.CSTVisitor):
                def __init__(self):
                    self.comments = []

                def visit_Comment(self, node):
                    self.comments.append(node.value)

            visitor = CommentVisitor()
            cst_tree.visit(visitor)
            result["comments"] = visitor.comments
        except Exception:
            pass


class ClusterEngine:
    """Orchestrates the branch clustering logic."""

    def __init__(self, repo_path: str = ".", mode: str = "hybrid"):
        self.analyzer = BranchAnalyzer(repo_path)
        self.mode = mode

    def execute(self, branches: List[str], base_branch: str = "origin/main") -> Dict[str, Any]:
        branch_metrics = {}

        # 1. Feature Extraction (Map)
        for branch in branches:
            # We want all files for context, but we only run AST on .py files.
            all_files = self.analyzer.get_changed_files(branch, base_branch)
            py_files = [f for f in all_files if f.endswith('.py')]

            features = {
                "files_changed": all_files,
                "functions": set(),
                "classes": set(),
                "imports": set(),
                "docstrings": [],
                "comments": [],
                "structural_hashes": set()
            }

            for f in py_files:
                content = self.analyzer.get_file_content(branch, f)
                file_features = self.analyzer.analyze_file(content)
                features["functions"].update(file_features["functions"])
                features["classes"].update(file_features["classes"])
                features["imports"].update(file_features["imports"])
                features["docstrings"].extend(file_features["docstrings"])
                features["comments"].extend(file_features["comments"])
                if file_features["structural_hash"]:
                    features["structural_hashes"].add(
                        file_features["structural_hash"])

            # Convert sets to sorted lists for deterministic outputs
            features["functions"] = sorted(features["functions"])
            features["classes"] = sorted(features["classes"])
            features["imports"] = sorted(features["imports"])
            features["structural_hashes"] = sorted(features["structural_hashes"])

            branch_metrics[branch] = features

        # 2. Assignment / Clustering (Reduce) based on mode
        assignments = {}
        for branch, metrics in branch_metrics.items():
            if self.mode in ("identification", "hybrid"):
                target, confidence, reasoning, tags = self._assign_target(branch, metrics)
            else:
                target, confidence, reasoning, tags = "main", 0.5, "Clustering mode bypassing identification", ["tag:unsupervised_cluster"]

            assignments[branch] = {
                "target": target,
                "confidence": confidence,
                "reasoning": reasoning,
                "tags": tags,
                "metrics": metrics
            }

        return assignments

    def _assign_target(self, branch: str, metrics: Dict[str, Any]) -> tuple:
        """Rule-based supervised heuristic assignment."""
        target = "main"
        confidence = 0.5
        reasoning = "Default assignment"
        tags = []

        name = branch.lower()
        # Tokenize the branch name for robust semantic matching (no false substring positives)
        tokens = re.split(r'[-_/\s\.]', name)

        files = metrics.get("files_changed", [])
        imports = set(metrics.get("imports", []))

        # Rule 1: Orchestration
        if any("taskmaster" in f or "cli/commands" in f for f in files) or "orch" in tokens or "orchestration" in tokens:
            target = "orchestration-tools"
            confidence = 0.85
            reasoning = "Modifies CLI/orchestration paths"
            tags.append("tag:orchestration_branch")

        # Rule 2: Scientific
        elif any("python_nlp" in f or "ai_engine" in f for f in files) or "scientific" in tokens or "ml" in tokens:
            target = "scientific"
            confidence = 0.85
            reasoning = "Modifies NLP/AI paths"
            tags.append("tag:scientific_branch")

        # Rule 3: Dependency Overlap heuristics
        if any("torch" in i or "transformers" in i for i in imports):
            target = "scientific"
            confidence = 0.90
            reasoning = "Introduces heavy ML dependencies"
            tags.append("tag:ml_deps")

        if not tags:
            tags.append("tag:feature_branch")

        return target, confidence, reasoning, tags
