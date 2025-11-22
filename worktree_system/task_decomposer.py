"""
Micro-Task Decomposition System for Documentation Worktree Migration

This module implements the core task decomposition algorithm that breaks large
documentation tasks into micro-tasks completable in <15 minutes for better
parallel agent utilization.
"""

import re
import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of documentation tasks that can be decomposed."""
    API_DOCS = "api_docs"
    GUIDE = "guide"
    ARCHITECTURE = "architecture"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    OVERVIEW = "overview"


class MicroTaskType(Enum):
    """Types of micro-tasks that documentation can be broken into."""
    SECTION_ANALYSIS = "section_analysis"
    CONTENT_OUTLINE = "content_outline"
    EXAMPLE_WRITING = "example_writing"
    CODE_SNIPPET = "code_snippet"
    DIAGRAM_CREATION = "diagram_creation"
    CROSS_REFERENCE = "cross_reference"
    REVIEW_EDITING = "review_editing"
    FORMATTING = "formatting"
    LINK_VALIDATION = "link_validation"
    SEO_OPTIMIZATION = "seo_optimization"


@dataclass
class MicroTask:
    """Represents a micro-task that can be completed in <15 minutes."""
    id: str
    type: MicroTaskType
    title: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    estimated_time: int = 10  # minutes
    dependencies: Set[str] = field(default_factory=set)
    agent_requirements: Set[str] = field(default_factory=set)
    priority: int = 1
    created_at: float = field(default_factory=time.time)

    def __post_init__(self):
        if self.estimated_time > 15:
            raise ValueError(f"Micro-task estimated time must be <= 15 minutes, got {self.estimated_time}")


@dataclass
class TaskDecompositionResult:
    """Result of decomposing a large task into micro-tasks."""
    original_task: str
    micro_tasks: List[MicroTask]
    execution_paths: List[List[str]]  # Parallel execution paths
    estimated_total_time: int
    parallelization_factor: float


class TaskDecomposer:
    """
    Decomposes large documentation tasks into micro-tasks for parallel execution.

    This class implements algorithms to:
    - Analyze documentation structure
    - Split tasks by section/type
    - Define clear inputs/outputs for each micro-task
    - Identify dependencies and parallel execution paths
    - Match tasks to agent capabilities
    """

    def __init__(self):
        self.section_patterns = {
            TaskType.API_DOCS: [
                r'^#{1,3}\s+(GET|POST|PUT|DELETE|PATCH)\s+',
                r'^#{1,3}\s+API\s+',
                r'^#{1,3}\s+Endpoint\s+',
                r'^#{1,3}\s+Request\s+',
                r'^#{1,3}\s+Response\s+',
            ],
            TaskType.GUIDE: [
                r'^#{1,3}\s+(Step|Guide|Tutorial)\s+',
                r'^#{1,3}\s+Getting\s+Started',
                r'^#{1,3}\s+Installation\s+',
                r'^#{1,3}\s+Configuration\s+',
            ],
            TaskType.ARCHITECTURE: [
                r'^#{1,3}\s+(Architecture|Design|System)\s+',
                r'^#{1,3}\s+Component\s+',
                r'^#{1,3}\s+Data\s+Flow',
                r'^#{1,3}\s+Database\s+',
            ],
            TaskType.TUTORIAL: [
                r'^#{1,3}\s+(Tutorial|Example|Walkthrough)\s+',
                r'^#{1,3}\s+Exercise\s+',
                r'^#{1,3}\s+Practice\s+',
            ],
            TaskType.REFERENCE: [
                r'^#{1,3}\s+(Reference|API|Function|Class)\s+',
                r'^#{1,3}\s+Parameters?\s+',
                r'^#{1,3}\s+Returns?\s+',
            ],
            TaskType.OVERVIEW: [
                r'^#{1,3}\s+(Overview|Introduction|Summary)\s+',
                r'^#{1,3}\s+Features?\s+',
                r'^#{1,3}\s+Benefits?\s+',
            ]
        }

    def decompose_task(self, task_title: str, content: str, task_type: TaskType) -> TaskDecompositionResult:
        """
        Decompose a large documentation task into micro-tasks.

        Args:
            task_title: Title of the original task
            content: Full content of the documentation
            task_type: Type of documentation task

        Returns:
            TaskDecompositionResult with micro-tasks and execution plan
        """
        logger.info(f"Decomposing task: {task_title}")

        # Step 1: Analyze content structure
        sections = self._analyze_content_structure(content, task_type)

        # Step 2: Create micro-tasks for each section
        micro_tasks = []
        task_counter = 0

        for section_title, section_content in sections.items():
            section_tasks = self._create_section_micro_tasks(
                section_title, section_content, task_type, task_counter
            )
            micro_tasks.extend(section_tasks)
            task_counter += len(section_tasks)

        # Step 3: Identify dependencies and parallel execution paths
        execution_paths = self._identify_execution_paths(micro_tasks)

        # Step 4: Calculate performance metrics
        total_time = sum(task.estimated_time for task in micro_tasks)
        parallelization_factor = self._calculate_parallelization_factor(micro_tasks, execution_paths)

        result = TaskDecompositionResult(
            original_task=task_title,
            micro_tasks=micro_tasks,
            execution_paths=execution_paths,
            estimated_total_time=total_time,
            parallelization_factor=parallelization_factor
        )

        logger.info(f"Task decomposed into {len(micro_tasks)} micro-tasks with {parallelization_factor:.1f}x parallelization")
        return result

    def _analyze_content_structure(self, content: str, task_type: TaskType) -> Dict[str, str]:
        """Analyze the content structure and split into sections."""
        sections = {}
        lines = content.split('\n')
        current_section = "Introduction"
        current_content = []

        patterns = self.section_patterns.get(task_type, [])

        for line in lines:
            # Check if this line starts a new section
            is_new_section = False
            for pattern in patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content).strip()

                    # Start new section
                    current_section = line.strip('# \n')
                    current_content = [line]
                    is_new_section = True
                    break

            if not is_new_section:
                current_content.append(line)

        # Save the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _create_section_micro_tasks(self, section_title: str, section_content: str,
                                  task_type: TaskType, task_offset: int) -> List[MicroTask]:
        """Create micro-tasks for a specific section."""
        tasks = []
        base_id = f"task_{task_offset}"

        # Task 1: Section Analysis
        tasks.append(MicroTask(
            id=f"{base_id}_analysis",
            type=MicroTaskType.SECTION_ANALYSIS,
            title=f"Analyze {section_title} section requirements",
            description=f"Review the {section_title} section and identify key points, examples needed, and structure requirements.",
            inputs=[f"{section_title} content"],
            outputs=[f"{section_title} analysis notes"],
            estimated_time=5,
            agent_requirements={"content_analysis"}
        ))

        # Task 2: Content Outline
        tasks.append(MicroTask(
            id=f"{base_id}_outline",
            type=MicroTaskType.CONTENT_OUTLINE,
            title=f"Create detailed outline for {section_title}",
            description=f"Create a detailed outline with subsections, key points, and examples for the {section_title} section.",
            inputs=[f"{section_title} analysis notes"],
            outputs=[f"{section_title} detailed outline"],
            estimated_time=8,
            dependencies={f"{base_id}_analysis"},
            agent_requirements={"content_planning"}
        ))

        # Task 3: Content Writing
        content_tasks = self._create_content_writing_tasks(section_title, section_content, task_type, base_id)
        tasks.extend(content_tasks)

        # Task 4: Review and Editing
        tasks.append(MicroTask(
            id=f"{base_id}_review",
            type=MicroTaskType.REVIEW_EDITING,
            title=f"Review and edit {section_title} content",
            description=f"Review the written content for clarity, accuracy, grammar, and consistency.",
            inputs=[f"{section_title} written content"],
            outputs=[f"{section_title} reviewed content"],
            estimated_time=6,
            dependencies={f"{base_id}_outline"},  # Depends on outline, but can run parallel with writing
            agent_requirements={"editing", "technical_writing"}
        ))

        # Task 5: Formatting and Links
        tasks.append(MicroTask(
            id=f"{base_id}_format",
            type=MicroTaskType.FORMATTING,
            title=f"Format and add links for {section_title}",
            description=f"Apply proper markdown formatting, add cross-references, and validate internal links.",
            inputs=[f"{section_title} reviewed content"],
            outputs=[f"{section_title} formatted content"],
            estimated_time=4,
            dependencies={f"{base_id}_review"},
            agent_requirements={"markdown", "linking"}
        ))

        return tasks

    def _create_content_writing_tasks(self, section_title: str, section_content: str,
                                    task_type: TaskType, base_id: str) -> List[MicroTask]:
        """Create content writing micro-tasks based on section type."""
        tasks = []

        if task_type == TaskType.API_DOCS:
            # API docs need examples and parameter documentation
            tasks.extend([
                MicroTask(
                    id=f"{base_id}_examples",
                    type=MicroTaskType.EXAMPLE_WRITING,
                    title=f"Write API examples for {section_title}",
                    description=f"Create practical code examples and usage scenarios for the {section_title} API.",
                    inputs=[f"{section_title} outline"],
                    outputs=[f"{section_title} code examples"],
                    estimated_time=10,
                    agent_requirements={"coding", "api_design"}
                ),
                MicroTask(
                    id=f"{base_id}_params",
                    type=MicroTaskType.CONTENT_OUTLINE,
                    title=f"Document parameters for {section_title}",
                    description=f"Document all parameters, types, and validation rules for {section_title}.",
                    inputs=[f"{section_title} outline"],
                    outputs=[f"{section_title} parameter documentation"],
                    estimated_time=7,
                    agent_requirements={"technical_writing", "api_design"}
                )
            ])

        elif task_type == TaskType.GUIDE:
            # Guides need step-by-step instructions
            tasks.append(MicroTask(
                id=f"{base_id}_steps",
                type=MicroTaskType.CONTENT_OUTLINE,
                title=f"Write step-by-step instructions for {section_title}",
                description=f"Create clear, numbered steps with explanations for the {section_title} guide.",
                inputs=[f"{section_title} outline"],
                outputs=[f"{section_title} step-by-step content"],
                estimated_time=12,
                agent_requirements={"technical_writing", "instructional_design"}
            ))

        elif task_type == TaskType.ARCHITECTURE:
            # Architecture docs need diagrams and system descriptions
            tasks.extend([
                MicroTask(
                    id=f"{base_id}_diagram",
                    type=MicroTaskType.DIAGRAM_CREATION,
                    title=f"Create architecture diagram for {section_title}",
                    description=f"Design and create visual diagrams showing the {section_title} architecture.",
                    inputs=[f"{section_title} outline"],
                    outputs=[f"{section_title} architecture diagram"],
                    estimated_time=15,
                    agent_requirements={"diagramming", "system_design"}
                ),
                MicroTask(
                    id=f"{base_id}_components",
                    type=MicroTaskType.CONTENT_OUTLINE,
                    title=f"Document system components for {section_title}",
                    description=f"Document all system components, their responsibilities, and interactions.",
                    inputs=[f"{section_title} outline"],
                    outputs=[f"{section_title} component documentation"],
                    estimated_time=10,
                    agent_requirements={"technical_writing", "system_design"}
                )
            ])

        else:
            # Generic content writing task
            tasks.append(MicroTask(
                id=f"{base_id}_content",
                type=MicroTaskType.CONTENT_OUTLINE,
                title=f"Write content for {section_title}",
                description=f"Write comprehensive content for the {section_title} section following the outline.",
                inputs=[f"{section_title} outline"],
                outputs=[f"{section_title} written content"],
                estimated_time=12,
                agent_requirements={"technical_writing"}
            ))

        return tasks

    def _identify_execution_paths(self, micro_tasks: List[MicroTask]) -> List[List[str]]:
        """Identify parallel execution paths for micro-tasks."""
        # Simple dependency-based path identification
        # In a real implementation, this would use topological sorting

        paths = []
        completed_tasks = set()
        remaining_tasks = {task.id: task for task in micro_tasks}

        while remaining_tasks:
            # Find tasks with no unresolved dependencies
            available_tasks = []
            for task_id, task in remaining_tasks.items():
                if task.dependencies.issubset(completed_tasks):
                    available_tasks.append(task_id)

            if not available_tasks:
                # Circular dependency or error
                logger.warning("Circular dependency detected in micro-tasks")
                break

            # Create a new execution path
            paths.append(available_tasks)

            # Mark tasks as completed
            for task_id in available_tasks:
                completed_tasks.add(task_id)
                del remaining_tasks[task_id]

        return paths

    def _calculate_parallelization_factor(self, micro_tasks: List[MicroTask],
                                        execution_paths: List[List[str]]) -> float:
        """Calculate the parallelization factor (speedup potential)."""
        if not micro_tasks:
            return 1.0

        total_time = sum(task.estimated_time for task in micro_tasks)
        max_path_time = max(
            sum(micro_tasks[next(i for i, t in enumerate(micro_tasks) if t.id == task_id)].estimated_time
                for task_id in path)
            for path in execution_paths
        ) if execution_paths else total_time

        return total_time / max_path_time if max_path_time > 0 else 1.0

    def get_agent_requirements_summary(self, micro_tasks: List[MicroTask]) -> Dict[str, int]:
        """Get summary of agent capabilities needed."""
        requirements = {}
        for task in micro_tasks:
            for req in task.agent_requirements:
                requirements[req] = requirements.get(req, 0) + 1
        return requirements