"""
NLP Service Module (High-Fidelity Comparison Edition)

Provides robust semantic and lexical analysis capabilities for internal CLI operations.
Includes TF-IDF and Cosine Similarity for high-fidelity "Similaroty Comparison".

CRITICAL ARCHITECTURAL REQUIREMENT:
If user feedback is required and needs to be processed to understand user intent and purpose,
the feedback MUST be sent to an LLM (Large Language Model) via the agent-based workflow.
Direct NLP engine piping for user intent is prohibited.
"""

import logging
import re
import collections
import math
from typing import Any, Dict, List, Optional, Set
from difflib import SequenceMatcher, get_close_matches

# Optional scientific dependencies for high-fidelity comparison
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

logger = logging.getLogger(__name__)

class NLPService:
    """
    Service providing multi-factor string similarity and matching.
    Uses TF-IDF + Cosine Similarity when available, falling back to difflib.
    """

    def __init__(self):
        self._initialized = True

    async def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates similarity using the best available method.
        1. TF-IDF + Cosine Similarity (High-Fidelity)
        2. SequenceMatcher + Jaccard (Balanced Fallback)
        """
        if not text1 or not text2:
            return 0.0

        if HAS_SKLEARN:
            try:
                return self._calculate_cosine_similarity(text1, text2)
            except Exception as e:
                logger.debug(f"Cosine similarity failed: {e}")

        return self._calculate_fallback_similarity(text1, text2)

    def _calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        """High-fidelity vector-based similarity."""
        vectorizer = TfidfVectorizer(token_pattern=r'\w+')
        tfidf = vectorizer.fit_transform([text1, text2])
        return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])

    def _calculate_fallback_similarity(self, text1: str, text2: str) -> float:
        """Balanced structural and lexical fallback."""
        t1, t2 = text1.lower().strip(), text2.lower().strip()
        
        # 1. Structural (difflib)
        struct_score = SequenceMatcher(None, t1, t2).ratio()
        
        # 2. Lexical (Jaccard)
        tokens1 = set(re.findall(r'\w+', t1))
        tokens2 = set(re.findall(r'\w+', t2))
        if not tokens1 or not tokens2: return struct_score
        
        lexical_score = len(tokens1 & tokens2) / len(tokens1 | tokens2)
        return (struct_score * 0.4) + (lexical_score * 0.6)

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
