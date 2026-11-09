import pytest
import json
import time
import sys

class JSONReportPlugin:
    def __init__(self):
        self.results = {}
        self.passed = 0
        self.failed = 0
        
    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.results[report.nodeid] = {
                "status": report.outcome,
                "execution_time": report.duration,
            }
            if report.outcome == "passed":
                self.passed += 1
            elif report.outcome == "failed":
                self.failed += 1

def main():
    test_path = sys.argv[1] if len(sys.argv) > 1 else "tests/test_e2e_subset.py"
    
    start = time.time()
    plugin = JSONReportPlugin()
    exit_code = pytest.main([test_path, "-q"], plugins=[plugin])
    duration = time.time() - start
    
    total = plugin.passed + plugin.failed
    success_rate = plugin.passed / total if total > 0 else 0
    
    report = {
        "test_results": plugin.results,
        "performance_metrics": {
            "total_execution_time": round(duration, 4)
        },
        "quality_metrics": {
            "pass_count": plugin.passed,
            "fail_count": plugin.failed,
            "total": total,
            "success_rate": round(success_rate, 4)
        },
        "overall_status": "passed" if plugin.failed == 0 and total > 0 else "failed"
    }
    
    with open("e2e_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print(json.dumps(report, indent=2))
    sys.exit(0 if exit_code == 0 else 1)

if __name__ == "__main__":
    main()
