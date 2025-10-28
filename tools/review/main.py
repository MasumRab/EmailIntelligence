#!/usr/bin/env python3
"""
Multi-Agent Code Review System for EmailIntelligence

This script orchestrates multiple specialized agents to perform comprehensive
code reviews covering security, performance, quality, and architectural aspects.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.review.security_agent import SecurityReviewAgent
from tools.review.performance_agent import PerformanceReviewAgent
from tools.review.quality_agent import QualityReviewAgent
from tools.review.architecture_agent import ArchitectureReviewAgent


class MultiAgentCodeReview:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or ROOT_DIR / "tools" / "review" / "config.json"
        self.load_config()
        self.initialize_agents()
        
    def load_config(self):
        """Load configuration from JSON file."""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
            
    def initialize_agents(self):
        """Initialize all review agents based on configuration."""
        self.agents = {}
        
        if self.config["review_agents"]["security"]["enabled"]:
            self.agents["security"] = SecurityReviewAgent()
            
        if self.config["review_agents"]["performance"]["enabled"]:
            self.agents["performance"] = PerformanceReviewAgent()
            
        if self.config["review_agents"]["quality"]["enabled"]:
            self.agents["quality"] = QualityReviewAgent()
            
        if self.config["review_agents"]["architecture"]["enabled"]:
            self.agents["architecture"] = ArchitectureReviewAgent()
            
    def get_files_to_review(self, target_paths: List[str] = None) -> List[str]:
        """Get list of files to review based on configuration patterns."""
        if target_paths:
            # If specific paths provided, use those
            files = []
            for path in target_paths:
                if os.path.isfile(path):
                    files.append(path)
                elif os.path.isdir(path):
                    # Get all files in directory matching patterns
                    for pattern in self.config["file_patterns"]["include"]:
                        files.extend([str(p) for p in Path(path).glob(pattern)])
            return files
        
        # Default behavior: scan project directories
        files = []
        include_patterns = self.config["file_patterns"]["include"]
        exclude_patterns = self.config["file_patterns"]["exclude"]
        
        for pattern in include_patterns:
            matched_files = [str(p) for p in ROOT_DIR.glob(pattern)]
            files.extend(matched_files)
            
        # Filter out excluded files
        filtered_files = []
        for file_path in files:
            should_exclude = False
            for exclude_pattern in exclude_patterns:
                if exclude_pattern in file_path:
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_files.append(file_path)
                
        return list(set(filtered_files))  # Remove duplicates
        
    def run_review(self, target_paths: List[str] = None) -> Dict:
        """Run code review using all enabled agents."""
        files_to_review = self.get_files_to_review(target_paths)
        results = {}
        
        print(f"Starting multi-agent code review for {len(files_to_review)} files...")
        
        # Run each agent on the files
        for agent_name, agent in self.agents.items():
            print(f"Running {agent_name} review agent...")
            agent_results = agent.review_files(files_to_review)
            results[agent_name] = agent_results
            
        return results
        
    def generate_report(self, results: Dict, format: str = "console") -> str:
        """Generate a report in the specified format."""
        if format == "console":
            return self._generate_console_report(results)
        elif format == "markdown":
            return self._generate_markdown_report(results)
        elif format == "json":
            return json.dumps(results, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
    def _generate_console_report(self, results: Dict) -> str:
        """Generate a console-friendly report."""
        report_lines = ["# Multi-Agent Code Review Report", ""]
        
        for agent_name, agent_results in results.items():
            report_lines.append(f"## {agent_name.capitalize()} Review")
            report_lines.append("")
            
            if not agent_results.get("issues"):
                report_lines.append("No issues found.")
                report_lines.append("")
                continue
                
            # Group issues by priority
            critical_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "critical"]
            high_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "high"]
            medium_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "medium"]
            low_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "low"]
            
            if critical_issues:
                report_lines.append("### Critical Issues")
                for issue in critical_issues:
                    report_lines.append(f"- {issue.get('description', 'No description')}")
                    report_lines.append(f"  File: {issue.get('file', 'Unknown')}")
                    report_lines.append(f"  Line: {issue.get('line', 'Unknown')}")
                    report_lines.append("")
                    
            if high_issues:
                report_lines.append("### High Priority Issues")
                for issue in high_issues:
                    report_lines.append(f"- {issue.get('description', 'No description')}")
                    report_lines.append(f"  File: {issue.get('file', 'Unknown')}")
                    report_lines.append(f"  Line: {issue.get('line', 'Unknown')}")
                    report_lines.append("")
                    
            if medium_issues:
                report_lines.append("### Medium Priority Issues")
                for issue in medium_issues:
                    report_lines.append(f"- {issue.get('description', 'No description')}")
                    report_lines.append(f"  File: {issue.get('file', 'Unknown')}")
                    report_lines.append(f"  Line: {issue.get('line', 'Unknown')}")
                    report_lines.append("")
                    
            if low_issues:
                report_lines.append("### Low Priority Issues")
                for issue in low_issues:
                    report_lines.append(f"- {issue.get('description', 'No description')}")
                    report_lines.append(f"  File: {issue.get('file', 'Unknown')}")
                    report_lines.append(f"  Line: {issue.get('line', 'Unknown')}")
                    report_lines.append("")
                    
        return "\n".join(report_lines)
        
    def _generate_markdown_report(self, results: Dict) -> str:
        """Generate a markdown report."""
        report_lines = ["# Multi-Agent Code Review Report", ""]
        
        for agent_name, agent_results in results.items():
            report_lines.append(f"## {agent_name.capitalize()} Review")
            report_lines.append("")
            
            if not agent_results.get("issues"):
                report_lines.append("No issues found.")
                report_lines.append("")
                continue
                
            # Group issues by priority
            critical_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "critical"]
            high_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "high"]
            medium_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "medium"]
            low_issues = [issue for issue in agent_results["issues"] if issue.get("priority") == "low"]
            
            if critical_issues:
                report_lines.append("### Critical Issues")
                report_lines.append("| Description | File | Line |")
                report_lines.append("|-------------|------|------|")
                for issue in critical_issues:
                    desc = issue.get('description', 'No description')
                    file = issue.get('file', 'Unknown')
                    line = str(issue.get('line', 'Unknown'))
                    report_lines.append(f"| {desc} | {file} | {line} |")
                report_lines.append("")
                    
            if high_issues:
                report_lines.append("### High Priority Issues")
                report_lines.append("| Description | File | Line |")
                report_lines.append("|-------------|------|------|")
                for issue in high_issues:
                    desc = issue.get('description', 'No description')
                    file = issue.get('file', 'Unknown')
                    line = str(issue.get('line', 'Unknown'))
                    report_lines.append(f"| {desc} | {file} | {line} |")
                report_lines.append("")
                    
            if medium_issues:
                report_lines.append("### Medium Priority Issues")
                report_lines.append("| Description | File | Line |")
                report_lines.append("|-------------|------|------|")
                for issue in medium_issues:
                    desc = issue.get('description', 'No description')
                    file = issue.get('file', 'Unknown')
                    line = str(issue.get('line', 'Unknown'))
                    report_lines.append(f"| {desc} | {file} | {line} |")
                report_lines.append("")
                    
            if low_issues:
                report_lines.append("### Low Priority Issues")
                report_lines.append("| Description | File | Line |")
                report_lines.append("|-------------|------|------|")
                for issue in low_issues:
                    desc = issue.get('description', 'No description')
                    file = issue.get('file', 'Unknown')
                    line = str(issue.get('line', 'Unknown'))
                    report_lines.append(f"| {desc} | {file} | {line} |")
                report_lines.append("")
                    
        return "\n".join(report_lines)
        
    def save_report(self, report: str, format: str, output_path: str = None):
        """Save the report to a file."""
        if not output_path:
            output_path = ROOT_DIR / f"code_review_report.{format}"
            
        with open(output_path, 'w') as f:
            f.write(report)
            
        print(f"Report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Code Review System")
    parser.add_argument("--target", nargs="*", help="Specific files or directories to review")
    parser.add_argument("--format", choices=["console", "markdown", "json"], 
                       default="console", help="Output format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--config", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Initialize the review system
    review_system = MultiAgentCodeReview(config_path=args.config)
    
    # Run the review
    results = review_system.run_review(args.target)
    
    # Generate and save report
    report = review_system.generate_report(results, format=args.format)
    
    if args.output:
        review_system.save_report(report, args.format, args.output)
    else:
        print(report)


if __name__ == "__main__":
    main()