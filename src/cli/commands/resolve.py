import typer
from src.core.resolution.engine import AutoResolver, ResolutionStrategy
from src.core.models.git import ConflictModel, ConflictType
from src.core.utils.logger import get_console

app = typer.Typer()

@app.command()
def resolve(
    conflict_path: str = typer.Argument(..., help="Path of the conflicting file"),
    strategy: ResolutionStrategy = typer.Option(
        ResolutionStrategy.TAKE_OURS, 
        "--strategy", "-s",
        help="Resolution strategy"
    )
):
    """Resolve a conflict using a specific strategy."""
    console = get_console()
    resolver = AutoResolver()
    
    # Mocking conflict object since we don't have persistence yet
    conflict = ConflictModel(
        path=conflict_path, 
        type=ConflictType.CONTENT,
        oid_base="base", oid_ours="ours", oid_theirs="theirs"
    )
    
    result = resolver.resolve(conflict, strategy)
    console.print(f"[bold green]{result}[/bold green]")
