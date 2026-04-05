import json
from pathlib import Path
from typing import Optional, Dict

class AnswerService:
    """Injects answers into interactive prompts."""
    
    def __init__(self, answers_source: Optional[str] = None):
        self.answers: Dict[str, str] = {}
        if answers_source:
            if answers_source.startswith("{"):
                self.answers = json.loads(answers_source)
            else:
                self.answers = json.loads(Path(answers_source).read_text())

    def get(self, key: str) -> Optional[str]:
        return self.answers.get(key)
