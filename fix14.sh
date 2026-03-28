sed -i 's/from backend.node_engine.security_manager import SecurityLevel/from src.core.security import SecurityLevel/g' src/backend/python_backend/advanced_workflow_routes.py
sed -i '/from .workflow_engine import WorkflowEngine/d' src/backend/python_backend/email_routes.py
sed -i 's/from backend.node_engine.workflow_engine import WorkflowEngine/from src.core.workflow_engine import WorkflowEngine/g' src/backend/python_backend/email_routes.py
