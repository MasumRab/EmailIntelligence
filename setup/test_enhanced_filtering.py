"""
Test script for the enhanced email filtering system
"""
import asyncio
from datetime import datetime
from backend.node_engine.node_base import ExecutionContext
from backend.node_engine.email_nodes import FilterNode

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
            "size_estimate": 1024
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
            "size_estimate": 2048
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
            "size_estimate": 512
        }
    ]
    
    # Test 1: Basic keyword filtering
    print("\nTest 1: Basic Keyword Filtering")
    print("-" * 30)
    
    filter_node = FilterNode()
    context = ExecutionContext()
    
    # Set inputs for the node
    filter_node.set_input("emails", sample_emails)
    filter_node.set_input("criteria", {
        "required_keywords": ["urgent", "report"],
        "excluded_keywords": ["marketing", "advertisement"]
    })
    
    # Execute the filter node
    result = asyncio.run(filter_node.execute(context))
    
    print(f"Filtered emails count: {len(result['filtered_emails'])}")
    print(f"Discarded emails count: {len(result['discarded_emails'])}")
    
    for email in result['filtered_emails']:
        print(f"  - ID: {email['id']}, Subject: {email['subject']}")
    
    # Test 2: Category-based filtering
    print("\nTest 2: Category-Based Filtering")
    print("-" * 30)
    
    filter_node2 = FilterNode()
    context2 = ExecutionContext()
    
    filter_node2.set_input("emails", sample_emails)
    filter_node2.set_input("criteria", {
        "required_categories": ["work"],
        "excluded_categories": ["promotions"]
    })
    
    result2 = asyncio.run(filter_node2.execute(context2))
    
    print(f"Filtered emails count: {len(result2['filtered_emails'])}")
    print(f"Discarded emails count: {len(result2['discarded_emails'])}")
    
    for email in result2['filtered_emails']:
        print(f"  - ID: {email['id']}, Category: {email['category']}")
    
    # Test 3: Sender-based filtering
    print("\nTest 3: Sender-Based Filtering")
    print("-" * 30)
    
    filter_node3 = FilterNode()
    context3 = ExecutionContext()
    
    filter_node3.set_input("emails", sample_emails)
    filter_node3.set_input("criteria", {
        "required_senders": ["boss@company.com"],
        "excluded_senders": ["newsletter@marketing.com"]
    })
    
    result3 = asyncio.run(filter_node3.execute(context3))
    
    print(f"Filtered emails count: {len(result3['filtered_emails'])}")
    print(f"Discarded emails count: {len(result3['discarded_emails'])}")
    
    for email in result3['filtered_emails']:
        print(f"  - ID: {email['id']}, From: {email['from']}")
    
    # Test 4: Size-based filtering
    print("\nTest 4: Size-Based Filtering")
    print("-" * 30)
    
    filter_node4 = FilterNode()
    context4 = ExecutionContext()
    
    filter_node4.set_input("emails", sample_emails)
    filter_node4.set_input("criteria", {
        "size_criteria": {
            "min_size": 1000,
            "max_size": 2500
        }
    })
    
    result4 = asyncio.run(filter_node4.execute(context4))
    
    print(f"Filtered emails count: {len(result4['filtered_emails'])}")
    print(f"Discarded emails count: {len(result4['discarded_emails'])}")
    
    for email in result4['filtered_emails']:
        print(f"  - ID: {email['id']}, Size: {email['size_estimate']}")
    
    # Test 5: Complex boolean filtering
    print("\nTest 5: Complex Boolean Filtering")
    print("-" * 30)
    
    filter_node5 = FilterNode()
    context5 = ExecutionContext()
    
    filter_node5.set_input("emails", sample_emails)
    filter_node5.set_input("criteria", {
        "and": [
            {"type": "contains_keyword", "value": "report"},
        ],
        "or": [
            {"type": "from_sender", "value": "boss@company.com"},
            {"type": "has_category", "value": "work"}
        ]
    })
    
    result5 = asyncio.run(filter_node5.execute(context5))
    
    print(f"Filtered emails count: {len(result5['filtered_emails'])}")
    print(f"Discarded emails count: {len(result5['discarded_emails'])}")
    
    for email in result5['filtered_emails']:
        print(f"  - ID: {email['id']}, Subject: {email['subject']}, From: {email['from']}")
    
    print("\n" + "="*50)
    print("Enhanced filtering tests completed!")

if __name__ == "__main__":
    test_enhanced_filtering()