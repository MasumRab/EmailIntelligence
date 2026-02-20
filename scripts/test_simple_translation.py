#!/usr/bin/env python3
"""
Simple test for distributed translation system
"""

import tempfile
from pathlib import Path
from distributed_translation import DistributedTranslationManager


def test_basic_functionality():
    """Test basic distributed translation functionality."""
    print("Testing basic distributed translation functionality...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_translation.json"
        
        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)
        
        # Register agent capability
        success = manager.register_agent_capability("translator-1", "en", "es")
        assert success, "Should register agent capability"
        
        # Create translation job
        source_segments = ["Hello world", "This is a test"]
        job_id = manager.create_translation_job(
            document_id="test-doc",
            source_language="en",
            target_language="es",
            source_segments=source_segments
        )
        
        assert job_id, "Should create translation job"
        
        # Start job
        success = manager.start_translation_job(job_id, ["translator-1"])
        assert success, "Should start translation job"
        
        # Get job
        job = manager.get_translation_job(job_id)
        assert job is not None, "Should retrieve job"
        assert len(job.segments) == 2, "Should have 2 segments"
        
        # Translate segment
        segment_id = job.segments[0].segment_id
        success = manager.translate_segment(
            job_id=job_id,
            segment_id=segment_id,
            agent_id="translator-1",
            translated_text="Hola mundo",
            confidence_score=0.9
        )
        
        assert success, "Should translate segment"
        
        # Check translation
        updated_job = manager.get_translation_job(job_id)
        assert updated_job.segments[0].translated_text == "Hola mundo", "Translation should match"
        assert updated_job.segments[0].translation_status == "completed", "Status should be completed"
        
        print("✓ Basic distributed translation functionality test passed")


def main():
    """Run tests."""
    print("Running Distributed Translation Tests")
    print("=" * 38)
    
    try:
        test_basic_functionality()
        print("\n" + "=" * 38)
        print("All tests passed! ✓")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()