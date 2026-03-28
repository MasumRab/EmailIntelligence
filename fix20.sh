cat << 'INNER_EOF' > /tmp/repl.txt
from .routes.v1.category_routes import router as category_router_v1
from .routes.v1.email_routes import router as email_router_v1
from .enhanced_routes import router as enhanced_router
from .workflow_routes import router as workflow_router
from .advanced_workflow_routes import router as advanced_workflow_router
from .node_workflow_routes import router as node_workflow_router
INNER_EOF
sed -i -e '/# Mount versioned APIs/r /tmp/repl.txt' src/backend/python_backend/main.py
