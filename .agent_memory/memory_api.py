#!/usr/bin/env python3
"""
Agent Memory API - Structured session logging and retrieval for agentic workflows.

This module provides a simple, JSON-based memory system for tracking agent activities,
decisions, dependencies, and outstanding todos across sessions.

Usage:
    from memory_api import AgentMemory
    
    memory = AgentMemory()
    memory.load_session()
    
    # Log work
    memory.add_work_log("Analyzed task files", "Started documentation phase")
    
    # Track objectives
    memory.update_objective("obj_1", "completed")
    
    # Query memory
    blocked_tasks = memory.get_blocked_tasks()
    outstanding = memory.get_outstanding_todos()
    
    memory.save_session()
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class AgentMemory:
    """
    Manages agent session memory in structured JSON format.
    
    Provides:
    - Session tracking (metadata, objectives, artifacts)
    - Work logging (timestamped activities)
    - Dependency tracking (task blocking relationships)
    - Decision history (with rationale and impact)
    - Outstanding todos (prioritized action items)
    """
    
    def __init__(self, memory_dir: str = ".agent_memory"):
        """Initialize agent memory system.
        
        Args:
            memory_dir: Directory for memory files (default: .agent_memory)
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.session_file = self.memory_dir / "session_log.json"
        self.memory = {}
        
    def load_session(self) -> bool:
        """Load existing session memory.
        
        Returns:
            True if loaded, False if file doesn't exist
        """
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.memory = json.load(f)
                return True
            except json.JSONDecodeError:
                print(f"Error loading session from {self.session_file}")
                return False
        return False
    
    def save_session(self) -> bool:
        """Save session memory to disk.
        
        Returns:
            True if saved successfully
        """
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving session: {e}")
            return False
    
    def get_session_metadata(self) -> Dict[str, Any]:
        """Get current session metadata."""
        return self.memory.get("session_metadata", {})
    
    def get_objectives(self, status: Optional[str] = None) -> List[Dict]:
        """Get objectives, optionally filtered by status.
        
        Args:
            status: Filter by status (e.g., 'completed', 'in_progress', 'pending')
        
        Returns:
            List of objectives
        """
        objectives = self.memory.get("objectives", [])
        if status:
            objectives = [o for o in objectives if o.get("status") == status]
        return objectives
    
    def update_objective(self, obj_id: str, status: str, completion_date: Optional[str] = None) -> bool:
        """Update objective status.
        
        Args:
            obj_id: Objective ID
            status: New status
            completion_date: ISO format date (default: now if completing)
        
        Returns:
            True if updated
        """
        objectives = self.memory.get("objectives", [])
        for obj in objectives:
            if obj.get("id") == obj_id:
                obj["status"] = status
                if status == "completed" and not completion_date:
                    obj["completion_date"] = datetime.utcnow().isoformat() + "Z"
                elif completion_date:
                    obj["completion_date"] = completion_date
                return True
        return False
    
    def add_work_log(self, action: str, details: str, status: str = "completed") -> bool:
        """Add work log entry.
        
        Args:
            action: Brief action description
            details: Detailed information
            status: Status (default: 'completed')
        
        Returns:
            True if added
        """
        work_log = self.memory.get("work_log", [])
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "details": details,
            "status": status
        }
        work_log.append(entry)
        self.memory["work_log"] = work_log
        return True
    
    def get_work_log(self, status: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get work log entries.
        
        Args:
            status: Filter by status
            limit: Maximum entries to return
        
        Returns:
            List of work log entries (most recent first)
        """
        log = self.memory.get("work_log", [])
        if status:
            log = [e for e in log if e.get("status") == status]
        return log[-limit:][::-1]  # Return most recent first
    
    def add_artifact(self, artifact_id: str, name: str, description: str, 
                     file_path: str, status: str = "created") -> bool:
        """Add artifact entry.
        
        Args:
            artifact_id: Unique artifact identifier
            name: Artifact name
            description: Detailed description
            file_path: Path to artifact file
            status: Status (created, verified, deployed)
        
        Returns:
            True if added
        """
        artifacts = self.memory.get("artifacts_created", [])
        artifact = {
            "id": artifact_id,
            "name": name,
            "description": description,
            "file_path": file_path,
            "status": status
        }
        artifacts.append(artifact)
        self.memory["artifacts_created"] = artifacts
        return True
    
    def get_blocked_tasks(self) -> List[Dict]:
        """Get tasks that are currently blocked.
        
        Returns:
            List of blocked task statuses
        """
        dependencies = self.memory.get("dependencies", {})
        blocked = []
        for task_id, task_info in dependencies.items():
            if task_info.get("status") == "blocked":
                blocked.append({
                    "task": task_id,
                    "blocked_by": task_info.get("blocked_by", []),
                    "blocks": task_info.get("blocks", [])
                })
        return blocked
    
    def get_ready_tasks(self) -> List[str]:
        """Get tasks ready for implementation (not blocked).
        
        Returns:
            List of ready task IDs
        """
        dependencies = self.memory.get("dependencies", {})
        ready = []
        for task_id, task_info in dependencies.items():
            if task_info.get("status") == "ready_for_implementation":
                ready.append(task_id)
        return ready
    
    def get_outstanding_todos(self, priority: Optional[str] = None, 
                             status: Optional[str] = None) -> List[Dict]:
        """Get outstanding todos.
        
        Args:
            priority: Filter by priority (high, medium, low)
            status: Filter by status (pending, in_progress, blocked)
        
        Returns:
            List of outstanding todos
        """
        todos = self.memory.get("outstanding_todos", [])
        
        if priority:
            todos = [t for t in todos if t.get("priority") == priority]
        if status:
            todos = [t for t in todos if t.get("status") == status]
        
        # Sort by priority: high > medium > low
        priority_order = {"high": 0, "medium": 1, "low": 2}
        todos.sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 1))
        
        return todos
    
    def add_todo(self, todo_id: str, title: str, description: str,
                 priority: str = "medium", depends_on: Optional[List[str]] = None) -> bool:
        """Add outstanding todo.
        
        Args:
            todo_id: Unique todo identifier
            title: Brief title
            description: Detailed description
            priority: Priority level (high, medium, low)
            depends_on: List of todo IDs this depends on
        
        Returns:
            True if added
        """
        todos = self.memory.get("outstanding_todos", [])
        todo = {
            "id": todo_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "assigned_to": self.memory.get("session_metadata", {}).get("agent_name", "Unknown"),
            "depends_on": depends_on or []
        }
        todos.append(todo)
        self.memory["outstanding_todos"] = todos
        return True
    
    def update_todo(self, todo_id: str, status: str) -> bool:
        """Update todo status.
        
        Args:
            todo_id: Todo ID
            status: New status (pending, in_progress, completed, blocked)
        
        Returns:
            True if updated
        """
        todos = self.memory.get("outstanding_todos", [])
        for todo in todos:
            if todo.get("id") == todo_id:
                todo["status"] = status
                return True
        return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics.
        
        Returns:
            Dictionary of metrics
        """
        return self.memory.get("metrics", {})
    
    def update_metrics(self, **kwargs) -> bool:
        """Update metrics.
        
        Args:
            **kwargs: Metric key-value pairs
        
        Returns:
            True if updated
        """
        metrics = self.memory.get("metrics", {})
        metrics.update(kwargs)
        self.memory["metrics"] = metrics
        return True
    
    def get_context(self) -> Dict[str, Any]:
        """Get session context (directory, project, etc)."""
        return self.memory.get("context", {})
    
    def add_decision(self, decision_id: str, decision: str, rationale: str, 
                     impact: str) -> bool:
        """Log a significant decision.
        
        Args:
            decision_id: Unique decision identifier
            decision: Description of the decision
            rationale: Why this decision was made
            impact: Impact on the project
        
        Returns:
            True if added
        """
        decisions = self.memory.get("decisions", [])
        entry = {
            "id": decision_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "decision": decision,
            "rationale": rationale,
            "impact": impact
        }
        decisions.append(entry)
        self.memory["decisions"] = decisions
        return True
    
    def print_summary(self) -> None:
        """Print human-readable summary of session state."""
        print("\n" + "="*80)
        print("AGENT MEMORY SUMMARY")
        print("="*80)
        
        metadata = self.get_session_metadata()
        print(f"\nSession ID: {metadata.get('session_id')}")
        print(f"Agent: {metadata.get('agent_name')}")
        print(f"Project: {metadata.get('project')}")
        
        # Objectives
        objectives = self.get_objectives()
        print(f"\nObjectives: {len(objectives)}")
        for obj in objectives:
            print(f"  [{obj['status'].upper()}] {obj['title']}")
        
        # Outstanding todos
        todos = self.get_outstanding_todos()
        if todos:
            print(f"\nOutstanding Todos: {len(todos)}")
            for todo in todos[:5]:  # Show top 5
                print(f"  [{todo['priority'].upper()}] {todo['title']}")
        
        # Ready tasks
        ready = self.get_ready_tasks()
        if ready:
            print(f"\nReady for Implementation: {len(ready)}")
            for task in ready:
                print(f"  - {task}")
        
        # Blocked tasks
        blocked = self.get_blocked_tasks()
        if blocked:
            print(f"\nBlocked Tasks: {len(blocked)}")
            for task_info in blocked:
                print(f"  - {task_info['task']} (blocked by {', '.join(task_info['blocked_by'])})")
        
        # Metrics
        metrics = self.get_metrics()
        if metrics:
            print(f"\nMetrics:")
            for key, value in list(metrics.items())[:5]:
                print(f"  {key}: {value}")
        
        print("\n" + "="*80 + "\n")


def create_or_load_memory(memory_dir: str = ".agent_memory") -> AgentMemory:
    """Convenience function to create or load agent memory.
    
    Args:
        memory_dir: Directory for memory files
    
    Returns:
        Initialized AgentMemory instance
    """
    memory = AgentMemory(memory_dir)
    memory.load_session()
    return memory


if __name__ == "__main__":
    # Example usage
    memory = create_or_load_memory(".agent_memory")
    memory.print_summary()
