"""
AI Training and Prompt Engineering System
Implements comprehensive model training, prompt optimization, and model versioning
"""

import hashlib
import json
import logging
import pickle
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np

from server.python_nlp.text_utils import clean_text


@dataclass
class ModelConfig:
    """Configuration for AI model training"""

    model_type: str  # 'topic_modeling', 'sentiment', 'intent', 'urgency'
    algorithm: str  # 'naive_bayes', 'svm', 'logistic_regression', 'neural_net'
    hyperparameters: Dict[str, Any]
    feature_set: List[str]
    training_data_version: str
    validation_split: float = 0.2
    test_split: float = 0.1


@dataclass
class TrainingResult:
    """Results from model training"""

    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    feature_importance: Dict[str, float]
    training_time: float
    model_size: int


@dataclass
class PromptTemplate:
    """Template for prompt engineering"""

    template_id: str
    name: str
    description: str
    template: str
    parameters: List[str]
    examples: List[Dict[str, str]]
    performance_metrics: Dict[str, float]


class FeatureExtractor:
    """Advanced feature extraction for email content"""

    def __init__(self):
        self.stopwords = self._load_stopwords()
        self.sentiment_lexicon = self._load_sentiment_lexicon()
        self.urgency_indicators = self._load_urgency_indicators()

    def _load_stopwords(self) -> set:
        """Load comprehensive stopwords list"""
        return {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "has",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "will",
            "with",
            "would",
            "i",
            "you",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
            "this",
            "that",
            "these",
            "those",
            "do",
            "does",
            "did",
            "have",
            "had",
            "been",
            "being",
            "can",
            "could",
            "should",
            "would",
        }

    def _load_sentiment_lexicon(self) -> Dict[str, float]:
        """Load sentiment lexicon with polarity scores"""
        return {
            # Positive words
            "excellent": 0.9,
            "great": 0.8,
            "good": 0.7,
            "wonderful": 0.9,
            "amazing": 0.9,
            "fantastic": 0.9,
            "pleased": 0.7,
            "happy": 0.8,
            "satisfied": 0.7,
            "thank": 0.6,
            "thanks": 0.6,
            "appreciate": 0.7,
            "love": 0.8,
            "perfect": 0.9,
            "awesome": 0.8,
            "brilliant": 0.8,
            # Negative words
            "terrible": -0.9,
            "awful": -0.9,
            "bad": -0.7,
            "horrible": -0.9,
            "disappointed": -0.8,
            "frustrated": -0.8,
            "angry": -0.8,
            "upset": -0.7,
            "problem": -0.6,
            "issue": -0.6,
            "wrong": -0.7,
            "error": -0.6,
            "hate": -0.9,
            "disgusted": -0.8,
            "annoyed": -0.6,
            "irritated": -0.6,
            # Neutral/context words
            "okay": 0.1,
            "fine": 0.2,
            "normal": 0.0,
            "regular": 0.0,
        }

    def _load_urgency_indicators(self) -> Dict[str, float]:
        """Load urgency indicators with weights"""
        return {
            "urgent": 0.9,
            "emergency": 1.0,
            "asap": 0.9,
            "immediate": 0.9,
            "critical": 0.9,
            "now": 0.7,
            "today": 0.6,
            "tomorrow": 0.5,
            "soon": 0.4,
            "deadline": 0.7,
            "priority": 0.6,
            "important": 0.5,
            "rush": 0.8,
            "fast": 0.6,
            "quickly": 0.6,
            "hurry": 0.7,
        }

    def extract_features(self, text: str, include_advanced: bool = True) -> Dict[str, Any]:
        """Extract comprehensive features from text"""
        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)

        features = {
            # Basic features
            "word_count": len(words),
            "char_count": len(text),
            "sentence_count": len(re.split(r"[.!?]+", text)),
            "avg_word_length": np.mean([len(word) for word in words]) if words else 0,
            # Punctuation features
            "exclamation_count": text.count("!"),
            "question_count": text.count("?"),
            "capital_ratio": (sum(1 for c in text if c.isupper()) / len(text) if text else 0),
            # Sentiment features
            "sentiment_score": self._calculate_sentiment_score(words),
            "positive_word_count": sum(
                1 for word in words if self.sentiment_lexicon.get(word, 0) > 0
            ),
            "negative_word_count": sum(
                1 for word in words if self.sentiment_lexicon.get(word, 0) < 0
            ),
            # Urgency features
            "urgency_score": self._calculate_urgency_score(words),
            "urgency_word_count": sum(1 for word in words if word in self.urgency_indicators),
            # Communication patterns
            "has_greeting": any(word in text_lower for word in ["hello", "hi", "hey", "dear"]),
            "has_closing": any(
                word in text_lower for word in ["regards", "sincerely", "thanks", "best"]
            ),
            "has_request": any(
                phrase in text_lower for phrase in ["please", "could you", "would you", "can you"]
            ),
            "has_question": "?" in text,
            "has_apology": any(word in text_lower for word in ["sorry", "apologize", "apology"]),
        }

        if include_advanced:
            features.update(self._extract_advanced_features(text, words))

        return features

    def _calculate_sentiment_score(self, words: List[str]) -> float:
        """Calculate overall sentiment score"""
        scores = [self.sentiment_lexicon.get(word, 0) for word in words]
        return np.mean(scores) if scores else 0.0

    def _calculate_urgency_score(self, words: List[str]) -> float:
        """Calculate urgency score"""
        scores = [self.urgency_indicators.get(word, 0) for word in words]
        return max(scores) if scores else 0.0

    def _extract_advanced_features(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Extract advanced linguistic features"""
        return {
            # Lexical diversity
            "unique_word_ratio": len(set(words)) / len(words) if words else 0,
            "stopword_ratio": (
                sum(1 for word in words if word in self.stopwords) / len(words) if words else 0
            ),
            # N-gram features (top bigrams)
            "top_bigrams": self._extract_top_ngrams(words, n=2, top_k=5),
            "top_trigrams": self._extract_top_ngrams(words, n=3, top_k=3),
            # Email-specific patterns
            "has_email_address": bool(
                re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
            ),
            "has_phone_number": bool(re.search(r"\b\d{3}-\d{3}-\d{4}\b", text)),
            "has_url": bool(re.search(r"http[s]?://\S+", text)),
            "has_date": bool(re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)),
            "has_time": bool(re.search(r"\b\d{1,2}:\d{2}\b", text)),
            "has_money": bool(re.search(r"\$\d+", text)),
            # Topic indicators
            "business_terms": self._count_business_terms(words),
            "personal_terms": self._count_personal_terms(words),
            "technical_terms": self._count_technical_terms(words),
        }

    def _extract_top_ngrams(self, words: List[str], n: int, top_k: int) -> List[str]:
        """Extract top n-grams"""
        if len(words) < n:
            return []

        ngrams = [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]
        counter = Counter(ngrams)
        return [ngram for ngram, _ in counter.most_common(top_k)]

    def _count_business_terms(self, words: List[str]) -> int:
        """Count business-related terms"""
        business_terms = {
            "meeting",
            "project",
            "deadline",
            "budget",
            "report",
            "presentation",
            "client",
            "customer",
            "revenue",
            "profit",
            "strategy",
            "team",
            "department",
            "manager",
            "director",
            "ceo",
            "conference",
            "call",
        }
        return sum(1 for word in words if word in business_terms)

    def _count_personal_terms(self, words: List[str]) -> int:
        """Count personal-related terms"""
        personal_terms = {
            "family",
            "friend",
            "birthday",
            "wedding",
            "vacation",
            "holiday",
            "weekend",
            "dinner",
            "lunch",
            "party",
            "celebration",
            "anniversary",
            "child",
            "parent",
            "spouse",
            "sibling",
            "relative",
            "personal",
        }
        return sum(1 for word in words if word in personal_terms)

    def _count_technical_terms(self, words: List[str]) -> int:
        """Count technical terms"""
        technical_terms = {
            "software",
            "hardware",
            "system",
            "database",
            "server",
            "network",
            "application",
            "program",
            "code",
            "bug",
            "feature",
            "update",
            "version",
            "api",
            "integration",
            "deployment",
            "configuration",
        }
        return sum(1 for word in words if word in technical_terms)


class ModelTrainer:
    """Advanced model training with multiple algorithms"""

    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.models = {}
        self.training_history = []
        self.logger = logging.getLogger(__name__)

    def prepare_training_data(
        self, samples: List[Dict[str, Any]], target_field: str
    ) -> tuple[List[Dict[str, Any]], List[str]]:
        """Prepare training data with feature extraction"""
        features = []
        labels = []

        for sample in samples:
            email_text = f"{sample.get('subject', '')} {sample.get('content', '')}"
            cleaned_text = clean_text(email_text)  # Use shared cleaning function
            feature_vector = self.feature_extractor.extract_features(cleaned_text)
            features.append(feature_vector)
            labels.append(sample.get("labels", {}).get(target_field, "unknown"))

        return features, labels

    def train_naive_bayes(
        self, features: List[Dict[str, Any]], labels: List[str], config: ModelConfig
    ) -> TrainingResult:
        """Train Naive Bayes classifier"""
        import math
        from collections import defaultdict

        start_time = datetime.now()

        # Convert features to numerical format
        feature_names = list(set().union(*(f.keys() for f in features)))
        X = []
        for feature_dict in features:
            vector = [feature_dict.get(name, 0) for name in feature_names]
            X.append(vector)

        # Split data
        train_size = int(len(X) * (1 - config.validation_split - config.test_split))
        val_size = int(len(X) * config.validation_split)

        X_train = X[:train_size]
        y_train = labels[:train_size]
        X_val = X[train_size : train_size + val_size]
        y_val = labels[train_size : train_size + val_size]

        # Train Naive Bayes
        class_counts = Counter(y_train)
        feature_means = defaultdict(lambda: defaultdict(float))
        feature_stds = defaultdict(lambda: defaultdict(float))

        # Calculate statistics for each class
        for label in set(y_train):
            class_features = [X_train[i] for i, y in enumerate(y_train) if y == label]
            for feature_idx in range(len(feature_names)):
                values = [features[feature_idx] for features in class_features]
                feature_means[label][feature_idx] = np.mean(values)
                feature_stds[label][feature_idx] = (
                    np.std(values) + 1e-6
                )  # Add small value to avoid division by zero

        # Validation
        correct = 0
        predictions = []

        for i, x in enumerate(X_val):
            class_scores = {}
            for label in class_counts:
                score = math.log(class_counts[label] / len(y_train))  # Prior probability
                for feature_idx, value in enumerate(x):
                    mean = feature_means[label][feature_idx]
                    std = feature_stds[label][feature_idx]
                    # Gaussian probability
                    prob = (1 / (std * math.sqrt(2 * math.pi))) * math.exp(
                        -0.5 * ((value - mean) / std) ** 2
                    )
                    score += math.log(prob + 1e-10)  # Add small value to avoid log(0)
                class_scores[label] = score

            predicted = max(class_scores, key=class_scores.get)
            predictions.append(predicted)
            if predicted == y_val[i]:
                correct += 1

        accuracy = correct / len(y_val) if y_val else 0

        # Calculate additional metrics
        precision, recall, f1 = self._calculate_metrics(y_val, predictions)
        confusion_matrix = self._calculate_confusion_matrix(y_val, predictions)

        training_time = (datetime.now() - start_time).total_seconds()

        # Store model
        model_data = {
            "type": "naive_bayes",
            "feature_names": feature_names,
            "class_counts": dict(class_counts),
            "feature_means": dict(feature_means),
            "feature_stds": dict(feature_stds),
            "config": asdict(config),
        }

        model_id = self._generate_model_id(config)
        self.models[model_id] = model_data

        return TrainingResult(
            model_id=model_id,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            confusion_matrix=confusion_matrix,
            feature_importance=self._calculate_feature_importance(feature_names, feature_means),
            training_time=training_time,
            model_size=len(pickle.dumps(model_data)),
        )

    def train_logistic_regression(
        self, features: List[Dict[str, Any]], labels: List[str], config: ModelConfig
    ) -> TrainingResult:
        """Train logistic regression classifier"""
        start_time = datetime.now()

        # Simplified logistic regression implementation
        feature_names = list(set().union(*(f.keys() for f in features)))
        X = np.array(
            [[feature_dict.get(name, 0) for name in feature_names] for feature_dict in features]
        )

        # Encode labels
        unique_labels = list(set(labels))
        y = np.array([unique_labels.index(label) for label in labels])

        # Split data
        train_size = int(len(X) * (1 - config.validation_split - config.test_split))
        val_size = int(len(X) * config.validation_split)

        X_train = X[:train_size]
        y_train = y[:train_size]
        X_val = X[train_size : train_size + val_size]
        y_val = labels[train_size : train_size + val_size]

        # Simple gradient descent for logistic regression
        num_features = X_train.shape[1]
        num_classes = len(unique_labels)
        weights = np.random.normal(0, 0.01, (num_features, num_classes))
        learning_rate = config.hyperparameters.get("learning_rate", 0.01)
        epochs = config.hyperparameters.get("epochs", 100)

        for epoch in range(epochs):
            # Forward pass
            scores = X_train.dot(weights)
            probabilities = self._softmax(scores)

            # One-hot encode targets
            targets = np.zeros((len(y_train), num_classes))
            targets[np.arange(len(y_train)), y_train] = 1

            # Backward pass
            gradient = X_train.T.dot(probabilities - targets) / len(y_train)
            weights -= learning_rate * gradient

        # Validation
        val_scores = X_val.dot(weights)
        val_probabilities = self._softmax(val_scores)
        predictions = [unique_labels[np.argmax(prob)] for prob in val_probabilities]

        accuracy = sum(1 for i, pred in enumerate(predictions) if pred == y_val[i]) / len(y_val)
        precision, recall, f1 = self._calculate_metrics(y_val, predictions)
        confusion_matrix = self._calculate_confusion_matrix(y_val, predictions)

        training_time = (datetime.now() - start_time).total_seconds()

        # Store model
        model_data = {
            "type": "logistic_regression",
            "feature_names": feature_names,
            "weights": weights.tolist(),
            "unique_labels": unique_labels,
            "config": asdict(config),
        }

        model_id = self._generate_model_id(config)
        self.models[model_id] = model_data

        return TrainingResult(
            model_id=model_id,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            confusion_matrix=confusion_matrix,
            feature_importance={
                name: abs(weights[i].mean()) for i, name in enumerate(feature_names)
            },
            training_time=training_time,
            model_size=len(pickle.dumps(model_data)),
        )

    def _softmax(self, x):
        """Softmax activation function"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def _calculate_metrics(
        self, y_true: List[str], y_pred: List[str]
    ) -> tuple[float, float, float]:
        """Calculate precision, recall, and F1 score"""
        if not y_true or not y_pred:
            return 0.0, 0.0, 0.0

        # For multi-class, calculate macro-averaged metrics
        labels = list(set(y_true + y_pred))
        precisions = []
        recalls = []

        for label in labels:
            tp = sum(1 for i, pred in enumerate(y_pred) if pred == label and y_true[i] == label)
            fp = sum(1 for pred in y_pred if pred == label) - tp
            fn = sum(1 for true in y_true if true == label) - tp

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0

            precisions.append(precision)
            recalls.append(recall)

        avg_precision = np.mean(precisions)
        avg_recall = np.mean(recalls)
        f1 = (
            2 * (avg_precision * avg_recall) / (avg_precision + avg_recall)
            if (avg_precision + avg_recall) > 0
            else 0
        )

        return avg_precision, avg_recall, f1

    def _calculate_confusion_matrix(self, y_true: List[str], y_pred: List[str]) -> List[List[int]]:
        """Calculate confusion matrix"""
        labels = sorted(list(set(y_true + y_pred)))
        matrix = [[0 for _ in labels] for _ in labels]

        for i, true_label in enumerate(y_true):
            pred_label = y_pred[i] if i < len(y_pred) else "unknown"
            true_idx = labels.index(true_label) if true_label in labels else -1
            pred_idx = labels.index(pred_label) if pred_label in labels else -1

            if true_idx >= 0 and pred_idx >= 0:
                matrix[true_idx][pred_idx] += 1

        return matrix

    def _calculate_feature_importance(
        self, feature_names: List[str], feature_means: Dict[str, Dict[int, float]]
    ) -> Dict[str, float]:
        """Calculate feature importance scores"""
        importance = {}

        for i, name in enumerate(feature_names):
            # Calculate variance across classes
            class_means = [class_data.get(i, 0) for class_data in feature_means.values()]
            importance[name] = np.var(class_means) if class_means else 0

        return importance

    def _generate_model_id(self, config: ModelConfig) -> str:
        """Generate unique model ID"""
        config_str = json.dumps(asdict(config), sort_keys=True)
        return hashlib.md5(f"{config_str}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]

    def save_model(self, model_id: str, filepath: str) -> None:
        """Save trained model to file"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")

        with open(filepath, "wb") as f:
            pickle.dump(self.models[model_id], f)

        self.logger.info(f"Model {model_id} saved to {filepath}")

    def load_model(self, filepath: str) -> str:
        """Load model from file"""
        with open(filepath, "rb") as f:
            model_data = pickle.load(f)

        model_id = self._generate_model_id(ModelConfig(**model_data["config"]))
        self.models[model_id] = model_data

        self.logger.info(f"Model loaded with ID {model_id}")
        return model_id


class PromptEngineer:
    """Advanced prompt engineering for AI responses"""

    def __init__(self):
        self.templates = {}
        self.performance_history = []
        self.logger = logging.getLogger(__name__)

    def create_prompt_template(
        self,
        name: str,
        template: str,
        parameters: List[str],
        examples: List[Dict[str, str]],
        description: str = "",
    ) -> str:
        """Create a new prompt template"""
        template_id = hashlib.md5(
            f"{name}_{template}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        prompt_template = PromptTemplate(
            template_id=template_id,
            name=name,
            description=description,
            template=template,
            parameters=parameters,
            examples=examples,
            performance_metrics={},
        )

        self.templates[template_id] = prompt_template
        return template_id

    def generate_email_classification_prompts(self) -> Dict[str, str]:
        """Generate optimized prompts for email classification tasks"""
        templates = {}

        # Topic classification prompt
        topic_template = """
        Analyze the following email and classify it into one of these categories:
        - work_business: Professional emails, meetings, projects
        - personal_family: Personal conversations, family updates
        - finance_banking: Bills, statements, transactions
        - healthcare: Medical appointments, health updates
        - travel: Travel bookings, itineraries, confirmations
        - promotions: Newsletters, offers, advertisements
        
        Email Subject: {subject}
        Email Content: {content}
        
        Based on the content and context, classify this email and provide your reasoning.
        
        Classification: [CATEGORY]
        Confidence: [0-100]
        Reasoning: [Brief explanation]
        """

        templates["topic_classification"] = self.create_prompt_template(
            name="Topic Classification",
            template=topic_template,
            parameters=["subject", "content"],
            examples=[
                {
                    "input": "Subject: Q4 Budget Meeting\nContent: We need to discuss the quarterly budget...",
                    "output": "Classification: work_business\nConfidence: 95\nReasoning: Contains business terminology and meeting context",
                }
            ],
            description="Classifies emails into topic categories",
        )

        # Sentiment analysis prompt
        sentiment_template = """
        Analyze the sentiment of the following email content:
        
        Email Subject: {subject}
        Email Content: {content}
        
        Determine the overall emotional tone and sentiment.
        
        Sentiment: [positive/negative/neutral]
        Intensity: [low/medium/high]
        Key Indicators: [Words or phrases that indicate sentiment]
        Confidence: [0-100]
        """

        templates["sentiment_analysis"] = self.create_prompt_template(
            name="Sentiment Analysis",
            template=sentiment_template,
            parameters=["subject", "content"],
            examples=[
                {
                    "input": "Subject: Thank you!\nContent: I really appreciate your help with the project...",
                    "output": 'Sentiment: positive\nIntensity: high\nKey Indicators: "thank you", "appreciate"\nConfidence: 90',
                }
            ],
            description="Analyzes emotional sentiment in emails",
        )

        # Intent recognition prompt
        intent_template = """
        Identify the primary intent of this email:
        
        Email Subject: {subject}
        Email Content: {content}
        
        Possible intents:
        - request: Asking for something or action
        - information: Sharing information or updates
        - question: Seeking answers or clarification
        - complaint: Expressing dissatisfaction
        - confirmation: Confirming details or arrangements
        
        Intent: [INTENT]
        Action Required: [yes/no]
        Priority: [low/medium/high]
        Reasoning: [Brief explanation]
        """

        templates["intent_recognition"] = self.create_prompt_template(
            name="Intent Recognition",
            template=intent_template,
            parameters=["subject", "content"],
            examples=[
                {
                    "input": "Subject: Can you help?\nContent: Could you please review this document...",
                    "output": "Intent: request\nAction Required: yes\nPriority: medium\nReasoning: Contains clear request for action",
                }
            ],
            description="Identifies the intent behind email communication",
        )

        # Urgency classification prompt
        urgency_template = """
        Assess the urgency level of this email:
        
        Email Subject: {subject}
        Email Content: {content}
        
        Consider:
        - Time-sensitive language
        - Explicit urgency indicators
        - Context and implications
        - Business impact
        
        Urgency: [low/medium/high/critical]
        Time Frame: [When response/action is needed]
        Urgency Indicators: [Specific words or phrases]
        Recommended Action: [What should be done]
        """

        templates["urgency_classification"] = self.create_prompt_template(
            name="Urgency Classification",
            template=urgency_template,
            parameters=["subject", "content"],
            examples=[
                {
                    "input": "Subject: URGENT: Server Down\nContent: Our main server is down and customers cannot access...",
                    "output": 'Urgency: critical\nTime Frame: immediate\nUrgency Indicators: "URGENT", "server down"\nRecommended Action: Immediate technical response required',
                }
            ],
            description="Assesses urgency level for prioritization",
        )

        return templates

    def optimize_prompt(
        self,
        template_id: str,
        test_cases: List[Dict[str, Any]],
        optimization_strategy: str = "performance",
    ) -> str:
        """Optimize prompt template based on performance metrics"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")

        template = self.templates[template_id]
        original_template = template.template

        # Try different optimization strategies
        if optimization_strategy == "performance":
            optimized_template = self._optimize_for_performance(template, test_cases)
        elif optimization_strategy == "clarity":
            optimized_template = self._optimize_for_clarity(template)
        elif optimization_strategy == "brevity":
            optimized_template = self._optimize_for_brevity(template)
        else:
            optimized_template = original_template

        # Create new optimized template
        new_template_id = self.create_prompt_template(
            name=f"{template.name} (Optimized)",
            template=optimized_template,
            parameters=template.parameters,
            examples=template.examples,
            description=f"Optimized version of {template.name}",
        )

        return new_template_id

    def _optimize_for_performance(
        self, template: PromptTemplate, test_cases: List[Dict[str, Any]]
    ) -> str:
        """Optimize template for better performance"""
        # Add more specific instructions and examples
        optimized = template.template

        # Add clarity improvements
        if "Analyze" in optimized:
            optimized = optimized.replace("Analyze", "Carefully analyze and categorize")

        # Add confidence requirements
        if "Confidence:" not in optimized:
            optimized += (
                "\nConfidence: [Provide confidence score 0-100 based on clarity of indicators]"
            )

        # Add reasoning requirement
        if "Reasoning:" not in optimized and "reasoning" not in optimized.lower():
            optimized += "\nReasoning: [Explain the key factors that led to this classification]"

        return optimized

    def _optimize_for_clarity(self, template: PromptTemplate) -> str:
        """Optimize template for clarity"""
        optimized = template.template

        # Add clearer instructions
        optimized = "Please follow these instructions carefully:\n\n" + optimized

        # Add format requirements
        optimized += "\n\nIMPORTANT: Provide your response in the exact format specified above."

        return optimized

    def _optimize_for_brevity(self, template: PromptTemplate) -> str:
        """Optimize template for brevity while maintaining effectiveness"""
        lines = template.template.split("\n")

        # Remove redundant lines and simplify language
        simplified_lines = []
        for line in lines:
            if line.strip():
                # Simplify language
                simplified = line.replace("Determine the overall", "Determine")
                simplified = simplified.replace("Based on the content and context,", "")
                simplified = simplified.replace("Please", "")
                simplified_lines.append(simplified)

        return "\n".join(simplified_lines)

    def evaluate_prompt_performance(
        self, template_id: str, test_results: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Evaluate prompt performance using test results"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")

        metrics = {
            "accuracy": 0.0,
            "consistency": 0.0,
            "clarity_score": 0.0,
            "response_quality": 0.0,
        }

        if not test_results:
            return metrics

        # Calculate accuracy
        correct_responses = sum(1 for result in test_results if result.get("correct", False))
        metrics["accuracy"] = correct_responses / len(test_results)

        # Calculate consistency (how often same input produces same output)
        consistency_scores = [result.get("consistency_score", 0) for result in test_results]
        metrics["consistency"] = np.mean(consistency_scores)

        # Calculate clarity score (based on response format adherence)
        clarity_scores = [result.get("format_adherence", 0) for result in test_results]
        metrics["clarity_score"] = np.mean(clarity_scores)

        # Calculate overall response quality
        quality_scores = [result.get("quality_score", 0) for result in test_results]
        metrics["response_quality"] = np.mean(quality_scores)

        # Update template performance metrics
        self.templates[template_id].performance_metrics = metrics

        return metrics

    def get_best_template(self, task_type: str) -> Optional[str]:
        """Get the best performing template for a specific task"""
        task_templates = [
            (tid, template)
            for tid, template in self.templates.items()
            if task_type.lower() in template.name.lower()
        ]

        if not task_templates:
            return None

        # Sort by performance metrics
        best_template = max(
            task_templates,
            key=lambda x: x[1].performance_metrics.get("accuracy", 0)
            * x[1].performance_metrics.get("response_quality", 0),
        )

        return best_template[0]


def main():
    """Example usage of AI training system"""
    # Initialize components
    trainer = ModelTrainer()
    prompt_engineer = PromptEngineer()

    # Generate sample training data
    sample_data = [
        {
            "subject": "Q4 Budget Meeting",
            "content": "We need to discuss the quarterly budget allocation for next year.",
            "labels": {
                "topic": "work_business",
                "sentiment": "neutral",
                "intent": "information",
                "urgency": "medium",
            },
        },
        {
            "subject": "Birthday Party Invitation",
            "content": "You are invited to my birthday party this Saturday!",
            "labels": {
                "topic": "personal_family",
                "sentiment": "positive",
                "intent": "information",
                "urgency": "low",
            },
        },
    ]

    # Train models
    config = ModelConfig(
        model_type="topic_modeling",
        algorithm="naive_bayes",
        hyperparameters={"smoothing": 1.0},
        feature_set=["word_count", "sentiment_score", "urgency_score"],
        training_data_version="v1.0",
    )

    features, labels = trainer.prepare_training_data(sample_data, "topic")
    result = trainer.train_naive_bayes(features, labels, config)

    print(f"Model {result.model_id} trained with accuracy: {result.accuracy:.2f}")

    # Create prompt templates
    templates = prompt_engineer.generate_email_classification_prompts()
    print(f"Created {len(templates)} prompt templates")

    # Save model
    trainer.save_model(result.model_id, f"model_{result.model_id}.pkl")


if __name__ == "__main__":
    main()
