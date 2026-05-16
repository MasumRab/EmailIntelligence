with open("src/backend/python_backend/__init__.py", "r") as f:
    content = f.read()

import re

# Move imports up
new_imports = """
from backend.python_nlp.gmail_service import GmailAIService
from backend.python_nlp.smart_filters import EmailFilter, SmartFilterManager
from .ai_engine import AdvancedAIEngine, AIAnalysisResult
from .database import DatabaseManager, get_db
from .models import (
    ActivityCreate,
    ActivityResponse,
    AIAnalysisResponse,
    CategoryCreate,
    CategoryResponse,
    DashboardStats,
    EmailCreate,
    EmailResponse,
    EmailUpdate,
    FilterRequest,
    GmailSyncRequest,
    GmailSyncResponse,
    SmartRetrievalRequest,
)

__version__ = "2.0.0"
"""

content = re.sub(r'__version__ = "2.0.0".*?SmartRetrievalRequest,\n\)', new_imports, content, flags=re.DOTALL)

# Add get_db to __all__
content = content.replace('"DatabaseManager",', '"DatabaseManager",\n    "get_db",')

with open("src/backend/python_backend/__init__.py", "w") as f:
    f.write(content)
