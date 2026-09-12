#!/usr/bin/env python3
"""
Backlog Relationship Building Script
Phase 4 of Backlog Consolidation Plan

This script analyzes task content to identify and build relationships between tasks,
including dependencies, prerequisites, and logical connections.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

class RelationshipBuilder:
    def __init__(self, reorganized_tasks_file: str):
        self.reorganized_tasks_file = reorganized_tasks_file
        self.tasks = []
        self.task_index = {}  # id -> task mapping
        self.relationships = {
            'depends_on': defaultdict(list),  # task_id -> [prerequisite_task_ids]
            'blocks': defaultdict(list),      # task_id -> [blocked_task_ids]
            'related_to': defaultdict(list),  # task_id -> [related_task_ids]
            'parent_of': defaultdict(list),   # task_id -> [subtask_ids]
            'part_of': {}                     # task_id -> parent_task_id
        }

    def load_tasks(self):
        """Load reorganized tasks from JSON file"""
        with open(self.reorganized_tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = []
            for category_data in data['categories'].values():
                self.tasks.extend(category_data['tasks'])

        # Build task index
        for task in self.tasks:
            self.task_index[task['id']] = task

        print(f"Loaded {len(self.tasks)} tasks for relationship analysis")

    def normalize_text(self, text: str) -> str:
        """Normalize text for analysis"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_explicit_dependencies(self, task: Dict) -> List[str]:
        """Extract explicitly mentioned dependencies from task content"""
        dependencies = []

        # Check acceptance criteria for task references
        ac_text = self.normalize_text(task.get('acceptance_criteria', ''))
        task_refs = re.findall(r'task[-\s](\d+)', ac_text)
        dependencies.extend([f"task-{ref}" for ref in task_refs])

        # Check description for task references
        desc_text = self.normalize_text(task.get('description', ''))
        task_refs = re.findall(r'task[-\s](\d+)', desc_text)
        dependencies.extend([f"task-{ref}" for ref in task_refs])

        # Check for subtask patterns (task-X.Y format)
        subtask_refs = re.findall(r'task[-\s](\d+)\.(\d+)', ac_text + ' ' + desc_text)
        dependencies.extend([f"task-{ref[0]}" for ref in subtask_refs])

        return list(set(dependencies))  # Remove duplicates

    def find_content_based_relationships(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Find relationships based on content similarity and keywords"""
        relationships = defaultdict(list)

        # Keywords that indicate dependencies
        dependency_keywords = [
            'after', 'before', 'once', 'when', 'following', 'subsequent',
            'prerequisite', 'requires', 'depends on', 'must complete',
            'foundation', 'base', 'core', 'essential'
        ]

        # Keywords that indicate blocking relationships
        blocking_keywords = [
            'blocks', 'prevents', 'stops', 'cannot proceed', 'waiting for',
            'blocked by', 'depends on', 'requires completion'
        ]

        # Keywords that indicate related work
        related_keywords = [
            'related to', 'similar to', 'also', 'additionally', 'furthermore',
            'in addition', 'complements', 'enhances', 'extends'
        ]

        for task in self.tasks:
            task_id = task['id']
            content = self.normalize_text(
                task.get('title', '') + ' ' +
                task.get('description', '') + ' ' +
                task.get('acceptance_criteria', '')
            )

            # Check for dependency indicators
            for keyword in dependency_keywords:
                if keyword in content:
                    # Look for task references in the same sentence/context
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            task_refs = re.findall(r'task[-\s](\d+)', sentence)
                            for ref in task_refs:
                                dep_id = f"task-{ref}"
                                if dep_id in self.task_index and dep_id != task_id:
                                    relationships['depends_on'].append((task_id, dep_id, f"content_keyword: {keyword}"))

            # Check for blocking indicators
            for keyword in blocking_keywords:
                if keyword in content:
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            task_refs = re.findall(r'task[-\s](\d+)', sentence)
                            for ref in task_refs:
                                block_id = f"task-{ref}"
                                if block_id in self.task_index and block_id != task_id:
                                    relationships['blocks'].append((task_id, block_id, f"content_keyword: {keyword}"))

            # Check for related work indicators
            for keyword in related_keywords:
                if keyword in content:
                    sentences = content.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            task_refs = re.findall(r'task[-\s](\d+)', sentence)
                            for ref in task_refs:
                                rel_id = f"task-{ref}"
                                if rel_id in self.task_index and rel_id != task_id:
                                    relationships['related_to'].append((task_id, rel_id, f"content_keyword: {keyword}"))

        return relationships

    def identify_parent_child_relationships(self) -> List[Tuple[str, str]]:
        """Identify parent-child relationships based on task naming patterns"""
        parent_child_pairs = []

        # Look for patterns like "task-1" and "task-1.1", "task-1.2", etc.
        task_ids = list(self.task_index.keys())

        for task_id in task_ids:
            # Check if this is a parent task (no dot in ID)
            if '.' not in task_id and task_id.startswith('task-'):
                base_id = task_id
                # Find all subtasks
                subtasks = [tid for tid in task_ids if tid.startswith(base_id + '.')]

                for subtask in subtasks:
                    parent_child_pairs.append((base_id, subtask))

        return parent_child_pairs

    def identify_category_based_relationships(self) -> List[Tuple[str, str, str]]:
        """Identify relationships based on category dependencies"""
        category_dependencies = {
            'development_code_quality': [],  # Foundation layer
            'architecture_infrastructure': ['development_code_quality'],  # Depends on code
            'security_compliance': ['development_code_quality', 'architecture_infrastructure'],  # Depends on both
            'user_experience': ['development_code_quality'],  # Depends on code
            'ai_machine_learning': ['development_code_quality', 'architecture_infrastructure'],  # Depends on code and infra
            'integration_workflows': ['development_code_quality', 'architecture_infrastructure', 'ai_machine_learning']  # Depends on all
        }

        relationships = []

        # Group tasks by category
        tasks_by_category = defaultdict(list)
        for task in self.tasks:
            # Determine category from source file or content analysis
            category = self.determine_category_from_task(task)
            tasks_by_category[category].append(task)

        # Create relationships based on category dependencies
        for category, deps in category_dependencies.items():
            category_tasks = tasks_by_category.get(category, [])

            for dep_category in deps:
                dep_tasks = tasks_by_category.get(dep_category, [])

                # Create relationships between tasks in dependent categories
                for task in category_tasks:
                    # Link to a few key tasks in dependency categories
                    for dep_task in dep_tasks[:3]:  # Limit to avoid too many relationships
                        relationships.append((
                            task['id'],
                            dep_task['id'],
                            f"category_dependency: {category} depends on {dep_category}"
                        ))

        return relationships

    def determine_category_from_task(self, task: Dict) -> str:
        """Determine category from task content (simplified version)"""
        content = self.normalize_text(
            task.get('title', '') + ' ' + task.get('description', '') + ' ' +
            task.get('source_file', '')
        )

        categories = {
            'development_code_quality': ['test', 'code', 'refactor', 'backend', 'frontend'],
            'architecture_infrastructure': ['architecture', 'infrastructure', 'deployment', 'docker', 'api'],
            'security_compliance': ['security', 'auth', 'encryption', 'compliance'],
            'user_experience': ['ui', 'ux', 'interface', 'design', 'frontend'],
            'ai_machine_learning': ['ai', 'machine learning', 'nlp', 'llm'],
            'integration_workflows': ['integration', 'workflow', 'business logic']
        }

        for category, keywords in categories.items():
            if any(keyword in content for keyword in keywords):
                return category

        return 'development_code_quality'  # Default

    def build_relationships(self) -> Dict[str, Any]:
        """Build all types of relationships between tasks"""
        print("Building task relationships...")

        # 1. Extract explicit dependencies
        print("  • Extracting explicit dependencies...")
        for task in self.tasks:
            deps = self.extract_explicit_dependencies(task)
            if deps:
                self.relationships['depends_on'][task['id']].extend(deps)

        # 2. Find content-based relationships
        print("  • Analyzing content for relationship indicators...")
        content_relationships = self.find_content_based_relationships()
        for rel_type, relations in content_relationships.items():
            for task_id, related_id, reason in relations:
                if related_id not in self.relationships[rel_type][task_id]:
                    self.relationships[rel_type][task_id].append(related_id)

        # 3. Identify parent-child relationships
        print("  • Identifying parent-child relationships...")
        parent_child_pairs = self.identify_parent_child_relationships()
        for parent_id, child_id in parent_child_pairs:
            if child_id not in self.relationships['parent_of'][parent_id]:
                self.relationships['parent_of'][parent_id].append(child_id)
            self.relationships['part_of'][child_id] = parent_id

        # 4. Add category-based relationships (limited to avoid clutter)
        print("  • Adding category-based relationships...")
        category_relationships = self.identify_category_based_relationships()
        for task_id, related_id, reason in category_relationships[:50]:  # Limit relationships
            if related_id not in self.relationships['depends_on'][task_id]:
                self.relationships['depends_on'][task_id].append(related_id)

        # Convert defaultdicts to regular dicts for JSON serialization
        relationships_data = {
            'metadata': {
                'relationship_building_date': '2025-11-22T17:33:46.707002',
                'total_tasks': len(self.tasks),
                'relationship_types': len(self.relationships)
            },
            'relationships': dict(self.relationships),
            'relationship_summary': self.generate_relationship_summary()
        }

        print("✅ Relationship building complete")
        return relationships_data

    def generate_relationship_summary(self) -> Dict[str, Any]:
        """Generate a summary of relationship statistics"""
        summary = {}

        for rel_type, relations in self.relationships.items():
            if rel_type == 'part_of':
                summary[rel_type] = len(relations)
            else:
                total_relations = sum(len(rel_list) for rel_list in relations.values())
                summary[rel_type] = {
                    'total_relationships': total_relations,
                    'tasks_with_relationships': len(relations)
                }

        return summary

    def save_relationships(self, relationships_data: Dict[str, Any]):
        """Save relationship data"""
        output_dir = Path(self.reorganized_tasks_file).parent.parent / "relationships"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "task_relationships.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(relationships_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved relationship data to {output_dir}")

def main():
    builder = RelationshipBuilder("backlog/reorganization/reorganized_tasks.json")
    builder.load_tasks()
    relationships_data = builder.build_relationships()
    builder.save_relationships(relationships_data)

    print("\n📊 RELATIONSHIP BUILDING SUMMARY:")
    summary = relationships_data['relationship_summary']
    for rel_type, stats in summary.items():
        if isinstance(stats, dict):
            print(f"  • {rel_type}: {stats['total_relationships']} relationships across {stats['tasks_with_relationships']} tasks")
        else:
            print(f"  • {rel_type}: {stats} relationships")

if __name__ == "__main__":
    main()