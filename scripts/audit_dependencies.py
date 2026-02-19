import json
import re
from pathlib import Path

# --- Configuration ---
ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "tasks"

# --- Dependency extraction regex patterns (from update_option_c_visual_map.py) ---
TASK_FILE_RE = re.compile(r"^task_(\d{3}(?:\.\d+)*)\.md$")
TITLE_RE = re.compile(r"^#\s+Task\s+\d+\s*[:\-]?\s*(.+)$")
DEPENDENCY_PATTERNS = [
    re.compile(r"^\*\*Dependencies:\*\*\s*(.+)$", re.I),
    re.compile(r"^\*\*Dependencies\*\*:\s*(.+)$", re.I),
    re.compile(r"^Dependencies:\s*(.+)$", re.I),
]

def normalize_dependency_value(value: str) -> str:
    """Normalizes a raw dependency string from a Markdown header."""
    cleaned = value.strip()
    # Remove any leading/trailing asterisks that might be part of markdown formatting
    cleaned = re.sub(r"^\*+|\*+$", "", cleaned).strip()
    
    # Remove any text within parentheses (e.g., "(can run parallel)")
    cleaned = re.sub(r"\(.*?\)", "", cleaned).strip()

    # Check for "None" or "Varies" specifically after stripping extra text
    if cleaned.lower() in ["none", "varies"]:
        return "None"
    
    # Otherwise, perform general cleanup, keeping only alphanumeric characters, dots, and commas for IDs
    # This also removes text like "Task" from "Task 001"
    cleaned = re.sub(r"[^0-9.,\s]", "", cleaned).strip()
    return cleaned or "None"

def parse_dependency_string(dep_str: str) -> list[str]:
    """Parses a dependency string (e.g., "001, 002.1") into a list of IDs and adds leading zeros."""
    if dep_str == "None":
        return []
    
    parsed_ids = []
    for d in dep_str.split(','):
        d_cleaned = d.strip()
        if d_cleaned:
            parts = d_cleaned.split('.')
            main_id = parts[0]
            # Add leading zeros to main ID part if it's not already 3 digits
            if main_id.isdigit():
                main_id = f"{int(main_id):03d}"
            
            if len(parts) > 1:
                # Reconstruct subtask ID
                parsed_ids.append(f"{main_id}.{'.'.join(parts[1:])}")
            else:
                parsed_ids.append(main_id)
    return parsed_ids

def extract_task_info_from_md(path: Path) -> dict:
    """Extracts task ID, title, and dependencies from a Markdown task file."""
    task_id = path.stem.replace("task_", "")
    title = None
    dependencies = "None" # Default to 'None' if not found

    for line in path.read_text().splitlines():
        if title is None:
            title_match = TITLE_RE.match(line)
            if title_match:
                title = title_match.group(1).strip()

        # Check for dependency line using known patterns
        stripped = line.strip()
        for pattern in DEPENDENCY_PATTERNS:
            match = pattern.match(stripped)
            if match:
                # Normalize and parse the dependency string
                dependencies = normalize_dependency_value(match.group(1))
                break
        
        if title is not None and dependencies != "None": # Stop if both found
            break

    # If dependencies string is still "None", ensure it's an empty list for processing
    parsed_dependencies = parse_dependency_string(dependencies) if dependencies != "None" else []

    return {
        "id": task_id,
        "title": title or "Untitled Task",
        "dependencies": parsed_dependencies,
    }


def main():
    print("=== DEPENDENCY CORRUPTION AUDIT (Markdown Files) ===\n")

    all_tasks_data = []
    task_files = sorted(
        [path for path in TASKS_ROOT.glob("task_*.md") if TASK_FILE_RE.match(path.name)],
        key=lambda p: [int(x) for x in TASK_FILE_RE.match(p.name).group(1).split('.')],
    )

    for path in task_files:
        if TASK_FILE_RE.match(path.name): # Ensure it's a valid task_XXX.md file
            task_info = extract_task_info_from_md(path)
            all_tasks_data.append(task_info)

    if not all_tasks_data:
        print("No task Markdown files found to audit.")
        return

    valid_ids = {t['id'] for t in all_tasks_data}
    issues = {}

    for task in all_tasks_data:
        task_id = task['id']
        deps = task.get('dependencies', [])
        
        if not deps:
            print(f"Task {task_id}: No dependencies declared ✓")
            continue
        
        current_task_issues = {
            'self_refs': [],
            'invalid_ids': [],
            'duplicates': [],
        }
        
        # Check for self-reference
        if task_id in deps:
            current_task_issues['self_refs'].append(task_id)
        
        # Check for invalid IDs
        for dep in deps:
            if dep not in valid_ids and dep != task_id: # A dependency on itself might be handled by 'self_refs'
                current_task_issues['invalid_ids'].append(dep)
        
        # Check for duplicates
        if len(deps) != len(set(deps)):
            current_task_issues['duplicates'] = [d for d in deps if deps.count(d) > 1]
        
        if any(current_task_issues.values()):
            issues[task_id] = current_task_issues
            print(f"Task {task_id}: CORRUPTED")
            if current_task_issues['self_refs']:
                print(f"  - Self-references: {current_task_issues['self_refs']}")
            if current_task_issues['invalid_ids']:
                print(f"  - Invalid IDs: {current_task_issues['invalid_ids']}")
            if current_task_issues['duplicates']:
                print(f"  - Duplicates: {current_task_issues['duplicates']}")

    print(f"\n=== SUMMARY ===")
    corrupted_count = len(issues)
    total_tasks = len(all_tasks_data)
    print(f"Total tasks audited: {total_tasks}")
    print(f"Total corrupted tasks: {corrupted_count}/{total_tasks}")

if __name__ == "__main__":
    main()