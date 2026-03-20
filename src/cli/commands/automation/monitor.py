"""
Monitor Command Module

Implements system resource tracking and workflow bottleneck detection.
Ported from scripts/resource_monitor.py and scripts/bottleneck_detector.py.
"""

import time
import json
import psutil
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..interface import Command


class MonitorCommand(Command):
    """
    Command for monitoring system resources and detecting workflow bottlenecks.
    
    Tracks CPU, memory, and disk usage while identifying long-running tasks
    or resource contention issues that may slow down parallel agents.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "monitor"

    @property
    def description(self) -> str:
        return "Monitor system resources and workflow performance"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--interval", 
            type=float, 
            default=5.0,
            help="Monitoring interval in seconds"
        )
        parser.add_argument(
            "--output", 
            default=".resource_monitoring.json",
            help="Path to save monitoring data"
        )
        parser.add_argument(
            "--once", 
            action="store_true", 
            help="Run a single snapshot and exit"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the monitor command."""
        output_path = Path(args.output)

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(output_path.absolute()))
            if not is_safe:
                print(f"Error: Security violation: {error}")
                return 1

        print("📊 Starting Resource Monitor...")
        
        try:
            while True:
                snapshot = self._take_snapshot()
                self._print_snapshot(snapshot)
                
                # Save data
                with open(output_path, 'w') as f:
                    json.dump(snapshot, f, indent=2)
                
                if args.once:
                    break
                    
                time.sleep(args.interval)
            
            return 0
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
            return 0
        except Exception as e:
            print(f"Error during monitoring: {e}")
            return 1

    def _take_snapshot(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        return {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory": {
                "percent": psutil.virtual_memory().percent,
                "available_gb": psutil.virtual_memory().available / (1024**3)
            },
            "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0,0,0),
            "process_count": len(psutil.pids())
        }

    def _print_snapshot(self, s: Dict[str, Any]) -> None:
        """Print snapshot to console."""
        print(f"[{time.strftime('%H:%M:%S')}] CPU: {s['cpu_percent']}% | MEM: {s['memory']['percent']}% | Load: {s['load_avg'][0]}")
