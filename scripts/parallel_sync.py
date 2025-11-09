#!/usr/bin/env python3
"""
Parallel Sync Workers
Implement multiple sync processes for different worktrees simultaneously.
"""

import time
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from incremental_sync import IncrementalSync
import json


class SyncWorker:
    def __init__(self, worker_id: str, source_dir: Path, target_dir: Path):
        self.worker_id = worker_id
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.sync = IncrementalSync(source_dir, target_dir)
        self.is_active = False
        self.last_sync_result = None
        self.sync_count = 0

    def sync_once(self, extensions: set = None) -> Dict:
        """Perform a single sync operation."""
        self.is_active = True
        try:
            result = self.sync.sync_changes(extensions)
            self.last_sync_result = result
            self.sync_count += 1
            return result
        except Exception as e:
            return {"error": str(e)}
        finally:
            self.is_active = False

    def get_status(self) -> Dict:
        """Get worker status."""
        return {
            "worker_id": self.worker_id,
            "source": str(self.source_dir),
            "target": str(self.target_dir),
            "is_active": self.is_active,
            "sync_count": self.sync_count,
            "last_sync_result": self.last_sync_result,
            "last_sync_stats": self.sync.get_sync_stats(),
        }


class ParallelSyncManager:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.workers: Dict[str, SyncWorker] = {}
        self.sync_history: List[Dict] = []
        self.sync_log_file = Path("parallel_sync_log.json")
        self.load_sync_log()

    def load_sync_log(self):
        """Load sync log from file."""
        if self.sync_log_file.exists():
            try:
                with open(self.sync_log_file, "r") as f:
                    self.sync_history = json.load(f)
            except Exception as e:
                print(f"Error loading sync log: {e}")

    def save_sync_log(self):
        """Save sync log to file."""
        try:
            with open(self.sync_log_file, "w") as f:
                json.dump(self.sync_history, f, indent=2)
        except Exception as e:
            print(f"Error saving sync log: {e}")

    def add_worker(self, worker_id: str, source_dir: Path, target_dir: Path) -> bool:
        """Add a sync worker."""
        if worker_id in self.workers:
            return False

        if not source_dir.exists():
            print(f"Source directory does not exist: {source_dir}")
            return False

        worker = SyncWorker(worker_id, source_dir, target_dir)
        self.workers[worker_id] = worker
        return True

    def remove_worker(self, worker_id: str) -> bool:
        """Remove a sync worker."""
        if worker_id in self.workers:
            del self.workers[worker_id]
            return True
        return False

    def sync_worker(self, worker_id: str, extensions: set = None) -> Optional[Dict]:
        """Sync a specific worker."""
        if worker_id not in self.workers:
            return None

        worker = self.workers[worker_id]
        result = worker.sync_once(extensions)

        # Log the sync operation
        log_entry = {"timestamp": time.time(), "worker_id": worker_id, "result": result}
        self.sync_history.append(log_entry)
        self.save_sync_log()

        return result

    def sync_all_workers(self, extensions: set = None) -> Dict[str, Dict]:
        """Sync all workers in parallel using threads."""
        if not self.workers:
            return {}

        results = {}

        # Use ThreadPoolExecutor for I/O bound operations
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all sync tasks
            future_to_worker = {
                executor.submit(self.sync_worker, worker_id, extensions): worker_id
                for worker_id in self.workers.keys()
            }

            # Collect results as they complete
            for future in as_completed(future_to_worker):
                worker_id = future_to_worker[future]
                try:
                    result = future.result()
                    results[worker_id] = result
                except Exception as e:
                    results[worker_id] = {"error": str(e)}

        return results

    def sync_all_workers_sequential(self, extensions: set = None) -> Dict[str, Dict]:
        """Sync all workers sequentially."""
        results = {}
        for worker_id in self.workers:
            results[worker_id] = self.sync_worker(worker_id, extensions)
        return results

    def get_worker_status(self, worker_id: str) -> Optional[Dict]:
        """Get status of a specific worker."""
        if worker_id in self.workers:
            return self.workers[worker_id].get_status()
        return None

    def get_all_workers_status(self) -> Dict[str, Dict]:
        """Get status of all workers."""
        return {
            worker_id: self.workers[worker_id].get_status()
            for worker_id in self.workers
        }

    def get_sync_summary(self) -> Dict:
        """Get summary of all sync operations."""
        total_workers = len(self.workers)
        active_workers = len([w for w in self.workers.values() if w.is_active])

        total_syncs = sum(w.sync_count for w in self.workers.values())
        total_files_synced = 0

        # Calculate total files synced
        for worker in self.workers.values():
            stats = worker.sync.get_sync_stats()
            total_files_synced += stats.get("total_files_synced", 0)

        return {
            "total_workers": total_workers,
            "active_workers": active_workers,
            "total_syncs": total_syncs,
            "total_files_synced": total_files_synced,
            "worker_statuses": self.get_all_workers_status(),
        }

    def scale_workers(self, target_count: int) -> int:
        """Scale the number of workers (conceptual - would require dynamic worker management)."""
        current_count = len(self.workers)
        if target_count > current_count:
            return target_count - current_count  # Need to add workers
        elif target_count < current_count:
            return current_count - target_count  # Need to remove workers
        else:
            return 0  # No change needed


def main():
    # Example usage
    print("Parallel Sync Workers System")
    print("=" * 30)

    # Create sync manager
    manager = ParallelSyncManager(max_workers=4)

    # Add some workers (this would be configured based on actual worktrees)
    print("Parallel sync manager initialized")
    print("System ready to sync multiple worktrees simultaneously")

    # Example of what the configuration might look like:
    print("\nExample configuration:")
    print("  Worker 1: docs/main -> worktrees/docs-main/docs/common/docs")
    print("  Worker 2: docs/main -> worktrees/docs-scientific/docs/common/docs")
    print(
        "  Worker 3: worktrees/docs-main/docs/main -> worktrees/docs-scientific/docs/main"
    )

    print("\nWorkers can be synced in parallel for improved performance")


if __name__ == "__main__":
    main()
