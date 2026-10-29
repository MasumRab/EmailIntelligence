#!/usr/bin/env python3
"""
Documentation Review Manager

Manages the review workflow for documentation sharing decisions,
provides dashboard interface, and tracks review progress.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import argparse


class DocsReviewManager:
    def __init__(self):
        self.review_queue_file = Path("docs/.review-queue.json")
        self.reviews_dir = Path("docs/reviews")
        self.reviews_dir.mkdir(exist_ok=True)

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

    def get_pending_reviews(self) -> List[Dict]:
        """Get all pending reviews."""
        queue = self.load_review_queue()
        return queue["pending_reviews"]

    def get_completed_reviews(self) -> List[Dict]:
        """Get all completed reviews."""
        queue = self.load_review_queue()
        return queue["completed_reviews"]

    def get_review_by_id(self, review_id: str) -> Optional[Dict]:
        """Get a specific review by ID."""
        queue = self.load_review_queue()
        for review in queue["pending_reviews"] + queue["completed_reviews"]:
            if review["id"] == review_id:
                return review
        return None

    def create_review_request(self, doc_path: str, analysis: Dict, branch: str, priority: str = "medium"):
        """Create a new review request."""
        queue = self.load_review_queue()

        review_id = f"{Path(doc_path).stem}_{int(datetime.now().timestamp())}"

        review_request = {
            "id": review_id,
            "doc_path": doc_path,
            "branch": branch,
            "change_type": "content_update",
            "analysis": analysis,
            "strategy": analysis.get('recommendation', 'UNKNOWN'),
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "reviewers": ["team-lead", "tech-writer"],
            "priority": priority,
            "due_date": (datetime.now() + timedelta(days=3)).isoformat()
        }

        queue["pending_reviews"].append(review_request)
        self.save_review_queue(queue)

        # Create review markdown file
        self.create_review_markdown(review_request)

        print(f"Created review request: {review_id}")
        return review_id

    def create_review_markdown(self, review_request: Dict):
        """Create a detailed markdown review file."""
        review_id = review_request['id']
        review_file = self.reviews_dir / f"review_{review_id}.md"

        analysis = review_request['analysis']
        doc_path = review_request['doc_path']

        # Build content
        content = f"""# Documentation Review: {Path(doc_path).name}

**Review ID**: {review_id}
**Document**: {doc_path}
**Branch**: {review_request['branch']}
**Priority**: {review_request['priority']}
**Created**: {review_request['created_at']}
**Due Date**: {review_request['due_date']}
**Status**: {review_request['status']}

## Analysis Summary

### Goal Similarity: {analysis.get('goal_analysis', {}).get('similarity', 'N/A')}
- **Main Goals**: {len(analysis.get('goal_analysis', {}).get('main_goals', []))}
- **Scientific Goals**: {len(analysis.get('goal_analysis', {}).get('scientific_goals', []))}
- **Overlapping Goals**: {analysis.get('goal_analysis', {}).get('overlap', 0)}
- **Different Goals**: {analysis.get('goal_analysis', {}).get('differences', 0)}

### Audience Analysis
- **Overlap**: {', '.join(analysis.get('audience_analysis', {}).get('overlap', [])) or 'None'}
- **Main Only**: {', '.join(analysis.get('audience_analysis', {}).get('main_unique', [])) or 'None'}
- **Scientific Only**: {', '.join(analysis.get('audience_analysis', {}).get('scientific_unique', [])) or 'None'}

### Technical Depth Comparison
| Branch | Level | Score | Code Blocks | Technical Terms |
|--------|-------|-------|-------------|-----------------|
| Main | {analysis.get('technical_analysis', {}).get('main', {}).get('level', 'N/A')} | {analysis.get('technical_analysis', {}).get('main', {}).get('technical_score', 0):.2f} | {analysis.get('technical_analysis', {}).get('main', {}).get('code_blocks', 0)} | {analysis.get('technical_analysis', {}).get('main', {}).get('technical_terms', 0)} |
| Scientific | {analysis.get('technical_analysis', {}).get('scientific', {}).get('level', 'N/A')} | {analysis.get('technical_analysis', {}).get('scientific', {}).get('technical_score', 0):.2f} | {analysis.get('technical_analysis', {}).get('scientific', {}).get('code_blocks', 0)} | {analysis.get('technical_analysis', {}).get('scientific', {}).get('technical_terms', 0)} |

## Recommended Strategy: {review_request['strategy']}

## Review Decision

**☐ SHARE** - Merge documentation to both branches (recommended for high similarity)
**☐ BRANCH_SPECIFIC** - Keep separate versions (recommended for significant differences)
**☐ MANUAL_REVIEW** - Needs further discussion

### Reasoning:
*(Provide detailed reasoning for your decision)*

### Additional Notes:
*(Any additional context or concerns)*

## Reviewers
{chr(10).join(f"- [ ] @{reviewer}" for reviewer in review_request['reviewers'])}

---
*Review submitted by: [Your Name]*
*Date: {datetime.now().strftime('%Y-%m-%d')}*
"""

        with open(review_file, 'w') as f:
            f.write(content)

        print(f"Review file created: {review_file}")

    def approve_review(self, review_id: str, decision: str, reviewer: str, reason: str = ""):
        """Approve a review with decision."""
        queue = self.load_review_queue()

        # Find the review
        for review in queue["pending_reviews"]:
            if review["id"] == review_id:
                # Update review
                review["status"] = "approved"
                review["decision"] = decision
                review["approved_by"] = reviewer
                review["reason"] = reason
                review["approved_at"] = datetime.now().isoformat()

                # Move to completed
                queue["completed_reviews"].append(review)
                queue["pending_reviews"].remove(review)

                self.save_review_queue(queue)

                # Update the markdown file
                self.update_review_markdown(review)

                print(f"Review {review_id} approved with decision: {decision}")
                return True

        print(f"Review {review_id} not found in pending reviews")
        return False

    def update_review_markdown(self, review: Dict):
        """Update the review markdown file with approval information."""
        review_file = self.reviews_dir / f"review_{review['id']}.md"

        if review_file.exists():
            with open(review_file, 'r') as f:
                content = f.read()

            # Add approval information
            approval_section = f"""

## Approval Information
**Decision**: {review['decision']}
**Approved By**: {review.get('approved_by', 'Unknown')}
**Approved At**: {review.get('approved_at', 'Unknown')}
**Reason**: {review.get('reason', 'Not provided')}
"""
            content += approval_section

            with open(review_file, 'w') as f:
                f.write(content)

    def show_dashboard(self):
        """Display the review dashboard."""
        queue = self.load_review_queue()

        print("📋 Documentation Review Dashboard")
        print("=" * 50)

        pending = queue["pending_reviews"]
        completed = queue["completed_reviews"]

        print(f"\n📝 Pending Reviews: {len(pending)}")
        if pending:
            for review in pending:
                priority_icon = "🔴" if review["priority"] == "high" else "🟡" if review["priority"] == "medium" else "🟢"
                print(f"  {priority_icon} {review['id']}: {Path(review['doc_path']).name}")
                print(f"      Branch: {review['branch']} | Strategy: {review['strategy']}")
                print(f"      Created: {review['created_at'][:10]}")
        else:
            print("  ✅ No pending reviews")

        print(f"\n✅ Completed Reviews: {len(completed)}")
        if completed:
            share_count = sum(1 for r in completed if r.get("decision") == "SHARE")
            branch_count = sum(1 for r in completed if r.get("decision") == "BRANCH_SPECIFIC")
            print(f"  📤 Shared: {share_count} | 🔀 Branch-Specific: {branch_count}")

        print(f"\n📊 Overall Status:")
        total = len(pending) + len(completed)
        if total > 0:
            completion_rate = len(completed) / total * 100
            print(f"  Completion Rate: {completion_rate:.1f}%")
            print(f"  Average Reviews/Day: {total / max(1, (datetime.now() - datetime.fromisoformat(min(r['created_at'] for r in pending + completed))).days):.1f}")

    def show_review_details(self, review_id: str):
        """Show detailed information about a specific review."""
        review = self.get_review_by_id(review_id)

        if not review:
            print(f"Review {review_id} not found")
            return

        print(f"\n📄 Review Details: {review_id}")
        print("-" * 40)
        print(f"Document: {review['doc_path']}")
        print(f"Branch: {review['branch']}")
        print(f"Status: {review['status']}")
        print(f"Priority: {review['priority']}")
        print(f"Strategy: {review['strategy']}")
        print(f"Created: {review['created_at']}")

        if 'approved_at' in review:
            print(f"Approved: {review['approved_at']}")
            print(f"Decision: {review.get('decision', 'Unknown')}")
            print(f"Reason: {review.get('reason', 'Not provided')}")

        analysis = review['analysis']
        if 'goal_analysis' in analysis:
            print(f"\nGoal Similarity: {analysis['goal_analysis'].get('similarity', 'N/A')}")
            print(f"Overlapping Goals: {analysis['goal_analysis'].get('overlap', 0)}")

    def cleanup_old_reviews(self, days: int = 30):
        """Clean up old completed reviews."""
        queue = self.load_review_queue()
        cutoff_date = datetime.now() - timedelta(days=days)

        # Filter out old completed reviews
        filtered_completed = []
        for review in queue["completed_reviews"]:
            review_date = datetime.fromisoformat(review.get("approved_at", review["created_at"]))
            if review_date > cutoff_date:
                filtered_completed.append(review)

        removed_count = len(queue["completed_reviews"]) - len(filtered_completed)
        queue["completed_reviews"] = filtered_completed

        self.save_review_queue(queue)
        print(f"Cleaned up {removed_count} old reviews")


def main():
    parser = argparse.ArgumentParser(description="Documentation Review Manager")
    parser.add_argument("--dashboard", action="store_true", help="Show review dashboard")
    parser.add_argument("--details", help="Show details for specific review ID")
    parser.add_argument("--approve", help="Approve review (format: review_id:decision:reviewer:reason)")
    parser.add_argument("--create", help="Create review for document", metavar="DOC_PATH")
    parser.add_argument("--branch", default="main", help="Branch for new review")
    parser.add_argument("--cleanup", type=int, metavar="DAYS", help="Clean up reviews older than DAYS")

    args = parser.parse_args()

    manager = DocsReviewManager()

    if args.dashboard:
        manager.show_dashboard()

    elif args.details:
        manager.show_review_details(args.details)

    elif args.approve:
        parts = args.approve.split(":", 3)
        if len(parts) >= 3:
            review_id, decision, reviewer = parts[0], parts[1], parts[2]
            reason = parts[3] if len(parts) > 3 else ""
            manager.approve_review(review_id, decision, reviewer, reason)
        else:
            print("Invalid approve format. Use: review_id:decision:reviewer:reason")

    elif args.create:
        # Import analyzer to create review
        from docs_content_analyzer import DocsContentAnalyzer
        analyzer = DocsContentAnalyzer()
        analysis = analyzer.compare_branches(args.create)
        review_id = manager.create_review_request(args.create, analysis, args.branch)
        print(f"Created review: {review_id}")

    elif args.cleanup:
        manager.cleanup_old_reviews(args.cleanup)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()