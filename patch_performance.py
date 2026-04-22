import re

with open("src/core/performance_monitor.py", "r") as f:
    content = f.read()

# Add # noqa: E402 to imports not at top
content = re.sub(r'^(import atexit)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from collections import defaultdict, deque)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from dataclasses import asdict, dataclass)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from pathlib import Path)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from typing import Any, Dict, Optional, Union)', r'\1  # noqa: E402', content, flags=re.MULTILINE)

# Remove redefined PerformanceMetric
content = re.sub(r'@dataclass\nclass PerformanceMetric:\n    """Represents a performance metric with minimal overhead."""\n    name: str\n    value: float\n    unit: str\n    timestamp: float\n    tags: Optional\[Dict\[str, str\]\] = None\n\n\n', '', content)

# Remove redefined log_performance
content = re.sub(r'    def log_performance\(self, log_entry: Dict\[str, Any\]\) -> None:\n        """Compatibility method for legacy log_performance decorator."""\n        operation = log_entry\.get\("operation", "unknown"\)\n        duration = log_entry\.get\("execution_time_ms", 0\.0\)\n        tags = {k: str\(v\) for k, v in log_entry\.items\(\) if k not in \("operation", "execution_time_ms"\)}\n        self\.record_metric\("legacy_op", float\(duration\), "ms", tags\)\n', '', content)

with open("src/core/performance_monitor.py", "w") as f:
    f.write(content)
