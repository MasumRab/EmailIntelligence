"""
Smart Gmail Retrieval with Advanced Filtering and Batching Strategies
Implements intelligent filtering, date-based incremental sync, and optimized batch processing
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import asyncio
from collections import defaultdict
import hashlib

@dataclass
class RetrievalStrategy:
    """Configuration for smart retrieval strategy"""
    name: str
    query_filter: str
    priority: int  # 1-10, higher is more priority
    batch_size: int
    frequency: str  # hourly, daily, weekly
    max_emails_per_run: int
    include_folders: List[str]
    exclude_folders: List[str]
    date_range_days: int
    
@dataclass
class SyncCheckpoint:
    """Checkpoint for incremental synchronization"""
    strategy_name: str
    last_sync_date: datetime
    last_history_id: str
    processed_count: int
    next_page_token: Optional[str]
    errors_count: int

class SmartGmailRetriever:
    """Advanced Gmail retrieval with intelligent filtering and batching"""
    
    def __init__(self, checkpoint_db_path: str = "sync_checkpoints.db"):
        self.checkpoint_db_path = checkpoint_db_path
        self.logger = logging.getLogger(__name__)
        self._init_checkpoint_db()
        
        # Gmail API quotas and limits
        self.api_limits = {
            'daily_quota': 1000000000,  # 1 billion units per day
            'per_user_per_100_seconds': 250,  # 250 units per 100 seconds
            'batch_size_limit': 100,    # Max emails per batch request
            'concurrent_requests': 10   # Max concurrent API calls
        }
        
        # Smart filtering categories
        self.folder_mappings = {
            'INBOX': {'priority': 10, 'frequency': 'hourly'},
            'SENT': {'priority': 5, 'frequency': 'daily'},
            'IMPORTANT': {'priority': 9, 'frequency': 'hourly'},
            'STARRED': {'priority': 8, 'frequency': 'hourly'},
            'CATEGORY_PERSONAL': {'priority': 7, 'frequency': 'daily'},
            'CATEGORY_SOCIAL': {'priority': 4, 'frequency': 'daily'},
            'CATEGORY_PROMOTIONS': {'priority': 2, 'frequency': 'weekly'},
            'CATEGORY_UPDATES': {'priority': 3, 'frequency': 'daily'},
            'CATEGORY_FORUMS': {'priority': 2, 'frequency': 'weekly'},
            'SPAM': {'priority': 1, 'frequency': 'weekly'},
            'TRASH': {'priority': 1, 'frequency': 'never'}
        }
        
    def _init_checkpoint_db(self):
        """Initialize checkpoint database for sync state management"""
        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sync_checkpoints (
                strategy_name TEXT PRIMARY KEY,
                last_sync_date TEXT,
                last_history_id TEXT,
                processed_count INTEGER DEFAULT 0,
                next_page_token TEXT,
                errors_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS retrieval_stats (
                date TEXT PRIMARY KEY,
                total_retrieved INTEGER DEFAULT 0,
                api_calls_used INTEGER DEFAULT 0,
                quota_remaining INTEGER DEFAULT 0,
                strategies_executed TEXT,
                performance_metrics TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_optimized_retrieval_strategies(self) -> List[RetrievalStrategy]:
        """Generate optimized retrieval strategies based on folder types and priorities"""
        strategies = []
        
        # High-priority real-time strategies
        strategies.extend([
            # Critical inbox monitoring
            RetrievalStrategy(
                name="critical_inbox",
                query_filter="in:inbox is:important newer_than:1h",
                priority=10,
                batch_size=50,
                frequency="hourly",
                max_emails_per_run=200,
                include_folders=["INBOX", "IMPORTANT"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=1
            ),
            
            # Starred items
            RetrievalStrategy(
                name="starred_recent",
                query_filter="is:starred newer_than:6h",
                priority=9,
                batch_size=30,
                frequency="hourly",
                max_emails_per_run=100,
                include_folders=["STARRED"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=7
            ),
            
            # Unread priority emails
            RetrievalStrategy(
                name="unread_priority",
                query_filter="is:unread (is:important OR from:manager OR from:ceo OR subject:urgent OR subject:asap) newer_than:2h",
                priority=9,
                batch_size=40,
                frequency="hourly",
                max_emails_per_run=150,
                include_folders=["INBOX", "IMPORTANT"],
                exclude_folders=["SPAM", "TRASH", "CATEGORY_PROMOTIONS"],
                date_range_days=1
            )
        ])
        
        # Medium-priority daily strategies
        strategies.extend([
            # Personal category
            RetrievalStrategy(
                name="personal_daily",
                query_filter="category:primary newer_than:1d",
                priority=7,
                batch_size=100,
                frequency="daily",
                max_emails_per_run=500,
                include_folders=["CATEGORY_PERSONAL", "INBOX"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=3
            ),
            
            # Social updates
            RetrievalStrategy(
                name="social_daily", 
                query_filter="category:social newer_than:1d",
                priority=5,
                batch_size=75,
                frequency="daily",
                max_emails_per_run=300,
                include_folders=["CATEGORY_SOCIAL"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=2
            ),
            
            # Updates and notifications
            RetrievalStrategy(
                name="updates_daily",
                query_filter="category:updates newer_than:1d",
                priority=4,
                batch_size=80,
                frequency="daily",
                max_emails_per_run=400,
                include_folders=["CATEGORY_UPDATES"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=2
            ),
            
            # Work-related emails
            RetrievalStrategy(
                name="work_comprehensive",
                query_filter="(from:company.com OR subject:meeting OR subject:project OR subject:deadline) newer_than:1d",
                priority=8,
                batch_size=60,
                frequency="daily",
                max_emails_per_run=300,
                include_folders=["INBOX", "SENT"],
                exclude_folders=["SPAM", "TRASH", "CATEGORY_PROMOTIONS"],
                date_range_days=2
            )
        ])
        
        # Low-priority weekly strategies
        strategies.extend([
            # Promotional emails
            RetrievalStrategy(
                name="promotions_weekly",
                query_filter="category:promotions newer_than:7d",
                priority=2,
                batch_size=100,
                frequency="weekly",
                max_emails_per_run=1000,
                include_folders=["CATEGORY_PROMOTIONS"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=7
            ),
            
            # Forums and communities
            RetrievalStrategy(
                name="forums_weekly",
                query_filter="category:forums newer_than:7d",
                priority=2,
                batch_size=50,
                frequency="weekly",
                max_emails_per_run=200,
                include_folders=["CATEGORY_FORUMS"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=7
            ),
            
            # Sent items analysis
            RetrievalStrategy(
                name="sent_analysis",
                query_filter="in:sent newer_than:7d",
                priority=3,
                batch_size=75,
                frequency="weekly",
                max_emails_per_run=500,
                include_folders=["SENT"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=7
            )
        ])
        
        # Special strategies for training and analysis
        strategies.extend([
            # Comprehensive training data
            RetrievalStrategy(
                name="training_data_comprehensive",
                query_filter="newer_than:30d",
                priority=1,
                batch_size=200,
                frequency="monthly",
                max_emails_per_run=5000,
                include_folders=["INBOX", "SENT", "CATEGORY_PERSONAL", "CATEGORY_SOCIAL"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=30
            ),
            
            # Historical important emails
            RetrievalStrategy(
                name="historical_important",
                query_filter="is:important OR is:starred older_than:30d newer_than:365d",
                priority=2,
                batch_size=50,
                frequency="monthly",
                max_emails_per_run=1000,
                include_folders=["IMPORTANT", "STARRED"],
                exclude_folders=["SPAM", "TRASH"],
                date_range_days=365
            )
        ])
        
        return sorted(strategies, key=lambda x: x.priority, reverse=True)
    
    def get_incremental_query(self, strategy: RetrievalStrategy, checkpoint: Optional[SyncCheckpoint] = None) -> str:
        """Build incremental query based on checkpoint and strategy"""
        base_query = strategy.query_filter
        
        if checkpoint and checkpoint.last_sync_date:
            # Use checkpoint date for incremental sync
            last_sync = checkpoint.last_sync_date
            if isinstance(last_sync, str):
                last_sync = datetime.fromisoformat(last_sync.replace('Z', '+00:00'))
            
            # Calculate time since last sync
            time_diff = datetime.now() - last_sync
            
            if time_diff.days > 0:
                date_filter = f"newer_than:{time_diff.days}d"
            elif time_diff.seconds > 3600:
                hours = int(time_diff.seconds / 3600)
                date_filter = f"newer_than:{hours}h"
            else:
                date_filter = "newer_than:1h"
            
            # Replace or add date filter to base query
            if "newer_than:" in base_query:
                # Replace existing date filter
                import re
                base_query = re.sub(r'newer_than:\d+[hdw]', date_filter, base_query)
            else:
                # Add date filter
                base_query = f"{base_query} {date_filter}"
        
        # Add folder-specific filters
        if strategy.include_folders:
            folder_filters = " OR ".join([f"in:{folder.lower()}" for folder in strategy.include_folders])
            base_query = f"({base_query}) AND ({folder_filters})"
        
        if strategy.exclude_folders:
            exclude_filters = " AND ".join([f"-in:{folder.lower()}" for folder in strategy.exclude_folders])
            base_query = f"{base_query} {exclude_filters}"
        
        return base_query
    
    async def execute_smart_retrieval(
        self, 
        strategies: Optional[List[RetrievalStrategy]] = None,
        max_api_calls: int = 100,
        time_budget_minutes: int = 30
    ) -> Dict[str, Any]:
        """Execute smart retrieval with multiple strategies and rate limiting"""
        
        if strategies is None:
            strategies = self.get_optimized_retrieval_strategies()
        
        results = {
            'strategies_executed': [],
            'total_emails_retrieved': 0,
            'api_calls_used': 0,
            'errors': [],
            'performance_metrics': {},
            'quota_status': {}
        }
        
        start_time = datetime.now()
        api_calls_used = 0
        
        # Execute strategies in priority order
        for strategy in strategies:
            # Check time and API budget
            elapsed_time = (datetime.now() - start_time).total_seconds() / 60
            if elapsed_time >= time_budget_minutes or api_calls_used >= max_api_calls:
                self.logger.info(f"Stopping retrieval: time={elapsed_time:.1f}min, api_calls={api_calls_used}")
                break
            
            try:
                # Load checkpoint for this strategy
                checkpoint = self._load_checkpoint(strategy.name)
                
                # Build incremental query
                query = self.get_incremental_query(strategy, checkpoint)
                
                # Execute retrieval for this strategy
                strategy_result = await self._execute_strategy_retrieval(
                    strategy, 
                    query, 
                    checkpoint,
                    remaining_api_calls=max_api_calls - api_calls_used
                )
                
                # Update results
                results['strategies_executed'].append({
                    'strategy_name': strategy.name,
                    'emails_retrieved': strategy_result['emails_count'],
                    'api_calls': strategy_result['api_calls'],
                    'success': strategy_result['success']
                })
                
                results['total_emails_retrieved'] += strategy_result['emails_count']
                api_calls_used += strategy_result['api_calls']
                
                if not strategy_result['success']:
                    results['errors'].append({
                        'strategy': strategy.name,
                        'error': strategy_result.get('error', 'Unknown error')
                    })
                
                # Update checkpoint
                if strategy_result['success']:
                    self._save_checkpoint(SyncCheckpoint(
                        strategy_name=strategy.name,
                        last_sync_date=datetime.now(),
                        last_history_id=strategy_result.get('last_history_id', ''),
                        processed_count=checkpoint.processed_count + strategy_result['emails_count'] if checkpoint else strategy_result['emails_count'],
                        next_page_token=strategy_result.get('next_page_token'),
                        errors_count=checkpoint.errors_count if checkpoint else 0
                    ))
                
                # Rate limiting between strategies
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Strategy {strategy.name} failed: {e}")
                results['errors'].append({
                    'strategy': strategy.name,
                    'error': str(e)
                })
        
        # Calculate performance metrics
        total_time = (datetime.now() - start_time).total_seconds()
        results['performance_metrics'] = {
            'total_time_seconds': total_time,
            'emails_per_second': results['total_emails_retrieved'] / total_time if total_time > 0 else 0,
            'api_efficiency': results['total_emails_retrieved'] / api_calls_used if api_calls_used > 0 else 0
        }
        
        results['api_calls_used'] = api_calls_used
        results['quota_status'] = {
            'daily_quota_used_percent': (api_calls_used / self.api_limits['daily_quota']) * 100,
            'remaining_calls': max_api_calls - api_calls_used
        }
        
        # Store daily statistics
        self._store_daily_stats(results)
        
        return results
    
    async def _execute_strategy_retrieval(
        self, 
        strategy: RetrievalStrategy, 
        query: str,
        checkpoint: Optional[SyncCheckpoint],
        remaining_api_calls: int
    ) -> Dict[str, Any]:
        """Execute retrieval for a specific strategy"""
        
        try:
            emails_retrieved = []
            api_calls = 0
            page_token = checkpoint.next_page_token if checkpoint else None
            
            # Calculate max emails for this strategy
            max_emails = min(strategy.max_emails_per_run, remaining_api_calls * strategy.batch_size)
            
            while len(emails_retrieved) < max_emails and api_calls < remaining_api_calls:
                # Simulate Gmail API call (in production, replace with actual API call)
                batch_result = await self._fetch_email_batch(
                    query=query,
                    batch_size=min(strategy.batch_size, max_emails - len(emails_retrieved)),
                    page_token=page_token
                )
                
                api_calls += 1
                
                if not batch_result['messages']:
                    break
                
                emails_retrieved.extend(batch_result['messages'])
                page_token = batch_result.get('nextPageToken')
                
                if not page_token:
                    break
                
                # Rate limiting between batches
                await asyncio.sleep(0.5)
            
            return {
                'success': True,
                'emails_count': len(emails_retrieved),
                'api_calls': api_calls,
                'emails': emails_retrieved,
                'next_page_token': page_token,
                'last_history_id': batch_result.get('historyId', '')
            }
            
        except Exception as e:
            return {
                'success': False,
                'emails_count': 0,
                'api_calls': api_calls,
                'error': str(e)
            }
    
    async def _fetch_email_batch(
        self, 
        query: str, 
        batch_size: int, 
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch a batch of emails (simulated for development)"""
        
        # In production, this would make actual Gmail API calls:
        # service = build('gmail', 'v1', credentials=creds)
        # result = service.users().messages().list(
        #     userId='me',
        #     q=query,
        #     maxResults=batch_size,
        #     pageToken=page_token
        # ).execute()
        
        # Simulated response for development
        await asyncio.sleep(0.1)  # Simulate API latency
        
        messages = []
        for i in range(min(batch_size, 10)):  # Limit simulation
            message_id = f"msg_{datetime.now().timestamp()}_{i:03d}"
            messages.append({
                'id': message_id,
                'threadId': f"thread_{message_id.split('_')[1]}_{i//3:03d}",
                'snippet': f"Sample email content for {query}...",
                'payload': {
                    'headers': [
                        {'name': 'Subject', 'value': f'Sample Email {i+1}'},
                        {'name': 'From', 'value': f'sender{i}@example.com'},
                        {'name': 'Date', 'value': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}
                    ]
                }
            })
        
        response = {
            'messages': messages,
            'resultSizeEstimate': len(messages),
            'historyId': f"history_{datetime.now().timestamp()}"
        }
        
        # Add next page token if there would be more results
        if batch_size >= 10 and not page_token:
            response['nextPageToken'] = f"token_{datetime.now().timestamp()}"
        
        return response
    
    def _load_checkpoint(self, strategy_name: str) -> Optional[SyncCheckpoint]:
        """Load sync checkpoint for strategy"""
        conn = sqlite3.connect(self.checkpoint_db_path)
        cursor = conn.execute(
            "SELECT * FROM sync_checkpoints WHERE strategy_name = ?",
            (strategy_name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return SyncCheckpoint(
                strategy_name=row[0],
                last_sync_date=datetime.fromisoformat(row[1]) if row[1] else datetime.now(),
                last_history_id=row[2] or '',
                processed_count=row[3] or 0,
                next_page_token=row[4],
                errors_count=row[5] or 0
            )
        return None
    
    def _save_checkpoint(self, checkpoint: SyncCheckpoint):
        """Save sync checkpoint"""
        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute("""
            INSERT OR REPLACE INTO sync_checkpoints 
            (strategy_name, last_sync_date, last_history_id, processed_count, 
             next_page_token, errors_count, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            checkpoint.strategy_name,
            checkpoint.last_sync_date.isoformat(),
            checkpoint.last_history_id,
            checkpoint.processed_count,
            checkpoint.next_page_token,
            checkpoint.errors_count,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    
    def _store_daily_stats(self, results: Dict[str, Any]):
        """Store daily retrieval statistics"""
        today = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.checkpoint_db_path)
        conn.execute("""
            INSERT OR REPLACE INTO retrieval_stats 
            (date, total_retrieved, api_calls_used, strategies_executed, performance_metrics)
            VALUES (?, ?, ?, ?, ?)
        """, (
            today,
            results['total_emails_retrieved'],
            results['api_calls_used'],
            json.dumps([s['strategy_name'] for s in results['strategies_executed']]),
            json.dumps(results['performance_metrics'])
        ))
        conn.commit()
        conn.close()
    
    def get_retrieval_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get retrieval analytics for the past N days"""
        conn = sqlite3.connect(self.checkpoint_db_path)
        
        # Get daily stats
        cursor = conn.execute("""
            SELECT date, total_retrieved, api_calls_used, strategies_executed, performance_metrics
            FROM retrieval_stats 
            WHERE date >= date('now', '-{} days')
            ORDER BY date DESC
        """.format(days))
        
        daily_stats = []
        for row in cursor.fetchall():
            daily_stats.append({
                'date': row[0],
                'total_retrieved': row[1],
                'api_calls_used': row[2],
                'strategies_executed': json.loads(row[3]) if row[3] else [],
                'performance_metrics': json.loads(row[4]) if row[4] else {}
            })
        
        # Get strategy performance
        cursor = conn.execute("""
            SELECT strategy_name, 
                   COUNT(*) as sync_count,
                   SUM(processed_count) as total_processed,
                   AVG(processed_count) as avg_per_sync,
                   SUM(errors_count) as total_errors
            FROM sync_checkpoints 
            GROUP BY strategy_name
        """)
        
        strategy_performance = []
        for row in cursor.fetchall():
            strategy_performance.append({
                'strategy_name': row[0],
                'sync_count': row[1],
                'total_processed': row[2],
                'avg_per_sync': row[3],
                'total_errors': row[4],
                'error_rate': (row[4] / row[1]) * 100 if row[1] > 0 else 0
            })
        
        conn.close()
        
        # Calculate summary metrics
        total_retrieved = sum(day['total_retrieved'] for day in daily_stats)
        total_api_calls = sum(day['api_calls_used'] for day in daily_stats)
        
        return {
            'summary': {
                'total_emails_retrieved': total_retrieved,
                'total_api_calls_used': total_api_calls,
                'average_daily_retrieval': total_retrieved / len(daily_stats) if daily_stats else 0,
                'api_efficiency': total_retrieved / total_api_calls if total_api_calls > 0 else 0,
                'days_analyzed': len(daily_stats)
            },
            'daily_stats': daily_stats,
            'strategy_performance': strategy_performance
        }
    
    def optimize_strategies_based_on_performance(self) -> List[RetrievalStrategy]:
        """Optimize retrieval strategies based on historical performance"""
        analytics = self.get_retrieval_analytics(days=7)
        
        # Get current strategies
        strategies = self.get_optimized_retrieval_strategies()
        
        # Adjust strategies based on performance
        strategy_performance = {s['strategy_name']: s for s in analytics['strategy_performance']}
        
        optimized_strategies = []
        for strategy in strategies:
            perf = strategy_performance.get(strategy.name, {})
            
            # Adjust batch size based on error rate
            error_rate = perf.get('error_rate', 0)
            if error_rate > 10:  # High error rate
                strategy.batch_size = max(10, strategy.batch_size // 2)
            elif error_rate < 2:  # Low error rate
                strategy.batch_size = min(200, int(strategy.batch_size * 1.2))
            
            # Adjust frequency based on retrieval volume
            avg_per_sync = perf.get('avg_per_sync', 0)
            if avg_per_sync < 10 and strategy.frequency == 'hourly':
                strategy.frequency = 'daily'
            elif avg_per_sync > 100 and strategy.frequency == 'daily':
                strategy.frequency = 'hourly'
            
            optimized_strategies.append(strategy)
        
        return optimized_strategies

async def main():
    """Example usage of smart Gmail retriever"""
    retriever = SmartGmailRetriever()
    
    # Get optimized strategies
    strategies = retriever.get_optimized_retrieval_strategies()
    print(f"Generated {len(strategies)} retrieval strategies")
    
    # Execute smart retrieval
    results = await retriever.execute_smart_retrieval(
        strategies=strategies[:5],  # Execute top 5 priority strategies
        max_api_calls=50,
        time_budget_minutes=10
    )
    
    print(f"Retrieval completed:")
    print(f"- Total emails: {results['total_emails_retrieved']}")
    print(f"- API calls used: {results['api_calls_used']}")
    print(f"- Strategies executed: {len(results['strategies_executed'])}")
    
    # Get analytics
    analytics = retriever.get_retrieval_analytics(days=7)
    print(f"Analytics summary: {analytics['summary']}")

if __name__ == "__main__":
    asyncio.run(main())