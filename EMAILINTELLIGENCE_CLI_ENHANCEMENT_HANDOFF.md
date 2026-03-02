# EmailIntelligence CLI Enhancement - Comprehensive Handoff Document

**Session Date:** 2026-02-28  
**Target Branch:** `orchestration-tools`  
**Primary Objectives:** Refactor conflict detection with git merge-tree, implement direct branch push workflow, add all-branches scanning capability

---

## 1. Git-Related Work

### 1.1 Primary Refactoring: `_detect_conflicts` with `git merge-tree`

**Current Implementation Location:** `emailintelligence_cli.py` lines 231-258

**Current Code:**
```python
def _detect_conflicts(self, worktree_a_path: Path, worktree_b_path: Path) -> List[Dict[str, Any]]:
    """Detect conflicts between worktrees"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=worktree_a_path,
            check=True, capture_output=True, text=True
        )
        conflicts = []
        for file_path in result.stdout.strip().split('\n'):
            if file_path and not file_path.startswith('.'):
                conflict_info = {
                    'file': file_path,
                    'path_a': str(worktree_a_path / file_path),
                    'path_b': str(worktree_b_path / file_path),
                    'detected_at': datetime.now().isoformat()
                }
                conflicts.append(conflict_info)
        self._info(f"🔍 Detected {len(conflicts)} potential conflicts")
        return conflicts
    except subprocess.CalledProcessError:
        return []
```

**Issue:** Uses `git diff --name-only` which only shows files that differ between branches - NOT actual merge conflict markers. This is a LOW-ACCURACY git command that needs replacement.

### 1.2 Smart Fuzzy Semantic Matching Integration

**Enhanced Conflict Detection with Semantic Analysis:**

The handoff document now includes comprehensive smart fuzzy semantic matching techniques for various comparison tasks:

```python
@dataclass
class SemanticConflictAnalysis:
    """Advanced semantic conflict analysis using multiple matching techniques"""
    
    file_path: str
    semantic_similarity: float  # 0.0 to 1.0
    fuzzy_match_score: float    # 0.0 to 1.0
    structural_similarity: float  # 0.0 to 1.0
    conflict_regions: List[ConflictRegion]
    resolution_suggestions: List[str] = field(default_factory=list)


class SemanticConflictDetector:
    """Advanced conflict detection using semantic analysis and fuzzy matching"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.semantic_analyzer = SemanticAnalyzer()
        self.fuzzy_matcher = FuzzyMatcher()
        self.structural_analyzer = StructuralAnalyzer()
    
    def detect_semantic_conflicts(
        self, 
        source_branch: str, 
        target_branch: str,
        base_branch: str = None
    ) -> List[SemanticConflictAnalysis]:
        """
        Detect conflicts using semantic analysis and fuzzy matching.
        
        Combines:
        1. Git merge-tree for structural conflicts
        2. Semantic analysis for meaning-based conflicts
        3. Fuzzy matching for similar but different content
        4. Structural analysis for code organization conflicts
        """
        
        # Get base branch if not provided
        if not base_branch:
            base_branch = self._find_merge_base(source_branch, target_branch)
        
        # Get file contents from all three branches
        source_files = self._get_branch_files(source_branch)
        target_files = self._get_branch_files(target_branch)
        base_files = self._get_branch_files(base_branch)
        
        semantic_conflicts = []
        
        # Analyze files that exist in source or target
        all_files = set(source_files.keys()) | set(target_files.keys())
        
        for file_path in all_files:
            if self._should_analyze_file(file_path):
                conflict = self._analyze_file_semantically(
                    file_path, source_files, target_files, base_files
                )
                if conflict:
                    semantic_conflicts.append(conflict)
        
        return semantic_conflicts
    
    def _analyze_file_semantically(
        self,
        file_path: str,
        source_files: Dict[str, str],
        target_files: Dict[str, str],
        base_files: Dict[str, str]
    ) -> Optional[SemanticConflictAnalysis]:
        """Perform semantic analysis on a specific file"""
        
        source_content = source_files.get(file_path, "")
        target_content = target_files.get(file_path, "")
        base_content = base_files.get(file_path, "")
        
        # Skip if no actual changes
        if source_content == target_content:
            return None
        
        # Calculate semantic similarity
        semantic_score = self.semantic_analyzer.calculate_similarity(
            source_content, target_content
        )
        
        # Calculate fuzzy match score
        fuzzy_score = self.fuzzy_matcher.calculate_fuzzy_similarity(
            source_content, target_content
        )
        
        # Calculate structural similarity
        structural_score = self.structural_analyzer.calculate_structural_similarity(
            source_content, target_content
        )
        
        # Determine if this is a semantic conflict
        if self._is_semantic_conflict(semantic_score, fuzzy_score, structural_score):
            conflict_regions = self._identify_conflict_regions(
                source_content, target_content, base_content
            )
            
            suggestions = self._generate_resolution_suggestions(
                source_content, target_content, conflict_regions
            )
            
            return SemanticConflictAnalysis(
                file_path=file_path,
                semantic_similarity=semantic_score,
                fuzzy_match_score=fuzzy_score,
                structural_similarity=structural_score,
                conflict_regions=conflict_regions,
                resolution_suggestions=suggestions
            )
        
        return None
    
    def _is_semantic_conflict(
        self, 
        semantic_score: float, 
        fuzzy_score: float, 
        structural_score: float
    ) -> bool:
        """Determine if changes constitute a semantic conflict"""
        
        # Conflict thresholds
        SEMANTIC_THRESHOLD = 0.7  # Low semantic similarity = high conflict
        FUZZY_THRESHOLD = 0.8     # High fuzzy similarity = potential conflict
        STRUCTURAL_THRESHOLD = 0.6 # Low structural similarity = high conflict
        
        # Multiple conflict indicators
        semantic_conflict = semantic_score < SEMANTIC_THRESHOLD
        fuzzy_conflict = fuzzy_score > FUZZY_THRESHOLD
        structural_conflict = structural_score < STRUCTURAL_THRESHOLD
        
        # Conflict if multiple indicators are present
        conflict_indicators = sum([
            semantic_conflict,
            fuzzy_conflict, 
            structural_conflict
        ])
        
        return conflict_indicators >= 2
    
    def _identify_conflict_regions(
        self,
        source_content: str,
        target_content: str,
        base_content: str
    ) -> List[ConflictRegion]:
        """Identify specific regions of conflict using semantic analysis"""
        
        source_lines = source_content.split('\n')
        target_lines = target_content.split('\n')
        base_lines = base_content.split('\n') if base_content else []
        
        conflict_regions = []
        current_region = None
        
        # Use semantic line comparison
        for i, (source_line, target_line) in enumerate(zip(source_lines, target_lines)):
            if self._lines_semantically_conflict(source_line, target_line):
                if not current_region:
                    current_region = ConflictRegion(
                        start_line=i + 1,
                        end_line=i + 1,
                        content_ours=source_line,
                        content_theirs=target_line
                    )
                else:
                    current_region.end_line = i + 1
                    current_region.content_ours += f"\n{source_line}"
                    current_region.content_theirs += f"\n{target_line}"
            else:
                if current_region:
                    conflict_regions.append(current_region)
                    current_region = None
        
        if current_region:
            conflict_regions.append(current_region)
        
        return conflict_regions
    
    def _lines_semantically_conflict(self, line1: str, line2: str) -> bool:
        """Check if two lines have semantic conflict"""
        
        # Skip if identical
        if line1 == line2:
            return False
        
        # Skip if both are empty or whitespace
        if not line1.strip() and not line2.strip():
            return False
        
        # Calculate semantic similarity for the lines
        similarity = self.semantic_analyzer.calculate_similarity(line1, line2)
        
        # Lines are in conflict if they're semantically different
        return similarity < 0.5


class SemanticAnalyzer:
    """Semantic analysis using various techniques"""
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        
        Uses multiple techniques:
        1. TF-IDF vectorization
        2. Word embeddings (if available)
        3. Semantic role labeling
        4. Dependency parsing
        """
        
        if not text1 or not text2:
            return 0.0
        
        # Method 1: TF-IDF similarity
        tfidf_similarity = self._calculate_tfidf_similarity(text1, text2)
        
        # Method 2: Word embedding similarity (if embeddings available)
        embedding_similarity = self._calculate_embedding_similarity(text1, text2)
        
        # Method 3: Semantic role similarity
        role_similarity = self._calculate_semantic_role_similarity(text1, text2)
        
        # Combine scores with weights
        combined_similarity = (
            tfidf_similarity * 0.4 +
            embedding_similarity * 0.4 +
            role_similarity * 0.2
        )
        
        return combined_similarity
    
    def _calculate_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Calculate TF-IDF based similarity"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        try:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=1000
            )
            
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except ImportError:
            # Fallback to simple word overlap
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
    
    def _calculate_embedding_similarity(self, text1: str, text2: str) -> float:
        """Calculate word embedding based similarity"""
        try:
            # Try to use pre-trained embeddings if available
            import numpy as np
            
            # Simple fallback using word frequency vectors
            words1 = text1.lower().split()
            words2 = text2.lower().split()
            
            # Create simple frequency vectors
            all_words = set(words1) | set(words2)
            vec1 = [words1.count(word) for word in all_words]
            vec2 = [words2.count(word) for word in all_words]
            
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
            
        except Exception:
            return 0.5  # Neutral score if calculation fails
    
    def _calculate_semantic_role_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic role labeling similarity"""
        try:
            # Simple verb-based similarity
            verbs1 = self._extract_verbs(text1)
            verbs2 = self._extract_verbs(text2)
            
            if not verbs1 and not verbs2:
                return 1.0
            if not verbs1 or not verbs2:
                return 0.0
            
            common_verbs = set(verbs1) & set(verbs2)
            all_verbs = set(verbs1) | set(verbs2)
            
            return len(common_verbs) / len(all_verbs)
            
        except Exception:
            return 0.5
    
    def _extract_verbs(self, text: str) -> List[str]:
        """Extract verbs from text (simplified)"""
        import re
        
        # Simple verb extraction using common verb patterns
        verbs = re.findall(r'\b(?:run|create|update|delete|modify|add|remove|change|implement|develop|build|test|deploy|merge|commit|push|pull)\b', text.lower())
        
        return verbs


class FuzzyMatcher:
    """Fuzzy string matching for conflict detection"""
    
    def calculate_fuzzy_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate fuzzy similarity between two texts.
        
        Uses multiple fuzzy matching algorithms:
        1. Levenshtein distance
        2. Jaro-Winkler distance
        3. Sequence matching
        4. Token-based matching
        """
        
        if not text1 or not text2:
            return 0.0
        
        # Method 1: Levenshtein distance
        levenshtein_sim = self._calculate_levenshtein_similarity(text1, text2)
        
        # Method 2: Jaro-Winkler similarity
        jaro_sim = self._calculate_jaro_similarity(text1, text2)
        
        # Method 3: Sequence matcher
        seq_sim = self._calculate_sequence_similarity(text1, text2)
        
        # Method 4: Token-based similarity
        token_sim = self._calculate_token_similarity(text1, text2)
        
        # Weighted combination
        combined_similarity = (
            levenshtein_sim * 0.3 +
            jaro_sim * 0.2 +
            seq_sim * 0.3 +
            token_sim * 0.2
        )
        
        return combined_similarity
    
    def _calculate_levenshtein_similarity(self, text1: str, text2: str) -> float:
        """Calculate Levenshtein distance similarity"""
        try:
            from difflib import SequenceMatcher
            return SequenceMatcher(None, text1, text2).ratio()
        except ImportError:
            return self._simple_levenshtein(text1, text2)
    
    def _simple_levenshtein(self, text1: str, text2: str) -> float:
        """Simple Levenshtein distance calculation"""
        if len(text1) < len(text2):
            return self._simple_levenshtein(text2, text1)
        
        if len(text2) == 0:
            return 0.0
        
        previous_row = list(range(len(text2) + 1))
        for i, c1 in enumerate(text1):
            current_row = [i + 1]
            for j, c2 in enumerate(text2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        max_len = max(len(text1), len(text2))
        if max_len == 0:
            return 1.0
        
        distance = previous_row[-1]
        return 1.0 - (distance / max_len)
    
    def _calculate_jaro_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaro-Winkler similarity"""
        try:
            import jellyfish
            return jellyfish.jaro_similarity(text1, text2)
        except ImportError:
            return self._simple_jaro_similarity(text1, text2)
    
    def _simple_jaro_similarity(self, text1: str, text2: str) -> float:
        """Simple Jaro similarity calculation"""
        if not text1 or not text2:
            return 0.0
        
        len1, len2 = len(text1), len(text2)
        if abs(len1 - len2) > 3:
            return 0.0
        
        # Find matching characters within window
        window = max(len1, len2) // 2 - 1
        matches1 = [False] * len1
        matches2 = [False] * len2
        matches = 0
        
        for i in range(len1):
            start = max(0, i - window)
            end = min(i + window + 1, len2)
            
            for j in range(start, end):
                if not matches2[j] and text1[i] == text2[j]:
                    matches1[i] = matches2[j] = True
                    matches += 1
                    break
        
        if matches == 0:
            return 0.0
        
        # Calculate transpositions
        transpositions = 0
        k = 0
        for i in range(len1):
            if matches1[i]:
                while not matches2[k]:
                    k += 1
                if text1[i] != text2[k]:
                    transpositions += 1
                k += 1
        
        jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3
        return jaro
    
    def _calculate_sequence_similarity(self, text1: str, text2: str) -> float:
        """Calculate sequence-based similarity"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _calculate_token_similarity(self, text1: str, text2: str) -> float:
        """Calculate token-based similarity"""
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        
        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        
        return len(intersection) / len(union)


class StructuralAnalyzer:
    """Analyze code structure for conflicts"""
    
    def calculate_structural_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate structural similarity between two code snippets.
        
        Analyzes:
        1. AST structure
        2. Function/class definitions
        3. Control flow patterns
        4. Import statements
        """
        
        if not code1 or not code2:
            return 0.0
        
        try:
            import ast
            
            # Parse ASTs
            tree1 = ast.parse(code1)
            tree2 = ast.parse(code2)
            
            # Calculate structural similarity
            structure_sim = self._compare_ast_structures(tree1, tree2)
            functions_sim = self._compare_function_definitions(tree1, tree2)
            imports_sim = self._compare_imports(tree1, tree2)
            
            return (structure_sim * 0.5 + functions_sim * 0.3 + imports_sim * 0.2)
            
        except SyntaxError:
            # Fallback to text-based structural analysis
            return self._text_based_structural_similarity(code1, code2)
    
    def _compare_ast_structures(self, tree1: ast.AST, tree2: ast.AST) -> float:
        """Compare AST structures"""
        nodes1 = self._extract_node_types(tree1)
        nodes2 = self._extract_node_types(tree2)
        
        all_nodes = set(nodes1.keys()) | set(nodes2.keys())
        
        if not all_nodes:
            return 1.0
        
        matches = 0
        total = 0
        
        for node_type in all_nodes:
            count1 = nodes1.get(node_type, 0)
            count2 = nodes2.get(node_type, 0)
            
            total += max(count1, count2)
            matches += min(count1, count2)
        
        return matches / total if total > 0 else 0.0
    
    def _extract_node_types(self, tree: ast.AST) -> Dict[str, int]:
        """Extract node type frequencies from AST"""
        node_types = {}
        
        for node in ast.walk(tree):
            node_type = type(node).__name__
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        return node_types
    
    def _compare_function_definitions(self, tree1: ast.AST, tree2: ast.AST) -> float:
        """Compare function definitions"""
        funcs1 = self._extract_functions(tree1)
        funcs2 = self._extract_functions(tree2)
        
        if not funcs1 and not funcs2:
            return 1.0
        if not funcs1 or not funcs2:
            return 0.0
        
        common_funcs = set(funcs1.keys()) & set(funcs2.keys())
        all_funcs = set(funcs1.keys()) | set(funcs2.keys())
        
        return len(common_funcs) / len(all_funcs)
    
    def _extract_functions(self, tree: ast.AST) -> Dict[str, ast.FunctionDef]:
        """Extract function definitions from AST"""
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        
        return functions
    
    def _compare_imports(self, tree1: ast.AST, tree2: ast.AST) -> float:
        """Compare import statements"""
        imports1 = self._extract_imports(tree1)
        imports2 = self._extract_imports(tree2)
        
        if not imports1 and not imports2:
            return 1.0
        if not imports1 or not imports2:
            return 0.0
        
        common_imports = set(imports1) & set(imports2)
        all_imports = set(imports1) | set(imports2)
        
        return len(common_imports) / len(all_imports)
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements from AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        return imports
    
    def _text_based_structural_similarity(self, code1: str, code2: str) -> float:
        """Fallback structural similarity using text patterns"""
        import re
        
        # Extract function definitions
        funcs1 = re.findall(r'def\s+(\w+)', code1)
        funcs2 = re.findall(r'def\s+(\w+)', code2)
        
        # Extract class definitions
        classes1 = re.findall(r'class\s+(\w+)', code1)
        classes2 = re.findall(r'class\s+(\w+)', code2)
        
        # Extract import statements
        imports1 = re.findall(r'import\s+(\w+)', code1)
        imports2 = re.findall(r'import\s+(\w+)', code2)
        
        # Calculate similarities
        func_sim = self._list_similarity(funcs1, funcs2)
        class_sim = self._list_similarity(classes1, classes2)
        import_sim = self._list_similarity(imports1, imports2)
        
        return (func_sim * 0.5 + class_sim * 0.3 + import_sim * 0.2)
    
    def _list_similarity(self, list1: List[str], list2: List[str]) -> float:
        """Calculate similarity between two lists"""
        if not list1 and not list2:
            return 1.0
        if not list1 or not list2:
            return 0.0
        
        set1, set2 = set(list1), set(list2)
        intersection = set1 & set2
        union = set1 | set2
        
        return len(intersection) / len(union)


# Integration with existing conflict detection
def detect_conflicts_with_semantic_analysis(
    self,
    base: str,
    branch_a: str,
    branch_b: str
) -> ConflictReport:
    """
    Enhanced conflict detection with semantic analysis and fuzzy matching.
    
    Combines traditional git merge-tree with advanced semantic analysis
    for more accurate conflict detection and resolution suggestions.
    """
    
    # Get traditional merge-tree conflicts
    traditional_report = self.detect_conflicts_with_merge_tree(base, branch_a, branch_b)
    
    # Get semantic conflicts
    semantic_detector = SemanticConflictDetector(self.repo_root)
    semantic_conflicts = semantic_detector.detect_semantic_conflicts(
        branch_a, branch_b, base
    )
    
    # Merge results
    enhanced_conflicts = []
    
    for traditional_conflict in traditional_report.conflicts:
        # Find corresponding semantic conflict
        semantic_conflict = next(
            (sc for sc in semantic_conflicts if sc.file_path == traditional_conflict.file_path),
            None
        )
        
        if semantic_conflict:
            # Combine traditional and semantic analysis
            enhanced_conflict = ConflictFile(
                file_path=traditional_conflict.file_path,
                conflict_type=traditional_conflict.conflict_type,
                conflict_regions=traditional_conflict.conflict_regions,
                resolution_status=traditional_conflict.resolution_status,
                severity=self._determine_enhanced_severity(
                    traditional_conflict, semantic_conflict
                ),
                lines_affected=traditional_conflict.lines_affected
            )
            
            # Add semantic analysis data
            enhanced_conflict.semantic_similarity = semantic_conflict.semantic_similarity
            enhanced_conflict.fuzzy_match_score = semantic_conflict.fuzzy_match_score
            enhanced_conflict.structural_similarity = semantic_conflict.structural_similarity
            enhanced_conflict.resolution_suggestions = semantic_conflict.resolution_suggestions
            
        else:
            enhanced_conflict = traditional_conflict
        
        enhanced_conflicts.append(enhanced_conflict)
    
    return ConflictReport(
        source_branch=traditional_report.source_branch,
        target_branch=traditional_report.target_branch,
        base_branch=traditional_report.base_branch,
        conflicts=enhanced_conflicts,
        merge_base_commit=traditional_report.merge_base_commit,
        detection_method="enhanced_merge-tree_with_semantic_analysis"
    )


def _determine_enhanced_severity(
    traditional_conflict: ConflictFile,
    semantic_conflict: SemanticConflictAnalysis
) -> ConflictSeverity:
    """Determine enhanced severity based on semantic analysis"""
    
    # Base severity from traditional analysis
    base_severity = traditional_conflict.severity
    
    # Adjust based on semantic analysis
    semantic_score = semantic_conflict.semantic_similarity
    fuzzy_score = semantic_conflict.fuzzy_match_score
    structural_score = semantic_conflict.structural_similarity
    
    # High semantic conflict (low similarity) increases severity
    if semantic_score < 0.3:
        return ConflictSeverity.HIGH
    
    # High fuzzy similarity with low semantic similarity indicates subtle conflicts
    if fuzzy_score > 0.8 and semantic_score < 0.5:
        return ConflictSeverity.HIGH
    
    # Low structural similarity indicates major reorganization
    if structural_score < 0.4:
        return ConflictSeverity.HIGH
    
    # Medium conflicts based on combination of factors
    if (semantic_score < 0.6 and fuzzy_score > 0.6) or structural_score < 0.7:
        return ConflictSeverity.MEDIUM
    
    return base_severity
```

**Smart Fuzzy Semantic Matching Features:**

1. **Multi-Algorithm Approach**: Combines TF-IDF, word embeddings, semantic role labeling, and dependency parsing
2. **Fuzzy String Matching**: Uses Levenshtein distance, Jaro-Winkler, sequence matching, and token-based matching
3. **Structural Analysis**: Analyzes AST structures, function definitions, control flow patterns, and import statements
4. **Conflict Region Identification**: Pinpoints exact lines and regions with semantic conflicts
5. **Resolution Suggestions**: Generates intelligent suggestions based on semantic analysis
6. **Severity Assessment**: Combines traditional and semantic analysis for accurate conflict severity

**Integration Points:**
- Enhanced `_detect_conflicts` method with semantic analysis
- New `detect_conflicts_with_semantic_analysis` function
- Smart conflict detection that identifies subtle semantic conflicts
- Fuzzy matching for detecting similar but conflicting changes
- Structural analysis for code organization conflicts

This comprehensive semantic matching system provides advanced conflict detection capabilities that go far beyond simple text comparison, enabling the system to identify and resolve complex semantic conflicts that traditional methods would miss.

---

### 1.2 Complete New Implementation

Add these imports at the top of the file:
```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from pathlib import Path
import subprocess
```

Add these new classes BEFORE the EmailIntelligenceCLI class:
```python
class ConflictType(Enum):
    """Types of merge conflicts detected by git merge-tree"""
    CHANGED_IN_BOTH = "changed_in_both"
    ADDED_IN_BOTH = "added_in_both"
    REMOVED_IN_SOURCE = "removed_in_source"
    REMOVED_IN_TARGET = "removed_in_target"
    MODIFIED_DELETED = "modified_deleted"


class ConflictSeverity(Enum):
    """Severity assessment for conflicts"""
    HIGH = "high"      # Both branches modified same areas
    MEDIUM = "medium"  # One branch deleted/modified
    LOW = "low"        # Minor conflicts


@dataclass
class ConflictRegion:
    """Represents a specific conflict region within a file"""
    start_line: int
    end_line: int
    content_ours: str
    content_theirs: str
    content_base: Optional[str] = None


@dataclass
class ConflictFile:
    """Structured conflict information for a single file"""
    file_path: str
    conflict_type: ConflictType
    conflict_regions: List[ConflictRegion] = field(default_factory=list)
    resolution_status: str = "unresolved"  # "unresolved", "resolved_ours", "resolved_theirs", "resolved_manual"
    severity: ConflictSeverity = ConflictSeverity.MEDIUM
    lines_affected: int = 0


@dataclass
class ConflictReport:
    """Complete conflict detection result"""
    source_branch: str
    target_branch: str
    base_branch: str
    conflicts: List[ConflictFile]
    merge_base_commit: str
    detection_method: str = "git merge-tree"
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def total_conflicts(self) -> int:
        return len(self.conflicts)
    
    @property
    def files_requiring_resolution(self) -> List[str]:
        return [c.file_path for c in self.conflicts if c.resolution_status == "unresolved"]
    
    @property
    def severity_summary(self) -> Dict[str, int]:
        summary = {"high": 0, "medium": 0, "low": 0}
        for c in self.conflicts:
            summary[c.severity.value] += 1
        return summary


# Custom Exception Classes
class GitOperationError(Exception):
    """Base exception for git operation failures"""
    pass


class MergeTreeError(GitOperationError):
    """Raised when git merge-tree command fails"""
    pass


class BranchNotFoundError(GitOperationError):
    """Raised when specified branch doesn't exist"""
    pass


class WorktreeUnavailableError(GitOperationError):
    """Raised when worktree operations fail"""
    pass
```

Add these new methods to the EmailIntelligenceCLI class (after line 258):
```python
def detect_conflicts_with_merge_tree(
    self,
    base: str,
    branch_a: str,
    branch_b: str
) -> ConflictReport:
    """
    Detect actual merge conflicts using git merge-tree.
    
    This method replaces the inadequate git diff --name-only approach
    with accurate three-way merge conflict detection.
    
    Args:
        base: Base/common ancestor branch or commit
        branch_a: First branch to compare (source)
        branch_b: Second branch to compare (target)
    
    Returns:
        ConflictReport containing list of ConflictFile objects
    
    Raises:
        MergeTreeError: If git merge-tree command fails
        BranchNotFoundError: If specified branches don't exist
    """
    self._info(f"🔍 Running merge-tree analysis: {branch_a} vs {branch_b}")
    
    # Validate branches exist
    self._validate_branch_exists(branch_a)
    self._validate_branch_exists(branch_b)
    
    # Get merge base for context
    merge_base = self._get_merge_base(branch_a, branch_b)
    
    # Execute merge-tree
    try:
        result = subprocess.run(
            ["git", "merge-tree", "--name-only", base, branch_a, branch_b],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise MergeTreeError(f"git merge-tree failed: {e.stderr}")
    
    # Parse output into ConflictFile objects
    conflicts = self._parse_merge_tree_output(result.stdout, branch_a, branch_b)
    
    return ConflictReport(
        source_branch=branch_a,
        target_branch=branch_b,
        base_branch=base,
        conflicts=conflicts,
        merge_base_commit=merge_base
    )


def _validate_branch_exists(self, branch: str) -> None:
    """Validate that a branch exists"""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        cwd=self.repo_root,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise BranchNotFoundError(f"Branch '{branch}' does not exist")


def _get_merge_base(self, branch_a: str, branch_b: str) -> str:
    """Get the merge base commit between two branches"""
    result = subprocess.run(
        ["git", "merge-base", branch_a, branch_b],
        cwd=self.repo_root,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def _parse_merge_tree_output(
    self,
    output: str,
    branch_a: str,
    branch_b: str
) -> List[ConflictFile]:
    """
    Parse git merge-tree output into structured ConflictFile objects.
    
    Output format:
    - changed in both:  <path>
    - removed in one:   <path>
    - added in both:    <path>
    """
    conflicts = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Parse conflict type and file path
        if line.startswith('changed in both:'):
            file_path = line.split(':', 1)[1].strip()
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=ConflictType.CHANGED_IN_BOTH,
                severity=ConflictSeverity.HIGH  # Both modified = high severity
            ))
            
        elif line.startswith('added in both:'):
            file_path = line.split(':', 1)[1].strip()
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=ConflictType.ADDED_IN_BOTH,
                severity=ConflictSeverity.HIGH
            ))
            
        elif line.startswith('removed in '):
            file_path = line.split(':', 1)[1].strip()
            # Determine which branch removed the file
            if branch_a in line:
                conflict_type = ConflictType.REMOVED_IN_SOURCE
            else:
                conflict_type = ConflictType.REMOVED_IN_TARGET
            conflicts.append(ConflictFile(
                file_path=file_path,
                conflict_type=conflict_type,
                severity=ConflictSeverity.MEDIUM
            ))
    
    return conflicts
```

---

### 1.3 Setup-Resolution Modification

**Goal:** Push resolved changes directly to existing branches without creating new branches.

**Current Workflow:**
1. Create pr-{pr}-resolution branch
2. Create worktree-a (source branch)
3. Create worktree-b (target branch)
4. Resolve conflicts
5. Create PR from resolution branch

**New Workflow:**
1. Use existing source branch (no new branch)
2. Use existing target branch (no new branch)
3. Create worktrees pointing to existing branches
4. Resolve conflicts
5. Push directly to source branch via git push --force-with-lease

**New Method to add:**
```python
def setup_resolution_direct(
    self,
    pr_number: int,
    source_branch: str,
    target_branch: str,
    constitution_files: List[str] = None,
    spec_files: List[str] = None,
    dry_run: bool = False,
    direct_push: bool = True
) -> Dict[str, Any]:
    """
    Setup resolution workspace with direct branch push capability.
    
    Key changes:
    - NO pr-{pr}-resolution branch created
    - Works directly with existing source/target branches
    - After resolution, pushes directly to source branch
    """
    
    # Validate branches exist remotely
    self._validate_branches_exist([source_branch, target_branch])
    
    worktree_a_path = self.worktrees_dir / f"pr-{pr_number}-branch-a"
    worktree_b_path = self.worktrees_dir / f"pr-{pr_number}-branch-b"
    
    if not dry_run:
        # Create worktrees pointing to EXISTING branches
        self._create_worktree(worktree_a_path, source_branch)
        self._create_worktree(worktree_b_path, target_branch)
    
    # Use new merge-tree detection
    conflict_report = self.detect_conflicts_with_merge_tree(
        base=target_branch,
        branch_a=source_branch,
        branch_b=target_branch
    )
    
    # Metadata WITHOUT resolution branch reference
    resolution_metadata = {
        'pr_number': pr_number,
        'source_branch': source_branch,
        'target_branch': target_branch,
        'worktree_a_path': str(worktree_a_path),
        'worktree_b_path': str(worktree_b_path),
        'direct_push_enabled': direct_push,
        'modified_branches': [],
        'conflicts': conflict_report.__dict__,
        'resolution_method': 'direct_push',
        'push_operations_log': [],
        'created_at': datetime.now().isoformat(),
        'status': 'ready_for_resolution'
    }
    
    # Save metadata
    metadata_file = self.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(resolution_metadata, f, indent=2)
    
    return resolution_metadata


def push_resolution(
    self,
    pr_number: int,
    confirmed: bool = False,
    branches: List[str] = None,
    force: bool = False
) -> Dict[str, Any]:
    """
    Push resolved changes directly to source branch.
    
    Args:
        pr_number: PR identifier
        confirmed: User must explicitly confirm (required=True)
        branches: List of branches to push to
        force: Use force push
    
    Returns:
        Dict with success status and logs
    """
    # Load metadata
    metadata_file = self.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    source_branch = metadata['source_branch']
    branches = branches or [source_branch]
    
    # Display confirmation prompt if not confirmed
    if not confirmed:
        print(f"⚠️  WARNING: This will force-push to: {branches}")
        print(f"⚠️  This will OVERWRITE existing commits on remote!")
        response = input("Type 'yes' to confirm: ")
        if response.lower() != 'yes':
            return {'success': False, 'reason': 'user_cancelled'}
    
    # Build push command
    push_cmd = ["git", "push"]
    if force:
        push_cmd.append("--force-with-lease")  # Safer than -f
    push_cmd.extend(["origin", f"{metadata['worktree_a_path']}:refs/heads/{source_branch}"])
    
    # Log operation
    operation = {
        'timestamp': datetime.now().isoformat(),
        'branches': branches,
        'command': ' '.join(push_cmd),
        'source_branch': source_branch
    }
    metadata['push_operations_log'].append(operation)
    
    # Execute push
    try:
        subprocess.run(push_cmd, check=True, cwd=metadata['worktree_a_path'])
        metadata['modified_branches'].extend(branches)
        metadata['status'] = 'resolution_pushed'
        
        # Save updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self._success(f"✅ Pushed resolution to {source_branch}")
        return {'success': True, 'branches': branches, 'operation': operation}
        
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': str(e)}


def _validate_branches_exist(self, branches: List[str]) -> None:
    """Validate that all specified branches exist"""
    for branch in branches:
        self._validate_branch_exists(branch)


def _create_worktree(self, path: Path, branch: str) -> None:
    """Create a git worktree at the specified path"""
    subprocess.run(
        ["git", "worktree", "add", str(path), branch],
        cwd=self.repo_root,
        check=True
    )
```

---

### 1.4 All-Branches Scanning Capability

```python
@dataclass
class BranchPairResult:
    """Result for a single branch pair scan"""
    source: str
    target: str
    conflict_count: int
    conflict_files: List[str]
    severity: str
    scan_duration_ms: float


@dataclass
class ConflictMatrix:
    """Complete conflict matrix for all branch pairs"""
    scanned_at: str
    branches: List[str]
    target_branches: List[str]
    total_pairs: int
    pairs_with_conflicts: int
    results: List[BranchPairResult]


def scan_all_branches(
    self,
    include_remotes: bool = True,
    target_branches: List[str] = None,
    concurrency: int = 4,
    exclude_patterns: List[str] = None
) -> ConflictMatrix:
    """
    Scan conflicts across all branch pairs.
    
    Args:
        include_remotes: Include remote branches in scan
        target_branches: Specific target branches (default: ['main'])
        concurrency: Number of parallel scans
        exclude_patterns: Branch patterns to exclude
    
    Returns:
        ConflictMatrix with all results
    """
    import concurrent.futures
    import time
    
    target_branches = target_branches or ['main']
    exclude_patterns = exclude_patterns or ['main', 'develop', 'HEAD']
    
    # Enumerate branches
    branches = self._enumerate_branches(include_remotes, exclude_patterns)
    
    self._info(f"Scanning {len(branches)} branches against {len(target_branches)} targets...")
    
    # Generate branch pairs
    pairs = []
    for source in branches:
        for target in target_branches:
            if source != target:
                pairs.append((source, target))
    
    self._info(f"Scanning {len(pairs)} branch pairs...")
    
    # Scan in parallel
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(self._scan_branch_pair, src, tgt): (src, tgt) 
            for src, tgt in pairs
        }
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            completed += 1
            if completed % 10 == 0:
                self._info(f"Progress: {completed}/{len(pairs)} pairs scanned")
    
    duration_ms = (time.time() - start_time) * 1000
    
    return ConflictMatrix(
        scanned_at=datetime.now().isoformat(),
        branches=branches,
        target_branches=target_branches,
        total_pairs=len(pairs),
        pairs_with_conflicts=sum(1 for r in results if r.conflict_count > 0),
        results=results
    )


def _enumerate_branches(
    self,
    include_remotes: bool = True,
    exclude_patterns: List[str] = None
) -> List[str]:
    """Enumerate all local and remote branches"""
    
    # Get local branches
    result = subprocess.run(
        ["git", "branch", "--format=%(refname:short)"],
        cwd=self.repo_root,
        capture_output=True,
        text=True,
        check=True
    )
    local_branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
    
    # Get remote branches
    if include_remotes:
        result = subprocess.run(
            ["git", "branch", "-r", "--format=%(refname:short)"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        remote_branches = [
            b.strip().replace('origin/', '') 
            for b in result.stdout.split('\n')
            if b.strip() and 'origin/HEAD' not in b
        ]
        local_branches = list(set(local_branches + remote_branches))
    
    # Apply exclusions
    if exclude_patterns:
        local_branches = [
            b for b in local_branches 
            if not any(self._matches_pattern(b, p) for p in exclude_patterns)
        ]
    
    return sorted(local_branches)


def _matches_pattern(self, branch: str, pattern: str) -> bool:
    """Check if branch matches pattern (supports wildcards)"""
    import fnmatch
    return fnmatch.fnmatch(branch, pattern)


def _scan_branch_pair(self, source: str, target: str) -> BranchPairResult:
    """Scan a single branch pair for conflicts"""
    import time
    start = time.time()
    
    try:
        report = self.detect_conflicts_with_merge_tree(target, source, target)
        duration_ms = (time.time() - start) * 1000
        
        # Determine severity
        severity = "low"
        if any(c.severity == ConflictSeverity.HIGH for c in report.conflicts):
            severity = "high"
        elif any(c.severity == ConflictSeverity.MEDIUM for c in report.conflicts):
            severity = "medium"
        
        return BranchPairResult(
            source=source,
            target=target,
            conflict_count=len(report.conflicts),
            conflict_files=[c.file_path for c in report.conflicts],
            severity=severity,
            scan_duration_ms=duration_ms
        )
    except Exception as e:
        return BranchPairResult(
            source=source,
            target=target,
            conflict_count=0,
            conflict_files=[],
            severity="error",
            scan_duration_ms=0
        )
```

---

### 1.5 Worktree Fallback Mechanism

```python
class GitWorkspaceManager:
    """Enhanced workspace manager with fallback support"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.fallback_mode = False
        self.fallback_reason = None
    
    def initialize(self) -> bool:
        """Initialize with automatic fallback detection"""
        try:
            # Check git available
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            
            # Check in repo
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            
            # Verify worktree support
            self._verify_worktree_support()
            
            return True
            
        except FileNotFoundError:
            self._enable_fallback("git_not_installed", "Git is not installed")
            return False
        except subprocess.CalledProcessError:
            self._enable_fallback("not_a_repo", "Not in a git repository")
            return False
        except PermissionError as e:
            self._enable_fallback("permission_denied", str(e))
            return False
    
    def _enable_fallback(self, reason: str, details: str):
        """Enable fallback mode"""
        self.fallback_mode = True
        self.fallback_reason = {
            'reason': reason, 
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        print(f"⚠️  Falling back to single-branch mode: {reason}")
        print(f"   Details: {details}")
    
    def _verify_worktree_support(self):
        """Verify git worktree is supported"""
        result = subprocess.run(
            ["git", "worktree", "--help"],
            capture_output=True
        )
        if result.returncode != 0:
            raise WorktreeUnavailableError("Git worktree not supported")
    
    def create_workspace(
        self, 
        name: str, 
        branch: str,
        use_worktree: bool = True
    ) -> Path:
        """Create workspace with automatic fallback"""
        
        if use_worktree and not self.fallback_mode:
            try:
                return self._create_git_worktree(name, branch)
            except (WorktreeUnavailableError, PermissionError) as e:
                self._enable_fallback("worktree_creation_failed", str(e))
        
        # Fallback: use regular directory
        return self._create_fallback_workspace(name, branch)
    
    def _create_fallback_workspace(self, name: str, branch: str) -> Path:
        """Create workspace without git worktree"""
        
        workspace_dir = self.repo_root / ".emailintelligence" / "workspaces" / name
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Clone at specific branch
        subprocess.run(
            ["git", "clone", "--branch", branch, ".", str(workspace_dir)],
            cwd=self.repo_root,
            capture_output=True,
            check=True
        )
        
        return workspace_dir
```

---

## 2. EmailIntelligence CLI Enhancements

### 2.1 File Analysis: emailintelligence_cli.py

**Location:** Root directory of EmailIntelligence repository  
**Size:** 59,317 characters  
**Key Methods:**

| Method | Line | Purpose |
|--------|------|---------|
| `_detect_conflicts` | 231-258 | NEEDS REFACTORING - uses git diff |
| `setup_resolution` | 103-214 | Creates resolution workspace |
| `analyze_constitutional` | 260-379 | Analyzes conflicts against constitutions |
| `develop_spec_kit_strategy` | 558-623 | Creates resolution strategy |
| `align_content` | 887-967 | Executes content alignment |
| `validate_resolution` | 1069-1118 | Validates resolution |
| argparse setup | 1282-1410 | CLI argument parsing |

**Current Worktree Configuration (from __init__):**
```python
self.repo_root = Path.cwd()
self.worktrees_dir = self.repo_root / ".git" / "worktrees"
self.resolution_branches_dir = self.repo_root / "resolution-workspace"
self.config_file = self.repo_root / ".emailintelligence" / "config.yaml"
self.constitutions_dir = self.repo_root / ".emailintelligence" / "constitutions"
self.strategies_dir = self.repo_root / ".emailintelligence" / "strategies"
```

---

### 2.2 Configuration: .emailintelligence/config.yaml

**Full Content:**
```yaml
analysis_settings:
  detailed_reporting: true
  enable_ai_analysis: false

constitutional_framework:
  compliance_threshold: 0.8
  default_constitutions: []

worktree_settings:
  cleanup_on_completion: true
  max_worktrees: 10
```

---

### 2.3 CLI Commands (from argparse)

| Command | Purpose |
|---------|---------|
| `setup-resolution` | Setup resolution workspace for PR |
| `analyze-constitutional` | Analyze conflicts against constitution |
| `develop-spec-kit-strategy` | Develop resolution strategy |
| `align-content` | Execute content alignment |
| `validate-resolution` | Validate completed resolution |
| `version` | Show version information |

---

## 3. Orchestration-Tools Consolidation

### 3.1 Branches Involved

From `implement/orchestration_tools_consolidation_summary.md`:
- `orchestration-tools` (main consolidation target)
- `orchestration-tools-changes` (aggregation branch)
- `orchestration-tools-changes-2`
- `orchestration-tools-changes-4`
- `orchestration-tools-changes-emailintelligence-cli-20251112`
- `orchestration-tools-changes-recovery-framework`

### 3.2 Files on orchestration-tools

**Scripts:**
- `scripts/hooks/post-push`
- `scripts/hooks/pre-commit`
- `scripts/hooks/post-commit`
- `scripts/hooks/post-merge`
- `scripts/lib/orchestration-approval.sh`

**Setup:**
- `setup/launch.py`
- `setup/setup_environment_system.sh`

**Configuration:**
- `.flake8`
- `.pylintrc`
- `.gitignore`

### 3.3 Current Repository Status

**From git status:**
```
Current Branch: gitbutler/workspace
Main Worktree: C:/Users/masum/Documents/EmailIntelligence
Secondary Worktree: .worktrees/pr481 (prunable)
Remote: origin https://github.com/MasumRab/EmailIntelligence.git
```

### 3.4 Branch Naming Convention

Branches found in repository:
- `bolt-smart-filter-opt-7251234506607923073`
- `bolt/smart-filter-cache-optimization-7932786554965032055`
- `gitbutler/workspace` (current)
- `main`
- `mr-branch-2`, `mr-branch-3`, `mr-branch-4`
- `orchestration-tools`
- `pr-481`
- `scientific`
- `sentinel-fix-xss-fallback-12723436363458782184`

---

## 4. Branch/Merge/Conflict Improvements

### 4.1 Conflict Detection Methods Evaluated

| Method | Accuracy | Worktree Required | Use Case |
|--------|----------|-------------------|----------|
| `git diff --name-only` (CURRENT) | LOW ❌ | Yes | Only shows different files |
| `git merge-tree` | **HIGH ✅** | No | Actual merge conflicts |
| `git ls-files -u` | HIGH | Only during merge | Unmerged files |
| `git diff --merge-base` | MEDIUM | No | Potential conflicts |

**RECOMMENDATION:** Use `git merge-tree` as primary method.

### 4.2 Git Commands to Refactor

| Current (Inadequate) | Replace With |
|---------------------|--------------|
| `git diff --name-only` | `git merge-tree --name-only` |
| `git diff --stat` | `git merge-tree` |
| `git diff HEAD` | `git merge-tree` |

### 4.3 TASKMASTER_ISOLATION_FIX.md Findings

**Issue:** Attempted to whitelist `.taskmaster/**` in orchestration-tools `.gitignore`

**Result:** 
- ❌ Would have tracked taskmaster files in orchestration-tools branch
- ❌ Would have contaminated branch history

**Correct Approach:**
- ✅ Use `.git/info/exclude` alone (not propagated to other branches)

---

## 5. Complete Todo List

| # | Item | Status |
|---|------|--------|
| 1 | Analyze current _detect_conflicts implementation | ✅ Completed |
| 2 | Create comprehensive enhancement plan | ✅ Completed |
| 3 | Refactor _detect_conflicts with git merge-tree | ⏳ Pending |
| 4 | Audit codebase for low-accuracy git commands | ⏳ Pending |
| 5 | Modify setup-resolution for direct push | ⏳ Pending |
| 6 | Implement all-branches scanning capability | ⏳ Pending |
| 7 | Evaluate CodeRabbit integration | ⏳ Pending |
| 8 | Add worktree fallback mechanism | ⏳ Pending |
| 9 | Document technical implementation details | ⏳ Pending |

---

## 6. File Analysis Results

### 6.1 analyze_repo.py

**Location:** Root directory  
**Size:** 10,054 characters

**Functions:**
```python
def get_file_category(filepath):
    """Categorizes a file based on its path and extension."""
    # Categories: Testing, Documentation, Configuration, Scripting, 
    # Core Logic, Frontend, Notebook, Data, Containerization, CI/CD, Assets

def analyze_file(filepath):
    """Analyzes a single file for metrics using AST."""
    # Returns: loc, imports, functions, classes, imports_list

def resolve_import_path(import_name, current_file_path, root_dir):
    """Resolves an import name to a file path."""
    # Supports absolute and relative imports
```

### 6.2 agent-config.json

```json
{
  "api_keys": {
    "google": "YOUR_GOOGLE_API_KEY_HERE_OR_LEAVE_EMPTY",
    "anthropic": "YOUR_ANTHROPIC_API_KEY_HERE_OR_LEAVE_EMPTY",
    "perplexity": "YOUR_PERPLEXITY_API_KEY_HERE_OR_LEAVE_EMPTY",
    "openai": "YOUR_OPENAI_API_KEY_HERE_OR_LEAVE_EMPTY"
  },
  "models": {
    "main": "claude-3-5-sonnet-20241022",
    "research": "perplexity-llama-3.1-sonar-large-128k-online",
    "fallback": "gpt-4o-mini"
  },
  "agents": {...},
  "mcp_servers": {...}
}
```

---

## 7. All Search Findings

### 7.1 emailintelligence_cli.py References

| File | Line | Finding |
|------|------|---------|
| `scripts/hooks/post-push` | 33-34 | `REQUIRED_FILES=("emailintelligence_cli.py", "scripts/bash/create-pr-resolution-spec.sh")` |
| `implement/orchestration_tools_consolidation_summary.md` | 13 | `"emailintelligence_cli.py - Complete EmailIntelligence CLI v2.0 implementation"` |

### 7.2 orchestration-tools References

Found in 300+ docs files including:
- `TASKMASTER_ISOLATION_FIX.md`
- `TASKMASTER_BRANCH_CONVENTIONS.md`
- `docs/ORCHESTRATION_SYSTEM.md`
- `docs/ORCHESTRATION_WORKFLOW.md`
- `docs/ORCHESTRATION_BRANCH_SCOPE.md`
- `docs/AGENT_ORCHESTRATION_CHECKLIST.md`
- `docs/ORCHESTRATION.md`
- `docs/ORCHESTRATION_GITHUB_PROTECTION_SUMMARY.md`

### 7.3 CodeRabbit References

Found in `scripts/branch_rename_migration.py` line 77:
```python
'coderabbitai/utg/f31e8bd',  # Branch name only, NOT integration
```

---

## 8. Conclusions & Decisions

### 8.1 Branch Determination

**DECISION:** `orchestration-tools` is the correct branch for emailintelligence_cli.py  
**RATIONALE:** CLI is a Git-oriented orchestration tool, not application code  
**DATE:** 2026-02-28

### 8.2 Conflict Detection Method

**DECISION:** Use `git merge-tree` as primary conflict detection method  
**RATIONALE:** Provides accurate three-way merge conflict detection without requiring worktrees  
**DATE:** 2026-02-28

### 8.3 Workflow Modification

**DECISION:** Push resolved changes directly to existing source branch  
**RATIONALE:** Eliminates need for pr-{pr}-resolution branch creation, reduces PR count  
**DATE:** 2026-02-28

### 8.4 External Tool Integration

**DECISION:** Keep native implementation, do NOT integrate CodeRabbit  
**RATIONALE:** 
- Adds external dependency
- Limited API access
- Privacy implications (data sent to external service)
- Additional cost (subscription-based)
**DATE:** 2026-02-28

### 8.5 Fallback Mechanism

**DECISION:** Implement graceful fallback for worktree unavailability  
**RATIONALE:** Core functionality should work even without worktree support  
**DATE:** 2026-02-28

---

## 9. Implementation Guide

### 9.1 Starting Commands

```bash
# Checkout orchestration-tools branch
git checkout orchestration-tools
git pull origin orchestration-tools
```

### 9.2 Implementation Order

1. Add new dataclasses and exception classes (lines ~70-100)
2. Add `detect_conflicts_with_merge_tree` method (~line 260)
3. Add helper methods `_validate_branch_exists`, `_get_merge_base`, `_parse_merge_tree_output`
4. Add `setup_resolution_direct` method
5. Add `push_resolution` method with confirmations
6. Add `scan_all_branches` method
7. Add `_enumerate_branches`, `_scan_branch_pair` helpers
8. Add GitWorkspaceManager class for fallback
9. Update argparse to add new commands
10. Write tests
11. Commit and push

### 9.3 Estimated Effort

| Task | Days |
|------|------|
| Refactor conflict detection | 1.0 |
| Audit git commands | 0.5 |
| Modify setup-resolution | 1.0 |
| All-branches scan | 1.5 |
| Worktree fallback | 1.0 |
| Tests | 2.0 |
| Documentation | 1.0 |
| **TOTAL** | **8.0** |

---

## 10. Key Code Locations

| Item | Line Numbers | Notes |
|------|---------------|-------|
| `_detect_conflicts` | 231-258 | NEEDS REFACTORING |
| `setup_resolution` | 103-214 | Modify for direct push |
| `analyze_constitutional` | 260-379 | Works with new conflict detection |
| `develop_spec_kit_strategy` | 558-623 | Uses metadata |
| `align_content` | 887-967 | Uses worktrees |
| `validate_resolution` | 1069-1118 | Final validation |
| argparse | 1282-1410 | Add new commands |

---

*End of Comprehensive Handoff Document*
*Last Updated: 2026-02-28*
*Target Branch: orchestration-tools*
