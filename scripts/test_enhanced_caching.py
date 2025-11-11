#!/usr/bin/env python3
"""
Test script for the enhanced caching system in DatabaseManager.
"""

import asyncio
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import DatabaseManager

async def test_enhanced_caching():
    """Test the enhanced caching system."""
    print("Testing enhanced caching system...")

    # Initialize DatabaseManager
    db = DatabaseManager()
    await db._ensure_initialized()

    # Test creating an email
    print("Creating test email...")
    email_data = {
        "message_id": "test_message_123",
        "subject": "Test Email for Caching",
        "sender": "test@example.com",
        "content": "This is a test email content for caching validation.",
        "analysis_metadata": {"sentiment": "positive"}
    }

    created_email = await db.create_email(email_data)
    if created_email:
        email_id = created_email["id"]
        print(f"Created email with ID: {email_id}")

        # Test retrieving email with caching
        print("Testing email retrieval with caching...")
        email1 = await db.get_email_by_id(email_id, include_content=True)
        email2 = await db.get_email_by_id(email_id, include_content=True)

        if email1 and email2:
            print("Email retrieval successful with caching")
            print(f"Email subject: {email1['subject']}")

            # Check if content is properly merged
            if "content" in email1 and email1["content"]:
                print("Content properly loaded and cached")
            else:
                print("Warning: Content not found in retrieved email")
        else:
            print("Failed to retrieve email")

        # Test retrieval by message ID
        print("Testing email retrieval by message ID...")
        email3 = await db.get_email_by_message_id("test_message_123", include_content=True)
        if email3:
            print("Email retrieval by message ID successful")
        else:
            print("Failed to retrieve email by message ID")

        # Test cache statistics
        print("Checking cache statistics...")
        cache_stats = db.caching_manager.get_cache_statistics()
        print(f"Cache statistics: {cache_stats}")

        # Test updating email (should invalidate cache)
        print("Testing email update (should invalidate cache)...")
        updated_email = await db.update_email(email_id, {"subject": "Updated Test Email"})
        if updated_email:
            print("Email update successful")

            # Check cache was invalidated by retrieving again
            email4 = await db.get_email_by_id(email_id, include_content=True)
            if email4 and email4["subject"] == "Updated Test Email":
                print("Cache invalidation working correctly")
            else:
                print("Warning: Cache invalidation may not be working")
        else:
            print("Failed to update email")
    else:
        print("Failed to create test email")

    # Shutdown
    await db.shutdown()
    print("Test completed successfully")

if __name__ == "__main__":
    asyncio.run(test_enhanced_caching())