#!/usr/bin/env python3
"""
Query tool for task progress findings.

Usage:
    python query_findings.py --phase phase2_assessment
    python query_findings.py --task 3.1.4
    python query_findings.py --from 2026-01-01 --to 2026-01-31
    python query_findings.py --pattern "merge-base"
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


class FindingsQuery:
    def __init__(self, base_dir="task_data/findings"):
        self.base_dir = Path(base_dir)
        self.findings = []
        self.load_all_findings()

    def load_all_findings(self):
        """Load all JSON findings from all phase directories."""
        if not self.base_dir.exists():
            print(f"Findings directory not found: {self.base_dir}")
            return

        for phase_dir in self.base_dir.glob("phase*"):
            if phase_dir.is_dir():
                for json_file in phase_dir.glob("*.json"):
                    try:
                        with open(json_file, "r") as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                self.findings.extend(data)
                            elif isinstance(data, dict):
                                self.findings.append(data)
                    except (json.JSONDecodeError, FileNotFoundError) as e:
                        print(f"Warning: Could not load {json_file}: {e}")

    def query_by_phase(self, phase):
        """Query findings by phase."""
        return [f for f in self.findings if f.get("phase") == phase]

    def query_by_task(self, task_id):
        """Query findings by task ID."""
        return [f for f in self.findings if f.get("task_id") == task_id]

    def query_by_date_range(self, from_date, to_date):
        """Query findings by date range."""
        results = []
        for f in self.findings:
            timestamp = f.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if from_date <= dt.date() <= to_date:
                        results.append(f)
                except ValueError:
                    continue
        return results

    def query_by_pattern(self, pattern):
        """Query findings by text pattern."""
        pattern = pattern.lower()
        results = []
        for f in self.findings:
            # Search in all string fields
            for key, value in f.items():
                if isinstance(value, str) and pattern in value.lower():
                    results.append(f)
                    break
                elif isinstance(value, dict):
                    for k, v in value.items():
                        if isinstance(v, str) and pattern in v.lower():
                            results.append(f)
                            break
        return results

    def print_findings(self, findings, format_type="table"):
        """Print findings in specified format."""
        if not findings:
            print("No findings found.")
            return

        if format_type == "table":
            self.print_table(findings)
        elif format_type == "json":
            print(json.dumps(findings, indent=2))
        else:
            for f in findings:
                print(f"Task {f.get('task_id', 'Unknown')}: {f.get('decision', 'No decision')}")

    def print_table(self, findings):
        """Print findings in table format."""
        print(f"{'Task ID':<10} {'Phase':<20} {'Success':<8} {'Duration':<10} {'Decision':<50}")
        print("-" * 100)
        for f in findings:
            task_id = f.get("task_id", "Unknown")[:10]
            phase = f.get("phase", "Unknown")[:20]
            success = str(f.get("outcome", {}).get("success", "Unknown"))[:8]
            duration = str(f.get("outcome", {}).get("duration_ms", "N/A"))[:10]
            decision = f.get("decision", "No decision")[:50]
            print(f"{task_id:<10} {phase:<20} {success:<8} {duration:<10} {decision:<50}")

    def get_summary_stats(self):
        """Get summary statistics for all findings."""
        if not self.findings:
            return {}

        total = len(self.findings)
        successful = sum(1 for f in self.findings if f.get("outcome", {}).get("success"))
        phases = set(f.get("phase") for f in self.findings if f.get("phase"))

        return {
            "total_findings": total,
            "successful": successful,
            "success_rate": f"{successful / total * 100:.1f}%" if total > 0 else "0%",
            "phases": list(phases),
            "date_range": self.get_date_range(),
        }

    def get_date_range(self):
        """Get date range of findings."""
        dates = []
        for f in self.findings:
            timestamp = f.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    dates.append(dt.date())
                except ValueError:
                    continue

        if dates:
            return f"{min(dates)} to {max(dates)}"
        return "No dates found"


def main():
    parser = argparse.ArgumentParser(description="Query task progress findings")
    parser.add_argument("--phase", help="Query by phase (e.g., phase2_assessment)")
    parser.add_argument("--task", help="Query by task ID (e.g., 3.1.4)")
    parser.add_argument("--from", dest="from_date", help="From date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="To date (YYYY-MM-DD)")
    parser.add_argument("--pattern", help="Search for text pattern")
    parser.add_argument(
        "--format", choices=["table", "json"], default="table", help="Output format"
    )
    parser.add_argument("--stats", action="store_true", help="Show summary statistics")

    args = parser.parse_args()

    # Initialize query
    query = FindingsQuery()

    # Execute query
    if args.stats:
        stats = query.get_summary_stats()
        print("Summary Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        return

    if args.phase:
        findings = query.query_by_phase(args.phase)
        print(f"Findings for phase {args.phase}:")
    elif args.task:
        findings = query.query_by_task(args.task)
        print(f"Findings for task {args.task}:")
    elif args.from_date and args.to_date:
        from_date = datetime.strptime(args.from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(args.to_date, "%Y-%m-%d").date()
        findings = query.query_by_date_range(from_date, to_date)
        print(f"Findings from {args.from_date} to {args.to_date}:")
    elif args.pattern:
        findings = query.query_by_pattern(args.pattern)
        print(f"Findings matching pattern '{args.pattern}':")
    else:
        print("Please specify a query option (--phase, --task, --from/--to, --pattern, or --stats)")
        sys.exit(1)

    # Print results
    query.print_findings(findings, args.format)


if __name__ == "__main__":
    main()
