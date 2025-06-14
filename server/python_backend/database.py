"""
Database management for Gmail AI email processing
SQLite with async support and optimized queries
"""

import sqlite3
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import os
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Async database manager for email data"""

    def __init__(self, db_path: str = "emails.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)

        # Create emails table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                thread_id TEXT,
                subject TEXT,
                sender TEXT,
                sender_email TEXT,
                content TEXT,
                snippet TEXT,
                labels TEXT,
                timestamp TEXT,
                is_read BOOLEAN DEFAULT FALSE,
                category_id INTEGER,
                confidence INTEGER DEFAULT 0,
                analysis_metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create categories table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#6366f1',
                count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create activities table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                email_id INTEGER,
                email_subject TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email_id) REFERENCES emails (id)
            )
        """)

        # Insert default categories
        default_categories = [
            ('Work & Business', 'Work-related emails and business communications', '#2563eb'),
            ('Personal & Family', 'Personal emails from friends and family', '#16a34a'),
            ('Finance & Banking', 'Financial statements, bills, and banking', '#dc2626'),
            ('Healthcare', 'Medical appointments and health-related emails', '#7c3aed'),
            ('Travel', 'Travel bookings, confirmations, and itineraries', '#ea580c'),
            ('Promotions', 'Marketing emails and promotional content', '#0891b2'),
            ('General', 'Uncategorized emails', '#6b7280')
        ]

        for name, desc, color in default_categories:
            conn.execute("""
                INSERT OR IGNORE INTO categories (name, description, color)
                VALUES (?, ?, ?)
            """, (name, desc, color))

        conn.commit()
        conn.close()

    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    async def initialize(self):
        """Initialize database asynchronously"""
        # Re-run initialization to ensure tables exist
        self.init_database()

    async def create_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new email record"""
        async with self.get_connection() as conn:
            try:
                cursor = conn.execute("""
                    INSERT INTO emails 
                    (message_id, thread_id, subject, sender, sender_email, content, 
                     snippet, labels, timestamp, is_read, category_id, confidence, analysis_metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    email_data['message_id'],
                    email_data.get('thread_id'),
                    email_data.get('subject'),
                    email_data.get('sender'),
                    email_data.get('sender_email'),
                    email_data.get('content'),
                    email_data.get('snippet'),
                    json.dumps(email_data.get('labels', [])),
                    email_data.get('timestamp'),
                    email_data.get('is_read', False),
                    email_data.get('category_id'),
                    email_data.get('confidence', 0),
                    json.dumps(email_data.get('analysis_metadata', {}))
                ))

                email_id = cursor.lastrowid
                conn.commit()

                # Update category count
                if email_data.get('category_id'):
                    await self._update_category_count(email_data['category_id'])

                return await self.get_email_by_id(email_id)

            except sqlite3.IntegrityError:
                # Email already exists, update it
                return await self.update_email_by_message_id(email_data['message_id'], email_data)

    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                WHERE e.id = ?
            """, (email_id,))

            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row)
            return None

    async def get_emails(self, limit: int = 50, offset: int = 0, 
                        category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get emails with pagination and filtering"""
        async with self.get_connection() as conn:
            where_clause = ""
            params = []

            if category_id:
                where_clause = "WHERE e.category_id = ?"
                params.append(category_id)

            cursor = conn.execute(f"""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                {where_clause}
                ORDER BY e.timestamp DESC
                LIMIT ? OFFSET ?
            """, params + [limit, offset])

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    async def update_email_by_message_id(self, message_id: str, 
                                       update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update email by message ID"""
        async with self.get_connection() as conn:
            set_clauses = []
            params = []

            for key, value in update_data.items():
                if key in ['subject', 'sender', 'sender_email', 'content', 'snippet', 
                          'timestamp', 'is_read', 'category_id', 'confidence']:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
                elif key == 'labels':
                    set_clauses.append("labels = ?")
                    params.append(json.dumps(value))
                elif key == 'analysis_metadata':
                    set_clauses.append("analysis_metadata = ?")
                    params.append(json.dumps(value))

            if set_clauses:
                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                params.append(message_id)

                conn.execute(f"""
                    UPDATE emails SET {', '.join(set_clauses)}
                    WHERE message_id = ?
                """, params)
                conn.commit()

            # Get updated email
            cursor = conn.execute("SELECT id FROM emails WHERE message_id = ?", (message_id,))
            row = cursor.fetchone()
            if row:
                return await self.get_email_by_id(row['id'])
            return {}

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, description, color, 
                       (SELECT COUNT(*) FROM emails WHERE category_id = categories.id) as count
                FROM categories
                ORDER BY name
            """)

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    async def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO categories (name, description, color)
                VALUES (?, ?, ?)
            """, (
                category_data['name'],
                category_data.get('description'),
                category_data.get('color', '#6366f1')
            ))

            category_id = cursor.lastrowid
            conn.commit()

            return {
                'id': category_id,
                'name': category_data['name'],
                'description': category_data.get('description'),
                'color': category_data.get('color', '#6366f1'),
                'count': 0
            }

    async def create_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new activity record"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO activities (type, description, email_id, email_subject, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                activity_data['type'],
                activity_data['description'],
                activity_data.get('email_id'),
                activity_data.get('email_subject'),
                json.dumps(activity_data.get('metadata', {}))
            ))

            activity_id = cursor.lastrowid
            conn.commit()

            return {
                'id': activity_id,
                'type': activity_data['type'],
                'description': activity_data['description'],
                'email_id': activity_data.get('email_id'),
                'email_subject': activity_data.get('email_subject'),
                'metadata': activity_data.get('metadata', {}),
                'created_at': datetime.now().isoformat()
            }

    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM activities
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        async with self.get_connection() as conn:
            # Get total emails
            cursor = conn.execute("SELECT COUNT(*) as total FROM emails")
            total_emails = cursor.fetchone()['total']

            # Get unread emails
            cursor = conn.execute("SELECT COUNT(*) as unread FROM emails WHERE is_read = FALSE")
            unread_emails = cursor.fetchone()['unread']

            # Get categories count
            cursor = conn.execute("SELECT COUNT(*) as total FROM categories")
            total_categories = cursor.fetchone()['total']

            # Get recent activities count
            cursor = conn.execute("SELECT COUNT(*) as total FROM activities")
            total_activities = cursor.fetchone()['total']

            # Get top categories
            cursor = conn.execute("""
                SELECT c.name, c.color, COUNT(e.id) as count
                FROM categories c
                LEFT JOIN emails e ON c.id = e.category_id
                GROUP BY c.id, c.name, c.color
                ORDER BY count DESC
                LIMIT 5
            """)
            top_categories = [self._row_to_dict(row) for row in cursor.fetchall()]

            return {
                'totalEmails': total_emails,
                'autoLabeled': total_emails,  # Assuming all are auto-labeled
                'categories': total_categories,
                'timeSaved': "2.5 hours",
                'weeklyGrowth': {
                    'emails': total_emails,
                    'percentage': 15.0
                },
                'topCategories': top_categories
            }

    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit, offset)

    async def get_emails_by_category(self, category_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit, offset, category_id)

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails by content or subject"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                WHERE e.subject LIKE ? OR e.content LIKE ?
                ORDER BY e.timestamp DESC
                LIMIT ?
            """, (f"%{search_term}%", f"%{search_term}%", limit))

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    async def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        return await self.get_categories()

    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent emails for analysis"""
        async with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT e.*, c.name as category_name, c.color as category_color
                FROM emails e
                LEFT JOIN categories c ON e.category_id = c.id
                ORDER BY e.timestamp DESC
                LIMIT ?
            """, (limit,))

            return [self._row_to_dict(row) for row in cursor.fetchall()]

    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update email by ID"""
        async with self.get_connection() as conn:
            set_clauses = []
            params = []

            for key, value in update_data.items():
                if key in ['subject', 'content', 'sender', 'sender_email', 
                          'is_read', 'is_important', 'is_starred', 'category_id', 'confidence']:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
                elif key == 'labels':
                    set_clauses.append("labels = ?")
                    params.append(json.dumps(value))

            if set_clauses:
                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                params.append(email_id)

                conn.execute(f"""
                    UPDATE emails SET {', '.join(set_clauses)}
                    WHERE id = ?
                """, params)
                conn.commit()

                return await self.get_email_by_id(email_id)
            return None

    async def _update_category_count(self, category_id: int):
        """Update category email count"""
        async with self.get_connection() as conn:
            conn.execute("""
                UPDATE categories 
                SET count = (SELECT COUNT(*) FROM emails WHERE category_id = ?)
                WHERE id = ?
            """, (category_id, category_id))
            conn.commit()

    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary"""
        result = dict(row)

        # Parse JSON fields
        if 'labels' in result and result['labels']:
            try:
                result['labels'] = json.loads(result['labels'])
            except:
                result['labels'] = []

        if 'analysis_metadata' in result and result['analysis_metadata']:
            try:
                result['analysis_metadata'] = json.loads(result['analysis_metadata'])
            except:
                result['analysis_metadata'] = {}

        if 'metadata' in result and result['metadata']:
            try:
                result['metadata'] = json.loads(result['metadata'])
            except:
                result['metadata'] = {}

        return result

async def get_db() -> DatabaseManager:
    """Dependency injection for database"""
    return DatabaseManager()