#!/usr/bin/env python3
"""
Documentation Content Analyzer

Compares documentation content between branches and analyzes differences
in purpose, audience, and technical depth to determine sharing strategies.
"""

import os
import re
import difflib
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json


class DocsContentAnalyzer:
    def __init__(self):
        self.main_branch = "main"
        self.scientific_branch = "scientific"
        self.docs_dir = Path("docs")

    def get_file_content(self, branch: str, file_path: str) -> str:
        """Get file content from a specific branch."""
        try:
            result = subprocess.run(
                ["git", "show", f"{branch}:{file_path}"],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def generate_text_diff(self, content1: str, content2: str) -> str:
        """Generate a unified diff between two content versions."""
        lines1 = content1.splitlines(keepends=True)
        lines2 = content2.splitlines(keepends=True)

        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile="main", tofile="scientific",
            lineterm=""
        )
        return "".join(diff)

    def extract_goals(self, content: str) -> List[str]:
        """Extract goal/purpose statements from documentation."""
        goals = []

        # Look for common goal indicators
        goal_patterns = [
            r'goal[s]?[:\s]+(.+)',
            r'purpose[:\s]+(.+)',
            r'objective[s]?[:\s]+(.+)',
            r'intended\s+to\s+(.+)',
            r'design\s+to\s+(.+)',
            r'aim[s]?[:\s]+(.+)',
        ]

        content_lower = content.lower()
        for pattern in goal_patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            goals.extend(matches)

        # Extract from headings that might indicate purpose
        heading_pattern = r'^#{1,3}\s+(.+)$'
        headings = re.findall(heading_pattern, content, re.MULTILINE)
        goals.extend([h.lower() for h in headings if any(word in h.lower()
                      for word in ['overview', 'introduction', 'purpose', 'goals', 'objectives'])])

        return list(set(goals))  # Remove duplicates

    def extract_audience(self, content: str) -> List[str]:
        """Extract target audience information."""
        audiences = []

        audience_indicators = [
            r'audience[:\s]+(.+)',
            r'intended\s+for[:\s]+(.+)',
            r'target\s+users?[:\s]+(.+)',
            r'for\s+(developers|users|administrators|researchers|scientists)',
        ]

        content_lower = content.lower()
        for pattern in audience_indicators:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            audiences.extend(matches)

        return list(set(audiences))

    def analyze_technical_depth(self, content: str) -> Dict:
        """Analyze the technical depth of documentation."""
        # Count technical indicators
        code_blocks = len(re.findall(r'```', content))
        technical_terms = len(re.findall(r'\b(api|algorithm|implementation|architecture|framework|protocol)\b', content, re.IGNORECASE))
        complexity_indicators = len(re.findall(r'\b(advanced|complex|optimization|scalability|performance)\b', content, re.IGNORECASE))

        # Calculate technical score
        technical_score = (code_blocks * 2 + technical_terms + complexity_indicators * 1.5) / max(len(content.split()), 1) * 1000

        return {
            'code_blocks': code_blocks,
            'technical_terms': technical_terms,
            'complexity_indicators': complexity_indicators,
            'technical_score': technical_score,
            'level': 'high' if technical_score > 5 else 'medium' if technical_score > 2 else 'low'
        }

    def calculate_similarity(self, goals1: List[str], goals2: List[str]) -> float:
        """Calculate similarity between goal sets."""
        if not goals1 and not goals2:
            return 1.0
        if not goals1 or not goals2:
            return 0.0

        # Simple Jaccard similarity
        set1 = set(goals1)
        set2 = set(goals2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def generate_recommendation(self, analysis: Dict) -> str:
        """Generate sharing recommendation based on analysis."""
        goal_similarity = analysis['goal_analysis']['similarity']
        audience_overlap = len(analysis['audience_analysis']['overlap'])
        audience_differences = len(analysis['audience_analysis']['main_unique']) + len(analysis['audience_analysis']['scientific_unique'])

        tech_diff = abs(analysis['technical_analysis']['main']['technical_score'] -
                       analysis['technical_analysis']['scientific']['technical_score'])

        # Decision logic
        if goal_similarity > 0.8 and audience_differences < audience_overlap * 2 and tech_diff < 2:
            return "SHARE"
        elif goal_similarity < 0.3 or audience_differences > audience_overlap * 3 or tech_diff > 5:
            return "BRANCH_SPECIFIC"
        else:
            return "MANUAL_REVIEW"

    def compare_branches(self, doc_path: str) -> Dict:
        """Compare documentation between branches."""
        main_content = self.get_file_content(self.main_branch, doc_path)
        scientific_content = self.get_file_content(self.scientific_branch, doc_path)

        if not main_content and not scientific_content:
            return {'error': 'File not found in either branch'}

        if not main_content:
            return {'recommendation': 'SCIENTIFIC_ONLY'}
        if not scientific_content:
            return {'recommendation': 'MAIN_ONLY'}

        # Extract and analyze components
        main_goals = self.extract_goals(main_content)
        scientific_goals = self.extract_goals(scientific_content)
        main_audience = self.extract_audience(main_content)
        scientific_audience = self.extract_audience(scientific_content)

        analysis = {
            'text_diff': self.generate_text_diff(main_content, scientific_content),
            'goal_analysis': {
                'main_goals': main_goals,
                'scientific_goals': scientific_goals,
                'similarity': self.calculate_similarity(main_goals, scientific_goals),
                'overlap': len(set(main_goals) & set(scientific_goals)),
                'differences': len(set(main_goals) ^ set(scientific_goals))
            },
            'audience_analysis': {
                'main_audience': main_audience,
                'scientific_audience': scientific_audience,
                'overlap': list(set(main_audience) & set(scientific_audience)),
                'main_unique': list(set(main_audience) - set(scientific_audience)),
                'scientific_unique': list(set(scientific_audience) - set(main_audience))
            },
            'technical_analysis': {
                'main': self.analyze_technical_depth(main_content),
                'scientific': self.analyze_technical_depth(scientific_content)
            }
        }

        analysis['recommendation'] = self.generate_recommendation(analysis)

        return analysis

    def save_analysis(self, doc_path: str, analysis: Dict, output_file: Optional[str] = None):
        """Save analysis results to file."""
        if output_file is None:
            output_file = f"docs/analysis_{Path(doc_path).stem}.json"

        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"Analysis saved to {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Documentation Content Analyzer")
    parser.add_argument("doc_path", help="Path to documentation file to analyze")
    parser.add_argument("--output", help="Output file for analysis results")
    parser.add_argument("--save", action="store_true", help="Save analysis to file")

    args = parser.parse_args()

    analyzer = DocsContentAnalyzer()
    analysis = analyzer.compare_branches(args.doc_path)

    if args.save or args.output:
        analyzer.save_analysis(args.doc_path, analysis, args.output)
    else:
        print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()