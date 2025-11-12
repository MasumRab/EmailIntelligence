"""
Reporting Engine for Validation Results

Generates comprehensive validation reports in multiple formats
with detailed analysis, metrics, and recommendations.

Features:
- Multi-format report generation (JSON, Markdown, HTML)
- Detailed validation metrics and analysis
- Executive summary generation
- Trend analysis and recommendations
- Performance benchmarking reports
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json
import structlog
import os

from .quick_validator import QuickValidator, QuickValidationResult
from .standard_validator import StandardValidator, StandardValidationResult
from .comprehensive_validator import ComprehensiveValidator, ComprehensiveValidationResult

logger = structlog.get_logger()


@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    report_id: str
    report_type: str
    timestamp: str
    validation_level: str
    overall_summary: Dict[str, Any]
    detailed_results: Dict[str, Any]
    metrics_summary: Dict[str, Any]
    recommendations: List[str]
    quality_gates: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    executive_summary: str


class ValidationReportingEngine:
    """
    Comprehensive validation reporting engine
    
    Generates detailed reports for all validation levels with
    executive summaries, detailed analysis, and actionable recommendations.
    """
    
    def __init__(self, output_directory: str = "validation_reports"):
        """Initialize reporting engine"""
        self.output_directory = output_directory
        self.quick_validator = QuickValidator()
        self.standard_validator = StandardValidator()
        self.comprehensive_validator = ComprehensiveValidator()
        
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        logger.info(f"Validation reporting engine initialized, output: {output_directory}")
    
    def generate_quick_validation_report(
        self,
        validation_result: QuickValidationResult,
        conflict_context: Dict[str, Any],
        output_format: str = "json"
    ) -> str:
        """
        Generate quick validation report
        
        Args:
            validation_result: Quick validation result
            conflict_context: Conflict context information
            output_format: Output format (json, markdown, html)
        
        Returns:
            Path to generated report file
        """
        
        try:
            # Generate report ID
            report_id = f"quick_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create comprehensive report data
            report_data = ValidationReport(
                report_id=report_id,
                report_type="quick_validation",
                timestamp=datetime.now().isoformat(),
                validation_level="quick",
                overall_summary={
                    "status": validation_result.status.value,
                    "overall_score": validation_result.overall_score,
                    "resolution_readiness": validation_result.resolution_readiness,
                    "validation_time": validation_result.validation_time
                },
                detailed_results={
                    "basic_checks": validation_result.basic_checks,
                    "quick_issues": validation_result.quick_issues,
                    "validation_statistics": self.quick_validator.get_validation_statistics()
                },
                metrics_summary={
                    "validation_level": "Quick (Basic)",
                    "focus": "Essential conflict resolution validation",
                    "typical_use_case": "Iterative development, quick feedback",
                    "computational_overhead": "Minimal"
                },
                recommendations=validation_result.recommendations,
                quality_gates={
                    "focus": "Basic validation gates",
                    "gates_passed": sum(1 for check in validation_result.basic_checks.values() if check.get("passed", False)),
                    "total_gates": len(validation_result.basic_checks)
                },
                performance_metrics=self.quick_validator.get_performance_metrics(),
                risk_assessment={
                    "level": "Low",
                    "description": "Quick validation with minimal risk assessment"
                },
                executive_summary=self._generate_quick_executive_summary(validation_result)
            )
            
            # Generate report in requested format
            report_path = self._generate_report_file(
                report_data, output_format, report_id
            )
            
            logger.info(f"Quick validation report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error("Failed to generate quick validation report", error=str(e))
            raise
    
    def generate_standard_validation_report(
        self,
        validation_result: StandardValidationResult,
        conflict_context: Dict[str, Any],
        constitutional_context: Optional[Dict[str, Any]] = None,
        output_format: str = "json"
    ) -> str:
        """
        Generate standard validation report
        
        Args:
            validation_result: Standard validation result
            conflict_context: Conflict context information
            constitutional_context: Optional constitutional context
            output_format: Output format (json, markdown, html)
        
        Returns:
            Path to generated report file
        """
        
        try:
            # Generate report ID
            report_id = f"standard_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create comprehensive report data
            report_data = ValidationReport(
                report_id=report_id,
                report_type="standard_validation",
                timestamp=datetime.now().isoformat(),
                validation_level="standard",
                overall_summary={
                    "status": validation_result.status.value,
                    "overall_score": validation_result.overall_score,
                    "constitutional_score": validation_result.constitutional_score,
                    "feature_preservation_score": validation_result.feature_preservation_score,
                    "readiness_assessment": validation_result.readiness_assessment,
                    "validation_time": validation_result.validation_time
                },
                detailed_results={
                    "compliance_issues": validation_result.compliance_issues,
                    "preservation_issues": validation_result.preservation_issues,
                    "basic_validation_inherited": validation_result.overall_score,  # Simplified
                    "constitutional_analysis": self._format_constitutional_context(constitutional_context),
                    "validation_statistics": self.standard_validator.get_standard_validation_statistics()
                },
                metrics_summary={
                    "validation_level": "Standard (Constitutional + Preservation)",
                    "focus": "Constitutional compliance and feature preservation",
                    "typical_use_case": "Standard resolution validation",
                    "computational_overhead": "Moderate"
                },
                recommendations=validation_result.recommendations,
                quality_gates=validation_result.quality_gates,
                performance_metrics={
                    "constitutional_compliance_rate": validation_result.constitutional_score,
                    "feature_preservation_rate": validation_result.feature_preservation_score,
                    "overall_quality_rate": validation_result.overall_score
                },
                risk_assessment={
                    "level": "Medium",
                    "constitutional_risk": 1.0 - validation_result.constitutional_score,
                    "preservation_risk": 1.0 - validation_result.feature_preservation_score,
                    "overall_risk": 1.0 - validation_result.overall_score
                },
                executive_summary=self._generate_standard_executive_summary(validation_result)
            )
            
            # Generate report in requested format
            report_path = self._generate_report_file(
                report_data, output_format, report_id
            )
            
            logger.info(f"Standard validation report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error("Failed to generate standard validation report", error=str(e))
            raise
    
    def generate_comprehensive_validation_report(
        self,
        validation_result: ComprehensiveValidationResult,
        conflict_context: Dict[str, Any],
        constitutional_context: Optional[Dict[str, Any]] = None,
        performance_context: Optional[Dict[str, Any]] = None,
        output_format: str = "json"
    ) -> str:
        """
        Generate comprehensive validation report
        
        Args:
            validation_result: Comprehensive validation result
            conflict_context: Conflict context information
            constitutional_context: Optional constitutional context
            performance_context: Optional performance context
            output_format: Output format (json, markdown, html)
        
        Returns:
            Path to generated report file
        """
        
        try:
            # Generate report ID
            report_id = f"comprehensive_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create comprehensive report data
            report_data = ValidationReport(
                report_id=report_id,
                report_type="comprehensive_validation",
                timestamp=datetime.now().isoformat(),
                validation_level="comprehensive",
                overall_summary={
                    "status": validation_result.status.value,
                    "overall_score": validation_result.overall_score,
                    "workflow_score": validation_result.workflow_score,
                    "performance_score": validation_result.performance_score,
                    "execution_readiness": validation_result.execution_readiness,
                    "deployment_readiness": validation_result.deployment_readiness,
                    "validation_time": validation_result.validation_time
                },
                detailed_results={
                    "critical_issues": validation_result.critical_issues,
                    "workflow_validation": validation_result.workflow_validation,
                    "performance_benchmarks": validation_result.performance_benchmarks,
                    "quality_metrics": validation_result.quality_metrics,
                    "validation_statistics": self.comprehensive_validator.get_comprehensive_validation_statistics()
                },
                metrics_summary={
                    "validation_level": "Comprehensive (Full Workflow + Performance)",
                    "focus": "Complete resolution quality assurance",
                    "typical_use_case": "Production deployment, critical systems",
                    "computational_overhead": "High"
                },
                recommendations=validation_result.recommendations,
                quality_gates=validation_result.quality_gates,
                performance_metrics=self._format_performance_context(performance_context),
                risk_assessment={
                    "level": "Comprehensive",
                    "risk_factors": validation_result.workflow_validation.get("risk_factors", {}),
                    "mitigation_effectiveness": validation_result.performance_benchmarks.get("mitigation_effectiveness", 0.0),
                    "overall_risk_score": 1.0 - validation_result.overall_score
                },
                executive_summary=self._generate_comprehensive_executive_summary(validation_result)
            )
            
            # Generate report in requested format
            report_path = self._generate_report_file(
                report_data, output_format, report_id
            )
            
            logger.info(f"Comprehensive validation report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error("Failed to generate comprehensive validation report", error=str(e))
            raise
    
    def generate_comparative_validation_report(
        self,
        validation_results: List[Any],
        report_title: str = "Comparative Validation Analysis",
        output_format: str = "markdown"
    ) -> str:
        """
        Generate comparative validation report across multiple results
        
        Args:
            validation_results: List of validation results to compare
            report_title: Title for the comparative report
            output_format: Output format (json, markdown, html)
        
        Returns:
            Path to generated report file
        """
        
        try:
            report_id = f"comparative_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze validation results
            comparative_analysis = self._analyze_validation_results(validation_results)
            
            # Generate comparative report data
            report_data = {
                "report_id": report_id,
                "report_type": "comparative_validation",
                "title": report_title,
                "timestamp": datetime.now().isoformat(),
                "overall_summary": {
                    "total_validations": len(validation_results),
                    "validation_types": [type(result).__name__ for result in validation_results],
                    "comparative_analysis": comparative_analysis
                },
                "detailed_comparison": self._generate_detailed_comparison(validation_results),
                "trend_analysis": self._generate_trend_analysis(validation_results),
                "recommendations": self._generate_comparative_recommendations(validation_results),
                "executive_summary": self._generate_comparative_executive_summary(comparative_analysis)
            }
            
            # Generate report in requested format
            report_path = self._generate_comparative_report_file(
                report_data, output_format, report_id, report_title
            )
            
            logger.info(f"Comparative validation report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error("Failed to generate comparative validation report", error=str(e))
            raise
    
    def _generate_report_file(
        self,
        report_data: ValidationReport,
        output_format: str,
        report_id: str
    ) -> str:
        """Generate report file in specified format"""
        
        filename = f"{report_id}.{output_format}"
        filepath = os.path.join(self.output_directory, filename)
        
        if output_format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(report_data), f, indent=2, ensure_ascii=False)
        
        elif output_format == "markdown":
            markdown_content = self._generate_markdown_report(report_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        
        elif output_format == "html":
            html_content = self._generate_html_report(report_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        return filepath
    
    def _generate_markdown_report(self, report_data: ValidationReport) -> str:
        """Generate markdown format report"""
        
        md_content = f"""# Validation Report: {report_data.report_type.replace('_', ' ').title()}

**Report ID:** {report_data.report_id}  
**Timestamp:** {report_data.timestamp}  
**Validation Level:** {report_data.validation_level}

---

## Executive Summary

{report_data.executive_summary}

---

## Overall Summary

| Metric | Value |
|--------|--------|
| Status | {report_data.overall_summary.get('status', 'Unknown')} |
| Overall Score | {report_data.overall_summary.get('overall_score', 0.0):.3f} |
| Validation Time | {report_data.overall_summary.get('validation_time', 0.0):.2f}s |
"""

        # Add level-specific metrics
        if report_data.validation_level == "standard":
            md_content += f"| Constitutional Score | {report_data.overall_summary.get('constitutional_score', 0.0):.3f} |\n"
            md_content += f"| Feature Preservation Score | {report_data.overall_summary.get('feature_preservation_score', 0.0):.3f} |\n"
            md_content += f"| Readiness Assessment | {report_data.overall_summary.get('readiness_assessment', 'Unknown')} |\n"
        elif report_data.validation_level == "comprehensive":
            md_content += f"| Workflow Score | {report_data.overall_summary.get('workflow_score', 0.0):.3f} |\n"
            md_content += f"| Performance Score | {report_data.overall_summary.get('performance_score', 0.0):.3f} |\n"
            md_content += f"| Execution Readiness | {report_data.overall_summary.get('execution_readiness', 'Unknown')} |\n"
            md_content += f"| Deployment Readiness | {report_data.overall_summary.get('deployment_readiness', 'Unknown')} |\n"

        md_content += "\n---\n\n## Recommendations\n\n"
        
        for i, recommendation in enumerate(report_data.recommendations, 1):
            md_content += f"{i}. {recommendation}\n"
        
        md_content += "\n---\n\n## Quality Gates\n\n"
        
        if isinstance(report_data.quality_gates, dict):
            md_content += "| Gate | Score | Threshold | Status |\n"
            md_content += "|------|-------|-----------|--------|\n"
            
            for gate_name, gate_data in report_data.quality_gates.items():
                if isinstance(gate_data, dict):
                    score = gate_data.get('score', 0.0)
                    threshold = gate_data.get('threshold', 0.0)
                    status = "✅ PASS" if gate_data.get('passed', False) else "❌ FAIL"
                    md_content += f"| {gate_name.replace('_', ' ').title()} | {score:.3f} | {threshold:.3f} | {status} |\n"
        
        md_content += "\n---\n\n## Detailed Analysis\n\n"
        
        # Add detailed results based on validation level
        if report_data.validation_level == "quick":
            md_content += "### Basic Checks\n\n"
            if isinstance(report_data.detailed_results.get('basic_checks'), dict):
                for check_name, check_result in report_data.detailed_results['basic_checks'].items():
                    status = "✅ PASS" if check_result.get('passed', False) else "❌ FAIL"
                    score = check_result.get('score', 0.0)
                    md_content += f"- **{check_name.replace('_', ' ').title()}**: {status} (Score: {score:.3f})\n"
        
        elif report_data.validation_level == "standard":
            md_content += "### Constitutional Compliance\n\n"
            for issue in report_data.detailed_results.get('compliance_issues', []):
                severity = issue.get('severity', 'unknown')
                description = issue.get('description', 'No description')
                md_content += f"- **{severity.upper()}**: {description}\n"
            
            md_content += "\n### Feature Preservation\n\n"
            for issue in report_data.detailed_results.get('preservation_issues', []):
                severity = issue.get('severity', 'unknown')
                description = issue.get('description', 'No description')
                md_content += f"- **{severity.upper()}**: {description}\n"
        
        elif report_data.validation_level == "comprehensive":
            md_content += "### Critical Issues\n\n"
            for issue in report_data.detailed_results.get('critical_issues', []):
                severity = issue.get('severity', 'unknown')
                description = issue.get('description', 'No description')
                md_content += f"- **{severity.upper()}**: {description}\n"
            
            md_content += "\n### Performance Benchmarks\n\n"
            benchmarks = report_data.detailed_results.get('performance_benchmarks', {})
            if isinstance(benchmarks.get('benchmarks'), dict):
                for component, result in benchmarks['benchmarks'].items():
                    actual = result.get('actual_time', 0.0)
                    target = result.get('target_time', 0.0)
                    passed = "✅ PASS" if result.get('passed', False) else "❌ FAIL"
                    md_content += f"- **{component.title()}**: {passed} ({actual:.2f}s / {target:.2f}s)\n"
        
        md_content += "\n---\n\n"
        md_content += f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n"
        
        return md_content
    
    def _generate_html_report(self, report_data: ValidationReport) -> str:
        """Generate HTML format report"""
        
        # Basic HTML template with embedded styles
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validation Report - {report_data.report_type.replace('_', ' ').title()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .summary-card {{ background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
        .score {{ font-size: 2em; font-weight: bold; color: #333; }}
        .status-pass {{ color: #28a745; }}
        .status-warning {{ color: #ffc107; }}
        .status-fail {{ color: #dc3545; }}
        .recommendations {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .gates-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .gates-table th, .gates-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .gates-table th {{ background-color: #f2f2f2; }}
        .executive-summary {{ background: #e9ecef; padding: 20px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Validation Report: {report_data.report_type.replace('_', ' ').title()}</h1>
        <p><strong>Report ID:</strong> {report_data.report_id}</p>
        <p><strong>Timestamp:</strong> {report_data.timestamp}</p>
        <p><strong>Validation Level:</strong> {report_data.validation_level.title()}</p>
    </div>
    
    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <p>{report_data.executive_summary}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Overall Score</h3>
            <div class="score">{report_data.overall_summary.get('overall_score', 0.0):.3f}</div>
        </div>
        <div class="summary-card">
            <h3>Status</h3>
            <div class="status-{report_data.overall_summary.get('status', 'unknown').lower()}">
                {report_data.overall_summary.get('status', 'Unknown').upper()}
            </div>
        </div>
        <div class="summary-card">
            <h3>Validation Time</h3>
            <div>{report_data.overall_summary.get('validation_time', 0.0):.2f}s</div>
        </div>
    </div>
    
    <div class="recommendations">
        <h2>Recommendations</h2>
        <ul>
"""

        for recommendation in report_data.recommendations:
            html_content += f"            <li>{recommendation}</li>\n"

        html_content += """        </ul>
    </div>
    
    <h2>Quality Gates</h2>
    <table class="gates-table">
        <thead>
            <tr>
                <th>Gate</th>
                <th>Score</th>
                <th>Threshold</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
"""

        if isinstance(report_data.quality_gates, dict):
            for gate_name, gate_data in report_data.quality_gates.items():
                if isinstance(gate_data, dict):
                    score = gate_data.get('score', 0.0)
                    threshold = gate_data.get('threshold', 0.0)
                    status = "✅ PASS" if gate_data.get('passed', False) else "❌ FAIL"
                    html_content += f"""            <tr>
                <td>{gate_name.replace('_', ' ').title()}</td>
                <td>{score:.3f}</td>
                <td>{threshold:.3f}</td>
                <td>{status}</td>
            </tr>
"""

        html_content += """        </tbody>
    </table>
    
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p><em>Report generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """ UTC</em></p>
    </footer>
</body>
</html>"""
        
        return html_content
    
    # Executive summary generation methods
    def _generate_quick_executive_summary(self, result: QuickValidationResult) -> str:
        """Generate executive summary for quick validation"""
        
        if result.overall_score >= 0.8:
            status_desc = "excellent"
        elif result.overall_score >= 0.6:
            status_desc = "good"
        else:
            status_desc = "needs improvement"
        
        summary = f"""This quick validation assessment indicates {status_desc} readiness for conflict resolution with an overall score of {result.overall_score:.3f}.

The resolution is {result.resolution_readiness.replace('_', ' ')} for implementation. Key findings include:

"""
        
        if result.quick_issues:
            summary += f"- {len(result.quick_issues)} areas identified for improvement\n"
        
        summary += f"- Validation completed in {result.validation_time:.2f} seconds\n"
        
        if result.recommendations:
            summary += f"- {len(result.recommendations)} specific recommendations provided\n"
        
        return summary
    
    def _generate_standard_executive_summary(self, result: StandardValidationResult) -> str:
        """Generate executive summary for standard validation"""
        
        const_score = result.constitutional_score
        preserv_score = result.feature_preservation_score
        
        if const_score >= 0.8 and preserv_score >= 0.8:
            status_desc = "strong"
        elif const_score >= 0.7 and preserv_score >= 0.7:
            status_desc = "adequate"
        else:
            status_desc = "requires attention"
        
        summary = f"""This standard validation assessment shows {status_desc} constitutional compliance and feature preservation capabilities with an overall score of {result.overall_score:.3f}.

Key metrics indicate:
- Constitutional compliance: {const_score:.3f} ({'✅ Compliant' if const_score >= 0.7 else '⚠️ Needs attention'})
- Feature preservation: {preserv_score:.3f} ({'✅ Adequate' if preserv_score >= 0.7 else '⚠️ Needs attention'})
- Resolution readiness: {result.readiness_assessment.replace('_', ' ').title()}

"""
        
        if result.compliance_issues:
            summary += f"- {len(result.compliance_issues)} constitutional compliance issues identified\n"
        
        if result.preservation_issues:
            summary += f"- {len(result.preservation_issues)} feature preservation concerns identified\n"
        
        summary += f"- Validation completed in {result.validation_time:.2f} seconds\n"
        
        return summary
    
    def _generate_comprehensive_executive_summary(self, result: ComprehensiveValidationResult) -> str:
        """Generate executive summary for comprehensive validation"""
        
        workflow_score = result.workflow_score
        perf_score = result.performance_score
        
        if result.overall_score >= 0.9:
            status_desc = "production-ready"
        elif result.overall_score >= 0.8:
            status_desc = "staging-ready"
        elif result.overall_score >= 0.7:
            status_desc = "development-ready"
        else:
            status_desc = "requires significant improvement"
        
        summary = f"""This comprehensive validation assessment indicates the resolution strategy is {status_desc} for deployment with an overall quality score of {result.overall_score:.3f}.

Assessment Summary:
- Overall Quality: {result.overall_score:.3f} ({'✅ Excellent' if result.overall_score >= 0.9 else '✅ Good' if result.overall_score >= 0.8 else '⚠️ Fair' if result.overall_score >= 0.7 else '❌ Poor'})
- Workflow Quality: {workflow_score:.3f}
- Performance Score: {perf_score:.3f}
- Execution Readiness: {result.execution_readiness.replace('_', ' ').title()}
- Deployment Readiness: {result.deployment_readiness.replace('_', ' ').title()}

"""
        
        if result.critical_issues:
            summary += f"- {len(result.critical_issues)} critical issues require immediate attention\n"
        
        summary += f"- Validation completed in {result.validation_time:.2f} seconds\n"
        
        if result.recommendations:
            summary += f"- {len(result.recommendations)} actionable recommendations provided\n"
        
        return summary
    
    # Comparative report generation methods
    def _analyze_validation_results(self, results: List[Any]) -> Dict[str, Any]:
        """Analyze validation results for comparative report"""
        
        if not results:
            return {}
        
        scores = []
        statuses = []
        types = []
        
        for result in results:
            if hasattr(result, 'overall_score'):
                scores.append(result.overall_score)
            if hasattr(result, 'status'):
                statuses.append(result.status.value)
            types.append(type(result).__name__)
        
        analysis = {
            "average_score": sum(scores) / len(scores) if scores else 0.0,
            "max_score": max(scores) if scores else 0.0,
            "min_score": min(scores) if scores else 0.0,
            "score_variance": self._calculate_variance(scores) if len(scores) > 1 else 0.0,
            "status_distribution": {status: statuses.count(status) for status in set(statuses)},
            "validation_types": list(set(types))
        }
        
        return analysis
    
    def _generate_detailed_comparison(self, results: List[Any]) -> List[Dict[str, Any]]:
        """Generate detailed comparison of validation results"""
        
        comparison_data = []
        
        for i, result in enumerate(results, 1):
            comparison_item = {
                "validation_number": i,
                "validation_type": type(result).__name__,
                "status": getattr(result, 'status', {}).value if hasattr(result, 'status') else "unknown",
                "overall_score": getattr(result, 'overall_score', 0.0),
                "validation_time": getattr(result, 'validation_time', 0.0)
            }
            
            # Add level-specific metrics
            if hasattr(result, 'constitutional_score'):
                comparison_item["constitutional_score"] = result.constitutional_score
            if hasattr(result, 'feature_preservation_score'):
                comparison_item["feature_preservation_score"] = result.feature_preservation_score
            if hasattr(result, 'workflow_score'):
                comparison_item["workflow_score"] = result.workflow_score
            if hasattr(result, 'performance_score'):
                comparison_item["performance_score"] = result.performance_score
            
            comparison_data.append(comparison_item)
        
        return comparison_data
    
    def _generate_trend_analysis(self, results: List[Any]) -> Dict[str, Any]:
        """Generate trend analysis across validation results"""
        
        if len(results) < 2:
            return {"trend": "insufficient_data", "message": "Need at least 2 results for trend analysis"}
        
        scores = [getattr(result, 'overall_score', 0.0) for result in results]
        
        # Simple trend calculation
        if len(scores) >= 3:
            # Check if scores are generally improving or declining
            recent_avg = sum(scores[-3:]) / 3
            earlier_avg = sum(scores[:-3]) / len(scores[:-3]) if len(scores) > 3 else scores[0]
            
            if recent_avg > earlier_avg + 0.05:
                trend = "improving"
                message = f"Scores showing improvement trend (recent: {recent_avg:.3f}, earlier: {earlier_avg:.3f})"
            elif recent_avg < earlier_avg - 0.05:
                trend = "declining"
                message = f"Scores showing declining trend (recent: {recent_avg:.3f}, earlier: {earlier_avg:.3f})"
            else:
                trend = "stable"
                message = f"Scores remaining stable (recent: {recent_avg:.3f}, earlier: {earlier_avg:.3f})"
        else:
            # For 2 results, just compare
            if scores[-1] > scores[0]:
                trend = "improving"
                message = f"Second validation shows improvement ({scores[0]:.3f} → {scores[-1]:.3f})"
            elif scores[-1] < scores[0]:
                trend = "declining"
                message = f"Second validation shows decline ({scores[0]:.3f} → {scores[-1]:.3f})"
            else:
                trend = "stable"
                message = "Scores remain consistent between validations"
        
        return {
            "trend": trend,
            "message": message,
            "score_progression": scores
        }
    
    def _generate_comparative_recommendations(self, results: List[Any]) -> List[str]:
        """Generate recommendations based on comparative analysis"""
        
        recommendations = []
        
        scores = [getattr(result, 'overall_score', 0.0) for result in results]
        
        if len(scores) > 1:
            score_variance = self._calculate_variance(scores)
            
            if score_variance > 0.1:
                recommendations.append("High variance in validation scores suggests inconsistent resolution quality")
                recommendations.append("Consider standardizing resolution approach to achieve more consistent results")
            
            if max(scores) - min(scores) > 0.2:
                recommendations.append("Significant range in validation scores indicates optimization opportunities")
                recommendations.append("Analyze highest-scoring approach for lessons learned")
        
        if any(getattr(result, 'status', {}).value == 'fail' for result in results):
            recommendations.append("Some validations failed quality gates - review and address failing criteria")
        
        return recommendations
    
    def _generate_comparative_executive_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate executive summary for comparative report"""
        
        avg_score = analysis.get('average_score', 0.0)
        total_validations = analysis.get('total_validations', 0)
        
        if avg_score >= 0.8:
            status_desc = "strong overall"
        elif avg_score >= 0.6:
            status_desc = "acceptable overall"
        else:
            status_desc = "requiring attention overall"
        
        summary = f"""Comparative analysis of {total_validations} validation results shows {status_desc} resolution quality with an average score of {avg_score:.3f}.

Key findings:
"""
        
        score_variance = analysis.get('score_variance', 0.0)
        if score_variance > 0.05:
            summary += f"- High variance ({score_variance:.3f}) indicates inconsistent quality\n"
        else:
            summary += f"- Consistent quality with low variance ({score_variance:.3f})\n"
        
        status_dist = analysis.get('status_distribution', {})
        pass_count = status_dist.get('pass', 0) + status_dist.get('warning', 0)
        summary += f"- {pass_count}/{total_validations} validations passed or showed warnings\n"
        
        return summary
    
    def _generate_comparative_report_file(self, report_data: Dict[str, Any], output_format: str, report_id: str, title: str) -> str:
        """Generate comparative report file"""
        
        filename = f"{report_id}.{output_format}"
        filepath = os.path.join(self.output_directory, filename)
        
        if output_format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        elif output_format == "markdown":
            md_content = f"# {title}\n\n"
            md_content += f"**Report ID:** {report_data['report_id']}\n"
            md_content += f"**Timestamp:** {report_data['timestamp']}\n\n"
            md_content += "## Executive Summary\n\n"
            md_content += f"{report_data['executive_summary']}\n\n"
            
            # Add comparative analysis
            analysis = report_data['overall_summary']['comparative_analysis']
            md_content += f"## Comparative Analysis\n\n"
            md_content += f"- Total Validations: {analysis.get('total_validations', 0)}\n"
            md_content += f"- Average Score: {analysis.get('average_score', 0.0):.3f}\n"
            md_content += f"- Score Variance: {analysis.get('score_variance', 0.0):.3f}\n"
            md_content += f"- Validation Types: {', '.join(analysis.get('validation_types', []))}\n\n"
            
            # Add detailed comparison table
            detailed = report_data['detailed_comparison']
            if detailed:
                md_content += "## Detailed Comparison\n\n"
                md_content += "| # | Type | Score | Status | Time |\n"
                md_content += "|---|------|-------|--------|------|\n"
                
                for item in detailed:
                    md_content += f"| {item['validation_number']} | {item['validation_type']} | {item['overall_score']:.3f} | {item['status']} | {item['validation_time']:.2f}s |\n"
            
            # Add trend analysis
            trend = report_data['trend_analysis']
            md_content += f"\n## Trend Analysis\n\n"
            md_content += f"- **Trend:** {trend['trend'].title()}\n"
            md_content += f"- **Analysis:** {trend['message']}\n\n"
            
            # Add recommendations
            recommendations = report_data['recommendations']
            md_content += "## Recommendations\n\n"
            for i, rec in enumerate(recommendations, 1):
                md_content += f"{i}. {rec}\n"
            
            md_content += f"\n\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
        
        else:
            raise ValueError(f"Unsupported output format for comparative report: {output_format}")
        
        return filepath
    
    # Utility methods
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _format_constitutional_context(self, constitutional_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Format constitutional context for reporting"""
        if not constitutional_context:
            return {"status": "not_provided"}
        return constitutional_context
    
    def _format_performance_context(self, performance_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Format performance context for reporting"""
        if not performance_context:
            return {"status": "not_provided"}
        return performance_context
    
    def get_reporting_statistics(self) -> Dict[str, Any]:
        """Get reporting engine statistics"""
        
        return {
            "output_directory": self.output_directory,
            "reports_generated": len(os.listdir(self.output_directory)) if os.path.exists(self.output_directory) else 0,
            "supported_formats": ["json", "markdown", "html"],
            "validation_levels_supported": ["quick", "standard", "comprehensive"]
        }