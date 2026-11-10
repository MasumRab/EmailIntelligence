import argparse
import shutil
from pathlib import Path
from enum import Enum
from typing import Any, Dict

from .interface import Command

class IDETarget(str, Enum):
    VSCODE = "vscode"
    ANTIGRAVITY = "antigravity"
    WINDSURF = "windsurf"

class IDECommand(Command):
    """
    Command to initialize IDE configuration.
    """

    @property
    def name(self) -> str:
        return "ide"

    @property
    def description(self) -> str:
        return "Initialize IDE configuration."

    def get_dependencies(self) -> Dict[str, Any]:
        return {}

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--target",
            choices=["vscode", "antigravity", "windsurf"],
            default="vscode",
            help="The target IDE to configure."
        )

    async def execute(self, args: argparse.Namespace) -> int:
        target = args.target
        template_map = {
            "vscode": ("vscode_tasks.json.j2", ".vscode/tasks.json"),
            "antigravity": ("antigravity.json.j2", ".antigravity/config.json"),
            "windsurf": ("windsurf.json.j2", ".windsurf/config.json")
        }
        
        src, dest = template_map[target]
        src_path = Path(f"src/core/templates/{src}")
        dest_path = Path(dest)
        
        dest_path.parent.mkdir(exist_ok=True, parents=True)
        try:
            shutil.copy(src_path, dest_path)
            print(f"Initialized {target} config at {dest}")
        except FileNotFoundError:
            print(f"Template {src_path} not found")
            return 1
            
        return 0
