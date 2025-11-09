#!/usr/bin/env python3
"""
Documentation Maintenance and Health Check Script
Performs regular maintenance tasks and health checks on the documentation system.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse


class DocsMaintenance:
    """Documentation maintenance and health check system."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_path = project_root / "scripts" / "sync_config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def run_full_maintenance(self):
        """Run complete maintenance suite."""
        print("🔧 Running full documentation maintenance...")

        results = {}

        # Health checks
        results["health"] = self.check_system_health()

        # Cleanup tasks
        results["cleanup"] = self.perform_cleanup_tasks()

        # Integrity checks
        results["integrity"] = self.check_documentation_integrity()

        # Optimization
        results["optimization"] = self.optimize_storage()

        # Generate report
        self.generate_maintenance_report(results)

        print("✅ Maintenance completed")
        return results

    def check_system_health(self) -> Dict:
        """Check overall system health."""
        print("  📊 Checking system health...")

        health = {
            "worktrees_exist": True,
            "inheritance_base_exists": True,
            "sync_scripts_executable": True,
            "config_valid": True,
            "permissions_ok": True,
            "issues": [],
        }

        # Check worktrees
        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        for worktree in worktrees:
            worktree_path = self.project_root / "worktrees" / worktree
            if not worktree_path.exists():
                health["worktrees_exist"] = False
                health["issues"].append(f"Worktree missing: {worktree}")

        # Check inheritance base
        inheritance_base = self.project_root / "docs"
        if not inheritance_base.exists():
            health["inheritance_base_exists"] = False
            health["issues"].append("Inheritance base docs directory missing")

        # Check sync scripts
        sync_scripts = [
            "sync-common-docs.sh",
            "sync_common_docs.py",
            "auto_sync_docs.py",
        ]
        for script in sync_scripts:
            script_path = self.project_root / "scripts" / script
            if not script_path.exists():
                health["sync_scripts_executable"] = False
                health["issues"].append(f"Sync script missing: {script}")
            elif not os.access(script_path, os.X_OK) and script.endswith(".sh"):
                health["issues"].append(f"Script not executable: {script}")

        # Check config
        if not self.config:
            health["config_valid"] = False
            health["issues"].append("Configuration file missing or invalid")

        # Check permissions
        docs_dirs = []
        for worktree in worktrees:
            docs_dirs.extend(
                [
                    self.project_root
                    / "worktrees"
                    / worktree
                    / "docs"
                    / "common"
                    / "docs",
                    self.project_root
                    / "worktrees"
                    / worktree
                    / self.config.get("sync_rules", {})
                    .get("branch_docs_paths", {})
                    .get(worktree, f"docs/{worktree.split('-')[1]}"),
                ]
            )

        for docs_dir in docs_dirs:
            if docs_dir.exists() and not os.access(docs_dir, os.R_OK | os.W_OK):
                health["permissions_ok"] = False
                health["issues"].append(f"Permission issue: {docs_dir}")

        health["overall_status"] = "healthy" if not health["issues"] else "issues_found"
        return health

    def perform_cleanup_tasks(self) -> Dict:
        """Perform cleanup tasks."""
        print("  🧹 Performing cleanup tasks...")

        cleanup = {
            "old_backups_removed": 0,
            "temp_files_removed": 0,
            "empty_dirs_removed": 0,
            "cache_cleared": False,
            "misplaced_files_moved": 0,
        }

        # Clean old backups
        retention_days = self.config.get("conflict_resolution", {}).get(
            "backup_retention_days", 30
        )
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        common_path = self.config.get("sync_rules", {}).get(
            "common_docs_path", "docs/common/docs"
        )

        for worktree in worktrees:
            worktree_path = self.project_root / "worktrees" / worktree / common_path
            if worktree_path.exists():
                for backup_file in worktree_path.glob("*.backup_*"):
                    try:
                        parts = backup_file.name.split("_")
                        if len(parts) >= 2:
                            timestamp_str = parts[-1]
                            if len(timestamp_str) == 15:  # YYYYMMDD_HHMMSS
                                file_date = datetime.strptime(
                                    timestamp_str, "%Y%m%d_%H%M%S"
                                )
                            elif len(timestamp_str) == 13:  # YYMMDD_HHMMSS
                                file_date = datetime.strptime(
                                    timestamp_str, "%y%m%d_%H%M%S"
                                )
                            else:
                                continue

                            if file_date < cutoff_date:
                                backup_file.unlink()
                                cleanup["old_backups_removed"] += 1
                    except (ValueError, OSError):
                        continue

        # Clean temp files
        temp_patterns = ["*.tmp", "*.bak", ".DS_Store", "Thumbs.db"]
        for pattern in temp_patterns:
            for temp_file in self.project_root.rglob(pattern):
                if temp_file.is_file():
                    temp_file.unlink()
                    cleanup["temp_files_removed"] += 1

        # Remove empty directories
        def remove_empty_dirs(path: Path):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                cleanup["empty_dirs_removed"] += 1
                return True
            return False

        # Walk backwards to remove nested empty dirs
        for path in sorted(self.project_root.rglob("*"), reverse=True):
            remove_empty_dirs(path)

        # Clear Python cache
        for cache_dir in self.project_root.rglob("__pycache__"):
            if cache_dir.is_dir():
                shutil.rmtree(cache_dir)
                cleanup["cache_cleared"] = True

        # Move misplaced documentation files
        misplaced_files = self._find_misplaced_documentation()
        for misplaced_file in misplaced_files:
            if self._move_misplaced_file(misplaced_file):
                cleanup["misplaced_files_moved"] += 1

        return cleanup

    def check_documentation_integrity(self) -> Dict:
        """Check documentation integrity."""
        print("  🔍 Checking documentation integrity...")

        integrity = {
            "missing_files": [],
            "orphaned_files": [],
            "misplaced_files": [],
            "inconsistent_sync": [],
            "total_files_checked": 0,
            "integrity_score": 100,
        }

        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        inheritance_base = self.project_root / "docs"

        if not inheritance_base.exists():
            return integrity

        # Get all files from inheritance base
        base_files = set()
        for file_path in inheritance_base.rglob("*.md"):
            if file_path.is_file():
                relative_path = file_path.relative_to(inheritance_base)
                base_files.add(str(relative_path))
                integrity["total_files_checked"] += 1

        # Check each worktree
        for worktree in worktrees:
            worktree_path = self.project_root / "worktrees" / worktree
            common_docs_path = worktree_path / "docs" / "common" / "docs"

            if not common_docs_path.exists():
                integrity["missing_files"].append(f"Common docs missing in {worktree}")
                continue

            # Check common docs
            worktree_files = set()
            for file_path in common_docs_path.rglob("*.md"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(common_docs_path)
                    worktree_files.add(str(relative_path))

            # Find missing files
            missing = base_files - worktree_files
            if missing:
                integrity["missing_files"].extend(
                    [f"{worktree}:{file}" for file in missing]
                )

            # Find orphaned files (files in worktree but not in base)
            orphaned = worktree_files - base_files
            if orphaned:
                integrity["orphaned_files"].extend(
                    [f"{worktree}:{file}" for file in orphaned]
                )

        # Check for misplaced documentation files
        misplaced_files = self._find_misplaced_documentation()
        integrity["misplaced_files"] = misplaced_files

        # Calculate integrity score
        total_issues = (
            len(integrity["missing_files"])
            + len(integrity["orphaned_files"])
            + len(integrity["inconsistent_sync"])
            + len(integrity["misplaced_files"])
        )
        if integrity["total_files_checked"] > 0:
            integrity["integrity_score"] = max(0, 100 - (total_issues * 10))

        return integrity

    def optimize_storage(self) -> Dict:
        """Optimize storage usage."""
        print("  💾 Optimizing storage...")

        optimization = {
            "duplicate_files_found": 0,
            "large_files": [],
            "compression_savings": 0,
            "optimizations_applied": [],
        }

        # Find duplicate files (same content)
        file_hashes = {}
        for worktree in self.config.get("sync_rules", {}).get("worktrees", []):
            worktree_path = self.project_root / "worktrees" / worktree
            for md_file in worktree_path.rglob("*.md"):
                if md_file.is_file():
                    try:
                        with open(md_file, "rb") as f:
                            file_hash = hash(f.read())
                        if file_hash in file_hashes:
                            optimization["duplicate_files_found"] += 1
                        else:
                            file_hashes[file_hash] = md_file
                    except OSError:
                        continue

        # Find large files
        for md_file in self.project_root.rglob("*.md"):
            if md_file.is_file() and md_file.stat().st_size > 1024 * 1024:  # > 1MB
                optimization["large_files"].append(
                    {
                        "file": str(md_file.relative_to(self.project_root)),
                        "size": md_file.stat().st_size,
                    }
                )

        return optimization

    def _find_misplaced_documentation(self) -> List[str]:
        """Find documentation files in inappropriate locations."""
        misplaced = []

        # Define allowed documentation directories
        allowed_doc_dirs = {
            "docs",  # inheritance base
            "backlog",  # task management
        }

        # Add worktree-specific allowed directories
        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        for worktree in worktrees:
            allowed_doc_dirs.add(f"worktrees/{worktree}/docs")
            allowed_doc_dirs.add(f"worktrees/{worktree}/backlog")

        # Define forbidden directories (where docs shouldn't be)
        forbidden_patterns = [
            "src/",
            "python_backend/",
            "client/",
            "backend/",
            "modules/",
            "tests/",
            "scripts/",
            "deployment/",
            "config/",
            "data/",
            "models/",
            "plugins/",
            "shared/",
            "venv/",
            "node_modules/",
            "__pycache__/",
            ".git/",
            "logs/",
            ".github/",
            "jules-scratch/",
            "mock_models/",
            "email_intelligence.egg-info/",
            "temp_retrieve/",
            "performance_metrics_log.jsonl",
        ]

        # Find all markdown files in the project
        for md_file in self.project_root.rglob("*.md"):
            if md_file.is_file():
                # Get relative path from project root
                relative_path = str(md_file.relative_to(self.project_root))

                # Check if file is in an allowed documentation directory
                in_allowed_dir = False
                for allowed_dir in allowed_doc_dirs:
                    if relative_path.startswith(allowed_dir):
                        in_allowed_dir = True
                        break

                # If not in allowed directory, check if it's in a forbidden location
                if not in_allowed_dir:
                    for forbidden in forbidden_patterns:
                        if forbidden in relative_path:
                            misplaced.append(relative_path)
                            break

        return misplaced

    def _move_misplaced_file(self, misplaced_path: str) -> bool:
        """Move a misplaced documentation file to an appropriate location."""
        try:
            source_path = self.project_root / misplaced_path

            # Determine appropriate destination based on file content and location
            destination_path = self._determine_correct_location(misplaced_path)

            if destination_path:
                # Create destination directory if it doesn't exist
                destination_path.parent.mkdir(parents=True, exist_ok=True)

                # Check if destination already exists
                if destination_path.exists():
                    # Create a backup of the existing file
                    backup_path = destination_path.with_suffix(
                        f"{destination_path.suffix}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                    shutil.copy2(destination_path, backup_path)
                    print(f"    Backed up existing file: {backup_path.name}")

                # Move the file
                shutil.move(source_path, destination_path)
                print(
                    f"    Moved misplaced file: {misplaced_path} -> {destination_path.relative_to(self.project_root)}"
                )
                return True

        except Exception as e:
            print(f"    Error moving file {misplaced_path}: {e}")

        return False

    def _determine_correct_location(self, misplaced_path: str) -> Optional[Path]:
        """Determine the correct location for a misplaced documentation file."""
        file_path = self.project_root / misplaced_path
        file_name = file_path.name

        # Read first few lines to understand the file type
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                first_lines = f.read(500).lower()
        except:
            first_lines = ""

        # Check if it's a task file (contains task metadata)
        if "---" in first_lines and (
            "id: task-" in first_lines or "status:" in first_lines
        ):
            # This is a task file - should go in backlog/tasks/
            # Determine which worktree it belongs to based on path
            if "worktrees/docs-main" in misplaced_path:
                return (
                    self.project_root
                    / "worktrees"
                    / "docs-main"
                    / "backlog"
                    / "tasks"
                    / file_name
                )
            elif "worktrees/docs-scientific" in misplaced_path:
                return (
                    self.project_root
                    / "worktrees"
                    / "docs-scientific"
                    / "backlog"
                    / "tasks"
                    / file_name
                )
            else:
                # Default to main worktree
                return (
                    self.project_root
                    / "worktrees"
                    / "docs-main"
                    / "backlog"
                    / "tasks"
                    / file_name
                )

        # Check if it's documentation content (not a task)
        elif any(
            keyword in first_lines
            for keyword in ["# ", "## ", "### ", "overview", "introduction", "guide"]
        ):
            # This is general documentation - should go in branch-specific docs
            if "worktrees/docs-main" in misplaced_path:
                return (
                    self.project_root
                    / "worktrees"
                    / "docs-main"
                    / "docs"
                    / "main"
                    / file_name
                )
            elif "worktrees/docs-scientific" in misplaced_path:
                return (
                    self.project_root
                    / "worktrees"
                    / "docs-scientific"
                    / "docs"
                    / "scientific"
                    / file_name
                )
            else:
                # If in main project, move to inheritance base
                return self.project_root / "docs" / file_name

        # Default: move to branch-specific docs
        if "worktrees/docs-main" in misplaced_path:
            return (
                self.project_root
                / "worktrees"
                / "docs-main"
                / "docs"
                / "main"
                / file_name
            )
        elif "worktrees/docs-scientific" in misplaced_path:
            return (
                self.project_root
                / "worktrees"
                / "docs-scientific"
                / "docs"
                / "scientific"
                / file_name
            )
        else:
            return self.project_root / "docs" / file_name

    def generate_maintenance_report(self, results: Dict):
        """Generate maintenance report."""
        report_path = (
            self.project_root
            / "logs"
            / f"maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        report = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": {
                "overall_health": "good"
                if not any(
                    r.get("issues", []) for r in results.values() if isinstance(r, dict)
                )
                else "needs_attention",
                "total_issues": sum(
                    len(r.get("issues", []))
                    for r in results.values()
                    if isinstance(r, dict)
                ),
                "integrity_score": results.get("integrity", {}).get(
                    "integrity_score", 0
                ),
            },
        }

        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📄 Maintenance report saved to: {report_path}")

        # Print summary
        print("\n📊 Maintenance Summary:")
        print(f"  Health: {report['summary']['overall_health']}")
        print(f"  Issues: {report['summary']['total_issues']}")
        print(f"  Integrity: {report['summary']['integrity_score']}%")


def main():
    parser = argparse.ArgumentParser(description="Documentation Maintenance Script")
    parser.add_argument(
        "--full", "-f", action="store_true", help="Run full maintenance suite"
    )
    parser.add_argument(
        "--health", action="store_true", help="Check system health only"
    )
    parser.add_argument(
        "--cleanup", "-c", action="store_true", help="Perform cleanup tasks only"
    )
    parser.add_argument(
        "--integrity",
        "-i",
        action="store_true",
        help="Check documentation integrity only",
    )
    parser.add_argument(
        "--fix-misplaced",
        action="store_true",
        help="Automatically fix misplaced documentation files",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    maintenance = DocsMaintenance(project_root)

    if args.fix_misplaced:
        print("🔧 Fixing misplaced documentation files...")
        misplaced_files = maintenance._find_misplaced_documentation()
        if misplaced_files:
            print(f"Found {len(misplaced_files)} misplaced files:")
            for file in misplaced_files:
                print(f"  - {file}")

            moved_count = 0
            for misplaced_file in misplaced_files:
                if maintenance._move_misplaced_file(misplaced_file):
                    moved_count += 1

            print(
                f"✅ Successfully moved {moved_count} out of {len(misplaced_files)} files"
            )
        else:
            print("✅ No misplaced documentation files found")
    elif args.full or not any(
        [args.health, args.cleanup, args.integrity, args.fix_misplaced]
    ):
        maintenance.run_full_maintenance()
    elif args.health:
        result = maintenance.check_system_health()
        print(json.dumps(result, indent=2))
    elif args.cleanup:
        result = maintenance.perform_cleanup_tasks()
        print(json.dumps(result, indent=2))
    elif args.integrity:
        result = maintenance.check_documentation_integrity()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
