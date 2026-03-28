"""
A script to download and save Hugging Face models for the Email Intelligence application.

This script iterates through a predefined dictionary of model names, downloads each
model and its corresponding tokenizer from the Hugging Face Hub, and saves them
to a local directory structure. This allows the application to load the models
from a local cache instead of downloading them at runtime.

To run the script, execute the following command in the terminal:
    python download_hf_models.py
"""

import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer

# A dictionary mapping model categories to their Hugging Face model identifiers.
MODELS = {
    "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
    "topic": "cardiffnlp/tweet-topic-21-multi",
    "intent": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
    # Placeholder: Using a spam detection model for urgency as an example.
    # This should be replaced with a more suitable model if available.
    "urgency": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
}

for category, model_name in MODELS.items():
    save_dir = os.path.join("models", category)
    os.makedirs(save_dir, exist_ok=True)
    print(f"Downloading {model_name} for {category}...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Saved {category} model to {save_dir}\n")

print("All models downloaded and saved.")
