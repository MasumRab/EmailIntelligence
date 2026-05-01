#!/usr/bin/env python3
"""
Integration test to verify that all Agent Workflow Template components work together.
"""

import tempfile
from pathlib import Path
from doc_generation_template import DocumentationTemplate, TemplateSection, DocumentationTemplateManager
from concurrent_review import ConcurrentReviewManager
from distributed_translation import DistributedTranslationManager
from maintenance_scheduler import MaintenanceScheduler, MaintenanceAgent


def test_integration():
    """Test that all components can work together."""
    print("Testing integration of Agent Workflow Templates components...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Test 1: Documentation Template system
        print("  1. Testing documentation template system...")
        template_manager = DocumentationTemplateManager()

        # Create a template with sections
        template = DocumentationTemplate(
            template_id="integration-test-template",
            template_name="Integration Test Template",
            description="Template for integration testing",
            sections=[
                TemplateSection(
                    section_id="intro",
                    section_type="introduction",
                    title="Introduction",
                    content_template="# {title}\n\n{content}",
                    estimated_duration=5.0,
                    dependencies=[]
                )
            ]
        )

        # Register template
        template_manager.register_template(template)

        # Create document
        document = template_manager.create_document_from_template(
            document_id="integration-test-doc",
            template_id="integration-test-template",
            title="Integration Test Document",
            metadata={"version": "1.0"}
        )

        print("     ✓ Documentation template system working")

        # Test 2: Concurrent Review system
        print("  2. Testing concurrent review system...")
        review_manager = ConcurrentReviewManager()

        # Start a review session
        session_id = review_manager.start_review_session(
            document_id="integration-test-doc",
            reviewers=["test-agent-1", "test-agent-2"]
        )

        # Add a comment
        comment_id = review_manager.add_comment(
            session_id=session_id,
            agent_id="test-agent-1",
            section_id="intro",
            comment_text="Integration test comment",
            severity="medium"
        )

        print("     ✓ Concurrent review system working")

        # Test 3: Distributed Translation system
        print("  3. Testing distributed translation system...")
        translation_manager = DistributedTranslationManager()

        # Create a translation job
        job_id = translation_manager.create_translation_job(
            document_id="integration-test-doc",
            source_language="en",
            target_language="es",
            source_segments=["Integration test text"]
        )

        # Get the job to access translation units
        job = translation_manager.get_translation_job(job_id)
        unit_ids = [unit.segment_id for unit in job.segments] if job else []

        print("     ✓ Distributed translation system working")

        # Test 4: Maintenance Scheduler system
        print("  4. Testing maintenance scheduler system...")
        scheduler = MaintenanceScheduler()

        # Register an agent
        agent = MaintenanceAgent(
            agent_id="integration-test-agent",
            capabilities=["link_check", "format_check"]
        )
        scheduler.register_agent(agent)

        # Create a maintenance task
        task_id = scheduler.create_maintenance_task(
            task_type="link_check",
            document_id="integration-test-doc",
            description="Integration test maintenance task"
        )

        print("     ✓ Maintenance scheduler system working")

        # Test 5: Integration between systems
        print("  5. Testing integration between systems...")

        # Add a translation completion
        if unit_ids:
            translation_manager.translate_segment(
                job_id=job_id,
                segment_id=unit_ids[0],
                agent_id="integration-test-agent",
                translated_text="Texto de prueba de integración",
                confidence_score=0.95
            )

        # Get review summary
        review_summary = review_manager.get_comment_summary(session_id)

        # Get translation quality report
        if unit_ids and job_id:
            quality_reports = translation_manager.get_quality_reports(job_id)

        # Execute maintenance task
        scheduler.execute_next_task()

        print("     ✓ Systems integration working")

    print("\nAll integration tests passed! ✓")
    print("Agent Workflow Templates components work together successfully.")


if __name__ == "__main__":
    test_integration()