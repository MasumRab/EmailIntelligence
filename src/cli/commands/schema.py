import json
from src.core.models.git import ConflictModel
from src.core.models.history import HistoryPlan
from src.core.models.orchestration import Session

def schema():
    """Output JSON schemas for all models."""
    schemas = {
        "ConflictModel": ConflictModel.model_json_schema(),
        "HistoryPlan": HistoryPlan.model_json_schema(),
        "Session": Session.model_json_schema()
    }
    print(json.dumps(schemas, indent=2))
