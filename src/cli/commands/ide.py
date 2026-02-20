import typer
import shutil
from pathlib import Path
from enum import Enum

class IDETarget(str, Enum):
    VSCODE = "vscode"
    ANTIGRAVITY = "antigravity"
    WINDSURF = "windsurf"

app = typer.Typer()

@app.command()
def init(target: IDETarget = IDETarget.VSCODE):
    """Initialize IDE configuration."""
    template_map = {
        IDETarget.VSCODE: ("vscode_tasks.json.j2", ".vscode/tasks.json"),
        IDETarget.ANTIGRAVITY: ("antigravity.json.j2", ".antigravity/config.json"),
        IDETarget.WINDSURF: ("windsurf.json.j2", ".windsurf/config.json")
    }
    
    src, dest = template_map[target]
    src_path = Path(f"src/core/templates/{src}")
    dest_path = Path(dest)
    
    dest_path.parent.mkdir(exist_ok=True)
    shutil.copy(src_path, dest_path)
    print(f"Initialized {target} config at {dest}")
