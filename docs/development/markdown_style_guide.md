# Markdown Style Guide for EmailIntelligence

This document outlines the standards for formatting Markdown files in the EmailIntelligence project to ensure consistency across all documentation.

## 1. Document Structure

### Headings
- Use `#` for main title (H1) - only one per document
- Use `##` for main sections (H2) 
- Use `###` for subsections (H3)
- Use `####` for sub-subsections (H4) when needed
- Do not skip heading levels (e.g., don't go from H2 directly to H4)

Example:
```markdown
# Document Title
## Main Section
### Subsection
#### Sub-subsection
```

## 2. Text Formatting

### Bold Text
- Use `**double asterisks**` for bold text
- Do not use `__underscores__` for bold

### Italic Text
- Use `*single asterisks*` for italic text
- Do not use `_underscores_` for italic

### Code
- Use `backticks` for inline code
- Use triple backticks with language specification for code blocks:
  ```language
  // Code example
  ```

## 3. Lists

### Unordered Lists
- Use `-` (dash) for all list items
- Maintain one space between the dash and the content
- Use consistent indentation (2 spaces) for nested lists

Example:
```markdown
- First item
- Second item
  - Nested item
- Third item
```

### Ordered Lists
- Use `1.`, `2.`, `3.` for numbered lists
- You may use `1.` for all items and let the Markdown renderer auto-number

Example:
```markdown
1. First step
2. Second step
3. Third step
```

## 4. Code Blocks

### Language Specification
- Always specify the language after the opening triple backticks
- Use correct language identifiers: `python`, `javascript`, `bash`, `json`, `yaml`, etc.

Example:
```markdown
```python
def example_function():
    return "Hello, World!"
```
```

### Inline Code
- Use single backticks for variable names, code snippets, and technical terms
- Example: `function_name()`, `class MyExample`

## 5. Links and References

### Inline Links
- Use `[text](url)` format
- Place links immediately after the linked text without extra spaces

Example:
```markdown
[Learn more](https://example.com)
```

### Emojis
- Emojis are acceptable when they add meaning or visual cues
- Follow emojis with appropriate text, e.g., `⚠️ Warning`

## 6. Tables (when needed)

When tables are necessary, use proper formatting:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

## 7. Horizontal Rules

Use horizontal rules (`---`) to separate major sections when needed.

## 8. Best Practices

- End all files with a blank line
- Use line breaks to separate paragraphs
- Limit line length to 100 characters where possible for readability in terminals
- Use consistent terminology throughout all documentation
- When referring to project-specific terms, maintain capitalization consistency

## 9. File Organization

- Store documentation in the `docs/` directory
- Use descriptive, lowercase filenames with hyphens: `project-setup.md`
- Include a Table of Contents at the beginning of longer documents
- Use relative links between documentation files

## 10. Branch Consistency

This style guide should be followed across all branches to ensure documentation consistency when switching between branches or merging changes.