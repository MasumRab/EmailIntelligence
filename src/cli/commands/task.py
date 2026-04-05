import typer
from pathlib import Path
from src.core.execution.task_runner import TaskRunner

app = typer.Typer()

@app.command()
def run(
    file: Path = typer.Argument("tasks.md", help="Path to tasks markdown file")
):
    """Execute tasks defined in a markdown file."""
    runner = TaskRunner()
    runner.run(file)
