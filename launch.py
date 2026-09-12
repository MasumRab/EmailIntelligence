#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher Wrapper
Redirects to the main launcher in the setup package.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from setup.launch import main

if __name__ == "__main__":
    sys.exit(main())
