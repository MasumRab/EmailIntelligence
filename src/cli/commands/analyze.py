import typer
from src.core.git.plumbing import GitPlumbing
from src.core.git.detector import ConflictDetector
from src.core.utils.logger import get_console

def analyze(
    base: str = typer.Argument("main", help="Base branch/commit"),
    head: str = typer.Argument("HEAD", help="Head branch/commit"),
    repo_path: str = typer.Option(".", help="Path to repository")
):
    """Analyze conflicts between two branches/commits."""
    console = get_console()
    plumbing = GitPlumbing(repo_path)
    detector = ConflictDetector(plumbing)
    
    conflicts = detector.detect(base, head)
    
    if not conflicts:
        console.print("[bold green]No conflicts detected.[/bold green]")
        return
        
    console.print(f"[bold red]Found {len(conflicts)} conflicts:[/bold red]")
    for conflict in conflicts:
        console.print(f" - {conflict.path} ({conflict.type})")
