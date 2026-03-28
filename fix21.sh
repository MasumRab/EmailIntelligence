sed -i 's/import importlib.util/import importlib.util\nimport importlib/g' src/backend/python_backend/plugin_manager.py
sed -i 's/from src.core.auth import get_current_active_user/from src.core.auth import get_current_active_user\nfrom fastapi import Depends/g' src/backend/python_backend/training_routes.py
sed -i 's/from src.core.security import Permission, SecurityLevel, get_security_manager/pass/g' src/backend/python_backend/workflow_editor_ui.py
sed -i 's/initialize_workflow_system()/# initialize_workflow_system()/g' src/backend/python_backend/workflow_editor_ui.py
