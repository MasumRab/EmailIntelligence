import concurrent.futures
import shlex
import subprocess
import time
from typing import List, Dict, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoFeasibilityRunner:
    """
    Runs a command across a list of repositories and reports feasibility.
    """
    def __init__(self, max_workers: int = 4, timeout: int = 30):
        self.max_workers = max_workers
        self.timeout = timeout

    def run_feasibility_repo(self, repo_path: str, command: List[str]) -> Dict[str, Any]:
        """
        Executes a real command on a single repository to determine feasibility.
        Note: The command runs for real and any side effects (like file modifications)
        will leave the repository modified.
        """
        start_time = time.time()
        try:
            executable = command[0] if command else "unknown"
            logger.info(f"Running feasibility check executable '{executable}' ({len(command)} args) on {repo_path}")
            
            # No shell: the command string is already an argv list, so shell
            # metacharacters in it are inert. That also means shell chaining
            # ("a && b") is not interpreted -- pass one command per run.
            result = subprocess.run(
                command,
                cwd=repo_path,
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

    def run_feasibility_all(self, repos: List[str], command_str: str) -> Dict[str, Any]:
        """
        Runs a command across all given repositories concurrently.
        Note: This is not a dry run; it executes the command for real.
        """
        results = []
        command = shlex.split(command_str)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_repo = {
                executor.submit(self.run_feasibility_repo, repo, command): repo 
                for repo in repos
            }
            
            for future in concurrent.futures.as_completed(future_to_repo):
                repo = future_to_repo[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.exception("Unhandled exception processing %s", repo)
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
    runner = RepoFeasibilityRunner()
    print(json.dumps(runner.run_feasibility_all([".", "nonexistent_repo"], "git status"), indent=2))
