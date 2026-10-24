import pytest
from src.core.audit_logger import AuditLogger

def test_audit_logger_empty_queue_exception_handling():
    logger = AuditLogger()
    
    # We want to test shutdown() handles queue.Empty gracefully instead of raising.
    # Stop processing thread
    logger._stop_event.set()
    logger._processing_thread.join()
    
    # Mock empty() so it enters the while loop but gets nothing.
    logger._event_queue.empty = lambda: False
    
    try:
        logger.shutdown()
        # Should reach here without raising queue.Empty
        assert True
    except Exception as e:
        pytest.fail(f"shutdown() raised an exception: {e}")

