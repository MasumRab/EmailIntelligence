# Task 005.2: Implement Garbled Text Detection and Import Extraction

**Status:** pending
**Priority:** high
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 005.1
**Created:** 2026-01-06
**Parent:** Task 005: Develop Automated Error Detection Scripts for Merges

---

## Purpose

Detect encoding issues and extract import statements from Python files.

---

## Details

Implement garbled text detection and basic import extraction for Python files.

### Steps

1. **Detect encoding issues**
   - Open files with utf-8 and error replacement
   - Check for replacement characters ()
   - Flag potential encoding errors

2. **Extract import statements**
   ```python
   import re
   IMPORT_PATTERN = re.compile(r'^(?:from|import)\s+(\S+)')
   
   def extract_imports(filepath):
       imports = []
       with open(filepath) as f:
           for line in f:
               match = IMPORT_PATTERN.match(line)
               if match:
                   imports.append(match.group(1))
       return imports
   ```

3. **Track backend→src migration imports**
   - Flag imports still pointing to 'backend'

4. **Generate detailed report**

---

## Success Criteria

- [ ] Encoding issues detected
- [ ] Imports extracted from Python files
- [ ] Backend imports flagged
- [ ] Clear error reporting

---

## Test Strategy

- Create file with encoding issues (should detect)
- Extract imports from valid Python (should extract)
- Test with backend imports (should flag)

---

## Implementation Notes

### Garbled Text Detection

```python
def detect_encoding_issues(filepath):
    """Check for encoding problems."""
    issues = []
    try:
        with open(filepath, encoding='utf-8', errors='replace') as f:
            content = f.read()
            if '' in content:
                issues.append(f"Replacement characters found in {filepath}")
            if '\x00' in content:
                issues.append(f"Null bytes found in {filepath}")
    except UnicodeDecodeError as e:
        issues.append(f"Decode error in {filepath}: {e}")
    return issues
```

### Import Extraction

```python
def extract_python_imports(filepath):
    """Extract import statements from Python file."""
    imports = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('import '):
                modules = line.replace('import ', '').split(',')
                for m in modules:
                    m = m.strip().split(' as ')[0]
                    imports.append(m)
            elif line.startswith('from '):
                match = re.match(r'from\s+(\S+)', line)
                if match:
                    imports.append(match.group(1))
    return imports
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 005.3**: Consolidate Error Detection
