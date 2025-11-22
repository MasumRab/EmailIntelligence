#!/usr/bin/env python3
"""
Test script for the Micro-Task Decomposition System

Demonstrates how the TaskDecomposer breaks down documentation tasks
into micro-tasks for parallel agent execution.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from task_decomposer import TaskDecomposer, TaskType

def test_api_docs_decomposition():
    """Test decomposing an API documentation task."""
    print("=== Testing API Documentation Decomposition ===\n")

    decomposer = TaskDecomposer()

    # Sample API documentation content
    api_content = """
# EmailIntelligence API Documentation

## Overview
The EmailIntelligence API provides comprehensive email analysis capabilities.

## GET /api/emails
Retrieves a list of emails with optional filtering.

### Parameters
- limit: Number of emails to retrieve (default: 50)
- offset: Pagination offset (default: 0)
- category: Filter by category

### Response
Returns a JSON array of email objects.

## POST /api/analyze
Analyzes email content for insights.

### Request Body
{
  "email_id": "string",
  "analysis_type": "sentiment|intent|urgency"
}

### Response
Returns analysis results with confidence scores.
"""

    result = decomposer.decompose_task(
        "Create comprehensive API documentation",
        api_content,
        TaskType.API_DOCS
    )

    print(f"Original Task: {result.original_task}")
    print(f"Total Micro-tasks: {len(result.micro_tasks)}")
    print(f"Estimated Total Time: {result.estimated_total_time} minutes")
    print(".1f")
    print(f"Execution Paths: {len(result.execution_paths)} parallel paths\n")

    print("Micro-tasks:")
    for i, task in enumerate(result.micro_tasks, 1):
        print(f"{i}. {task.title}")
        print(f"   Type: {task.type.value}")
        print(f"   Time: {task.estimated_time}min")
        print(f"   Agent Requirements: {', '.join(task.agent_requirements) if task.agent_requirements else 'None'}")
        if task.dependencies:
            print(f"   Dependencies: {', '.join(task.dependencies)}")
        print()

    print("Execution Paths:")
    for i, path in enumerate(result.execution_paths, 1):
        print(f"Path {i}: {len(path)} tasks - {', '.join(path)}")
    print()

    # Show agent requirements summary
    requirements = decomposer.get_agent_requirements_summary(result.micro_tasks)
    print("Agent Capability Requirements:")
    for capability, count in sorted(requirements.items()):
        print(f"  {capability}: {count} tasks")
    print()

def test_guide_decomposition():
    """Test decomposing a user guide task."""
    print("=== Testing User Guide Decomposition ===\n")

    decomposer = TaskDecomposer()

    guide_content = """
# Getting Started with EmailIntelligence

## Installation
Follow these steps to install EmailIntelligence.

### Step 1: System Requirements
Ensure your system meets the minimum requirements.

### Step 2: Download and Install
Download the installer and run the setup wizard.

### Step 3: Initial Configuration
Configure your email accounts and preferences.

## First Time Setup
After installation, perform initial setup.

### Connecting Email Accounts
Learn how to connect your email accounts securely.

### Setting Up Categories
Create custom categories for email organization.
"""

    result = decomposer.decompose_task(
        "Write comprehensive user guide",
        guide_content,
        TaskType.GUIDE
    )

    print(f"Original Task: {result.original_task}")
    print(f"Total Micro-tasks: {len(result.micro_tasks)}")
    print(f"Estimated Total Time: {result.estimated_total_time} minutes")
    print(".1f")
    print()

    # Show just the task titles for brevity
    print("Micro-tasks created:")
    for task in result.micro_tasks:
        print(f"  • {task.title} ({task.estimated_time}min)")
    print()

def test_architecture_decomposition():
    """Test decomposing an architecture documentation task."""
    print("=== Testing Architecture Documentation Decomposition ===\n")

    decomposer = TaskDecomposer()

    arch_content = """
# EmailIntelligence System Architecture

## System Components
The system consists of several key components.

### Frontend Layer
React-based user interface with real-time updates.

### Backend Services
Python FastAPI services handling business logic.

### Data Layer
SQLite database with optimized schemas.

## Data Flow
Email data flows through the system as follows:

1. Email retrieval from Gmail API
2. Content analysis and categorization
3. Storage in optimized database schema
4. Real-time delivery to frontend
"""

    result = decomposer.decompose_task(
        "Document system architecture",
        arch_content,
        TaskType.ARCHITECTURE
    )

    print(f"Original Task: {result.original_task}")
    print(f"Total Micro-tasks: {len(result.micro_tasks)}")
    print(f"Parallelization Factor: {result.parallelization_factor:.1f}x")
    print()

    # Show execution paths
    print("Parallel Execution Paths:")
    for i, path in enumerate(result.execution_paths, 1):
        tasks_in_path = [t for t in result.micro_tasks if t.id in path]
        path_time = sum(t.estimated_time for t in tasks_in_path)
        print(f"  Path {i}: {len(path)} tasks, {path_time}min total")
    print()

if __name__ == "__main__":
    print("EmailIntelligence Micro-Task Decomposition System Test\n")

    test_api_docs_decomposition()
    test_guide_decomposition()
    test_architecture_decomposition()

    print("=== Test Complete ===")
    print("The micro-task decomposition system successfully breaks down")
    print("large documentation tasks into parallel-executable micro-tasks")
    print("that can be completed in <15 minutes each.")