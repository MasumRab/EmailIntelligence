import typer
from InquirerPy import inquirer
from src.core.utils.logger import get_console

app = typer.Typer()

@app.command()
def guide():
    """Interactive workflow guide."""
    console = get_console()
    console.print("[bold green]Orchestration Core Guide[/bold green]")
    
    action = inquirer.select(
        message="What do you want to do?",
        choices=[
            "Analyze Conflicts",
            "Plan Rebase",
            "Sync Tools",
            "Exit"
        ],
    ).execute()
    
    if action == "Exit":
        return
        
    # Dispatch logic would go here
    console.print(f"Selected: {action} (Not implemented yet)")
