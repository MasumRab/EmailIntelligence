from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from server.python_backend.ai_engine import AdvancedAIEngine, AIAnalysisResult
from server.python_nlp.nlp_engine import NLPEngine  # NLPEngine is used by AdvancedAIEngine

# Mock for DatabaseManager
mock_db_manager_for_ai_engine = MagicMock()
mock_db_manager_for_ai_engine.get_all_categories = AsyncMock()


@pytest.fixture
def ai_engine_instance():
    # We need to mock NLPEngine that AdvancedAIEngine instantiates,
    # or mock its analyze_email method.
    with patch.object(NLPEngine, "analyze_email") as mock_nlp_analyze:
        # Configure the mock for NLPEngine().analyze_email
        mock_nlp_analyze.return_value = {
            "topic": "some_topic",  # Raw topic from NLPEngine
            "sentiment": "neutral",
            "intent": "informational",
            "urgency": "low",
            "confidence": 0.8,
            "categories": ["AI Category Suggestion 1", "Work Related"],  # Text suggestions
            "keywords": ["test", "ai"],
            "reasoning": "mocked nlp reasoning",
            "suggested_labels": ["label1"],
            "risk_flags": [],
            "action_items": [],
            "category_id": None,  # NLPEngine doesn't set this ID
        }
        engine = AdvancedAIEngine()
        # Store the mock for assertions if needed directly on nlp_engine's mock
        engine.nlp_engine.analyze_email = mock_nlp_analyze
        yield engine


@pytest.mark.asyncio
async def test_analyze_email_no_db_provided(ai_engine_instance: AdvancedAIEngine):
    subject = "Test Subject"
    content = "Test Content"

    # NLPEngine().analyze_email is already mocked in the fixture
    ai_engine_instance.nlp_engine.analyze_email.return_value["categories"] = [
        "AI Category Suggestion 1"
    ]

    result = await ai_engine_instance.analyze_email(subject, content, db=None)

    assert isinstance(result, AIAnalysisResult)
    assert result.topic == "some_topic"
    assert result.category_id is None  # No DB, so no ID matching
    assert result.categories == ["AI Category Suggestion 1"]  # Should still have text categories
    ai_engine_instance.nlp_engine.analyze_email.assert_called_once_with(subject, content)


@pytest.mark.asyncio
async def test_analyze_email_with_db_category_match(ai_engine_instance: AdvancedAIEngine):
    subject = "Work Email"
    content = "Project discussion about work."

    ai_engine_instance.nlp_engine.analyze_email.return_value["categories"] = [
        "Work Related",
        "Important Stuff",
    ]

    # Mock database categories
    mock_db_categories = [
        {"id": 1, "name": "Personal", "description": "", "color": "", "count": 0},
        {
            "id": 5,
            "name": "Work Related",
            "description": "",
            "color": "",
            "count": 0,
        },  # This should match
        {"id": 10, "name": "Finance", "description": "", "color": "", "count": 0},
    ]
    mock_db_manager_for_ai_engine.get_all_categories.return_value = mock_db_categories

    result = await ai_engine_instance.analyze_email(
        subject, content, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id == 5  # Matched 'Work Related'
    assert result.categories == ["Work Related", "Important Stuff"]  # Original AI suggestions
    mock_db_manager_for_ai_engine.get_all_categories.assert_called_once()


@pytest.mark.asyncio
async def test_analyze_email_with_db_no_category_match(ai_engine_instance: AdvancedAIEngine):
    subject = "Unique Topic"
    content = "Content about something new."

    ai_engine_instance.nlp_engine.analyze_email.return_value["categories"] = [
        "Very New AI Category"
    ]

    mock_db_categories = [
        {"id": 1, "name": "Personal"},
        {"id": 5, "name": "Work"},
    ]
    mock_db_manager_for_ai_engine.get_all_categories.return_value = mock_db_categories

    result = await ai_engine_instance.analyze_email(
        subject, content, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id is None  # No match
    assert result.categories == ["Very New AI Category"]


@pytest.mark.asyncio
async def test_analyze_email_db_error_during_category_match(ai_engine_instance: AdvancedAIEngine):
    subject = "Test Subject"
    content = "Test Content"

    ai_engine_instance.nlp_engine.analyze_email.return_value["categories"] = ["Some AI Category"]
    mock_db_manager_for_ai_engine.get_all_categories.side_effect = Exception("DB connection error")

    result = await ai_engine_instance.analyze_email(
        subject, content, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id is None  # Error during matching, so no ID
    # Should still return the rest of the analysis from NLPEngine
    assert result.topic == "some_topic"
    assert result.categories == ["Some AI Category"]


@pytest.mark.asyncio
async def test_analyze_email_no_ai_categories_to_match(ai_engine_instance: AdvancedAIEngine):
    subject = "Test Subject"
    content = "Test Content"

    ai_engine_instance.nlp_engine.analyze_email.return_value["categories"] = (
        []
    )  # NLP engine returns no categories

    mock_db_categories = [{"id": 1, "name": "Personal"}]
    mock_db_manager_for_ai_engine.get_all_categories.return_value = mock_db_categories

    result = await ai_engine_instance.analyze_email(
        subject, content, db=mock_db_manager_for_ai_engine
    )

    assert isinstance(result, AIAnalysisResult)
    assert result.category_id is None
    assert result.categories == []
    # Ensure get_all_categories is not called if there are no AI categories to match
    mock_db_manager_for_ai_engine.get_all_categories.assert_not_called()
