#!/usr/bin/env python3
"""
Run Application Module for EmailIntelligence

This module provides functions for running the application in different stages,
including development, testing, staging, and production.
"""

import os
import sys
import subprocess
import logging
import time
import json
import argparse
import signal
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Import environment manager
from deployment.env_manager import env_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("run-app")

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

class RunApplication:
    """Manages running the application in different stages."""
    
    def __init__(self, root_dir: Path = ROOT_DIR):
        """Initialize the run application manager."""
        self.root_dir = root_dir
        self.env_manager = env_manager
        self.processes = []
    
    def _handle_sigint(self, signum, frame):
        """Handle SIGINT signal."""
        logger.info("Received SIGINT, shutting down...")
        self.stop_all()
        sys.exit(0)
    
    def _setup_signal_handlers(self):
        """Set up signal handlers."""
        signal.signal(signal.SIGINT, self._handle_sigint)
        signal.signal(signal.SIGTERM, self._handle_sigint)
    
    def run_dev_backend(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False) -> subprocess.Popen:
        """Run the backend in development mode."""
        logger.info(f"Starting backend in development mode on {host}:{port}...")
        
        # Ensure development dependencies are installed
        if not self.env_manager.setup_environment_for_stage("dev"):
            return None
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [
            python,
            "-m", "uvicorn",
            "server.python_backend.main:app",
            "--host", host,
            "--port", str(port),
            "--reload"
        ]
        
        if debug:
            cmd.append("--log-level=debug")
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)
        env["NODE_ENV"] = "development"
        env["DEBUG"] = "True" if debug else "False"
        
        # Run the backend
        process = subprocess.Popen(cmd, env=env)
        self.processes.append(process)
        
        # Wait for the server to start
        time.sleep(2)
        
        return process
    
    def run_dev_frontend(self, host: str = "127.0.0.1", port: int = 5173) -> subprocess.Popen:
        """Run the frontend in development mode."""
        logger.info(f"Starting frontend in development mode on {host}:{port}...")
        
        # Check if Node.js is installed
        try:
            subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Node.js is not installed or not in PATH")
            return None
        
        # Build command
        cmd = ["npm", "run", "dev", "--", "--host", host, "--port", str(port)]
        
        # Set environment variables
        env = os.environ.copy()
        env["VITE_API_URL"] = f"http://{host}:8000"
        env["NODE_ENV"] = "development"
        
        # Run the frontend
        process = subprocess.Popen(cmd, cwd=str(self.root_dir / "client"), env=env)
        self.processes.append(process)
        
        # Wait for the server to start
        time.sleep(2)
        
        return process
    
    def run_dev_mode(self, host: str = "127.0.0.1", backend_port: int = 8000, frontend_port: int = 5173, debug: bool = False) -> bool:
        """Run the application in development mode."""
        logger.info("Starting application in development mode...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Start the backend
        backend_process = self.run_dev_backend(host, backend_port, debug)
        if not backend_process:
            logger.error("Failed to start backend")
            return False
        
        # Start the frontend
        frontend_process = self.run_dev_frontend(host, frontend_port)
        if not frontend_process:
            logger.error("Failed to start frontend")
            backend_process.terminate()
            return False
        
        logger.info(f"Application started in development mode")
        logger.info(f"Backend: http://{host}:{backend_port}")
        logger.info(f"Frontend: http://{host}:{frontend_port}")
        
        try:
            # Wait for processes to complete
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
        
        return True
    
    def run_test_mode(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False) -> bool:
        """Run the application in test mode."""
        logger.info("Starting application in test mode...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [
            python,
            "-m", "uvicorn",
            "server.python_backend.main:app",
            "--host", host,
            "--port", str(port)
        ]
        
        if debug:
            cmd.append("--log-level=debug")
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)
        env["NODE_ENV"] = "test"
        env["DEBUG"] = "True" if debug else "False"
        env["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/emailintelligence_test"
        
        # Run the application
        process = subprocess.Popen(cmd, env=env)
        self.processes.append(process)
        
        logger.info(f"Application started in test mode: http://{host}:{port}")
        
        try:
            # Wait for process to complete
            process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
        
        return True
    
    def run_staging_mode(self) -> bool:
        """Run the application in staging mode."""
        logger.info("Starting application in staging mode...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [
            python,
            str(self.root_dir / "deployment" / "deploy.py"),
            "staging",
            "up"
        ]
        
        # Run the application
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        
        logger.info("Application started in staging mode")
        
        try:
            # Wait for process to complete
            process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
            
            # Run the down command to clean up
            subprocess.call([
                python,
                str(self.root_dir / "deployment" / "deploy.py"),
                "staging",
                "down"
            ])
        
        return True
    
    def run_production_mode(self) -> bool:
        """Run the application in production mode."""
        logger.info("Starting application in production mode...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [
            python,
            str(self.root_dir / "deployment" / "deploy.py"),
            "prod",
            "up"
        ]
        
        # Run the application
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        
        logger.info("Application started in production mode")
        
        try:
            # Wait for process to complete
            process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
            
            # Run the down command to clean up
            subprocess.call([
                python,
                str(self.root_dir / "deployment" / "deploy.py"),
                "prod",
                "down"
            ])
        
        return True
    
    def run_api_only(self, host: str = "127.0.0.1", port: int = 8000, debug: bool = False, stage: str = "dev") -> bool:
        """Run only the API server."""
        logger.info(f"Starting API server in {stage} mode on {host}:{port}...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Ensure dependencies are installed
        if not self.env_manager.setup_environment_for_stage(stage):
            return False
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [
            python,
            "-m", "uvicorn",
            "server.python_backend.main:app",
            "--host", host,
            "--port", str(port)
        ]
        
        if stage == "dev":
            cmd.append("--reload")
        
        if debug:
            cmd.append("--log-level=debug")
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.root_dir)
        env["NODE_ENV"] = stage
        env["DEBUG"] = "True" if debug else "False"
        
        # Run the API server
        process = subprocess.Popen(cmd, env=env)
        self.processes.append(process)
        
        logger.info(f"API server started in {stage} mode: http://{host}:{port}")
        
        try:
            # Wait for process to complete
            process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
        
        return True
    
    def run_frontend_only(self, host: str = "127.0.0.1", port: int = 5173, api_url: str = None, stage: str = "dev") -> bool:
        """Run only the frontend."""
        logger.info(f"Starting frontend in {stage} mode on {host}:{port}...")
        
        # Set up signal handlers
        self._setup_signal_handlers()
        
        # Check if Node.js is installed
        try:
            subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Node.js is not installed or not in PATH")
            return False
        
        # Build command
        if stage == "dev":
            cmd = ["npm", "run", "dev", "--", "--host", host, "--port", str(port)]
        else:
            cmd = ["npm", "run", "preview", "--", "--host", host, "--port", str(port)]
        
        # Set environment variables
        env = os.environ.copy()
        env["VITE_API_URL"] = api_url or f"http://{host}:8000"
        env["NODE_ENV"] = stage
        
        # Run the frontend
        process = subprocess.Popen(cmd, cwd=str(self.root_dir / "client"), env=env)
        self.processes.append(process)
        
        logger.info(f"Frontend started in {stage} mode: http://{host}:{port}")
        
        try:
            # Wait for process to complete
            process.wait()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop_all()
        
        return True
    
    def stop_all(self) -> None:
        """Stop all running processes."""
        for process in self.processes:
            if process.poll() is None:  # Process is still running
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        self.processes = []

# Create a singleton instance
run_app = RunApplication()

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Application for EmailIntelligence")
    
    # Stage argument
    parser.add_argument("--stage", choices=["dev", "test", "staging", "prod"], default="dev",
                        help="Specify the application stage to run")
    
    # Server configuration
    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Specify the host to run on (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Specify the port to run on (default: 8000)")
    parser.add_argument("--frontend-port", type=int, default=5173,
                        help="Specify the frontend port to run on (default: 5173)")
    parser.add_argument("--api-url", type=str,
                        help="Specify the API URL for the frontend")
    
    # Mode arguments
    parser.add_argument("--api-only", action="store_true",
                        help="Run only the API server without the frontend")
    parser.add_argument("--frontend-only", action="store_true",
                        help="Run only the frontend without the API server")
    
    # Debug mode
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")
    
    return parser.parse_args()

def main() -> int:
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Run the application in the specified mode
    if args.api_only:
        success = run_app.run_api_only(args.host, args.port, args.debug, args.stage)
    elif args.frontend_only:
        success = run_app.run_frontend_only(args.host, args.frontend_port, args.api_url, args.stage)
    elif args.stage == "dev":
        success = run_app.run_dev_mode(args.host, args.port, args.frontend_port, args.debug)
    elif args.stage == "test":
        success = run_app.run_test_mode(args.host, args.port, args.debug)
    elif args.stage == "staging":
        success = run_app.run_staging_mode()
    elif args.stage == "prod":
        success = run_app.run_production_mode()
    else:
        logger.error(f"Unknown stage: {args.stage}")
        success = False
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())