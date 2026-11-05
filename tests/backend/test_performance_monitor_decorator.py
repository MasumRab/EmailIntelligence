import asyncio
import unittest
from unittest.mock import patch

# Import the decorator and monitor from the target file
from src.backend.python_backend.performance_monitor import (
    log_performance,
)


class TestPerformanceMonitorDecorator(unittest.TestCase):
    def setUp(self):
        # Clear the mock before each test if needed
        pass

    def test_bare_decorator_sync(self):
        """Test @log_performance without arguments on a sync function."""

        @log_performance
        def sample_sync_func(a, b):
            return a + b

        # Test __name__ preservation
        self.assertEqual(sample_sync_func.__name__, "sample_sync_func")

        # Test functionality and return value
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = sample_sync_func(2, 3)
            self.assertEqual(result, 5)
            # Decorator should append to log file
            mock_file.assert_called_once()

            # Since operation_or_func is None internally handled by the first branch,
            # operation should be the function name
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "sample_sync_func"', written)

    def test_bare_decorator_async(self):
        """Test @log_performance without arguments on an async function."""

        @log_performance
        async def sample_async_func(a, b):
            return a * b

        self.assertEqual(sample_async_func.__name__, "sample_async_func")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = asyncio.run(sample_async_func(4, 5))
            self.assertEqual(result, 20)
            mock_file.assert_called_once()
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "sample_async_func"', written)

    def test_positional_string_decorator_sync(self):
        """Test @log_performance("custom_name") on a sync function."""

        @log_performance("custom_sync_op")
        def another_sync_func(x):
            return x * 2

        self.assertEqual(another_sync_func.__name__, "another_sync_func")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = another_sync_func(10)
            self.assertEqual(result, 20)
            mock_file.assert_called_once()
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "custom_sync_op"', written)

    def test_positional_string_decorator_async(self):
        """Test @log_performance("custom_name") on an async function."""

        @log_performance("custom_async_op")
        async def another_async_func(x):
            return x + 10

        self.assertEqual(another_async_func.__name__, "another_async_func")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = asyncio.run(another_async_func(5))
            self.assertEqual(result, 15)
            mock_file.assert_called_once()
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "custom_async_op"', written)

    def test_keyword_decorator_sync(self):
        """Test @log_performance(operation="custom_name") on a sync function."""

        @log_performance(operation="keyword_sync_op")
        def keyword_sync_func(text):
            return text.upper()

        self.assertEqual(keyword_sync_func.__name__, "keyword_sync_func")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = keyword_sync_func("hello")
            self.assertEqual(result, "HELLO")
            mock_file.assert_called_once()
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "keyword_sync_op"', written)

    def test_keyword_decorator_async(self):
        """Test @log_performance(operation="custom_name") on an async function."""

        @log_performance(operation="keyword_async_op")
        async def keyword_async_func(text):
            return text.lower()

        self.assertEqual(keyword_async_func.__name__, "keyword_async_func")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = asyncio.run(keyword_async_func("WORLD"))
            self.assertEqual(result, "world")
            mock_file.assert_called_once()
            written = mock_file().write.call_args[0][0]
            self.assertIn('"operation": "keyword_async_op"', written)

    def test_decorator_preserves_exceptions_sync(self):
        """Test that the decorator preserves exceptions raised by the wrapped function."""

        @log_performance("failing_op")
        def failing_sync_func():
            raise ValueError("Test error")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            with self.assertRaises(ValueError):
                failing_sync_func()
            # The current implementation of log_performance in performance_monitor.py
            # does not capture/log exceptions, it just lets them propagate natively
            # so the mock file write is not expected to be called upon exception.
            mock_file.assert_not_called()

    def test_decorator_preserves_exceptions_async(self):
        """Test that the decorator preserves exceptions raised by the wrapped async function."""

        @log_performance(operation="async_failing_op")
        async def failing_async_func():
            raise RuntimeError("Async test error")

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            with self.assertRaises(RuntimeError):
                asyncio.run(failing_async_func())
            # Same here, exceptions propagate directly
            mock_file.assert_not_called()

    def test_import_database_does_not_raise(self):
        """
        Verify that importing the database module does not raise an UnboundLocalError
        or any other exception due to the @log_performance decorator usage.

        The import is done here, at test time, so a decorator that blows up while
        the module is being defined fails this test instead of breaking collection
        for the whole file.
        """
        import importlib

        importlib.import_module("src.backend.python_backend.json_database")

if __name__ == '__main__':
    unittest.main()
