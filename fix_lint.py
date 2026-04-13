with open("src/backend/python_nlp/nlp_engine.py", "r") as f:
    content = f.read()

content = content.replace("from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline", "from transformers import pipeline")

with open("src/backend/python_nlp/nlp_engine.py", "w") as f:
    f.write(content)

with open("src/backend/python_backend/workflow_editor_ui.py", "r") as f:
    content = f.read()

import re
content = content.replace("try:\n    from src.core.security import Permission, SecurityLevel, get_security_manager\n\n    security_manager_available = True\nexcept ImportError:\n    security_manager_available = False\n", "")
content = content.replace("initialize_workflow_system()", "# initialize_workflow_system()")

with open("src/backend/python_backend/workflow_editor_ui.py", "w") as f:
    f.write(content)
