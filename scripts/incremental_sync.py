#!/usr/bin/env python3
"""
Incremental Sync with Change Detection
Efficient sync system that only transfers changed content between worktrees.
"""

import os
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from filecmp import dircmp
import shutil


class FileHash:
    def __init__(self, path: str, hash_value: str, mtime: float):
        self.path = path
        self.hash = hash_value
        self.mtime = mtime
        self.size = os.path.getsize(path) if os.path.exists(path) else 0


class ChangeDetector:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.hash_cache_file = base_dir / ".sync_cache.json"
        self.hash_cache: Dict[str, FileHash] = {}
        self.load_hash_cache()
        
    def load_hash_cache(self):
        """Load hash cache from file."""
        if self.hash_cache_file.exists():
            try:
                with open(self.hash_cache_file, 'r') as f:
                    data = json.load(f)
                    for path, item in data.items():
                        self.hash_cache[path] = FileHash(
                            path, item['hash'], item['mtime']
                        )
            except Exception as e:
                print(f"Error loading hash cache: {e}")
                
    def save_hash_cache(self):
        """Save hash cache to file."""
        try:
            data = {}
            for path, file_hash in self.hash_cache.items():
                data[path] = {
                    'hash': file_hash.hash,
                    'mtime': file_hash.mtime
                }
            with open(self.hash_cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving hash cache: {e}")
            
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
        
    def get_file_hash(self, file_path: Path) -> FileHash:
        """Get file hash, calculating if not in cache."""
        relative_path = str(file_path.relative_to(self.base_dir))
        mtime = file_path.stat().st_mtime
        
        # Check if file is in cache and hasn't changed
        if relative_path in self.hash_cache:
            cached = self.hash_cache[relative_path]
            if cached.mtime == mtime:
                return cached
                
        # Calculate new hash
        hash_value = self.calculate_file_hash(file_path)
        file_hash = FileHash(str(file_path), hash_value, mtime)
        self.hash_cache[relative_path] = file_hash
        self.save_hash_cache()
        return file_hash
        
    def scan_directory(self, directory: Path, extensions: Set[str] = None) -> Dict[str, FileHash]:
        """Scan directory and calculate hashes for all files."""
        if extensions is None:
            extensions = {'.md', '.txt', '.py', '.json', '.yml', '.yaml', '.xml', '.html', '.css', '.js'}
            
        file_hashes = {}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions and Path(file).suffix.lower() not in extensions:
                    continue
                    
                file_path = Path(root) / file
                try:
                    relative_path = str(file_path.relative_to(self.base_dir))
                    file_hashes[relative_path] = self.get_file_hash(file_path)
                except Exception:
                    # Skip files that can't be read
                    continue
                    
        return file_hashes
        
    def detect_changes(self, source_dir: Path, target_dir: Path, 
                      extensions: Set[str] = None) -> Dict[str, List[str]]:
        """Detect changes between source and target directories."""
        if extensions is None:
            extensions = {'.md', '.txt', '.py', '.json', '.yml', '.yaml', '.xml', '.html', '.css', '.js'}
            
        source_hashes = self.scan_directory(source_dir, extensions)
        target_hashes = self.scan_directory(target_dir, extensions)
        
        added = []
        modified = []
        deleted = []
        
        # Check for added and modified files
        for relative_path, source_hash in source_hashes.items():
            if relative_path not in target_hashes:
                added.append(relative_path)
            elif target_hashes[relative_path].hash != source_hash.hash:
                modified.append(relative_path)
                
        # Check for deleted files
        for relative_path in target_hashes:
            if relative_path not in source_hashes:
                deleted.append(relative_path)
                
        return {
            'added': added,
            'modified': modified,
            'deleted': deleted
        }
        
    def get_changed_files(self, source_dir: Path, target_dir: Path, 
                         extensions: Set[str] = None) -> List[str]:
        """Get list of all changed files between directories."""
        changes = self.detect_changes(source_dir, target_dir, extensions)
        return changes['added'] + changes['modified']
        
    def is_file_changed(self, source_file: Path, target_file: Path) -> bool:
        """Check if a specific file has changed."""
        if not target_file.exists():
            return True
            
        source_hash = self.get_file_hash(source_file)
        target_hash = self.get_file_hash(target_file)
        
        return source_hash.hash != target_hash.hash


class IncrementalSync:
    def __init__(self, source_dir: Path, target_dir: Path):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.change_detector = ChangeDetector(source_dir)
        self.sync_log_file = source_dir / ".sync_log.json"
        self.sync_log: List[Dict] = []
        self.load_sync_log()
        
    def load_sync_log(self):
        """Load sync log from file."""
        if self.sync_log_file.exists():
            try:
                with open(self.sync_log_file, 'r') as f:
                    self.sync_log = json.load(f)
            except Exception as e:
                print(f"Error loading sync log: {e}")
                
    def save_sync_log(self):
        """Save sync log to file."""
        try:
            with open(self.sync_log_file, 'w') as f:
                json.dump(self.sync_log, f, indent=2)
        except Exception as e:
            print(f"Error saving sync log: {e}")
            
    def sync_changes(self, extensions: Set[str] = None) -> Dict[str, int]:
        """Sync only changed files from source to target."""
        if extensions is None:
            extensions = {'.md', '.txt', '.py', '.json', '.yml', '.yaml', '.xml', '.html', '.css', '.js'}
            
        start_time = time.time()
        
        changes = self.change_detector.detect_changes(self.source_dir, self.target_dir, extensions)
        
        # Create target directory if it doesn't exist
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Sync added and modified files
        synced_files = 0
        for relative_path in changes['added'] + changes['modified']:
            source_path = self.source_dir / relative_path
            target_path = self.target_dir / relative_path
            
            # Create target directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, target_path)
            synced_files += 1
            
        # Remove deleted files from target
        for relative_path in changes['deleted']:
            target_path = self.target_dir / relative_path
            if target_path.exists():
                target_path.unlink()
                
        # Log sync operation
        sync_entry = {
            'timestamp': datetime.now().isoformat(),
            'source': str(self.source_dir),
            'target': str(self.target_dir),
            'added_count': len(changes['added']),
            'modified_count': len(changes['modified']),
            'deleted_count': len(changes['deleted']),
            'synced_count': synced_files,
            'duration': time.time() - start_time
        }
        
        self.sync_log.append(sync_entry)
        self.save_sync_log()
        
        return {
            'added': len(changes['added']),
            'modified': len(changes['modified']),
            'deleted': len(changes['deleted']),
            'synced': synced_files,
            'duration': time.time() - start_time
        }
        
    def get_sync_stats(self) -> Dict:
        """Get statistics about sync operations."""
        if not self.sync_log:
            return {'total_syncs': 0}
            
        total_syncs = len(self.sync_log)
        total_files_synced = sum(entry['synced_count'] for entry in self.sync_log)
        avg_duration = sum(entry['duration'] for entry in self.sync_log) / total_syncs
        
        last_sync = self.sync_log[-1] if self.sync_log else None
        
        return {
            'total_syncs': total_syncs,
            'total_files_synced': total_files_synced,
            'avg_sync_duration': avg_duration,
            'last_sync': last_sync
        }
        
    def preview_sync(self, extensions: Set[str] = None) -> Dict[str, List[str]]:
        """Preview what would be synced without actually syncing."""
        if extensions is None:
            extensions = {'.md', '.txt', '.py', '.json', '.yml', '.yaml', '.xml', '.html', '.css', '.js'}
            
        return self.change_detector.detect_changes(self.source_dir, self.target_dir, extensions)


def main():
    # Example usage
    print("Incremental Sync with Change Detection System")
    print("=" * 50)
    
    # This would typically be used to sync between worktrees
    # For example: source = worktrees/docs-main/docs/common/docs, target = worktrees/docs-scientific/docs/common/docs
    print("Incremental sync system initialized")
    print("System ready to detect and sync only changed files between worktrees")


if __name__ == "__main__":
    main()