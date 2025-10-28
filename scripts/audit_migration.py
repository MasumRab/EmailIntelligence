#!/usr/bin/env python3
"""
Data Migration Audit Script

This script performs data integrity verification between SQLite database
and migrated JSON files to ensure no data loss occurred during migration.

Usage:
    python scripts/audit_migration.py --sqlite-db data/emails.sqlite3 --json-dir data/processed --sample-size 100
"""

import argparse
import hashlib
import json
import logging
import random
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MigrationAuditError(Exception):
    """Exception raised when migration audit fails."""
    pass


class DataIntegrityAuditor:
    """Auditor class for verifying data integrity between SQLite and JSON."""

    def __init__(self, sqlite_db_path: str, json_dir: str, sample_size: int = 100):
        """
        Initialize the auditor.

        Args:
            sqlite_db_path: Path to the SQLite database file
            json_dir: Directory containing JSON files
            sample_size: Number of records to sample for detailed comparison
        """
        self.sqlite_db_path = sqlite_db_path
        self.json_dir = Path(json_dir)
        self.sample_size = sample_size

        # Validate inputs
        if not Path(sqlite_db_path).exists():
            raise MigrationAuditError(f"SQLite database not found: {sqlite_db_path}")
        if not self.json_dir.exists():
            raise MigrationAuditError(f"JSON directory not found: {json_dir}")

    def connect_db(self) -> sqlite3.Connection:
        """Connect to SQLite database with row factory."""
        conn = sqlite3.connect(self.sqlite_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def load_json_file(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load data from JSON file.

        Args:
            filename: Name of the JSON file

        Returns:
            List of records from the JSON file
        """
        json_path = self.json_dir / filename
        if not json_path.exists():
            raise MigrationAuditError(f"JSON file not found: {json_path}")

        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_sqlite_record_count(self, table: str) -> int:
        """
        Get record count from SQLite table.

        Args:
            table: Table name

        Returns:
            Number of records in the table
        """
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_json_record_count(self, data: List[Dict[str, Any]]) -> int:
        """
        Get record count from JSON data.

        Args:
            data: JSON data list

        Returns:
            Number of records in the JSON data
        """
        return len(data)

    def sample_sqlite_records(self, table: str, sample_size: int) -> List[sqlite3.Row]:
        """
        Sample records from SQLite table.

        Args:
            table: Table name
            sample_size: Number of records to sample

        Returns:
            List of sampled records
        """
        conn = self.connect_db()
        try:
            cursor = conn.cursor()

            # Get total count
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            total_count = cursor.fetchone()[0]

            if total_count == 0:
                return []

            # Sample records
            if sample_size >= total_count:
                # Return all records if sample size is larger than total
                cursor.execute(f'SELECT * FROM {table} ORDER BY id')
            else:
                # Random sampling using ROWID
                sample_ids = random.sample(range(1, total_count + 1), sample_size)
                placeholders = ','.join('?' * len(sample_ids))
                cursor.execute(f'SELECT * FROM {table} WHERE id IN ({placeholders})', sample_ids)

            return cursor.fetchall()
        finally:
            conn.close()

    def find_json_record_by_id(self, json_data: List[Dict[str, Any]], record_id: int) -> Optional[Dict[str, Any]]:
        """
        Find a record in JSON data by ID.

        Args:
            json_data: JSON data list
            record_id: Record ID to find

        Returns:
            Matching record or None
        """
        for record in json_data:
            if record.get('id') == record_id:
                return record
        return None

    def calculate_field_hash(self, value: Any) -> str:
        """
        Calculate hash of a field value for comparison.

        Args:
            value: Field value

        Returns:
            SHA256 hash of the value
        """
        if value is None:
            return hashlib.sha256(b'null').hexdigest()

        # Convert to string and hash
        str_value = str(value).encode('utf-8')
        return hashlib.sha256(str_value).hexdigest()

    def compare_records(self, sqlite_record: sqlite3.Row, json_record: Dict[str, Any], table: str) -> Dict[str, Any]:
        """
        Compare a SQLite record with its JSON counterpart.

        Args:
            sqlite_record: SQLite record
            json_record: JSON record
            table: Table name for context

        Returns:
            Comparison results dictionary
        """
        comparison = {
            'record_id': sqlite_record['id'],
            'table': table,
            'match': True,
            'field_differences': [],
            'missing_fields': [],
            'extra_fields': []
        }

        if table == 'emails':
            # Define critical fields for emails
            critical_fields = {
                'id': ('id', 'number'),
                'message_id': ('message_id', 'string'),
                'subject': ('subject', 'string'),
                'sender': ('sender', 'string'),
                'sender_email': ('sender_email', 'string'),
                'content': ('content', 'string'),
                'content_html': ('content_html', 'string'),
                'category_id': ('category_id', 'number'),
                'is_unread': ('is_unread', 'boolean'),
                'created_at': ('created_at', 'string'),
                'updated_at': ('updated_at', 'string')
            }

            # Check each critical field
            for sqlite_field, (json_field, expected_type) in critical_fields.items():
                sqlite_value = sqlite_record[sqlite_field]
                json_value = json_record.get(json_field)

                # Type conversions for comparison
                if sqlite_field == 'is_unread':
                    # SQLite stores as int, JSON as boolean
                    sqlite_value = bool(sqlite_value)

                # Compare values
                if sqlite_value != json_value:
                    comparison['match'] = False
                    comparison['field_differences'].append({
                        'field': json_field,
                        'sqlite_value': sqlite_value,
                        'json_value': json_value,
                        'sqlite_hash': self.calculate_field_hash(sqlite_value),
                        'json_hash': self.calculate_field_hash(json_value)
                    })

            # Check for analysis_metadata (special handling)
            sqlite_metadata = sqlite_record['analysis_metadata']
            json_metadata = json_record.get('analysis_metadata')

            if sqlite_metadata:
                try:
                    sqlite_metadata_parsed = json.loads(sqlite_metadata)
                    if sqlite_metadata_parsed != json_metadata:
                        comparison['match'] = False
                        comparison['field_differences'].append({
                            'field': 'analysis_metadata',
                            'sqlite_value': sqlite_metadata_parsed,
                            'json_value': json_metadata,
                            'sqlite_hash': self.calculate_field_hash(str(sqlite_metadata_parsed)),
                            'json_hash': self.calculate_field_hash(str(json_metadata))
                        })
                except json.JSONDecodeError:
                    comparison['match'] = False
                    comparison['field_differences'].append({
                        'field': 'analysis_metadata',
                        'sqlite_value': 'INVALID_JSON',
                        'json_value': json_metadata,
                        'error': 'SQLite analysis_metadata contains invalid JSON'
                    })

            # Check for enriched fields (categoryName, categoryColor)
            if 'categoryName' not in json_record:
                comparison['missing_fields'].append('categoryName')
            if 'categoryColor' not in json_record:
                comparison['missing_fields'].append('categoryColor')

        elif table in ['categories', 'users']:
            # For categories and users, compare all fields
            for key, value in dict(sqlite_record).items():
                json_value = json_record.get(key)
                if value != json_value:
                    comparison['match'] = False
                    comparison['field_differences'].append({
                        'field': key,
                        'sqlite_value': value,
                        'json_value': json_value,
                        'sqlite_hash': self.calculate_field_hash(value),
                        'json_hash': self.calculate_field_hash(json_value)
                    })

        return comparison

    def audit_emails_table(self) -> Dict[str, Any]:
        """
        Audit the emails table migration.

        Returns:
            Audit results for emails table
        """
        logger.info("Auditing emails table...")

        # Load JSON data
        json_emails = self.load_json_file('email_data.json')

        # Get record counts
        sqlite_count = self.get_sqlite_record_count('emails')
        json_count = self.get_json_record_count(json_emails)

        audit_results = {
            'table': 'emails',
            'sqlite_count': sqlite_count,
            'json_count': json_count,
            'count_match': sqlite_count == json_count,
            'sampled_records': [],
            'total_sampled': 0,
            'matches': 0,
            'mismatches': 0,
            'missing_records': [],
            'issues': []
        }

        # Sample records for detailed comparison
        sampled_sqlite = self.sample_sqlite_records('emails', self.sample_size)

        for sqlite_record in sampled_sqlite:
            record_id = sqlite_record['id']
            json_record = self.find_json_record_by_id(json_emails, record_id)

            if json_record is None:
                audit_results['missing_records'].append(record_id)
                audit_results['mismatches'] += 1
                continue

            comparison = self.compare_records(sqlite_record, json_record, 'emails')
            audit_results['sampled_records'].append(comparison)

            if comparison['match']:
                audit_results['matches'] += 1
            else:
                audit_results['mismatches'] += 1

        audit_results['total_sampled'] = len(sampled_sqlite)

        # Calculate percentages
        if audit_results['total_sampled'] > 0:
            audit_results['match_percentage'] = (audit_results['matches'] / audit_results['total_sampled']) * 100
        else:
            audit_results['match_percentage'] = 100.0

        logger.info(f"Emails audit: {audit_results['matches']}/{audit_results['total_sampled']} records match ({audit_results['match_percentage']:.1f}%)")
        return audit_results

    def audit_categories_table(self) -> Dict[str, Any]:
        """
        Audit the categories table migration.

        Returns:
            Audit results for categories table
        """
        logger.info("Auditing categories table...")

        # Load JSON data
        json_categories = self.load_json_file('categories.json')

        # Get record counts
        sqlite_count = self.get_sqlite_record_count('categories')
        json_count = self.get_json_record_count(json_categories)

        audit_results = {
            'table': 'categories',
            'sqlite_count': sqlite_count,
            'json_count': json_count,
            'count_match': sqlite_count == json_count,
            'sampled_records': [],
            'total_sampled': 0,
            'matches': 0,
            'mismatches': 0,
            'issues': []
        }

        # For categories, check all records (usually small table)
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories ORDER BY id')
            sqlite_records = cursor.fetchall()

            for sqlite_record in sqlite_records:
                record_id = sqlite_record['id']
                json_record = self.find_json_record_by_id(json_categories, record_id)

                if json_record is None:
                    audit_results['issues'].append(f"Category {record_id} missing in JSON")
                    audit_results['mismatches'] += 1
                    continue

                comparison = self.compare_records(sqlite_record, json_record, 'categories')
                audit_results['sampled_records'].append(comparison)

                if comparison['match']:
                    audit_results['matches'] += 1
                else:
                    audit_results['mismatches'] += 1

            audit_results['total_sampled'] = len(sqlite_records)

        finally:
            conn.close()

        if audit_results['total_sampled'] > 0:
            audit_results['match_percentage'] = (audit_results['matches'] / audit_results['total_sampled']) * 100
        else:
            audit_results['match_percentage'] = 100.0

        logger.info(f"Categories audit: {audit_results['matches']}/{audit_results['total_sampled']} records match ({audit_results['match_percentage']:.1f}%)")
        return audit_results

    def audit_users_table(self) -> Dict[str, Any]:
        """
        Audit the users table migration.

        Returns:
            Audit results for users table
        """
        logger.info("Auditing users table...")

        # Load JSON data
        json_users = self.load_json_file('users.json')

        # Get record counts
        sqlite_count = self.get_sqlite_record_count('users')
        json_count = self.get_json_record_count(json_users)

        audit_results = {
            'table': 'users',
            'sqlite_count': sqlite_count,
            'json_count': json_count,
            'count_match': sqlite_count == json_count,
            'sampled_records': [],
            'total_sampled': 0,
            'matches': 0,
            'mismatches': 0,
            'issues': []
        }

        # For users, check all records (usually small table)
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY id')
            sqlite_records = cursor.fetchall()

            for sqlite_record in sqlite_records:
                record_id = sqlite_record['id']
                json_record = self.find_json_record_by_id(json_users, record_id)

                if json_record is None:
                    audit_results['issues'].append(f"User {record_id} missing in JSON")
                    audit_results['mismatches'] += 1
                    continue

                comparison = self.compare_records(sqlite_record, json_record, 'users')
                audit_results['sampled_records'].append(comparison)

                if comparison['match']:
                    audit_results['matches'] += 1
                else:
                    audit_results['mismatches'] += 1

            audit_results['total_sampled'] = len(sqlite_records)

        finally:
            conn.close()

        if audit_results['total_sampled'] > 0:
            audit_results['match_percentage'] = (audit_results['matches'] / audit_results['total_sampled']) * 100
        else:
            audit_results['match_percentage'] = 100.0

        logger.info(f"Users audit: {audit_results['matches']}/{audit_results['total_sampled']} records match ({audit_results['match_percentage']:.1f}%)")
        return audit_results

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Run complete audit of all tables.

        Returns:
            Complete audit results
        """
        logger.info("Starting full migration audit...")

        audit_results = {
            'timestamp': datetime.now().isoformat(),
            'sqlite_database': self.sqlite_db_path,
            'json_directory': str(self.json_dir),
            'sample_size': self.sample_size,
            'tables': {},
            'summary': {
                'overall_success': True,
                'total_issues': 0,
                'critical_issues': []
            }
        }

        # Audit each table
        try:
            audit_results['tables']['emails'] = self.audit_emails_table()
            audit_results['tables']['categories'] = self.audit_categories_table()
            audit_results['tables']['users'] = self.audit_users_table()

            # Generate summary
            for table_name, table_results in audit_results['tables'].items():
                if not table_results['count_match']:
                    audit_results['summary']['overall_success'] = False
                    audit_results['summary']['critical_issues'].append(
                        f"{table_name}: Count mismatch ({table_results['sqlite_count']} vs {table_results['json_count']})"
                    )

                audit_results['summary']['total_issues'] += table_results['mismatches']

                if table_results['match_percentage'] < 95.0:
                    audit_results['summary']['critical_issues'].append(
                        f"{table_name}: Low match percentage ({table_results['match_percentage']:.1f}%)"
                    )

            logger.info(f"Audit completed. Overall success: {audit_results['summary']['overall_success']}")

        except Exception as e:
            logger.error(f"Audit failed: {e}")
            audit_results['summary']['overall_success'] = False
            audit_results['summary']['critical_issues'].append(f"Audit failed: {str(e)}")

        return audit_results

    def save_audit_report(self, audit_results: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Save audit results to JSON file.

        Args:
            audit_results: Audit results dictionary
            output_path: Optional output path

        Returns:
            Path to saved report
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"migration_audit_report_{timestamp}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_results, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Audit report saved to: {output_path}")
        return output_path


def main():
    """Main entry point for the audit script."""
    parser = argparse.ArgumentParser(description='Audit data migration integrity between SQLite and JSON')
    parser.add_argument('--sqlite-db', required=True, help='Path to SQLite database file')
    parser.add_argument('--json-dir', required=True, help='Directory containing JSON files')
    parser.add_argument('--sample-size', type=int, default=100, help='Number of records to sample for detailed comparison')
    parser.add_argument('--output', help='Output path for audit report (optional)')

    args = parser.parse_args()

    try:
        auditor = DataIntegrityAuditor(args.sqlite_db, args.json_dir, args.sample_size)
        audit_results = auditor.run_full_audit()
        report_path = auditor.save_audit_report(audit_results, args.output)

        # Print summary
        print("\n=== Migration Audit Summary ===")
        print(f"Overall Success: {audit_results['summary']['overall_success']}")
        print(f"Total Issues: {audit_results['summary']['total_issues']}")
        print(f"Report saved to: {report_path}")

        if audit_results['summary']['critical_issues']:
            print("\nCritical Issues:")
            for issue in audit_results['summary']['critical_issues']:
                print(f"  - {issue}")

        # Exit with appropriate code
        exit(0 if audit_results['summary']['overall_success'] else 1)

    except MigrationAuditError as e:
        logger.error(f"Audit error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)


if __name__ == '__main__':
    main()