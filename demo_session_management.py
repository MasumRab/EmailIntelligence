#!/usr/bin/env python3
"""
Demonstration script for the Session Management System

This script demonstrates how to use the session management system
for documented development sessions with full state management.
"""

import json
from pathlib import Path
import sys

# Add the .qwen directory to the path to import session_manager
sys.path.insert(0, str(Path(__file__).parent / ".qwen"))

from session_manager import SessionManager


def demo_session_management():
    """Demonstrate the session management system."""
    print("🎯 Session Management System Demo")
    print("=" * 50)
    
    # Initialize session manager for the current project
    project_root = Path.cwd()
    sm = SessionManager(project_root)
    
    print(f"📁 Project root: {sm.project_root}")
    print(f"⚙️  Qwen directory: {sm.qwen_dir}")
    print()
    
    # Show initial context
    print("📋 Initial Project Context:")
    context = sm.get_project_context()
    print(f"  • QWEN.md found: {'Yes' if 'qwem_md_content' in context else 'No'}")
    print(f"  • Pending handoffs: {len(context.get('pending_handoffs', []))}")
    print(f"  • Command history entries: {len(context.get('command_history', []))}")
    print()
    
    # Start a new session
    print("🚀 Starting a new development session...")
    goals = [
        "Implement session management system",
        "Document development process",
        "Ensure state persistence across sessions",
        "Create command-line interface"
    ]
    
    session_info = sm.start_session(goals=goals)
    print(f"✅ Session started: {session_info['session_id']}")
    print(f"📅 Start time: {session_info['start_time']}")
    print(f"🎯 Goals: {session_info['goals']}")
    print()
    
    # Show state after starting session
    print("📊 State after starting session:")
    with open(sm.state_file, 'r') as f:
        state_data = json.load(f)
    print(f"  • Current session: {state_data['current_session']}")
    print(f"  • Command history count: {len(state_data['command_history'])}")
    print()
    
    # Show session file content
    print("📋 Session file content:")
    with open(sm.session_file, 'r') as f:
        session_data = json.load(f)
    print(f"  • Status: {session_data['status']}")
    print(f"  • Goals: {session_data['goals']}")
    print()
    
    # End the session
    print("🛑 Ending the development session...")
    ended_session_id = sm.end_session()
    print(f"✅ Session ended: {ended_session_id}")
    print()
    
    # Show state after ending session
    print("📊 State after ending session:")
    with open(sm.state_file, 'r') as f:
        state_data = json.load(f)
    print(f"  • Current session: {state_data['current_session']}")
    print(f"  • Command history count: {len(state_data['command_history'])}")
    print()
    
    # Show final session file content
    print("📋 Final session file content:")
    with open(sm.session_file, 'r') as f:
        session_data = json.load(f)
    print(f"  • Status: {session_data['status']}")
    print()
    
    # Show command history
    print("📜 Command history:")
    for entry in state_data['command_history']:
        print(f"  • {entry['command']} at {entry['timestamp'][:19]} (session: {entry.get('session_id', 'N/A')})")
    print()
    
    print("🎉 Demo completed successfully!")


if __name__ == "__main__":
    demo_session_management()