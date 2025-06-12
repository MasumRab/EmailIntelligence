"""
Gmail API Integration with Rate Limiting and Efficient Data Retrieval
Implements smart batching, caching, and rate limit management for email collection
"""

import time
import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import asyncio
from collections import deque
import hashlib

@dataclass
class RateLimitConfig:
    """Configuration for Gmail API rate limiting"""
    # Gmail API quotas (per day unless specified)
    queries_per_day: int = 1000000000  # 1 billion quota units per day
    queries_per_100_seconds: int = 250  # 250 quota units per 100 seconds per user
    queries_per_second: int = 5  # Practical limit to avoid bursts
    
    # Email retrieval limits
    messages_per_request: int = 100  # Max messages per list request
    max_concurrent_requests: int = 10  # Max concurrent API calls
    
    # Backoff configuration
    initial_backoff: float = 1.0  # Initial backoff in seconds
    max_backoff: float = 60.0  # Maximum backoff in seconds
    backoff_multiplier: float = 2.0  # Exponential backoff multiplier

@dataclass
class EmailBatch:
    """Batch of emails for processing"""
    messages: List[Dict[str, Any]]
    batch_id: str
    timestamp: datetime
    query_filter: str
    total_count: int

class RateLimiter:
    """Token bucket rate limiter for Gmail API"""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens = config.queries_per_second
        self.last_update = time.time()
        self.request_times = deque()
        
    async def acquire(self) -> None:
        """Acquire permission to make an API request"""
        current_time = time.time()
        
        # Remove requests older than 100 seconds
        while self.request_times and current_time - self.request_times[0] > 100:
            self.request_times.popleft()
        
        # Check if we're within the 100-second limit
        if len(self.request_times) >= self.config.queries_per_100_seconds:
            sleep_time = 100 - (current_time - self.request_times[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        # Token bucket for per-second limiting
        time_passed = current_time - self.last_update
        self.tokens = min(
            self.config.queries_per_second,
            self.tokens + time_passed * (self.config.queries_per_second / 1.0)
        )
        self.last_update = current_time
        
        if self.tokens < 1:
            sleep_time = (1 - self.tokens) / self.config.queries_per_second
            await asyncio.sleep(sleep_time)
            self.tokens = 0
        else:
            self.tokens -= 1
        
        # Record this request
        self.request_times.append(current_time)

class EmailCache:
    """SQLite-based cache for email metadata and content"""
    
    def __init__(self, cache_path: str = "email_cache.db"):
        self.cache_path = cache_path
        self.conn = sqlite3.connect(cache_path, check_same_thread=False)
        self._init_cache()
        
    def _init_cache(self):
        """Initialize cache database tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                subject TEXT,
                sender TEXT,
                sender_email TEXT,
                content TEXT,
                labels TEXT,
                timestamp TEXT,
                retrieved_at TEXT,
                content_hash TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_metadata (
                sync_id TEXT PRIMARY KEY,
                query_filter TEXT,
                last_sync TEXT,
                total_messages INTEGER,
                processed_messages INTEGER,
                next_page_token TEXT
            )
        """)
        
        self.conn.commit()
    
    def get_cached_email(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached email by message ID"""
        cursor = self.conn.execute(
            "SELECT * FROM emails WHERE message_id = ?", (message_id,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "message_id": row[0],
                "thread_id": row[1],
                "subject": row[2],
                "sender": row[3],
                "sender_email": row[4],
                "content": row[5],
                "labels": json.loads(row[6]) if row[6] else [],
                "timestamp": row[7],
                "retrieved_at": row[8],
                "content_hash": row[9]
            }
        return None
    
    def cache_email(self, email_data: Dict[str, Any]) -> None:
        """Cache email data"""
        content_hash = hashlib.md5(
            email_data.get("content", "").encode()
        ).hexdigest()
        
        self.conn.execute("""
            INSERT OR REPLACE INTO emails 
            (message_id, thread_id, subject, sender, sender_email, content, 
             labels, timestamp, retrieved_at, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email_data["message_id"],
            email_data.get("thread_id", ""),
            email_data.get("subject", ""),
            email_data.get("sender", ""),
            email_data.get("sender_email", ""),
            email_data.get("content", ""),
            json.dumps(email_data.get("labels", [])),
            email_data.get("timestamp", ""),
            datetime.now().isoformat(),
            content_hash
        ))
        self.conn.commit()
    
    def get_sync_state(self, query_filter: str) -> Optional[Dict[str, Any]]:
        """Get synchronization state for a query filter"""
        cursor = self.conn.execute(
            "SELECT * FROM sync_metadata WHERE query_filter = ?", (query_filter,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                "sync_id": row[0],
                "query_filter": row[1],
                "last_sync": row[2],
                "total_messages": row[3],
                "processed_messages": row[4],
                "next_page_token": row[5]
            }
        return None
    
    def update_sync_state(self, sync_data: Dict[str, Any]) -> None:
        """Update synchronization state"""
        self.conn.execute("""
            INSERT OR REPLACE INTO sync_metadata 
            (sync_id, query_filter, last_sync, total_messages, processed_messages, next_page_token)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            sync_data["sync_id"],
            sync_data["query_filter"],
            sync_data["last_sync"],
            sync_data["total_messages"],
            sync_data["processed_messages"],
            sync_data.get("next_page_token", "")
        ))
        self.conn.commit()

class GmailDataCollector:
    """
    Gmail API data collector with intelligent rate limiting and caching
    Implements efficient email retrieval strategies
    """
    
    def __init__(self, config: RateLimitConfig = None):
        self.config = config or RateLimitConfig()
        self.rate_limiter = RateLimiter(self.config)
        self.cache = EmailCache()
        self.logger = logging.getLogger(__name__)
        
        # In production, this would be initialized with actual Gmail API credentials
        self.gmail_service = None  # Placeholder for Gmail API service
        
    def set_gmail_service(self, service):
        """Set the Gmail API service instance"""
        self.gmail_service = service
    
    async def collect_emails_incremental(
        self, 
        query_filter: str = "", 
        max_emails: Optional[int] = None,
        since_date: Optional[datetime] = None
    ) -> EmailBatch:
        """
        Collect emails incrementally with rate limiting and caching
        
        Args:
            query_filter: Gmail search query (e.g., "category:primary newer_than:7d")
            max_emails: Maximum number of emails to collect
            since_date: Only collect emails after this date
        """
        sync_id = hashlib.md5(f"{query_filter}_{datetime.now().date()}".encode()).hexdigest()
        
        # Check cache for existing sync state
        sync_state = self.cache.get_sync_state(query_filter)
        if not sync_state:
            sync_state = {
                "sync_id": sync_id,
                "query_filter": query_filter,
                "last_sync": datetime.now().isoformat(),
                "total_messages": 0,
                "processed_messages": 0,
                "next_page_token": None
            }
        
        # Build query with date filter if provided
        if since_date:
            date_str = since_date.strftime("%Y/%m/%d")
            query_filter = f"{query_filter} after:{date_str}".strip()
        
        collected_messages = []
        page_token = sync_state.get("next_page_token")
        
        try:
            while len(collected_messages) < (max_emails or float('inf')):
                # Rate limiting
                await self.rate_limiter.acquire()
                
                # Get message list from Gmail API (simulated)
                message_list = await self._get_message_list(
                    query_filter, 
                    page_token,
                    min(self.config.messages_per_request, (max_emails or 100) - len(collected_messages))
                )
                
                if not message_list.get("messages"):
                    break
                
                # Process messages in parallel with rate limiting
                batch_messages = await self._process_message_batch(
                    message_list["messages"]
                )
                
                collected_messages.extend(batch_messages)
                
                # Update sync state
                sync_state["processed_messages"] += len(batch_messages)
                sync_state["next_page_token"] = message_list.get("nextPageToken")
                sync_state["last_sync"] = datetime.now().isoformat()
                
                self.cache.update_sync_state(sync_state)
                
                # Break if no more pages
                if not message_list.get("nextPageToken"):
                    break
                
                page_token = message_list["nextPageToken"]
                
                # Log progress
                self.logger.info(f"Collected {len(collected_messages)} emails so far...")
        
        except Exception as e:
            self.logger.error(f"Error collecting emails: {e}")
            # Save current state for resumption
            self.cache.update_sync_state(sync_state)
            raise
        
        return EmailBatch(
            messages=collected_messages,
            batch_id=sync_id,
            timestamp=datetime.now(),
            query_filter=query_filter,
            total_count=len(collected_messages)
        )
    
    async def _get_message_list(
        self, 
        query: str, 
        page_token: Optional[str] = None,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Get list of message IDs from Gmail API
        In production, this would make actual Gmail API calls
        """
        # Simulate Gmail API response with realistic structure
        if self.gmail_service:
            # Actual Gmail API call would be:
            # return self.gmail_service.users().messages().list(
            #     userId='me',
            #     q=query,
            #     pageToken=page_token,
            #     maxResults=max_results
            # ).execute()
            pass
        
        # Simulated response for development
        return await self._simulate_gmail_response(query, page_token, max_results)
    
    async def _simulate_gmail_response(
        self, 
        query: str, 
        page_token: Optional[str],
        max_results: int
    ) -> Dict[str, Any]:
        """Simulate Gmail API response for development"""
        # Generate realistic message IDs
        base_time = int(time.time())
        messages = []
        
        for i in range(min(max_results, 10)):  # Limit simulation to 10 messages
            message_id = f"msg_{base_time}_{i:03d}"
            messages.append({"id": message_id, "threadId": f"thread_{base_time}_{i//3:03d}"})
        
        response = {
            "messages": messages,
            "resultSizeEstimate": len(messages)
        }
        
        # Add next page token if there would be more results
        if len(messages) == max_results and not page_token:
            response["nextPageToken"] = f"token_{base_time}_next"
        
        return response
    
    async def _process_message_batch(self, message_ids: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process a batch of message IDs to get full email content"""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        tasks = []
        
        for msg_info in message_ids:
            task = self._get_message_with_semaphore(semaphore, msg_info["id"])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None results
        valid_messages = [
            result for result in results 
            if not isinstance(result, Exception) and result is not None
        ]
        
        return valid_messages
    
    async def _get_message_with_semaphore(
        self, 
        semaphore: asyncio.Semaphore, 
        message_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get message content with concurrency control"""
        async with semaphore:
            await self.rate_limiter.acquire()
            return await self._get_message_content(message_id)
    
    async def _get_message_content(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full message content from Gmail API
        Implements caching to avoid duplicate requests
        """
        # Check cache first
        cached_email = self.cache.get_cached_email(message_id)
        if cached_email:
            return cached_email
        
        try:
            if self.gmail_service:
                # Actual Gmail API call would be:
                # message = self.gmail_service.users().messages().get(
                #     userId='me',
                #     id=message_id,
                #     format='full'
                # ).execute()
                pass
            
            # Simulate message content for development
            email_data = await self._simulate_email_content(message_id)
            
            # Cache the email
            self.cache.cache_email(email_data)
            
            return email_data
            
        except Exception as e:
            self.logger.error(f"Error retrieving message {message_id}: {e}")
            return None
    
    async def _simulate_email_content(self, message_id: str) -> Dict[str, Any]:
        """Simulate email content for development"""
        # Generate realistic email content based on message ID
        email_templates = [
            {
                "subject": "Project Update - Q4 Planning",
                "sender": "Project Manager",
                "sender_email": "pm@company.com",
                "content": "Hi team, I wanted to provide an update on our Q4 planning initiatives. We've made significant progress on the roadmap and need to finalize the budget allocations by end of week.",
                "labels": ["IMPORTANT", "WORK"]
            },
            {
                "subject": "Invoice #12345 - Payment Due",
                "sender": "Accounting",
                "sender_email": "billing@vendor.com",
                "content": "Your invoice #12345 for $2,500 is now due. Please process payment within 30 days to avoid late fees.",
                "labels": ["FINANCE", "BILLING"]
            },
            {
                "subject": "Weekend Plans",
                "sender": "Sarah",
                "sender_email": "sarah@gmail.com",
                "content": "Hey! Are you free this weekend? We're planning a barbecue and would love to have you join us!",
                "labels": ["PERSONAL", "SOCIAL"]
            }
        ]
        
        # Cycle through templates based on message ID
        template_idx = hash(message_id) % len(email_templates)
        template = email_templates[template_idx]
        
        return {
            "message_id": message_id,
            "thread_id": f"thread_{message_id.split('_')[1]}",
            "subject": template["subject"],
            "sender": template["sender"],
            "sender_email": template["sender_email"],
            "content": template["content"],
            "labels": template["labels"],
            "timestamp": datetime.now().isoformat()
        }
    
    def get_collection_strategies(self) -> Dict[str, Dict[str, Any]]:
        """
        Define different email collection strategies based on use case
        """
        return {
            "daily_sync": {
                "description": "Daily incremental sync for recent emails",
                "query": "newer_than:1d",
                "max_emails": 1000,
                "frequency": "daily",
                "priority": "high"
            },
            "weekly_bulk": {
                "description": "Weekly bulk collection for training data",
                "query": "newer_than:7d",
                "max_emails": 5000,
                "frequency": "weekly",
                "priority": "medium"
            },
            "historical_import": {
                "description": "One-time historical data import",
                "query": "older_than:30d",
                "max_emails": 10000,
                "frequency": "once",
                "priority": "low"
            },
            "category_specific": {
                "description": "Category-specific collection",
                "query": "category:primary OR category:social OR category:promotions",
                "max_emails": 2000,
                "frequency": "daily",
                "priority": "medium"
            }
        }
    
    async def execute_collection_strategy(self, strategy_name: str) -> EmailBatch:
        """Execute a predefined collection strategy"""
        strategies = self.get_collection_strategies()
        
        if strategy_name not in strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy = strategies[strategy_name]
        
        self.logger.info(f"Executing collection strategy: {strategy_name}")
        self.logger.info(f"Description: {strategy['description']}")
        
        return await self.collect_emails_incremental(
            query_filter=strategy["query"],
            max_emails=strategy["max_emails"]
        )

async def main():
    """Example usage of Gmail data collector"""
    collector = GmailDataCollector()
    
    # Execute daily sync strategy
    try:
        batch = await collector.execute_collection_strategy("daily_sync")
        print(f"Collected {batch.total_count} emails in batch {batch.batch_id}")
        
        # Print first few emails
        for email in batch.messages[:3]:
            print(f"Subject: {email['subject']}")
            print(f"From: {email['sender']} <{email['sender_email']}>")
            print(f"Preview: {email['content'][:100]}...")
            print("---")
            
    except Exception as e:
        print(f"Collection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())