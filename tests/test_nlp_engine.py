import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json

# Adjust path to import module from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.python_nlp.nlp_engine import NLPEngine, main as nlp_main

# Mock NLTK and TextBlob if they are not installed or to ensure consistent behavior
MOCK_NLTK = not hasattr(sys.modules.get('nltk'), 'corpus')
MOCK_TEXTBLOB = 'TextBlob' not in sys.modules

class TestNLPEngine(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        # Mock environment variables for model paths if necessary
        os.environ["NLP_MODEL_DIR"] = "mock_models" # Point to a dummy model dir
        if not os.path.exists("mock_models"):
            os.makedirs("mock_models")

        # Mock joblib.load to simulate model loading
        self.mock_sentiment_model = MagicMock()
        self.mock_sentiment_model.predict = MagicMock(return_value=['positive'])
        self.mock_sentiment_model.predict_proba = MagicMock(return_value=[[0.1, 0.2, 0.7]]) # neg, neu, pos
        self.mock_sentiment_model.classes_ = ['negative', 'neutral', 'positive']

        self.mock_topic_model = MagicMock()
        self.mock_topic_model.predict = MagicMock(return_value=['work_business'])
        self.mock_topic_model.predict_proba = MagicMock(return_value=[[0.8, 0.1, 0.1]])
        self.mock_topic_model.classes_ = ['work_business', 'personal', 'finance']

        self.mock_intent_model = MagicMock()
        self.mock_intent_model.predict = MagicMock(return_value=['request'])
        self.mock_intent_model.predict_proba = MagicMock(return_value=[[0.9, 0.05, 0.05]])
        self.mock_intent_model.classes_ = ['request', 'inquiry', 'informational']

        self.mock_urgency_model = MagicMock()
        self.mock_urgency_model.predict = MagicMock(return_value=['high'])
        self.mock_urgency_model.predict_proba = MagicMock(return_value=[[0.1, 0.1, 0.8]]) # low, medium, high
        self.mock_urgency_model.classes_ = ['low', 'medium', 'high']


        self.patcher_joblib_load = patch('joblib.load')
        self.mock_joblib_load = self.patcher_joblib_load.start()

        # Simulate model files exist for specific paths
        def side_effect_joblib_load(path):
            if path == os.path.join("mock_models", "sentiment_model.pkl"):
                return self.mock_sentiment_model
            elif path == os.path.join("mock_models", "topic_model.pkl"):
                return self.mock_topic_model
            elif path == os.path.join("mock_models", "intent_model.pkl"):
                return self.mock_intent_model
            elif path == os.path.join("mock_models", "urgency_model.pkl"):
                return self.mock_urgency_model
            raise FileNotFoundError(f"Mock model not found at {path}")

        self.mock_joblib_load.side_effect = side_effect_joblib_load

        # Patch os.path.exists for model loading
        self.patcher_os_path_exists = patch('os.path.exists')
        self.mock_os_path_exists = self.patcher_os_path_exists.start()
        self.mock_os_path_exists.return_value = True # Assume all model files exist by default

        # Mock NLTK and TextBlob if necessary
        if MOCK_NLTK:
            self.nltk_patcher = patch.dict('sys.modules', {'nltk': MagicMock(), 'nltk.corpus': MagicMock()})
            self.nltk_patcher.start()
            sys.modules['nltk'].corpus.stopwords.words.return_value = ['i', 'me', 'my']

        if MOCK_TEXTBLOB:
            self.textblob_patcher = patch('server.python_nlp.nlp_engine.TextBlob')
            self.mock_textblob_constructor = self.textblob_patcher.start()
            self.mock_textblob_instance = MagicMock()
            self.mock_textblob_instance.sentiment.polarity = 0.6
            self.mock_textblob_instance.sentiment.subjectivity = 0.5
            self.mock_textblob_instance.noun_phrases = ['good time', 'sample phrase']
            self.mock_textblob_instance.words = ['this', 'is', 'a', 'good', 'time']
            self.mock_textblob_constructor.return_value = self.mock_textblob_instance

        self.engine = NLPEngine()

    def tearDown(self):
        self.patcher_joblib_load.stop()
        self.patcher_os_path_exists.stop()
        if MOCK_NLTK and hasattr(self, 'nltk_patcher'):
            self.nltk_patcher.stop()
        if MOCK_TEXTBLOB and hasattr(self, 'textblob_patcher'):
            self.textblob_patcher.stop()
        if os.path.exists("mock_models/sentiment_model.pkl"): # Clean up dummy files if any were made
             pass # For now, no actual files are created, joblib.load is mocked.
        if os.path.exists("mock_models"):
            if not os.listdir("mock_models"): # only remove if empty
                 os.rmdir("mock_models")


    def test_analyze_email_with_all_models_available(self):
        """Test analyze_email when all models are loaded."""
        subject = "Important meeting update"
        content = "Please be advised the meeting time has changed. This is an urgent request."

        result = self.engine.analyze_email(subject, content)

        self.assertEqual(result['sentiment'], 'positive')
        self.assertEqual(result['topic'], 'work_business')
        self.assertEqual(result['intent'], 'request')
        self.assertEqual(result['urgency'], 'high')
        self.assertIn('reasoning', result)
        self.assertTrue(result['validation']['reliable'])
        self.mock_sentiment_model.predict.assert_called_once()
        self.mock_topic_model.predict.assert_called_once()
        self.mock_intent_model.predict.assert_called_once()
        self.mock_urgency_model.predict.assert_called_once()

    @patch('server.python_nlp.nlp_engine.NLPEngine._analyze_sentiment_model', return_value=None)
    @patch('server.python_nlp.nlp_engine.NLPEngine._analyze_sentiment_textblob')
    def test_sentiment_fallback_to_textblob(self, mock_textblob_method, mock_model_method):
        """Test sentiment analysis falls back to TextBlob when model fails."""
        mock_textblob_method.return_value = {
            'sentiment': 'positive_textblob', 'polarity': 0.7, 'subjectivity': 0.3,
            'confidence': 0.8, 'method_used': 'fallback_textblob_sentiment'
        }
        text = "This is a test sentence."
        # Re-initialize engine to ensure mocks are correctly picked up if setUp is complex
        current_engine_state = self.engine.sentiment_model
        self.engine.sentiment_model = None # Simulate model not loaded or failed

        # Or directly test the _analyze_sentiment method
        result = self.engine._analyze_sentiment(text)

        self.engine.sentiment_model = current_engine_state # Restore

        mock_model_method.assert_called_once_with(text)
        mock_textblob_method.assert_called_once_with(text)
        self.assertEqual(result['sentiment'], 'positive_textblob')
        self.assertEqual(result['method_used'], 'fallback_textblob_sentiment')

    @patch('server.python_nlp.nlp_engine.NLPEngine._analyze_sentiment_model', return_value=None)
    @patch('server.python_nlp.nlp_engine.NLPEngine._analyze_sentiment_textblob', return_value=None)
    @patch('server.python_nlp.nlp_engine.NLPEngine._analyze_sentiment_keyword')
    def test_sentiment_fallback_to_keyword(self, mock_keyword_method, mock_textblob_method, mock_model_method):
        """Test sentiment analysis falls back to keyword when model and TextBlob fail."""
        mock_keyword_method.return_value = {
            'sentiment': 'negative_keyword', 'polarity': -0.5, 'subjectivity': 0.5,
            'confidence': 0.6, 'method_used': 'fallback_keyword_sentiment'
        }
        text = "This is a bad test sentence."
        result = self.engine._analyze_sentiment(text)

        mock_model_method.assert_called_once_with(text)
        mock_textblob_method.assert_called_once_with(text)
        mock_keyword_method.assert_called_once_with(text)
        self.assertEqual(result['sentiment'], 'negative_keyword')
        self.assertEqual(result['method_used'], 'fallback_keyword_sentiment')

    def test_generate_reasoning(self):
        """Test _generate_reasoning formats messages correctly."""
        sentiment_info = {'sentiment': 'positive', 'method_used': 'model_sentiment'}
        topic_info = {'topic': 'work_business', 'method_used': 'fallback_keyword_topic'}
        intent_info = {'intent': 'request', 'method_used': 'model_intent'}
        urgency_info = {'urgency': 'high', 'method_used': 'fallback_regex_urgency'}

        reasoning = self.engine._generate_reasoning(sentiment_info, topic_info, intent_info, urgency_info)
        self.assertIn("Sentiment analysis detected positive sentiment (using AI model)", reasoning)
        self.assertIn("Identified topic: work_business (using fallback: keyword_topic)", reasoning)
        self.assertIn("Detected intent: request (using AI model)", reasoning)
        self.assertIn("Assessed urgency level: high (using fallback: regex_urgency)", reasoning)

        # Test neutral/general cases
        sentiment_info_neutral = {'sentiment': 'neutral'}
        topic_info_general = {'topic': 'General'}
        intent_info_informational = {'intent': 'informational'}
        urgency_info_low = {'urgency': 'low'}
        reasoning_neutral = self.engine._generate_reasoning(sentiment_info_neutral, topic_info_general, intent_info_informational, urgency_info_low)
        self.assertEqual(reasoning_neutral, "No significant insights detected from the email content through automated analysis.")


    def test_preprocess_text(self):
        text = "  Test Text with Punctuation!!  "
        processed = self.engine._preprocess_text(text)
        self.assertEqual(processed, "test text with punctuation")

    def test_extract_keywords_nltk_available(self):
        """Test keyword extraction when NLTK (and TextBlob) is available."""
        if MOCK_TEXTBLOB or MOCK_NLTK: # Ensure TextBlob mock is active
            self.mock_textblob_instance.noun_phrases = ['sample phrase', 'keyword extraction']
            self.mock_textblob_instance.words = ['this', 'is', 'sample', 'phrase', 'for', 'keyword', 'extraction', 'test']
            sys.modules['nltk'].corpus.stopwords.words.return_value = ['this', 'is', 'for']


        text = "This is a sample phrase for keyword extraction test."
        # Temporarily set HAS_NLTK to True for this test if it was mocked to False
        original_has_nltk = self.engine.HAS_NLTK
        self.engine.HAS_NLTK = True

        keywords = self.engine._extract_keywords(text)

        self.engine.HAS_NLTK = original_has_nltk # Restore

        self.assertIn("sample phrase", keywords)
        self.assertIn("keyword extraction", keywords)
        self.assertIn("test", keywords) # From individual words
        self.assertNotIn("this", keywords) # Stopword

    @patch('server.python_nlp.nlp_engine.HAS_NLTK', False) # Simulate NLTK not available
    def test_extract_keywords_nltk_unavailable(self, mock_has_nltk_false):
        """Test keyword extraction when NLTK is not available."""
        engine_no_nltk = NLPEngine() # Create new engine instance where HAS_NLTK is False
        text = "Important meeting project deadline work personal email."
        keywords = engine_no_nltk._extract_keywords(text)
        expected = ['important', 'meeting', 'project', 'deadline', 'work', 'personal', 'email']
        self.assertEqual(sorted(keywords), sorted(expected))

    def test_categorize_content(self):
        text_work = "This email is about a project meeting and budget."
        categories_work = self.engine._categorize_content(text_work)
        self.assertIn("Work & Business", categories_work)

        text_finance = "Invoice for payment, account statement."
        categories_finance = self.engine._categorize_content(text_finance)
        self.assertIn("Finance & Banking", categories_finance)

        text_none = "Simple hello world."
        categories_none = self.engine._categorize_content(text_none)
        self.assertEqual(categories_none, ["General"])

    def test_suggest_labels(self):
        categories = ["Work & Business", "Finance"]
        urgency = "high"
        labels = self.engine._suggest_labels(categories, urgency)
        self.assertIn("Work & Business", labels)
        self.assertIn("Finance", labels)
        self.assertIn("High Priority", labels)

    def test_detect_risk_factors(self):
        text_spam = "Congratulations you are a winner claim your free prize click here now limited time offer"
        risks_spam = self.engine._detect_risk_factors(text_spam)
        self.assertIn("potential_spam", risks_spam)

        text_sensitive = "Please provide your password and social security number ssn for verification."
        risks_sensitive = self.engine._detect_risk_factors(text_sensitive)
        self.assertIn("sensitive_data", risks_sensitive)

    @patch('sys.stdout', new_callable=mock_open) # Mock print
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_health_check(self, mock_parse_args, mock_stdout):
        mock_parse_args.return_value = MagicMock(
            health_check=True, analyze_email=False, output_format='json',
            subject=None, content=None
        )
        with self.assertRaises(SystemExit) as cm:
            nlp_main()
        self.assertEqual(cm.exception.code, 0)

        output = mock_stdout.mock_calls[0][1][0] # Get what was "printed"
        health_status = json.loads(output)
        self.assertIn("status", health_status)
        self.assertIn("models_available", health_status)
        self.assertTrue(all(model_name in ["sentiment", "topic", "intent", "urgency"] for model_name in health_status["models_available"]))


    @patch('sys.stdout', new_callable=mock_open) # Mock print
    @patch('argparse.ArgumentParser.parse_args')
    @patch('server.python_nlp.nlp_engine.NLPEngine.analyze_email') # Mock the main analysis method
    def test_main_analyze_email(self, mock_analyze_email, mock_parse_args, mock_stdout):
        mock_parse_args.return_value = MagicMock(
            health_check=False, analyze_email=True,
            subject="test subject", content="test content", output_format='json'
        )
        mock_analyze_email.return_value = {"analysis": "done"}

        with self.assertRaises(SystemExit) as cm:
            nlp_main()
        self.assertEqual(cm.exception.code, 0)

        mock_analyze_email.assert_called_once_with("test subject", "test content")
        output = mock_stdout.mock_calls[0][1][0]
        self.assertEqual(json.loads(output), {"analysis": "done"})

    @patch('sys.stdout', new_callable=mock_open) # Mock print
    @patch('argparse.ArgumentParser.parse_args')
    @patch('server.python_nlp.nlp_engine.NLPEngine.analyze_email')
    def test_main_backward_compatible_invocation(self, mock_analyze_email, mock_parse_args, mock_stdout):
        # Simulate old style invocation: python nlp_engine.py "subject" "content"
        # sys.argv needs to be patched carefully for argparse to re-evaluate it

        with patch('sys.argv', ['nlp_engine.py', 'old_subject', 'old_content']):
            # Mock parse_args to return defaults for non-action flags, and no action flags set.
            # This is tricky because argparse parses sys.argv by default.
            # We need the _handle_backward_compatible_cli_invocation to be triggered.
            # The args object passed to _handle_backward_compatible_cli_invocation
            # will be the one from the initial parse_args based on the patched sys.argv.
             mock_parse_args.return_value = MagicMock(
                health_check=False, analyze_email=False,
                subject="", content="", output_format='text' # Simulating no flags passed
            )
             mock_analyze_email.return_value = {"analysis_old_style": "done"}

             with self.assertRaises(SystemExit) as cm:
                 nlp_main()
             self.assertEqual(cm.exception.code, 0)

        mock_analyze_email.assert_called_once_with("old_subject", "old_content")
        output = mock_stdout.mock_calls[0][1][0] # Get what was "printed"
        self.assertEqual(json.loads(output), {"analysis_old_style": "done"})


if __name__ == '__main__':
    unittest.main()
