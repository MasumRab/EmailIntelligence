#!/usr/bin/env python3
"""
Test script for conflict prediction and pre-resolution
"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from conflict_predictor import ConflictPredictor, ConflictResolver, ConflictPrediction, ConflictType, ConflictSeverity

def test_conflict_prediction():
    """Test the conflict prediction and resolution system."""
    print("Testing Conflict Prediction and Pre-resolution System...")

    # Create predictor and resolver
    predictor = ConflictPredictor()
    resolver = ConflictResolver()

    # Add some sample changes that would cause conflicts
    predictor.add_file_change("docs/api.md", "# API Docs\nOriginal content", "modify", "worker1")
    predictor.add_file_change("docs/guide.md", "# User Guide\nInstructions", "add", "worker2")

    # Create pending changes that would conflict
    from conflict_predictor import FileChange
    import time

    pending_changes = [
        FileChange("docs/api.md", "hash1", "modify", "worker3", time.time()),
        FileChange("docs/api.md", "hash2", "modify", "worker4", time.time()),
        FileChange("docs/new.md", "hash3", "add", "worker1", time.time()),
        FileChange("docs/new.md", "hash4", "add", "worker2", time.time())
    ]

    # Predict conflicts
    conflicts = predictor.predict_conflicts(pending_changes)
    print(f"Predicted conflicts: {len(conflicts)}")

    for i, conflict in enumerate(conflicts):
        print(f"  Conflict {i+1}:")
        print(f"    File: {conflict.file_path}")
        print(f"    Type: {conflict.conflict_type.value}")
        print(f"    Severity: {conflict.severity.value}")
        print(f"    Confidence: {conflict.confidence:.2f}")
        print(f"    Description: {conflict.description}")
        print(f"    Suggested resolution: {conflict.suggested_resolution}")
        print(f"    Affected workers: {conflict.affected_workers}")

    # Test conflict resolution
    if conflicts:
        # Create sample file contents for resolution
        file_contents = {
            "worker3:docs/api.md": "# API Docs\nContent from worker 3",
            "worker4:docs/api.md": "# API Docs\nContent from worker 4"
        }

        # Attempt to pre-resolve first conflict
        resolved_content = resolver.pre_resolve_conflict(conflicts[0], file_contents)
        if resolved_content:
            print(f"Successfully pre-resolved conflict, merged content length: {len(resolved_content)}")
        else:
            print("Conflict requires manual resolution")

    # Get statistics
    pred_stats = predictor.get_conflict_statistics()
    res_stats = resolver.get_resolution_statistics()
    print(f"Prediction stats: {pred_stats}")
    print(f"Resolution stats: {res_stats}")

    print("Conflict prediction test completed successfully!")

if __name__ == "__main__":
    test_conflict_prediction()
