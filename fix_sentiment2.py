import re

file_path = "src/backend/python_nlp/nlp_engine.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from .analysis_components.sentiment_model import LocalSentimentModel as SentimentModel", "from .analysis_components.sentiment_model import SentimentModel")

with open(file_path, "w") as f:
    f.write(content)
