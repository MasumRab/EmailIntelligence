import typer
from src.core.git.plumbing import GitPlumbing
from src.core.git.comparison import BranchComparator
from src.core.utils.logger import get_console

app = typer.Typer()

@app.command()
def compare(
    base: str = typer.Argument("main", help="Base branch/commit"),
    head: str = typer.Argument("HEAD", help="Head branch/commit"),
    repo_path: str = typer.Option(".", help="Path to repository")
):
    """Compare branches (Similarity Score & Unique Commits)."""
    console = get_console()
    plumbing = GitPlumbing(repo_path)
    comparator = BranchComparator(plumbing)
    
    score = comparator.calculate_similarity(base, head)
    base_only, head_only = comparator.get_unique_commits(base, head)
    
    console.print(f"[bold]Similarity Score:[/bold] {score:.2%}")
    console.print(f"[bold red]Base Only ({len(base_only)}):[/bold red]")
    for oid in base_only[:5]:
        console.print(f"  {oid[:7]}")
    if len(base_only) > 5:
        console.print("  ...")
        
    console.print(f"[bold green]Head Only ({len(head_only)}):[/bold green]")
    for oid in head_only[:5]:
        console.print(f"  {oid[:7]}")
    if len(head_only) > 5:
        console.print("  ...")
