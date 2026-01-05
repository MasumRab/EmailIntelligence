"""
Resolution execution module.
"""

from typing import Dict, Any
from pathlib import Path
import os
import shutil
import tempfile

from ..core.conflict_models import ResolutionPlan, ResolutionStep, ExecutionStatus, ConflictBlock
from ..git.repository import RepositoryOperations
from .semantic_merger import SemanticMerger
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ResolutionExecutor:
    """
    Executes resolution plans.
    """

    def __init__(self, repo_path: Path = None):
        self.repo = RepositoryOperations(repo_path)
        self.semantic_merger = SemanticMerger()

    async def execute_plan(self, plan: ResolutionPlan) -> bool:
        """
        Execute a resolution plan step-by-step.
        """
        logger.info("Executing plan", plan_id=plan.id)

        plan.status = ExecutionStatus.IN_PROGRESS
        context = {}  # Shared context between steps

        try:
            for step in plan.steps:
                success = await self._execute_step(step, context)
                if not success:
                    logger.error("Step failed", step=step.description)
                    plan.status = ExecutionStatus.FAILED
                    # TODO: Trigger rollback
                    return False

            plan.status = ExecutionStatus.COMPLETED
            logger.info("Plan executed successfully")
            return True

        except Exception as e:
            logger.error("Plan execution error", error=str(e))
            plan.status = ExecutionStatus.FAILED
            return False

    async def _execute_step(self, step: ResolutionStep, context: Dict[str, Any]) -> bool:
        """Execute a single resolution step."""
        logger.info("Executing step", action=step.action)

        try:
            if step.action == "git_checkout":
                # params: source, file
                await self.repo.run_git(
                    ["checkout", step.params["source"], "--", step.params["file"]]
                )

            elif step.action == "git_add":
                # params: file
                await self.repo.run_git(["add", step.params["file"]])

            elif step.action == "write_file":
                # params: file, content (optional if passed in context)
                file_path = step.params["file"]
                content = step.params.get("content")

                # If content not in params, check context (from previous merge step)
                if not content and "merged_content" in context:
                    content = context["merged_content"]

                if content:

                    try:
                        # 1. Path Validation
                        target_path = Path(file_path).resolve()
                        base_dir = Path.cwd().resolve()
                        try:
                            # Verify target_path is within base_dir
                            target_path.relative_to(base_dir)
                        except ValueError:
                            logger.error("Path traversal attempt detected", path=file_path)
                            return False

                        # 2. Ensure parent directories exist
                        target_path.parent.mkdir(parents=True, exist_ok=True)

                        # 3. Create Backup
                        if target_path.exists():
                            backup_path = target_path.with_suffix(target_path.suffix + ".bak")
                            shutil.copy2(target_path, backup_path)
                            logger.info("Created backup", backup=str(backup_path))

                        # 4. Atomic Write
                        with tempfile.NamedTemporaryFile(
                            "w", dir=target_path.parent, delete=False, encoding="utf-8"
                        ) as tmp_file:
                            tmp_file.write(content)
                            tmp_path = Path(tmp_file.name)

                        # Preserve permissions if possible
                        if target_path.exists():
                            shutil.copymode(target_path, tmp_path)

                        # Atomic replace
                        os.replace(tmp_path, target_path)
                        logger.info("File written successfully", path=str(target_path))

                    except Exception as e:
                        logger.error("Failed to write file", path=file_path, error=str(e))
                        if "tmp_path" in locals() and tmp_path.exists():
                            os.unlink(tmp_path)
                        return False
                else:
                    logger.error("No content provided for write_file")
                    return False

            elif step.action == "semantic_merge":
                # params: conflict_block (passed as dict or object)
                # This step attempts to merge and stores result in context
                block_data = step.params.get("block")
                if block_data:
                    # Assuming block_data is a dictionary or ConflictBlock object
                    if isinstance(block_data, dict):
                        block = ConflictBlock(**block_data)
                    else:
                        block = block_data

                    merged = await self.semantic_merger.merge_blocks(block)
                    if merged:
                        context["merged_content"] = merged
                    else:

                        logger.warning("Semantic merge returned None")
                        return False
                else:
                    logger.error("No block data for semantic_merge")
                    return False

            elif step.action == "apply_merge":
                # params: file, block (dict)
                file_path = step.params["file"]
                block_data = step.params["block"]
                content = context.get("merged_content")

                if content is None:
                    logger.error("No merged content to apply")
                    return False

                try:
                    # Path Validation
                    target_path = Path(file_path).resolve()
                    base_dir = Path.cwd().resolve()
                    try:
                        target_path.relative_to(base_dir)
                    except ValueError:
                        logger.error("Path traversal attempt detected", path=file_path)
                        return False

                    # Read file
                    with open(target_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    start = block_data["start_line"] - 1
                    end = block_data["end_line"]

                    # Ensure range is valid
                    if start < 0 or end > len(lines):
                        logger.error(
                            "Invalid line range for merge application",
                            start=start,
                            end=end,
                        )
                        return False

                    # Replace lines with merged content
                    # We need to ensure content ends with newline if needed,
                    # or matches surrounding style
                    # For now, simplistic replacement
                    if not content.endswith("\n"):
                        content += "\n"

                    lines[start:end] = [content]

                    with open(target_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)

                except Exception as e:
                    logger.error("Failed to apply merge to file", error=str(e))
                    return False

            elif step.action == "manual_edit":
                # Pause for user input (CLI interaction)
                # For now, just log
                logger.info("Waiting for manual edit...")

            return True

        except Exception as e:
            logger.error("Step execution failed", error=str(e))
            return False
