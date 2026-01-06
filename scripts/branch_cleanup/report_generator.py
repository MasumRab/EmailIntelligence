#!/usr/bin/env python3
"""
Report Generator for Branch Cleanup Operations

Comprehensive reporting system including HTML, JSON, and text reports
with detailed operation summaries and analytics.
"""

import json
import subprocess
from pathlib import Path

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

class OperationType(Enum):
    DELETE = "delete"
    MERGE = "merge"
    REBASE = "rebase"
    ARCHIVE = "archive"
    RENAME = "rename"
    SYNC = "sync"

class OperationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW_REQUIRED = "review_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"

@dataclass
class BranchOperation:
    operation_id: str
    branch_name: str
    operation_type: OperationType
    target_branch: str = None
    priority: str = "normal"
    reason: str = ""
    metadata: dict = None
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    error_message: str = None
    rollback_available: bool = False

@dataclass
class CleanupPlan:
    plan_id: str
    name: str
    description: str
    operations: list = None
    created_at: datetime = None
    status: str = "draft"
    reviewed: bool = False
    approved: bool = False
    executed: bool = False
    rollback_available: bool = False


@dataclass
class ReportMetrics:
    """Metrics for cleanup operations."""
    total_operations: int = 0
    completed_operations: int = 0
    failed_operations: int = 0
    deleted_branches: int = 0
    merged_branches: int = 0
    archived_branches: int = 0
    unique_commits_preserved: int = 0
    unique_commits_lost: int = 0
    execution_time_seconds: float = 0.0


class ReportGenerator:
    """Comprehensive report generation for branch cleanup."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.reports_dir = self.repo_path / "reports" / "branch_cleanup"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_plan_report(self, plan: CleanupPlan, format: str = "html") -> str:
        """Generate comprehensive report for cleanup plan."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cleanup_report_{plan.plan_id}_{timestamp}"
        
        if format.lower() == "html":
            filepath = self._generate_html_report(plan, filename)
        elif format.lower() == "json":
            filepath = self._generate_json_report(plan, filename)
        elif format.lower() == "text":
            filepath = self._generate_text_report(plan, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return str(filepath)
    
    def _generate_html_report(self, plan: CleanupPlan, filename: str) -> Path:
        """Generate HTML report."""
        filepath = self.reports_dir / f"{filename}.html"
        
        # Calculate metrics
        metrics = self._calculate_metrics(plan)
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Branch Cleanup Report - {plan.name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 2px solid #e1e5e9;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .metric-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .operations {{
            margin-top: 30px;
        }}
        .operation {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #28a745;
        }}
        .operation.delete {{ border-left-color: #dc3545; }}
        .operation.merge {{ border-left-color: #28a745; }}
        .operation.archive {{ border-left-color: #ffc107; }}
        .operation.failed {{ border-left-color: #dc3545; }}
        .operation.pending {{ border-left-color: #6c757d; }}
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-completed {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
        .status-pending {{ background: #e2e3e5; color: #383d41; }}
        .status-in_progress {{ background: #cce5ff; color: #004085; }}
        .priority-high {{ color: #dc3545; }}
        .priority-normal {{ color: #6c757d; }}
        .priority-low {{ color: #28a745; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #f8f9fa;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Branch Cleanup Report</h1>
            <h2>{plan.name}</h2>
            <p><strong>Plan ID:</strong> {plan.plan_id}</p>
            <p><strong>Description:</strong> {plan.description}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Status:</strong> <span class="status-badge status-{plan.status}">{plan.status}</span></p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{metrics.total_operations}</div>
                <div class="metric-label">Total Operations</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.completed_operations}</div>
                <div class="metric-label">Completed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.failed_operations}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.deleted_branches}</div>
                <div class="metric-label">Branches Deleted</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.merged_branches}</div>
                <div class="metric-label">Branches Merged</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics.archived_branches}</div>
                <div class="metric-label">Branches Archived</div>
            </div>
        </div>

        <div class="operations">
            <h3>Operations Details</h3>
            {self._generate_operations_table(plan.operations)}
        </div>

        <div class="footer">
            <p>Report generated by Branch Cleanup Manager</p>
            <p>Repository: {self.repo_path}</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_operations_table(self, operations: List[BranchOperation]) -> str:
        """Generate operations table HTML."""
        rows = []
        for op in operations:
            status_class = f"status-{op.status.value}"
            priority_class = f"priority-{op.priority}"
            op_class = op.operation_type.value
            
            duration = ""
            if op.started_at and op.completed_at:
                duration = str(op.completed_at - op.started_at).split('.')[0]
            
            error_info = ""
            if op.error_message:
                error_info = f'<br><small style="color: #dc3545;">Error: {op.error_message}</small>'
            
            row = f"""
            <tr class="operation {op_class}">
                <td>{op.branch_name}</td>
                <td><span class="status-badge {status_class}">{op.status.value}</span></td>
                <td>{op.operation_type.value}</td>
                <td class="{priority_class}">{op.priority}</td>
                <td>{op.reason}</td>
                <td>{duration}</td>
                <td>{op.target_branch or '-'}{error_info}</td>
            </tr>
            """
            rows.append(row)
        
        return f"""
        <table>
            <thead>
                <tr>
                    <th>Branch</th>
                    <th>Status</th>
                    <th>Operation</th>
                    <th>Priority</th>
                    <th>Reason</th>
                    <th>Duration</th>
                    <th>Target/Error</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
    
    def _generate_json_report(self, plan: CleanupPlan, filename: str) -> Path:
        """Generate JSON report."""
        filepath = self.reports_dir / f"{filename}.json"
        
        # Convert to serializable format
        report_data = {
            "report_info": {
                "plan_id": plan.plan_id,
                "plan_name": plan.name,
                "description": plan.description,
                "generated_at": datetime.now().isoformat(),
                "status": plan.status,
                "reviewed": plan.reviewed,
                "approved": plan.approved,
                "executed": plan.executed
            },
            "metrics": asdict(self._calculate_metrics(plan)),
            "operations": [
                {
                    "operation_id": op.operation_id,
                    "branch_name": op.branch_name,
                    "operation_type": op.operation_type.value,
                    "target_branch": op.target_branch,
                    "priority": op.priority,
                    "reason": op.reason,
                    "status": op.status.value,
                    "created_at": op.created_at.isoformat(),
                    "started_at": op.started_at.isoformat() if op.started_at else None,
                    "completed_at": op.completed_at.isoformat() if op.completed_at else None,
                    "error_message": op.error_message,
                    "rollback_available": op.rollback_available,
                    "metadata": op.metadata
                }
                for op in plan.operations
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return filepath
    
    def _generate_text_report(self, plan: CleanupPlan, filename: str) -> Path:
        """Generate text report."""
        filepath = self.reports_dir / f"{filename}.txt"
        
        metrics = self._calculate_metrics(plan)
        
        lines = [
            "=" * 80,
            "BRANCH CLEANUP REPORT",
            "=" * 80,
            f"Plan Name: {plan.name}",
            f"Plan ID: {plan.plan_id}",
            f"Description: {plan.description}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Status: {plan.status}",
            f"Reviewed: {plan.reviewed}",
            f"Approved: {plan.approved}",
            f"Executed: {plan.executed}",
            "",
            "METRICS",
            "-" * 40,
            f"Total Operations: {metrics.total_operations}",
            f"Completed: {metrics.completed_operations}",
            f"Failed: {metrics.failed_operations}",
            f"Branches Deleted: {metrics.deleted_branches}",
            f"Branches Merged: {metrics.merged_branches}",
            f"Branches Archived: {metrics.archived_branches}",
            f"Unique Commits Preserved: {metrics.unique_commits_preserved}",
            f"Unique Commits Lost: {metrics.unique_commits_lost}",
            f"Execution Time: {metrics.execution_time_seconds:.2f} seconds",
            "",
            "OPERATIONS",
            "-" * 40,
        ]
        
        for i, op in enumerate(plan.operations, 1):
            lines.extend([
                f"{i}. {op.branch_name}",
                f"   Operation: {op.operation_type.value}",
                f"   Status: {op.status.value}",
                f"   Priority: {op.priority}",
                f"   Reason: {op.reason}",
                f"   Target: {op.target_branch or 'N/A'}",
            ])
            
            if op.started_at and op.completed_at:
                duration = op.completed_at - op.started_at
                lines.append(f"   Duration: {duration}")
            
            if op.error_message:
                lines.append(f"   Error: {op.error_message}")
            
            lines.append("")
        
        lines.extend([
            "=" * 80,
            f"Repository: {self.repo_path}",
            f"Report generated by Branch Cleanup Manager",
            "=" * 80
        ])
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        
        return filepath
    
    def _calculate_metrics(self, plan: CleanupPlan) -> ReportMetrics:
        """Calculate operation metrics."""
        metrics = ReportMetrics()
        
        metrics.total_operations = len(plan.operations)
        
        # Count by status
        for op in plan.operations:
            if op.status == OperationStatus.COMPLETED:
                metrics.completed_operations += 1
            elif op.status == OperationStatus.FAILED:
                metrics.failed_operations += 1
            
            # Count by operation type
            if op.operation_type == OperationType.DELETE and op.status == OperationStatus.COMPLETED:
                metrics.deleted_branches += 1
            elif op.operation_type == OperationType.MERGE and op.status == OperationStatus.COMPLETED:
                metrics.merged_branches += 1
            elif op.operation_type == OperationType.ARCHIVE and op.status == OperationStatus.COMPLETED:
                metrics.archived_branches += 1
        
        # Calculate execution time
        if plan.operations:
            start_times = [op.started_at for op in plan.operations if op.started_at]
            end_times = [op.completed_at for op in plan.operations if op.completed_at]
            
            if start_times and end_times:
                total_time = (max(end_times) - min(start_times)).total_seconds()
                metrics.execution_time_seconds = total_time
        
        # Count unique commits
        for op in plan.operations:
            if op.operation_type == OperationType.DELETE:
                unique_count = self._count_unique_commits(op.branch_name)
                if op.status == OperationStatus.COMPLETED:
                    metrics.unique_commits_lost += unique_count
                else:
                    metrics.unique_commits_preserved += unique_count
        
        return metrics
    
    def _count_unique_commits(self, branch_name: str) -> int:
        """Count unique commits on branch."""
        try:
            result = subprocess.run(
                ["git", "log", "main..{branch_name}", "--oneline"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return len(result.stdout.strip().splitlines())
        except subprocess.CalledProcessError:
            return 0
    
    def generate_summary_report(self, plans: List[CleanupPlan]) -> Path:
        """Generate summary report for multiple plans."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cleanup_summary_{timestamp}"
        filepath = self.reports_dir / f"{filename}.html"
        
        # Calculate overall metrics
        total_operations = sum(len(plan.operations) for plan in plans)
        total_completed = sum(
            len([op for op in plan.operations if op.status == OperationStatus.COMPLETED])
            for plan in plans
        )
        total_failed = sum(
            len([op for op in plan.operations if op.status == OperationStatus.FAILED])
            for plan in plans
        )
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Branch Cleanup Summary Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }}
        .summary-value {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .summary-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #f8f9fa;
            font-weight: bold;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-completed {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
        .status-draft {{ background: #e2e3e5; color: #383d41; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Branch Cleanup Summary Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="summary-card">
                <div class="summary-value">{len(plans)}</div>
                <div class="summary-label">Total Plans</div>
            </div>
            <div class="summary-card">
                <div class="summary-value">{total_operations}</div>
                <div class="summary-label">Total Operations</div>
            </div>
            <div class="summary-card">
                <div class="summary-value">{total_completed}</div>
                <div class="summary-label">Completed</div>
            </div>
            <div class="summary-card">
                <div class="summary-value">{total_failed}</div>
                <div class="summary-label">Failed</div>
            </div>
        </div>

        <h2>Plans Overview</h2>
        <table>
            <thead>
                <tr>
                    <th>Plan Name</th>
                    <th>Plan ID</th>
                    <th>Status</th>
                    <th>Operations</th>
                    <th>Completed</th>
                    <th>Failed</th>
                    <th>Created</th>
                </tr>
            </thead>
            <tbody>
                {''.join(self._generate_summary_rows(plans))}
            </tbody>
        </table>
    </div>
</body>
</html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_summary_rows(self, plans: List[CleanupPlan]) -> List[str]:
        """Generate summary table rows."""
        rows = []
        for plan in plans:
            completed = len([op for op in plan.operations if op.status == OperationStatus.COMPLETED])
            failed = len([op for op in plan.operations if op.status == OperationStatus.FAILED])
            
            row = f"""
            <tr>
                <td>{plan.name}</td>
                <td>{plan.plan_id}</td>
                <td><span class="status-badge status-{plan.status}">{plan.status}</span></td>
                <td>{len(plan.operations)}</td>
                <td>{completed}</td>
                <td>{failed}</td>
                <td>{plan.created_at.strftime('%Y-%m-%d')}</td>
            </tr>
            """
            rows.append(row)
        
        return rows