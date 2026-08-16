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
        tokens1 = set(re.findall(r"\w+", t1))
        tokens2 = set(re.findall(r"\w+", t2))
        if not tokens1 or not tokens2:
            return struct_score

        lexical_score = len(tokens1 & tokens2) / len(tokens1 | tokens2)
        return (struct_score * 0.4) + (lexical_score * 0.6)


class ScientificSimilarityStrategy(SimilarityStrategy):
    """Intended: High-fidelity similarity using the project's scientific NLPEngine."""

    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine:
            return self._engine
        try:
            from src.backend.python_nlp.nlp_engine import NLPEngine
            self._engine = NLPEngine()
            return self._engine
        except ImportError:
            return None
        except Exception as e:
            import logging
            logging.debug(f"NLP engine unavailable due to backend error: {e}")
            return None

    def calculate(self, text1: str, text2: str) -> float:
        engine = self._get_engine()
        # If the real engine has a similarity method, use it
        if engine and hasattr(engine, "calculate_similarity"):
            try:
                return float(engine.calculate_similarity(text1, text2))
            except ImportError as e:
                import logging
                logging.debug(f"NLP engine unavailable: {e}")
            except Exception as e:
                # Log but don't fail silently - fall through to fallback
                import logging

                logging.warning(f"NLP similarity calculation failed: {e}")

        # Fallback to local BM25 ranking (per spec 004-guided-workflow) if engine doesn't support generic similarities
        if not HAS_SCIENTIFIC:
            return 0.0
        try:
            from rank_bm25 import BM25Okapi

            # Simple tokenization
            tokenized_doc1 = text1.lower().split()
            tokenized_doc2 = text2.lower().split()

            if not tokenized_doc1 or not tokenized_doc2:
                return 0.0

            bm25 = BM25Okapi([tokenized_doc1])
            # BM25 scores can be greater than 1, normalize via log or arbitrary ceiling for interface compatibility
            raw_score = bm25.get_scores(tokenized_doc2)[0]
            import math
            normalized_score = min(1.0, max(0.0, math.log1p(raw_score) / 10.0))
            return float(normalized_score)
        except ImportError:
            # Fall back to TF-IDF if rank_bm25 is missing
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.metrics.pairwise import cosine_similarity

                vectorizer = TfidfVectorizer(token_pattern=r"\w+")
                tfidf = vectorizer.fit_transform([text1, text2])
                return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
            except Exception:
                return 0.0
        except Exception as e:
            import logging
            logging.debug(f"BM25 Error: {e}")
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

    async def calculate_with_feedback(
        self,
        text1: str,
        text2: str,
        threshold: float,
        min_keyword_hits: int = 1,
    ) -> Dict[str, Any]:
        """
        Compute similarity with a feedback loop on unsuccessful matches.

        When the raw score falls at or below ``threshold``, the query is
        refined: keywords are extracted from ``text2`` and the document
        (``text1``) is scored on keyword presence. This turns a hard "out of
        scope" verdict into a measurable, tunable decision and records the
        miss for later adjustment.

        Returns::

            {
                "score": float,            # best score achieved (0.0-1.0)
                "refined": bool,           # True if the keyword retry improved the score
                "keywords": List[str],     # keywords used for the retry
                "keyword_hits": int,       # how many keywords matched in text1
                "missed": bool,            # True if even the refeined score is below threshold
            }
        """
        if not text1 or not text2:
            return {"score": 0.0, "refined": False, "keywords": [], "keyword_hits": 0, "missed": True}

        score = await self.calculate_similarity(text1, text2)
        raw_score = score
        keywords = await self.extract_keywords(text2)
        hits = 0
        refined = False

        if score <= threshold:
            tokens1 = set(re.findall(r"\w+", text1.lower()))
            hits = sum(1 for kw in keywords if kw in tokens1)
            if hits >= min_keyword_hits:
                # Keyword overlap is evidence the document shares intent with
                # the scope sentence even when lexical similarity is low.
                inferred = max(score, min(1.0, 0.5 + 0.1 * hits))
                refined = inferred > score
                score = inferred
                logger.info(
                    "NLP similarity below threshold; keyword refinement raised score "
                    "%.2f -> %.2f (hits=%d keywords=%s)",
                    raw_score, score, hits, keywords,
                )

        missed = score <= threshold
        if missed:
            logger.warning(
                "NLP semantic match missed: score=%.2f threshold=%.2f keywords=%s hits=%d",
                score, threshold, keywords, hits,
            )

        return {
            "score": score,
            "refined": refined,
            "keywords": keywords,
            "keyword_hits": hits,
            "missed": missed,
        }

    async def extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        """Independent keyword extraction using frequency analysis."""
        words = re.findall(r"\w+", text.lower())
        stop_words = {
            "the",
            "a",
            "an",
            "in",
            "on",
            "at",
            "for",
            "to",
            "is",
            "it",
            "and",
            "or",
            "of",
            "with",
        }
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        counts = collections.Counter(filtered)
        return [w for w, c in counts.most_common(limit)]

    async def find_matches(
        self, query: str, choices: List[str], cutoff: float = 0.6
    ) -> List[str]:
        """FZF-style fuzzy matching with automatic cutoff relaxation.

        If no match is found at the requested cutoff, the cutoff is lowered
        (feedback loop) so a near-miss still surfaces instead of silently
        returning nothing.
        """
        if not choices:
            return []
        matches = get_close_matches(query, choices, n=5, cutoff=cutoff)
        if not matches and cutoff > 0.3:
            logger.info(
                "NLP find_matches returned nothing at cutoff=%.2f; retrying at 0.3",
                cutoff,
            )
            matches = get_close_matches(query, choices, n=5, cutoff=0.3)
        return matches

    def is_available(self) -> bool:
        return True
