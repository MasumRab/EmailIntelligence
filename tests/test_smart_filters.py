import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta

# Adjust path to import module from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.python_nlp.smart_filters import SmartFilterManager, EmailFilter, FilterPerformance

class TestSmartFilterManager(unittest.TestCase):

    def setUp(self):
        """Set up for test methods using an in-memory SQLite database."""
        self.db_path = ":memory:" # Use in-memory database for tests
        self.manager = SmartFilterManager(db_path=self.db_path)
        # _init_filter_db is called in SmartFilterManager constructor

        self.sample_emails = [
            {
                'id': 'email1',
                'senderEmail': 'user@company.com',
                'subject': 'Urgent: Project Alpha Deadline',
                'content': 'The deadline for Project Alpha is approaching. All team members must submit their reports by Friday. This is an important project.',
                'category': 'work_business',
                'isImportant': True,
                'expected_filter_match': True # For evaluate_filter_performance tests
            },
            {
                'id': 'email2',
                'senderEmail': 'newsletter@example.org',
                'subject': 'Weekly Newsletter - Updates and Offers',
                'content': 'Check out our latest updates and special offers in this week\'s newsletter. Unsubscribe here.',
                'category': 'promotions',
                'expected_filter_match': False
            },
            {
                'id': 'email3',
                'senderEmail': 'billing@financeprovider.com',
                'subject': 'Your Monthly Invoice INV-001 is ready',
                'content': 'Please find attached your monthly invoice. Amount due: $50.00',
                'category': 'finance_banking',
                'attachment_types': ['pdf'],
                'expected_filter_match': True
            }
        ]

    def tearDown(self):
        """Clean up after tests (in-memory DB is automatically discarded)."""
        pass # No explicit cleanup needed for in-memory DB

    def test_db_initialization(self):
        """Test that database tables are created."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if tables exist
        tables = ["email_filters", "filter_performance", "google_scripts"]
        for table_name in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            self.assertIsNotNone(cursor.fetchone(), f"Table {table_name} was not created.")
        conn.close()

    def test_save_and_load_filter(self):
        """Test saving and loading a single filter."""
        filter_data = EmailFilter(
            filter_id="test_filter_001",
            name="Test Filter",
            description="A filter for testing",
            criteria={"subject_keywords": ["test", "example"]},
            actions={"add_label": "Tested"},
            priority=5,
            effectiveness_score=0.75,
            created_date=datetime.now(),
            last_used=datetime.now(),
            usage_count=10,
            false_positive_rate=0.1,
            performance_metrics={"f1": 0.75}
        )
        self.manager._save_filter(filter_data)

        loaded_filter = self.manager._load_filter("test_filter_001")
        self.assertIsNotNone(loaded_filter)
        self.assertEqual(loaded_filter.name, "Test Filter")
        self.assertEqual(loaded_filter.criteria["subject_keywords"], ["test", "example"])

    def test_load_all_filters(self):
        """Test loading all filters (initially empty, then after adding some)."""
        filters = self.manager._load_all_filters()
        self.assertEqual(len(filters), 0)

        filter1_data = EmailFilter("f1", "Filter 1", "", {}, {}, 1, 0, datetime.now(), datetime.now(), 0, 0, {})
        filter2_data = EmailFilter("f2", "Filter 2", "", {}, {}, 1, 0, datetime.now(), datetime.now(), 0, 0, {})
        self.manager._save_filter(filter1_data)
        self.manager._save_filter(filter2_data)

        filters = self.manager._load_all_filters()
        self.assertEqual(len(filters), 2)

        # Test disabling a filter
        self.manager._disable_filter("f1")
        active_filters = self.manager._load_all_filters() # _load_all_filters (as per previous refactor) loads active only
        # This needs to be aligned. If _load_all_filters means "all regardless of status" (as per its last refactor),
        # then this test needs to change. If it means "all active", then it's fine.
        # The previous refactor made _load_all_filters load ALL filters.
        # The pruning logic then uses _is_filter_active_in_db.
        # So, let's rename _load_all_filters to _load_all_filters_from_db_regardless_of_status
        # and create a new _load_active_filters for clarity.
        # For now, assuming _load_all_filters fetches everything and test logic should reflect this.

        all_db_filters = self.manager._load_all_filters() # This loads all, active or not
        self.assertEqual(len(all_db_filters), 2) # Still 2 in DB

        is_f1_active = self.manager._is_filter_active_in_db("f1")
        self.assertFalse(is_f1_active)


    def test_apply_filter_to_email_subject_keyword(self):
        """Test _apply_filter_to_email for subject keyword matching."""
        filter_criteria = {"subject_keywords": ["urgent", "report"], "keyword_operator": "AND"}
        filter_obj = EmailFilter("test_subj", "Subject Test", "", filter_criteria, {}, 1,0,datetime.now(),datetime.now(),0,0,{})

        email_match = {'subject': 'Urgent project report needed'}
        self.assertTrue(self.manager._apply_filter_to_email(filter_obj, email_match))

        email_no_match1 = {'subject': 'Project report needed'} # Missing urgent
        self.assertFalse(self.manager._apply_filter_to_email(filter_obj, email_no_match1))

        filter_criteria_or = {"subject_keywords": ["urgent", "report"], "keyword_operator": "OR", "min_keyword_matches": 1}
        filter_obj_or = EmailFilter("test_subj_or", "Subject Test OR", "", filter_criteria_or, {}, 1,0,datetime.now(),datetime.now(),0,0,{})
        self.assertTrue(self.manager._apply_filter_to_email(filter_obj_or, email_no_match1))


    def test_apply_filter_to_email_from_pattern(self):
        """Test _apply_filter_to_email for sender pattern matching."""
        filter_criteria = {"from_patterns": [r".*@company\.com"]}
        filter_obj = EmailFilter("test_from", "From Test", "", filter_criteria, {}, 1,0,datetime.now(),datetime.now(),0,0,{})

        email_match = {'senderEmail': 'employee@company.com'}
        self.assertTrue(self.manager._apply_filter_to_email(filter_obj, email_match))

        email_no_match = {'senderEmail': 'user@external.com'}
        self.assertFalse(self.manager._apply_filter_to_email(filter_obj, email_no_match))

    def test_apply_filter_to_email_exclusion(self):
        """Test _apply_filter_to_email for exclusion patterns."""
        filter_criteria = {"subject_keywords": ["update"], "exclude_patterns": ["newsletter", r"automated message"]}
        filter_obj = EmailFilter("test_excl", "Exclusion Test", "", filter_criteria, {}, 1,0,datetime.now(),datetime.now(),0,0,{})

        email_match = {'subject': 'Project update', 'content': 'Here is the latest status.'}
        self.assertTrue(self.manager._apply_filter_to_email(filter_obj, email_match))

        email_no_match_subject = {'subject': 'Newsletter update'} # Excluded by subject
        self.assertFalse(self.manager._apply_filter_to_email(filter_obj, email_no_match_subject))

        email_no_match_content = {'subject': 'System update', 'content': 'This is an automated message.'} # Excluded by content
        self.assertFalse(self.manager._apply_filter_to_email(filter_obj, email_no_match_content))


    def test_create_intelligent_filters(self):
        """Test creation of intelligent filters from email samples."""
        # This is a high-level test, ensure it runs and creates some filters
        # More detailed tests for _create_filter_from_template, _create_custom_filters can be added

        # Mock _should_create_filter to True for specific templates to ensure they are created
        with patch.object(self.manager, '_should_create_filter', return_value=True):
            created_filters = self.manager.create_intelligent_filters(self.sample_emails)

        self.assertGreater(len(created_filters), 0)
        # Check if filters were saved by trying to load one
        if created_filters:
            a_filter_id = created_filters[0].filter_id
            loaded = self.manager._load_filter(a_filter_id) # _load_filter loads regardless of active status
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.filter_id, a_filter_id)

    def test_evaluate_filter_performance(self):
        """Test filter performance evaluation."""
        filter_data = EmailFilter(
            filter_id="perf_test_001", name="Perf Test Filter", description="",
            criteria={"subject_keywords": ["urgent"]}, # Simple criteria for testing
            actions={}, priority=1, effectiveness_score=0, created_date=datetime.now(),
            last_used=datetime.now(), usage_count=0, false_positive_rate=0, performance_metrics={}
        )
        self.manager._save_filter(filter_data)

        # Sample emails for performance testing (defined in setUp, but can be specific here)
        # Email1: subject "Urgent: Project Alpha Deadline", expected_filter_match = True
        # Email2: subject "Weekly Newsletter...", expected_filter_match = False

        performance = self.manager.evaluate_filter_performance("perf_test_001", self.sample_emails)

        self.assertEqual(performance.filter_id, "perf_test_001")
        self.assertEqual(performance.emails_processed, len(self.sample_emails))
        # Based on sample_emails and criteria {"subject_keywords": ["urgent"]}
        # Email1: Predicted=True, Actual=True (TP=1)
        # Email2: Predicted=False, Actual=False (TN=1)
        # Email3: Predicted=False, Actual=True (FN=1) -> if "urgent" is not in subject.
        # Let's adjust sample_emails for clearer TP/FP/FN for this specific filter.

        test_emails_for_perf = [
            {'subject': 'urgent call', 'expected_filter_match': True}, # TP
            {'subject': 'another subject', 'expected_filter_match': False}, # TN
            {'subject': 'urgent meeting', 'expected_filter_match': True}, # TP
            {'subject': 'not urgent but important', 'expected_filter_match': False}, # TN (Corrected, this should be TN)
            {'subject': 'something else', 'expected_filter_match': True}, # FN (Predicted False, Actual True)
        ]

        performance = self.manager.evaluate_filter_performance("perf_test_001", test_emails_for_perf)

        self.assertEqual(performance.true_positives, 2) # "urgent call", "urgent meeting"
        self.assertEqual(performance.false_positives, 0)
        self.assertEqual(performance.false_negatives, 1) # "something else"
        # TN = 2 ("another subject", "not urgent but important")

        # Accuracy = (TP+TN)/Total = (2+2)/5 = 4/5 = 0.8
        self.assertAlmostEqual(performance.accuracy, 0.8)
        # Precision = TP / (TP+FP) = 2 / (2+0) = 1.0
        self.assertAlmostEqual(performance.precision, 1.0)
        # Recall = TP / (TP+FN) = 2 / (2+1) = 2/3
        self.assertAlmostEqual(performance.recall, 2/3)
        # F1 = 2 * (Prec*Rec) / (Prec+Rec) = 2 * (1 * 2/3) / (1 + 2/3) = (4/3) / (5/3) = 4/5 = 0.8
        self.assertAlmostEqual(performance.f1_score, 0.8)

        loaded_filter = self.manager._load_filter("perf_test_001")
        self.assertAlmostEqual(loaded_filter.effectiveness_score, 0.8) # F1 score
        # FP Rate = FP / Total = 0 / 5 = 0
        self.assertAlmostEqual(loaded_filter.false_positive_rate, 0)


    def test_prune_ineffective_filters_low_effectiveness(self):
        """Test that a filter with low effectiveness is pruned."""
        fid = "prune_eff_test"
        filter_data = EmailFilter(
            fid, "LowEff", "", {"subject_keywords":["test"]}, {}, 1,
            effectiveness_score=0.1, # Below threshold
            created_date=datetime.now() - timedelta(days=100),
            last_used=datetime.now() - timedelta(days=100),
            usage_count=100, false_positive_rate=0.01, performance_metrics={}
        )
        self.manager._save_filter(filter_data)
        self.assertTrue(self.manager._is_filter_active_in_db(fid)) # Ensure it's active

        results = self.manager.prune_ineffective_filters()

        self.assertEqual(len(results["pruned_filters"]), 1)
        self.assertEqual(results["pruned_filters"][0]["filter_id"], fid)
        # Verify it's deleted from DB (or marked inactive if soft delete was chosen)
        # _delete_filter in current code does hard delete.
        self.assertIsNone(self.manager._load_filter(fid))

    def test_prune_ineffective_filters_high_fp_rate(self):
        """Test that a filter with high false positive rate is pruned."""
        fid = "prune_fp_test"
        filter_data = EmailFilter(
            fid, "HighFP", "", {}, {}, 1,
            effectiveness_score=0.8, false_positive_rate=0.5, # High FP
            created_date=datetime.now(), last_used=datetime.now(),
            usage_count=100, performance_metrics={}
        )
        self.manager._save_filter(filter_data)
        self.assertTrue(self.manager._is_filter_active_in_db(fid))

        results = self.manager.prune_ineffective_filters()
        self.assertEqual(len(results["pruned_filters"]), 1)
        self.assertEqual(results["pruned_filters"][0]["filter_id"], fid)

    def test_prune_ineffective_filters_disable_unused(self):
        """Test that an old, underused filter is disabled."""
        fid = "disable_unused_test"
        filter_data = EmailFilter(
            fid, "UnusedOld", "", {}, {}, 1,
            effectiveness_score=0.9, false_positive_rate=0.01,
            created_date=datetime.now() - timedelta(days=100), # Old
            last_used=datetime.now() - timedelta(days=100), # Not used recently
            usage_count=5, performance_metrics={} # Low usage
        )
        self.manager._save_filter(filter_data)
        self.assertTrue(self.manager._is_filter_active_in_db(fid))

        results = self.manager.prune_ineffective_filters()
        self.assertEqual(len(results["disabled_filters"]), 1)
        self.assertEqual(results["disabled_filters"][0]["filter_id"], fid)
        self.assertFalse(self.manager._is_filter_active_in_db(fid)) # Check it's marked inactive
        self.assertIsNotNone(self.manager._load_filter(fid)) # Still exists


    @patch('server.python_nlp.smart_filters.SmartFilterManager._get_filter_performance')
    def test_prune_ineffective_filters_optimize(self, mock_get_performance):
        """Test that a filter needing optimization is marked for update."""
        fid = "optimize_test"
        # Mock performance data that suggests optimization
        mock_perf_data = FilterPerformance(fid, 0.5, 0.5, 0.5, 0.5, 10, 100, 5, 5, 5) # Low accuracy/f1
        mock_get_performance.return_value = mock_perf_data

        filter_data = EmailFilter(
            fid, "NeedsOptim", "", {"subject_keywords":["original"]}, {}, 1,
            effectiveness_score=0.8, # Good enough not to be pruned/disabled by this alone
            false_positive_rate=0.05,
            created_date=datetime.now(), last_used=datetime.now(),
            usage_count=100, performance_metrics={}
        )
        self.manager._save_filter(filter_data)
        self.assertTrue(self.manager._is_filter_active_in_db(fid))

        # Mock _optimize_filter to track call and simulate change
        with patch.object(self.manager, '_optimize_filter', side_effect=lambda f: f) as mock_optimizer:
            results = self.manager.prune_ineffective_filters()

        self.assertEqual(len(results["updated_filters"]), 1)
        self.assertEqual(results["updated_filters"][0]["filter_id"], fid)
        mock_optimizer.assert_called_once()
        # Check if _update_filter was implicitly called by _save_filter within the flow
        # The _optimize_filter is called, then _update_filter.
        # The filter should still be active and exist
        self.assertTrue(self.manager._is_filter_active_in_db(fid))


if __name__ == '__main__':
    unittest.main()
