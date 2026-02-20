import typer
from src.core.git.plumbing import GitPlumbing
from src.core.git.history import HistoryService, DAGBuilder
from src.core.utils.logger import get_console

app = typer.Typer()

@app.command()
def plan(
    base: str = typer.Argument("main", help="Base branch/commit"),
    head: str = typer.Argument("HEAD", help="Head branch/commit"),
    repo_path: str = typer.Option(".", help="Path to repository")
):
    """Generate a topologically sorted rebase plan."""
    console = get_console()
    plumbing = GitPlumbing(repo_path)
    dag_builder = DAGBuilder(plumbing)
    service = HistoryService(dag_builder)
    
    plan_obj = service.plan_rebase(base, head)
    
    console.print(f"[bold green]Rebase Plan ({len(plan_obj.commits)} commits):[/bold green]")
    for commit in plan_obj.commits:
        console.print(f" - {commit.oid[:7]} {commit.message} ({commit.author})")

@app.command()
def apply():
    """Apply the rebase plan (Mock)."""
    console = get_console()
    console.print("[bold yellow]Rebase execution not fully implemented in logic core yet.[/bold yellow]")
