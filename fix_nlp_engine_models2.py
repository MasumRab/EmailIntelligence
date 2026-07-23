import re

file_path = "src/backend/python_nlp/nlp_engine.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from src.backend.python_nlp.text_utils import clean_text", "from src.backend.python_nlp.text_utils import clean_text\n\ntry:\n    from .analysis_components.sentiment_model import LocalSentimentModel as SentimentModel\n    from .analysis_components.importance_model import ImportanceModel\n    from .analysis_components.intent_model import IntentModel\n    from .analysis_components.topic_model import TopicModel\n    from .analysis_components.urgency_model import UrgencyModel\nexcept ImportError:\n    pass\n")

with open(file_path, "w") as f:
    f.write(content)
