#!/usr/bin/env python3
"""
Standalone test runner for configuration files.
Does not require pytest or other test dependencies.
Can be run directly with: python tests/test_config_files_standalone.py
"""
import configparser
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("Warning: PyYAML not installed, YAML tests will be skipped")


class TestRunner:
    """Simple test runner that collects and executes tests."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors: List[Tuple[str, str]] = []

    def assert_true(self, condition: bool, message: str):
        """Assert that a condition is true."""
        if not condition:
            raise AssertionError(message)

    def assert_equal(self, actual, expected, message: str = ""):
        """Assert that two values are equal."""
        if actual != expected:
            msg = f"Expected {expected}, got {actual}"
            if message:
                msg = f"{message}: {msg}"
            raise AssertionError(msg)

    def assert_in(self, item, container, message: str = ""):
        """Assert that item is in container."""
        if item not in container:
            msg = f"{item} not found in {container}"
            if message:
                msg = f"{message}: {msg}"
            raise AssertionError(msg)

    def run_test(self, test_func, test_name: str):
        """Run a single test function."""
        try:
            test_func()
            print(f"✓ {test_name}")
            self.passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            self.failed += 1
            self.errors.append((test_name, str(e)))
        except Exception as e:  # noqa: BLE001 - test harness should record unexpected failures
            print(f"E {test_name}: {e}")
            self.failed += 1
            self.errors.append((test_name, f"Exception: {e}"))

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed + self.skipped
        print("\n" + "=" * 70)
        print(f"Test Results: {self.passed} passed, {self.failed} failed, {self.skipped} skipped out of {total} total")

        if self.errors:
            print("\nFailed tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")

        print("=" * 70)
        return self.failed == 0


class ConfigFileTests(TestRunner):
    """Test suite for configuration files."""

    def test_claude_mcp_json_valid(self):
        """Test .claude/mcp.json is valid (may be empty)."""
        file_path = self.repo_root / ".claude" / "mcp.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            content = f.read().strip()

        # File may be empty or contain valid JSON
        if content:
            data = json.loads(content)
            self.assert_true(isinstance(data, dict), "MCP config must be a dict")

    def test_claude_settings_json_valid(self):
        """Test .claude/settings.json has valid permissions structure."""
        file_path = self.repo_root / ".claude" / "settings.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate structure
        self.assert_in("env", data)
        self.assert_in("permissions", data)
        self.assert_in("allow", data["permissions"])
        self.assert_in("deny", data["permissions"])

        # Validate allow list
        self.assert_in("Edit", data["permissions"]["allow"])
        self.assert_in("Bash(*)", data["permissions"]["allow"])

        # Validate deny list blocks credentials
        deny_list = data["permissions"]["deny"]
        has_cred_block = any("credential" in str(item).lower() for item in deny_list)
        self.assert_true(has_cred_block, "Should block credentials directory")

        # Validate env
        self.assert_in("ANTHROPIC_BASE_URL", data["env"])

    def test_claude_settings_local_json_valid(self):
        """Test .claude/settings.local.json has valid structure."""
        file_path = self.repo_root / ".claude" / "settings.local.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = json.load(f)

        self.assert_in("permissions", data)
        self.assert_true(isinstance(data["permissions"]["deny"], list),
                        "permissions.deny must be a list")

    def test_claude_slash_commands_json_valid(self):
        """Test .claude/slash_commands.json has valid command structure."""
        file_path = self.repo_root / ".claude" / "slash_commands.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = json.load(f)

        self.assert_in("commands", data)
        self.assert_true(isinstance(data["commands"], list),
                        "commands must be a list")

        # Validate each command has required fields
        for cmd in data["commands"]:
            self.assert_in("name", cmd)
            self.assert_in("description", cmd)
            self.assert_in("command", cmd)
            self.assert_in("working_directory", cmd)

        # Check for specific expected commands
        command_names = [cmd["name"] for cmd in data["commands"]]
        expected_commands = ["task-next", "task-start", "task-complete"]
        for expected_cmd in expected_commands:
            self.assert_in(expected_cmd, command_names)

    def test_concurrent_reviews_json_valid(self):
        """Test .concurrent_reviews.json has valid review session structure."""
        file_path = self.repo_root / ".concurrent_reviews.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = json.load(f)

        self.assert_in("timestamp", data)
        self.assert_in("review_sessions", data)
        self.assert_true(isinstance(data["review_sessions"], dict),
                        "review_sessions must be a dict")

        # Validate each review session (if any exist)
        for _session_id, session in data["review_sessions"].items():
            self.assert_in("session_id", session)
            self.assert_in("document_id", session)
            self.assert_in("reviewers", session)
            self.assert_in("status", session)
            self.assert_in("comments", session)

            # Validate status
            valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
            self.assert_in(session["status"], valid_statuses)

    def test_context_control_profile_valid(self):
        """Test .context-control/profiles/orchestration-tools.json is valid."""
        file_path = self.repo_root / ".context-control" / "profiles" / "orchestration-tools.json"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = json.load(f)

        # Validate required fields
        required_fields = ["id", "name", "description", "branch_patterns",
                          "allowed_files", "blocked_files", "agent_settings"]
        for field in required_fields:
            self.assert_in(field, data)

        # Validate types
        self.assert_true(isinstance(data["branch_patterns"], list),
                        "branch_patterns must be a list")
        self.assert_true(isinstance(data["allowed_files"], list),
                        "allowed_files must be a list")
        self.assert_true(isinstance(data["blocked_files"], list),
                        "blocked_files must be a list")
        self.assert_true(isinstance(data["agent_settings"], dict),
                        "agent_settings must be a dict")

    def test_aider_conf_yml_valid(self):
        """Test .aider.conf.yml is valid YAML with correct structure."""
        if not HAS_YAML:
            self.skipped += 1
            print("⊘ Skipped: test_aider_conf_yml_valid (PyYAML not available)")
            return

        file_path = self.repo_root / ".aider.conf.yml"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        self.assert_in("model", data)
        self.assert_true(isinstance(data["model"], str), "model must be a string")
        self.assert_true(len(data["model"]) > 0, "model must not be empty")

    def test_bandit_config_valid(self):
        """Test .bandit configuration is valid."""
        file_path = self.repo_root / ".bandit"
        self.assert_true(file_path.exists(), f"{file_path} does not exist")

        with open(file_path, "r") as f:
            content = f.read()

        config = configparser.ConfigParser()
        config.read_string(content)

        self.assert_in("bandit", config)
        self.assert_in("exclude_dirs", config["bandit"])

        excluded = config["bandit"]["exclude_dirs"]
        expected_exclusions = [".git", "__pycache__", "venv"]
        for expected in expected_exclusions:
            self.assert_true(expected in excluded, f"Missing exclusion: {expected}")

    def test_markdown_frontmatter(self):
        """Test that key markdown files have valid YAML frontmatter."""
        if not HAS_YAML:
            self.skipped += 1
            print("⊘ Skipped: test_markdown_frontmatter (PyYAML not available)")
            return

        files_to_check = [
            ".agents/commands/speckit.analyze.md",
            ".agents/commands/speckit.checklist.md",
            ".claude/agents/planner.md",
        ]

        for md_file in files_to_check:
            file_path = self.repo_root / md_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Extract frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            self.assert_true(match, f"{md_file}: Missing YAML frontmatter")

            frontmatter_text = match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)

            self.assert_in("description", frontmatter, f"{md_file}: Missing description")

    def test_markdown_code_blocks_closed(self):
        """Test that markdown files have properly closed code blocks."""
        markdown_files = [
            ".RULES_ANALYSIS.md",
            ".clinerules/cline_rules.md",
            ".clinerules/dev_workflow.md",
        ]

        for md_file in markdown_files:
            file_path = self.repo_root / md_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            code_block_count = content.count("```")
            self.assert_equal(code_block_count % 2, 0,
                            f"{md_file}: Unclosed code block")

    def test_no_hardcoded_secrets(self):
        """Test that configuration files don't contain hardcoded secrets."""
        secret_patterns = [
            r'api[_-]?key\s*[:=]\s*["\'][\w-]{20,}["\']',
            r'password\s*[:=]\s*["\'][^"\']{8,}["\']',
        ]

        config_files = [
            ".aider.conf.yml",
            ".claude/settings.json",
        ]

        for config_file in config_files:
            file_path = self.repo_root / config_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                # Filter out env var references like ${VAR_NAME}
                actual_secrets = [m for m in matches if not "${" in m]
                self.assert_equal(len(actual_secrets), 0,
                                f"{config_file} may contain hardcoded secrets")

    def test_json_no_trailing_commas(self):
        """Test that JSON files don't have trailing commas."""
        json_files = [
            ".claude/settings.json",
            ".claude/settings.local.json",
            ".claude/slash_commands.json",
            ".concurrent_reviews.json",
            ".context-control/profiles/orchestration-tools.json",
        ]

        for json_file in json_files:
            file_path = self.repo_root / json_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            try:
                json.loads(content)
            except json.JSONDecodeError as e:
                self.assert_true(False, f"{json_file}: Invalid JSON - {e}")

    def test_permissions_structure(self):
        """Test that permission configurations have proper structure."""
        settings_files = [
            ".claude/settings.json",
            ".claude/settings.local.json",
        ]

        for settings_file in settings_files:
            file_path = self.repo_root / settings_file
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                data = json.load(f)

            if "permissions" in data:
                self.assert_true(isinstance(data["permissions"], dict),
                                f"{settings_file}: permissions must be a dict")

                if "deny" in data["permissions"]:
                    deny_list = data["permissions"]["deny"]
                    self.assert_true(isinstance(deny_list, list),
                                    f"{settings_file}: permissions.deny must be a list")

    def test_speckit_commands_structure(self):
        """Test that speckit command files have consistent structure."""
        speckit_dir = self.repo_root / ".agents" / "commands"
        if not speckit_dir.exists():
            self.skipped += 1
            print("⊘ Skipped: test_speckit_commands_structure (directory not found)")
            return

        speckit_files = list(speckit_dir.glob("speckit.*.md"))

        for file_path in speckit_files:
            with open(file_path, "r") as f:
                content = f.read()

            # Each command should handle user input
            has_user_input = "User Input" in content or "$ARGUMENTS" in content
            self.assert_true(has_user_input,
                           f"{file_path.name}: Missing user input handling")

    def run_all_tests(self):
        """Run all tests and return success status."""
        print("Running configuration file tests...")
        print("=" * 70)

        # JSON tests
        self.run_test(self.test_claude_mcp_json_valid, "test_claude_mcp_json_valid")
        self.run_test(self.test_claude_settings_json_valid, "test_claude_settings_json_valid")
        self.run_test(self.test_claude_settings_local_json_valid, "test_claude_settings_local_json_valid")
        self.run_test(self.test_claude_slash_commands_json_valid, "test_claude_slash_commands_json_valid")
        self.run_test(self.test_concurrent_reviews_json_valid, "test_concurrent_reviews_json_valid")
        self.run_test(self.test_context_control_profile_valid, "test_context_control_profile_valid")

        # YAML tests
        self.run_test(self.test_aider_conf_yml_valid, "test_aider_conf_yml_valid")

        # Config tests
        self.run_test(self.test_bandit_config_valid, "test_bandit_config_valid")

        # Markdown tests
        self.run_test(self.test_markdown_frontmatter, "test_markdown_frontmatter")
        self.run_test(self.test_markdown_code_blocks_closed, "test_markdown_code_blocks_closed")

        # Security tests
        self.run_test(self.test_no_hardcoded_secrets, "test_no_hardcoded_secrets")
        self.run_test(self.test_json_no_trailing_commas, "test_json_no_trailing_commas")
        self.run_test(self.test_permissions_structure, "test_permissions_structure")

        # Structure tests
        self.run_test(self.test_speckit_commands_structure, "test_speckit_commands_structure")

        return self.print_summary()


def main():
    """Main entry point."""
    runner = ConfigFileTests()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()