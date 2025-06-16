# Script to download and save Hugging Face models for EmailIntelligence
# Run: python download_hf_models.py

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

MODELS = {
    "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
    "topic": "cardiffnlp/tweet-topic-21-multi",
    "intent": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
    "urgency": "mrm8488/bert-tiny-finetuned-sms-spam-detection"  # Placeholder, replace with a better urgency model if needed
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
