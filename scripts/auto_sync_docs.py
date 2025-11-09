#!/usr/bin/env python3
"""
Automated Documentation Synchronization System
Provides scheduled sync, monitoring, and automated conflict resolution.
"""

import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict
import argparse

try:
    import schedule

    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False


class AutoDocSync:
    """Automated documentation synchronization system."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.project_root = Path(__file__).resolve().parent.parent
        self._setup_logging()

    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in config file: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Set up logging based on configuration."""
        log_config = self.config.get("monitoring", {})
        log_file = log_config.get("log_file", "logs/docs_sync.log")

        # Ensure log directory exists
        log_path = self.project_root / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        # Also log to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)

        self.logger = logging.getLogger(__name__)

    def run_scheduled_sync(self):
        """Run scheduled synchronization."""
        self.logger.info("Starting scheduled documentation sync")

        try:
            # Sync from inheritance base
            self._sync_from_inheritance_base()

            # Sync between worktrees if configured
            self._sync_between_worktrees()

            # Clean up old backups
            self._cleanup_old_backups()

            # Update metrics
            self._update_metrics()

            self.logger.info("Scheduled sync completed successfully")

        except Exception as e:
            self.logger.error(f"Scheduled sync failed: {e}")
            raise

    def _sync_from_inheritance_base(self):
        """Sync from inheritance base to all worktrees."""
        from sync_common_docs import DocumentationSync

        sync_config = self.config.get("sync_rules", {})
        conflict_strategy = self.config.get("conflict_resolution", {}).get(
            "default_strategy", "backup"
        )

        sync = DocumentationSync(self.project_root, conflict_strategy)
        success = sync.sync_from_inheritance_base()

        if success:
            self.logger.info("Successfully synced from inheritance base")
        else:
            self.logger.error("Failed to sync from inheritance base")

        return success

    def _sync_between_worktrees(self):
        """Sync between worktrees if configured."""
        # For now, sync main to scientific to keep scientific up to date
        from sync_common_docs import DocumentationSync

        conflict_strategy = self.config.get("conflict_resolution", {}).get(
            "default_strategy", "backup"
        )
        sync = DocumentationSync(self.project_root, conflict_strategy)

        try:
            success = sync.sync_between_worktrees("docs-main", "docs-scientific")
            if success:
                self.logger.info("Successfully synced between worktrees")
            else:
                self.logger.warning("Failed to sync between worktrees")
        except Exception as e:
            self.logger.error(f"Error syncing between worktrees: {e}")

    def _cleanup_old_backups(self):
        """Clean up old backup files."""
        retention_days = self.config.get("conflict_resolution", {}).get(
            "backup_retention_days", 30
        )
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        common_path = self.config.get("sync_rules", {}).get(
            "common_docs_path", "docs/common/docs"
        )

        backup_count = 0
        for worktree in worktrees:
            worktree_path = self.project_root / "worktrees" / worktree / common_path
            if worktree_path.exists():
                for backup_file in worktree_path.glob("*.backup_*"):
                    try:
                        # Extract timestamp from filename (format: filename.backup_YYMMDD_HHMMSS)
                        parts = backup_file.name.split("_")
                        if len(parts) >= 2:
                            timestamp_str = parts[
                                -1
                            ]  # Last part should be the timestamp
                            # Handle both YYYYMMDD_HHMMSS and YYMMDD_HHMMSS formats
                            if len(timestamp_str) == 15:  # YYYYMMDD_HHMMSS
                                file_date = datetime.strptime(
                                    timestamp_str, "%Y%m%d_%H%M%S"
                                )
                            elif len(timestamp_str) == 13:  # YYMMDD_HHMMSS
                                file_date = datetime.strptime(
                                    timestamp_str, "%y%m%d_%H%M%S"
                                )
                            else:
                                raise ValueError(
                                    f"Unexpected timestamp format: {timestamp_str}"
                                )
                        else:
                            raise ValueError("Invalid backup filename format")

                        if file_date < cutoff_date:
                            backup_file.unlink()
                            backup_count += 1
                            self.logger.info(f"Removed old backup: {backup_file}")
                    except (ValueError, OSError) as e:
                        self.logger.warning(
                            f"Error processing backup file {backup_file}: {e}"
                        )

        if backup_count > 0:
            self.logger.info(f"Cleaned up {backup_count} old backup files")

    def _update_metrics(self):
        """Update synchronization metrics."""
        if not self.config.get("monitoring", {}).get("enable_metrics", False):
            return

        metrics_file = self.config.get("monitoring", {}).get(
            "metrics_file", "logs/docs_sync_metrics.json"
        )
        metrics_path = self.project_root / metrics_file
        metrics_path.parent.mkdir(parents=True, exist_ok=True)

        # Collect current metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "worktrees": {},
            "total_syncs": 0,
        }

        worktrees = self.config.get("sync_rules", {}).get("worktrees", [])
        for worktree in worktrees:
            worktree_path = self.project_root / "worktrees" / worktree
            if worktree_path.exists():
                common_count = len(
                    list((worktree_path / "docs" / "common" / "docs").glob("*.md"))
                )
                branch_path = (
                    self.config.get("sync_rules", {})
                    .get("branch_docs_paths", {})
                    .get(worktree, f"docs/{worktree.split('-')[1]}")
                )
                branch_count = len(list((worktree_path / branch_path).glob("*.md")))

                metrics["worktrees"][worktree] = {
                    "common_docs": common_count,
                    "branch_docs": branch_count,
                    "total_docs": common_count + branch_count,
                }

        # Load existing metrics and append
        if metrics_path.exists():
            try:
                with open(metrics_path, "r") as f:
                    existing_metrics = json.load(f)
                    existing_metrics.append(metrics)
                    metrics = existing_metrics[-100:]  # Keep last 100 entries
            except (json.JSONDecodeError, IOError):
                metrics = [metrics]
        else:
            metrics = [metrics]

        # Save metrics
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)

    def start_scheduler(self):
        """Start the automated scheduler."""
        if not SCHEDULE_AVAILABLE:
            self.logger.error(
                "schedule module not available. Install with: pip install schedule"
            )
            return

        automation_config = self.config.get("automation", {})
        schedule_config = automation_config.get("sync_schedule", "daily")
        sync_time = automation_config.get("sync_time", "02:00")

        if schedule_config == "daily":
            schedule.every().day.at(sync_time).do(self.run_scheduled_sync)
            self.logger.info(f"Scheduled daily sync at {sync_time}")
        elif schedule_config == "hourly":
            schedule.every().hour.do(self.run_scheduled_sync)
            self.logger.info("Scheduled hourly sync")
        else:
            self.logger.warning(f"Unknown schedule config: {schedule_config}")
            return

        self.logger.info("Starting automated sync scheduler")
        self.logger.info("Press Ctrl+C to stop")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")


def main():
    parser = argparse.ArgumentParser(description="Automated Documentation Sync System")
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        default=Path(__file__).parent / "sync_config.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--run-once", "-r", action="store_true", help="Run sync once and exit"
    )
    parser.add_argument(
        "--schedule", "-s", action="store_true", help="Start scheduled sync (default)"
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Configuration file not found: {args.config}")
        sys.exit(1)

    sync_system = AutoDocSync(args.config)

    if args.run_once:
        sync_system.run_scheduled_sync()
    else:
        # Default to scheduled mode
        sync_system.start_scheduler()


if __name__ == "__main__":
    main()
