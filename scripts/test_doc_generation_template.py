#!/usr/bin/env python3
"""
Test script for documentation generation template system
"""

import tempfile
from pathlib import Path
from doc_generation_template import (
    DocumentationTemplateManager,
    DocumentationTemplate,
    TemplateSection,
    TemplateDashboard,
)


def test_template_registration():
    """Test template registration and retrieval."""
    print("Testing template registration and retrieval...")

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Create a test template
        sections = [
            TemplateSection(
                section_id="intro",
                section_type="introduction",
                title="Introduction",
                content_template="Introduction to {topic}",
                estimated_duration=5.0,
            ),
            TemplateSection(
                section_id="main",
                section_type="main_content",
                title="Main Content",
                content_template="Main content about {topic}",
                estimated_duration=15.0,
                dependencies=["intro"],
            ),
        ]

        template = DocumentationTemplate(
            template_id="test-template",
            template_name="Test Template",
            description="A test template for documentation",
            sections=sections,
            required_sections=["intro", "main"],
            optional_sections=[],
        )

        # Register template
        template_manager.register_template(template)

        # Retrieve template
        retrieved_template = template_manager.get_template("test-template")

        # Verify template was registered correctly
        assert retrieved_template is not None, "Should retrieve registered template"
        assert retrieved_template.template_id == "test-template", (
            "Template ID should match"
        )
        assert retrieved_template.template_name == "Test Template", (
            "Template name should match"
        )
        assert len(retrieved_template.sections) == 2, "Should have 2 sections"

        # List templates
        templates = template_manager.list_templates()
        assert len(templates) >= 1, "Should have at least 1 template"

        print("✓ Template registration and retrieval test passed")


def test_document_generation():
    """Test document generation from templates."""
    print("\nTesting document generation from templates...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Create a document from an existing template
        document = template_manager.create_document_from_template(
            document_id="test-doc-1",
            template_id="api_documentation",  # Use existing template
            title="Test API Documentation",
        )

        # Verify document was created
        assert document is not None, "Should create document from template"
        assert document.document_id == "test-doc-1", "Document ID should match"
        assert document.template_id == "api_documentation", "Template ID should match"
        assert document.title == "Test API Documentation", "Title should match"
        assert len(document.sections) > 0, "Should have sections from template"

        # Retrieve document
        retrieved_document = template_manager.get_document("test-doc-1")
        assert retrieved_document is not None, "Should retrieve created document"
        assert retrieved_document.document_id == "test-doc-1", (
            "Document ID should match"
        )

        print("✓ Document generation from templates test passed")


def test_section_content_update():
    """Test updating section content."""
    print("\nTesting section content update...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Create a document
        document = template_manager.create_document_from_template(
            document_id="content-test-doc",
            template_id="api_documentation",
            title="Content Test Document",
        )

        # Get first section
        first_section = document.sections[0] if document.sections else None
        assert first_section is not None, "Should have at least one section"

        # Update section content
        success = template_manager.update_section_content(
            document_id="content-test-doc",
            section_id=first_section.section_id,
            content="# Introduction\n\nThis is a test introduction.",
            agent_id="test-agent-1",
            status="completed",
        )

        # Verify update was successful
        assert success, "Should successfully update section content"

        # Retrieve updated document
        updated_document = template_manager.get_document("content-test-doc")
        assert updated_document is not None, "Should retrieve updated document"

        # Verify content was updated
        updated_section = None
        for section in updated_document.sections:
            if section.section_id == first_section.section_id:
                updated_section = section
                break

        assert updated_section is not None, "Should find updated section"
        assert (
            updated_section.content == "# Introduction\n\nThis is a test introduction."
        ), "Content should match"
        assert updated_section.agent_id == "test-agent-1", "Agent ID should match"
        assert updated_section.status == "completed", "Status should be completed"
        assert updated_section.generation_time > 0, "Generation time should be set"

        print("✓ Section content update test passed")


def test_document_progress():
    """Test document progress tracking."""
    print("\nTesting document progress tracking...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Create a document
        document = template_manager.create_document_from_template(
            document_id="progress-test-doc",
            template_id="api_documentation",
            title="Progress Test Document",
        )

        # Get initial progress
        progress = template_manager.get_document_progress("progress-test-doc")

        print(f"Initial progress: {progress}")

        # Verify progress structure
        assert "total_sections" in progress, "Should have total_sections"
        assert "completed_sections" in progress, "Should have completed_sections"
        assert "progress_percentage" in progress, "Should have progress_percentage"

        # Update one section to completed
        if document.sections:
            first_section = document.sections[0]
            template_manager.update_section_content(
                document_id="progress-test-doc",
                section_id=first_section.section_id,
                content="# Test Content\n\nThis is test content.",
                agent_id="progress-agent",
                status="completed",
            )

            # Get updated progress
            updated_progress = template_manager.get_document_progress(
                "progress-test-doc"
            )

            print(f"Updated progress: {updated_progress}")

            # Verify progress was updated
            assert updated_progress["completed_sections"] == 1, (
                "Should have 1 completed section"
            )
            assert updated_progress["progress_percentage"] > 0, (
                "Progress percentage should be > 0"
            )

        print("✓ Document progress tracking test passed")


def test_parallel_generation_plan():
    """Test parallel generation plan calculation."""
    print("\nTesting parallel generation plan calculation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Create a document
        document = template_manager.create_document_from_template(
            document_id="plan-test-doc",
            template_id="api_documentation",
            title="Plan Test Document",
        )

        # Get generation plan
        plan = template_manager.get_parallel_generation_plan("plan-test-doc")

        print(f"Generation plan: {plan}")

        # Verify plan structure
        assert isinstance(plan, list), "Plan should be a list"
        assert len(plan) > 0, "Plan should have at least one wave"

        # Each wave should be a list of section IDs
        for wave in plan:
            assert isinstance(wave, list), "Each wave should be a list"
            assert len(wave) > 0, "Each wave should have sections"

        print("✓ Parallel generation plan calculation test passed")


def test_template_complexity():
    """Test template complexity calculation."""
    print("\nTesting template complexity calculation...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager
        template_manager = DocumentationTemplateManager(templates_file=templates_file)

        # Get complexity for existing template
        complexity = template_manager.get_template_complexity("api_documentation")

        print(f"API template complexity: {complexity}")

        # Verify complexity metrics
        assert "total_sections" in complexity, "Should have total_sections"
        assert "total_dependencies" in complexity, "Should have total_dependencies"
        assert "max_dependency_depth" in complexity, "Should have max_dependency_depth"
        assert "complexity_score" in complexity, "Should have complexity_score"

        # Values should be non-negative
        assert complexity["total_sections"] >= 0, (
            "Total sections should be non-negative"
        )
        assert complexity["total_dependencies"] >= 0, (
            "Total dependencies should be non-negative"
        )
        assert complexity["max_dependency_depth"] >= 0, (
            "Max dependency depth should be non-negative"
        )
        assert complexity["complexity_score"] >= 0, (
            "Complexity score should be non-negative"
        )

        print("✓ Template complexity calculation test passed")


def test_template_dashboard():
    """Test template dashboard functionality."""
    print("\nTesting template dashboard functionality...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_doc_templates.json"

        # Initialize template manager and dashboard
        template_manager = DocumentationTemplateManager(templates_file=templates_file)
        dashboard = TemplateDashboard(template_manager)

        # Test dashboard methods (should not crash)
        dashboard.display_available_templates()
        dashboard.display_template_details("api_documentation")

        # Create a document for progress display
        document = template_manager.create_document_from_template(
            document_id="dashboard-test-doc",
            template_id="api_documentation",
            title="Dashboard Test Document",
        )

        dashboard.display_document_progress("dashboard-test-doc")
        dashboard.display_section_estimates("api_documentation")

        print("✓ Template dashboard functionality test passed")


def test_template_persistence():
    """Test template and document persistence."""
    print("\nTesting template and document persistence...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        templates_file = tmp_path / ".test_persistence_templates.json"

        # Initialize template manager and add data
        template_manager1 = DocumentationTemplateManager(templates_file=templates_file)

        # Create a document
        document1 = template_manager1.create_document_from_template(
            document_id="persistence-test-doc",
            template_id="api_documentation",
            title="Persistence Test Document",
        )

        # Update a section
        if document1.sections:
            first_section = document1.sections[0]
            template_manager1.update_section_content(
                document_id="persistence-test-doc",
                section_id=first_section.section_id,
                content="# Persistent Content\n\nThis content should persist.",
                agent_id="persistence-agent",
                status="completed",
            )

        # Create new template manager and load data
        template_manager2 = DocumentationTemplateManager(templates_file=templates_file)

        # Verify data was loaded correctly
        loaded_document = template_manager2.get_document("persistence-test-doc")
        assert loaded_document is not None, "Should load persisted document"
        assert loaded_document.title == "Persistence Test Document", (
            "Title should match"
        )

        # Check if section was loaded correctly
        if loaded_document.sections:
            loaded_section = loaded_document.sections[0]
            assert (
                loaded_section.content
                == "# Persistent Content\n\nThis content should persist."
            ), "Content should match"
            assert loaded_section.agent_id == "persistence-agent", (
                "Agent ID should match"
            )
            assert loaded_section.status == "completed", "Status should match"

        print("✓ Template and document persistence test passed")


def main():
    """Run all tests."""
    print("Running Documentation Generation Template Tests")
    print("=" * 50)

    try:
        test_template_registration()
        test_document_generation()
        test_section_content_update()
        test_document_progress()
        test_parallel_generation_plan()
        test_template_complexity()
        test_template_dashboard()
        test_template_persistence()

        print("\n" + "=" * 50)
        print("All tests passed! ✓")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
