import re

with open("src/backend/python_backend/__init__.py", "r") as f:
    content = f.read()

content = re.sub(r'^(from backend\.python_nlp\.gmail_service import GmailAIService)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from backend\.python_nlp\.smart_filters import EmailFilter, SmartFilterManager)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.ai_engine import AdvancedAIEngine, AIAnalysisResult)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.database import DatabaseManager, get_db)', r'\1  # noqa: E402', content, flags=re.MULTILINE)
content = re.sub(r'^(from \.models import \(\n    ActivityCreate,\n    ActivityResponse,\n    AIAnalysisResponse,\n    CategoryCreate,\n    CategoryResponse,\n    DashboardStats,\n    EmailCreate,\n    EmailResponse,\n    EmailUpdate,\n    FilterRequest,\n    GmailSyncRequest,\n    GmailSyncResponse,\n    SmartRetrievalRequest,\n\))', r'\1  # noqa: E402', content, flags=re.MULTILINE)

content = content.replace("from .database import DatabaseManager, get_db  # noqa: E402", "from .database import DatabaseManager  # noqa: E402")

with open("src/backend/python_backend/__init__.py", "w") as f:
    f.write(content)
