# AI Model Training Guide for EmailIntelligence

This guide provides comprehensive instructions for training, evaluating, and deploying AI models used in the EmailIntelligence platform for email analysis tasks including sentiment analysis, topic classification, intent recognition, and urgency detection.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Data Acquisition and Preparation](#data-acquisition-and-preparation)
- [Model Types and Configurations](#model-types-and-configurations)
- [Training Process](#training-process)
- [Model Evaluation and Validation](#model-evaluation-and-validation)
- [Model Deployment](#model-deployment)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The EmailIntelligence platform uses multiple AI models for comprehensive email analysis:

- **Sentiment Analysis**: Determines emotional tone (positive, negative, neutral)
- **Topic Classification**: Categorizes emails by subject matter
- **Intent Recognition**: Identifies the purpose or goal of the email
- **Urgency Detection**: Assesses time-sensitivity and priority level

Models are trained using machine learning techniques and stored in the `models/` directory for deployment.

## Prerequisites

### Software Requirements
- Python 3.12+
- scikit-learn
- pandas
- numpy
- transformers (for BERT-based models)
- nltk
- joblib

### Hardware Requirements
- At least 8GB RAM (16GB recommended)
- Sufficient disk space for training data and models
- GPU recommended for transformer model training

### Data Requirements
- Minimum 1000 labeled examples per category
- Balanced class distribution
- Clean, preprocessed text data
- Proper data splits (train/validation/test)

## Data Acquisition and Preparation

### Step 1: Data Collection

#### Option 1: Using Existing Email Datasets
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load email dataset
df = pd.read_csv('emails_dataset.csv')

# Expected columns: 'text', 'label' (and optionally 'metadata')
print(f"Dataset size: {len(df)}")
print(f"Label distribution:\n{df['label'].value_counts()}")
```

#### Option 2: Creating Custom Dataset from Emails
```python
import json
from pathlib import Path

def extract_emails_from_directory(directory_path):
    """Extract emails from JSON files in directory."""
    emails = []
    directory = Path(directory_path)

    for json_file in directory.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            email_data = json.load(f)
            emails.append({
                'text': email_data.get('content', ''),
                'subject': email_data.get('subject', ''),
                'metadata': email_data
            })

    return pd.DataFrame(emails)
```

### Step 2: Data Labeling

#### Sentiment Analysis Labels
- `positive`: Happy, satisfied, appreciative content
- `negative`: Angry, frustrated, dissatisfied content
- `neutral`: Factual, informational content

#### Topic Classification Labels
- `work_business`: Professional communications
- `finance_banking`: Financial transactions and inquiries
- `healthcare`: Medical appointments and health-related
- `personal`: Personal communications
- `marketing`: Promotional and advertising content
- `technical_support`: Help requests and support tickets

#### Intent Recognition Labels
- `question`: Seeking information or clarification
- `request`: Asking for action or assistance
- `complaint`: Expressing dissatisfaction
- `feedback`: Providing opinions or reviews
- `notification`: Informing about events or updates
- `confirmation`: Acknowledging receipt or agreement

#### Urgency Detection Labels
- `high`: Time-critical, immediate action required
- `medium`: Important but not immediate
- `low`: Routine or informational

### Step 3: Data Preprocessing

```python
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class EmailPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """Clean and preprocess email text."""
        # Convert to lowercase
        text = text.lower()

        # Remove email addresses
        text = re.sub(r'\S+@\S+', '[EMAIL]', text)

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '[URL]', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stopwords and lemmatize
        cleaned_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]

        return ' '.join(cleaned_tokens)

# Usage
preprocessor = EmailPreprocessor()
df['cleaned_text'] = df['text'].apply(preprocessor.clean_text)
```

### Step 4: Data Splitting

```python
from sklearn.model_selection import train_test_split

# Split into train/validation/test sets
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

print(f"Train: {len(train_df)}, Validation: {len(val_df)}, Test: {len(test_df)}")

# Save splits
train_df.to_csv('data/train.csv', index=False)
val_df.to_csv('data/validation.csv', index=False)
test_df.to_csv('data/test.csv', index=False)
```

## Model Types and Configurations

### 1. Traditional ML Models (Scikit-learn)

#### Configuration Example
```python
from backend.python_nlp.ai_training import ModelConfig

# Sentiment Analysis Configuration
sentiment_config = ModelConfig(
    model_name="sentiment_classifier",
    model_type="classification",
    parameters={
        "algorithm": "svm",  # or 'rf', 'nb', 'lr'
        "vectorizer": "tfidf",
        "max_features": 5000,
        "ngram_range": (1, 2),
        "C": 1.0,  # SVM regularization parameter
        "kernel": "linear"
    },
    training_data_path="data/sentiment_train.csv"
)
```

#### Supported Algorithms
- **SVM (Support Vector Machine)**: Good for text classification
- **Random Forest**: Robust and interpretable
- **Logistic Regression**: Fast training and prediction
- **Naive Bayes**: Simple and effective for text

### 2. Transformer-Based Models (BERT/RoBERTa)

#### Configuration Example
```python
# Advanced Sentiment Analysis with BERT
bert_sentiment_config = ModelConfig(
    model_name="sentiment_bert",
    model_type="transformer",
    parameters={
        "model_name": "microsoft/DialoGPT-medium",
        "max_length": 512,
        "batch_size": 16,
        "learning_rate": 2e-5,
        "num_epochs": 3,
        "warmup_steps": 500
    },
    training_data_path="data/sentiment_train.csv"
)
```

## Training Process

### Step 1: Configure Training Environment

```python
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ['PYTHONPATH'] = str(project_root)
```

### Step 2: Create Training Script

```python
#!/usr/bin/env python3
"""
Email Intelligence Model Training Script

This script trains AI models for email analysis using the configured datasets.
"""

import argparse
import logging
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from backend.python_nlp.ai_training import ModelConfig
from backend.python_nlp.model_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_sentiment_model():
    """Train sentiment analysis model."""
    # Load training data
    train_df = pd.read_csv('data/train.csv')
    val_df = pd.read_csv('data/validation.csv')

    # Configure model
    config = ModelConfig(
        model_name="sentiment_classifier",
        model_type="classification",
        parameters={
            "algorithm": "svm",
            "vectorizer": "tfidf",
            "max_features": 5000,
            "C": 1.0
        }
    )

    # Initialize trainer
    trainer = ModelTrainer(config)

    # Train model
    logger.info("Starting sentiment model training...")
    model = trainer.train(train_df['cleaned_text'], train_df['sentiment'])

    # Validate model
    val_predictions = trainer.predict(val_df['cleaned_text'])
    accuracy = accuracy_score(val_df['sentiment'], val_predictions)
    logger.info(f"Validation Accuracy: {accuracy:.4f}")

    # Save model
    trainer.save_model('models/sentiment/sentiment_model.pkl')

    return model

def train_topic_model():
    """Train topic classification model."""
    # Similar structure to sentiment training
    train_df = pd.read_csv('data/train.csv')

    config = ModelConfig(
        model_name="topic_classifier",
        model_type="classification",
        parameters={
            "algorithm": "rf",  # Random Forest for topic classification
            "vectorizer": "tfidf",
            "max_features": 10000,
            "n_estimators": 100
        }
    )

    trainer = ModelTrainer(config)
    model = trainer.train(train_df['cleaned_text'], train_df['topic'])
    trainer.save_model('models/topic/topic_model.pkl')

    return model

def main():
    parser = argparse.ArgumentParser(description='Train Email Intelligence Models')
    parser.add_argument('--model', choices=['sentiment', 'topic', 'intent', 'urgency', 'all'],
                       default='all', help='Model to train')
    parser.add_argument('--data-dir', default='data', help='Data directory')
    parser.add_argument('--output-dir', default='models', help='Output directory')

    args = parser.parse_args()

    if args.model in ['sentiment', 'all']:
        train_sentiment_model()

    if args.model in ['topic', 'all']:
        train_topic_model()

    # Add similar functions for intent and urgency models

    logger.info("Training completed successfully!")

if __name__ == "__main__":
    main()
```

### Step 3: Execute Training

```bash
# Train all models
python train_models.py --model all

# Train specific model
python train_models.py --model sentiment

# Use custom data directory
python train_models.py --data-dir /path/to/data --output-dir /path/to/models
```

## Model Evaluation and Validation

### Step 1: Performance Metrics

```python
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model_path, test_data_path):
    """Comprehensive model evaluation."""

    # Load model and test data
    trainer = ModelTrainer.load_model(model_path)
    test_df = pd.read_csv(test_data_path)

    # Generate predictions
    predictions = trainer.predict(test_df['cleaned_text'])
    true_labels = test_df['label']

    # Calculate metrics
    accuracy = accuracy_score(true_labels, predictions)
    report = classification_report(true_labels, predictions)

    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)

    # Confusion Matrix
    cm = confusion_matrix(true_labels, predictions)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('evaluation_results/confusion_matrix.png')
    plt.show()

    return {
        'accuracy': accuracy,
        'precision': precision_score(true_labels, predictions, average='weighted'),
        'recall': recall_score(true_labels, predictions, average='weighted'),
        'f1_score': f1_score(true_labels, predictions, average='weighted')
    }
```

### Step 2: Cross-Validation

```python
from sklearn.model_selection import cross_val_score

def cross_validate_model(X, y, model_config):
    """Perform cross-validation for model evaluation."""

    trainer = ModelTrainer(model_config)

    # Perform 5-fold cross-validation
    scores = cross_val_score(
        trainer.model,
        X, y,
        cv=5,
        scoring='accuracy'
    )

    print(f"Cross-validation scores: {scores}")
    print(".4f"
    return scores.mean(), scores.std()
```

### Step 3: Model Comparison

```python
def compare_models(model_configs, X, y):
    """Compare multiple model configurations."""

    results = {}

    for config in model_configs:
        trainer = ModelTrainer(config)
        scores = cross_val_score(trainer.model, X, y, cv=3)

        results[config.model_name] = {
            'mean_accuracy': scores.mean(),
            'std_accuracy': scores.std(),
            'config': config.parameters
        }

    # Print comparison table
    print("Model Comparison:")
    print("-" * 50)
    for name, metrics in results.items():
        print("15"
              "15.4f"
              "15.4f")

    return results
```

## Model Deployment

### Step 1: Model File Structure

After training, models are saved in the following structure:

```
models/
├── sentiment/
│   ├── sentiment_model.pkl          # Trained model file
│   └── vectorizer.pkl               # Text vectorizer (if applicable)
├── topic/
│   ├── topic_model.pkl
│   └── vectorizer.pkl
├── intent/
│   ├── intent_model.pkl
│   └── vectorizer.pkl
└── urgency/
    ├── urgency_model.pkl
    └── vectorizer.pkl
```

### Step 2: Update Model Configuration

```python
# In nlp_engine.py or settings
MODEL_PATHS = {
    'sentiment': 'models/sentiment/sentiment_model.pkl',
    'topic': 'models/topic/topic_model.pkl',
    'intent': 'models/intent/intent_model.pkl',
    'urgency': 'models/urgency/urgency_model.pkl'
}
```

### Step 3: Deploy and Test

```python
from backend.python_nlp.nlp_engine import NLPEngine

# Initialize engine with new models
engine = NLPEngine()

# Test with sample email
test_email = "Urgent: Project deadline moved to tomorrow"
result = engine.analyze_email(test_email)

print("Analysis Result:")
print(f"Sentiment: {result['sentiment']}")
print(f"Topic: {result['topic']}")
print(f"Intent: {result['intent']}")
print(f"Urgency: {result['urgency']}")
```

## Best Practices

### Data Quality
1. **Diverse Dataset**: Ensure training data represents real-world email patterns
2. **Balanced Classes**: Avoid class imbalance that can bias model performance
3. **Data Cleaning**: Remove duplicates, correct mislabeling, handle missing data
4. **Domain Adaptation**: Fine-tune models on domain-specific email data

### Model Training
1. **Hyperparameter Tuning**: Use grid search or random search for optimal parameters
2. **Regularization**: Prevent overfitting with appropriate regularization techniques
3. **Early Stopping**: Monitor validation loss to prevent overfitting
4. **Cross-Validation**: Use k-fold cross-validation for robust evaluation

### Model Evaluation
1. **Multiple Metrics**: Don't rely solely on accuracy; consider precision, recall, F1-score
2. **Confusion Analysis**: Analyze confusion matrices to understand model weaknesses
3. **Error Analysis**: Manually review misclassified examples to identify patterns
4. **A/B Testing**: Compare new models against baselines in production-like environments

### Model Maintenance
1. **Version Control**: Track model versions and training data used
2. **Retraining Schedule**: Establish regular retraining intervals
3. **Performance Monitoring**: Monitor model performance in production
4. **Feedback Loop**: Use user feedback to improve model accuracy

## Troubleshooting

### Common Issues

#### 1. Memory Errors During Training
```python
# Reduce batch size or use smaller model
config.parameters.update({
    'batch_size': 8,  # Reduce from 16
    'max_features': 3000  # Reduce from 5000
})
```

#### 2. Poor Model Performance
- **Check data quality**: Ensure labels are correct and data is clean
- **Feature engineering**: Add domain-specific features
- **Model complexity**: Try different algorithms or ensemble methods
- **Hyperparameter tuning**: Perform thorough parameter optimization

#### 3. Class Imbalance
```python
from imblearn.over_sampling import SMOTE

# Use SMOTE for oversampling minority classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
```

#### 4. Overfitting
```python
# Add regularization
config.parameters.update({
    'C': 0.1,  # Reduce regularization for SVM
    'max_depth': 10,  # Limit tree depth for Random Forest
    'min_samples_split': 10  # Minimum samples for split
})
```

### Getting Help

1. Check the [model training logs](#) for detailed error messages
2. Validate data format and preprocessing steps
3. Test with smaller datasets to isolate issues
4. Review model configuration parameters
5. Consult the [troubleshooting guide](../troubleshooting.md) for common issues

## Advanced Topics

### Transfer Learning with Pre-trained Models

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def fine_tune_bert_model(train_data, model_name="microsoft/DialoGPT-medium"):
    """Fine-tune a pre-trained BERT model."""

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Tokenize data
    train_encodings = tokenizer(
        train_data['text'].tolist(),
        truncation=True,
        padding=True,
        max_length=512
    )

    # Fine-tuning code here...
    # (Implementation depends on specific transformer library used)
```

### Ensemble Methods

```python
from sklearn.ensemble import VotingClassifier

def create_ensemble_model(model_configs):
    """Create an ensemble model from multiple configurations."""

    estimators = []
    for config in model_configs:
        trainer = ModelTrainer(config)
        estimators.append((config.model_name, trainer.model))

    # Create voting classifier
    ensemble = VotingClassifier(
        estimators=estimators,
        voting='soft'  # Use probability-based voting
    )

    return ensemble
```

### Model Interpretability

```python
import shap

def explain_model_predictions(model, vectorizer, sample_texts):
    """Use SHAP to explain model predictions."""

    # Create explainer
    explainer = shap.Explainer(model)

    # Transform text data
    X_transformed = vectorizer.transform(sample_texts)

    # Calculate SHAP values
    shap_values = explainer.shap_values(X_transformed)

    # Visualize explanations
    shap.summary_plot(shap_values, X_transformed, feature_names=vectorizer.get_feature_names_out())
```

This guide provides a comprehensive foundation for training and deploying AI models in the EmailIntelligence platform. Regular updates and improvements to the training pipeline will enhance model performance over time.
