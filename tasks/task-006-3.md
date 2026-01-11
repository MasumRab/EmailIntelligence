# Task 006.3: Integrate Backup/Restore into Automated Workflow

**Status:** pending
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 7/10
**Dependencies:** 006.1, 006.2
**Created:** 2026-01-06
**Parent:** Task 006: Implement Robust Branch Backup and Restore Mechanism

---

## Purpose

Create central orchestration script that integrates backup/restore into alignment workflow.

---

## Details

Develop comprehensive script that manages backup, alignment, restore, and cleanup.

### Steps

1. **Create orchestration script**
   - Backup before alignment
   - Run alignment
   - Validate results
   - Handle failures with restore
   - Cleanup old backups

2. **Add robust error handling**

3. **Implement logging**

4. **Test complete workflow**

---

## Success Criteria

- [ ] Central orchestration working
- [ ] Backup before alignment
- [ ] Automatic restore on failure
- [ ] Cleanup of old backups
- [ ] Comprehensive logging

---

## Test Strategy

- Test complete workflow with mock alignment
- Test restore after simulated failure
- Test cleanup functionality
- Test error handling

---

## Implementation Notes

### Orchestration Script

```python
#!/usr/bin/env python3
"""Central backup/restore orchestration script."""

import subprocess
import sys
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupOrchestrator:
    def __init__(self, branch_name):
        self.branch = branch_name
        self.backup_name = None
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup(self):
        """Create backup before alignment."""
        logger.info(f"Creating backup of {self.branch}")
        self.backup_name = f"backup-{self.branch}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        result = subprocess.run(
            ["git", "branch", self.backup_name, self.branch],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            logger.info(f"Backup created: {self.backup_name}")
            return True
        else:
            logger.error(f"Backup failed: {result.stderr}")
            return False
    
    def run_alignment(self, alignment_script):
        """Run alignment operation."""
        logger.info("Running alignment")
        result = subprocess.run(
            [sys.executable, alignment_script, self.branch],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            logger.info("Alignment completed successfully")
            return True
        else:
            logger.error(f"Alignment failed: {result.stderr}")
            return False
    
    def restore(self):
        """Restore from backup if available."""
        if not self.backup_name:
            logger.error("No backup available for restore")
            return False
        
        logger.info(f"Restoring from backup: {self.backup_name}")
        
        subprocess.run(["git", "checkout", self.backup_name])
        subprocess.run(["git", "branch", "-f", self.branch, self.backup_name])
        subprocess.run(["git", "checkout", self.branch])
        
        logger.info(f"Restored {self.branch} from {self.backup_name}")
        return True
    
    def cleanup(self):
        """Remove temporary backup."""
        if self.backup_name:
            logger.info(f"Cleaning up backup: {self.backup_name}")
            subprocess.run(["git", "branch", "-D", self.backup_name])
    
    def orchestrate(self, alignment_script):
        """Run complete alignment workflow with backup."""
        try:
            if not self.backup():
                return False
            
            success = self.run_alignment(alignment_script)
            
            if success:
                self.cleanup()
                return True
            else:
                self.restore()
                return False
        
        except Exception as e:
            logger.error(f"Error during orchestration: {e}")
            self.restore()
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python backup_orchestrate.py <branch> <alignment_script>")
        sys.exit(1)
    
    orchestrator = BackupOrchestrator(sys.argv[1])
    success = orchestrator.orchestrate(sys.argv[2])
    sys.exit(0 if success else 1)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 006 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Feature branch backup working
- [ ] Primary branch backup working
- [ ] Orchestration script working
- [ ] Restore capability tested
