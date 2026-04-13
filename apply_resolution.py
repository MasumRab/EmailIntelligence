with open("src/backend/python_backend/main.py", "r") as f:
    content = f.read()

import re
content = content.replace("    action_routes,\n    admin_routes,\n    auth_routes,\n    category_routes,\n    dashboard_routes,\n    email_routes,\n    filter_routes,\n    training_routes,\n    user_routes,\n", "    admin_routes,\n    auth_routes,\n    category_routes,\n    dashboard_routes,\n    email_routes,\n    filter_routes,\n    training_routes,\n    user_routes,\n")
content = content.replace("app.include_router(action_routes.router, prefix=\"/api\")\n", "")

with open("src/backend/python_backend/main.py", "w") as f:
    f.write(content)
