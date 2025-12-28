
import os
import re
import fnmatch
import time
import timeit
from typing import List, Pattern, Optional

# Mock logger
class Logger:
    def error(self, msg): pass
    def info(self, msg): pass

logger = Logger()

class OriginalContextIsolator:
    def __init__(self, patterns):
        self._restricted_patterns = self._compile_patterns(patterns)

    def _compile_patterns(self, patterns: List[str]) -> List[Pattern]:
        compiled = []
        for p in patterns:
            try:
                regex_str = fnmatch.translate(p)
                compiled.append(re.compile(regex_str))
            except Exception:
                pass
        return compiled

    def _matches_patterns(self, file_path: str, patterns: List[Pattern]) -> bool:
        try:
            filename = os.path.basename(file_path)
        except Exception:
            filename = file_path

        for pattern in patterns:
            try:
                if pattern.match(file_path):
                    return True
                if pattern.match(filename):
                    return True
            except Exception:
                continue
        return False

    def check(self, path):
        return self._matches_patterns(path, self._restricted_patterns)

class OptimizedContextIsolator:
    def __init__(self, patterns):
        self._restricted_patterns = self._compile_patterns(patterns)

    def _compile_patterns(self, patterns: List[str]) -> Optional[Pattern]:
        if not patterns:
            return None

        regex_parts = []
        for p in patterns:
            try:
                # fnmatch.translate returns '(?s:pattern)\Z'
                # We want to combine them with OR
                regex_str = fnmatch.translate(p)
                regex_parts.append(f"(?:{regex_str})")
            except Exception:
                pass

        if not regex_parts:
            return None

        combined_regex = "|".join(regex_parts)
        try:
            return re.compile(combined_regex)
        except Exception:
            return None

    def _matches_patterns(self, file_path: str, pattern: Optional[Pattern]) -> bool:
        if pattern is None:
            return False

        try:
            if pattern.match(file_path):
                return True

            filename = os.path.basename(file_path)
            if pattern.match(filename):
                return True
        except Exception:
            pass

        return False

    def check(self, path):
        return self._matches_patterns(path, self._restricted_patterns)


def run_benchmark():
    # Setup
    patterns = [
        "*.pyc", "__pycache__", ".git", "*.log", "*.tmp",
        "node_modules", "venv", ".env", "*.secret", "private/*",
        "**/*.lock", "*.md", "*.txt", "src/**/*.swp"
    ]
    # Add some complexity
    patterns.extend([f"pattern_{i}*" for i in range(50)])

    files_to_check = [
        "/path/to/project/src/main.py",
        "/path/to/project/src/utils.py",
        "/path/to/project/.env",  # Should match
        "/path/to/project/node_modules/react/index.js", # Should match
        "simple_file.txt", # Should match
        "/path/to/project/README.md", # Should match
        "/path/to/project/src/core/logic.py",
        "pattern_25_test.dat" # Should match
    ]

    original = OriginalContextIsolator(patterns)
    optimized = OptimizedContextIsolator(patterns)

    # Verify correctness first
    print("Verifying correctness...")
    for f in files_to_check:
        res_orig = original.check(f)
        res_opt = optimized.check(f)
        if res_orig != res_opt:
            print(f"MISMATCH for {f}: Original={res_orig}, Optimized={res_opt}")
            # Identify why
            # fnmatch.translate('*.py') -> (?s:.*\.py)\Z
            # pattern.match matches from beginning.
            # Original: pattern.match(file_path) checks if file_path matches pattern fully (due to \Z)
            # Optimized: pattern.match(file_path) checks if file_path matches combined pattern fully.
            # Wait, `re.match` anchors at the start. `\Z` anchors at the end.
            # So `(?s:.*\.py)\Z` passed to `re.match` matches the whole string.
            # It should be identical.

    # Benchmark
    iterations = 10000

    def run_orig():
        for f in files_to_check:
            original.check(f)

    def run_opt():
        for f in files_to_check:
            optimized.check(f)

    t_orig = timeit.timeit(run_orig, number=iterations)
    t_opt = timeit.timeit(run_opt, number=iterations)

    print(f"\nBenchmark Results ({iterations} iterations over {len(files_to_check)} files):")
    print(f"Original:  {t_orig:.4f}s")
    print(f"Optimized: {t_opt:.4f}s")
    print(f"Speedup:   {t_orig / t_opt:.2f}x")

if __name__ == "__main__":
    run_benchmark()
