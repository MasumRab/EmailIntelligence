# AI Models Setup Guide

**Archived from:** IFLOW.md git history (EmailIntelligenceGem worktree)  
**Date:** 2026-04-09  
**Status:** Reference only — AI models not fully implemented

---

## Overview

This document preserves the AI models organization guide from the EmailIntelligence project history. The current repository contains documentation and placeholder structures.

---

## Model Directory Structure

```
models/
├── sentiment/           # Sentiment analysis models
│   ├── model.pkl        # Trained model weights
│   └── config.json      # Model configuration
├── topic/               # Topic classification models
│   ├── model.pkl
│   └── config.json
├── intent/              # Intent recognition models
│   ├── model.pkl
│   └── config.json
└── urgency/             # Urgency detection models
    ├── model.pkl
    └── config.json
```

---

## Training Setup

### 1. Prepare Labeled Datasets

Required datasets for each classification type:
- Sentiment: Positive/Negative/Neutral labels
- Topic: Email category labels (Work, Personal, Promotional, etc.)
- Intent: Action labels (Reply, Forward, Archive, Delete, etc.)
- Urgency: Priority labels (High, Medium, Low)

### 2. Implement Training Scripts

Example: `scripts/train_sentiment_model.py`

```python
# Training script structure (aspirational)
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def train_sentiment_model(data_path: str, output_dir: str):
    # Load labeled dataset
    # Preprocess and tokenize
    # Train model
    # Evaluate and save
    pass
```

### 3. Model Training Workflow

```bash
# Train each model type
python scripts/train_sentiment_model.py --data data/sentiment.csv --output models/sentiment/
python scripts/train_topic_model.py --data data/topic.csv --output models/topic/
python scripts/train_intent_model.py --data data/intent.csv --output models/intent/
python scripts/train_urgency_model.py --data data/urgency.csv --output models/urgency/
```

---

## Environment Configuration

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NLP_MODEL_DIR` | Directory for trained NLP models | `models/` |
| `SENTIMENT_MODEL_PATH` | Path to sentiment model | `models/sentiment/` |
| `TOPIC_MODEL_PATH` | Path to topic model | `models/topic/` |

---

## Integration Points

### Backend Integration (src/core/ai_engine.py)

```python
# Model loading (aspirational)
class AIEngine:
    def __init__(self, model_dir: str = "models/"):
        self.sentiment_model = self._load_model(f"{model_dir}/sentiment/")
        self.topic_model = self._load_model(f"{model_dir}/topic/")
        # ...
```

### API Endpoints (backend/python_backend/)

```python
# Analysis endpoint (aspirational)
@app.post("/analyze")
async def analyze_email(email: EmailRequest):
    sentiment = ai_engine.analyze_sentiment(email.text)
    topic = ai_engine.classify_topic(email.text)
    intent = ai_engine.detect_intent(email.text)
    urgency = ai_engine.assess_urgency(email.text)
    return AnalysisResult(sentiment, topic, intent, urgency)
```

---

## Related Documentation

- `docs/source-of-truth/project/PROJECT_SUMMARY.md` — Project overview
- `src/core/ai_engine.py` — AI engine implementation
- `backend/python_nlp/nlp_engine.py` — NLP engine (if exists)
