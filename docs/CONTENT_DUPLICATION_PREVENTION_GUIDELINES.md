# Content Duplication Prevention Guidelines

## Overview

This document outlines the methodology to prevent content duplication and corruption during task-to-todo creation processes. These guidelines were developed in response to issues identified in the Task 75 → Task 002 migration where 98.7% of success criteria were lost and extensive content duplication occurred.

## Root Causes of Duplication and Corruption

### 1. Over-Generalization of Scripts
- Scripts applied uniform transformations across entire codebase without considering file-specific requirements
- Applied templates repeatedly without checking if already present
- Failed to distinguish between unique content and template sections

### 2. Lack of Content Validation
- No validation to check if content was already present before adding
- No integrity checks to ensure content wasn't corrupted during transformation
- Missing duplicate detection mechanisms

### 3. Improper Migration Techniques
- Concatenated content from multiple sources without deduplication
- Didn't preserve original content boundaries during migration
- Applied transformations without proper backup/recovery mechanisms

## Prevention Methodology

### 1. Content Validation Framework

#### Pre-processing Validation
```python
def validate_content_before_add(content_to_add, target_file_content):
    """Check if content already exists before adding."""
    # Check for exact matches
    if content_to_add in target_file_content:
        return False, "Content already exists"
    
    # Check for partial matches (similar sections)
    if is_similar_content(content_to_add, target_file_content):
        return False, "Similar content already exists"
    
    return True, "Content is unique"
```

#### Integrity Validation
```python
def validate_content_integrity(content):
    """Verify content structure and formatting."""
    # Check for proper markdown structure
    if not has_proper_headers(content):
        return False, "Missing proper headers"
    
    # Check for balanced sections
    if not has_balanced_sections(content):
        return False, "Unbalanced sections"
    
    # Check for valid links and references
    if not has_valid_references(content):
        return False, "Invalid references"
    
    return True, "Content is valid"
```

#### Duplicate Detection
```python
def detect_duplicates(content_blocks):
    """Scan for duplicate content blocks."""
    seen_content = set()
    duplicates = []
    
    for block in content_blocks:
        block_hash = hash_content_block(block)
        if block_hash in seen_content:
            duplicates.append(block)
        else:
            seen_content.add(block_hash)
    
    return duplicates
```

### 2. Template Application Controls

#### Single Application Enforcement
```python
def apply_template_once(template_name, target_file, template_content):
    """Ensure templates are applied only once per file."""
    # Check if template already applied
    if is_template_applied(target_file, template_name):
        return False, f"Template {template_name} already applied"
    
    # Apply template
    add_template_to_file(target_file, template_content)
    
    # Mark template as applied
    mark_template_as_applied(target_file, template_name)
    
    return True, f"Template {template_name} applied successfully"
```

#### Conditional Application
```python
def apply_template_conditionally(template_name, target_file, template_content):
    """Apply templates only if not already present."""
    # Check if template sections already exist
    required_sections = get_template_sections(template_name)
    existing_sections = get_existing_sections(target_file)
    
    missing_sections = set(required_sections) - set(existing_sections)
    
    if not missing_sections:
        return False, "All template sections already present"
    
    # Apply only missing sections
    apply_missing_sections(target_file, template_content, missing_sections)
    
    return True, f"Applied missing sections: {missing_sections}"
```

### 3. Atomic Operations

#### Transaction-Based Changes
```python
def atomic_content_operation(operation_func, *args, **kwargs):
    """Either complete the entire operation or revert completely."""
    # Create backup
    backup = create_file_backup(kwargs.get('target_file'))
    
    try:
        # Perform operation
        result = operation_func(*args, **kwargs)
        
        # Validate result
        if not validate_content_integrity(kwargs.get('target_file')):
            # Revert to backup
            restore_from_backup(backup)
            return False, "Operation failed validation, reverted"
        
        return True, result
    except Exception as e:
        # Revert to backup on error
        restore_from_backup(backup)
        return False, f"Operation failed with error: {str(e)}, reverted"
```

### 4. Content Boundary Management

#### Preserve Original Content
```python
def preserve_original_content(original_content, new_content):
    """Keep original content separate from generated content."""
    # Use clear delimiters
    preserved_section = f"<!-- ORIGINAL_CONTENT_START -->\n{original_content}\n<!-- ORIGINAL_CONTENT_END -->"
    generated_section = f"<!-- GENERATED_CONTENT_START -->\n{new_content}\n<!-- GENERATED_CONTENT_END -->"
    
    return f"{preserved_section}\n\n{generated_section}"
```

#### Source Attribution
```python
def add_source_attribution(content, source_file):
    """Track which source each content section originated from."""
    return f"<!-- IMPORTED_FROM: {source_file} -->\n{content}"
```

## Best Practices for Task-to-Todo Creation

### 1. Before Processing
- Create backup of original files
- Validate that target files exist and are accessible
- Check for existing content to avoid duplication
- Verify file format and structure

### 2. During Processing
- Apply content validation at each step
- Use atomic operations to prevent partial changes
- Track applied transformations
- Validate content integrity after each operation

### 3. After Processing
- Verify all required sections are present
- Check for unintended content duplication
- Validate file structure and formatting
- Update documentation with changes made

## Quality Assurance Checks

### 1. Content Uniqueness Check
```bash
# Check for duplicate sections in files
grep -n "^## " file.md | sort | uniq -D -w 2
```

### 2. Template Application Check
```bash
# Verify template sections are applied correctly
for template_section in $(cat TEMPLATE_SECTIONS.txt); do
  if ! grep -q "$template_section" file.md; then
    echo "Missing template section: $template_section"
  fi
done
```

### 3. Content Boundary Check
```bash
# Verify content boundaries are preserved
grep -c "ORIGINAL_CONTENT_START\|GENERATED_CONTENT_START" file.md
```

## Recovery Procedures

### 1. Duplicate Content Removal
```python
def remove_duplicate_content(file_path):
    """Remove duplicate content from file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split content into logical blocks
    blocks = split_into_blocks(content)
    
    # Remove duplicate blocks
    unique_blocks = remove_duplicates(blocks)
    
    # Reassemble content
    new_content = join_blocks(unique_blocks)
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(new_content)
```

### 2. Content Integrity Restoration
```python
def restore_content_integrity(file_path):
    """Restore content integrity using backup and validation."""
    # Load backup if available
    if backup_exists(file_path):
        backup_content = load_backup(file_path)
        
        # Validate backup content
        if validate_content_integrity(backup_content)[0]:
            # Restore from backup
            restore_from_backup(file_path, backup_content)
            return True
    
    return False
```

## Monitoring and Alerting

### 1. Duplication Detection
- Monitor for files with excessive repetition of sections
- Alert when content duplication exceeds threshold (e.g., 20% of file)
- Track template application frequency to detect over-application

### 2. Integrity Monitoring
- Monitor file structure and formatting
- Alert when files become malformed
- Track content validation failures

## Implementation Checklist

- [ ] Implement content validation framework
- [ ] Add duplicate detection mechanisms
- [ ] Create template application controls
- [ ] Implement atomic operations
- [ ] Add content boundary management
- [ ] Update all migration scripts with validation
- [ ] Create backup and recovery mechanisms
- [ ] Add monitoring and alerting
- [ ] Train team on prevention methodology
- [ ] Document procedures in AGENTS.md

## Conclusion

By implementing these prevention guidelines, we can avoid the content duplication and corruption issues that occurred during the Task 75 → Task 002 migration. The key is to validate content before adding, apply templates conditionally, use atomic operations, and preserve content boundaries.