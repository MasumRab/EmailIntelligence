import sys
import unittest
import queue
from unittest import mock

class TestAuditLoggerQueue(unittest.TestCase):
    def test_audit_logger_shutdown_empty_queue(self):
        sys.modules['src.core.database'] = mock.Mock()
        sys.modules['src.core.notmuch_data_source'] = mock.Mock()
        sys.modules['src.core.smart_filter_manager'] = mock.Mock()
        sys.modules['src.core'] = mock.Mock()

        import importlib.util
        spec = importlib.util.spec_from_file_location("audit_logger", "src/core/audit_logger.py")
        audit_logger = importlib.util.module_from_spec(spec)
        sys.modules["audit_logger"] = audit_logger
        spec.loader.exec_module(audit_logger)

        logger = audit_logger.AuditLogger()
        logger.shutdown()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
