
import asyncio
import time
import re
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class EmailFilter:
    filter_id: str
    criteria: Dict[str, Any]

def _apply_filter_original(filter_obj: EmailFilter, email_context: Dict[str, Any]) -> bool:
    criteria = filter_obj.criteria

    if "subject_keywords" in criteria:
        subject = email_context["subject_lower"]
        if not any(keyword.lower() in subject for keyword in criteria["subject_keywords"]):
            return False

    if "from_patterns" in criteria:
        sender_email = email_context["sender_lower"]
        if not any(re.search(p, sender_email, re.IGNORECASE) for p in criteria["from_patterns"]):
            return False

    return True

# Optimized version
@dataclass
class OptimizedEmailFilter(EmailFilter):
    _compiled_patterns: Dict[str, Any] = None

    def __post_init__(self):
        self._compiled_patterns = {}
        if "subject_keywords" in self.criteria:
            self._compiled_patterns["subject_keywords"] = [k.lower() for k in self.criteria["subject_keywords"]]
        if "from_patterns" in self.criteria:
            self._compiled_patterns["from_patterns"] = [re.compile(p, re.IGNORECASE) for p in self.criteria["from_patterns"]]

def _apply_filter_optimized(filter_obj: OptimizedEmailFilter, email_context: Dict[str, Any]) -> bool:
    criteria = filter_obj.criteria
    compiled = filter_obj._compiled_patterns

    if "subject_keywords" in criteria:
        subject = email_context["subject_lower"]
        # Use pre-lowercased keywords
        keywords = compiled.get("subject_keywords", criteria["subject_keywords"])
        if not any(keyword in subject for keyword in keywords):
            return False

    if "from_patterns" in criteria:
        sender_email = email_context["sender_lower"]
        # Use pre-compiled regex
        patterns = compiled.get("from_patterns", [])
        if not any(p.search(sender_email) for p in patterns):
            return False

    return True

async def benchmark():
    # Setup data
    filters = []
    for i in range(100):
        filters.append(EmailFilter(
            filter_id=str(i),
            criteria={
                "subject_keywords": [f"keyword{j}" for j in range(10)] + ["urgent", "important"],
                "from_patterns": [f"user{j}@example\.com" for j in range(5)] + [r".*@company\.com"]
            }
        ))

    optimized_filters = []
    for f in filters:
        optimized_filters.append(OptimizedEmailFilter(
            filter_id=f.filter_id,
            criteria=f.criteria
        ))

    email_context = {
        "subject_lower": "this is an important message about keyword5",
        "sender_lower": "boss@company.com"
    }

    # Warmup
    for f in filters:
        _apply_filter_original(f, email_context)
    for f in optimized_filters:
        _apply_filter_optimized(f, email_context)

    iterations = 10000

    start = time.time()
    for _ in range(iterations):
        for f in filters:
            _apply_filter_original(f, email_context)
    original_time = time.time() - start

    start = time.time()
    for _ in range(iterations):
        for f in optimized_filters:
            _apply_filter_optimized(f, email_context)
    optimized_time = time.time() - start

    print(f"Original time: {original_time:.4f}s")
    print(f"Optimized time: {optimized_time:.4f}s")
    print(f"Improvement: {original_time / optimized_time:.2f}x")

if __name__ == "__main__":
    asyncio.run(benchmark())
