#!/usr/bin/env python3
"""
Backlog Consolidated System Validation Script
Phase 6 of Backlog Consolidation Plan

This script validates the consolidated backlog system for completeness,
consistency, and usability.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from datetime import datetime

class BacklogValidator:
    def __init__(self, consolidated_dir: str = "backlog/consolidated"):
        self.consolidated_dir = Path(consolidated_dir)
        self.issues = []
        self.warnings = []
        self.stats = {}

    def validate_file_structure(self) -> bool:
        """Validate that all required files exist"""
        required_files = [
            "search_index.json",
            "master_backlog.md",
            "statistics_report.md",
            "statistics.json"
        ]

        required_dirs = [
            "categories"
        ]

        # Check files
        for file in required_files:
            if not (self.consolidated_dir / file).exists():
                self.issues.append(f"Missing required file: {file}")
                return False

        # Check directories
        for dir_name in required_dirs:
            if not (self.consolidated_dir / dir_name).exists():
                self.issues.append(f"Missing required directory: {dir_name}")
                return False

        # Check category files
        categories_dir = self.consolidated_dir / "categories"
        category_files = list(categories_dir.glob("*.md"))
        if len(category_files) < 6:
            self.warnings.append(f"Expected 6 category files, found {len(category_files)}")

        print("✅ File structure validation passed")
        return True

    def validate_search_index(self) -> bool:
        """Validate the search index for completeness and consistency"""
        search_index_file = self.consolidated_dir / "search_index.json"

        try:
            with open(search_index_file, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load search index: {e}")
            return False

        tasks = search_data.get('tasks', [])
        if not tasks:
            self.issues.append("Search index contains no tasks")
            return False

        # Validate required fields
        required_fields = ['id', 'title', 'status', 'priority', 'category', 'searchable_content']
        missing_fields = []

        for task in tasks:
            for field in required_fields:
                if field not in task:
                    missing_fields.append(f"Task {task.get('id', 'unknown')} missing field: {field}")

        if missing_fields:
            self.issues.extend(missing_fields[:10])  # Limit error messages
            if len(missing_fields) > 10:
                self.issues.append(f"... and {len(missing_fields) - 10} more field validation errors")

        # Check for duplicate IDs
        task_ids = [task.get('id') for task in tasks if task.get('id')]
        duplicate_ids = set([x for x in task_ids if task_ids.count(x) > 1])
        if duplicate_ids:
            self.issues.append(f"Duplicate task IDs found: {list(duplicate_ids)[:5]}")

        # Validate categories
        categories = set(task.get('category') for task in tasks if task.get('category'))
        expected_categories = {
            'Development & Code Quality',
            'Architecture & Infrastructure',
            'Security & Compliance',
            'User Experience',
            'AI & Machine Learning',
            'Integration & Workflows'
        }

        missing_categories = expected_categories - categories
        if missing_categories:
            self.warnings.append(f"Missing categories in search index: {missing_categories}")

        self.stats['search_index_tasks'] = len(tasks)
        self.stats['search_index_categories'] = len(categories)

        print(f"✅ Search index validation passed ({len(tasks)} tasks)")
        return len(self.issues) == 0

    def validate_category_files(self) -> bool:
        """Validate category markdown files"""
        categories_dir = self.consolidated_dir / "categories"
        category_files = list(categories_dir.glob("*.md"))

        total_tasks_in_categories = 0

        for file_path in category_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for basic structure
                if not content.startswith('# '):
                    self.warnings.append(f"Category file {file_path.name} doesn't start with header")

                # Count tasks (### headers indicate tasks)
                task_count = len(re.findall(r'^### ', content, re.MULTILINE))
                total_tasks_in_categories += task_count

                # Check for status sections
                status_sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
                if not status_sections:
                    self.warnings.append(f"Category file {file_path.name} has no status sections")

            except Exception as e:
                self.issues.append(f"Failed to validate category file {file_path.name}: {e}")

        self.stats['category_files'] = len(category_files)
        self.stats['tasks_in_category_files'] = total_tasks_in_categories

        print(f"✅ Category files validation passed ({len(category_files)} files, {total_tasks_in_categories} tasks)")
        return len(self.issues) == 0

    def validate_statistics_consistency(self) -> bool:
        """Validate that statistics are consistent across files"""
        # Load statistics from different sources
        stats_file = self.consolidated_dir / "statistics.json"
        search_index_file = self.consolidated_dir / "search_index.json"

        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)

            with open(search_index_file, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load statistics files: {e}")
            return False

        # Compare total task counts
        stats_total = stats_data.get('total_tasks', 0)
        search_total = len(search_data.get('tasks', []))
        category_total = self.stats.get('tasks_in_category_files', 0)

        if stats_total != search_total:
            self.issues.append(f"Task count mismatch: statistics ({stats_total}) vs search index ({search_total})")

        # Allow small differences in category file counting (due to formatting variations)
        if abs(stats_total - category_total) > 1:
            self.issues.append(f"Task count mismatch: statistics ({stats_total}) vs category files ({category_total})")
        elif stats_total != category_total:
            self.warnings.append(f"Minor task count difference: statistics ({stats_total}) vs category files ({category_total})")

        # Validate category distribution
        stats_categories = stats_data.get('categories', {})
        search_tasks = search_data.get('tasks', [])

        for cat_key, cat_stats in stats_categories.items():
            search_cat_count = len([t for t in search_tasks if t.get('category_key') == cat_key])
            if cat_stats.get('count', 0) != search_cat_count:
                self.warnings.append(f"Category {cat_key} count mismatch: stats ({cat_stats.get('count', 0)}) vs search ({search_cat_count})")

        print("✅ Statistics consistency validation passed")
        return len(self.issues) == 0

    def validate_relationships(self) -> bool:
        """Validate task relationships for consistency"""
        # Load relationships if available
        relationships_file = Path("backlog/relationships/task_relationships.json")

        if not relationships_file.exists():
            self.warnings.append("Relationships file not found, skipping relationship validation")
            return True

        try:
            with open(relationships_file, 'r', encoding='utf-8') as f:
                rel_data = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load relationships file: {e}")
            return False

        relationships = rel_data.get('relationships', {})

        # Check for invalid task references
        all_task_ids = set()
        search_index_file = self.consolidated_dir / "search_index.json"

        try:
            with open(search_index_file, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
                all_task_ids = set(task.get('id') for task in search_data.get('tasks', []) if task.get('id'))
        except:
            pass  # Already handled in other validation

        invalid_refs = []

        for rel_type, rel_dict in relationships.items():
            if rel_type == 'part_of':
                for child_id, parent_id in rel_dict.items():
                    if parent_id not in all_task_ids:
                        invalid_refs.append(f"{rel_type}: {child_id} -> {parent_id}")
            else:
                for source_id, target_ids in rel_dict.items():
                    if source_id not in all_task_ids:
                        invalid_refs.append(f"{rel_type}: source {source_id} not found")
                    for target_id in target_ids:
                        if target_id not in all_task_ids:
                            invalid_refs.append(f"{rel_type}: {source_id} -> {target_id}")

        if invalid_refs:
            self.issues.extend(invalid_refs[:10])  # Limit error messages
            if len(invalid_refs) > 10:
                self.issues.append(f"... and {len(invalid_refs) - 10} more invalid relationship references")

        self.stats['relationship_types'] = len(relationships)
        total_relationships = sum(len(rel_dict) if isinstance(rel_dict, dict) else 1 for rel_dict in relationships.values())
        self.stats['total_relationships'] = total_relationships

        print(f"✅ Relationship validation passed ({len(relationships)} types, {total_relationships} relationships)")
        return len(self.issues) == 0

    def validate_search_functionality(self) -> bool:
        """Validate that the search index is properly formatted for searching"""
        search_index_file = self.consolidated_dir / "search_index.json"

        try:
            with open(search_index_file, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
        except Exception as e:
            self.issues.append(f"Failed to load search index for search validation: {e}")
            return False

        tasks = search_data.get('tasks', [])

        # Check that searchable content exists and is reasonable
        empty_searchable = 0
        for task in tasks:
            searchable = task.get('searchable_content', '')
            if not searchable or len(searchable.strip()) < 10:
                empty_searchable += 1

        if empty_searchable > len(tasks) * 0.1:  # More than 10% have poor searchable content
            self.warnings.append(f"{empty_searchable} tasks have insufficient searchable content")

        # Test a few sample searches
        sample_searches = ['test', 'security', 'ui', 'api']
        for search_term in sample_searches:
            matches = [t for t in tasks if search_term.lower() in t.get('searchable_content', '').lower()]
            if not matches:
                self.warnings.append(f"No tasks found for search term: '{search_term}'")

        print("✅ Search functionality validation passed")
        return len(self.issues) == 0

    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate a comprehensive validation report"""
        report = {
            'validation_date': datetime.now().isoformat(),
            'overall_status': 'PASSED' if not self.issues else 'FAILED',
            'issues': self.issues,
            'warnings': self.warnings,
            'statistics': self.stats,
            'recommendations': []
        }

        # Generate recommendations based on issues and warnings
        if self.issues:
            report['recommendations'].append("Fix critical issues before using the consolidated backlog")

        if self.warnings:
            report['recommendations'].append("Review warnings to improve system quality")

        if not self.issues and not self.warnings:
            report['recommendations'].append("Consolidated backlog system is ready for use")

        # Add specific recommendations
        if any('duplicate' in issue.lower() for issue in self.issues):
            report['recommendations'].append("Resolve duplicate task IDs to ensure unique identification")

        if any('missing' in issue.lower() for issue in self.issues):
            report['recommendations'].append("Ensure all required files are present in the consolidated directory")

        if any('relationship' in issue.lower() for issue in self.issues):
            report['recommendations'].append("Fix invalid task references in relationships")

        return report

    def save_validation_report(self, report: Dict[str, Any]):
        """Save the validation report"""
        output_dir = Path("backlog/validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save JSON report
        with open(output_dir / "validation_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Save markdown report
        md_content = "# Backlog Consolidation Validation Report\n\n"
        md_content += f"**Validation Date:** {report['validation_date']}\n"
        md_content += f"**Overall Status:** {report['overall_status']}\n\n"

        if report['issues']:
            md_content += "## Issues (Must Fix)\n\n"
            for issue in report['issues']:
                md_content += f"- {issue}\n"
            md_content += "\n"

        if report['warnings']:
            md_content += "## Warnings (Should Review)\n\n"
            for warning in report['warnings']:
                md_content += f"- {warning}\n"
            md_content += "\n"

        if report['statistics']:
            md_content += "## Statistics\n\n"
            for key, value in report['statistics'].items():
                md_content += f"- **{key.replace('_', ' ').title()}:** {value}\n"
            md_content += "\n"

        if report['recommendations']:
            md_content += "## Recommendations\n\n"
            for rec in report['recommendations']:
                md_content += f"- {rec}\n"
            md_content += "\n"

        with open(output_dir / "validation_report.md", 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ Validation report saved to {output_dir}")

    def run_full_validation(self) -> bool:
        """Run all validation checks"""
        print("Running consolidated backlog system validation...")

        validations = [
            self.validate_file_structure,
            self.validate_search_index,
            self.validate_category_files,
            self.validate_statistics_consistency,
            self.validate_relationships,
            self.validate_search_functionality
        ]

        all_passed = True
        for validation in validations:
            try:
                if not validation():
                    all_passed = False
            except Exception as e:
                self.issues.append(f"Validation {validation.__name__} failed with error: {e}")
                all_passed = False

        # Generate and save report
        report = self.generate_validation_report()
        self.save_validation_report(report)

        status = "PASSED" if all_passed else "FAILED"
        print(f"\n📊 VALIDATION {status}")
        print(f"  • Issues found: {len(self.issues)}")
        print(f"  • Warnings: {len(self.warnings)}")

        return all_passed

def main():
    validator = BacklogValidator()
    success = validator.run_full_validation()

    if success:
        print("\n🎉 Backlog consolidation validation PASSED!")
        print("The consolidated backlog system is ready for use.")
    else:
        print("\n⚠️  Backlog consolidation validation FAILED!")
        print("Please review the validation report and fix the issues.")

if __name__ == "__main__":
    main()