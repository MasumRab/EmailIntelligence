#!/usr/bin/env python3
"""
Context Contamination Prevention Monitor

Implements Constitution v1.3.0 Context Contamination Prevention Principle.
Monitors and prevents resource waste and security issues from information leakage
between different operational contexts.

Target: 95% reduction in identified context contamination points
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass


@dataclass
class ContextBoundary:
    """Represents a context boundary definition."""
    name: str
    allowed_patterns: List[str]
    blocked_patterns: List[str]
    context_type: str
    security_level: str


@dataclass
class ContaminationEvent:
    """Represents a detected contamination event."""
    source_context: str
    target_context: str
    resource_type: str
    severity: str
    description: str
    timestamp: str
    remediation_steps: List[str]


class ContextContaminationMonitor:
    """Monitors and prevents context contamination across the system."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.context_boundaries = self._define_context_boundaries()
        self.contamination_events: List[ContaminationEvent] = []

    def _define_context_boundaries(self) -> Dict[str, ContextBoundary]:
        """Define context boundaries based on orchestration architecture."""
        return {
            "orchestration_tools": ContextBoundary(
                name="orchestration_tools",
                allowed_patterns=[
                    "scripts/",
                    "setup/",
                    "docs/orchestration*",
                    ".flake8",
                    ".pylintrc",
                    ".gitignore",
                    "launch.py"
                ],
                blocked_patterns=[
                    "src/",
                    "backend/",
                    "modules/",
                    "tests/",
                    "node_modules/",
                    ".env"
                ],
                context_type="infrastructure",
                security_level="high"
            ),
            "application_code": ContextBoundary(
                name="application_code",
                allowed_patterns=[
                    "src/",
                    "backend/",
                    "modules/",
                    "client/",
                    "tests/",
                    "package.json",
                    "tsconfig.json"
                ],
                blocked_patterns=[
                    "scripts/",
                    ".taskmaster/",
                    ".env"
                ],
                context_type="application",
                security_level="medium"
            ),
            "local_environment": ContextBoundary(
                name="local_environment",
                allowed_patterns=[
                    ".env.example",
                    ".vscode/",
                    ".cursor/"
                ],
                blocked_patterns=[
                    ".env",
                    ".taskmaster/",
                    "credentials/",
                    "secrets/"
                ],
                context_type="environment",
                security_level="critical"
            )
        }

    def scan_for_contamination(self) -> Tuple[bool, List[ContaminationEvent]]:
        """Scan the codebase for context contamination issues.

        Returns:
            Tuple of (is_clean, contamination_events)
        """
        contamination_events = []

        # Check file placement violations
        file_violations = self._check_file_placement_violations()
        contamination_events.extend(file_violations)

        # Check import boundary violations
        import_violations = self._check_import_boundary_violations()
        contamination_events.extend(import_violations)

        # Check configuration leakage
        config_leakage = self._check_configuration_leakage()
        contamination_events.extend(config_leakage)

        # Check resource sharing violations
        resource_violations = self._check_resource_sharing_violations()
        contamination_events.extend(resource_violations)

        self.contamination_events = contamination_events
        is_clean = len(contamination_events) == 0

        return is_clean, contamination_events

    def _check_file_placement_violations(self) -> List[ContaminationEvent]:
        """Check for files placed in wrong contexts."""
        violations = []

        # Scan all files in the project
        for root, dirs, files in os.walk(self.project_root):
            # Skip version control and build directories
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.next']):
                continue

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)

                # Check against each context boundary
                for context_name, boundary in self.context_boundaries.items():
                    if self._file_violates_boundary(relative_path, boundary):
                        violation = ContaminationEvent(
                            source_context="unknown",
                            target_context=context_name,
                            resource_type="file",
                            severity=boundary.security_level,
                            description=f"File {relative_path} violates {context_name} boundary",
                            timestamp=self._get_timestamp(),
                            remediation_steps=[
                                f"Move file to appropriate context directory",
                                f"Update context boundary rules if placement is intentional",
                                f"Review file dependencies for contamination"
                            ]
                        )
                        violations.append(violation)

        return violations

    def _file_violates_boundary(self, file_path: Path, boundary: ContextBoundary) -> bool:
        """Check if a file violates a context boundary."""
        path_str = str(file_path)

        # Check blocked patterns first (higher priority)
        for blocked_pattern in boundary.blocked_patterns:
            if path_str.startswith(blocked_pattern) or blocked_pattern in path_str:
                # This file should NOT be in this context
                return True

        # Check allowed patterns
        for allowed_pattern in boundary.allowed_patterns:
            if path_str.startswith(allowed_pattern) or allowed_pattern in path_str:
                # This file is allowed in this context
                return False

        # If file doesn't match any patterns, it's a potential violation
        # depending on the context type
        if boundary.context_type == "infrastructure":
            # Infrastructure context should be restrictive
            return not any(pattern in path_str for pattern in ["scripts/", "setup/", "docs/"])

        return False

    def _check_import_boundary_violations(self) -> List[ContaminationEvent]:
        """Check for import statements that cross context boundaries inappropriately."""
        violations = []

        # Scan Python files for imports
        for root, dirs, files in os.walk(self.project_root):
            if any(skip in root for skip in ['.git', '__pycache__', 'venv', 'node_modules']):
                continue

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()

                        relative_path = file_path.relative_to(self.project_root)

                        # Check for problematic imports
                        import_lines = [line.strip() for line in content.split('\n')
                                      if line.strip().startswith(('import ', 'from '))]

                        for import_line in import_lines:
                            if self._import_crosses_boundaries(import_line, str(relative_path)):
                                violation = ContaminationEvent(
                                    source_context=self._identify_context(str(relative_path)),
                                    target_context="cross-boundary",
                                    resource_type="import",
                                    severity="medium",
                                    description=f"Import boundary violation in {relative_path}: {import_line}",
                                    timestamp=self._get_timestamp(),
                                    remediation_steps=[
                                        "Review import necessity",
                                        "Consider interface abstraction",
                                        "Move shared code to appropriate context"
                                    ]
                                )
                                violations.append(violation)

                    except Exception as e:
                        # Skip files that can't be read
                        continue

        return violations

    def _import_crosses_boundaries(self, import_line: str, file_path: str) -> bool:
        """Check if an import crosses inappropriate context boundaries."""
        # This is a simplified check - in practice, this would need more sophisticated analysis
        if "orchestration" in import_line.lower() and "application" in file_path:
            return True
        if "application" in import_line.lower() and "orchestration" in file_path:
            return True
        return False

    def _check_configuration_leakage(self) -> List[ContaminationEvent]:
        """Check for configuration leakage between contexts."""
        violations = []

        # Check for .env files in wrong locations
        for root, dirs, files in os.walk(self.project_root):
            if '.env' in files and not str(root).endswith('project_root'):
                violation = ContaminationEvent(
                    source_context="environment",
                    target_context="unknown",
                    resource_type="configuration",
                    severity="critical",
                    description=f"Environment file found in wrong location: {root}/.env",
                    timestamp=self._get_timestamp(),
                    remediation_steps=[
                        "Move .env file to project root",
                        "Ensure .env is in .gitignore",
                        "Review exposed configuration"
                    ]
                )
                violations.append(violation)

        return violations

    def _check_resource_sharing_violations(self) -> List[ContaminationEvent]:
        """Check for inappropriate resource sharing between contexts."""
        violations = []

        # This would check for shared databases, caches, etc.
        # Simplified implementation for now

        return violations

    def _identify_context(self, file_path: str) -> str:
        """Identify which context a file belongs to."""
        if any(pattern in file_path for pattern in ['scripts/', 'setup/', 'docs/orchestration']):
            return "orchestration_tools"
        elif any(pattern in file_path for pattern in ['src/', 'backend/', 'tests/']):
            return "application_code"
        else:
            return "unknown"

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def generate_contamination_report(self) -> str:
        """Generate a detailed contamination report."""
        report_lines = []
        report_lines.append("# Context Contamination Prevention Report")
        report_lines.append("")

        is_clean, events = self.scan_for_contamination()

        report_lines.append("## Overall Status")
        report_lines.append(f"Status: {'✅ CLEAN' if is_clean else '❌ CONTAMINATED'}")
        report_lines.append(f"Contamination Events: {len(events)}")
        report_lines.append("")

        if events:
            report_lines.append("## Contamination Events")
            for i, event in enumerate(events, 1):
                report_lines.append(f"### Event {i}: {event.description}")
                report_lines.append(f"- **Severity**: {event.severity}")
                report_lines.append(f"- **Resource Type**: {event.resource_type}")
                report_lines.append(f"- **Source Context**: {event.source_context}")
                report_lines.append(f"- **Target Context**: {event.target_context}")
                report_lines.append(f"- **Timestamp**: {event.timestamp}")
                report_lines.append("- **Remediation Steps**:")
                for step in event.remediation_steps:
                    report_lines.append(f"  - {step}")
                report_lines.append("")

        # Context boundary summary
        report_lines.append("## Context Boundaries Defined")
        for name, boundary in self.context_boundaries.items():
            report_lines.append(f"### {name} ({boundary.context_type})")
            report_lines.append(f"- **Security Level**: {boundary.security_level}")
            report_lines.append(f"- **Allowed Patterns**: {', '.join(boundary.allowed_patterns)}")
            report_lines.append(f"- **Blocked Patterns**: {', '.join(boundary.blocked_patterns)}")
            report_lines.append("")

        return "\n".join(report_lines)


def main():
    """Main entry point for the contamination monitor."""
    project_root = Path(__file__).parent.parent

    monitor = ContextContaminationMonitor(project_root)
    is_clean, events = monitor.scan_for_contamination()

    if is_clean:
        print("✅ No context contamination detected")
        sys.exit(0)
    else:
        print(f"❌ Context contamination detected: {len(events)} events")
        for event in events:
            print(f"  - {event.severity.upper()}: {event.description}")
        print("")
        print("Run with --report for detailed analysis")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        project_root = Path(__file__).parent.parent
        monitor = ContextContaminationMonitor(project_root)
        print(monitor.generate_contamination_report())
    else:
        main()