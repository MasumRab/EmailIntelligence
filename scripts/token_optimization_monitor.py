#!/usr/bin/env python3
"""
Token Optimization Monitor

Implements Constitution v1.3.0 Token Optimization Principle.
Monitors and optimizes token usage to minimize computational overhead and prevent waste.

Target: 30% improvement in token usage efficiency
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TokenUsageMetrics:
    """Represents token usage metrics for a single operation."""
    operation_type: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    efficiency_score: float
    context_size: int
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class OptimizationRecommendation:
    """Represents a token optimization recommendation."""
    operation_type: str
    current_efficiency: float
    potential_savings: int
    recommendation: str
    implementation_effort: str
    expected_impact: str


class TokenOptimizationMonitor:
    """Monitors and optimizes token usage across the system."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.usage_history: List[TokenUsageMetrics] = []
        self.baseline_efficiency = 0.75  # Target efficiency baseline
        self.optimization_target = 0.30  # 30% improvement target

    def record_token_usage(self, metrics: TokenUsageMetrics) -> None:
        """Record token usage metrics for analysis."""
        self.usage_history.append(metrics)

        # Keep only last 1000 records to prevent memory issues
        if len(self.usage_history) > 1000:
            self.usage_history = self.usage_history[-1000:]

    def analyze_efficiency_trends(self) -> Dict[str, Any]:
        """Analyze token efficiency trends over time."""
        if not self.usage_history:
            return {"status": "no_data", "message": "No token usage data recorded"}

        # Group by operation type
        operations = {}
        for metric in self.usage_history:
            op_type = metric.operation_type
            if op_type not in operations:
                operations[op_type] = []
            operations[op_type].append(metric)

        # Calculate efficiency metrics per operation type
        efficiency_analysis = {}
        for op_type, metrics in operations.items():
            total_tokens = sum(m.total_tokens for m in metrics)
            avg_efficiency = sum(m.efficiency_score for m in metrics) / len(metrics)
            context_sizes = [m.context_size for m in metrics]
            avg_context = sum(context_sizes) / len(context_sizes)

            efficiency_analysis[op_type] = {
                "total_operations": len(metrics),
                "total_tokens_used": total_tokens,
                "average_efficiency": avg_efficiency,
                "average_context_size": avg_context,
                "efficiency_trend": self._calculate_trend([m.efficiency_score for m in metrics[-10:]]),
                "context_trend": self._calculate_trend(context_sizes[-10:])
            }

        return {
            "status": "analyzed",
            "overall_efficiency": sum(ea["average_efficiency"] for ea in efficiency_analysis.values()) / len(efficiency_analysis),
            "total_operations": len(self.usage_history),
            "total_tokens_used": sum(m.total_tokens for m in self.usage_history),
            "operation_breakdown": efficiency_analysis,
            "efficiency_target_met": self._check_efficiency_target(efficiency_analysis)
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values."""
        if len(values) < 2:
            return "insufficient_data"

        # Simple linear trend calculation
        if len(values) >= 2:
            first_half = sum(values[:len(values)//2]) / len(values[:len(values)//2])
            second_half = sum(values[len(values)//2:]) / len(values[len(values)//2:])

            if second_half > first_half * 1.05:  # 5% improvement threshold
                return "improving"
            elif second_half < first_half * 0.95:  # 5% degradation threshold
                return "degrading"
            else:
                return "stable"

        return "unknown"

    def _check_efficiency_target(self, efficiency_analysis: Dict) -> bool:
        """Check if the 30% efficiency improvement target is met."""
        if not efficiency_analysis:
            return False

        overall_efficiency = sum(ea["average_efficiency"] for ea in efficiency_analysis.values()) / len(efficiency_analysis)

        # Target is 30% improvement over baseline
        target_efficiency = self.baseline_efficiency * (1 + self.optimization_target)

        return overall_efficiency >= target_efficiency

    def generate_optimization_recommendations(self) -> List[OptimizationRecommendation]:
        """Generate specific optimization recommendations."""
        recommendations = []
        analysis = self.analyze_efficiency_trends()

        if analysis["status"] != "analyzed":
            return recommendations

        for op_type, metrics in analysis["operation_breakdown"].items():
            efficiency = metrics["average_efficiency"]
            context_size = metrics["average_context_size"]

            # Context size optimization
            if context_size > 10000:  # Large context threshold
                potential_savings = int(context_size * 0.2)  # Estimate 20% reduction
                recommendations.append(OptimizationRecommendation(
                    operation_type=op_type,
                    current_efficiency=efficiency,
                    potential_savings=potential_savings,
                    recommendation="Implement context windowing or summarization to reduce context size",
                    implementation_effort="Medium",
                    expected_impact="High"
                ))

            # Efficiency optimization
            if efficiency < self.baseline_efficiency:
                potential_savings = int((self.baseline_efficiency - efficiency) * 1000)  # Token savings estimate
                recommendations.append(OptimizationRecommendation(
                    operation_type=op_type,
                    current_efficiency=efficiency,
                    potential_savings=potential_savings,
                    recommendation="Optimize prompts and reduce redundant information in context",
                    implementation_effort="Low",
                    expected_impact="Medium"
                ))

            # Trend-based recommendations
            if metrics["efficiency_trend"] == "degrading":
                recommendations.append(OptimizationRecommendation(
                    operation_type=op_type,
                    current_efficiency=efficiency,
                    potential_savings=500,  # Conservative estimate
                    recommendation="Review recent changes that may have reduced efficiency",
                    implementation_effort="Low",
                    expected_impact="Medium"
                ))

        return recommendations

    def simulate_optimization_impact(self) -> Dict[str, Any]:
        """Simulate the impact of implementing optimization recommendations."""
        recommendations = self.generate_optimization_recommendations()
        analysis = self.analyze_efficiency_trends()

        if analysis["status"] != "analyzed":
            return {"status": "no_data"}

        current_total_tokens = analysis["total_tokens_used"]
        estimated_savings = sum(rec.potential_savings for rec in recommendations)

        projected_tokens = current_total_tokens - estimated_savings
        projected_efficiency = (projected_tokens / current_total_tokens) * analysis["overall_efficiency"]

        return {
            "current_total_tokens": current_total_tokens,
            "estimated_savings": estimated_savings,
            "projected_total_tokens": projected_tokens,
            "savings_percentage": (estimated_savings / current_total_tokens) * 100,
            "projected_efficiency": projected_efficiency,
            "target_met_after_optimization": projected_efficiency >= (self.baseline_efficiency * (1 + self.optimization_target)),
            "recommendations_count": len(recommendations)
        }

    def generate_optimization_report(self) -> str:
        """Generate a comprehensive token optimization report."""
        report_lines = []
        report_lines.append("# Token Optimization Report")
        report_lines.append("")
        report_lines.append(f"**Generated**: {datetime.now().isoformat()}")
        report_lines.append(f"**Target**: {self.optimization_target * 100}% efficiency improvement")
        report_lines.append("")

        analysis = self.analyze_efficiency_trends()

        if analysis["status"] == "no_data":
            report_lines.append("## Status: No Token Usage Data")
            report_lines.append("No token usage metrics have been recorded yet.")
            report_lines.append("Begin monitoring by calling record_token_usage() with TokenUsageMetrics.")
            return "\n".join(report_lines)

        # Overall status
        report_lines.append("## Overall Status")
        target_met = analysis["efficiency_target_met"]
        report_lines.append(f"**Efficiency Target Met**: {'✅ YES' if target_met else '❌ NO'}")
        report_lines.append(f"**Overall Efficiency**: {analysis['overall_efficiency']:.3f}")
        report_lines.append(f"**Target Efficiency**: {self.baseline_efficiency * (1 + self.optimization_target):.3f}")
        report_lines.append(f"**Total Operations**: {analysis['total_operations']}")
        report_lines.append(f"**Total Tokens Used**: {analysis['total_tokens_used']:,}")
        report_lines.append("")

        # Operation breakdown
        report_lines.append("## Operation Breakdown")
        for op_type, metrics in analysis["operation_breakdown"].items():
            report_lines.append(f"### {op_type}")
            report_lines.append(f"- **Operations**: {metrics['total_operations']}")
            report_lines.append(f"- **Average Efficiency**: {metrics['average_efficiency']:.3f}")
            report_lines.append(f"- **Average Context Size**: {metrics['average_context_size']:.0f}")
            report_lines.append(f"- **Efficiency Trend**: {metrics['efficiency_trend']}")
            report_lines.append(f"- **Context Trend**: {metrics['context_trend']}")
            report_lines.append("")

        # Optimization recommendations
        recommendations = self.generate_optimization_recommendations()
        if recommendations:
            report_lines.append("## Optimization Recommendations")
            for i, rec in enumerate(recommendations, 1):
                report_lines.append(f"### Recommendation {i}: {rec.operation_type}")
                report_lines.append(f"- **Current Efficiency**: {rec.current_efficiency:.3f}")
                report_lines.append(f"- **Potential Savings**: {rec.potential_savings} tokens")
                report_lines.append(f"- **Implementation Effort**: {rec.implementation_effort}")
                report_lines.append(f"- **Expected Impact**: {rec.expected_impact}")
                report_lines.append(f"- **Action**: {rec.recommendation}")
                report_lines.append("")

        # Impact simulation
        impact = self.simulate_optimization_impact()
        if impact.get("status") != "no_data":
            report_lines.append("## Projected Impact")
            report_lines.append(f"- **Current Token Usage**: {impact['current_total_tokens']:,}")
            report_lines.append(f"- **Estimated Savings**: {impact['estimated_savings']:,} tokens")
            report_lines.append(f"- **Projected Usage**: {impact['projected_total_tokens']:,} tokens")
            report_lines.append(f"- **Savings Percentage**: {impact['savings_percentage']:.1f}%")
            report_lines.append(f"- **Target Met After Optimization**: {'✅ YES' if impact['target_met_after_optimization'] else '❌ NO'}")
            report_lines.append("")

        return "\n".join(report_lines)

    def export_metrics_to_json(self, output_path: Path) -> None:
        """Export token usage metrics to JSON file."""
        metrics_data = {
            "export_timestamp": datetime.now().isoformat(),
            "baseline_efficiency": self.baseline_efficiency,
            "optimization_target": self.optimization_target,
            "usage_history": [
                {
                    "operation_type": m.operation_type,
                    "input_tokens": m.input_tokens,
                    "output_tokens": m.output_tokens,
                    "total_tokens": m.total_tokens,
                    "efficiency_score": m.efficiency_score,
                    "context_size": m.context_size,
                    "timestamp": m.timestamp.isoformat(),
                    "metadata": m.metadata
                }
                for m in self.usage_history
            ]
        }

        with open(output_path, 'w') as f:
            json.dump(metrics_data, f, indent=2)


def main():
    """Main entry point for the token optimization monitor."""
    project_root = Path(__file__).parent.parent

    monitor = TokenOptimizationMonitor(project_root)

    # Add some sample data for demonstration
    sample_metrics = [
        TokenUsageMetrics(
            operation_type="task_analysis",
            input_tokens=1500,
            output_tokens=300,
            total_tokens=1800,
            efficiency_score=0.72,
            context_size=8000,
            timestamp=datetime.now() - timedelta(hours=2),
            metadata={"model": "claude-3", "task_id": "sample_1"}
        ),
        TokenUsageMetrics(
            operation_type="code_review",
            input_tokens=2200,
            output_tokens=150,
            total_tokens=2350,
            efficiency_score=0.68,
            context_size=12000,
            timestamp=datetime.now() - timedelta(hours=1),
            metadata={"model": "gpt-4", "task_id": "sample_2"}
        )
    ]

    for metric in sample_metrics:
        monitor.record_token_usage(metric)

    analysis = monitor.analyze_efficiency_trends()

    if analysis["efficiency_target_met"]:
        print("✅ Token optimization target met")
        sys.exit(0)
    else:
        print("❌ Token optimization target not met")
        print(".3f"        print("Run with --report for detailed analysis")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        project_root = Path(__file__).parent.parent
        monitor = TokenOptimizationMonitor(project_root)
        print(monitor.generate_optimization_report())
    else:
        main()