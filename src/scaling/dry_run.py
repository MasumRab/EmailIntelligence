import concurrent.futures
import subprocess
import time
from typing import List, Dict, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoDryRunner:
    """
    Dry-runs a command across a list of repositories and reports feasibility.
    """
    def __init__(self, max_workers: int = 4, timeout: int = 30):
        self.max_workers = max_workers
        self.timeout = timeout

    def dry_run_repo(self, repo_path: str, command: str) -> Dict[str, Any]:
        """
        Executes a dry-run command on a single repository.
        """
        start_time = time.time()
        try:
            logger.info(f"Dry-running '{command}' on {repo_path}")

            # Using shell=True for complex commands, but splitting normally might be safer.
            # Assuming the command is a string and we need to run it in the repo directory.
            # In a real environment, shell=True requires caution, but here it might be needed for commands like "git status && git branch"
            result = subprocess.run(
                command,
                cwd=repo_path,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            execution_time = time.time() - start_time

            return {
                "repository": repo_path,
                "status": "success" if result.returncode == 0 else "error",
                "feasible": result.returncode == 0,
                "execution_time_seconds": execution_time,
                "error": result.stderr if result.returncode != 0 else None,
                "output": result.stdout
            }
        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            return {
                "repository": repo_path,
                "status": "timeout",
                "feasible": False,
                "execution_time_seconds": execution_time,
                "error": f"Command timed out after {self.timeout} seconds",
                "output": None
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "repository": repo_path,
                "status": "error",
                "feasible": False,
                "execution_time_seconds": execution_time,
                "error": str(e),
                "output": None
            }

    def dry_run_all(self, repos: List[str], command: str) -> Dict[str, Any]:
        """
        Dry-runs a command across all given repositories concurrently.
        """
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_repo = {
                executor.submit(self.dry_run_repo, repo, command): repo
                for repo in repos
            }

            for future in concurrent.futures.as_completed(future_to_repo):
                repo = future_to_repo[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Unhandled exception processing {repo}: {e}")
                    results.append({
                        "repository": repo,
                        "status": "unhandled_error",
                        "feasible": False,
                        "execution_time_seconds": 0,
                        "error": str(e),
                        "output": None
                    })

        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] != "success"]

        return {
            "total_repositories": len(repos),
            "successful_runs": len(successful),
            "failed_runs": len(failed),
            "all_feasible": len(failed) == 0,
            "results": results
        }

if __name__ == "__main__":
    runner = RepoDryRunner()
    print(json.dumps(runner.dry_run_all([".", "nonexistent_repo"], "git status"), indent=2))
