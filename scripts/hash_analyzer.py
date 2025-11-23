#!/usr/bin/env python3
"""
Hash Analyzer - Canonical Implementation
Generates and compares content hashes for duplicate detection
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import difflib

logger = logging.getLogger(__name__)

class HashAnalyzer:
    """Canonical hash-based duplicate detection"""

    def __init__(self):
        self.content_hashes: Dict[str, str] = {}
        self.file_hashes: Dict[str, List[str]] = defaultdict(list)
        self.exact_duplicates: Dict[str, List[str]] = {}
        self.similar_content: List[Tuple[str, str, float]] = []

    def generate_content_hash(self, content: str, algorithm: str = 'sha256') -> str:
        """Generate hash of normalized content"""
        if algorithm == 'md5':
            return hashlib.md5(content.encode('utf-8')).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(content.encode('utf-8')).hexdigest()
        else:  # sha256 default
            return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def load_extracted_data(self, data_file: str) -> Dict[str, Dict]:
        """Load extracted task data from JSON file"""
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def process_extracted_data(self, extracted_data: Dict[str, Dict]):
        """Process extracted data and generate hashes"""
        for file_path, data in extracted_data.items():
            if 'normalized_content' in data:
                content = data['normalized_content']
                content_hash = self.generate_content_hash(content)

                self.content_hashes[file_path] = content_hash
                self.file_hashes[content_hash].append(file_path)

    def find_exact_duplicates(self) -> Dict[str, List[str]]:
        """Find files with identical content hashes"""
        exact_duplicates = {}

        for content_hash, file_paths in self.file_hashes.items():
            if len(file_paths) > 1:
                exact_duplicates[content_hash] = sorted(file_paths)

        self.exact_duplicates = exact_duplicates
        return exact_duplicates

    def calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity ratio between two content strings"""
        return difflib.SequenceMatcher(None, content1, content2).ratio()

    def find_similar_content(self, extracted_data: Dict[str, Dict], threshold: float = 0.85) -> List[Tuple[str, str, float]]:
        """Find content with high similarity (but not exact duplicates)"""
        similar_pairs = []
        processed_files = set()

        file_paths = list(extracted_data.keys())

        for i, file1 in enumerate(file_paths):
            if file1 in processed_files:
                continue

            content1 = extracted_data[file1].get('normalized_content', '')

            for j, file2 in enumerate(file_paths[i+1:], i+1):
                if file2 in processed_files:
                    continue

                content2 = extracted_data[file2].get('normalized_content', '')

                # Skip if same hash (already caught by exact duplicates)
                if (self.content_hashes.get(file1) == self.content_hashes.get(file2)):
                    continue

                similarity = self.calculate_similarity(content1, content2)

                if similarity >= threshold:
                    similar_pairs.append((file1, file2, similarity))
                    processed_files.add(file2)

        self.similar_content = sorted(similar_pairs, key=lambda x: x[2], reverse=True)
        return self.similar_content

    def analyze_repository_distribution(self, duplicate_groups: Dict[str, List[str]]) -> Dict[Tuple[str, str], int]:
        """Analyze which repositories have the most cross-duplication"""
        cross_repo_duplicates = defaultdict(int)

        for files in duplicate_groups.values():
            if len(files) < 2:
                continue

            repositories = set()

            for file_path in files:
                # Extract repository from path
                path_parts = Path(file_path).parts

                if 'worktrees' in path_parts:
                    worktree_idx = path_parts.index('worktrees')
                    if worktree_idx + 1 < len(path_parts):
                        repo = path_parts[worktree_idx + 1]
                    else:
                        repo = 'worktrees'
                else:
                    # Main repositories
                    repo = path_parts[1] if len(path_parts) > 1 else 'root'

                repositories.add(repo)

            # Count cross-repository duplicates
            if len(repositories) > 1:
                repo_list = sorted(repositories)
                for i in range(len(repo_list)):
                    for j in range(i + 1, len(repo_list)):
                        cross_repo_duplicates[(repo_list[i], repo_list[j])] += 1

        return dict(cross_repo_duplicates)

    def generate_comprehensive_report(self, extracted_data: Dict[str, Dict]) -> Dict:
        """Generate comprehensive analysis report"""
        exact_dups = self.find_exact_duplicates()
        similar_content = self.find_similar_content(extracted_data)

        total_files = len(extracted_data)
        exact_duplicate_files = sum(len(files) for files in exact_dups.values())
        unique_files = total_files - exact_duplicate_files

        return {
            'summary': {
                'total_task_files': total_files,
                'exact_duplicate_files': exact_duplicate_files,
                'unique_files': unique_files,
                'exact_duplicate_clusters': len(exact_dups),
                'similar_content_pairs': len(similar_content),
                'overall_duplication_rate': f"{(exact_duplicate_files/total_files)*100:.1f}%" if total_files > 0 else "0%"
            },
            'exact_duplicates': exact_dups,
            'similar_content': similar_content[:50],  # Top 50 most similar
            'repository_cross_duplicates': self.analyze_repository_distribution(exact_dups),
            'cluster_size_distribution': self.analyze_cluster_sizes(exact_dups)
        }

    def analyze_cluster_sizes(self, duplicate_groups: Dict[str, List[str]]) -> Dict[int, int]:
        """Analyze distribution of duplicate cluster sizes"""
        sizes = defaultdict(int)
        for files in duplicate_groups.values():
            sizes[len(files)] += 1
        return dict(sizes)

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze task content hashes for duplication')
    parser.add_argument('--input-data', required=True, help='JSON file with extracted task data')
    parser.add_argument('--output-report', required=True, help='Output report JSON file')
    parser.add_argument('--similarity-threshold', type=float, default=0.85, help='Similarity threshold for near-duplicates')

    args = parser.parse_args()

    analyzer = HashAnalyzer()

    # Load extracted data
    extracted_data = analyzer.load_extracted_data(args.input_data)

    # Process and analyze
    analyzer.process_extracted_data(extracted_data)

    # Generate comprehensive report
    report = analyzer.generate_comprehensive_report(extracted_data)

    # Save report
    with open(args.output_report, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Print summary
    summary = report['summary']
    print("📊 DUPLICATION ANALYSIS COMPLETE")
    print(f"Total task files: {summary['total_task_files']}")
    print(f"Exact duplicate files: {summary['exact_duplicate_files']}")
    print(f"Unique files: {summary['unique_files']}")
    print(f"Duplication rate: {summary['overall_duplication_rate']}")
    print(f"Duplicate clusters: {summary['exact_duplicate_clusters']}")
    print(f"Similar content pairs: {summary['similar_content_pairs']}")

if __name__ == "__main__":
    main()