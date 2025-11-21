"""
Tests for the Tools Dashboard API routes.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.backend.python_backend.tools_dashboard_routes import (
    AVAILABLE_TOOLS,
    get_tool_categories,
    run_script_safely,
    check_tool_health
)


class TestToolsDashboard:
    """Test cases for tools dashboard functionality."""

    def test_get_tool_categories(self):
        """Test that tool categories are extracted correctly."""
        categories = get_tool_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert "Context Control" in categories
        assert "Monitoring" in categories

    def test_available_tools_structure(self):
        """Test that available tools have the correct structure."""
        for tool in AVAILABLE_TOOLS:
            required_fields = ["name", "category", "description", "script_path", "health_check"]
            for field in required_fields:
                assert field in tool, f"Tool {tool.get('name', 'unknown')} missing field: {field}"

    @pytest.mark.asyncio
    async def test_run_script_safely_success(self):
        """Test successful script execution."""
        # Mock subprocess for successful execution
        with patch('asyncio.create_subprocess_exec') as mock_subprocess:
            mock_process = MagicMock()
            mock_process.communicate.return_value = (b"output", b"")
            mock_process.returncode = 0
            mock_subprocess.return_value = mock_process

            result = await run_script_safely("test_script.py")

            assert result["status"] == "success"
            assert result["output"] == "output"
            assert result["return_code"] == 0
            assert "execution_time" in result

    @pytest.mark.asyncio
    async def test_run_script_safely_timeout(self):
        """Test script execution timeout."""
        with patch('asyncio.create_subprocess_exec') as mock_subprocess:
            mock_process = MagicMock()
            mock_subprocess.return_value = mock_process

            # Simulate timeout
            with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError):
                result = await run_script_safely("test_script.py")

                assert result["status"] == "timeout"
                assert "timed out" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_run_script_safely_not_found(self):
        """Test script execution when file doesn't exist."""
        result = await run_script_safely("nonexistent_script.py")

        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_check_tool_health_healthy(self):
        """Test health check for a healthy tool."""
        # Mock a healthy Python script
        tool_config = {
            "name": "test_tool",
            "script_path": "scripts/test_tool.py",
            "category": "Test",
            "description": "Test tool",
            "health_check": "test"
        }

        with patch('builtins.__import__') as mock_import:
            mock_import.return_value = MagicMock()  # Mock successful import
            result = await check_tool_health(tool_config)
            assert result == "healthy"

    @pytest.mark.asyncio
    async def test_check_tool_health_import_error(self):
        """Test health check for a tool with import errors."""
        tool_config = {
            "name": "test_tool",
            "script_path": "scripts/test_tool.py",
            "category": "Test",
            "description": "Test tool",
            "health_check": "test"
        }

        with patch('builtins.__import__', side_effect=ImportError("Module not found")):
            result = await check_tool_health(tool_config)
            assert result == "import_error"

    def test_context_control_tools_included(self):
        """Test that context control tools are properly configured."""
        context_tools = [tool for tool in AVAILABLE_TOOLS if tool["category"] == "Context Control"]
        assert len(context_tools) > 0

        # Check that context-control script is included
        context_control = next((tool for tool in context_tools if tool["name"] == "context-control"), None)
        assert context_control is not None
        assert "context-control" in context_control["script_path"]

    def test_monitoring_tools_included(self):
        """Test that monitoring tools are properly configured."""
        monitoring_tools = [tool for tool in AVAILABLE_TOOLS if tool["category"] == "Monitoring"]
        assert len(monitoring_tools) > 0

        # Check that agent performance monitor is included
        perf_monitor = next((tool for tool in monitoring_tools if tool["name"] == "agent_performance_monitor"), None)
        assert perf_monitor is not None
        assert "agent_performance_monitor.py" in perf_monitor["script_path"]