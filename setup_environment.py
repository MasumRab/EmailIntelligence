
#!/usr/bin/env python3
"""
Environment Setup Script for Gmail AI Research Interface
Ensures correct Python version and installs all necessary packages
"""

import sys
import subprocess
import os
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements"""
    required_version = (3, 11)
    current_version = sys.version_info[:2]
    
    print(f"🐍 Python {current_version[0]}.{current_version[1]} detected")
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python version check passed")
    return True

def install_package(package_name, import_name=None):
    """Install a package if not already installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False

def setup_nltk():
    """Setup NLTK and download required data"""
    try:
        import nltk
        print("📚 Setting up NLTK data...")
        
        # Create NLTK data directory if it doesn't exist
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Download required NLTK data
        datasets = [
            'punkt',
            'stopwords',
            'vader_lexicon',
            'wordnet',
            'averaged_perceptron_tagger',
            'brown'
        ]
        
        for dataset in datasets:
            try:
                nltk.download(dataset, quiet=True, download_dir=nltk_data_dir)
                print(f"✅ NLTK {dataset} downloaded")
            except Exception as e:
                print(f"⚠️  Failed to download {dataset}: {e}")
        
        return True
    except ImportError:
        print("⚠️  NLTK not available, will use fallback analysis")
        return False

def install_core_packages():
    """Install all core packages required by the application"""
    packages = [
        # Core web framework
        ("fastapi", "fastapi"),
        ("uvicorn[standard]", "uvicorn"),
        ("python-multipart", "multipart"),
        ("jinja2", "jinja2"),
        
        # Database and async support
        ("asyncpg", "asyncpg"),
        ("pydantic", "pydantic"),
        
        # NLP and AI packages
        ("nltk", "nltk"),
        ("scikit-learn", "sklearn"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        
        # Additional utilities
        ("python-dotenv", "dotenv"),
        ("aiofiles", "aiofiles"),
        ("httpx", "httpx"),
    ]
    
    print("📦 Installing core packages...")
    all_successful = True
    
    for package_name, import_name in packages:
        if not install_package(package_name, import_name):
            all_successful = False
    
    return all_successful

def fix_nlp_engine():
    """Fix the NLP engine missing method issue"""
    nlp_engine_path = Path("server/python_nlp/nlp_engine.py")
    
    if not nlp_engine_path.exists():
        print("⚠️  NLP engine file not found, creating basic implementation...")
        return create_basic_nlp_engine()
    
    # Check if analyze_text method exists
    try:
        with open(nlp_engine_path, 'r') as f:
            content = f.read()
            if 'def analyze_text(' in content:
                print("✅ NLP engine analyze_text method exists")
                return True
            else:
                print("🔧 Adding missing analyze_text method...")
                return add_analyze_text_method(nlp_engine_path, content)
    except Exception as e:
        print(f"❌ Error checking NLP engine: {e}")
        return False

def create_basic_nlp_engine():
    """Create a basic NLP engine if missing"""
    nlp_engine_content = '''"""
Basic NLP Engine for Gmail AI Research Interface
Provides fallback analysis when NLTK is not available
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class NLPEngine:
    """Basic NLP engine with fallback implementations"""
    
    def __init__(self):
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic'],
            'negative': ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'poor'],
            'urgent': ['urgent', 'asap', 'immediately', 'emergency', 'critical', 'deadline']
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text and return comprehensive results"""
        if not text or not isinstance(text, str):
            return self._empty_analysis()
        
        text_lower = text.lower()
        
        return {
            'sentiment': self._analyze_sentiment(text_lower),
            'urgency': self._analyze_urgency(text_lower),
            'keywords': self._extract_keywords(text),
            'topics': self._identify_topics(text_lower),
            'word_count': len(text.split()),
            'char_count': len(text),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis"""
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative' 
            confidence = min(0.8, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.6
        
        return {
            'label': sentiment,
            'confidence': confidence,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count
        }
    
    def _analyze_urgency(self, text: str) -> Dict[str, Any]:
        """Basic urgency analysis"""
        urgent_count = sum(1 for word in self.sentiment_keywords['urgent'] if word in text)
        
        if urgent_count > 0:
            urgency = 'high'
            confidence = min(0.9, 0.7 + urgent_count * 0.1)
        elif any(word in text for word in ['soon', 'quick', 'fast']):
            urgency = 'medium'
            confidence = 0.6
        else:
            urgency = 'low'
            confidence = 0.7
        
        return {
            'level': urgency,
            'confidence': confidence,
            'indicators': urgent_count
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Basic keyword extraction"""
        # Remove common stop words and extract meaningful words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
        
        words = re.findall(r'\\b\\w{3,}\\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Return top 10 most frequent keywords
        from collections import Counter
        word_freq = Counter(keywords)
        return [word for word, count in word_freq.most_common(10)]
    
    def _identify_topics(self, text: str) -> List[str]:
        """Basic topic identification"""
        topics = []
        
        # Work/Business topics
        if any(word in text for word in ['meeting', 'project', 'deadline', 'business', 'work', 'office', 'team']):
            topics.append('work_business')
        
        # Personal topics
        if any(word in text for word in ['family', 'friend', 'personal', 'birthday', 'party', 'vacation']):
            topics.append('personal_family')
        
        # Finance topics
        if any(word in text for word in ['payment', 'invoice', 'bank', 'money', 'budget', 'financial']):
            topics.append('finance_banking')
        
        # Technology topics
        if any(word in text for word in ['software', 'app', 'technology', 'computer', 'digital', 'online']):
            topics.append('technology')
        
        return topics if topics else ['general']
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            'sentiment': {'label': 'neutral', 'confidence': 0.5, 'positive_indicators': 0, 'negative_indicators': 0},
            'urgency': {'level': 'low', 'confidence': 0.5, 'indicators': 0},
            'keywords': [],
            'topics': ['general'],
            'word_count': 0,
            'char_count': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
'''
    
    try:
        os.makedirs("server/python_nlp", exist_ok=True)
        with open("server/python_nlp/nlp_engine.py", 'w') as f:
            f.write(nlp_engine_content)
        print("✅ Basic NLP engine created")
        return True
    except Exception as e:
        print(f"❌ Failed to create NLP engine: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Gmail AI Research Interface Environment...")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("❌ Setup failed: Python version requirements not met")
        sys.exit(1)
    
    # Install core packages
    if not install_core_packages():
        print("⚠️  Some packages failed to install, but continuing...")
    
    # Setup NLTK
    setup_nltk()
    
    # Fix NLP engine
    fix_nlp_engine()
    
    print("=" * 60)
    print("✅ Environment setup complete!")
    print("🎯 You can now run: python3 simple_research_ui.py")
    print("🌐 The interface will be available at: http://0.0.0.0:8080")

if __name__ == "__main__":
    main()
