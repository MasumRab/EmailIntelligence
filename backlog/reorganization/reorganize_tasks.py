#!/usr/bin/env python3
"""
Backlog Functional Reorganization Script
Phase 3 of Backlog Consolidation Plan

This script reorganizes deduplicated tasks into 6 functional categories:
1. Development & Code Quality
2. Architecture & Infrastructure
3. Security & Compliance
4. User Experience
5. AI & Machine Learning
6. Integration & Workflows
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

class TaskReorganizer:
    def __init__(self, deduplicated_tasks_file: str):
        self.deduplicated_tasks_file = deduplicated_tasks_file
        self.tasks = []
        self.categories = {
            'development_code_quality': {
                'name': 'Development & Code Quality',
                'description': 'Code development, testing, refactoring, and quality assurance',
                'keywords': [
                    'test', 'testing', 'code', 'refactor', 'quality', 'lint', 'format',
                    'typescript', 'python', 'javascript', 'backend', 'frontend',
                    'component', 'function', 'class', 'module', 'package',
                    'dependency', 'import', 'export', 'build', 'compile',
                    'debug', 'fix', 'bug', 'error', 'exception'
                ],
                'tasks': []
            },
            'architecture_infrastructure': {
                'name': 'Architecture & Infrastructure',
                'description': 'System architecture, infrastructure, deployment, and DevOps',
                'keywords': [
                    'architecture', 'infrastructure', 'deployment', 'docker', 'kubernetes',
                    'aws', 'azure', 'gcp', 'cloud', 'server', 'database', 'storage',
                    'api', 'service', 'microservice', 'scalability', 'performance',
                    'monitoring', 'logging', 'ci/cd', 'pipeline', 'automation',
                    'migration', 'upgrade', 'configuration', 'environment'
                ],
                'tasks': []
            },
            'security_compliance': {
                'name': 'Security & Compliance',
                'description': 'Security measures, authentication, authorization, and compliance',
                'keywords': [
                    'security', 'auth', 'authentication', 'authorization', 'login',
                    'password', 'encryption', 'ssl', 'tls', 'certificate', 'token',
                    'oauth', 'jwt', 'session', 'permission', 'role', 'access',
                    'privacy', 'gdpr', 'compliance', 'audit', 'vulnerability',
                    'penetration', 'firewall', 'backup', 'recovery'
                ],
                'tasks': []
            },
            'user_experience': {
                'name': 'User Experience',
                'description': 'UI/UX design, user interface, and user interaction',
                'keywords': [
                    'ui', 'ux', 'user', 'interface', 'design', 'frontend', 'web',
                    'mobile', 'responsive', 'accessibility', 'a11y', 'usability',
                    'navigation', 'layout', 'theme', 'style', 'css', 'html',
                    'component', 'widget', 'form', 'input', 'button', 'modal',
                    'dashboard', 'page', 'view', 'screen', 'interaction'
                ],
                'tasks': []
            },
            'ai_machine_learning': {
                'name': 'AI & Machine Learning',
                'description': 'AI models, machine learning, NLP, and intelligent features',
                'keywords': [
                    'ai', 'artificial intelligence', 'machine learning', 'ml',
                    'neural network', 'nlp', 'natural language', 'llm', 'gpt',
                    'claude', 'openai', 'huggingface', 'transformers', 'embedding',
                    'classification', 'prediction', 'recommendation', 'chatbot',
                    'automation', 'intelligence', 'cognitive', 'learning'
                ],
                'tasks': []
            },
            'integration_workflows': {
                'name': 'Integration & Workflows',
                'description': 'Third-party integrations, workflows, and business logic',
                'keywords': [
                    'integration', 'workflow', 'business logic', 'process',
                    'automation', 'orchestration', 'pipeline', 'webhook',
                    'api integration', 'third-party', 'external', 'sync',
                    'import', 'export', 'data flow', 'etl', 'middleware',
                    'connector', 'plugin', 'extension', 'task management'
                ],
                'tasks': []
            }
        }

    def load_tasks(self):
        """Load deduplicated tasks from JSON file"""
        with open(self.deduplicated_tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = data['tasks']
        print(f"Loaded {len(self.tasks)} deduplicated tasks for reorganization")

    def normalize_text(self, text: str) -> str:
        """Normalize text for keyword matching"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def categorize_task(self, task: Dict) -> str:
        """Categorize a single task based on its content"""
        # Combine title, description, and acceptance criteria for analysis
        content_parts = [
            task.get('title', ''),
            task.get('description', ''),
            task.get('acceptance_criteria', ''),
            task.get('source_file', '')
        ]
        content = ' '.join(content_parts)
        normalized_content = self.normalize_text(content)

        # Check for category-specific keywords
        category_scores = {}

        for category_key, category_info in self.categories.items():
            score = 0
            keywords = category_info['keywords']

            for keyword in keywords:
                if keyword in normalized_content:
                    score += 1

            category_scores[category_key] = score

        # Find the category with the highest score
        best_category = max(category_scores.keys(), key=lambda k: category_scores[k])

        # If no keywords match, check file path patterns
        if category_scores[best_category] == 0:
            source_file = task.get('source_file', '').lower()
            if 'test' in source_file or 'spec' in source_file:
                return 'development_code_quality'
            elif 'security' in source_file or 'auth' in source_file:
                return 'security_compliance'
            elif 'ui' in source_file or 'ux' in source_file or 'frontend' in source_file:
                return 'user_experience'
            elif 'ai' in source_file or 'ml' in source_file:
                return 'ai_machine_learning'
            elif 'integration' in source_file or 'workflow' in source_file:
                return 'integration_workflows'
            elif 'infra' in source_file or 'deploy' in source_file:
                return 'architecture_infrastructure'

        return best_category

    def reorganize_tasks(self) -> Dict[str, Any]:
        """Reorganize all tasks into functional categories"""
        print("Starting task reorganization...")

        # Categorize each task
        for task in self.tasks:
            category = self.categorize_task(task)
            self.categories[category]['tasks'].append(task)

        # Prepare the reorganized structure
        reorganized = {
            'metadata': {
                'reorganization_date': '2025-11-22T17:33:46.707002',
                'total_tasks': len(self.tasks),
                'categories': len(self.categories)
            },
            'categories': {}
        }

        # Add category summaries
        for category_key, category_data in self.categories.items():
            tasks_in_category = category_data['tasks']
            reorganized['categories'][category_key] = {
                'name': category_data['name'],
                'description': category_data['description'],
                'task_count': len(tasks_in_category),
                'tasks': tasks_in_category
            }

        print("✅ Task reorganization complete")
        return reorganized

    def save_reorganized_data(self, reorganized_data: Dict[str, Any]):
        """Save reorganized task data"""
        output_dir = Path(self.deduplicated_tasks_file).parent.parent / "reorganization"
        output_dir.mkdir(exist_ok=True)

        # Save complete reorganized data
        output_file = output_dir / "reorganized_tasks.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reorganized_data, f, indent=2, ensure_ascii=False)

        # Save category summary
        summary_file = output_dir / "category_summary.json"
        summary = {
            'metadata': reorganized_data['metadata'],
            'category_summary': []
        }

        for category_key, category_data in reorganized_data['categories'].items():
            summary['category_summary'].append({
                'key': category_key,
                'name': category_data['name'],
                'description': category_data['description'],
                'task_count': category_data['task_count']
            })

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved reorganized data to {output_dir}")

def main():
    reorganizer = TaskReorganizer("backlog/deduplication/deduplicated_tasks.json")
    reorganizer.load_tasks()
    reorganized_data = reorganizer.reorganize_tasks()
    reorganizer.save_reorganized_data(reorganized_data)

    print("\n📊 REORGANIZATION SUMMARY:")
    total_tasks = reorganized_data['metadata']['total_tasks']
    print(f"  • Total tasks reorganized: {total_tasks}")

    for category_key, category_data in reorganized_data['categories'].items():
        count = category_data['task_count']
        percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
        print(f"  • {category_data['name']}: {count} tasks ({percentage:.1f}%)")

if __name__ == "__main__":
    main()