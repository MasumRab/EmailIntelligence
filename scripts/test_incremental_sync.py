#!/usr/bin/env python3
"""
Test script for incremental sync with change detection
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from incremental_sync import IncrementalSync, ChangeDetector

def test_incremental_sync():
    """Test the incremental sync system."""
    print("Testing Incremental Sync with Change Detection...")
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_dir = temp_path / "source"
        target_dir = temp_path / "target"
        
        # Create source directory with some files
        source_dir.mkdir()
        target_dir.mkdir()
        
        # Create test files
        (source_dir / "test1.md").write_text("# Test Document 1\n\nThis is test content.")
        (source_dir / "test2.md").write_text("# Test Document 2\n\nThis is more test content.")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "test3.md").write_text("# Test Document 3\n\nContent in subdirectory.")
        
        # Create some initial files in target that will be detected as changed
        (target_dir / "test1.md").write_text("# Test Document 1\n\nThis is OLD content.")
        (target_dir / "test4.md").write_text("# Test Document 4\n\nThis file will be deleted.")
        
        # Create sync system
        sync = IncrementalSync(source_dir, target_dir)
        
        # Preview sync
        preview = sync.preview_sync()
        print(f"Preview - Added: {len(preview['added'])}, Modified: {len(preview['modified'])}, Deleted: {len(preview['deleted'])}")
        print(f"  Added: {preview['added']}")
        print(f"  Modified: {preview['modified']}")
        print(f"  Deleted: {preview['deleted']}")
        
        # Perform sync
        result = sync.sync_changes()
        print(f"Sync result - Added: {result['added']}, Modified: {result['modified']}, Deleted: {result['deleted']}")
        print(f"  Files synced: {result['synced']}")
        print(f"  Duration: {result['duration']:.2f} seconds")
        
        # Check if files were properly synced
        test1_source = (source_dir / "test1.md").read_text()
        test1_target = (target_dir / "test1.md").read_text()
        print(f"test1.md synced correctly: {test1_source == test1_target}")
        
        # Check if new file was added
        test2_exists = (target_dir / "test2.md").exists()
        print(f"test2.md added: {test2_exists}")
        
        # Check if deleted file was removed
        test4_exists = (target_dir / "test4.md").exists()
        print(f"test4.md deleted: {not test4_exists}")
        
        # Get sync stats
        stats = sync.get_sync_stats()
        print(f"Sync stats: {stats}")
        
        print("Incremental sync test completed successfully!")

if __name__ == "__main__":
    test_incremental_sync()