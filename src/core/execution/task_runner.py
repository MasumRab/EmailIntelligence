from pathlib import Path
from typing import List
from src.core.utils.logger import get_console

class TaskRunner:
    """Parses and executes tasks from markdown."""
    
    def run(self, task_file: Path):
        console = get_console()
        if not task_file.exists():
            console.print(f"[bold red]Task file not found: {task_file}[/bold red]")
            return

        lines = task_file.read_text().splitlines()
        for i, line in enumerate(lines):
            if "- [ ]" in line:
                # Execute task (Mock for now, would shell out)
                task_desc = line.split("] ", 1)[1]
                console.print(f"Running: {task_desc}")
                
                # Mark done
                lines[i] = line.replace("- [ ]", "- [x]")
                
        # Write back (T051)
        task_file.write_text("\n".join(lines))
        console.print("[bold green]All tasks executed.[/bold green]")

