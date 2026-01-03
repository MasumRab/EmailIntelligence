#!/usr/bin/env python3
"""
Parallel Documentation Generation Templates
Develop templates for agents to generate documentation in parallel.
"""

import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import re


@dataclass
class TemplateSection:
    section_id: str
    section_type: str  # "header", "introduction", "api_reference", "examples", "troubleshooting", etc.
    title: str
    content_template: str
    estimated_duration: float  # minutes
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentationTemplate:
    template_id: str
    template_name: str
    description: str
    sections: List[TemplateSection]
    required_sections: List[str] = field(default_factory=list)
    optional_sections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedSection:
    section_id: str
    template_section_id: str
    title: str
    content: str
    generation_time: float
    agent_id: str
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedDocument:
    document_id: str
    template_id: str
    title: str
    sections: List[GeneratedSection]
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    start_time: float = 0.0
    end_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentationTemplateManager:
    def __init__(self, templates_file: Path = None):
        self.templates_file = templates_file or Path(".doc_templates.json")
        self.templates: Dict[str, DocumentationTemplate] = {}
        self.generated_documents: Dict[str, GeneratedDocument] = {}
        self._lock = threading.RLock()
        self.load_templates()
        
    def register_template(self, template: DocumentationTemplate):
        """Register a new documentation template."""
        with self._lock:
            self.templates[template.template_id] = template
            self._save_templates()
            
    def get_template(self, template_id: str) -> Optional[DocumentationTemplate]:
        """Get a template by ID."""
        with self._lock:
            return self.templates.get(template_id)
            
    def list_templates(self) -> List[DocumentationTemplate]:
        """List all available templates."""
        with self._lock:
            return list(self.templates.values())
            
    def create_document_from_template(self, document_id: str, template_id: str, 
                                    title: str, metadata: Dict[str, Any] = None) -> Optional[GeneratedDocument]:
        """Create a new document based on a template."""
        if metadata is None:
            metadata = {}
            
        with self._lock:
            template = self.templates.get(template_id)
            if not template:
                return None
                
            # Create sections based on template
            sections = [
                GeneratedSection(
                    section_id=f"{document_id}-{section.section_id}",
                    template_section_id=section.section_id,
                    title=section.title,
                    content="",  # Will be filled by agents
                    generation_time=0.0,
                    agent_id="",  # Will be assigned by workflow
                    status="pending"
                )
                for section in template.sections
            ]
            
            document = GeneratedDocument(
                document_id=document_id,
                template_id=template_id,
                title=title,
                sections=sections,
                status="pending",
                start_time=time.time(),
                metadata=metadata
            )
            
            self.generated_documents[document_id] = document
            self._save_templates()
            
            return document
            
    def get_document(self, document_id: str) -> Optional[GeneratedDocument]:
        """Get a generated document by ID."""
        with self._lock:
            return self.generated_documents.get(document_id)
            
    def update_section_content(self, document_id: str, section_id: str, 
                             content: str, agent_id: str, 
                             status: str = "completed") -> bool:
        """Update the content of a document section."""
        with self._lock:
            document = self.generated_documents.get(document_id)
            if not document:
                return False
                
            # Find the section
            for section in document.sections:
                if section.section_id == section_id:
                    section.content = content
                    section.agent_id = agent_id
                    section.status = status
                    section.generation_time = time.time() - document.start_time
                    self._save_templates()
                    return True
                    
            return False
            
    def get_sections_by_status(self, document_id: str, 
                              status: str) -> List[GeneratedSection]:
        """Get all sections of a document with a specific status."""
        with self._lock:
            document = self.generated_documents.get(document_id)
            if not document:
                return []
                
            return [section for section in document.sections if section.status == status]
            
    def get_document_progress(self, document_id: str) -> Dict[str, Any]:
        """Get progress information for a document."""
        with self._lock:
            document = self.generated_documents.get(document_id)
            if not document:
                return {}
                
            total_sections = len(document.sections)
            completed_sections = len([s for s in document.sections if s.status == "completed"])
            in_progress_sections = len([s for s in document.sections if s.status == "in_progress"])
            pending_sections = len([s for s in document.sections if s.status == "pending"])
            
            return {
                'document_id': document_id,
                'total_sections': total_sections,
                'completed_sections': completed_sections,
                'in_progress_sections': in_progress_sections,
                'pending_sections': pending_sections,
                'progress_percentage': (completed_sections / total_sections * 100) if total_sections > 0 else 0,
                'status': document.status
            }
            
    def get_parallel_generation_plan(self, document_id: str) -> List[List[str]]:
        """Get a plan for parallel section generation based on dependencies."""
        with self._lock:
            document = self.generated_documents.get(document_id)
            if not document:
                return []
                
            template = self.templates.get(document.template_id)
            if not template:
                return []
                
            # Build dependency graph
            dependencies = defaultdict(set)
            dependents = defaultdict(set)
            
            for section in template.sections:
                for dep in section.dependencies:
                    dependencies[section.section_id].add(dep)
                    dependents[dep].add(section.section_id)
                    
            # Create generation waves (sections that can be generated in parallel)
            waves = []
            completed_sections = set()
            remaining_sections = set(section.template_section_id for section in document.sections)
            
            while remaining_sections:
                # Find sections with all dependencies met
                ready_sections = [
                    section_id for section_id in remaining_sections
                    if dependencies[section_id].issubset(completed_sections)
                ]
                
                if not ready_sections:
                    # Circular dependency or missing dependency
                    ready_sections = list(remaining_sections)
                    
                waves.append(ready_sections)
                
                # Mark these sections as completed
                completed_sections.update(ready_sections)
                remaining_sections.difference_update(ready_sections)
                
            return waves
            
    def get_section_estimated_duration(self, template_id: str, section_id: str) -> float:
        """Get estimated duration for a section."""
        with self._lock:
            template = self.templates.get(template_id)
            if not template:
                return 0.0
                
            for section in template.sections:
                if section.section_id == section_id:
                    return section.estimated_duration
                    
            return 0.0
            
    def get_template_complexity(self, template_id: str) -> Dict[str, Any]:
        """Get complexity metrics for a template."""
        with self._lock:
            template = self.templates.get(template_id)
            if not template:
                return {}
                
            total_sections = len(template.sections)
            total_dependencies = sum(len(section.dependencies) for section in template.sections)
            max_dependency_depth = self._calculate_max_dependency_depth(template)
            
            return {
                'template_id': template_id,
                'total_sections': total_sections,
                'total_dependencies': total_dependencies,
                'avg_dependencies_per_section': total_dependencies / total_sections if total_sections > 0 else 0,
                'max_dependency_depth': max_dependency_depth,
                'complexity_score': total_sections + total_dependencies + max_dependency_depth
            }
            
    def _calculate_max_dependency_depth(self, template: DocumentationTemplate) -> int:
        """Calculate maximum dependency depth in a template."""
        # Build dependency graph
        dependencies = defaultdict(set)
        for section in template.sections:
            dependencies[section.section_id].update(section.dependencies)
            
        # Calculate depth using BFS
        max_depth = 0
        for section in template.sections:
            depth = self._get_dependency_depth(section.section_id, dependencies, set())
            max_depth = max(max_depth, depth)
            
        return max_depth
        
    def _get_dependency_depth(self, section_id: str, dependencies: Dict[str, Set[str]], 
                            visited: Set[str]) -> int:
        """Get dependency depth for a section."""
        if section_id in visited:
            return 0  # Circular dependency
            
        visited.add(section_id)
        max_child_depth = 0
        
        for dep in dependencies.get(section_id, set()):
            child_depth = self._get_dependency_depth(dep, dependencies, visited.copy())
            max_child_depth = max(max_child_depth, child_depth)
            
        return max_child_depth + 1
        
    def _save_templates(self):
        """Save templates and generated documents to file."""
        try:
            data = {
                'timestamp': time.time(),
                'templates': {
                    template_id: {
                        'template_id': template.template_id,
                        'template_name': template.template_name,
                        'description': template.description,
                        'sections': [
                            {
                                'section_id': section.section_id,
                                'section_type': section.section_type,
                                'title': section.title,
                                'content_template': section.content_template,
                                'estimated_duration': section.estimated_duration,
                                'dependencies': section.dependencies,
                                'metadata': section.metadata
                            }
                            for section in template.sections
                        ],
                        'required_sections': template.required_sections,
                        'optional_sections': template.optional_sections,
                        'metadata': template.metadata
                    }
                    for template_id, template in self.templates.items()
                },
                'generated_documents': {
                    doc_id: {
                        'document_id': doc.document_id,
                        'template_id': doc.template_id,
                        'title': doc.title,
                        'sections': [
                            {
                                'section_id': section.section_id,
                                'template_section_id': section.template_section_id,
                                'title': section.title,
                                'content': section.content,
                                'generation_time': section.generation_time,
                                'agent_id': section.agent_id,
                                'status': section.status,
                                'metadata': section.metadata
                            }
                            for section in doc.sections
                        ],
                        'status': doc.status,
                        'start_time': doc.start_time,
                        'end_time': doc.end_time,
                        'metadata': doc.metadata
                    }
                    for doc_id, doc in self.generated_documents.items()
                }
            }
            
            with open(self.templates_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving templates: {e}")
            
    def load_templates(self):
        """Load templates and generated documents from file."""
        try:
            if not self.templates_file.exists():
                # Create default templates
                self._create_default_templates()
                return
                
            with open(self.templates_file, 'r') as f:
                data = json.load(f)
                
            # Restore templates
            self.templates.clear()
            for template_id, template_data in data.get('templates', {}).items():
                sections = [
                    TemplateSection(
                        section_id=section_data['section_id'],
                        section_type=section_data['section_type'],
                        title=section_data['title'],
                        content_template=section_data['content_template'],
                        estimated_duration=section_data['estimated_duration'],
                        dependencies=section_data['dependencies'],
                        metadata=section_data.get('metadata', {})
                    )
                    for section_data in template_data.get('sections', [])
                ]
                
                template = DocumentationTemplate(
                    template_id=template_data['template_id'],
                    template_name=template_data['template_name'],
                    description=template_data['description'],
                    sections=sections,
                    required_sections=template_data.get('required_sections', []),
                    optional_sections=template_data.get('optional_sections', []),
                    metadata=template_data.get('metadata', {})
                )
                
                self.templates[template_id] = template
                
            # Restore generated documents
            self.generated_documents.clear()
            for doc_id, doc_data in data.get('generated_documents', {}).items():
                sections = [
                    GeneratedSection(
                        section_id=section_data['section_id'],
                        template_section_id=section_data['template_section_id'],
                        title=section_data['title'],
                        content=section_data['content'],
                        generation_time=section_data['generation_time'],
                        agent_id=section_data['agent_id'],
                        status=section_data['status'],
                        metadata=section_data.get('metadata', {})
                    )
                    for section_data in doc_data.get('sections', [])
                ]
                
                document = GeneratedDocument(
                    document_id=doc_data['document_id'],
                    template_id=doc_data['template_id'],
                    title=doc_data['title'],
                    sections=sections,
                    status=doc_data['status'],
                    start_time=doc_data['start_time'],
                    end_time=doc_data['end_time'],
                    metadata=doc_data.get('metadata', {})
                )
                
                self.generated_documents[doc_id] = document
                
        except Exception as e:
            print(f"Error loading templates: {e}")
            # Create default templates if loading fails
            self._create_default_templates()
            
    def _create_default_templates(self):
        """Create default documentation templates."""
        # API Documentation Template
        api_sections = [
            TemplateSection(
                section_id="header",
                section_type="header",
                title="API Documentation",
                content_template="# {title}\n\nAPI documentation for {api_name}",
                estimated_duration=2.0
            ),
            TemplateSection(
                section_id="introduction",
                section_type="introduction",
                title="Introduction",
                content_template="This document describes the {api_name} API.",
                estimated_duration=5.0,
                dependencies=["header"]
            ),
            TemplateSection(
                section_id="authentication",
                section_type="authentication",
                title="Authentication",
                content_template="## Authentication\n\nThis API uses {auth_type} authentication.",
                estimated_duration=8.0,
                dependencies=["introduction"]
            ),
            TemplateSection(
                section_id="endpoints",
                section_type="endpoints",
                title="Endpoints",
                content_template="## Endpoints\n\nList of available endpoints:",
                estimated_duration=15.0,
                dependencies=["authentication"]
            ),
            TemplateSection(
                section_id="examples",
                section_type="examples",
                title="Examples",
                content_template="## Examples\n\nExample usage:",
                estimated_duration=10.0,
                dependencies=["endpoints"]
            ),
            TemplateSection(
                section_id="errors",
                section_type="errors",
                title="Error Handling",
                content_template="## Error Handling\n\nCommon error responses:",
                estimated_duration=8.0,
                dependencies=["endpoints"]
            ),
            TemplateSection(
                section_id="rate_limiting",
                section_type="rate_limiting",
                title="Rate Limiting",
                content_template="## Rate Limiting\n\nAPI rate limits:",
                estimated_duration=5.0,
                dependencies=["endpoints"]
            )
        ]
        
        api_template = DocumentationTemplate(
            template_id="api_documentation",
            template_name="API Documentation Template",
            description="Template for API documentation with parallel section generation",
            sections=api_sections,
            required_sections=["header", "introduction", "endpoints"],
            optional_sections=["examples", "errors", "rate_limiting"]
        )
        
        self.register_template(api_template)
        
        # User Guide Template
        guide_sections = [
            TemplateSection(
                section_id="header",
                section_type="header",
                title="User Guide",
                content_template="# {title}\n\nUser guide for {product_name}",
                estimated_duration=2.0
            ),
            TemplateSection(
                section_id="getting_started",
                section_type="getting_started",
                title="Getting Started",
                content_template="## Getting Started\n\nQuick start guide:",
                estimated_duration=10.0,
                dependencies=["header"]
            ),
            TemplateSection(
                section_id="installation",
                section_type="installation",
                title="Installation",
                content_template="## Installation\n\nHow to install:",
                estimated_duration=12.0,
                dependencies=["getting_started"]
            ),
            TemplateSection(
                section_id="configuration",
                section_type="configuration",
                title="Configuration",
                content_template="## Configuration\n\nHow to configure:",
                estimated_duration=8.0,
                dependencies=["installation"]
            ),
            TemplateSection(
                section_id="usage",
                section_type="usage",
                title="Usage",
                content_template="## Usage\n\nHow to use:",
                estimated_duration=15.0,
                dependencies=["configuration"]
            ),
            TemplateSection(
                section_id="troubleshooting",
                section_type="troubleshooting",
                title="Troubleshooting",
                content_template="## Troubleshooting\n\nCommon issues and solutions:",
                estimated_duration=10.0
            ),
            TemplateSection(
                section_id="faq",
                section_type="faq",
                title="FAQ",
                content_template="## Frequently Asked Questions\n\nCommon questions:",
                estimated_duration=8.0
            )
        ]
        
        guide_template = DocumentationTemplate(
            template_id="user_guide",
            template_name="User Guide Template",
            description="Template for user guides with parallel section generation",
            sections=guide_sections,
            required_sections=["header", "getting_started", "usage"],
            optional_sections=["troubleshooting", "faq"]
        )
        
        self.register_template(guide_template)


class TemplateDashboard:
    def __init__(self, template_manager: DocumentationTemplateManager):
        self.template_manager = template_manager
        
    def display_available_templates(self):
        """Display all available templates."""
        templates = self.template_manager.list_templates()
        
        print(f"\nAvailable Documentation Templates ({len(templates)})")
        print("=" * 50)
        
        for template in templates:
            complexity = self.template_manager.get_template_complexity(template.template_id)
            print(f"\n{template.template_name}")
            print(f"  ID: {template.template_id}")
            print(f"  Description: {template.description}")
            print(f"  Sections: {len(template.sections)}")
            print(f"  Complexity Score: {complexity.get('complexity_score', 0)}")
            
    def display_template_details(self, template_id: str):
        """Display detailed information about a template."""
        template = self.template_manager.get_template(template_id)
        if not template:
            print(f"Template '{template_id}' not found")
            return
            
        complexity = self.template_manager.get_template_complexity(template_id)
        
        print(f"\nTemplate Details - {template.template_name}")
        print("=" * 40)
        print(f"ID: {template.template_id}")
        print(f"Description: {template.description}")
        print(f"Total Sections: {len(template.sections)}")
        print(f"Required Sections: {', '.join(template.required_sections)}")
        print(f"Optional Sections: {', '.join(template.optional_sections)}")
        print(f"Complexity Score: {complexity.get('complexity_score', 0)}")
        print(f"Max Dependency Depth: {complexity.get('max_dependency_depth', 0)}")
        
        print(f"\nSections:")
        for i, section in enumerate(template.sections, 1):
            print(f"  {i}. {section.title} ({section.section_type})")
            print(f"     ID: {section.section_id}")
            print(f"     Estimated Duration: {section.estimated_duration} minutes")
            if section.dependencies:
                print(f"     Dependencies: {', '.join(section.dependencies)}")
                
    def display_document_progress(self, document_id: str):
        """Display progress for a generated document."""
        progress = self.template_manager.get_document_progress(document_id)
        document = self.template_manager.get_document(document_id)
        
        if not progress or not document:
            print(f"Document '{document_id}' not found")
            return
            
        print(f"\nDocument Progress - {document.title}")
        print("=" * 35)
        print(f"Status: {document.status}")
        print(f"Total Sections: {progress['total_sections']}")
        print(f"Completed: {progress['completed_sections']}")
        print(f"In Progress: {progress['in_progress_sections']}")
        print(f"Pending: {progress['pending_sections']}")
        print(f"Progress: {progress['progress_percentage']:.1f}%")
        
        # Show generation plan
        plan = self.template_manager.get_parallel_generation_plan(document_id)
        print(f"\nParallel Generation Plan:")
        for i, wave in enumerate(plan, 1):
            print(f"  Wave {i}: {', '.join(wave)}")
            
    def display_section_estimates(self, template_id: str):
        """Display estimated durations for template sections."""
        template = self.template_manager.get_template(template_id)
        if not template:
            print(f"Template '{template_id}' not found")
            return
            
        print(f"\nSection Duration Estimates - {template.template_name}")
        print("=" * 45)
        
        total_time = 0.0
        for section in template.sections:
            print(f"{section.title}: {section.estimated_duration:.1f} minutes")
            total_time += section.estimated_duration
            
        print(f"\nTotal Estimated Time: {total_time:.1f} minutes ({total_time/60:.1f} hours)")
        
        # Show parallel time estimate
        plan = self._get_parallel_time_estimate(template_id)
        print(f"Estimated Parallel Time: {plan['parallel_time']:.1f} minutes ({plan['parallel_time']/60:.1f} hours)")
        print(f"Time Saved: {plan['time_saved']:.1f} minutes ({plan['time_saved']/60:.1f} hours)")
        print(f"Speedup: {plan['speedup']:.1f}x")
        
    def _get_parallel_time_estimate(self, template_id: str) -> Dict[str, float]:
        """Get parallel time estimate for a template."""
        template = self.template_manager.get_template(template_id)
        if not template:
            return {'parallel_time': 0, 'time_saved': 0, 'speedup': 1.0}
            
        # Get generation plan
        # For this example, we'll create a dummy document to get the plan
        dummy_doc = self.template_manager.create_document_from_template(
            "dummy", template_id, "Dummy Document"
        )
        
        if not dummy_doc:
            return {'parallel_time': 0, 'time_saved': 0, 'speedup': 1.0}
            
        plan = self.template_manager.get_parallel_generation_plan("dummy")
        
        # Calculate sequential time
        sequential_time = sum(
            self.template_manager.get_section_estimated_duration(template_id, section.section_id)
            for section in template.sections
        )
        
        # Calculate parallel time (sum of max time in each wave)
        parallel_time = 0.0
        for wave in plan:
            wave_max_time = 0.0
            for section_id in wave:
                section_time = self.template_manager.get_section_estimated_duration(template_id, section_id)
                wave_max_time = max(wave_max_time, section_time)
            parallel_time += wave_max_time
            
        time_saved = sequential_time - parallel_time
        speedup = sequential_time / parallel_time if parallel_time > 0 else 1.0
        
        return {
            'sequential_time': sequential_time,
            'parallel_time': parallel_time,
            'time_saved': time_saved,
            'speedup': speedup
        }


def main():
    # Example usage
    print("Parallel Documentation Generation Templates")
    print("=" * 48)
    
    # Create template manager and dashboard
    template_manager = DocumentationTemplateManager()
    dashboard = TemplateDashboard(template_manager)
    
    print("Documentation template system initialized")
    print("System ready to generate documentation in parallel")
    
    # Example of what the workflow would look like:
    print("\nExample workflow:")
    print("  1. Create templates for different documentation types")
    print("  2. Generate documents based on templates")
    print("  3. Assign sections to agents for parallel generation")
    print("  4. Track progress and coordinate parallel workflows")
    print("  5. Combine sections into final documentation")


if __name__ == "__main__":
    main()
