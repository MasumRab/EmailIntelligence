#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [arguments]
"""

import argparse
import atexit
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
import threading
import venv
from pathlib import Path
from typing import List

# Add project root to sys.path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Command pattern not available in this branch

from deployment.test_stages import test_stages
try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")


# --- Global state ---