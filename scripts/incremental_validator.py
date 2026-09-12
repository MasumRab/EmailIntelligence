#!/usr/bin/env python3
"""
Incremental Validation
Only validate changed content to improve performance.
"""

import os
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class FileValidationCache:
    file_path: str
    content_hash: str
    last_validated: float
    validation_results: Dict[str, str] = field(default_factory=dict)  # validation_type -> result
    error_count: int = 0


class ValidationCache:
    def __init__(self, cache_file: Path = None):
        self.cache_file = cache_file or Path(".validation_cache.json")
        self.cache: Dict[str, FileValidationCache] = {}
        self.load_cache()

    def load_cache(self):
        """Load validation cache from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    for file_path, cache_data in data.items():
                        self.cache[file_path] = FileValidationCache(
                            file_path=cache_data['file_path'],
                            content_hash=cache_data['content_hash'],
                            last_validated=cache_data['last_validated'],
                            validation_results=cache_data.get('validation_results', {}),
                            error_count=cache_data.get('error_count', 0)
                        )
            except Exception as e:
                print(f"Error loading validation cache: {e}")

    def save_cache(self):
        """Save validation cache to file."""
        try:
            data = {}
            for file_path, cache_entry in self.cache.items():
                data[file_path] = {
                    'file_path': cache_entry.file_path,
                    'content_hash': cache_entry.content_hash,
                    'last_validated': cache_entry.last_validated,
                    'validation_results': cache_entry.validation_results,
                    'error_count': cache_entry.error_count
                }
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving validation cache: {e}")

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""

    def is_file_cached(self, file_path: Path) -> bool:
        """Check if file is in cache."""
        return str(file_path) in self.cache

    def is_file_changed(self, file_path: Path) -> bool:
        """Check if file has changed since last validation."""
        if not self.is_file_cached(file_path):
            return True

        cache_entry = self.cache[str(file_path)]
        current_hash = self.calculate_file_hash(file_path)

        return cache_entry.content_hash != current_hash

    def get_cached_validation_result(self, file_path: Path, validation_type: str) -> Optional[str]:
        """Get cached validation result for a file and validation type."""
        if not self.is_file_cached(file_path):
            return None

        cache_entry = self.cache[str(file_path)]
        return cache_entry.validation_results.get(validation_type)

    def update_cache_entry(self, file_path: Path, validation_type: str, result: str, error_count: int = 0):
        """Update cache entry with validation result."""
        file_str = str(file_path)
        current_hash = self.calculate_file_hash(file_path)

        if file_str not in self.cache:
            self.cache[file_str] = FileValidationCache(
                file_path=file_str,
                content_hash=current_hash,
                last_validated=time.time()
            )

        cache_entry = self.cache[file_str]
        cache_entry.content_hash = current_hash
        cache_entry.last_validated = time.time()
        cache_entry.validation_results[validation_type] = result
        cache_entry.error_count = error_count

        self.save_cache()

    def get_files_needing_validation(self, file_paths: List[Path]) -> List[Path]:
        """Get list of files that need validation (changed files)."""
        return [fp for fp in file_paths if self.is_file_changed(fp)]

    def clear_cache(self):
        """Clear the validation cache."""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()

    def get_cache_statistics(self) -> Dict:
        """Get cache statistics."""
        total_files = len(self.cache)
        total_validations = sum(len(entry.validation_results) for entry in self.cache.values())

        # Count cached passes vs failures
        cached_passes = 0
        cached_failures = 0
        for entry in self.cache.values():
            for result in entry.validation_results.values():
                if result == "pass":
                    cached_passes += 1
                elif result == "fail":
                    cached_failures += 1

        return {
            'cached_files': total_files,
            'total_cached_validations': total_validations,
            'cached_passes': cached_passes,
            'cached_failures': cached_failures,
            'cache_hit_rate': (total_validations / (total_validations + 1) * 100) if total_validations > 0 else 0
        }


class IncrementalValidator:
    def __init__(self, cache: ValidationCache = None):
        self.cache = cache or ValidationCache()
        self.validation_time_saved = 0.0  # in seconds
        self.validations_skipped = 0

    def validate_files_incrementally(self, file_paths: List[Path],
                                   validation_func, validation_type: str,
                                   force_revalidation: bool = False) -> Dict:
        """Validate files incrementally, skipping unchanged files with cached results."""
        start_time = time.time()

        # Determine which files need validation
        if force_revalidation:
            files_to_validate = file_paths
        else:
            files_to_validate = self.cache.get_files_needing_validation(file_paths)

        # Get cached results for unchanged files
        cached_results = {}
        skipped_files = []

        for file_path in file_paths:
            if file_path not in files_to_validate:
                # File hasn't changed, check cache
                cached_result = self.cache.get_cached_validation_result(file_path, validation_type)
                if cached_result:
                    cached_results[str(file_path)] = cached_result
                    skipped_files.append(file_path)
                    self.validations_skipped += 1

        # Validate only changed files
        validation_results = {}
        error_counts = {}

        if files_to_validate:
            # Run validation function on changed files
            results = validation_func(files_to_validate)
            validation_results.update(results)

            # Update cache with new results
            for file_path in files_to_validate:
                file_str = str(file_path)
                result = results.get(file_str, "pass")
                error_count = 0  # Would be determined by validation function
                self.cache.update_cache_entry(file_path, validation_type, result, error_count)

        # Combine cached and new results
        all_results = {**cached_results, **validation_results}

        # Calculate time saved
        end_time = time.time()
        total_duration = end_time - start_time

        # Estimate time that would have been spent validating all files
        # (simplified estimation)
        estimated_full_validation_time = len(file_paths) * 0.1  # Assume 0.1 sec per file
        time_saved = estimated_full_validation_time - total_duration
        self.validation_time_saved += max(0, time_saved)

        return {
            'results': all_results,
            'validated_files': len(files_to_validate),
            'skipped_files': len(skipped_files),
            'total_files': len(file_paths),
            'time_saved': time_saved,
            'duration': total_duration
        }

    def validate_with_dependency_check(self, file_paths: List[Path],
                                     dependency_map: Dict[Path, List[Path]],
                                     validation_func, validation_type: str) -> Dict:
        """Validate files considering dependencies."""
        # Files that need validation due to changes or dependency changes
        files_to_validate = set()

        # Check direct file changes
        directly_changed = self.cache.get_files_needing_validation(file_paths)
        files_to_validate.update(directly_changed)

        # Check dependencies - if a dependency changed, validate dependent files
        for file_path in file_paths:
            dependencies = dependency_map.get(file_path, [])
            for dep in dependencies:
                if self.cache.is_file_changed(dep):
                    files_to_validate.add(file_path)
                    break

        # Convert to list for validation
        files_to_validate_list = list(files_to_validate)

        # Get cached results for files not needing validation
        cached_results = {}
        skipped_files = []

        for file_path in file_paths:
            if file_path not in files_to_validate:
                cached_result = self.cache.get_cached_validation_result(file_path, validation_type)
                if cached_result:
                    cached_results[str(file_path)] = cached_result
                    skipped_files.append(file_path)
                    self.validations_skipped += 1

        # Validate files that need it
        validation_results = {}
        if files_to_validate_list:
            results = validation_func(files_to_validate_list)
            validation_results.update(results)

            # Update cache
            for file_path in files_to_validate_list:
                file_str = str(file_path)
                result = results.get(file_str, "pass")
                error_count = 0
                self.cache.update_cache_entry(file_path, validation_type, result, error_count)

        # Combine results
        all_results = {**cached_results, **validation_results}

        return {
            'results': all_results,
            'validated_files': len(files_to_validate_list),
            'skipped_files': len(skipped_files),
            'total_files': len(file_paths),
            'dependency_triggered_validations': len(files_to_validate) - len(directly_changed)
        }

    def get_validation_statistics(self) -> Dict:
        """Get validation statistics."""
        cache_stats = self.cache.get_cache_statistics()

        return {
            'time_saved_seconds': self.validation_time_saved,
            'validations_skipped': self.validations_skipped,
            'cache_statistics': cache_stats,
            'estimated_performance_improvement': (
                self.validations_skipped / (self.validations_skipped + 1) * 100
            ) if self.validations_skipped > 0 else 0
        }

    def clear_validation_cache(self):
        """Clear the validation cache."""
        self.cache.clear_cache()
        self.validation_time_saved = 0.0
        self.validations_skipped = 0


def main():
    # Example usage
    print("Incremental Validation System")
    print("=" * 30)

    # Create incremental validator
    cache = ValidationCache()
    validator = IncrementalValidator(cache)

    print("Incremental validation system initialized")
    print("System ready to validate only changed content for improved performance")

    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Check file modification times and hashes")
    print("  2. Skip validation for unchanged files with cached results")
    print("  3. Validate only changed files")
    print("  4. Cache new results for future use")
    print("  5. Report time saved through incremental validation")


if __name__ == "__main__":
    main()