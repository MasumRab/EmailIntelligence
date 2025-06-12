"""
Database Manager for Gmail AI Email Management
Optimized PostgreSQL operations with async support
"""

import asyncio
import asyncpg
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from contextlib import asynccontextmanager

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Async PostgreSQL database manager with connection pooling"""
    
    def __init__(self):
        self.pool = None
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
    
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=5,
                max_size=20,
                command_timeout=60,
                server_settings={
                    'jit': 'off'  # Disable JIT for better performance on small queries
                }
            )
            
            # Initialize schema
            await self._create_tables()
            await self._create_indexes()
            
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def _create_tables(self):
        """Create database tables"""
        async with self.pool.acquire() as conn:
            # Categories table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    color VARCHAR(7) NOT NULL DEFAULT '#6366f1',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Enhanced emails table with comprehensive metadata
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    id SERIAL PRIMARY KEY,
                    message_id VARCHAR(255) UNIQUE,
                    thread_id VARCHAR(255),
                    history_id VARCHAR(255),
                    sender VARCHAR(255) NOT NULL,
                    sender_email VARCHAR(255) NOT NULL,
                    subject TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_html TEXT,
                    preview TEXT,
                    time TIMESTAMP NOT NULL,
                    category_id INTEGER REFERENCES categories(id),
                    labels JSONB DEFAULT '[]',
                    confidence INTEGER DEFAULT 0,
                    is_important BOOLEAN DEFAULT FALSE,
                    is_starred BOOLEAN DEFAULT FALSE,
                    is_unread BOOLEAN DEFAULT TRUE,
                    is_read BOOLEAN DEFAULT FALSE,
                    has_attachments BOOLEAN DEFAULT FALSE,
                    attachment_count INTEGER DEFAULT 0,
                    size_estimate INTEGER DEFAULT 0,
                    spam_score REAL DEFAULT 0.0,
                    encryption_status VARCHAR(50),
                    authentication_results JSONB,
                    delivery_status VARCHAR(50),
                    folder_location VARCHAR(255),
                    ai_analysis JSONB,
                    filter_results JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Activities table for audit trail
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id SERIAL PRIMARY KEY,
                    type VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    email_id INTEGER REFERENCES emails(id),
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Gmail sync sessions
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS gmail_sync_sessions (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) UNIQUE NOT NULL,
                    sync_type VARCHAR(100),
                    query_filter TEXT,
                    emails_processed INTEGER DEFAULT 0,
                    emails_created INTEGER DEFAULT 0,
                    errors_count INTEGER DEFAULT 0,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'running',
                    performance_metrics JSONB DEFAULT '{}'
                )
            """)
            
            # Email filters tracking
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS email_filters (
                    id SERIAL PRIMARY KEY,
                    filter_id VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    criteria JSONB NOT NULL,
                    actions JSONB NOT NULL,
                    priority INTEGER DEFAULT 5,
                    effectiveness_score REAL DEFAULT 0.0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0,
                    false_positive_rate REAL DEFAULT 0.0,
                    performance_metrics JSONB DEFAULT '{}',
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Performance metrics storage
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id SERIAL PRIMARY KEY,
                    metric_type VARCHAR(100) NOT NULL,
                    metric_name VARCHAR(255) NOT NULL,
                    metric_value REAL NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    async def _create_indexes(self):
        """Create database indexes for performance"""
        async with self.pool.acquire() as conn:
            # Email indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_sender_email ON emails(sender_email)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_time ON emails(time DESC)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_category ON emails(category_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_labels ON emails USING GIN(labels)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_message_id ON emails(message_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_thread_id ON emails(thread_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_is_unread ON emails(is_unread)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_is_important ON emails(is_important)")
            
            # Full text search
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_emails_search 
                ON emails USING GIN(to_tsvector('english', subject || ' ' || content))
            """)
            
            # Activity indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(type)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_activities_created_at ON activities(created_at DESC)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_activities_email_id ON activities(email_id)")
            
            # Performance indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_performance_type_name ON performance_metrics(metric_type, metric_name)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_performance_recorded_at ON performance_metrics(recorded_at DESC)")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        async with self.pool.acquire() as conn:
            yield conn
    
    # Dashboard Statistics
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        async with self.get_connection() as conn:
            # Total emails count
            total_emails = await conn.fetchval("SELECT COUNT(*) FROM emails")
            
            # Auto-labeled emails (with AI analysis)
            auto_labeled = await conn.fetchval("""
                SELECT COUNT(*) FROM emails 
                WHERE ai_analysis IS NOT NULL AND ai_analysis != '{}'
            """)
            
            # Categories count
            categories_count = await conn.fetchval("SELECT COUNT(*) FROM categories")
            
            # Weekly growth
            week_ago = datetime.now() - timedelta(days=7)
            weekly_growth = await conn.fetchval("""
                SELECT COUNT(*) FROM emails WHERE created_at >= $1
            """, week_ago)
            
            # Time saved estimation (based on auto-labeling)
            time_saved_minutes = auto_labeled * 2  # Assume 2 minutes saved per auto-labeled email
            time_saved = f"{time_saved_minutes // 60}h {time_saved_minutes % 60}m"
            
            return {
                "totalEmails": total_emails,
                "autoLabeled": auto_labeled,
                "categories": categories_count,
                "timeSaved": time_saved,
                "weeklyGrowth": {
                    "emails": weekly_growth,
                    "percentage": round((weekly_growth / max(total_emails - weekly_growth, 1)) * 100, 1)
                }
            }
    
    # Email Operations
    async def get_all_emails(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                ORDER BY e.time DESC
                LIMIT $1 OFFSET $2
            """, limit, offset)
            
            return [self._format_email_row(row) for row in rows]
    
    async def get_emails_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Get emails by category"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                WHERE e.category_id = $1
                ORDER BY e.time DESC
            """, category_id)
            
            return [self._format_email_row(row) for row in rows]
    
    async def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """Search emails using full-text search"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT e.*, c.name as category_name, c.color as category_color,
                       ts_rank(to_tsvector('english', e.subject || ' ' || e.content), plainto_tsquery('english', $1)) as rank
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                WHERE to_tsvector('english', e.subject || ' ' || e.content) @@ plainto_tsquery('english', $1)
                   OR e.sender_email ILIKE $2
                   OR e.sender ILIKE $2
                ORDER BY rank DESC, e.time DESC
                LIMIT 50
            """, query, f"%{query}%")
            
            return [self._format_email_row(row) for row in rows]
    
    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get specific email by ID"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                WHERE e.id = $1
            """, email_id)
            
            return self._format_email_row(row) if row else None
    
    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new email"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow("""
                INSERT INTO emails (
                    message_id, thread_id, sender, sender_email, subject, content,
                    content_html, preview, time, category_id, labels, confidence,
                    is_important, is_starred, is_unread, has_attachments,
                    attachment_count, size_estimate, ai_analysis, filter_results
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20
                ) RETURNING *
            """,
                email_data.get('messageId'),
                email_data.get('threadId'),
                email_data['sender'],
                email_data['senderEmail'],
                email_data['subject'],
                email_data['content'],
                email_data.get('contentHtml'),
                email_data.get('preview', email_data['content'][:200]),
                datetime.fromisoformat(email_data['time'].replace('Z', '+00:00')) if isinstance(email_data['time'], str) else email_data['time'],
                email_data.get('categoryId'),
                json.dumps(email_data.get('labels', [])),
                email_data.get('confidence', 0),
                email_data.get('isImportant', False),
                email_data.get('isStarred', False),
                email_data.get('isUnread', True),
                email_data.get('hasAttachments', False),
                email_data.get('attachmentCount', 0),
                email_data.get('sizeEstimate', 0),
                json.dumps(email_data.get('analysisMetadata', {})),
                json.dumps(email_data.get('filterResults', {}))
            )
            
            return self._format_email_row(row)
    
    async def update_email(self, email_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update email"""
        if not updates:
            return await self.get_email_by_id(email_id)
        
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        field_mapping = {
            'isImportant': 'is_important',
            'isStarred': 'is_starred',
            'isUnread': 'is_unread',
            'isRead': 'is_read',
            'categoryId': 'category_id'
        }
        
        for key, value in updates.items():
            db_field = field_mapping.get(key, key.lower())
            if key == 'labels':
                value = json.dumps(value)
            set_clauses.append(f"{db_field} = ${param_count}")
            values.append(value)
            param_count += 1
        
        set_clauses.append(f"updated_at = ${param_count}")
        values.append(datetime.now())
        param_count += 1
        
        values.append(email_id)
        
        query = f"""
            UPDATE emails 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *
        """
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, *values)
            return self._format_email_row(row) if row else None
    
    def _format_email_row(self, row) -> Dict[str, Any]:
        """Format email database row to response format"""
        if not row:
            return None
        
        return {
            "id": row['id'],
            "messageId": row['message_id'],
            "threadId": row['thread_id'],
            "sender": row['sender'],
            "senderEmail": row['sender_email'],
            "subject": row['subject'],
            "content": row['content'],
            "contentHtml": row.get('content_html'),
            "preview": row['preview'],
            "time": row['time'].isoformat(),
            "category": row.get('category_name'),
            "categoryId": row['category_id'],
            "labels": json.loads(row['labels']) if row['labels'] else [],
            "confidence": row['confidence'],
            "isImportant": row['is_important'],
            "isStarred": row['is_starred'],
            "isUnread": row['is_unread'],
            "hasAttachments": row.get('has_attachments', False),
            "attachmentCount": row.get('attachment_count', 0),
            "sizeEstimate": row.get('size_estimate', 0),
            "aiAnalysis": json.loads(row['ai_analysis']) if row.get('ai_analysis') else {},
            "filterResults": json.loads(row['filter_results']) if row.get('filter_results') else {}
        }
    
    # Category Operations
    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with email counts"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT c.*, COUNT(e.id) as email_count
                FROM categories c
                LEFT JOIN emails e ON c.id = e.category_id
                GROUP BY c.id, c.name, c.description, c.color, c.created_at
                ORDER BY c.name
            """)
            
            return [{
                "id": row['id'],
                "name": row['name'],
                "description": row['description'],
                "color": row['color'],
                "count": row['email_count']
            } for row in rows]
    
    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new category"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow("""
                INSERT INTO categories (name, description, color)
                VALUES ($1, $2, $3)
                RETURNING *
            """,
                category_data['name'],
                category_data.get('description'),
                category_data.get('color', '#6366f1')
            )
            
            return {
                "id": row['id'],
                "name": row['name'],
                "description": row['description'],
                "color": row['color'],
                "count": 0
            }
    
    # Activity Operations
    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT a.*, e.subject as email_subject
                FROM activities a
                LEFT JOIN emails e ON a.email_id = e.id
                ORDER BY a.created_at DESC
                LIMIT $1
            """, limit)
            
            return [{
                "id": row['id'],
                "type": row['type'],
                "description": row['description'],
                "emailId": row['email_id'],
                "emailSubject": row.get('email_subject'),
                "metadata": json.loads(row['metadata']) if row['metadata'] else {},
                "createdAt": row['created_at'].isoformat()
            } for row in rows]
    
    async def create_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new activity"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow("""
                INSERT INTO activities (type, description, email_id, metadata)
                VALUES ($1, $2, $3, $4)
                RETURNING *
            """,
                activity_data['type'],
                activity_data['description'],
                activity_data.get('emailId'),
                json.dumps(activity_data.get('metadata', {}))
            )
            
            return {
                "id": row['id'],
                "type": row['type'],
                "description": row['description'],
                "emailId": row['email_id'],
                "metadata": json.loads(row['metadata']) if row['metadata'] else {},
                "createdAt": row['created_at'].isoformat()
            }
    
    # Utility Methods
    async def get_recent_emails(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get recent emails for analysis"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT * FROM emails 
                ORDER BY created_at DESC 
                LIMIT $1
            """, limit)
            
            return [self._format_email_row(row) for row in rows]
    
    async def get_emails_for_training(self, query: str = "newer_than:30d", limit: int = 5000) -> List[Dict[str, Any]]:
        """Get emails for AI training"""
        # For now, get recent emails - in production this would parse the Gmail query
        return await self.get_recent_emails(limit)
    
    async def health_check(self) -> Dict[str, str]:
        """Check database health"""
        try:
            async with self.get_connection() as conn:
                await conn.fetchval("SELECT 1")
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()

# Dependency injection for FastAPI
async def get_db() -> DatabaseManager:
    """Get database manager instance"""
    db = DatabaseManager()
    if not db.pool:
        await db.initialize()
    return db