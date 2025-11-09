#!/usr/bin/env python3
"""
Test script for validation result caching system
"""

import tempfile
import time
from pathlib import Path
from validation_cache import ValidationResultCacheManager, ValidationCachingEngine


def mock_validation_func(file_path):
    """Mock validation function that simulates validation work."""
    # Simulate some validation work
    time.sleep(0.1)
    content = file_path.read_text()
    if "error" in content.lower():
        return "fail", ["Found error in content"]
    elif "warning" in content.lower():
        return "warning", ["Found warning in content"]
    else:
        return "pass", []


def test_cache_basic_functionality():
    """Test basic cache functionality."""
    print("Testing basic cache functionality...")

    # Create temporary directory and files for testing
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\nThis is a test document.")

        # Initialize cache manager
        cache_file = tmp_path / ".validation_cache.json"
        cache_manager = ValidationResultCacheManager(cache_file=cache_file)
        caching_engine = ValidationCachingEngine(cache_manager)

        # First validation (cache miss)
        result1, errors1, duration1 = caching_engine.validate_with_caching(
            "content_validator", test_file, mock_validation_func
        )

        # Second validation (should be cache hit)
        result2, errors2, duration2 = caching_engine.validate_with_caching(
            "content_validator", test_file, mock_validation_func
        )

        print(f"First validation: {result1}, duration: {duration1:.3f}s")
        print(f"Second validation: {result2}, duration: {duration2:.3f}s")
        print(
            f"Cache hits: {caching_engine.cache_hits}, misses: {caching_engine.cache_misses}"
        )

        # Verify cache hit worked
        assert result1 == result2, "Results should be the same"
        assert errors1 == errors2, "Errors should be the same"
        assert duration2 == 0.0, "Second validation should be instant (cache hit)"
        assert caching_engine.cache_hits == 1, "Should have one cache hit"
        assert caching_engine.cache_misses == 1, "Should have one cache miss"

        print("✓ Basic cache functionality test passed")


def test_cache_invalidation():
    """Test cache invalidation when content changes."""
    print("\nTesting cache invalidation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\nThis is a test document.")

        # Initialize cache manager
        cache_file = tmp_path / ".validation_cache.json"
        cache_manager = ValidationResultCacheManager(cache_file=cache_file)
        caching_engine = ValidationCachingEngine(cache_manager)

        # First validation
        result1, errors1, duration1 = caching_engine.validate_with_caching(
            "content_validator", test_file, mock_validation_func
        )

        # Modify file content
        test_file.write_text("# Test Document\nThis is a modified test document.")

        # Second validation (should be cache miss due to content change)
        result2, errors2, duration2 = caching_engine.validate_with_caching(
            "content_validator", test_file, mock_validation_func
        )

        print(f"Before modification: {result1}")
        print(f"After modification: {result2}")

        # Should have 2 misses and 0 hits since content changed
        assert caching_engine.cache_misses == 2, "Should have two cache misses"
        assert caching_engine.cache_hits == 0, "Should have no cache hits"

        print("✓ Cache invalidation test passed")


def test_cache_statistics():
    """Test cache statistics tracking."""
    print("\nTesting cache statistics...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create multiple test files
        files = []
        for i in range(3):
            test_file = tmp_path / f"test{i}.md"
            test_file.write_text(f"# Test Document {i}\nThis is test document {i}.")
            files.append(test_file)

        # Initialize cache manager
        cache_file = tmp_path / ".validation_cache.json"
        cache_manager = ValidationResultCacheManager(cache_file=cache_file)
        caching_engine = ValidationCachingEngine(cache_manager)

        # Validate all files twice to generate cache hits
        for file_path in files:
            # First validation (cache miss)
            caching_engine.validate_with_caching(
                "content_validator", file_path, mock_validation_func
            )

            # Second validation (cache hit)
            caching_engine.validate_with_caching(
                "content_validator", file_path, mock_validation_func
            )

        # Get statistics
        stats = caching_engine.get_caching_statistics()

        print(f"Cache hits: {stats['cache_hits']}")
        print(f"Cache misses: {stats['cache_misses']}")
        print(f"Hit rate: {stats['hit_rate_percent']:.1f}%")
        print(f"Time saved: {stats['time_saved_seconds']:.2f}s")

        # Verify statistics
        assert stats["cache_hits"] == 3, "Should have 3 cache hits"
        assert stats["cache_misses"] == 3, "Should have 3 cache misses"
        assert stats["hit_rate_percent"] > 0, "Hit rate should be positive"

        print("✓ Cache statistics test passed")


def main():
    """Run all tests."""
    print("Running Validation Cache System Tests")
    print("=" * 40)

    try:
        test_cache_basic_functionality()
        test_cache_invalidation()
        test_cache_statistics()

        print("\n" + "=" * 40)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
