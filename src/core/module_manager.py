import importlib
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class ModuleManager:
    def __init__(self, app, gradio_app):
        self.app = app
        self.gradio_app = gradio_app
        self.modules_dir = Path(__file__).resolve().parent.parent.parent / "modules"

    def load_modules(self):
        """
        Discovers and loads all modules from the 'modules' directory.
        """
        if not self.modules_dir.is_dir():
            logger.warning(f"Modules directory not found: {self.modules_dir}")
            return

        for module_path in self.modules_dir.iterdir():
            if module_path.is_dir():
                self._load_module(module_path)

    def _load_module(self, module_path: Path):
        """
        Loads a single module, expecting an 'init.py' file to register components.
        """
        module_name = module_path.name
        init_file = module_path / "__init__.py"

        if not init_file.exists():
            logger.debug(f"No '__init__.py' in module '{module_name}', skipping.")
            return

        try:
            # The module name for importlib should be `modules.module_name`
            # to reflect the package structure.
            module_import_name = f"modules.{module_name}"
            spec = importlib.util.spec_from_file_location(module_import_name, init_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_import_name] = module
                spec.loader.exec_module(module)

                if hasattr(module, "register"):
                    module.register(self.app, self.gradio_app)
                    logger.info(
                        f"Successfully loaded and registered module: {module_name}"
                    )
                else:
                    logger.warning(
                        f"Module '{module_name}' has an '__init__.py' but no 'register' function."
                    )
            else:
                logger.error(f"Could not create module spec for {module_name}")

        except Exception as e:
            logger.error(f"Failed to load module '{module_name}': {e}", exc_info=True)
