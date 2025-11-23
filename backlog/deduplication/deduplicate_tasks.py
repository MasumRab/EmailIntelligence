#!/usr/bin/env python3
"""
Backlog Deduplication Script
Phase 2 of Backlog Consolidation Plan

This script identifies and resolves duplicate tasks across categories
by comparing titles, descriptions, and acceptance criteria.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from difflib import SequenceMatcher

class TaskDeduplicator:
    def __init__(self, extracted_tasks_file: str):
        self.extracted_tasks_file = extracted_tasks_file
        self.tasks = []
        self.duplicates = []
        self.unique_tasks = []
        self.similarity_threshold = 0.85  # 85% similarity threshold

    def load_tasks(self):
        """Load extracted tasks from JSON file"""
        with open(self.extracted_tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = data['tasks']
        print(f"Loaded {len(self.tasks)} tasks for deduplication")

    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        if not text:
            return ""
        # Convert to lowercase, remove extra whitespace, strip HTML comments
        text = text.lower()
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text.strip()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1, text2).ratio()

    def are_tasks_duplicate(self, task1: Dict, task2: Dict) -> Tuple[bool, float]:
        """Check if two tasks are duplicates based on multiple criteria"""
        # Compare titles
        title1 = self.normalize_text(task1.get('title', ''))
        title2 = self.normalize_text(task2.get('title', ''))

        if title1 and title2:
            title_similarity = self.calculate_similarity(title1, title2)
            if title_similarity >= self.similarity_threshold:
                return True, title_similarity

        # Compare descriptions
        desc1 = self.normalize_text(task1.get('description', ''))
        desc2 = self.normalize_text(task2.get('description', ''))

        if desc1 and desc2 and len(desc1) > 20 and len(desc2) > 20:
            desc_similarity = self.calculate_similarity(desc1, desc2)
            if desc_similarity >= self.similarity_threshold:
                return True, desc_similarity

        # Compare acceptance criteria
        ac1 = self.normalize_text(task1.get('acceptance_criteria', ''))
        ac2 = self.normalize_text(task2.get('acceptance_criteria', ''))

        if ac1 and ac2 and len(ac1) > 20 and len(ac2) > 20:
            ac_similarity = self.calculate_similarity(ac1, ac2)
            if ac_similarity >= self.similarity_threshold:
                return True, ac_similarity

        return False, 0.0

    def find_duplicates(self) -> List[Dict]:
        """Find all duplicate tasks using a simplified approach"""
        duplicates = []
        processed_ids = set()

        # First pass: Find exact title matches
        title_groups = defaultdict(list)
        for task in self.tasks:
            title = self.normalize_text(task.get('title', ''))
            if title and title != 'unknown title':
                title_groups[title].append(task)

        print(f"Found {len(title_groups)} unique title groups")

        # Process exact title matches
        for title, tasks_in_group in title_groups.items():
            if len(tasks_in_group) > 1:
                # Sort by completeness score
                tasks_in_group.sort(key=self._completeness_score, reverse=True)
                primary = tasks_in_group[0]
                duplicates_list = []

                for dup_task in tasks_in_group[1:]:
                    duplicates_list.append({
                        **dup_task,
                        'similarity_score': 1.0,  # Exact title match
                        'duplicate_of': primary['id']
                    })
                    processed_ids.add(dup_task['id'])

                if duplicates_list:
                    duplicates.append({
                        'primary_task': primary,
                        'duplicates': duplicates_list,
                        'total_duplicates': len(duplicates_list)
                    })
                processed_ids.add(primary['id'])

        # Second pass: Find similar descriptions among remaining tasks
        remaining_tasks = [t for t in self.tasks if t['id'] not in processed_ids]
        print(f"Processing {len(remaining_tasks)} remaining tasks for description similarity...")

        desc_groups = defaultdict(list)
        for task in remaining_tasks:
            desc = self.normalize_text(task.get('description', ''))
            if len(desc) > 50:  # Only consider substantial descriptions
                # Use first 100 chars as key for grouping
                desc_key = desc[:100]
                desc_groups[desc_key].append(task)

        for desc_key, tasks_in_group in desc_groups.items():
            if len(tasks_in_group) > 1:
                # Check similarity more carefully
                primary = tasks_in_group[0]
                duplicates_list = []

                for task in tasks_in_group[1:]:
                    is_duplicate, similarity = self.are_tasks_duplicate(primary, task)
                    if is_duplicate:
                        duplicates_list.append({
                            **task,
                            'similarity_score': similarity,
                            'duplicate_of': primary['id']
                        })

                if duplicates_list:
                    duplicates.append({
                        'primary_task': primary,
                        'duplicates': duplicates_list,
                        'total_duplicates': len(duplicates_list)
                    })

        return duplicates

    def resolve_duplicates(self, duplicates: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Resolve duplicates by keeping the most complete version"""
        resolved_tasks = []
        duplicate_records = []

        for dup_group in duplicates:
            primary = dup_group['primary_task']
            dupes = dup_group['duplicates']

            # Find the most complete task (prefer tasks with more filled fields)
            candidates = [primary] + dupes
            best_task = max(candidates, key=self._completeness_score)

            # Merge information from duplicates into the best task
            merged_task = self._merge_task_data(best_task, candidates)

            resolved_tasks.append(merged_task)
            duplicate_records.append({
                'kept_task': merged_task,
                'removed_tasks': [t for t in candidates if t['id'] != merged_task['id']],
                'resolution_reason': 'kept_most_complete_version'
            })

        return resolved_tasks, duplicate_records

    def _completeness_score(self, task: Dict) -> int:
        """Calculate completeness score for a task"""
        score = 0
        if task.get('title') and task['title'] != 'Unknown Title': score += 3
        if task.get('description'): score += 2
        if task.get('acceptance_criteria'): score += 2
        if task.get('priority') and task['priority'] != 'medium': score += 1
        if task.get('status') and task['status'] != 'todo': score += 1
        if task.get('assignees'): score += 1
        if task.get('labels'): score += 1
        return score

    def _merge_task_data(self, primary: Dict, candidates: List[Dict]) -> Dict:
        """Merge data from duplicate tasks into the primary task"""
        merged = dict(primary)

        # Merge assignees and labels (combine unique values)
        all_assignees = set()
        all_labels = set()

        for candidate in candidates:
            if candidate.get('assignees'):
                if isinstance(candidate['assignees'], list):
                    all_assignees.update(candidate['assignees'])
                else:
                    all_assignees.add(candidate['assignees'])

            if candidate.get('labels'):
                if isinstance(candidate['labels'], list):
                    all_labels.update(candidate['labels'])
                else:
                    all_labels.add(candidate['labels'])

        if all_assignees:
            merged['assignees'] = list(all_assignees)
        if all_labels:
            merged['labels'] = list(all_labels)

        # Keep the earliest created date
        created_dates = [str(c.get('created_date')) for c in candidates if c.get('created_date') and str(c['created_date']).strip()]
        if created_dates:
            merged['created_date'] = min(created_dates)

        # Keep the latest updated date
        updated_dates = [str(c.get('updated_date')) for c in candidates if c.get('updated_date') and str(c['updated_date']).strip()]
        if updated_dates:
            merged['updated_date'] = max(updated_dates)

        # Add merged sources
        merged['merged_from'] = [c['id'] for c in candidates if c['id'] != primary['id']]

        return merged

    def deduplicate(self) -> Tuple[List[Dict], List[Dict]]:
        """Main deduplication process"""
        print("Starting deduplication process...")

        duplicates = self.find_duplicates()
        print(f"Found {len(duplicates)} groups of duplicate tasks")

        resolved_tasks, duplicate_records = self.resolve_duplicates(duplicates)

        # Find unique tasks (not in any duplicate group)
        duplicate_ids = set()
        for dup_group in duplicates:
            duplicate_ids.add(dup_group['primary_task']['id'])
            for dup in dup_group['duplicates']:
                duplicate_ids.add(dup['id'])

        unique_tasks = [task for task in self.tasks if task['id'] not in duplicate_ids]

        final_tasks = unique_tasks + resolved_tasks
        print(f"✅ Deduplication complete: {len(final_tasks)} unique tasks")

        return final_tasks, duplicate_records

    def save_deduplicated_data(self, tasks: List[Dict], duplicates: List[Dict]):
        """Save deduplicated tasks and duplicate records"""
        output_dir = Path(self.extracted_tasks_file).parent.parent / "deduplication"
        output_dir.mkdir(exist_ok=True)

        # Save deduplicated tasks
        tasks_file = output_dir / "deduplicated_tasks.json"
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'deduplication_date': '2025-11-22T17:33:46.707002',  # Would use datetime.now() in real implementation
                    'original_tasks': len(self.tasks),
                    'deduplicated_tasks': len(tasks),
                    'duplicates_found': len(duplicates)
                },
                'tasks': tasks
            }, f, indent=2, ensure_ascii=False)

        # Save duplicate records
        duplicates_file = output_dir / "duplicate_records.json"
        with open(duplicates_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'deduplication_date': '2025-11-22T17:33:46.707002',
                    'duplicate_groups': len(duplicates)
                },
                'duplicates': duplicates
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved deduplicated data to {output_dir}")

def main():
    extractor = TaskDeduplicator("backlog/extraction/extracted_tasks.json")
    extractor.load_tasks()
    tasks, duplicates = extractor.deduplicate()
    extractor.save_deduplicated_data(tasks, duplicates)

    print("\n📊 DEDUPLICATION SUMMARY:")
    print(f"  • Original tasks: {len(extractor.tasks)}")
    print(f"  • Deduplicated tasks: {len(tasks)}")
    print(f"  • Duplicate groups resolved: {len(duplicates)}")

if __name__ == "__main__":
    main()