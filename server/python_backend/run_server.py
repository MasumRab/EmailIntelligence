#!/usr/bin/env python3
"""
Production server runner for Gmail AI Email Management
Optimized Python FastAPI backend with comprehensive performance monitoring
"""

import logging
import os
import sys
from pathlib import Path

import uvicorn
from python_backend.database import DatabaseManager
from python_backend.main import app

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def startup():
    """Initialize database and services on startup"""
    try:
        # Initialize database
        db = DatabaseManager()
        await db.initialize()
        logger.info("Database initialized successfully")

        # Log startup information
        logger.info("Gmail AI Email Management Backend starting...")
        logger.info(f"Environment: {os.getenv('NODE_ENV', 'development')}")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"

    # Configure uvicorn for production
    config = {
        "host": host,
        "port": port,
        "log_level": "info",
        "access_log": True,
        "reload": os.getenv("NODE_ENV") == "development",
        "workers": 1 if os.getenv("NODE_ENV") == "development" else 4,
    }

    logger.info(f"Starting server on {host}:{port}")

    # Add startup event handler
    app.add_event_handler("startup", startup)

    uvicorn.run(app, **config)
