"""
NLP Service Module

Provides independent semantic and lexical analysis capabilities.
Uses sophisticated standard library algorithms to remain functional 
without heavy ML dependencies.
"""

import logging
import re
import collections
from typing import List
from difflib import SequenceMatcher, get_close_matches

logger = logging.getLogger(__name__)

class NLPService:
    """
    Independent service for providing semantic insights to CLI commands.
    """

    def __init__(self):
        self._engine = None
        self._initialized = False

    async def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates similarity using a multi-factor approach:
        1. Sequence matching (Structural)
        2. Token set overlap (Lexical)
        """
        if not text1 or not text2:
            return 0.0
            
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()
        
        # 1. Structural Similarity (difflib)
        struct_score = SequenceMatcher(None, t1, t2).ratio()
        
        # 2. Lexical Similarity (Jaccard Index)
        tokens1 = set(re.findall(r'\w+', t1))
        tokens2 = set(re.findall(r'\w+', t2))
        
        if not tokens1 or not tokens2:
            return struct_score
            
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        lexical_score = len(intersection) / len(union)
        
        # Weighted Average: 40% Structure, 60% Lexical
        return (struct_score * 0.4) + (lexical_score * 0.6)

    async def extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        """Independent keyword extraction using frequency analysis."""
        words = re.findall(r'\w+', text.lower())
        # Filter out common stop words (Basic list)
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'is', 'it', 'and', 'or'}
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        
        counts = collections.Counter(filtered)
        return [w for w, c in counts.most_common(limit)]

    def is_available(self) -> bool:
        """This independent version is always available."""
        return True

    async def find_matches(self, query: str, choices: List[str], cutoff: float = 0.6) -> List[str]:
        """FZF-style fuzzy matching."""
        return get_close_matches(query, choices, n=5, cutoff=cutoff)
