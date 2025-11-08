"""
Test script for the enhanced email filtering system
"""
import asyncio
from datetime import datetime
from unittest.mock import patch, MagicMock
from backend.node_engine.node_base import ExecutionContext
from backend.node_engine.email_nodes import EmailSourceNode, FilterNode
from backend.node_engine.workflow_engine import Workflow, workflow_engine

def test_enhanced_filtering():
    """
    Test the enhanced FilterNode with various filtering criteria
    """
    print("Testing Enhanced Email Filtering System")
    print("="*50)

    # Sample emails for testing
    sample_emails = [
        {
            "id": "1",
            "from": "boss@company.com",
            "to": ["employee@company.com"],
            "subject": "Urgent: Quarterly Report Due Today",
            "content": "The quarterly report is due by end of day. Please send it immediately.",
            "timestamp": datetime.now().isoformat(),
            "category": "work",
            "priority": "high",
            "size_estimate": 1024,
            "has_attachment": True,
        },
        {
            "id": "2",
            "from": "newsletter@marketing.com",
            "to": ["user@example.com"],
            "subject": "Special Offer - 50% Off All Items",
            "content": "Check out our special offer for you. Limited time only.",
            "timestamp": datetime.now().isoformat(),
            "category": "promotions",
            "priority": "low",
            "size_estimate": 2048,
            "has_attachment": False,
        },
        {
            "id": "3",
            "from": "friend@personal.com",
            "to": ["user@example.com"],
            "subject": "Weekend Plans",
            "content": "Hey, are we still on for Saturday? Let me know what time works for you.",
            "timestamp": datetime.now().isoformat(),
            "category": "personal",
            "priority": "normal",
            "size_estimate": 512,
            "has_attachment": False,
        }
    ]

    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"emails": sample_emails}
        mock_post.return_value = mock_response

        # Test 1: Basic keyword filtering
        print("\\nTest 1: Basic Keyword Filtering")
        print("-" * 30)

        workflow = Workflow(
            "Test Workflow 1",
            [
                EmailSourceNode(node_id="source"),
                FilterNode(node_id="filter", config={"criteria": {"required_keywords": ["urgent", "report"]}}),
            ],
            [{"source_node_id": "source", "source_port": "emails", "target_node_id": "filter", "target_port": "emails"}]
        )
        context = ExecutionContext()
        result = asyncio.run(workflow_engine.execute_workflow(workflow, {}, context))

        filtered_emails = result['filter']['filtered_emails']
        print(f"Filtered emails count: {len(filtered_emails)}")
        for email in filtered_emails:
            print(f" - ID: {email['id']}, Subject: {email['subject']}")

        assert len(filtered_emails) == 1
        assert filtered_emails[0]['id'] == '1'

    print("\\n" + "="*50)
    print("Enhanced filtering tests completed!")

if __name__ == "__main__":
    test_enhanced_filtering()
