import asyncio
import json
import logging
import sys
import os
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

async def _execute_async_command(cmd: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
    """Execute command asynchronously"""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            logger.error(f"Async command failed: {error_msg}")
            return {"error": error_msg}

        # Parse JSON output
        try:
            return json.loads(stdout.decode())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse command response: {e}")
            return {"error": f"Invalid JSON response: {e}"}

    except Exception as e:
        logger.error(f"Async command execution failed: {e}")
        return {"error": str(e)}
