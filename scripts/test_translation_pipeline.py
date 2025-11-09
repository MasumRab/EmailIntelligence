#!/usr/bin/env python3
"""
Test script for distributed translation pipeline system
"""

import tempfile
from pathlib import Path
from translation_pipeline import DistributedTranslationManager, TranslationDashboard


def test_agent_capability_registration():
    """Test registering agent translation capabilities."""
    print("Testing agent capability registration...")

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Start a translation job (this will register the language pair)
        job_id = manager.start_translation_job(
            document_id="test-doc-1",
            source_language="en",
            target_languages=["es", "fr"],
        )

        # Check if language pairs were registered
        language_pairs = manager.get_language_pairs("en")
        assert "es" in language_pairs, "Should support en->es"
        assert "fr" in language_pairs, "Should support en->fr"

        print("✓ Agent capability registration test passed")


def test_translation_job_creation():
    """Test creating translation jobs."""
    print("\nTesting translation job creation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Create a translation job
        job_id = manager.start_translation_job(
            document_id="test-doc-1",
            source_language="en",
            target_languages=["es", "fr"],
        )

        assert job_id, "Should return a job ID"

        # Get the job
        job = manager.get_translation_job(job_id)
        assert job is not None, "Should retrieve created job"
        assert job.document_id == "test-doc-1", "Document ID should match"
        assert job.source_language == "en", "Source language should match"
        assert "es" in job.target_languages, "Should have Spanish as target"
        assert "fr" in job.target_languages, "Should have French as target"
        assert job.status == "pending", "Job should be pending"

        print("✓ Translation job creation test passed")


def test_translation_memory():
    """Test translation memory functionality."""
    print("\nTesting translation memory functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Add a translation to memory
        manager._add_to_translation_memory(
            "Hello, how are you?", "Hola, ¿cómo estás?", "en", "es", 0.9
        )

        # Look up the translation
        entry = manager.lookup_translation_memory("Hello, how are you?", "en", "es")
        assert entry is not None, "Should find translation in memory"
        assert entry.target_text == "Hola, ¿cómo estás?", "Target text should match"
        assert entry.source_language == "en", "Source language should match"
        assert entry.target_language == "es", "Target language should match"
        assert entry.confidence_score == 0.9, "Confidence score should match"

        # Check that usage count was incremented
        assert entry.usage_count == 1, "Usage count should be 1"

        print("✓ Translation memory functionality test passed")


def test_segment_translation():
    """Test translating segments."""
    print("\nTesting segment translation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Register an agent
        manager.register_agent_capability("translator-agent", "en", "es")

        # Create a job
        source_segments = ["Hello, how are you?"]
        job_id = manager.create_translation_job(
            document_id="translate-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        # Get the segment ID
        job = manager.get_translation_job(job_id)
        assert job is not None, "Should retrieve job"
        assert len(job.translation_units) > 0, "Should have segments"
        unit_id = job.translation_units[0].unit_id

        # Assign agent to unit
        manager.assign_unit_to_agent(unit_id, "translator-agent")

        # Start the job
        manager.start_job_processing(job_id)

        # Translate the unit
        success = manager.complete_translation_unit(
            unit_id=unit_id, translated_text="Hola, ¿cómo estás?", quality_score=0.85
        )

        assert success, "Should translate segment successfully"

        # Check that segment was updated
        updated_job = manager.get_translation_job(job_id)
        assert updated_job is not None, "Should retrieve updated job"
        assert updated_job.translation_units[0].status == "completed", (
            "Unit should be completed"
        )
        assert (
            updated_job.translation_units[0].translated_text == "Hola, ¿cómo estás?"
        ), "Translation should match"
        assert updated_job.translation_units[0].assigned_agent == "translator-agent", (
            "Agent should match"
        )
        assert updated_job.translation_units[0].quality_score == 0.85, (
            "Quality score should match"
        )

        print("✓ Segment translation test passed")


def test_job_progress():
    """Test job progress tracking."""
    print("\nTesting job progress tracking...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Create a job
        source_segments = ["Hello", "World", "Test"]
        job_id = manager.create_translation_job(
            document_id="progress-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        # Get initial progress
        progress = manager.get_job_progress(job_id)
        assert progress["total_units"] == 3, "Should have 3 total units"
        assert progress["completed_units"] == 0, "Should have 0 completed units"
        assert progress["progress_percentage"] == 0.0, "Progress should be 0%"

        # Start the job
        manager.start_job_processing(job_id)

        # Update one unit
        job = manager.get_translation_job(job_id)
        if job and job.translation_units:
            success = manager.complete_translation_unit(
                unit_id=job.translation_units[0].unit_id,
                translated_text="Hola",
                quality_score=0.8,
            )
            assert success, "Should update unit"

        # Get updated progress
        updated_progress = manager.get_job_progress(job_id)
        assert updated_progress["completed_segments"] == 1, (
            "Should have 1 completed segment"
        )
        assert updated_progress["progress_percentage"] == 33.333333333333336, (
            "Progress should be ~33%"
        )

        print("✓ Job progress tracking test passed")


def test_quality_reports():
    """Test quality report functionality."""
    print("\nTesting quality report functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Create a job
        source_segments = ["Hello, world!"]
        job_id = manager.create_translation_job(
            document_id="quality-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        job = manager.get_translation_job(job_id)
        assert job is not None, "Should retrieve job"
        assert len(job.translation_units) > 0, "Should have segments"
        unit_id = job.translation_units[0].unit_id

        # Add a quality report
        report_id = manager.add_quality_report(
            job_id=job_id,
            unit_id=unit_id,
            quality_score=0.8,
            issues=["Minor grammar issue"],
            suggestions=["Consider alternative translation"],
            reviewer="quality-agent",
        )

        assert report_id, "Should return report ID"

        # Get quality reports
        reports = manager.get_quality_reports(job_id)
        assert len(reports) == 1, "Should have 1 quality report"
        assert reports[0].quality_score == 0.8, "Quality score should match"
        assert reports[0].reviewer == "quality-agent", "Reviewer should match"
        assert reports[0].issues[0] == "Minor grammar issue", "Issue should match"
        assert reports[0].suggestions[0] == "Consider alternative translation", (
            "Suggestion should match"
        )

        # Get job quality metrics
        metrics = manager.get_job_quality_metrics(job_id)
        assert metrics["total_segments"] == 1, "Should have 1 total segment"
        assert metrics["segments_with_quality_reports"] == 1, (
            "Should have 1 reported segment"
        )
        assert metrics["average_quality_score"] == 0.8, "Average quality should match"

        print("✓ Quality report functionality test passed")


def test_translation_memory_stats():
    """Test translation memory statistics."""
    print("\nTesting translation memory statistics...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Add some translations to memory
        manager._add_to_translation_memory("Hello", "Hola", "en", "es", 0.9)
        manager._add_to_translation_memory("Goodbye", "Adiós", "en", "es", 0.85)
        manager._add_to_translation_memory("Thank you", "Merci", "en", "fr", 0.95)

        # Get stats
        stats = manager.get_translation_memory_stats()

        assert stats["total_entries"] == 3, "Should have 3 entries"
        assert stats["language_pairs"]["en-es"] == 2, "Should have 2 en-es entries"
        assert stats["language_pairs"]["en-fr"] == 1, "Should have 1 en-fr entry"
        assert abs(stats["average_confidence"] - 0.9) < 0.01, (
            "Average confidence should be ~0.9"
        )

        # Check if language pairs are tracked
        supported_pairs = stats["supported_language_pairs"]
        assert "en" in supported_pairs, "Should have 'en' as source language"
        assert "es" in supported_pairs["en"], "Should have 'es' as target for 'en'"
        assert "fr" in supported_pairs["en"], "Should have 'fr' as target for 'en'"

        print("✓ Translation memory statistics test passed")


def test_agent_translation_stats():
    """Test agent translation statistics."""
    print("\nTesting agent translation statistics...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager
        manager = DistributedTranslationManager(translation_file=translation_file)

        # Register agent capability
        manager.register_agent_capability("stats-agent", "en", "es")

        # Create a job
        source_segments = ["Hello", "World"]
        job_id = manager.create_translation_job(
            document_id="stats-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        manager.start_translation_job(job_id, ["stats-agent"])

        # Translate segments
        job = manager.get_translation_job(job_id)
        if job:
            for i, segment in enumerate(job.translation_units):
                manager.translate_segment(
                    job_id=job_id,
                    unit_id=segment.unit_id,
                    agent_id="stats-agent",
                    translated_text=f"Translation {i + 1}",
                    quality_score=0.8 + i * 0.1,
                )

        # Get agent stats
        stats = manager.get_agent_translation_stats("stats-agent")

        assert stats["agent_id"] == "stats-agent", "Agent ID should match"
        assert stats["total_segments_translated"] == 2, (
            "Should have translated 2 segments"
        )
        assert abs(stats["average_confidence"] - 0.85) < 0.01, (
            "Average confidence should be ~0.85"
        )
        assert "en-es" in stats["language_pairs"], "Should have en-es language pair"

        print("✓ Agent translation statistics test passed")


def test_translation_dashboard():
    """Test translation dashboard functionality."""
    print("\nTesting translation dashboard functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_distributed_translation.json"

        # Initialize translation manager and dashboard
        manager = DistributedTranslationManager(translation_file=translation_file)
        dashboard = TranslationDashboard(manager)

        # Register agent and create job
        manager.register_agent_capability("dashboard-agent", "en", "es")

        source_segments = ["Hello", "World", "Test"]
        job_id = manager.create_translation_job(
            document_id="dashboard-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        # Add some quality reports
        job = manager.get_translation_job(job_id)
        if job and job.translation_units:
            manager.add_quality_report(
                job_id=job_id,
                unit_id=job.translation_units[0].unit_id,
                quality_score=0.9,
                reviewer="reviewer-1",
            )

        # Test dashboard methods (should not crash)
        dashboard.display_job_overview(job_id)
        dashboard.display_translation_memory_stats()
        dashboard.display_agent_stats("dashboard-agent")
        dashboard.display_quality_reports(job_id)
        dashboard.display_job_segments(job_id)

        print("✓ Translation dashboard functionality test passed")


def test_translation_persistence():
    """Test translation data persistence."""
    print("\nTesting translation data persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        translation_file = tmp_path / ".test_persistence_translation.json"

        # Initialize manager and add data
        manager1 = DistributedTranslationManager(translation_file=translation_file)

        # Register agent capability
        manager1.register_agent_capability("persist-agent", "en", "es")

        # Create and start a job
        source_segments = ["Test persistence"]
        job_id = manager1.create_translation_job(
            document_id="persist-doc-1",
            source_language="en",
            target_language="es",
            source_segments=source_segments,
        )

        manager1.start_translation_job(job_id, ["persist-agent"])

        # Translate a segment
        job = manager1.get_translation_job(job_id)
        if job and job.translation_units:
            manager1.translate_segment(
                job_id=job_id,
                unit_id=job.translation_units[0].unit_id,
                agent_id="persist-agent",
                translated_text="Prueba persistencia",
                quality_score=0.85,
            )

        # Add to translation memory
        manager1._add_to_translation_memory("Test", "Prueba", "en", "es", 0.8)

        # Add quality report
        if job and job.translation_units:
            manager1.add_quality_report(
                job_id=job_id,
                unit_id=job.translation_units[0].unit_id,
                quality_score=0.9,
            )

        # Create new manager and load data
        manager2 = DistributedTranslationManager(translation_file=translation_file)

        # Verify data was loaded correctly
        loaded_job = manager2.get_translation_job(job_id)
        assert loaded_job is not None, "Should load job"
        assert loaded_job.status == "in_progress", "Job status should match"
        assert (
            loaded_job.translation_units[0].translated_text == "Prueba persistencia"
        ), "Translation should match"
        assert loaded_job.translation_units[0].quality_score == 0.85, (
            "Quality score should match"
        )

        # Check translation memory
        entry = manager2.lookup_translation_memory("Test", "en", "es")
        assert entry is not None, "Should load translation memory"
        assert entry.target_text == "Prueba", "Memory translation should match"
        assert entry.confidence_score == 0.8, "Memory confidence should match"

        # Check quality reports
        reports = manager2.get_quality_reports(job_id)
        assert len(reports) == 1, "Should load quality report"
        assert reports[0].quality_score == 0.9, "Quality score should match"

        # Check agent capabilities
        available_agents = manager2.get_available_agents("en", "es")
        assert "persist-agent" in available_agents, "Agent capability should be loaded"

        print("✓ Translation data persistence test passed")


def main():
    """Run all tests."""
    print("Running Distributed Translation Pipeline Tests")
    print("=" * 48)

    try:
        test_agent_capability_registration()
        test_translation_job_creation()
        test_translation_memory()
        test_segment_translation()
        test_job_progress()
        test_quality_reports()
        test_translation_memory_stats()
        test_agent_translation_stats()
        test_translation_dashboard()
        test_translation_persistence()

        print("\n" + "=" * 48)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
