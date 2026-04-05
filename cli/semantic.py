"""
EmailIntelligence CLI - Smart Fuzzy Semantic Matching

This module provides advanced semantic conflict detection using multiple matching
techniques: TF-IDF, embeddings, fuzzy string matching, and structural analysis.
"""

import logging
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Set, Tuple

from cli.models import ConflictRegion, SemanticConflictAnalysis

# Try to import optional dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# FUZZY MATCHER
# ============================================================================


class FuzzyMatcher:
    """Fuzzy string matching using multiple algorithms."""
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return FuzzyMatcher.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def levenshtein_similarity(s1: str, s2: str) -> float:
        """Calculate normalized Levenshtein similarity (0.0 to 1.0)."""
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        
        max_len = max(len(s1), len(s2))
        distance = FuzzyMatcher.levenshtein_distance(s1, s2)
        return 1.0 - (distance / max_len)
    
    @staticmethod
    def jaro_winkler_similarity(s1: str, s2: str, winkler_prefix_weight: float = 0.1) -> float:
        """Calculate Jaro-Winkler similarity (0.0 to 1.0)."""
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        
        # Jaro similarity
        len_s1, len_s2 = len(s1), len(s2)
        match_distance = max(len_s1, len_s2) // 2 - 1
        match_distance = max(0, match_distance)
        
        s1_matches = [False] * len_s1
        s2_matches = [False] * len_s2
        
        matches = 0
        transpositions = 0
        
        for i in range(len_s1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len_s2)
            
            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break
        
        if matches == 0:
            return 0.0
        
        k = 0
        for i in range(len_s1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
        
        jaro = (matches / len_s1 + matches / len_s2 + 
                (matches - transpositions / 2) / matches) / 3
        
        # Winkler modification
        prefix_len = 0
        for i in range(min(4, len_s1, len_s2)):
            if s1[i] == s2[i]:
                prefix_len += 1
            else:
                break
        
        return jaro + prefix_len * winkler_prefix_weight * (1 - jaro)
    
    @staticmethod
    def sequence_matcher_similarity(s1: str, s2: str) -> float:
        """Calculate similarity using SequenceMatcher (0.0 to 1.0)."""
        return SequenceMatcher(None, s1, s2).ratio()
    
    @staticmethod
    def token_based_similarity(s1: str, s2: str) -> float:
        """Calculate token-based similarity (Jaccard on tokens)."""
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        
        tokens1 = set(re.findall(r'\w+', s1.lower()))
        tokens2 = set(re.findall(r'\w+', s2.lower()))
        
        if not tokens1 and not tokens2:
            return 1.0
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union) if union else 0.0
    
    @classmethod
    def compute_composite_score(cls, s1: str, s2: str) -> float:
        """Compute composite fuzzy match score using multiple techniques."""
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        
        # Weight different methods
        levenshtein = cls.levenshtein_similarity(s1, s2)
        jaro_winkler = cls.jaro_winkler_similarity(s1, s2)
        sequence = cls.sequence_matcher_similarity(s1, s2)
        token = cls.token_based_similarity(s1, s2)
        
        # Weighted average (sequence matcher is usually most reliable)
        return (0.2 * levenshtein + 0.3 * jaro_winkler + 
                0.3 * sequence + 0.2 * token)
    
    @classmethod
    def match_lines(cls, lines_a: List[str], lines_b: List[str]) -> float:
        """Match two lists of lines and return similarity score."""
        if not lines_a and not lines_b:
            return 1.0
        if not lines_a or not lines_b:
            return 0.0
        
        # Join and compare as strings
        content_a = '\n'.join(lines_a)
        content_b = '\n'.join(lines_b)
        return cls.compute_composite_score(content_a, content_b)


# ============================================================================
# SEMANTIC ANALYZER
# ============================================================================


class SemanticAnalyzer:
    """Semantic analysis using TF-IDF and embeddings."""
    
    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None
        self._initialize_vectorizer()
    
    def _initialize_vectorizer(self) -> None:
        """Initialize TF-IDF vectorizer if sklearn is available."""
        if SKLEARN_AVAILABLE:
            try:
                self.vectorizer = TfidfVectorizer(
                    analyzer='char_wb',
                    ngram_range=(2, 4),
                    max_features=5000
                )
            except Exception as e:
                logger.warning(f"Failed to initialize TF-IDF vectorizer: {e}")
                self.vectorizer = None
    
    def compute_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Compute TF-IDF based similarity."""
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        
        if not SKLEARN_AVAILABLE or self.vectorizer is None:
            return self._fallback_tfidf_similarity(text1, text2)
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.warning(f"TF-IDF similarity computation failed: {e}")
            return self._fallback_tfidf_similarity(text1, text2)
    
    def _fallback_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Fallback TF-IDF-like similarity without sklearn."""
        # Simple word frequency based similarity
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0
    
    def analyze_semantic_roles(self, content: str) -> Dict[str, Any]:
        """Analyze semantic roles in code content."""
        roles = {
            'functions': self._extract_functions(content),
            'classes': self._extract_classes(content),
            'imports': self._extract_imports(content),
            'variables': self._extract_variables(content),
            'comments': self._extract_comments(content)
        }
        return roles
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names."""
        patterns = [
            r'def\s+(\w+)',
            r'function\s+(\w+)',
            r'fn\s+(\w+)',
            r'def\s+(\w+)\s*\(',
        ]
        return self._extract_by_patterns(content, patterns)
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names."""
        patterns = [
            r'class\s+(\w+)',
            r'interface\s+(\w+)',
            r'struct\s+(\w+)',
        ]
        return self._extract_by_patterns(content, patterns)
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        patterns = [
            r'import\s+([^\s;]+)',
            r'from\s+([^\s]+)\s+import',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
        ]
        return self._extract_by_patterns(content, patterns)
    
    def _extract_variables(self, content: str) -> List[str]:
        """Extract variable names."""
        patterns = [
            r'\b(\w+)\s*=',
            r'let\s+(\w+)',
            r'const\s+(\w+)',
            r'var\s+(\w+)',
        ]
        return self._extract_by_patterns(content, patterns)
    
    def _extract_comments(self, content: str) -> List[str]:
        """Extract comments."""
        patterns = [
            r'//\s*(.+)$',
            r'#\s*(.+)$',
            r'/\*\s*(.+?)\s*\*/',
        ]
        return self._extract_by_patterns(content, patterns)
    
    def _extract_by_patterns(self, content: str, patterns: List[str]) -> List[str]:
        """Extract matches from content using multiple patterns."""
        results = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            results.update(matches)
        return list(results)
    
    def compute_role_similarity(self, roles1: Dict[str, Any], roles2: Dict[str, Any]) -> float:
        """Compute similarity based on semantic roles."""
        similarities = []
        
        for role_type in ['functions', 'classes', 'imports']:
            set1 = set(roles1.get(role_type, []))
            set2 = set(roles2.get(role_type, []))
            
            if not set1 and not set2:
                similarities.append(1.0)
            elif not set1 or not set2:
                similarities.append(0.0)
            else:
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                similarities.append(intersection / union if union > 0 else 0.0)
        
        return sum(similarities) / len(similarities) if similarities else 0.0


# ============================================================================
# STRUCTURAL ANALYZER
# ============================================================================


class StructuralAnalyzer:
    """Structural analysis for code comparison."""
    
    def __init__(self):
        self.fuzzy_matcher = FuzzyMatcher()
    
    def compute_structural_similarity(self, content_a: str, content_b: str) -> float:
        """Compute structural similarity between two code contents."""
        if not content_a and not content_b:
            return 1.0
        if not content_a or not content_b:
            return 0.0
        
        # Extract structural elements
        structure_a = self._extract_structure(content_a)
        structure_b = self._extract_structure(content_b)
        
        # Compare structures
        return self._compare_structures(structure_a, structure_b)
    
    def _extract_structure(self, content: str) -> Dict[str, Any]:
        """Extract structural elements from code."""
        return {
            'indent_pattern': self._analyze_indentation(content),
            'line_density': self._calculate_line_density(content),
            'brackets': self._count_brackets(content),
            'structure_markers': self._extract_structure_markers(content)
        }
    
    def _analyze_indentation(self, content: str) -> Dict[str, Any]:
        """Analyze indentation patterns."""
        lines = content.split('\n')
        indents = []
        
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                indents.append(indent)
        
        if not indents:
            return {'type': 'unknown', 'size': 0}
        
        avg_indent = sum(indents) / len(indents)
        
        # Determine indent type
        if avg_indent == 0:
            indent_type = 'none'
        elif avg_indent % 4 == 0:
            indent_type = '4spaces'
        elif avg_indent % 2 == 0:
            indent_type = '2spaces'
        elif avg_indent % 3 == 0:
            indent_type = '3spaces'
        else:
            indent_type = 'tabs' if '\t' in content else 'mixed'
        
        return {'type': indent_type, 'size': avg_indent}
    
    def _calculate_line_density(self, content: str) -> float:
        """Calculate code line density (non-empty / total)."""
        lines = content.split('\n')
        if not lines:
            return 0.0
        
        non_empty = sum(1 for line in lines if line.strip())
        return non_empty / len(lines)
    
    def _count_brackets(self, content: str) -> Dict[str, int]:
        """Count different bracket types."""
        return {
            'parentheses': content.count('(') + content.count(')'),
            'braces': content.count('{') + content.count('}'),
            'brackets': content.count('[') + content.count(']'),
            'angles': content.count('<') + content.count('>')
        }
    
    def _extract_structure_markers(self, content: str) -> List[str]:
        """Extract structural markers from code."""
        markers = []
        
        # Find all function/class definitions
        patterns = [
            (r'def\s+(\w+)', 'function'),
            (r'class\s+(\w+)', 'class'),
            (r'function\s+(\w+)', 'function'),
            (r'fn\s+(\w+)', 'function'),
            (r'def\s+(\w+)\s*\(', 'method'),
            (r'if\s*\(', 'if'),
            (r'for\s*\(', 'for'),
            (r'while\s*\(', 'while'),
            (r'return\s+', 'return'),
        ]
        
        for pattern, marker_type in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                markers.append(f"{marker_type}:{match}")
        
        return markers
    
    def _compare_structures(self, struct_a: Dict[str, Any], 
                           struct_b: Dict[str, Any]) -> float:
        """Compare two structures and return similarity score."""
        scores = []
        
        # Compare indentation
        indent_a = struct_a.get('indent_pattern', {}).get('type', 'unknown')
        indent_b = struct_b.get('indent_pattern', {}).get('type', 'unknown')
        scores.append(1.0 if indent_a == indent_b else 0.0)
        
        # Compare line density
        density_a = struct_a.get('line_density', 0)
        density_b = struct_b.get('line_density', 0)
        density_diff = abs(density_a - density_b)
        scores.append(1.0 - density_diff)
        
        # Compare brackets
        brackets_a = struct_a.get('brackets', {})
        brackets_b = struct_b.get('brackets', {})
        bracket_scores = []
        for key in brackets_a:
            if key in brackets_b:
                count_a, count_b = brackets_a[key], brackets_b[key]
                max_count = max(count_a, count_b, 1)
                bracket_scores.append(1.0 - abs(count_a - count_b) / max_count)
        if bracket_scores:
            scores.append(sum(bracket_scores) / len(bracket_scores))
        
        # Compare structure markers
        markers_a = set(struct_a.get('structure_markers', []))
        markers_b = set(struct_b.get('structure_markers', []))
        if markers_a and markers_b:
            intersection = len(markers_a & markers_b)
            union = len(markers_a | markers_b)
            scores.append(intersection / union if union > 0 else 0.0)
        elif not markers_a and not markers_b:
            scores.append(1.0)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def compare_functions(self, func_a: str, func_b: str) -> float:
        """Compare two function definitions."""
        return self.fuzzy_matcher.compute_composite_score(func_a, func_b)


# ============================================================================
# SEMANTIC CONFLICT DETECTOR
# ============================================================================


class SemanticConflictDetector:
    """Main detector combining all semantic analysis techniques."""
    
    # Threshold constants
    SEMANTIC_SIMILARITY_THRESHOLD = 0.6
    FUZZY_MATCH_THRESHOLD = 0.5
    STRUCTURAL_SIMILARITY_THRESHOLD = 0.7
    HIGH_CONFLICT_THRESHOLD = 0.8
    MEDIUM_CONFLICT_THRESHOLD = 0.5
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.fuzzy_matcher = FuzzyMatcher()
        self.structural_analyzer = StructuralAnalyzer()
    
    def detect_conflicts(
        self,
        file_path: str,
        content_a: str,
        content_b: str,
        conflict_regions: Optional[List[ConflictRegion]] = None
    ) -> SemanticConflictAnalysis:
        """Perform comprehensive semantic conflict analysis."""
        conflict_regions = conflict_regions or []
        
        # Compute individual similarity scores
        semantic_similarity = self.semantic_analyzer.compute_tfidf_similarity(
            content_a, content_b
        )
        
        fuzzy_score = self.fuzzy_matcher.compute_composite_score(
            content_a, content_b
        )
        
        structural_similarity = self.structural_analyzer.compute_structural_similarity(
            content_a, content_b
        )
        
        # Generate resolution suggestions
        suggestions = self._generate_suggestions(
            file_path, content_a, content_b,
            semantic_similarity, fuzzy_score, structural_similarity
        )
        
        return SemanticConflictAnalysis(
            file_path=file_path,
            semantic_similarity=semantic_similarity,
            fuzzy_match_score=fuzzy_score,
            structural_similarity=structural_similarity,
            conflict_regions=conflict_regions,
            resolution_suggestions=suggestions
        )
    
    def _generate_suggestions(
        self,
        file_path: str,
        content_a: str,
        content_b: str,
        semantic_sim: float,
        fuzzy_score: float,
        structural_sim: float
    ) -> List[str]:
        """Generate resolution suggestions based on analysis."""
        suggestions = []
        
        # High semantic similarity - content is similar
        if semantic_sim > self.HIGH_CONFLICT_THRESHOLD:
            suggestions.append(
                "High semantic similarity detected - consider automated merge"
            )
        
        # High fuzzy match - similar changes
        if fuzzy_score > self.HIGH_CONFLICT_THRESHOLD:
            suggestions.append(
                "Similar changes detected - review for redundant modifications"
            )
        
        # Structural differences
        if structural_sim < self.STRUCTURAL_SIMILARITY_THRESHOLD:
            suggestions.append(
                "Structural differences found - verify compatibility of changes"
            )
        
        # Analyze semantic roles
        roles_a = self.semantic_analyzer.analyze_semantic_roles(content_a)
        roles_b = self.semantic_analyzer.analyze_semantic_roles(content_b)
        role_similarity = self.semantic_analyzer.compute_role_similarity(roles_a, roles_b)
        
        if role_similarity < 0.5:
            suggestions.append(
                "Different semantic roles affected - manual review recommended"
            )
        
        # Add general suggestions
        if not suggestions:
            suggestions.append("Standard merge conflict resolution required")
        
        return suggestions
    
    def determine_conflict_severity(
        self,
        analysis: SemanticConflictAnalysis,
        traditional_severity: str = "medium"
    ) -> str:
        """Determine enhanced conflict severity combining traditional and semantic analysis."""
        # Get the combined semantic score
        combined = analysis.combined_score
        
        # Traditional severity weights
        severity_weights = {"high": 1.0, "medium": 0.5, "low": 0.2}
        trad_weight = severity_weights.get(traditional_severity, 0.5)
        
        # Combined score (weighted average)
        final_score = (combined * 0.6) + (trad_weight * 0.4)
        
        if final_score >= 0.7:
            return "high"
        elif final_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def analyze_conflict_regions(
        self,
        region_a: str,
        region_b: str
    ) -> Dict[str, float]:
        """Analyze specific conflict regions in detail."""
        return {
            'semantic_similarity': self.semantic_analyzer.compute_tfidf_similarity(
                region_a, region_b
            ),
            'fuzzy_score': self.fuzzy_matcher.compute_composite_score(
                region_a, region_b
            ),
            'structural_similarity': self.structural_analyzer.compute_structural_similarity(
                region_a, region_b
            )
        }


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    'FuzzyMatcher',
    'SemanticAnalyzer', 
    'StructuralAnalyzer',
    'SemanticConflictDetector',
]
