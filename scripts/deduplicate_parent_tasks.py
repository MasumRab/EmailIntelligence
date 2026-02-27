#!/usr/bin/env python3
"""Deduplicate bloated parent task files by merging best content from repeated sections.

Each bloated parent task file contains 6-9 copies of its content concatenated
together. This script:
1. Splits the file into sections based on ## headings
2. Groups sections by their canonical standard name
3. Picks the BEST (longest, most detailed) content for each standard section
4. Assembles the output in the 14-section standard order
5. Strips IMPORTED_FROM markers
6. Preserves the original # header and metadata

Usage:
    python scripts/deduplicate_parent_tasks.py --dry-run     # Preview changes
    python scripts/deduplicate_parent_tasks.py               # Apply changes
    python scripts/deduplicate_parent_tasks.py --file task_009.md  # Single file
"""

import argparse
import os
import re
import sys
from collections import defaultdict

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tasks")

# Canonical section names in standard order (sections 2-14)
STANDARD_ORDER = [
    "Overview/Purpose",
    "Success Criteria",
    "Prerequisites & Dependencies",
    "Sub-subtasks Breakdown",
    "Specification Details",
    "Implementation Guide",
    "Configuration Parameters",
    "Performance Targets",
    "Testing Strategy",
    "Common Gotchas & Solutions",
    "Integration Checkpoint",
    "Done Definition",
    "Next Steps",
]

# Map variant headings to canonical names
HEADING_ALIASES = {
    "## Overview/Purpose": "Overview/Purpose",
    "## Purpose": "Overview/Purpose",
    "## Overview": "Overview/Purpose",
    "## Success Criteria": "Success Criteria",
    "## Prerequisites & Dependencies": "Prerequisites & Dependencies",
    "## Prerequisites": "Prerequisites & Dependencies",
    "## Sub-subtasks Breakdown": "Sub-subtasks Breakdown",
    "## Sub-subtasks": "Sub-subtasks Breakdown",
    "## Subtasks Breakdown": "Sub-subtasks Breakdown",
    "## Subtasks": "Sub-subtasks Breakdown",
    "## Specification Details": "Specification Details",
    "## Specification": "Specification Details",
    "## Implementation Guide": "Implementation Guide",
    "## Implementation": "Implementation Guide",
    "## Implementation Notes": "Implementation Guide",
    "## Configuration Parameters": "Configuration Parameters",
    "## Configuration & Defaults": "Configuration Parameters",
    "## Configuration": "Configuration Parameters",
    "## Performance Targets": "Performance Targets",
    "## Testing Strategy": "Testing Strategy",
    "## Test Strategy": "Testing Strategy",
    "## Common Gotchas & Solutions": "Common Gotchas & Solutions",
    "## Common Gotchas": "Common Gotchas & Solutions",
    "## Integration Checkpoint": "Integration Checkpoint",
    "## Done Definition": "Done Definition",
    "## Next Steps": "Next Steps",
    "## Details": "Specification Details",  # Old format -> Specification Details
}

# Non-standard sections to DISCARD (old format cruft, redundant tracking)
DISCARD_SECTIONS = {
    "## EXPANSION COMMANDS",
    "## Progress Tracking",
    "## Subtask Status Summary",
    "## Key Files",
    "## Notes",
    "## Dependencies Summary",
    "## Target Branch Context",
    "## Action Plan (From Backlog)",
    "## Estimated Effort (From Backlog)",
    "## Success Criteria (From Backlog)",
    "## Subtask Definitions",
    "## Summary",
}

# Non-standard sections to KEEP if they contain useful content (first occurrence only)
KEEP_SECTIONS = {
    "## Architecture Overview",
    "## Architecture Alignment Guidance Integration",
    "## Integration with Task 001",
    "## Integration with Task 002",
    "## DEPENDENCY GRAPH",
    "## Progress Log",
}

BLOATED_FILES = [
    "task_001.md", "task_002.md", "task_005.md", "task_008.md", "task_009.md",
    "task_013.md", "task_014.md", "task_015.md", "task_016.md", "task_017.md",
    "task_018.md", "task_019.md", "task_020.md", "task_021.md", "task_022.md",
    "task_023.md", "task_024.md", "task_025.md",
]


def parse_sections(content):
    """Parse a markdown file into sections.
    
    Returns:
        header_block: Everything before the first ## heading (# title + metadata)
        sections: list of (heading_text, body_text, line_number) tuples
    """
    lines = content.split('\n')
    header_lines = []
    sections = []
    current_heading = None
    current_body = []
    current_line = 0
    in_header = True
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect ## headings (but not ### or deeper)
        if stripped.startswith('## ') and not stripped.startswith('### '):
            if in_header:
                in_header = False
                header_block = '\n'.join(header_lines)
            
            # Save previous section
            if current_heading is not None:
                sections.append((current_heading, '\n'.join(current_body), current_line))
            
            current_heading = stripped
            current_body = []
            current_line = i + 1
        elif in_header:
            header_lines.append(line)
        else:
            current_body.append(line)
    
    # Save last section
    if current_heading is not None:
        sections.append((current_heading, '\n'.join(current_body), current_line))
    
    if in_header:
        header_block = '\n'.join(header_lines)
    
    return header_block, sections


def strip_imported_from(text):
    """Remove <!-- IMPORTED_FROM: ... --> markers."""
    return re.sub(r'\n*<!-- IMPORTED_FROM:.*?-->\n*', '\n', text)


def clean_body(body):
    """Clean up a section body: strip trailing whitespace, normalize blank lines."""
    # Remove IMPORTED_FROM markers
    body = strip_imported_from(body)
    # Strip trailing whitespace
    body = body.rstrip()
    # Remove excessive blank lines (max 2 consecutive)
    body = re.sub(r'\n{4,}', '\n\n\n', body)
    return body


def score_section(body, section_name=""):
    """Score a section body for quality/completeness.
    
    Higher score = better content. Factors:
    - Length (more content is better, up to a point)
    - Has code blocks, checkboxes, tables
    - Task-specific references (task IDs, commit messages, handoff targets)
    - NOT just "to be defined" stubs
    - NOT generic boilerplate
    """
    if not body.strip():
        return 0
    
    text = body.strip()
    
    # Stub/placeholder detection
    stub_phrases = [
        "to be defined", "to be specified", "tbd", "[purpose to be defined]",
        "[overview to be defined]", "[success criteria to be defined]",
        "[specification to be defined]", "[implementation guide to be defined]",
        "[configuration parameters to be defined]", "[performance targets to be defined]",
        "[testing strategy to be defined]", "[common gotchas to be defined]",
        "[integration checkpoint to be defined]", "[done definition to be defined]",
        "[next steps to be defined]", "requirements to be specified",
        "- [ ] no next steps specified", "- [ ] additional steps to be defined",
    ]
    lower_text = text.lower()
    for stub in stub_phrases:
        if stub in lower_text and len(text) < 200:
            return 1  # Very low score for stubs
    
    # Generic boilerplate detection — penalize heavily
    generic_phrases = [
        "### completion criteria",
        "- [ ] all success criteria checkboxes marked complete",
        "- [ ] code quality standards met",
        "- [ ] performance targets achieved",
        "- [ ] all subtasks completed",
        "- [ ] integration checkpoint criteria satisfied",
        "### criteria for moving forward",
        "- [ ] all success criteria met",
        "- [ ] tests passing",
        "- [ ] documentation updated",
        "- [ ] no critical or high severity issues",
        "- **owner**: tbd",
        "- **initiative**: tbd",
        "- **scope**: tbd",
        "- **focus**: tbd",
    ]
    generic_count = sum(1 for gp in generic_phrases if gp in lower_text)
    
    score = 0
    
    # Length score (diminishing returns after 500 chars)
    score += min(len(text), 2000) / 100
    
    # Bonus for structured content
    score += text.count('- [ ]') * 2  # Checkboxes
    score += text.count('```') * 3    # Code blocks
    score += text.count('|') * 0.5    # Table rows
    score += text.count('### ') * 2   # Sub-headings
    score += text.count('**') * 0.3   # Bold emphasis
    
    # Strong bonus for task-specific content
    score += len(re.findall(r'Task \d{3}', text)) * 5      # Task references
    score += len(re.findall(r'\d{3}\.\d+', text)) * 3      # Subtask IDs
    score += text.count('feat: complete') * 10               # Commit messages
    score += text.count('hand-off to') * 8                   # Handoff targets
    score += text.count('Ready for') * 5                     # Ready-for transitions
    score += text.count('is done when') * 10                 # Task-specific done criteria
    score += text.count('Immediate:') * 5                    # Specific next steps
    score += text.count('Week ') * 3                         # Timeline references
    score += len(re.findall(r'✅', text)) * 3               # Completion markers
    
    # Heavy penalty for generic boilerplate
    if generic_count >= 3:
        score *= 0.3
    elif generic_count >= 2:
        score *= 0.5
    
    # Penalty for very short content
    if len(text) < 50:
        score *= 0.5
    
    return score


def deduplicate_file(filepath, dry_run=False):
    """Deduplicate a single parent task file.
    
    Returns (original_lines, new_lines, changes_made) tuple.
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original_lines = len(content.split('\n'))
    header_block, sections = parse_sections(content)
    
    # Clean header: strip IMPORTED_FROM from header too
    header_block = strip_imported_from(header_block)
    header_block = header_block.rstrip()
    
    # Group sections by canonical name
    canonical_groups = defaultdict(list)  # canonical_name -> [(body, line_num, original_heading)]
    extra_sections = []  # Non-standard sections to potentially keep
    discarded_sections = []
    
    for heading, body, line_num in sections:
        canonical = HEADING_ALIASES.get(heading)
        
        if canonical:
            canonical_groups[canonical].append((body, line_num, heading))
        elif heading in DISCARD_SECTIONS:
            discarded_sections.append((heading, line_num))
        elif heading in KEEP_SECTIONS:
            extra_sections.append((heading, body, line_num))
        else:
            # Unknown section - check if it's a duplicate of a known one
            # by looking for partial matches
            matched = False
            for alias_heading, canon in HEADING_ALIASES.items():
                if heading.startswith(alias_heading.split(':')[0]):
                    canonical_groups[canon].append((body, line_num, heading))
                    matched = True
                    break
            
            if not matched:
                # Keep it as extra if it has substantial content
                if score_section(body) > 5:
                    extra_sections.append((heading, body, line_num))
                else:
                    discarded_sections.append((heading, line_num))
    
    # For each canonical section, pick the BEST body
    best_sections = {}
    for canonical_name in STANDARD_ORDER:
        candidates = canonical_groups.get(canonical_name, [])
        if not candidates:
            continue
        
        # Score each candidate and pick the best
        scored = [(score_section(body), body, line_num, heading) 
                  for body, line_num, heading in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        
        best_score, best_body, best_line, best_heading = scored[0]
        best_sections[canonical_name] = clean_body(best_body)
    
    # Deduplicate extra sections (keep only first occurrence of each heading)
    seen_extra = set()
    unique_extras = []
    for heading, body, line_num in extra_sections:
        if heading not in seen_extra:
            seen_extra.add(heading)
            cleaned = clean_body(body)
            if cleaned.strip():
                unique_extras.append((heading, cleaned))
    
    # Assemble the output
    output_parts = [header_block]
    output_parts.append('')  # blank line after header
    
    for canonical_name in STANDARD_ORDER:
        body = best_sections.get(canonical_name, '')
        heading = f"## {canonical_name}"
        
        if body.strip():
            output_parts.append('')
            output_parts.append(heading)
            output_parts.append(body)
            output_parts.append('')
            output_parts.append('---')
        else:
            # Add stub for missing required sections
            output_parts.append('')
            output_parts.append(heading)
            output_parts.append('')
            output_parts.append(f'[{canonical_name} to be defined]')
            output_parts.append('')
            output_parts.append('---')
    
    # Append unique extra sections at the end (before the final ---)
    if unique_extras:
        for heading, body in unique_extras:
            output_parts.append('')
            output_parts.append(heading)
            output_parts.append(body)
            output_parts.append('')
            output_parts.append('---')
    
    output = '\n'.join(output_parts)
    # Normalize: remove excessive blank lines and trailing whitespace
    output = re.sub(r'\n{4,}', '\n\n\n', output)
    # Remove double --- separators
    output = re.sub(r'---\s*\n\s*---', '---', output)
    # Remove trailing --- at end of section bodies (before the one we add)
    output = re.sub(r'\n---\n\n---', '\n\n---', output)
    output = output.rstrip() + '\n'
    
    new_lines = len(output.split('\n'))
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
    
    return original_lines, new_lines, len(sections), len(discarded_sections)


def main():
    parser = argparse.ArgumentParser(description="Deduplicate bloated parent task files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--file", help="Process a single file (e.g., task_009.md)")
    parser.add_argument("--tasks-dir", default=TASKS_DIR, help="Path to tasks directory")
    args = parser.parse_args()
    
    if args.file:
        files = [args.file]
    else:
        files = BLOATED_FILES
    
    total_original = 0
    total_new = 0
    
    print("=" * 70)
    print("PARENT TASK DEDUPLICATION REPORT")
    print("=" * 70)
    if args.dry_run:
        print("MODE: DRY RUN (no files modified)")
    else:
        print("MODE: APPLYING CHANGES")
    print("=" * 70)
    print()
    
    print(f"{'File':<20} {'Original':>10} {'New':>10} {'Reduction':>10} {'Sections':>10} {'Discarded':>10}")
    print("-" * 70)
    
    for fname in files:
        fpath = os.path.join(args.tasks_dir, fname)
        if not os.path.exists(fpath):
            print(f"  SKIP: {fname} not found")
            continue
        
        orig, new, total_secs, discarded = deduplicate_file(fpath, dry_run=args.dry_run)
        reduction = ((orig - new) / orig * 100) if orig > 0 else 0
        total_original += orig
        total_new += new
        
        print(f"{fname:<20} {orig:>10} {new:>10} {reduction:>9.1f}% {total_secs:>10} {discarded:>10}")
    
    print("-" * 70)
    total_reduction = ((total_original - total_new) / total_original * 100) if total_original > 0 else 0
    print(f"{'TOTAL':<20} {total_original:>10} {total_new:>10} {total_reduction:>9.1f}%")
    print()
    
    if args.dry_run:
        print("Run without --dry-run to apply changes.")
    else:
        print("Changes applied successfully.")


if __name__ == "__main__":
    main()
