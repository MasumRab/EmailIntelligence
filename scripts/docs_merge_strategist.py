#!/usr/bin/env python3
"""
Documentation Merge Strategist

Determines whether documentation should be shared between branches or kept separate
based on content analysis and executes the appropriate merge strategy.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class DocsMergeStrategist:
    def __init__(self):
        self.main_branch = "main"
        self.scientific_branch = "scientific"
        self.review_queue_file = Path("docs/.review-queue.json")
        self.merge_history_file = Path("docs/.merge-history.json")

    def load_review_queue(self) -> Dict:
        """Load the current review queue."""
        if self.review_queue_file.exists():
            with open(self.review_queue_file, 'r') as f:
                return json.load(f)
        return {"pending_reviews": [], "completed_reviews": []}

    def save_review_queue(self, queue: Dict):
        """Save the review queue."""
        self.review_queue_file.parent.mkdir(exist_ok=True)
        with open(self.review_queue_file, 'w') as f:
            json.dump(queue, f, indent=2)

    def load_merge_history(self) -> List[Dict]:
        """Load merge history."""
        if self.merge_history_file.exists():
            with open(self.merge_history_file, 'r') as f:
                return json.load(f)
        return []

    def save_merge_history(self, history: List[Dict]):
        """Save merge history."""
        self.merge_history_file.parent.mkdir(exist_ok=True)
        with open(self.merge_history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def determine_strategy(self, analysis: Dict) -> str:
        """Determine merge strategy based on analysis."""
        if 'error' in analysis:
            return "ERROR"

        if analysis.get('recommendation') in ['SCIENTIFIC_ONLY', 'MAIN_ONLY']:
            return "BRANCH_SPECIFIC"

        goal_similarity = analysis['goal_analysis']['similarity']
        audience_overlap = len(analysis['audience_analysis']['overlap'])
        audience_differences = (len(analysis['audience_analysis']['main_unique']) +
                               len(analysis['audience_analysis']['scientific_unique']))

        tech_main = analysis['technical_analysis']['main']['technical_score']
        tech_scientific = analysis['technical_analysis']['scientific']['technical_score']
        tech_diff = abs(tech_main - tech_scientific)

        # Decision matrix
        if goal_similarity > 0.8 and audience_differences <= audience_overlap and tech_diff < 2:
            return "SHARE"
        elif goal_similarity < 0.3 or audience_differences > audience_overlap * 2 or tech_diff > 5:
            return "BRANCH_SPECIFIC"
        else:
            return "MANUAL_REVIEW"

    def create_review_request(self, doc_path: str, analysis: Dict, branch: str):
        """Create a review request for manual decision."""
        queue = self.load_review_queue()

        review_request = {
            "id": f"{Path(doc_path).stem}_{int(datetime.now().timestamp())}",
            "doc_path": doc_path,
            "branch": branch,
            "change_type": "content_update",
            "analysis": analysis,
            "strategy": analysis.get('recommendation', 'UNKNOWN'),
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "reviewers": ["team-lead", "tech-writer"],
            "priority": "medium"
        }

        queue["pending_reviews"].append(review_request)
        self.save_review_queue(queue)

        print(f"Created review request for {doc_path}")
        print(f"Strategy recommended: {review_request['strategy']}")

        # Create a simple markdown file for the review
        self.create_review_markdown(review_request)

    def create_review_markdown(self, review_request: Dict):
        """Create a markdown file for manual review."""
        doc_path = review_request['doc_path']
        review_id = review_request['id']

        review_file = Path(f"docs/reviews/review_{review_id}.md")

        analysis = review_request['analysis']

        content = f"""# Documentation Review: {Path(doc_path).name}

**Review ID**: {review_id}
**Document**: {doc_path}
**Branch**: {review_request['branch']}
**Created**: {review_request['created_at']}
**Status**: {review_request['status']}

## Analysis Summary

### Goal Similarity: {analysis['goal_analysis']['similarity']:.2f}
- **Main Goals**: {len(analysis['goal_analysis']['main_goals'])}
- **Scientific Goals**: {len(analysis['goal_analysis']['scientific_goals'])}
- **Overlapping Goals**: {analysis['goal_analysis']['overlap']}
- **Different Goals**: {analysis['goal_analysis']['differences']}

### Audience Analysis
- **Overlap**: {', '.join(analysis['audience_analysis']['overlap']) or 'None'}
- **Main Only**: {', '.join(analysis['audience_analysis']['main_unique']) or 'None'}
- **Scientific Only**: {', '.join(analysis['audience_analysis']['scientific_unique']) or 'None'}

### Technical Depth
- **Main**: {analysis['technical_analysis']['main']['level']} ({analysis['technical_analysis']['main']['technical_score']:.2f})
- **Scientific**: {analysis['technical_analysis']['scientific']['level']} ({analysis['technical_analysis']['scientific']['technical_score']:.2f})

## Recommended Strategy: {review_request['strategy']}

## Review Decision

**Decision**: [ ] SHARE  [ ] BRANCH_SPECIFIC  [ ] MANUAL_REVIEW
**Reasoning**:
"""

        review_file.parent.mkdir(exist_ok=True)
        with open(review_file, 'w') as f:
            f.write(content)

        print(f"Review file created: {review_file}")

    def execute_share_strategy(self, doc_path: str):
        """Execute SHARE strategy - merge documentation to both branches."""
        print(f"Executing SHARE strategy for {doc_path}")

        # For now, just log the decision
        # In a full implementation, this would:
        # 1. Copy the file to both branches
        # 2. Remove branch-specific versions
        # 3. Commit the changes

        history = self.load_merge_history()
        history.append({
            "timestamp": datetime.now().isoformat(),
            "doc_path": doc_path,
            "strategy": "SHARE",
            "action": "merged_to_both_branches"
        })
        self.save_merge_history(history)

    def execute_branch_specific_strategy(self, doc_path: str):
        """Execute BRANCH_SPECIFIC strategy - keep separate versions."""
        print(f"Executing BRANCH_SPECIFIC strategy for {doc_path}")

        # Keep the branch-specific versions as-is
        history = self.load_merge_history()
        history.append({
            "timestamp": datetime.now().isoformat(),
            "doc_path": doc_path,
            "strategy": "BRANCH_SPECIFIC",
            "action": "kept_separate_versions"
        })
        self.save_merge_history(history)

    def execute_strategy(self, strategy: str, doc_path: str, analysis: Dict = None, branch: str = None):
        """Execute the determined strategy."""
        if strategy == "SHARE":
            self.execute_share_strategy(doc_path)
        elif strategy == "BRANCH_SPECIFIC":
            self.execute_branch_specific_strategy(doc_path)
        elif strategy == "MANUAL_REVIEW":
            self.create_review_request(doc_path, analysis, branch)
        else:
            print(f"Unknown strategy: {strategy}")

    def approve_review(self, review_id: str, decision: str, reason: str = ""):
        """Approve a review decision."""
        queue = self.load_review_queue()

        # Find and update the review
        for review in queue["pending_reviews"]:
            if review["id"] == review_id:
                review["status"] = "approved"
                review["decision"] = decision
                review["reason"] = reason
                review["approved_at"] = datetime.now().isoformat()

                # Move to completed
                queue["completed_reviews"].append(review)
                queue["pending_reviews"].remove(review)

                self.save_review_queue(queue)
                print(f"Approved review {review_id} with decision: {decision}")
                return True

        print(f"Review {review_id} not found")
        return False

    def get_pending_reviews(self) -> List[Dict]:
        """Get list of pending reviews."""
        queue = self.load_review_queue()
        return queue["pending_reviews"]

    def get_review_status(self) -> Dict:
        """Get overall review status."""
        queue = self.load_review_queue()
        history = self.load_merge_history()

        return {
            "pending_reviews": len(queue["pending_reviews"]),
            "completed_reviews": len(queue["completed_reviews"]),
            "total_decisions": len(history),
            "share_decisions": len([h for h in history if h["strategy"] == "SHARE"]),
            "branch_specific_decisions": len([h for h in history if h["strategy"] == "BRANCH_SPECIFIC"])
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Documentation Merge Strategist")
    parser.add_argument("--analyze", help="Analyze and determine strategy for document")
    parser.add_argument("--execute", help="Execute strategy for document")
    parser.add_argument("--review", help="Create review request for document")
    parser.add_argument("--approve", help="Approve review (format: review_id:decision:reason)")
    parser.add_argument("--status", action="store_true", help="Show review status")
    parser.add_argument("--branch", default="main", help="Branch for analysis")

    args = parser.parse_args()

    strategist = DocsMergeStrategist()

    if args.status:
        status = strategist.get_review_status()
        print("Review Status:")
        print(json.dumps(status, indent=2))
        return

    if args.analyze:
        # Import the analyzer
        from docs_content_analyzer import DocsContentAnalyzer
        analyzer = DocsContentAnalyzer()
        analysis = analyzer.compare_branches(args.analyze)
        strategy = strategist.determine_strategy(analysis)
        print(f"Recommended strategy for {args.analyze}: {strategy}")
        print(f"Analysis: {json.dumps(analysis, indent=2)}")

    elif args.execute:
        # This would need analysis as well
        print("Execute requires analysis - use --analyze first")

    elif args.review:
        from docs_content_analyzer import DocsContentAnalyzer
        analyzer = DocsContentAnalyzer()
        analysis = analyzer.compare_branches(args.review)
        strategist.create_review_request(args.review, analysis, args.branch)

    elif args.approve:
        parts = args.approve.split(":", 2)
        if len(parts) >= 2:
            review_id, decision = parts[0], parts[1]
            reason = parts[2] if len(parts) > 2 else ""
            strategist.approve_review(review_id, decision, reason)
        else:
            print("Invalid approve format. Use: review_id:decision:reason")


if __name__ == "__main__":
    main()