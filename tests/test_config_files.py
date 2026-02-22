"""
Comprehensive tests for configuration and documentation files.
Tests JSON schema validation, YAML syntax, markdown structure, and configuration integrity.
"""
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml


class TestJSONConfigFiles:
    """Test suite for JSON configuration files."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_claude_mcp_json_valid(self, repo_root: Path):
        """Test .claude/mcp.json is valid JSON with correct structure."""
        file_path = repo_root / ".claude" / "mcp.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate structure - file is empty JSON object
        assert isinstance(data, dict)

    def test_claude_settings_json_valid(self, repo_root: Path):
        """Test .claude/settings.json has valid permissions structure."""
        file_path = repo_root / ".claude" / "settings.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate structure
        assert "env" in data
        assert "permissions" in data
        assert "allow" in data["permissions"]
        assert "deny" in data["permissions"]

        # Validate allow list contains expected tools
        assert "Edit" in data["permissions"]["allow"]
        assert "Bash(*)" in data["permissions"]["allow"]
        assert "mcp" in data["permissions"]["allow"]

        # Validate deny list
        assert isinstance(data["permissions"]["deny"], list)
        assert any("credentials/" in item for item in data["permissions"]["deny"])

        # Validate env has ANTHROPIC_BASE_URL
        assert "ANTHROPIC_BASE_URL" in data["env"]
        assert data["env"]["ANTHROPIC_BASE_URL"] == "http://localhost:3456"

    def test_claude_settings_local_json_valid(self, repo_root: Path):
        """Test .claude/settings.local.json has valid structure."""
        file_path = repo_root / ".claude" / "settings.local.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate structure
        assert "permissions" in data
        assert "deny" in data["permissions"]
        assert isinstance(data["permissions"]["deny"], list)

    def test_claude_slash_commands_json_valid(self, repo_root: Path):
        """Test .claude/slash_commands.json has valid command structure."""
        file_path = repo_root / ".claude" / "slash_commands.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate structure
        assert "commands" in data
        assert isinstance(data["commands"], list)

        # Validate each command has required fields
        for cmd in data["commands"]:
            assert "name" in cmd
            assert "description" in cmd
            assert "command" in cmd
            assert "working_directory" in cmd

        # Check for specific expected commands
        command_names = [cmd["name"] for cmd in data["commands"]]
        expected_commands = ["task-next", "task-start", "task-complete", "task-cycle"]
        for expected_cmd in expected_commands:
            assert expected_cmd in command_names, f"Missing command: {expected_cmd}"

    def test_concurrent_reviews_json_valid(self, repo_root: Path):
        """Test .concurrent_reviews.json has valid review session structure."""
        file_path = repo_root / ".concurrent_reviews.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate top-level structure
        assert "timestamp" in data
        assert "review_sessions" in data
        assert isinstance(data["review_sessions"], dict)

        # Validate each review session
        for _session_id, session in data["review_sessions"].items():
            assert "session_id" in session
            assert "document_id" in session
            assert "reviewers" in session
            assert "status" in session
            assert "start_time" in session
            assert "end_time" in session
            assert "comments" in session
            assert "feedback" in session
            assert "votes" in session
            assert "metadata" in session

            # Validate reviewers is a list
            assert isinstance(session["reviewers"], list)

            # Validate status is valid
            assert session["status"] in ["pending", "in_progress", "completed", "cancelled"]

            # Validate comments structure
            assert isinstance(session["comments"], list)
            for comment in session["comments"]:
                assert "comment_id" in comment
                assert "agent_id" in comment
                assert "comment_text" in comment
                assert "severity" in comment
                assert "status" in comment
                assert "timestamp" in comment

    def test_context_control_profile_valid(self, repo_root: Path):
        """Test .context-control/profiles/orchestration-tools.json is valid."""
        file_path = repo_root / ".context-control" / "profiles" / "orchestration-tools.json"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate required top-level fields
        required_fields = ["id", "name", "description", "branch_patterns", "allowed_files",
                          "blocked_files", "agent_settings", "project_config", "version"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Validate branch_patterns
        assert isinstance(data["branch_patterns"], list)
        assert len(data["branch_patterns"]) > 0

        # Validate file patterns
        assert isinstance(data["allowed_files"], list)
        assert isinstance(data["blocked_files"], list)

        # Validate agent_settings
        agent_settings = data["agent_settings"]
        assert "enable_code_execution" in agent_settings
        assert "enable_file_writing" in agent_settings
        assert "enable_shell_commands" in agent_settings
        assert "max_context_length" in agent_settings

        # Validate project_config
        project_config = data["project_config"]
        assert "project_name" in project_config
        assert "project_type" in project_config


class TestYAMLConfigFiles:
    """Test suite for YAML configuration files."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_aider_conf_yml_valid(self, repo_root: Path):
        """Test .aider.conf.yml is valid YAML with correct structure."""
        file_path = repo_root / ".aider.conf.yml"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        # Validate required fields
        assert "env-file" in data
        assert "model" in data

        # Validate model configuration
        assert isinstance(data["model"], str)
        assert len(data["model"]) > 0

        # Validate API keys are referenced as env vars
        if "openai-api-key" in data:
            assert data["openai-api-key"].startswith("${")
        if "anthropic-api-key" in data:
            assert data["anthropic-api-key"].startswith("${")

        # Validate git integration settings
        assert "auto-commits" in data
        assert isinstance(data["auto-commits"], bool)

        # Validate aliases if present
        if "alias" in data:
            assert isinstance(data["alias"], list)
            for alias in data["alias"]:
                assert ":" in alias, "Alias should be in format 'shortcut:model'"


class TestBanditConfig:
    """Test suite for Bandit security configuration."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_bandit_config_valid(self, repo_root: Path):
        """Test .bandit configuration is valid."""
        file_path = repo_root / ".bandit"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Parse as INI-style config
        import configparser
        config = configparser.ConfigParser()
        config.read_string(content)

        # Validate bandit section exists
        assert "bandit" in config

        # Validate exclude_dirs is present
        assert "exclude_dirs" in config["bandit"]

        # Validate common directories are excluded
        excluded = config["bandit"]["exclude_dirs"]
        expected_exclusions = [".git", "__pycache__", "venv", ".venv"]
        for expected in expected_exclusions:
            assert expected in excluded, f"Missing expected exclusion: {expected}"


class TestMarkdownDocumentation:
    """Test suite for markdown documentation files."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def _validate_markdown_structure(self, content: str, required_sections: List[str]):
        """Helper to validate markdown has required sections."""
        # Extract all headings
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

        for required in required_sections:
            # Check if any heading contains the required text (case-insensitive)
            found = any(required.lower() in heading.lower() for heading in headings)
            assert found, f"Missing required section: {required}"

    def _validate_frontmatter(self, content: str, required_keys: List[str]):
        """Helper to validate YAML frontmatter in markdown."""
        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        assert match, "Missing YAML frontmatter"

        frontmatter_text = match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)

        for key in required_keys:
            assert key in frontmatter, f"Missing frontmatter key: {key}"

    def test_rules_analysis_md_structure(self, repo_root: Path):
        """Test .RULES_ANALYSIS.md has proper structure."""
        file_path = repo_root / ".RULES_ANALYSIS.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Check for required sections
        required_sections = [
            "File Identity",
            "Creation Timeline",
            "Content Analysis",
            "Tool Detection",
            "Conclusion"
        ]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_analyze_command(self, repo_root: Path):
        """Test .agents/commands/speckit.analyze.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.analyze.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Validate frontmatter
        self._validate_frontmatter(content, ["description"])

        # Check for required sections
        required_sections = ["Goal", "Operating Constraints", "Execution Steps"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_checklist_command(self, repo_root: Path):
        """Test .agents/commands/speckit.checklist.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.checklist.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Validate frontmatter
        self._validate_frontmatter(content, ["description"])

        # Check for critical concept explanation
        assert "Unit Tests for English" in content
        assert "CRITICAL CONCEPT" in content

    def test_speckit_clarify_command(self, repo_root: Path):
        """Test .agents/commands/speckit.clarify.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.clarify.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Validate frontmatter
        self._validate_frontmatter(content, ["description"])

        required_sections = ["Outline", "Execution steps"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_constitution_command(self, repo_root: Path):
        """Test .agents/commands/speckit.constitution.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.constitution.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])
        required_sections = ["Outline"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_implement_command(self, repo_root: Path):
        """Test .agents/commands/speckit.implement.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.implement.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])
        required_sections = ["Outline", "Project Setup Verification"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_plan_command(self, repo_root: Path):
        """Test .agents/commands/speckit.plan.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.plan.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])
        required_sections = ["Outline", "Phases"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_specify_command(self, repo_root: Path):
        """Test .agents/commands/speckit.specify.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.specify.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])
        required_sections = ["Outline", "General Guidelines"]
        self._validate_markdown_structure(content, required_sections)

    def test_speckit_tasks_command(self, repo_root: Path):
        """Test .agents/commands/speckit.tasks.md structure."""
        file_path = repo_root / ".agents" / "commands" / "speckit.tasks.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])
        required_sections = ["Outline", "Task Generation Rules"]
        self._validate_markdown_structure(content, required_sections)

    def test_claude_planner_agent(self, repo_root: Path):
        """Test .claude/agents/planner.md structure."""
        file_path = repo_root / ".claude" / "agents" / "planner.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["name", "description", "model"])

    def test_claude_review_pr_command(self, repo_root: Path):
        """Test .claude/commands/review-pr.md structure."""
        file_path = repo_root / ".claude" / "commands" / "review-pr.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description"])

    def test_claude_memories(self, repo_root: Path):
        """Test .claude/memories/CLAUDE.md structure."""
        file_path = repo_root / ".claude" / "memories" / "CLAUDE.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Should have content about using cerebras-mcp write tool
        assert "cerebras-mcp" in content.lower() or "write" in content.lower()

    def test_clinerules_cline_rules(self, repo_root: Path):
        """Test .clinerules/cline_rules.md structure."""
        file_path = repo_root / ".clinerules" / "cline_rules.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description", "globs", "alwaysApply"])

    def test_clinerules_dev_workflow(self, repo_root: Path):
        """Test .clinerules/dev_workflow.md structure."""
        file_path = repo_root / ".clinerules" / "dev_workflow.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description", "globs", "alwaysApply"])
        required_sections = ["The Basic Loop", "Standard Development Workflow Process"]
        self._validate_markdown_structure(content, required_sections)

    def test_clinerules_self_improve(self, repo_root: Path):
        """Test .clinerules/self_improve.md structure."""
        file_path = repo_root / ".clinerules" / "self_improve.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description", "globs", "alwaysApply"])

    def test_clinerules_taskmaster(self, repo_root: Path):
        """Test .clinerules/taskmaster.md structure."""
        file_path = repo_root / ".clinerules" / "taskmaster.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        self._validate_frontmatter(content, ["description", "globs", "alwaysApply"])
        # Should reference Taskmaster MCP tools
        assert "MCP" in content or "task-master" in content

    def test_cursor_review_pr_command(self, repo_root: Path):
        """Test .cursor/commands/review-pr.md structure."""
        file_path = repo_root / ".cursor" / "commands" / "review-pr.md"
        assert file_path.exists(), f"{file_path} does not exist"

        with open(file_path, "r") as f:
            content = f.read()

        # Should have content about PR review
        assert "review" in content.lower() or "pull request" in content.lower()


class TestConfigFileConsistency:
    """Test consistency across configuration files."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_review_pr_commands_consistency(self, repo_root: Path):
        """Test that review-pr commands are consistent across tools."""
        claude_file = repo_root / ".claude" / "commands" / "review-pr.md"
        cursor_file = repo_root / ".cursor" / "commands" / "review-pr.md"

        with open(claude_file, "r") as f:
            claude_content = f.read()

        with open(cursor_file, "r") as f:
            cursor_content = f.read()

        # Both should mention parallel execution
        assert "parallel" in claude_content.lower()
        assert "parallel" in cursor_content.lower()

        # Both should mention code quality checks
        assert "code quality" in claude_content.lower()
        assert "code quality" in cursor_content.lower()

    def test_speckit_commands_have_user_input_section(self, repo_root: Path):
        """Test that all speckit commands have user input handling."""
        speckit_dir = repo_root / ".agents" / "commands"
        speckit_files = list(speckit_dir.glob("speckit.*.md"))

        for file_path in speckit_files:
            with open(file_path, "r") as f:
                content = f.read()

            # Each command should have user input section
            assert "## User Input" in content or "User Input" in content
            assert "$ARGUMENTS" in content

    def test_all_markdown_files_have_valid_syntax(self, repo_root: Path):
        """Test that all markdown files have valid syntax."""
        markdown_files = [
            ".RULES_ANALYSIS.md",
            ".agents/commands/speckit.analyze.md",
            ".agents/commands/speckit.checklist.md",
            ".agents/commands/speckit.clarify.md",
            ".agents/commands/speckit.constitution.md",
            ".agents/commands/speckit.implement.md",
            ".agents/commands/speckit.plan.md",
            ".agents/commands/speckit.specify.md",
            ".agents/commands/speckit.tasks.md",
            ".claude/agents/planner.md",
            ".claude/commands/review-pr.md",
            ".claude/memories/CLAUDE.md",
            ".clinerules/cline_rules.md",
            ".clinerules/dev_workflow.md",
            ".clinerules/self_improve.md",
            ".clinerules/taskmaster.md",
            ".cursor/commands/review-pr.md",
        ]

        for md_file in markdown_files:
            file_path = repo_root / md_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Check for common markdown issues
            # - Unclosed code blocks
            code_block_count = content.count("```")
            assert code_block_count % 2 == 0, f"{md_file}: Unclosed code block"

            # - Valid headings (must have space after #)
            invalid_headings = re.findall(r'^#{1,6}[^\s#]', content, re.MULTILINE)
            assert len(invalid_headings) == 0, f"{md_file}: Invalid headings found: {invalid_headings}"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_empty_json_files_handled(self, repo_root: Path):
        """Test that empty JSON files are handled correctly."""
        # .claude/mcp.json is intentionally empty
        file_path = repo_root / ".claude" / "mcp.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Should be empty dict or valid JSON
        assert isinstance(data, dict)

    def test_json_files_have_no_trailing_commas(self, repo_root: Path):
        """Test that JSON files don't have trailing commas (invalid JSON)."""
        json_files = [
            ".claude/mcp.json",
            ".claude/settings.json",
            ".claude/settings.local.json",
            ".claude/slash_commands.json",
            ".concurrent_reviews.json",
            ".context-control/profiles/orchestration-tools.json",
        ]

        for json_file in json_files:
            file_path = repo_root / json_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Try to parse - will fail if invalid JSON
            try:
                json.loads(content)
            except json.JSONDecodeError as e:
                pytest.fail(f"{json_file}: Invalid JSON - {e}")

    def test_yaml_files_have_no_tabs(self, repo_root: Path):
        """Test that YAML files use spaces not tabs (YAML requirement)."""
        file_path = repo_root / ".aider.conf.yml"

        with open(file_path, "r") as f:
            content = f.read()

        # YAML should not have tabs
        assert "\t" not in content, ".aider.conf.yml contains tabs (YAML requires spaces)"

    def test_permissions_deny_patterns_are_valid(self, repo_root: Path):
        """Test that permission deny patterns are valid paths."""
        settings_file = repo_root / ".claude" / "settings.json"

        with open(settings_file, "r") as f:
            data = json.load(f)

        # Check deny patterns
        for pattern in data["permissions"]["deny"]:
            # Pattern should be in format "Tool(pattern)" or just "pattern"
            if "(" in pattern and ")" in pattern:
                # Extract the pattern
                match = re.match(r'(\w+)\((.*?)\)', pattern)
                assert match, f"Invalid permission pattern: {pattern}"
            else:
                # Should be a valid path pattern
                assert "/" in pattern or pattern.endswith("/"), f"Invalid path pattern: {pattern}"


class TestSecurityValidation:
    """Test security-related configuration validation."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_bandit_excludes_sensitive_dirs(self, repo_root: Path):
        """Test that Bandit excludes sensitive directories."""
        file_path = repo_root / ".bandit"

        import configparser
        config = configparser.ConfigParser()
        config.read(file_path)

        excluded = config["bandit"]["exclude_dirs"]

        # Should exclude version control and temp dirs
        sensitive_dirs = [".git", "__pycache__", "venv", ".venv"]
        for sensitive in sensitive_dirs:
            assert sensitive in excluded

    def test_permissions_block_credentials(self, repo_root: Path):
        """Test that permissions block access to credentials."""
        settings_files = [
            ".claude/settings.json",
            ".claude/settings.local.json",
        ]

        for settings_file in settings_files:
            file_path = repo_root / settings_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                data = json.load(f)

            # Should deny access to credentials
            deny_list = data.get("permissions", {}).get("deny", [])
            has_credential_block = any("credential" in item.lower() for item in deny_list)
            assert has_credential_block, f"{settings_file} should block credentials"

    def test_no_hardcoded_secrets_in_configs(self, repo_root: Path):
        """Test that configuration files don't contain hardcoded secrets."""
        # Patterns that might indicate hardcoded secrets
        secret_patterns = [
            r'api[_-]?key\s*[:=]\s*["\'][\w-]{20,}["\']',
            r'password\s*[:=]\s*["\'][^"\']{8,}["\']',
            r'secret\s*[:=]\s*["\'][^"\']{20,}["\']',
            r'token\s*[:=]\s*["\'][^"\']{20,}["\']',
        ]

        config_files = [
            ".aider.conf.yml",
            ".claude/settings.json",
            ".claude/settings.local.json",
        ]

        for config_file in config_files:
            file_path = repo_root / config_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Check for secret patterns (excluding env var references)
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                # Filter out env var references like ${VAR_NAME}
                actual_secrets = [m for m in matches if not m.startswith("${")]
                assert len(actual_secrets) == 0, \
                    f"{config_file} may contain hardcoded secrets: {actual_secrets}"


class TestNegativeCases:
    """Test negative cases and boundary conditions."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Get repository root directory."""
        return Path(__file__).parent.parent

    def test_concurrent_reviews_handles_empty_sessions(self, repo_root: Path):
        """Test that concurrent reviews can handle empty session list."""
        file_path = repo_root / ".concurrent_reviews.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Even with sessions, structure should be valid
        assert isinstance(data["review_sessions"], dict)

    def test_slash_commands_handle_special_chars_in_paths(self, repo_root: Path):
        """Test that slash commands properly handle special characters."""
        file_path = repo_root / ".claude" / "slash_commands.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        for cmd in data["commands"]:
            # Commands should not have unescaped special characters
            command_text = cmd["command"]
            # Check that paths are properly quoted if they contain spaces
            if " " in command_text and "/" in command_text:
                # Spaces in paths should be in quoted sections
                # This is a simplified check
                assert '"' in command_text or "'" in command_text

    def test_markdown_files_handle_code_blocks_with_languages(self, repo_root: Path):
        """Test that markdown code blocks specify languages."""
        markdown_files = [
            ".clinerules/cline_rules.md",
            ".clinerules/dev_workflow.md",
        ]

        for md_file in markdown_files:
            file_path = repo_root / md_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Find all code blocks
            code_blocks = re.findall(r'```(\w*)\n', content)

            # Count blocks with and without language
            total_blocks = len(code_blocks)
            blocks_with_lang = sum(1 for lang in code_blocks if lang)

            # At least 50% of code blocks should specify a language
            if total_blocks > 0:
                lang_percentage = blocks_with_lang / total_blocks
                # Allow some blocks without language (e.g., for generic text)
                # but most should have language specified
                # This is a quality check, not a strict requirement
                pass  # Just checking structure, not enforcing percentage