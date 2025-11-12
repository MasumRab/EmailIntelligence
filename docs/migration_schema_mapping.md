# Data Migration Schema Mapping: SQLite to JSON

## Overview

This document outlines the schema mapping and data transformation process for migrating email data from SQLite database format to JSON format. The migration is performed by `src/migration_script.py` which converts data from `data/emails.sqlite3` to `data/processed/email_data.json`.

## Migration Process Summary

- **Source**: SQLite database (`data/emails.sqlite3`)
- **Target**: JSON files in `data/processed/` directory
- **Script**: `src/migration_script.py`
- **Validation**: Automatic count validation and data integrity checks

## SQLite Database Schema

### Emails Table
```sql
CREATE TABLE emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT UNIQUE NOT NULL,
    subject TEXT,
    sender TEXT,
    sender_email TEXT,
    content TEXT,
    content_html TEXT,
    category_id INTEGER,
    is_unread BOOLEAN DEFAULT 1,
    analysis_metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
```

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    count INTEGER DEFAULT 0
)
```

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## JSON Schema Mapping

### Email Data JSON Structure (`email_data.json`)

Each email record in the JSON array contains:

```json
{
  "id": 1,
  "message_id": "msg001",
  "subject": "Welcome to EmailIntelligence",
  "sender": "System Admin",
  "sender_email": "system@example.com",
  "content": "Welcome message content...",
  "content_html": "<p>Welcome message HTML...</p>",
  "category_id": 1,
  "categoryName": "Primary",
  "categoryColor": "#4CAF50",
  "is_unread": false,
  "analysis_metadata": {
    "sentiment": "positive",
    "importance": "high"
  },
  "created_at": "2025-11-13 05:29:28.073133",
  "updated_at": "2025-11-13 05:29:28.073152"
}
```

### Categories JSON Structure (`categories.json`)

```json
[
  {
    "id": 1,
    "name": "Primary",
    "description": "Default primary category",
    "color": "#4CAF50",
    "count": 0
  }
]
```

### Users JSON Structure (`users.json`)

```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "created_at": "2025-11-13 05:29:28.073000"
  }
]
```

## Field Mapping Details

### Emails Table Mapping

| SQLite Field | SQLite Type | JSON Field | JSON Type | Notes |
|-------------|-------------|------------|-----------|-------|
| `id` | INTEGER PRIMARY KEY | `id` | number | Direct mapping |
| `message_id` | TEXT UNIQUE | `message_id` | string | Direct mapping |
| `subject` | TEXT | `subject` | string | Direct mapping |
| `sender` | TEXT | `sender` | string | Direct mapping |
| `sender_email` | TEXT | `sender_email` | string | Direct mapping |
| `content` | TEXT | `content` | string | Direct mapping |
| `content_html` | TEXT | `content_html` | string | Direct mapping |
| `category_id` | INTEGER FK | `category_id` | number | Direct mapping |
| `is_unread` | BOOLEAN | `is_unread` | boolean | Converted from INTEGER (0/1) to boolean |
| `analysis_metadata` | TEXT (JSON) | `analysis_metadata` | object | Parsed from JSON string to object |
| `created_at` | TIMESTAMP | `created_at` | string | Converted to ISO format string |
| `updated_at` | TIMESTAMP | `updated_at` | string | Converted to ISO format string |
| `categories.name` | TEXT (joined) | `categoryName` | string | Joined from categories table |
| `categories.color` | TEXT (joined) | `categoryColor` | string | Joined from categories table |

### Categories Table Mapping

| SQLite Field | SQLite Type | JSON Field | JSON Type | Notes |
|-------------|-------------|------------|-----------|-------|
| `id` | INTEGER PRIMARY KEY | `id` | number | Direct mapping |
| `name` | TEXT | `name` | string | Direct mapping |
| `description` | TEXT | `description` | string | Direct mapping |
| `color` | TEXT | `color` | string | Direct mapping |
| `count` | INTEGER | `count` | number | Direct mapping |

### Users Table Mapping

| SQLite Field | SQLite Type | JSON Field | JSON Type | Notes |
|-------------|-------------|------------|-----------|-------|
| `id` | INTEGER PRIMARY KEY | `id` | number | Direct mapping |
| `username` | TEXT UNIQUE | `username` | string | Direct mapping |
| `email` | TEXT UNIQUE | `email` | string | Direct mapping |
| `created_at` | TIMESTAMP | `created_at` | string | Converted to ISO format string |

## Data Transformations

### Type Conversions
1. **Boolean Conversion**: SQLite stores booleans as integers (0/1). These are converted to JSON boolean values (`true`/`false`).
2. **JSON Parsing**: The `analysis_metadata` field in SQLite is stored as a JSON string and parsed into a JSON object in the output.
3. **Timestamp Formatting**: SQLite timestamps are converted to ISO format strings for JSON compatibility.

### Data Enrichment
1. **Category Information**: Email records are enriched with `categoryName` and `categoryColor` fields by joining with the categories table.
2. **Data Denormalization**: Foreign key relationships are preserved but denormalized in the JSON format for easier consumption.

## Migration Validation

The migration script performs automatic validation:

- **Record Count Validation**: Ensures the number of records in SQLite matches the number in JSON
- **Data Integrity Checks**: Validates that all required fields are present
- **JSON Parsing Validation**: Ensures `analysis_metadata` fields contain valid JSON

### Validation Results (Sample Run)
- **Emails**: 3 records migrated successfully
- **Categories**: 5 records migrated successfully
- **Users**: 1 record migrated successfully
- **Validation Status**: PASSED (no issues detected)

## Potential Issues and Considerations

### Data Loss Risks
1. **Large Content Fields**: Email content and HTML fields can be large, potentially impacting JSON file size and memory usage.
2. **JSON Parsing Errors**: Invalid JSON in `analysis_metadata` fields is handled gracefully but logged as warnings.
3. **Foreign Key Integrity**: While foreign key relationships are preserved conceptually, they become denormalized in JSON.

### Performance Considerations
1. **File Size**: JSON files can become large with many email records containing full content.
2. **Memory Usage**: Loading large JSON files into memory may require significant RAM.
3. **Query Performance**: JSON format requires loading entire datasets for queries vs. indexed database queries.

### Data Integrity
1. **Type Safety**: JSON is more permissive than SQLite's typed schema.
2. **Referential Integrity**: Foreign key constraints are not enforced in JSON format.
3. **Concurrent Access**: JSON files don't support concurrent read/write operations like databases.

## Recommendations

### For Production Use
1. **Backup Strategy**: Implement regular backups of both SQLite and JSON data.
2. **Monitoring**: Monitor JSON file sizes and migration performance.
3. **Validation**: Run validation checks after each migration.
4. **Versioning**: Consider implementing JSON data versioning for rollback capabilities.

### Alternative Approaches
1. **Hybrid Storage**: Keep critical data in SQLite and use JSON for derived/cached data.
2. **Incremental Migration**: Migrate data in batches rather than all at once.
3. **Compressed Storage**: Use compressed JSON formats (e.g., JSON.gz) for large datasets.

## Migration Script Usage

```bash
# Full migration
python src/migration_script.py --sqlite-db data/emails.sqlite3 --output-dir data/processed

# Validation only
python src/migration_script.py --sqlite-db data/emails.sqlite3 --output-dir data/processed --validate-only
```

## Files Generated

- `data/processed/email_data.json` - Migrated email records
- `data/processed/categories.json` - Category definitions
- `data/processed/users.json` - User accounts
- `data/processed/migration_report.json` - Migration validation report

---

*This document was generated as part of Task #15.1: Analyze Current Data Migration Process and Schemas*