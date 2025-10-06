"""
API routes for performance monitoring.
"""
import logging
import json
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter()

LOG_FILE = "performance_metrics_log.jsonl"

@router.get("/api/performance", response_model=List[Dict[str, Any]])
async def get_performance_metrics():
    """
    Retrieves performance metrics from the log file.
    """
    try:
        metrics = []
        with open(LOG_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
        return metrics
    except FileNotFoundError:
        logger.warning(f"Performance log file not found at '{LOG_FILE}'. Returning empty list.")
        return []
    except Exception as e:
        logger.error(f"Failed to read or parse performance log file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve performance metrics.")