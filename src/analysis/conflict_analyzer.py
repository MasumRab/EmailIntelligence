"""
Conflict Analyzer

Implements conflict analysis and resolution strategy determination.
"""
from typing import List, Dict, Any
from src.core.conflict_models import Conflict, ConflictTypeExtended, RiskLevel
from src.git.conflict_detector import GitConflictDetector


class ConflictAnalyzer:
    """Analyzes conflicts and determines resolution strategies"""
    
    def __init__(self):
        self.conflict_detector = GitConflictDetector()
    
    def analyze_conflicts(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """Analyze a list of conflicts and provide insights"""
        analysis_results = {
            'total_conflicts': len(conflicts),
            'by_type': self._categorize_by_type(conflicts),
            'by_severity': self._categorize_by_severity(conflicts),
            'total_resolution_time': sum(c.estimated_resolution_time for c in conflicts),
            'critical_files': self._identify_critical_files(conflicts),
            'resolution_strategies': self._determine_strategies(conflicts)
        }
        
        return analysis_results
    
    def _categorize_by_type(self, conflicts: List[Conflict]) -> Dict[str, int]:
        """Categorize conflicts by type"""
        type_counts = {}
        for conflict in conflicts:
            conflict_type = conflict.conflict_type.value
            type_counts[conflict_type] = type_counts.get(conflict_type, 0) + 1
        return type_counts
    
    def _categorize_by_severity(self, conflicts: List[Conflict]) -> Dict[str, int]:
        """Categorize conflicts by severity"""
        severity_counts = {}
        for conflict in conflicts:
            severity = conflict.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    def _identify_critical_files(self, conflicts: List[Conflict]) -> List[str]:
        """Identify critical files that appear in multiple conflicts"""
        file_counts = {}
        for conflict in conflicts:
            file_counts[conflict.file_path] = file_counts.get(conflict.file_path, 0) + 1
        
        # Return files that appear more than once
        return [file_path for file_path, count in file_counts.items() if count > 1]
    
    def _determine_strategies(self, conflicts: List[Conflict]) -> Dict[str, str]:
        """Determine resolution strategies for each conflict"""
        strategies = {}
        for conflict in conflicts:
            strategy = self._determine_single_strategy(conflict)
            strategies[conflict.file_path] = strategy
        return strategies
    
    def _determine_single_strategy(self, conflict: Conflict) -> str:
        """Determine resolution strategy for a single conflict"""
        if conflict.conflict_type == ConflictTypeExtended.ARCHITECTURAL:
            return "architectural_review"
        elif conflict.conflict_type == ConflictTypeExtended.SEMANTIC:
            return "semantic_merge"
        elif conflict.conflict_type == ConflictTypeExtended.BINARY:
            return "manual_resolution"
        elif conflict.severity == RiskLevel.CRITICAL:
            return "expert_review"
        else:
            return "standard_merge"
    
    def generate_resolution_report(self, conflicts: List[Conflict]) -> str:
        """Generate a human-readable resolution report"""
        analysis = self.analyze_conflicts(conflicts)
        
        report_lines = [
            "# Conflict Resolution Report",
            "",
            f"## Summary",
            f"- Total Conflicts: {analysis['total_conflicts']}",
            f"- Estimated Resolution Time: {analysis['total_resolution_time']} minutes",
            "",
            f"## By Type",
        ]
        
        for conflict_type, count in analysis['by_type'].items():
            report_lines.append(f"- {conflict_type}: {count}")
        
        report_lines.extend([
            "",
            f"## By Severity",
        ])
        
        for severity, count in analysis['by_severity'].items():
            report_lines.append(f"- {severity}: {count}")
        
        if analysis['critical_files']:
            report_lines.extend([
                "",
                f"## Critical Files",
            ])
            for file_path in analysis['critical_files']:
                report_lines.append(f"- {file_path}")
        
        report_lines.extend([
            "",
            f"## Resolution Strategies",
        ])
        
        for file_path, strategy in analysis['resolution_strategies'].items():
            report_lines.append(f"- {file_path}: {strategy}")
        
        return "\n".join(report_lines)