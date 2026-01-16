# Task Master AI Troubleshooting Guide

This guide helps resolve common issues with the Task Master AI integration in emailintelligence workflows.

## Quick Diagnosis

### Check System Status
```bash
# Overall system health check
task-master list

# Component-specific status
python scripts/task_completion_tracker.py --status
python scripts/incremental_validator.py --status
```

### View Recent Logs
```bash
# Check Task Master logs
task-master list  # Shows current state

# Check validation logs
tail -f logs/validation.log

# Check performance logs
python scripts/workflow_performance_monitor.py report
```

## Common Issues & Solutions

### 1. Task Master Initialization Fails

**Symptoms:**
- `task-master init` fails
- "Connection refused" or "Service unavailable" errors

**Solutions:**
```bash
# Check Task Master service
task-master models

# Restart Task Master service
task-master init --force

# Verify configuration
task-master models --setup
```

**Prevention:**
- Ensure Task Master AI is properly installed and configured
- Check network connectivity to Task Master endpoints
- Verify API keys and authentication tokens

### 2. Validation Scripts Not Running

**Symptoms:**
- Validation commands return no output
- Tasks show as "pending validation"
- Performance monitoring shows 0% validation rate

**Solutions:**
```bash
# Test individual validation scripts
python scripts/incremental_validator.py --test

# Check validation script permissions
ls -la scripts/validation_*.py

# Reinstall validation dependencies
pip install -r requirements-dev.txt
```

**Prevention:**
- Run validation scripts manually after installation
- Check file permissions regularly
- Keep validation scripts updated with main codebase

### 3. Cache Performance Issues

**Symptoms:**
- Slow validation times (>5 seconds per task)
- Cache hit rate below 50%
- Memory usage growing continuously

**Solutions:**
```bash
# Clear corrupted cache
python scripts/validation_cache_optimizer.py --clear

# Rebuild cache from scratch
python scripts/validation_cache_optimizer.py analyze

# Optimize cache settings
python scripts/validation_cache_optimizer.py optimize
```

**Prevention:**
- Monitor cache hit rates weekly
- Clear cache monthly during low-usage periods
- Adjust cache size based on available memory

### 4. Git Integration Problems

**Symptoms:**
- Stash operations fail
- Commit validation doesn't run
- Branch operations are slow

**Solutions:**
```bash
# Test git integration
./scripts/stash_manager.sh status

# Check git repository status
git status
git log --oneline -5

# Reset git integration
./scripts/stash_manager.sh reset
```

**Prevention:**
- Keep git repository clean and up-to-date
- Avoid concurrent git operations
- Use stash manager for complex branching scenarios

### 5. Performance Degradation

**Symptoms:**
- Workflow completion times increasing
- High CPU/memory usage
- System becoming unresponsive

**Solutions:**
```bash
# Generate performance diagnostic
python scripts/workflow_performance_monitor.py analyze

# Reset to baseline performance
python scripts/workflow_performance_monitor.py reset

# Apply performance optimizations
python scripts/validation_cache_optimizer.py optimize
```

**Prevention:**
- Monitor performance metrics daily
- Scale resources based on usage patterns
- Implement performance budgets for workflows

### 6. Task Dependencies Not Resolving

**Symptoms:**
- Tasks stuck in "waiting" status
- Circular dependency errors
- Invalid dependency chains

**Solutions:**
```bash
# Validate dependency graph
python scripts/task_dependency_resolver.py --validate

# Fix circular dependencies
python scripts/task_dependency_resolver.py --fix-circular

# Rebuild dependency cache
python scripts/task_dependency_resolver.py --rebuild
```

**Prevention:**
- Define dependencies explicitly when creating tasks
- Avoid creating circular dependencies
- Review dependency graphs during task planning

## Advanced Troubleshooting

### Log Analysis
```bash
# Search for specific error patterns
grep "ERROR" logs/taskmaster_*.log | tail -20

# Analyze performance bottlenecks
python scripts/workflow_performance_monitor.py analyze

# Export logs for external analysis
python scripts/task_completion_tracker.py --export-logs
```

### Configuration Validation
```bash
# Validate all configuration files
task-master models

# Check environment variables
env | grep -i taskmaster

# Test configuration changes
python scripts/incremental_validator.py --validate-config
```

### Database Issues
```bash
# Check database connectivity
python scripts/task_completion_tracker.py --check-db

# Repair database
python scripts/task_completion_tracker.py --repair-db

# Backup and restore
python scripts/task_completion_tracker.py --backup
python scripts/task_completion_tracker.py --restore backup_file
```

### Network Connectivity
```bash
# Test external service connectivity
curl -I https://api.github.com

# Check proxy settings
env | grep -i proxy

# Test local service ports
netstat -tlnp | grep :8000
```

## Emergency Procedures

### Complete System Reset
```bash
# Stop all services
pkill -f taskmaster
pkill -f validation

# Clear all caches and temporary files
python scripts/validation_cache_optimizer.py --clear
rm -rf .taskmaster/temp/*
rm -rf logs/*.log

# Reset configuration to defaults
task-master init --force
rm -f .taskmaster/config.json

# Restart services
task-master models --setup
```

### Data Recovery
```bash
# List available backups
ls -la backups/taskmaster_*

# Restore from latest backup
python scripts/task_completion_tracker.py --restore-latest

# Verify data integrity
python scripts/task_completion_tracker.py --verify-data
```

## Getting Help

### Support Resources
- **Documentation**: Task Master Integration README
- **Logs**: Check `logs/taskmaster_*.log` for detailed error information
- **Metrics**: Run `python scripts/workflow_performance_monitor.py report` for system health metrics
- **Community**: Search existing issues and discussions

### Escalation Steps
1. Check this troubleshooting guide
2. Review recent changes and deployments
3. Gather diagnostic information (logs, metrics, configuration)
4. Contact development team with complete diagnostic data
5. Escalate to infrastructure team if system-wide issues suspected

### Diagnostic Information to Collect
```bash
# System information
uname -a
python --version
node --version

# Task Master status
task-master list
task-master models

# Recent logs
tail -100 logs/validation.log

# Performance metrics
python scripts/workflow_performance_monitor.py report
```

## Prevention Best Practices

### Regular Maintenance
- Run health checks daily
- Monitor performance metrics weekly
- Update dependencies monthly
- Backup data regularly

### Monitoring Setup
- Set up alerts for critical metrics
- Monitor error rates and response times
- Track resource usage patterns
- Review logs for early warning signs

### Capacity Planning
- Monitor growth trends
- Plan for scaling requirements
- Test performance under load
- Maintain buffer capacity for spikes