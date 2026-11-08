from src.cli.commands.task.engine.branch_clustering import BranchAnalyzer
"""
Hierarchical Branch Clustering

Implements hierarchical clustering of Git branches based on ACTUAL CODE CONTENT
similarity (AST structure, imports, functions, classes, docstrings, comments)
using semantic and structural analysis. NOT based on branch names or keywords.
"""

import subprocess
import ast
import hashlib
import re
import numpy as np
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict, Counter

try:
    import libcst as cst
    HAVE_LIBCST = True
except ImportError:
    HAVE_LIBCST = False

try:
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.metrics.pairwise import euclidean_distances
    from sklearn.decomposition import TruncatedSVD
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class ClusterLevel(Enum):
    """Levels of clustering granularity."""
    BRANCH = "branch"           # Individual branch
    TOPIC = "topic"             # Feature area based on code similarity
    DOMAIN = "domain"           # Functional domain based on code patterns
    TARGET = "target"           # Integration target (main, scientific, orchestration-tools)


@dataclass
class ClusterNode:
    """Node in the hierarchical cluster tree."""
    id: str
    name: str
    level: ClusterLevel
    branches: List[str] = field(default_factory=list)
    children: List['ClusterNode'] = field(default_factory=list)
    parent: Optional['ClusterNode'] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    tags: List[str] = field(default_factory=list)
    
    def add_child(self, child: 'ClusterNode'):
        child.parent = self
        self.children.append(child)
    
    def get_all_branches(self) -> List[str]:
        """Get all branches in this cluster and its descendants."""
        branches = list(self.branches)
        for child in self.children:
            branches.extend(child.get_all_branches())
        return branches


class HierarchicalClusterEngine:
    """
    Performs hierarchical clustering of Git branches based on ACTUAL CODE CONTENT
    similarity (AST structure, imports, functions, classes, docstrings, comments).
    NOT based on branch names or keywords.
    """
    
    def __init__(self, repo_path: str = ".", base_branch: str = "origin/main"):
        self.repo_path = repo_path
        self.base_branch = base_branch
        from src.cli.commands.task.engine.branch_clustering import BranchAnalyzer
        self.branch_analyzer = BranchAnalyzer(repo_path)
        
    def cluster_branches_hierarchically(
        self, 
        branches: List[str], 
        min_cluster_size: int = 2,
        max_depth: int = 3,
        similarity_threshold: float = 0.3
    ) -> ClusterNode:
        """
        Perform hierarchical clustering of branches based on ACTUAL CODE CONTENT
        similarity (AST structure, imports, functions, classes, docstrings, comments).
        NOT based on branch names or keywords.
        
        Args:
            branches: List of branch names to cluster
            min_cluster_size: Minimum branches to form a cluster
            max_depth: Maximum depth of hierarchy
            similarity_threshold: Minimum similarity to group branches
            
        Returns:
            Root ClusterNode of the hierarchical tree
        """
        # 1. Extract semantic features for all branches ONCE
        branch_features = self._extract_branch_features(branches)
        
        # 2. Build similarity matrix using CODE CONTENT features
        similarity_matrix = self._build_similarity_matrix(branches, branch_features)
        
        # 3. Perform hierarchical clustering at multiple levels
        root = ClusterNode(
            id="root",
            name="All Branches",
            level=ClusterLevel.TARGET,
            branches=[]
        )
        
        # Level 1: Target clustering (main/scientific/orchestration) using code patterns
        target_clusters = self._cluster_by_target_cached(branches, branch_features)
        for cluster_id, cluster_branches in target_clusters.items():
            if len(cluster_branches) >= min_cluster_size:
                target_node = ClusterNode(
                    id=f"target_{cluster_id}",
                    name=cluster_id.replace("_", " ").title(),
                    level=ClusterLevel.TARGET,
                    branches=cluster_branches
                )
                root.add_child(target_node)
                
                # Level 2: Domain clustering within each target using CODE SIMILARITY
                domain_clusters = self._cluster_by_domain_features_cached(cluster_branches, branch_features)
                for domain_id, domain_branches in domain_clusters.items():
                    if len(domain_branches) >= min_cluster_size:
                        domain_node = ClusterNode(
                            id=f"domain_{cluster_id}_{domain_id}",
                            name=domain_id.replace("_", " ").title(),
                            level=ClusterLevel.DOMAIN,
                            branches=domain_branches
                        )
                        root.children[-1].add_child(domain_node)
                        
                        # Level 3: Topic clustering within each domain using CODE SIMILARITY
                        topic_clusters = self._cluster_by_topic_features_cached(domain_branches, branch_features)
                        for topic_id, topic_branches in topic_clusters.items():
                            if len(topic_branches) >= min_cluster_size:
                                topic_node = ClusterNode(
                                    id=f"topic_{topic_id}",
                                    name=topic_id.replace("_", " ").title(),
                                    level=ClusterLevel.TOPIC,
                                    branches=topic_branches
                                )
                                domain_node.add_child(topic_node)
        
        return root
    
    def _extract_branch_features(self, branches: List[str]) -> Dict[str, Dict[str, Any]]:
        """Extract semantic features for each branch from ACTUAL CODE CONTENT."""
        features = {}
        for branch in branches:
            features[branch] = self._extract_single_branch_features(branch)
        return features
    
    def _extract_single_branch_features(self, branch: str, max_files: int = 50) -> Dict[str, Any]:
        """Extract semantic features for a single branch from ACTUAL CODE CONTENT.
        
        Args:
            branch: Branch name
            max_files: Maximum Python files to analyze (default 50 for performance)
        """
        analyzer = BranchAnalyzer(self.repo_path)
        
        # Get changed files
        files = analyzer.get_changed_files(branch, self.base_branch)
        py_files = [f for f in files if f.endswith('.py')]
        
        # Sample files for performance (analyze max_files)
        if len(py_files) > max_files:
            # Sample evenly across the file list
            step = len(py_files) // max_files
            py_files = py_files[::step][:max_files]
        
        features = {
            "files_changed": files,
            "py_files": py_files,
            "functions": set(),
            "classes": set(),
            "imports": set(),
            "docstrings": [],
            "comments": [],
            "structural_hashes": set(),
            "directories": set(),
            "file_extensions": Counter(),
            "ast_nodes": Counter(),
            "parent_branch": self._detect_parent_branch(branch),  # Track origin branch
        }
        
        for f in py_files:
            content = BranchAnalyzer(self.repo_path).get_file_content(branch, f)
            if not content:
                continue
            file_features = BranchAnalyzer(self.repo_path).analyze_file(content)
            features["functions"].update(file_features["functions"])
            features["classes"].update(file_features["classes"])
            features["imports"].update(file_features["imports"])
            features["docstrings"].extend(file_features["docstrings"])
            features["comments"].extend(file_features["comments"])
            if file_features["structural_hash"]:
                features["structural_hashes"].add(file_features["structural_hash"])
            
            # Track directory structure
            for f in files:
                parts = f.split('/')
                if len(parts) > 1:
                    features["directories"].add(parts[0])
            features["file_extensions"][f.split('.')[-1]] += 1
            
            # Track AST node types for structural similarity
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    features["ast_nodes"][type(node).__name__] += 1
            except:
                pass
        
        # Convert sets to sorted lists, but KEEP ast_nodes as Counter for similarity computation
        for key in ["functions", "classes", "imports", "structural_hashes"]:
            features[key] = sorted(features[key])
        features["docstrings"] = list(features["docstrings"])
        features["comments"] = list(features["comments"])
        features["directories"] = sorted(features["directories"])
        features["file_extensions"] = dict(features["file_extensions"])
        # Keep ast_nodes as Counter for similarity computation
        
        return features
    
    def _detect_parent_branch(self, branch: str) -> str:
        """Detect which main branch this branch was created from (merge-base)."""
        import subprocess
        main_branches = ["origin/main", "origin/scientific", "origin/orchestration-tools"]
        
        for base in main_branches:
            result = subprocess.run(
                ["git", "merge-base", base, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                return base
        
        return "unknown"
    
    def _build_similarity_matrix(self, branches: List[str], features: Dict) -> Dict[Tuple[str, str], float]:
        """Build pairwise similarity matrix between branches using CODE CONTENT features."""
        similarity = {}
        for i, b1 in enumerate(branches):
            for b2 in branches[i+1:]:
                sim = self._compute_content_similarity(features[b1], features[b2])
                similarity[(b1, b2)] = sim
                similarity[(b2, b1)] = sim
        return similarity
    
    def _compute_content_similarity(self, f1: Dict, f2: Dict) -> float:
        """Compute similarity between two feature sets using CODE CONTENT features."""
        def jaccard(set1, set2):
            if not set1 and not set2:
                return 1.0
            if not set1 or not set2:
                return 0.0
            return len(set1 & set2) / len(set1 | set2)
        
        def counter_jaccard(c1: Counter, c2: Counter) -> float:
            if not c1 and not c2:
                return 1.0
            if not c1 or not c2:
                return 0.0
            all_keys = set(c1.keys()) | set(c2.keys())
            intersection = sum(min(c1[k], c2[k]) for k in all_keys)
            union = sum(c1.values()) + sum(c2.values()) - intersection
            return intersection / union if union > 0 else 0.0
        
        # Weighted similarity using CODE CONTENT features
        weights = {
            "functions": 0.18,
            "classes": 0.13,
            "imports": 0.18,
            "structural_hashes": 0.13,
            "ast_nodes": 0.13,
            "directories": 0.09,
            "file_extensions": 0.04,
            "parent_branch": 0.12,  # Origin branch is strong signal
        }
        
        total = 0.0
        total_weight = 0.0
        for key, weight in weights.items():
            if key in ("functions", "classes", "imports", "structural_hashes"):
                s1 = set(f1.get(key, []))
                s2 = set(f2.get(key, []))
                sim = len(s1 & s2) / max(len(s1 | s2), 1)
            elif key in ("ast_nodes",):
                c1 = Counter(f1.get(key, {}))
                c2 = Counter(f2.get(key, {}))
                sim = self._counter_jaccard(c1, c2)
            elif key == "parent_branch":
                # Exact match for parent branch
                p1 = f1.get(key, "unknown")
                p2 = f2.get(key, "unknown")
                sim = 1.0 if p1 == p2 and p1 != "unknown" else 0.0
            else:
                s1 = set(f1.get(key, []))
                s2 = set(f2.get(key, []))
                sim = len(s1 & s2) / max(len(s1 | s2), 1)
            
            total += weight * sim
            total_weight += weight
        
        return total / total_weight if total_weight > 0 else 0.0
    
    def _counter_jaccard(self, c1: Counter, c2: Counter) -> float:
        if not c1 and not c2:
            return 1.0
        if not c1 or not c2:
            return 0.0
        all_keys = set(c1.keys()) | set(c2.keys())
        intersection = sum(min(c1[k], c2[k]) for k in all_keys)
        union = sum(c1.values()) + sum(c2.values()) - intersection
        return intersection / union if union > 0 else 0.0

    def _cluster_by_target(self, branches: List[str]) -> Dict[str, List[str]]:
        """Cluster branches by integration target using CODE PATTERNS (not branch names)."""
        clusters = {"main": [], "scientific": [], "orchestration_tools": []}
        
        for branch in branches:
            # Use content-based heuristic: check actual code patterns
            target = self._assign_target_by_content(branch)
            if target == "orchestration-tools":
                clusters["orchestration_tools"].append(branch)
            elif target == "scientific":
                clusters["scientific"].append(branch)
            else:
                clusters["main"].append(branch)
        
        return {k: v for k, v in clusters.items() if v}
    
    def _cluster_by_target_cached(self, branches: List[str], branch_features: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Cluster branches by integration target using CODE PATTERNS (not branch names)."""
        clusters = {"main": [], "scientific": [], "orchestration_tools": []}
        
        for branch in branches:
            # Use cached features
            features = branch_features.get(branch, {})
            imports = features.get("imports", [])
            
            has_ml_imports = False
            has_orchestration_code = False
            has_nlp_code = False
            
            for imp in imports:
                imp_lower = imp.lower()
                if any(kw in imp_lower for kw in ["torch", "tensorflow", "sklearn", "pytorch", "transformers", "huggingface"]):
                    has_ml_imports = True
                if any(kw in imp_lower for kw in ["taskmaster", "orchestration", "cli/commands"]):
                    has_orchestration_code = True
                if any(kw in imp_lower for kw in ["nlp", "spacy", "bert", "transformers", "sentiment", "tokenizer"]):
                    has_nlp_code = True
            
            if has_orchestration_code:
                clusters["orchestration_tools"].append(branch)
            elif has_ml_imports or has_nlp_code:
                clusters["scientific"].append(branch)
            else:
                clusters["main"].append(branch)
        
        return {k: v for k, v in clusters.items() if v}
    
    def _cluster_by_domain_features_cached(self, branches: List[str], branch_features: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Cluster branches by functional domain using CODE CONTENT features (cached)."""
        if len(branches) < 2:
            return {}
        
        # Build similarity matrix using CACHED features
        n = len(branches)
        if n < 2:
            return {f"domain_{i}": [b] for i, b in enumerate(branches)}
        
        # Build similarity matrix using cached features
        similarity_matrix = []
        branches_list = list(branches)
        for i in range(n):
            row = []
            for j in range(n):
                sim = self._compute_content_similarity(
                    branch_features[branches_list[i]],
                    branch_features[branches_list[j]]
                )
                row.append(sim)
            similarity_matrix.append(row)
        
        # Hierarchical clustering
        if SKLEARN_AVAILABLE and n >= 3:
            distance_matrix = [[1 - sim for sim in row] for row in similarity_matrix]
            n_clusters = min(max(2, n // 3), n)
            clustering = AgglomerativeClustering(
                n_clusters=min(n_clusters, n),
                metric='precomputed',
                linkage='average'
            )
            try:
                labels = clustering.fit_predict(np.array(similarity_matrix))
                clusters = defaultdict(list)
                for idx, label in enumerate(labels):
                    clusters[f"domain_{label}"].append(branches_list[idx])
                return dict(clusters)
            except:
                pass
        
        # Fallback: greedy clustering based on content similarity
        clusters = {}
        assigned = set()
        
        for i, b1 in enumerate(branches):
            if b1 in assigned:
                continue
            cluster = [b1]
            assigned.add(b1)
            
            for j, b2 in enumerate(branches):
                if b2 in assigned or b1 == b2:
                    continue
                sim = self._compute_content_similarity(
                    branch_features[b1],
                    branch_features[b2]
                )
                if sim > 0.25:  # Similarity threshold for domain clustering
                    cluster.append(b2)
                    assigned.add(b2)
            
            if len(cluster) >= 2:
                clusters[f"domain_{len(clusters)}"] = cluster
        
        return clusters
    
    def _cluster_by_topic_features_cached(self, branches: List[str], branch_features: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Cluster branches by topic using content-based similarity (cached)."""
        if len(branches) < 2:
            return {f"topic_{i}": [b] for i, b in enumerate(branches)}
        
        # Build similarity matrix using CACHED features
        n = len(branches)
        similarity_matrix = []
        branches_list = list(branches)
        for i in range(n):
            row = []
            for j in range(n):
                sim = self._compute_content_similarity(
                    branch_features[branches_list[i]],
                    branch_features[branches_list[j]]
                )
                row.append(sim)
            similarity_matrix.append(row)
        
        if SKLEARN_AVAILABLE and n >= 3:
            distance_matrix = [[1 - sim for sim in row] for row in similarity_matrix]
            n_clusters = min(max(2, n // 3), n)
            clustering = AgglomerativeClustering(
                n_clusters=min(n_clusters, n),
                metric='precomputed',
                linkage='average'
            )
            try:
                labels = clustering.fit_predict(np.array(similarity_matrix))
                clusters = defaultdict(list)
                for idx, label in enumerate(labels):
                    clusters[f"topic_{label}"].append(branches_list[idx])
                return dict(clusters)
            except:
                pass
        
        # Fallback: greedy clustering based on content similarity
        clusters = {}
        assigned = set()
        
        for i, b1 in enumerate(branches):
            if b1 in assigned:
                continue
            cluster = [b1]
            assigned.add(b1)
            
            for j, b2 in enumerate(branches):
                if b2 in assigned or b1 == b2:
                    continue
                sim = self._compute_content_similarity(
                    branch_features[b1],
                    branch_features[b2]
                )
                if sim > 0.25:  # Topic similarity threshold
                    cluster.append(b2)
                    assigned.add(b2)
            
            if len(cluster) >= 2:
                clusters[f"topic_{len(clusters)}"] = cluster
        
        return dict(clusters)
    
    def _assign_target_by_content(self, branch: str, branch_features: Dict = None) -> str:
        """Assign target based on CODE CONTENT PATTERNS (not branch name).
        
        Args:
            branch: Branch name
            branch_features: Optional pre-extracted features (if available)
        """
        if branch_features and branch in branch_features:
            # Use cached features
            features = branch_features[branch]
            imports = features.get("imports", [])
        else:
            # Fallback to direct analysis
            analyzer = BranchAnalyzer(self.repo_path)
            
            # Get actual code content to determine target
            files = self.branch_analyzer.get_changed_files(branch, self.base_branch)
            py_files = [f for f in files if f.endswith('.py')]
            
            # Check imports and code patterns
            imports = set()
            for f in py_files[:50]:  # Sample files
                content = BranchAnalyzer(self.repo_path).get_file_content(branch, f)
                if not content:
                    continue
                file_features = BranchAnalyzer(self.repo_path).analyze_file(content)
                imports.update(file_features.get("imports", []))
        
        has_ml_imports = False
        has_orchestration_code = False
        has_nlp_code = False
        
        for imp in imports:
            imp_lower = imp.lower()
            if any(kw in imp_lower for kw in ["torch", "tensorflow", "sklearn", "pytorch", "transformers", "huggingface"]):
                has_ml_imports = True
            if any(kw in imp_lower for kw in ["taskmaster", "orchestration", "cli/commands"]):
                has_orchestration_code = True
            if any(kw in imp_lower for kw in ["nlp", "spacy", "bert", "transformers", "sentiment", "tokenizer"]):
                has_nlp_code = True
        
        if has_orchestration_code:
            return "orchestration-tools"
        if has_ml_imports or has_nlp_code:
            return "scientific"
        return "main"
    
    def _cluster_by_domain_features(self, branches: List[str]) -> Dict[str, List[str]]:
        """Cluster branches by functional domain using CODE CONTENT features."""
        if len(branches) < 2:
            return {}
        
        # Extract features ONCE per branch (cache them)
        branch_features = {}
        for branch in branches:
            branch_features[branch] = self._extract_single_branch_features(branch)
        
        # Build similarity matrix
        n = len(branches)
        if n < 2:
            return {f"domain_{i}": [b] for i, b in enumerate(branches)}
        
        # Build similarity matrix using cached features
        similarity_matrix = []
        branches_list = list(branches)
        for i in range(n):
            row = []
            for j in range(n):
                sim = self._compute_content_similarity(
                    branch_features[branches_list[i]],
                    branch_features[branches_list[j]]
                )
                row.append(sim)
            similarity_matrix.append(row)
        
        # Hierarchical clustering
        if SKLEARN_AVAILABLE and n >= 3:
            distance_matrix = [[1 - sim for sim in row] for row in similarity_matrix]
            n_clusters = min(max(2, n // 3), n)
            clustering = AgglomerativeClustering(
                n_clusters=min(n_clusters, n),
                metric='precomputed',
                linkage='average'
            )
            try:
                labels = clustering.fit_predict(np.array(similarity_matrix))
                clusters = defaultdict(list)
                for idx, label in enumerate(labels):
                    clusters[f"domain_{label}"].append(branches_list[idx])
                return dict(clusters)
            except:
                pass
        
        # Fallback: greedy clustering based on content similarity
        clusters = {}
        assigned = set()
        
        for i, b1 in enumerate(branches):
            if b1 in assigned:
                continue
            cluster = [b1]
            assigned.add(b1)
            
            for j, b2 in enumerate(branches):
                if b2 in assigned or b1 == b2:
                    continue
                sim = self._compute_content_similarity(
                    branch_features[b1],
                    branch_features[b2]
                )
                if sim > 0.25:  # Similarity threshold for domain clustering
                    cluster.append(b2)
                    assigned.add(b2)
            
            if len(cluster) >= 2:
                clusters[f"domain_{len(clusters)}"] = cluster
        
        return clusters
    
    def _cluster_by_topic_features(self, branches: List[str]) -> Dict[str, List[str]]:
        """Cluster branches by topic using content-based similarity."""
        if len(branches) < 2:
            return {f"topic_{i}": [b] for i, b in enumerate(branches)}
        
        # Use content similarity for topic clustering
        branch_features = self._extract_branch_features(branches)
        branches_list = list(branches)
        
        # Build similarity matrix
        n = len(branches)
        similarity_matrix = []
        for i in range(len(branches)):
            row = []
            for j in range(len(branches)):
                sim = self._compute_content_similarity(
                    self._extract_single_branch_features(branches_list[i]),
                    self._extract_single_branch_features(branches_list[j])
                )
                row.append(sim)
            similarity_matrix.append(row)
        
        if SKLEARN_AVAILABLE and len(branches) >= 3:
            distance_matrix = [[1 - sim for sim in row] for row in similarity_matrix]
            n_clusters = min(max(2, len(branches) // 3), len(branches))
            clustering = AgglomerativeClustering(
                n_clusters=min(n_clusters, len(branches)),
                metric='precomputed',
                linkage='average'
            )
            try:
                labels = clustering.fit_predict(np.array(similarity_matrix))
                clusters = defaultdict(list)
                for idx, label in enumerate(labels):
                    clusters[f"topic_{label}"].append(branches_list[idx])
                return dict(clusters)
            except:
                pass
        
        # Fallback: greedy clustering based on content similarity
        clusters = {}
        assigned = set()
        
        for i, b1 in enumerate(branches):
            if b1 in assigned:
                continue
            cluster = [b1]
            assigned.add(b1)
            
            for j, b2 in enumerate(branches):
                if b2 in assigned or b1 == b2:
                    continue
                sim = self._compute_content_similarity(
                    self._extract_single_branch_features(b1),
                    self._extract_single_branch_features(b2)
                )
                if sim > 0.25:  # Topic similarity threshold
                    cluster.append(b2)
                    assigned.add(b2)
            
            if len(cluster) >= 2:
                clusters[f"topic_{len(clusters)}"] = cluster
        
        return dict(clusters)
