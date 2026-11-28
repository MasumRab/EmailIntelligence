#!/usr/bin/env python3
"""
Branch Analysis Summary CLI

Universal quick reference tool for branch analysis and sync architecture findings.
Tool-agnostic - works with any AI assistant or manual analysis.

Usage:
    python scripts/branch_analysis_summary.py [--section SECTION] [--format FORMAT]

Examples:
    python scripts/branch_analysis_summary.py                    # Full summary
    python scripts/branch_analysis_summary.py --section metrics  # Just metrics
    python scripts/branch_analysis_summary.py --format json      # JSON output
"""

import json
from pathlib import Path
from typing import Optional, Any
import os


def load_analysis_results() -> Optional[dict]:
    """Load analysis results from JSON file.
    
    Searches in standard locations:
    - docs/analysis/ (universal)
    - .qwen/understand/ (Qwen-specific)
    - Current directory
    """
    # Universal paths first (tool-agnostic)
    possible_paths = [
        Path(__file__).parent.parent / "docs" / "analysis" / "branch_sync_architecture.json",
        Path.cwd() / "docs" / "analysis" / "branch_sync_architecture.json",
        # Fallback to Qwen-specific paths
        Path(__file__).parent.parent / ".qwen" / "understand" / "branch_sync_architecture.json",
        Path.cwd() / ".qwen" / "understand" / "branch_sync_architecture.json",
        Path(__file__).parent / "branch_sync_architecture.json",
    ]
    
    for analysis_file in possible_paths:
        if analysis_file.exists():
            with open(analysis_file, 'r') as f:
                return json.load(f)
    
    return None


def safe_get(data: dict, *keys: str, default: Any = "N/A") -> Any:
    """Safely get nested dictionary values."""
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data


def print_executive_summary(data: dict):
    """Print executive summary."""
    print("\n" + "="*80)
    print("BRANCH ANALYSIS & SYNC ARCHITECTURE - EXECUTIVE SUMMARY")
    print("="*80)

    health_score = safe_get(data, 'health_score', default=safe_get(data, 'analysis_metadata', 'health_score'))
    files_analyzed = safe_get(data, 'files_analyzed', default=safe_get(data, 'analysis_metadata', 'files_analyzed'))
    total_loc = safe_get(data, 'total_loc', default=safe_get(data, 'analysis_metadata', 'total_loc'))
    
    print(f"\n📊 Project Health Score: {health_score}/10")
    print(f"📁 Files Analyzed: {files_analyzed}")
    print(f"📏 Total Lines of Code: {total_loc:,}" if isinstance(total_loc, int) else f"📏 Total Lines of Code: {total_loc}")

    print("\n🚨 Issues by Priority:")
    issues = safe_get(data, 'issues_by_priority', default={})
    print(f"   Critical (P0): {issues.get('critical', 'N/A')} ❌")
    print(f"   High (P1):     {issues.get('high', 'N/A')} ⚠️")
    print(f"   Medium (P2):   {issues.get('medium', 'N/A')} ⚡")
    print(f"   Low (P3):      {issues.get('low', 'N/A')} ℹ️")

    print("\n🎯 Top 3 Critical Issues:")
    critical_issues = safe_get(data, 'critical_issues', default=[])
    for i, issue in enumerate(critical_issues[:3], 1):
        title = issue.get('title', 'N/A') if isinstance(issue, dict) else str(issue)
        location = issue.get('location', 'N/A') if isinstance(issue, dict) else 'N/A'
        impact = issue.get('impact', 'N/A') if isinstance(issue, dict) else 'N/A'
        print(f"   {i}. {title}")
        print(f"      Location: {location}")
        print(f"      Impact: {impact}")
        print()


def print_quantitative_metrics(data: dict):
    """Print quantitative metrics."""
    print("\n" + "="*80)
    print("QUANTITATIVE METRICS")
    print("="*80)

    print("\n📏 Size Metrics:")
    size_metrics = safe_get(data, 'size_metrics', default={})
    avg_size = safe_get(size_metrics, 'avg_module_size', default='N/A')
    largest = safe_get(size_metrics, 'largest_module', default={})
    smallest = safe_get(size_metrics, 'smallest_module', default={})
    
    print(f"   Average Module Size: {avg_size} LOC")
    print(f"   Largest Module: {largest.get('name', 'N/A')} ({largest.get('loc', 'N/A')} LOC)")
    print(f"   Smallest Module: {smallest.get('name', 'N/A')} ({smallest.get('loc', 'N/A')} LOC)")

    print("\n🔗 Coupling Metrics:")
    coupling = safe_get(data, 'coupling_metrics', default={})
    print(f"   Average Afferent Coupling: {coupling.get('avg_ca', 'N/A')}")
    print(f"   Average Efferent Coupling: {coupling.get('avg_ce', 'N/A')}")
    print(f"   Average Instability: {coupling.get('avg_instability', 'N/A')}")

    print("\n📊 Complexity Distribution:")
    complexity = safe_get(data, 'complexity_distribution', default={})
    print(f"   Low (1-5):      {complexity.get('low', 'N/A')}%")
    print(f"   Medium (6-10):  {complexity.get('medium', 'N/A')}%")
    print(f"   High (11-20):   {complexity.get('high', 'N/A')}%")
    print(f"   Very High (>20): {complexity.get('very_high', 'N/A')}%")

    print("\n📋 Code Duplication:")
    duplication = safe_get(data, 'duplication', default={})
    print(f"   Total Duplication: {duplication.get('total', 'N/A')}%")
    print(f"   Exact Duplicates: {duplication.get('exact', 'N/A')}%")
    print(f"   Near Duplicates: {duplication.get('near', 'N/A')}%")
    print(f"   Structural: {duplication.get('structural', 'N/A')}%")


def print_recommendations(data: dict):
    """Print top recommendations."""
    print("\n" + "="*80)
    print("TOP RECOMMENDATIONS")
    print("="*80)

    print("\n🔴 Critical (Fix This Week):")
    recommendations = safe_get(data, 'recommendations', 'critical', default=[])
    for rec in recommendations[:3]:
        title = rec.get('title', 'N/A') if isinstance(rec, dict) else str(rec)
        effort = rec.get('effort', 'N/A') if isinstance(rec, dict) else 'N/A'
        roi = rec.get('roi', 'N/A') if isinstance(rec, dict) else 'N/A'
        desc = rec.get('description', 'N/A') if isinstance(rec, dict) else ''
        print(f"   • {title}")
        print(f"     Effort: {effort} | ROI: {roi}")
        print(f"     {desc}")
        print()
    
    print("\n⚠️ High Priority (Fix This Sprint):")
    high_recs = safe_get(data, 'recommendations', 'high', default=[])
    for rec in high_recs[:3]:
        title = rec.get('title', 'N/A') if isinstance(rec, dict) else str(rec)
        effort = rec.get('effort', 'N/A') if isinstance(rec, dict) else 'N/A'
        roi = rec.get('roi', 'N/A') if isinstance(rec, dict) else 'N/A'
        print(f"   • {title}")
        print(f"     Effort: {effort} | ROI: {roi}")
        print()
    
    print("\n📋 Implementation Roadmap:")
    roadmap = safe_get(data, 'roadmap', default={})
    for phase in ['phase1', 'phase2', 'phase3', 'phase4']:
        phase_data = roadmap.get(phase, {})
        if phase_data:
            duration = phase_data.get('duration', 'N/A')
            focus = phase_data.get('focus', 'N/A')
            print(f"   {phase.replace('phase', 'Phase ').title()}: {duration} - {focus}")
    
    total_hours = roadmap.get('total_hours', 'N/A')
    risk_adjusted = roadmap.get('risk_adjusted_hours', 'N/A')
    developers = roadmap.get('developers', 'N/A')
    print(f"\n💰 Total Estimated Effort: {total_hours} hours ({risk_adjusted} risk-adjusted)")
    print(f"👥 Recommended Team: {developers} developers")


def print_shell_vs_python(data: dict):
    """Print Shell vs Python comparison."""
    print("\n" + "="*80)
    print("SHELL VS PYTHON COMPARISON")
    print("="*80)

    comparison = safe_get(data, 'shell_vs_python', default={})
    
    print("\n📝 Maintainability:")
    maint = comparison.get('maintainability', {})
    print(f"   Shell:   {maint.get('shell', 'N/A')}/10")
    print(f"   Python:  {maint.get('python', 'N/A')}/10 ✓")
    
    print("\n🛡️ Error Handling:")
    error = comparison.get('error_handling', {})
    print(f"   Shell:   {error.get('shell', 'N/A')}/10")
    print(f"   Python:  {error.get('python', 'N/A')}/10 ✓")
    
    print("\n🧪 Testability:")
    test = comparison.get('testability', {})
    print(f"   Shell:   {test.get('shell', 'N/A')}/10")
    print(f"   Python:  {test.get('python', 'N/A')}/10 ✓")
    
    print("\n⚡ Performance:")
    perf = comparison.get('performance', {})
    print(f"   Shell:   {perf.get('shell', 'N/A')}/10 ✓")
    print(f"   Python:  {perf.get('python', 'N/A')}/10")
    
    print("\n💡 Best Use Cases:")
    print("\n   Shell Excels At:")
    for use_case in comparison.get('shell_best_for', ['N/A']):
        print(f"     • {use_case}")
    
    print("\n   Python Excels At:")
    for use_case in comparison.get('python_best_for', ['N/A']):
        print(f"     • {use_case}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Branch Analysis Summary CLI - Universal tool-agnostic architecture analysis viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/branch_analysis_summary.py                    # View full summary
  python scripts/branch_analysis_summary.py --section summary  # Executive summary only
  python scripts/branch_analysis_summary.py --section metrics  # Quantitative metrics
  python scripts/branch_analysis_summary.py --format json      # JSON output

Analysis Files:
  docs/analysis/branch_sync_architecture_report.md  - Full report
  docs/analysis/branch_sync_diagrams.mermaid        - Architecture diagrams
  docs/analysis/metrics.json                        - Structured metrics
        """
    )
    parser.add_argument('--section', choices=['all', 'summary', 'metrics', 'recommendations', 'comparison'],
                       default='all', help='Section to display (default: all)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format (default: text)')
    
    args = parser.parse_args()
    
    # Load analysis results
    data = load_analysis_results()
    
    if not data:
        print("❌ Analysis results not found.")
        print("\n📁 Expected locations:")
        print("   - docs/analysis/branch_sync_architecture.json")
        print("   - docs/analysis/metrics.json")
        print("\n💡 Run the architecture analysis first:")
        print("   qwen /smart-understand branch analysis and sync task")
        print("   claude /smart-understand branch analysis and sync task")
        print("   cursor /smart-understand branch analysis and sync task")
        print("   (or any other AI assistant with architecture analysis capabilities)")
        return
    
    if args.format == 'json':
        print(json.dumps(data, indent=2))
        return
    
    # Print requested sections
    if args.section in ['all', 'summary']:
        print_executive_summary(data)
    
    if args.section in ['all', 'metrics']:
        print_quantitative_metrics(data)
    
    if args.section in ['all', 'recommendations']:
        print_recommendations(data)
    
    if args.section in ['all', 'comparison']:
        print_shell_vs_python(data)
    
    print("\n" + "="*80)
    print("📄 Full Report: docs/analysis/branch_sync_architecture_report.md")
    print("📊 Diagrams: docs/analysis/branch_sync_diagrams.mermaid")
    print("💾 Raw Data: docs/analysis/branch_sync_architecture.json")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
