import re

file_path = "src/backend/python_nlp/nlp_engine.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from .analysis_components.sentiment_model import SentimentModel", "")
content = content.replace("from .analysis_components.importance_model import ImportanceModel", "")
content = content.replace("from .analysis_components.intent_model import IntentModel", "")
content = content.replace("from .analysis_components.topic_model import TopicModel", "")
content = content.replace("from .analysis_components.urgency_model import UrgencyModel", "")

with open(file_path, "w") as f:
    f.write(content)
