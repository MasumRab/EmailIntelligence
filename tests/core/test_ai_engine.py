import asyncio
import time
import pytest
from src.core.ai_engine import ModernAIEngine

@pytest.mark.asyncio
async def test_ai_engine_analysis_correctness():
    """Test that the AI engine correctly analyzes email content using fallback methods."""
    engine = ModernAIEngine()
    engine.initialize()

    # Test Sentiment
    result = await engine.analyze_email("Good news", "I am very happy with the project progress.")
    assert result.sentiment == "positive"

    result = await engine.analyze_email("Bad news", "I have a terrible problem with the code.")
    assert result.sentiment == "negative"

    # Test Topic
    result = await engine.analyze_email("Meeting", "Let's schedule a meeting about the project deadline.")
    assert "work" in result.categories

    result = await engine.analyze_email("Invoice", "Please pay the invoice for the consultation.")
    assert "finance" in result.categories

    # Test Intent
    result = await engine.analyze_email("Question", "What is the status of the server?")
    assert result.intent == "question"

    result = await engine.analyze_email("Request", "Please help me with this bug.")
    assert result.intent == "request"

    # Test Urgency
    result = await engine.analyze_email("Urgent", "This is a critical issue, fix asap!")
    assert result.urgency == "high"

    result = await engine.analyze_email("Update", "Just a regular update.")
    assert result.urgency == "low"

@pytest.mark.asyncio
async def test_ai_engine_benchmark():
    """Benchmark the AI engine analysis performance."""
    engine = ModernAIEngine()
    engine.initialize()

    # Create a reasonably long email content
    subject = "Project Update and Urgent Issues"
    content = " ".join(["We need to discuss the project deadline."] * 100) + \
              " ".join(["I am very happy with the progress but we have a critical bug."] * 100) + \
              " ".join(["Please review the attached invoice."] * 100)

    # Warm up
    await engine.analyze_email(subject, content)

    start_time = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        await engine.analyze_email(subject, content)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"\nAverage analysis time: {avg_time:.6f} seconds")

    # Assert that it's reasonably fast (this is a loose assertion just to have one)
    assert avg_time < 0.1
