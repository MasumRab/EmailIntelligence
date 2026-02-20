import typer
from pathlib import Path
from typing import List
from InquirerPy import inquirer
from src.core.utils.logger import get_console
from src.core.utils.files import backup_and_overwrite
from src.core.analysis.sync import SyncService
from src.core.git.plumbing import GitPlumbing

app = typer.Typer()

MANAGED_FILES = [
    ".flake8",
    ".pylintrc",
    "pyproject.toml",
    "scripts/install-hooks.sh"
]

@app.callback(invoke_without_command=True)
def sync_cmd(ctx: typer.Context):
    """Sync local scripts with canonical source."""
    if ctx.invoked_subcommand is not None:
        return

    console = get_console()
    plumbing = GitPlumbing(".")
    service = SyncService(plumbing, canonical_ref="origin/orchestration-tools")
    
    console.print("Checking for divergence from origin/orchestration-tools...")
    try:
        report = service.check_sync(MANAGED_FILES)
    except Exception as e:
        console.print(f"[bold red]Error checking sync status: {e}[/bold red]")
        console.print("Ensure you have fetched the remote: git fetch origin")
        raise typer.Exit(1)

    if report.up_to_date:
        console.print("[bold green]All managed files are up to date.[/bold green]")
        return

    console.print(f"[bold yellow]Found {len(report.diverged_files)} diverged files.[/bold yellow]")
    
    selected = inquirer.checkbox(
        message="Select files to overwrite (local versions will be backed up to .bak):",
        choices=report.diverged_files,
        transformer=lambda result: f"{len(result)} files selected"
    ).execute()

    if not selected:
        console.print("No files selected. Exiting.")
        return

    for path_str in selected:
        try:
            # We need to get the content content from git to overwrite
            content = plumbing.cat_file("origin/orchestration-tools", path_str)
            dest = Path(path_str)
            
            # Write to a temp file first
            tmp_path = dest.with_suffix(".tmp_sync")
            tmp_path.write_text(content)
            
            # Use backup_and_overwrite logic
            backup_and_overwrite(tmp_path, dest)
            tmp_path.unlink(missing_ok=True)
            
            console.print(f"Synced: {path_str}")
        except Exception as e:
            console.print(f"[bold red]Failed to sync {path_str}: {e}[/bold red]")

@app.command()
def install_hooks():
    """Install constitutional pre-commit hooks."""
    console = get_console()
    hook_src = Path("scripts/hooks/pre-commit")
    hook_dest = Path(".git/hooks/pre-commit")
    
    if not hook_src.exists():
        console.print("[bold red]Hook source not found in scripts/hooks/pre-commit[/bold red]")
        return
        
    backup_and_overwrite(hook_src, hook_dest)
    hook_dest.chmod(0o755) # Ensure executable
    console.print("[bold green]Constitutional hooks installed (with backup).[/bold green]")
