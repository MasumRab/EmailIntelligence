"""
NLP Service Module - Strategy Pattern Edition

Provides robust semantic and lexical analysis capabilities for internal CLI operations.
Uses the Strategy Pattern to decouple similarity algorithms from the service logic.
"""

import logging
import re
import collections
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set
from difflib import SequenceMatcher, get_close_matches

# Optional scientific dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HAS_SCIENTIFIC = True
except ImportError:
    HAS_SCIENTIFIC = False

logger = logging.getLogger(__name__)

# --- Strategy Interfaces ---

class SimilarityStrategy(ABC):
    """Abstract base class for text similarity algorithms."""
    @abstractmethod
    def calculate(self, text1: str, text2: str) -> float:
        pass

# --- Concrete Strategies ---

class BasicSimilarityStrategy(SimilarityStrategy):
    """Existing: Balanced structural (difflib) and lexical (Jaccard) fallback."""
    def calculate(self, text1: str, text2: str) -> float:
        t1, t2 = text1.lower().strip(), text2.lower().strip()
        
        # 1. Structural (difflib)
        struct_score = SequenceMatcher(None, t1, t2).ratio()
        
        # 2. Lexical (Jaccard)
        tokens1 = set(re.findall(r'\w+', t1))
        tokens2 = set(re.findall(r'\w+', t2))
        if not tokens1 or not tokens2:
            return struct_score
            
        lexical_score = len(tokens1 & tokens2) / len(tokens1 | tokens2)
        return (struct_score * 0.4) + (lexical_score * 0.6)

class ScientificSimilarityStrategy(SimilarityStrategy):
    """Intended: High-fidelity vector-based similarity using TF-IDF and Cosine Similarity."""
    def calculate(self, text1: str, text2: str) -> float:
        if not HAS_SCIENTIFIC:
            return 0.0
        try:
            vectorizer = TfidfVectorizer(token_pattern=r'\w+')
            tfidf = vectorizer.fit_transform([text1, text2])
            return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        except Exception as e:
            logger.debug(f"Scientific similarity calculation failed: {e}")
            return 0.0

# --- Context (Service) ---

class NLPService:
    """
    Service providing multi-factor string similarity and matching.
    Orchestrates different SimilarityStrategies based on environment and requirements.
    """

    def __init__(self, strategy: Optional[SimilarityStrategy] = None):
        self._initialized = True
        # Default to scientific if available, otherwise fallback to basic
        if strategy:
            self.strategy = strategy
        elif HAS_SCIENTIFIC:
            self.strategy = ScientificSimilarityStrategy()
        else:
            self.strategy = BasicSimilarityStrategy()

    async def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculates similarity using the configured strategy."""
        if not text1 or not text2:
            return 0.0
        
        score = self.strategy.calculate(text1, text2)
        
        # If scientific strategy fails or returns 0 for non-empty strings, use basic fallback
        if score <= 0.0 and not isinstance(self.strategy, BasicSimilarityStrategy):
            return BasicSimilarityStrategy().calculate(text1, text2)
            
        return score

    async def extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        """Independent keyword extraction using frequency analysis."""
        words = re.findall(r'\w+', text.lower())
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'is', 'it', 'and', 'or', 'of', 'with'}
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        counts = collections.Counter(filtered)
        return [w for w, c in counts.most_common(limit)]

    async def find_matches(self, query: str, choices: List[str], cutoff: float = 0.6) -> List[str]:
        """FZF-style fuzzy matching."""
        if not choices: return []
        return get_close_matches(query, choices, n=5, cutoff=cutoff)

    def is_available(self) -> bool:
        return True
