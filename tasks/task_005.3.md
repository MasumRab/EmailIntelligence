# Task UNKNOWN: Untitled Task

**Status:** pending
**Priority:** high
**Effort:** 5-6 hours
**Complexity:** 7/10
**Dependencies:** 005.1, 005.2

---

## Overview/Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

## Success Criteria

- [ ] - [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated
- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: UNKNOWN
- **Title**: Untitled Task
- **Status**: pending
- **Priority**: high
- **Effort**: 5-6 hours
- **Complexity**: 7/10

### Requirements
Requirements to be specified

## Implementation Guide

Implementation guide to be defined

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-005-3.md -->

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged
**Priority:** high
**Effort:** 5-6 hours
**Complexity:** 7/10
**Dependencies:** 005.1, 005.2
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged
**Dependencies:** 005.1, 005.2
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged
**Effort:** TBD
**Complexity:** TBD

## Overview/Purpose
Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - ...

## Success Criteria

- [ ] [Success criteria to be defined]

## Prerequisites & Dependencies

### Required Before Starting
- [ ] 005.1, 005.2
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged

### Blocks (What This Task Unblocks)
- [ ] None specified

### External Dependencies
- [ ] None

## Sub-subtasks Breakdown

# No subtasks defined

## Specification Details

### Task Interface
- **ID**: 
- **Title**: 
- **Status**: pending
**Priority:** high
**Effort:** 5-6 hours
**Complexity:** 7/10
**Dependencies:** 005.1, 005.2
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged
- **Priority**: high
**Effort:** 5-6 hours
**Complexity:** 7/10
**Dependencies:** 005.1, 005.2
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Integrate all error detection into a single comprehensive script with AST-based validation.

---

## Details

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

---

## Success Criteria

- [ ] All detection mechanisms integrated
- [ ] AST validation working
- [ ] Backend imports flagged with fixes
- [ ] Comprehensive report generated

---

## Test Strategy

- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

---

## Implementation Notes

### Main Consolidation Script

```python
#!/usr/bin/env python3
"""Comprehensive error detection script."""

import subprocess
import sys
import ast
import re
from pathlib import Path

class MergeErrorDetector:
    def __init__(self):
        self.errors = []
    
    def detect_merge_markers(self, files):
        """Detect conflict markers."""
        for f in files:
            if not Path(f).exists():
                continue
            with open(f) as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(('<<<<<<<', '=======', '>>>>>>>')):
                        self.errors.append(f"MERGE MARKER: {f}:{i}")
    
    def detect_deleted_files(self):
        """Detect deleted files."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=D"],
            capture_output=True, text=True
        )
        for f in result.stdout.strip().split('\n'):
            if f:
                self.errors.append(f"DELETED FILE: {f}")
    
    def detect_encoding_issues(self, files):
        """Detect encoding problems."""
        for f in files:
            if not Path(f).exists():
                continue
            try:
                with open(f, encoding='utf-8', errors='replace') as fp:
                    content = fp.read()
                    if '' in content:
                        self.errors.append(f"ENCODING ISSUE: {f}")
            except Exception as e:
                self.errors.append(f"READ ERROR: {f} - {e}")
    
    def validate_imports(self, files):
        """Validate Python imports exist."""
        for f in files:
            if not f.endswith('.py') or not Path(f).exists():
                continue
            try:
                with open(f) as fp:
                    tree = ast.parse(fp.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if not self._module_exists(alias.name):
                                self.errors(f"IMPORT ERROR: {f} - {alias.name}")
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if not self._module_exists(node.module):
                                self.errors.append(f"IMPORT ERROR: {f} - {node.module}")
                            if node.module.startswith('backend'):
                                self.errors.append(f"BACKEND MIGRATION: {f} - {node.module}")
            except Exception as e:
                self.errors.append(f"PARSE ERROR: {f} - {e}")
    
    def _module_exists(self, module_name):
        """Check if module exists."""
        # Check if module is a file
        module_path = Path(module_name.replace('.', '/'))
        if module_path.exists():
            return True
        # Check if module can be imported
        try:
            __import__(module_name.split('.')[0])
            return True
        except ImportError:
            return False
    
    def run(self):
        """Run all detection."""
        files = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        ).stdout.strip().split('\n')
        
        self.detect_merge_markers(files)
        self.detect_deleted_files()
        self.detect_encoding_issues(files)
        self.validate_imports(files)
        
        return self.errors

if __name__ == "__main__":
    detector = MergeErrorDetector()
    errors = detector.run()
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 005 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifacts detected
- [ ] Encoding issues detected
- [ ] Import validation working
- [ ] Backend migrations flagged
- **Effort**: N/A
- **Complexity**: N/A

## Implementation Guide

Combine all detection mechanisms and implement full import validation using Python AST.

### Steps

1. **Consolidate detection logic**
   - Merge artifact detection
   - Deleted module detection
   - Garbled text detection
   - Import extraction

2. **Implement AST-based validation**
   ```python
   import ast
   
   def validate_imports_ast(filepath):
       """Use AST to validate imports exist."""
       with open(filepath) as f:
           tree = ast.parse(f.read())
       
       for node in ast.walk(tree):
           if isinstance(node, ast.Import):
               for alias in node.names:
                   if not module_exists(alias.name):
                       yield f"Missing module: {alias.name}"
           
           elif isinstance(node, ast.ImportFrom):
               if node.module:
                   if not module_exists(node.module):
                       yield f"Missing module: {node.module}"
   ```

3. **Validate backend→src migration**
   - Check for 'backend' imports
   - Suggest correct 'src' paths

4. **Create comprehensive report**
   - All errors grouped by type
   - Suggested fixes

5. **Ensure safe execution**

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Test with all error types (should detect all)
- Test valid file (should pass)
- Test with mixed errors (should report all)

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

## Next Steps

- [ ] No next steps specified
- [ ] Additional steps to be defined


<!-- EXTENDED_METADATA
END_EXTENDED_METADATA -->

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: 5-6 hours
- **Complexity Level**: 7/10

## Testing Strategy

Test strategy to be defined

## Common Gotchas & Solutions

- [ ] No common gotchas identified

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated

## Next Steps

- [ ] Next steps to be defined
