#!/usr/bin/env python3
"""
RQ Job Worker for Dashboard Background Tasks

This script starts RQ workers to process background jobs for dashboard calculations.
Run this script to enable background processing of heavy dashboard operations.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rq import Worker, Queue, Connection
from redis import Redis

def main():
    """Start RQ worker for dashboard jobs"""
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

    with Connection(Redis.from_url(redis_url)):
        worker = Worker(['dashboard_jobs'], name='dashboard-worker')
        print("Starting RQ worker for dashboard jobs...")
        print(f"Redis URL: {redis_url}")
        print("Press Ctrl+C to stop")
        worker.work()

if __name__ == '__main__':
    main()
