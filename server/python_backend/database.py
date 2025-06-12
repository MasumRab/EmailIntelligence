"""
Database management for Gmail AI email processing
PostgreSQL implementation.
"""

import psycopg2
import psycopg2.extras # For RealDictCursor
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import os
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Async database manager for email data using PostgreSQL"""

    def __init__(self, db_url: Optional[str] = None):
        self.database_url = db_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            logger.error("DATABASE_URL environment variable not set.")
            raise ValueError("DATABASE_URL environment variable not set.")
        # self.init_database() # Table creation handled by Drizzle ORM based on schema.ts
        # Seeding default data can be done here if needed, or via a separate script.

    async def _execute_query(self, query: str, params: Optional[Tuple] = None, fetch_one: bool = False, fetch_all: bool = False, commit: bool = False):
        """Helper to execute queries using asyncio.to_thread for sync psycopg2."""
        conn = await asyncio.to_thread(psycopg2.connect, self.database_url)
        try:
            # Use RealDictCursor for dictionary-like row access
            async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                await asyncio.to_thread(cur.execute, query, params)

                result = None
                if fetch_one:
                    result_row = await asyncio.to_thread(cur.fetchone)
                    result = dict(result_row) if result_row else None
                elif fetch_all:
                    result_rows = await asyncio.to_thread(cur.fetchall)
                    result = [dict(row) for row in result_rows]

                if commit:
                    await asyncio.to_thread(conn.commit)

                # For INSERT returning id, psycopg2 handles it differently
                if query.strip().upper().startswith("INSERT") and "RETURNING id" in query.lower() and not result:
                    # If RETURNING id was used and fetch_one wasn't (e.g. if we only want lastrowid equivalent)
                    # For psycopg2, RETURNING is the standard way.
                    # If we need the ID and didn't fetch_one, we assume the query was like "INSERT ... RETURNING id"
                    # and the result should have been fetched.
                    # If fetch_one was True with RETURNING id, it's already in 'result'.
                    # This part might need adjustment based on how INSERT ... RETURNING is used.
                    # If lastrowid is needed, it's better to use RETURNING id and fetch_one.
                    pass # result would be set if RETURNING was used with fetch_one

                return result
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            await asyncio.to_thread(conn.rollback) # Rollback on error
            raise
        finally:
            await asyncio.to_thread(conn.close)

    def init_database(self):
        """
        Initializes the database with default categories.
        Table creation is assumed to be handled by Drizzle migrations.
        This method now only seeds default categories if they don't exist.
        """
        default_categories = [
            ('Work & Business', 'Work-related emails and business communications', '#2563eb'),
            ('Personal & Family', 'Personal emails from friends and family', '#16a34a'),
            ('Finance & Banking', 'Financial statements, bills, and banking', '#dc2626'),
            ('Healthcare', 'Medical appointments and health-related emails', '#7c3aed'),
            ('Travel', 'Travel bookings, confirmations, and itineraries', '#ea580c'),
            ('Promotions', 'Marketing emails and promotional content', '#0891b2'),
            ('General', 'Uncategorized emails', '#6b7280')
        ]

        # This function must be called from an async context if it uses _execute_query
        # For simplicity in __init__, this part might be called separately or made synchronous
        # if __init__ itself is not async.
        # For now, let's make it a synchronous helper for init_database if needed.
        conn = psycopg2.connect(self.database_url)
        try:
            with conn.cursor() as cur:
                for name, desc, color in default_categories:
                    # Assuming 'name' should be unique for these default categories.
                    # The schema.ts doesn't enforce unique name for categories globally,
                    # but for default seeding, ON CONFLICT is useful.
                    # If categories table has a unique constraint on 'name':
                    # cur.execute("""
                    #     INSERT INTO categories (name, description, color)
                    #     VALUES (%s, %s, %s)
                    #     ON CONFLICT (name) DO NOTHING;
                    # """, (name, desc, color))
                    # If no unique constraint, or if userId is involved for uniqueness (not in current schema.ts for categories)
                    # We might need to check existence first
                    cur.execute("SELECT id FROM categories WHERE name = %s", (name,))
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO categories (name, description, color, count)
                            VALUES (%s, %s, %s, %s)
                        """, (name, desc, color, 0))
                conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Error seeding default categories: {e}")
            conn.rollback()
        finally:
            conn.close()


    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections using psycopg2."""
        conn = None
        try:
            conn = await asyncio.to_thread(psycopg2.connect, self.database_url)
            conn.autocommit = False # Ensure transactions are handled explicitly
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            if conn: # pragma: no cover
                 await asyncio.to_thread(conn.rollback) # Rollback before raising
            raise
        finally:
            if conn:
                await asyncio.to_thread(conn.close)
    
    async def initialize(self):
        """Initialize database asynchronously (e.g., seed data)"""
        # This method is kept for API consistency if needed later for more async init steps.
        # For now, default data seeding is in the synchronous init_database,
        # which itself could be called from here if made async or wrapped.
        # Let's assume init_database() is called from constructor for now for seeding.
        logger.info("DatabaseManager initialized. Default categories seeding attempted if constructor called it.")
        pass


    def _parse_json_fields(self, row: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """Helper to parse stringified JSON fields in a row."""
        if not row:
            return row
        for field in fields:
            if field in row and isinstance(row[field], str):
                try:
                    row[field] = json.loads(row[field])
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON for field {field} in row {row.get('id')}")
                    row[field] = {} if field == 'analysisMetadata' or field == 'metadata' else [] # Default based on expected type
        return row

    async def create_email(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new email record.
        Note: `schema.ts` has `isUnread` (bool) and a legacy `isRead` (bool).
        The input `email_data` might have `is_read`. We need to map to `isUnread`.
        `is_read = True` means `isUnread = False`.
        `is_read = False` means `isUnread = True`.
        """
        # Schema default for isUnread is TRUE. So if 'is_read' is not provided, assume it's NOT read (isUnread=True).
        # email_data.get('is_read', False) means if 'is_read' is absent, consider it False.
        # not False -> True. So isUnread defaults to True. This matches schema.
        is_unread = not email_data.get('is_read', False)

        query = """
            INSERT INTO emails
            ("messageId", "threadId", subject, sender, "senderEmail", content, snippet, labels, "time", "isUnread", "categoryId", confidence, "analysisMetadata", "createdAt", "updatedAt",
             "historyId", "contentHtml", preview, "toAddresses", "ccAddresses", "bccAddresses", "replyTo", "internalDate", "labelIds", category, "isStarred", "isImportant", "isDraft", "isSent", "isSpam", "isTrash", "isChat", "hasAttachments", "attachmentCount", "sizeEstimate", "spfStatus", "dkimStatus", "dmarcStatus", "isEncrypted", "isSigned", priority, "isAutoReply", "mailingList", "inReplyTo", "references", "isFirstInThread")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(),
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        # Ensure all fields from schema.ts are accounted for, using defaults if not provided
        params = (
            email_data.get('messageId', email_data.get('message_id')), # Map from old `message_id` if present
            email_data.get('threadId', email_data.get('thread_id')),
            email_data.get('subject'),
            email_data.get('sender'),
            email_data.get('senderEmail', email_data.get('sender_email')),
            email_data.get('content'),
            email_data.get('snippet'),
            email_data.get('labels', []), # Should be a list of strings
            email_data.get('time', email_data.get('timestamp')), # Map from old `timestamp`
            is_unread,
            email_data.get('categoryId', email_data.get('category_id')),
            email_data.get('confidence', 0),
            json.dumps(email_data.get('analysisMetadata', email_data.get('analysis_metadata', {}))),
            email_data.get('historyId'),
            email_data.get('contentHtml'),
            email_data.get('preview', email_data.get('snippet')), # Use snippet if preview not present
            email_data.get('toAddresses', []),
            email_data.get('ccAddresses', []),
            email_data.get('bccAddresses', []),
            email_data.get('replyTo'),
            email_data.get('internalDate'),
            email_data.get('labelIds', []),
            email_data.get('category'),
            email_data.get('isStarred', False),
            email_data.get('isImportant', False),
            email_data.get('isDraft', False),
            email_data.get('isSent', False),
            email_data.get('isSpam', False),
            email_data.get('isTrash', False),
            email_data.get('isChat', False),
            email_data.get('hasAttachments', False),
            email_data.get('attachmentCount', 0),
            email_data.get('sizeEstimate'),
            email_data.get('spfStatus'),
            email_data.get('dkimStatus'),
            email_data.get('dmarcStatus'),
            email_data.get('isEncrypted', False),
            email_data.get('isSigned', False),
            email_data.get('priority', 'normal'),
            email_data.get('isAutoReply', False),
            email_data.get('mailingList'),
            email_data.get('inReplyTo'),
            email_data.get('references', []),
            email_data.get('isFirstInThread', True)
        )
        try:
            result = await self._execute_query(query, params, fetch_one=True, commit=True)
            if result and result.get('id'):
                email_id = result['id']
                # Update category count if categoryId is present
                category_id = email_data.get('categoryId', email_data.get('category_id'))
                if category_id:
                    await self._update_category_count(category_id) # Make sure this is adapted too
                return await self.get_email_by_id(email_id) # Adapted to fetch full dict
            return None
        except psycopg2.IntegrityError as e:
            # This IntegrityError check is for UNIQUE constraint on messageId
            logger.warning(f"Email with messageId {email_data.get('messageId')} likely already exists: {e}")
            # Attempt to update if it already exists
            # Note: Drizzle schema for emails.messageId does not have .notNull() which is strange. Assuming it is effectively notNull.
            return await self.update_email_by_message_id(email_data['messageId'], email_data)


    async def get_email_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email by ID"""
        query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e."categoryId" = c.id
            WHERE e.id = %s
        """
        # Important: Accessing e.* will get all columns. If some are JSON strings, they need parsing.
        # RealDictCursor returns dicts, but JSON stored as text is still text.
        row = await self._execute_query(query, (email_id,), fetch_one=True)
        return self._parse_json_fields(row, ['analysisMetadata']) if row else None


    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their counts."""
        # The schema.ts has `count` in `categories` table.
        # This implies the count is maintained there.
        # The old query dynamically calculated count. If `categories.count` is reliable:
        query = """
            SELECT id, name, description, color, count
            FROM categories
            ORDER BY name
        """
        # If categories.count is NOT reliable and needs dynamic calculation:
        # query = """
        #     SELECT c.id, c.name, c.description, c.color,
        #            (SELECT COUNT(*) FROM emails e WHERE e."categoryId" = c.id) as count
        #     FROM categories c
        #     ORDER BY c.name
        # """
        # Assuming schema.ts `count` field is maintained and accurate.
        categories = await self._execute_query(query, fetch_all=True)
        return categories if categories else []

    async def create_category(self, category_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new category.
           The schema.ts for categories has id, name, description, color, count.
           It does not have userId.
        """
        query = """
            INSERT INTO categories (name, description, color, count)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, description, color, count;
        """
        params = (
            category_data['name'],
            category_data.get('description'),
            category_data.get('color', '#6366f1'),
            category_data.get('count', 0) # Default count to 0
        )
        try:
            # ON CONFLICT (name) DO NOTHING; could be added if name should be unique
            # but schema.ts doesn't specify this. For now, allow duplicates or handle at app level.
            new_category = await self._execute_query(query, params, fetch_one=True, commit=True)
            return new_category
        except psycopg2.Error as e:
            logger.error(f"Failed to create category {category_data.get('name')}: {e}")
            return None

    async def _update_category_count(self, category_id: int):
        """Update category email count."""
        # This method assumes there's a "count" column in the "categories" table.
        # schema.ts confirms `count: integer("count").default(0)`
        query = """
            UPDATE categories
            SET count = (SELECT COUNT(*) FROM emails WHERE "categoryId" = %s)
            WHERE id = %s
        """
        await self._execute_query(query, (category_id, category_id), commit=True)


    # ... other methods to be adapted ...
    # For now, let's placeholder them or comment out
    async def get_emails(self, limit: int = 50, offset: int = 0, 
                        category_id: Optional[int] = None, is_unread: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get emails with pagination and filtering.
        'is_unread' corresponds to 'isUnread' in the schema.
        'timestamp' from old code maps to 'time' in new schema for ordering.
        """
        params = []
        base_query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e."categoryId" = c.id
        """

        where_clauses = []
        if category_id is not None:
            where_clauses.append('e."categoryId" = %s')
            params.append(category_id)

        if is_unread is not None:
            where_clauses.append('e."isUnread" = %s') # Directly use isUnread
            params.append(is_unread)

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += ' ORDER BY e."time" DESC LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        emails = await self._execute_query(base_query, tuple(params), fetch_all=True)
        if emails:
            return [self._parse_json_fields(email, ['analysisMetadata']) for email in emails]
        return []

    async def update_email_by_message_id(self, message_id: str, 
                                       update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update email by messageId.
        Handles 'is_read' to 'isUnread' conversion.
        Other schema.ts fields should be used directly if present in update_data.
        """
        set_clauses = []
        params = []

        # Mapping from old Python keys to new schema keys if necessary, or direct use
        # Fields from schema.ts: subject, sender, senderEmail, content, snippet, time, isUnread, categoryId, confidence, labels, analysisMetadata, etc.
        # Quoted column names are essential.

        for key, value in update_data.items():
            column_name = key
            # Handle specific mappings or transformations
            if key == "message_id": continue # Cannot update message_id itself, it's for the WHERE clause
            if key == "is_read": # Legacy key from old Python code
                column_name = '"isUnread"'
                value = not value # Invert logic
            elif key == "category_id":
                column_name = '"categoryId"'
            elif key == "sender_email":
                column_name = '"senderEmail"'
            elif key == "thread_id":
                column_name = '"threadId"'
            elif key == "analysis_metadata": # Stored as JSON string
                column_name = '"analysisMetadata"'
                value = json.dumps(value)
            elif key == "labels": # Stored as text array
                column_name = '"labels"'
                # psycopg2 handles Python list to PG array, ensure value is a list
                if not isinstance(value, list):
                    logger.warning(f"Labels value for update is not a list: {value}, attempting to wrap.")
                    value = [str(value)] # Or handle error appropriately
            elif key == "timestamp": # old key, maps to "time"
                column_name = '"time"'
            else: # For other keys, assume they match schema.ts (camelCased) and quote them
                column_name = f'"{key}"'


            set_clauses.append(f"{column_name} = %s")
            params.append(value)

        if not set_clauses:
            logger.warning("No valid fields to update for message_id: {message_id}")
            return await self.get_email_by_message_id(message_id) # Return current state if no updates

        set_clauses.append('"updatedAt" = NOW()')

        query = f"""
            UPDATE emails SET {', '.join(set_clauses)}
            WHERE "messageId" = %s
        """
        params.append(message_id)

        await self._execute_query(query, tuple(params), commit=True)

        # Fetch and return the updated email using the internal ID
        # This requires a way to get 'id' from 'messageId' if not already available.
        # For simplicity, if get_email_by_message_id is implemented, use that.
        return await self.get_email_by_message_id(message_id)

    async def get_email_by_message_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get email by messageId (similar to get_email_by_id but uses messageId)"""
        query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e."categoryId" = c.id
            WHERE e."messageId" = %s
        """
        row = await self._execute_query(query, (message_id,), fetch_one=True)
        return self._parse_json_fields(row, ['analysisMetadata']) if row else None


    async def create_activity(self, activity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new activity record.
           Schema: id, type, description, details, timestamp, icon, iconBg
        """
        query = """
            INSERT INTO activities (type, description, details, "timestamp", icon, "iconBg")
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, type, description, details, "timestamp", icon, "iconBg";
        """
        # The old 'metadata' field can map to 'details' (as text/JSON string)
        # 'email_id' and 'email_subject' from old schema should be part of 'details' if needed.
        details_data = activity_data.get('metadata', {})
        if 'email_id' in activity_data:
            details_data['emailId'] = activity_data['email_id'] # Match camelCase
        if 'email_subject' in activity_data:
            details_data['emailSubject'] = activity_data['email_subject']

        params = (
            activity_data['type'],
            activity_data['description'],
            json.dumps(details_data) if details_data else None,
            activity_data.get('timestamp', datetime.now().isoformat()), # Ensure ISO format for text timestamp
            activity_data.get('icon', 'default_icon'), # Provide defaults if not in activity_data
            activity_data.get('iconBg', '#ffffff')    # Provide defaults
        )
        new_activity = await self._execute_query(query, params, fetch_one=True, commit=True)
        return self._parse_json_fields(new_activity, ['details']) if new_activity else None


    async def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities"""
        query = """
            SELECT id, type, description, details, "timestamp", icon, "iconBg"
            FROM activities
            ORDER BY "timestamp" DESC
            LIMIT %s
        """
        activities = await self._execute_query(query, (limit,), fetch_all=True)
        if activities:
            return [self._parse_json_fields(activity, ['details']) for activity in activities]
        return []

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        logger.warning("get_dashboard_stats not fully migrated to PostgreSQL yet.")
        # This method needs significant rework based on the new schema and how stats are derived.
        # For example, 'autoLabeled' and 'timeSaved' are not direct DB fields.
        # Category counts will need to use the 'categories.count' field or a new query.
        # For now, return a basic structure.

        results = await asyncio.gather(
            self._execute_query('SELECT COUNT(*) AS count FROM emails', fetch_one=True),
            self._execute_query('SELECT COUNT(*) AS count FROM emails WHERE "isUnread" = TRUE', fetch_one=True),
            self._execute_query('SELECT COUNT(*) AS count FROM emails WHERE priority = %s', ('high',), fetch_one=True), # For "important"
            self._execute_query('SELECT COUNT(*) AS count FROM emails WHERE "isSpam" = TRUE', fetch_one=True), # Using isSpam field
            self._execute_query('SELECT COUNT(*) AS count FROM categories', fetch_one=True),
            self._execute_query('SELECT name, color, count FROM categories ORDER BY count DESC LIMIT 5', fetch_all=True)
        )

        total_emails = results[0]['count'] if results[0] else 0
        unread_emails = results[1]['count'] if results[1] else 0
        important_emails = results[2]['count'] if results[2] else 0
        spam_emails = results[3]['count'] if results[3] else 0
        total_category_types = results[4]['count'] if results[4] else 0
        top_categories_list = results[5] if results[5] else []

        # The 'DashboardStats' type in schema.ts has more complex fields like 'weeklyGrowth'.
        # These are likely calculated in application logic or are placeholders.
        # The python backend should provide the raw counts it can get.
        return {
            'totalEmails': total_emails,
            'unreadEmails': unread_emails,
            'importantEmails': important_emails,
            'spamEmails': spam_emails,
            'totalCategoryTypes': total_category_types,
            'topCategories': top_categories_list,

            # Placeholders for fields not directly derivable from current DB structure by this function alone
            'autoLabeled': total_emails,  # Example: Assuming all emails are auto-labeled for now
            'timeSaved': "2.5 hours", # Example: static or calculated elsewhere
            # weeklyGrowth would require historical data not currently queried here.
            'weeklyGrowth': {
                'totalEmails': total_emails, # This is current total, not growth
                'autoLabeled': total_emails, # Placeholder
                'categories': total_category_types, # Placeholder
                'timeSaved': 0 # Placeholder
            }
        }


    # --- Methods to be fully adapted or verified ---
    async def get_all_emails(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all emails with pagination"""
        return await self.get_emails(limit=limit, offset=offset) # Relies on get_emails

    async def get_emails_by_category(self, category_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get emails by category"""
        return await self.get_emails(limit=limit, offset=offset, category_id=category_id) # Relies on get_emails

    async def search_emails(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search emails by content or subject.
        Uses ILIKE for case-insensitive search in PostgreSQL.
        Orders by 'time' (reception time).
        """
        query = """
            SELECT e.*, c.name as "categoryName", c.color as "categoryColor"
            FROM emails e
            LEFT JOIN categories c ON e."categoryId" = c.id
            WHERE e.subject ILIKE %s OR e.content ILIKE %s
            ORDER BY e."time" DESC
            LIMIT %s
        """
        # The schema has e.preview and e.snippet as well, could be included in search
        params = (f"%{search_term}%", f"%{search_term}%", limit)
        emails = await self._execute_query(query, params, fetch_all=True)
        if emails:
            return [self._parse_json_fields(email, ['analysisMetadata']) for email in emails]
        return []


    async def get_recent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent emails for analysis, ordered by reception time."""
        # This effectively calls get_emails without specific filters, ordered by time.
        return await self.get_emails(limit=limit, offset=0)


    async def update_email(self, email_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update email by its internal ID.
        This is similar to update_email_by_message_id but uses the primary key 'id'.
        """
        set_clauses = []
        params = []

        for key, value in update_data.items():
            column_name = key
            if key == "id": continue # Cannot update id itself

            if key == "is_read": # Legacy key
                column_name = '"isUnread"'
                value = not value
            elif key == "is_important": # schema.ts: isImportant
                 column_name = '"isImportant"'
            elif key == "is_starred": # schema.ts: isStarred
                 column_name = '"isStarred"'
            elif key == "category_id":
                column_name = '"categoryId"'
            elif key == "analysis_metadata":
                column_name = '"analysisMetadata"'
                value = json.dumps(value)
            elif key == "labels": # text[]
                column_name = '"labels"'
                if not isinstance(value, list): value = [str(value)]
            # Add other direct schema mappings here if they are simple string/bool/int
            # Example: subject, content, sender, senderEmail, confidence
            elif key in ['subject', 'content', 'sender', 'senderEmail', 'confidence', 'snippet', 'time', 'category', 'priority']:
                 column_name = f'"{key}"' # Quote camelCase keys
            else:
                logger.warning(f"update_email: Unhandled key '{key}' or key not directly updatable by internal ID method. Skipping.")
                continue

            set_clauses.append(f"{column_name} = %s")
            params.append(value)

        if not set_clauses:
            logger.info(f"No valid fields to update for email id: {email_id}")
            return await self.get_email_by_id(email_id)

        set_clauses.append('"updatedAt" = NOW()')

        query = f"""
            UPDATE emails SET {', '.join(set_clauses)}
            WHERE id = %s
        """
        params.append(email_id)

        await self._execute_query(query, tuple(params), commit=True)
        return await self.get_email_by_id(email_id)


async def get_db() -> DatabaseManager:
    """Dependency injection for database"""
    # Consider how DatabaseManager is instantiated, especially if init_database needs to be async
    # For now, assuming constructor handles necessary synchronous setup like assigning db_url
    # and actual async connections happen in methods.
    # If init_database (seeding) needs to be async, it should be called from an async context.
    # One option: db_manager = DatabaseManager(); await db_manager.initialize_async_components()
    return DatabaseManager()