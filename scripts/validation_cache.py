#!/usr/bin/env python3
"""
Validation Result Caching
Cache validation results to avoid redundant checks.
"""

import os
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class ValidationResultCache:
    validator_type: str
    file_path: str
    content_hash: str
    result: str  # "pass", "fail", "warning", etc.
    errors: List[str] = field(default_factory=list)
    timestamp: float = 0.0
    duration: float = 0.0  # Validation duration in seconds
    metadata: Dict = field(default_factory=dict)  # Additional metadata


class ValidationResultCacheManager:
    def __init__(self, cache_file: Path = None, max_cache_age_days: int = 7):
        self.cache_file = cache_file or Path(".validation_cache.json")
        self.max_cache_age_days = max_cache_age_days
        self.cache: Dict[str, ValidationResultCache] = {}
        self.load_cache()
        self._prune_old_entries()
        
    def load_cache(self):
        """Load validation result cache from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    
                for cache_key, cache_data in data.items():
                    cache_entry = ValidationResultCache(
                        validator_type=cache_data['validator_type'],
                        file_path=cache_data['file_path'],
                        content_hash=cache_data['content_hash'],
                        result=cache_data['result'],
                        errors=cache_data.get('errors', []),
                        timestamp=cache_data.get('timestamp', 0.0),
                        duration=cache_data.get('duration', 0.0),
                        metadata=cache_data.get('metadata', {})
                    )
                    self.cache[cache_key] = cache_entry
            except Exception as e:
                print(f"Error loading validation cache: {e}")
                
    def save_cache(self):
        """Save validation result cache to file."""
        try:
            data = {}
            for cache_key, cache_entry in self.cache.items():
                data[cache_key] = {
                    'validator_type': cache_entry.validator_type,
                    'file_path': cache_entry.file_path,
                    'content_hash': cache_entry.content_hash,
                    'result': cache_entry.result,
                    'errors': cache_entry.errors,
                    'timestamp': cache_entry.timestamp,
                    'duration': cache_entry.duration,
                    'metadata': cache_entry.metadata
                }
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving validation cache: {e}")
            
    def _generate_cache_key(self, validator_type: str, file_path: str) -> str:
        """Generate unique cache key."""
        return f"{validator_type}:{file_path}"
        
    def _calculate_content_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content."""
        if not file_path.exists():
            return ""
            
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""
            
    def _is_cache_age_valid(self, timestamp: float) -> bool:
        """Check if cache entry is still valid based on age."""
        cache_datetime = datetime.fromtimestamp(timestamp)
        age = datetime.now() - cache_datetime
        return age.days <= self.max_cache_age_days
        
    def _prune_old_entries(self):
        """Remove old cache entries."""
        current_time = time.time()
        old_entries = [
            key for key, entry in self.cache.items()
            if not self._is_cache_age_valid(entry.timestamp)
        ]
        
        for key in old_entries:
            del self.cache[key]
            
        if old_entries:
            self.save_cache()
            
    def get_result(self, validator_type: str, file_path: Path) -> Optional[ValidationResultCache]:
        """Get cached validation result."""
        cache_key = self._generate_cache_key(validator_type, str(file_path))
        cache_entry = self.cache.get(cache_key)
        
        if cache_entry:
            # Check if content has changed
            current_hash = self._calculate_content_hash(file_path)
            if cache_entry.content_hash == current_hash and self._is_cache_age_valid(cache_entry.timestamp):
                return cache_entry
                
        return None
        
    def set_result(self, validator_type: str, file_path: Path, result: str, 
                   errors: List[str] = None, duration: float = 0.0, 
                   metadata: Dict = None) -> bool:
        """Set validation result in cache."""
        if errors is None:
            errors = []
        if metadata is None:
            metadata = {}
            
        content_hash = self._calculate_content_hash(file_path)
        if not content_hash:
            return False
            
        cache_key = self._generate_cache_key(validator_type, str(file_path))
        
        cache_entry = ValidationResultCache(
            validator_type=validator_type,
            file_path=str(file_path),
            content_hash=content_hash,
            result=result,
            errors=errors,
            timestamp=time.time(),
            duration=duration,
            metadata=metadata
        )
        
        self.cache[cache_key] = cache_entry
        self.save_cache()
        return True
        
    def invalidate_result(self, validator_type: str, file_path: str) -> bool:
        """Invalidate a specific cached result."""
        cache_key = self._generate_cache_key(validator_type, file_path)
        if cache_key in self.cache:
            del self.cache[cache_key]
            self.save_cache()
            return True
        return False
        
    def invalidate_all_results(self, validator_type: str) -> int:
        """Invalidate all results for a specific validator type."""
        keys_to_remove = [
            key for key in self.cache.keys()
            if key.startswith(f"{validator_type}:")
        ]
        
        for key in keys_to_remove:
            del self.cache[key]
            
        if keys_to_remove:
            self.save_cache()
            
        return len(keys_to_remove)
        
    def invalidate_file_results(self, file_path: Path) -> int:
        """Invalidate all cached results for a specific file."""
        file_str = str(file_path)
        keys_to_remove = [
            key for key in self.cache.keys()
            if key.endswith(f":{file_str}")
        ]
        
        for key in keys_to_remove:
            del self.cache[key]
            
        if keys_to_remove:
            self.save_cache()
            
        return len(keys_to_remove)
        
    def get_cache_statistics(self) -> Dict:
        """Get statistics about the cache."""
        total_entries = len(self.cache)
        total_errors = sum(len(entry.errors) for entry in self.cache.values())
        
        # Group by validator type
        validator_types = {}
        for entry in self.cache.values():
            vtype = entry.validator_type
            if vtype not in validator_types:
                validator_types[vtype] = 0
            validator_types[vtype] += 1
            
        # Calculate cache hit rate (simplified)
        # In a real system, we would track hits vs misses
        estimated_hits = total_entries  # Placeholder
        
        age_distribution = {}
        for entry in self.cache.values():
            cache_datetime = datetime.fromtimestamp(entry.timestamp)
            age = (datetime.now() - cache_datetime).days
            if age not in age_distribution:
                age_distribution[age] = 0
            age_distribution[age] += 1
            
        return {
            'total_entries': total_entries,
            'total_errors': total_errors,
            'validator_types': validator_types,
            'estimated_cache_hits': estimated_hits,
            'cache_age_distribution': age_distribution,
            'max_cache_age_days': self.max_cache_age_days
        }
        
    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate (placeholder implementation)."""
        # In a real system, this would track actual cache hits vs misses
        return 0.0
        
    def clear_cache(self):
        """Clear all cache entries."""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
            
    def cleanup_cache(self):
        """Clean up cache by removing old entries."""
        self._prune_old_entries()


class ValidationCachingEngine:
    def __init__(self, cache_manager: ValidationResultCacheManager = None):
        self.cache_manager = cache_manager or ValidationResultCacheManager()
        self.cache_hits = 0
        self.cache_misses = 0
        self.time_saved = 0.0  # Time saved by using cache in seconds
        
    def validate_with_caching(self, validator_type: str, file_path: Path, 
                            validation_func, force_revalidate: bool = False) -> Tuple[str, List[str], float]:
        """
        Validate file with caching. Returns (result, errors, duration).
        """
        start_time = time.time()
        
        # Check cache first
        if not force_revalidate:
            cached_result = self.cache_manager.get_result(validator_type, file_path)
            if cached_result:
                self.cache_hits += 1
                # Estimate time saved
                self.time_saved += cached_result.duration
                return cached_result.result, cached_result.errors, 0.0  # No time spent validating
                
        # Cache miss - perform actual validation
        self.cache_misses += 1
        result, errors = validation_func(file_path)
        duration = time.time() - start_time
        
        # Cache the result
        self.cache_manager.set_result(validator_type, file_path, result, errors, duration)
        
        return result, errors, duration
        
    def batch_validate_with_caching(self, validator_type: str, file_paths: List[Path],
                                  validation_func) -> Dict:
        """Validate multiple files with caching."""
        results = {}
        
        for file_path in file_paths:
            result, errors, duration = self.validate_with_caching(
                validator_type, file_path, validation_func
            )
            results[str(file_path)] = {
                'result': result,
                'errors': errors,
                'duration': duration
            }
            
        return results
        
    def get_caching_statistics(self) -> Dict:
        """Get statistics about caching performance."""
        cache_stats = self.cache_manager.get_cache_statistics()
        
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'total_requests': total_requests,
            'hit_rate_percent': hit_rate,
            'time_saved_seconds': self.time_saved,
            'estimated_time_saved_percent': (
                self.time_saved / (self.time_saved + 1) * 100  # Avoid division by zero
            ) if self.time_saved > 0 else 0,
            'cache_statistics': cache_stats
        }
        
    def clear_caching_stats(self):
        """Clear caching statistics."""
        self.cache_hits = 0
        self.cache_misses = 0
        self.time_saved = 0.0


def main():
    # Example usage
    print("Validation Result Caching System")
    print("=" * 35)
    
    # Create cache manager and engine
    cache_manager = ValidationResultCacheManager()
    caching_engine = ValidationCachingEngine(cache_manager)
    
    print("Validation result caching system initialized")
    print("System ready to cache validation results and avoid redundant checks")
    
    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Check if validation result is already cached")
    print("  2. Skip validation if content hasn't changed")
    print("  3. Cache new results for future use")
    print("  4. Track cache hit rate and performance improvements")


if __name__ == "__main__":
    main()
