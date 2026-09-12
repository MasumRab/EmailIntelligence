# Task Master AI Workflow Guide

This guide provides user-facing instructions for leveraging the integrated Task Master AI system in emailintelligence development workflows.

## Overview

The Task Master AI integration provides AI-powered task management with automated verification, performance monitoring, and intelligent caching for efficient development workflows.

## Quick Start

### 1. Initialize Task Master
```bash
# Initialize Task Master with a PRD or task description
task-master init
task-master parse-prd requirements.md
```

### 2. Start Working on Tasks
```bash
# List available tasks
task-master list

# Start working on a specific task
task-master next
task-master show 1
task-master start --task-id 1
```

### 3. Validate Progress
```bash
# Run automated validation
python scripts/incremental_validator.py --validate

# Check task completion
python scripts/task_completion_tracker.py --report
```

## Core Features

### AI-Powered Task Breakdown
Task Master automatically decomposes complex requirements into manageable micro-tasks with dependencies.

### Automated Verification
Built-in validation scripts ensure task completion meets quality standards.

### Performance Monitoring
Real-time tracking of workflow efficiency and bottleneck identification.

### Intelligent Caching
Optimized validation caching reduces redundant operations.

## Workflow Commands

### Task Management
```bash
# Create new task from description
task-master add-task --prompt="Implement user authentication system"

# List all tasks with status
task-master list

# Start working on specific task
task-master start --task-id 1

# Mark task as completed
task-master set-status --id=1 --status=done

# View task dependencies
task-master validate-dependencies
```

### Validation & Verification
```bash
# Run incremental validation
python scripts/incremental_validator.py --validate

# Run parallel validation
python scripts/parallel_validator.py --validate-all

# Validate specific component
python scripts/incremental_validator.py --files src/auth/
```

### Performance Monitoring
```bash
# Generate performance report
python scripts/workflow_performance_monitor.py report

# Monitor cache efficiency
python scripts/validation_cache_optimizer.py analyze

# Generate workflow report
python scripts/workflow_performance_monitor.py generate-report
```

### Git Operations
```bash
# Safe stash with validation
./scripts/stash_manager.sh safe-operation "auth implementation" "git checkout feature/auth"

# Smart commit with validation
./scripts/stash_manager.sh safe-operation "commit auth" "git commit -m 'feat: implement authentication'"

# Branch management
./scripts/stash_manager.sh safe-branch-switch feature/auth
```

## Best Practices

### Task Organization
- Break down large features into smaller, testable tasks
- Use descriptive task names that clearly indicate the work
- Establish dependencies early to prevent blocking issues

### Validation Workflow
- Run validation checks frequently during development
- Address validation failures immediately
- Use incremental validation for faster feedback

### Performance Optimization
- Monitor cache hit rates regularly
- Clean up unused cache entries periodically
- Review performance reports for optimization opportunities

## Troubleshooting

### Common Issues

#### Task Master Not Responding
```bash
# Check Task Master status
task-master list

# Restart Task Master service
task-master init --force

# Check configuration
task-master models
```

#### Validation Failures
```bash
# Run diagnostic validation
python scripts/incremental_validator.py --diagnose

# Clear validation cache
python scripts/validation_cache_optimizer.py --clear

# Check validation logs
tail -f logs/validation.log
```

#### Performance Issues
```bash
# Generate performance report
python scripts/workflow_performance_monitor.py report

# Analyze bottlenecks
python scripts/workflow_performance_monitor.py analyze

# Optimize settings
python scripts/validation_cache_optimizer.py optimize
```

### Getting Help

- Check the Task Master Integration Documentation
- Review AGENTS.md for development conventions
- Contact the development team for complex issues

## Advanced Usage

### Custom Workflows
Create custom workflow scripts by extending the base Task Master integration:

```python
from scripts.task_completion_tracker import TaskCompletionTracker
from scripts.incremental_validator import IncrementalValidator

# Create custom workflow
tracker = TaskCompletionTracker()
validator = IncrementalValidator()
tracker.record_completion(task)
validator.validate_files(changed_files)
```

### Integration with CI/CD
The Task Master system integrates with CI/CD pipelines for automated validation:

```yaml
# .github/workflows/ci.yml
- name: Task Master Validation
  run: |
    python scripts/incremental_validator.py --validate
    python scripts/task_completion_tracker.py --report
```

### Performance Tuning
Adjust performance settings based on your environment:

```bash
# High-performance mode
export VALIDATION_PARALLEL_WORKERS=8
export VALIDATION_CACHE_SIZE=2000

# Memory-optimized mode
export VALIDATION_PARALLEL_WORKERS=2
export VALIDATION_CACHE_SIZE=500
```

## Metrics & Reporting

### Key Performance Indicators
- **Task Completion Rate**: Percentage of tasks completed on time
- **Validation Success Rate**: Percentage of validations passing
- **Cache Hit Rate**: Efficiency of validation caching
- **Average Task Duration**: Time to complete typical tasks

### Generating Reports
```bash
# Task completion analytics
python scripts/task_completion_tracker.py --generate-report

# Validation performance
python scripts/workflow_performance_monitor.py report

# Cache efficiency
python scripts/validation_cache_optimizer.py analyze
```

## Support & Resources

- **Documentation**: Task Master Integration README
- **API Reference**: Check individual script docstrings for API details
- **Community**: Join development discussions for workflow improvements
- **Issues**: Report bugs and request features via GitHub issues