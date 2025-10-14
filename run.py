"""
Development server runner for the FastAPI backend.

This script starts the Uvicorn server with hot-reloading enabled, making it
suitable for development purposes. It ensures that the application reloads
automatically when code changes are detected.
"""

import uvicorn
import os
import sys
from pathlib import Path

import uvicorn

# Add the current directory to the path to ensure modules can be found
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # We use a string to specify the app location to allow for reloading.
    uvicorn.run("backend.python_backend.main:app", host="0.0.0.0", port=port, reload=True)
