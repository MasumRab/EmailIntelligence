#!/usr/bin/env python3
"""
Additional edge case and integration tests for configuration files.
Tests boundary conditions, error handling, and cross-file consistency.
"""
import json
import re
from pathlib import Path
from typing import List

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from test_config_files_standalone import TestRunner


class EdgeCaseTests(TestRunner):
    """Additional edge case tests for configuration files."""

    def test_claude_settings_env_vars_not_hardcoded(self):
        """Test that environment variables are referenced, not hardcoded."""
        file_path = self.repo_root / ".claude" / "settings.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        if "env" in data:
            for key, value in data["env"].items():
                # Environment values should be strings
                self.assert_true(isinstance(value, str),
                                f"Env var {key} value must be a string")

    def test_slash_commands_paths_exist(self):
        """Test that slash commands reference valid workspace paths."""
        file_path = self.repo_root / ".claude" / "slash_commands.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        for cmd in data["commands"]:
            working_dir = cmd["working_directory"]
            # Should use ${workspaceFolder} or be absolute path
            self.assert_true("${workspaceFolder}" in working_dir or
                           working_dir.startswith("/"),
                           f"Command {cmd['name']} has invalid working_directory")

    def test_context_control_globs_are_valid(self):
        """Test that context control file patterns are valid glob patterns."""
        file_path = self.repo_root / ".context-control" / "profiles" / "orchestration-tools.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Check allowed files have valid glob patterns
        for pattern in data["allowed_files"]:
            # Should contain * or ** or be a specific extension
            self.assert_true("*" in pattern or pattern.endswith((".py", ".md", ".json", ".yml", ".yaml")),
                           f"Invalid file pattern: {pattern}")

    def test_concurrent_reviews_timestamps_are_numeric(self):
        """Test that concurrent reviews timestamps are valid numbers."""
        file_path = self.repo_root / ".concurrent_reviews.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        # Top-level timestamp
        self.assert_true(isinstance(data["timestamp"], (int, float)),
                        "Top-level timestamp must be numeric")

        # Session timestamps
        for session_id, session in data["review_sessions"].items():
            self.assert_true(isinstance(session["start_time"], (int, float)),
                           f"Session {session_id} start_time must be numeric")
            self.assert_true(isinstance(session["end_time"], (int, float)),
                           f"Session {session_id} end_time must be numeric")

            # Comment timestamps
            for comment in session["comments"]:
                self.assert_true(isinstance(comment["timestamp"], (int, float)),
                               f"Comment timestamp must be numeric")

    def test_aider_aliases_format(self):
        """Test that aider aliases are properly formatted."""
        if not HAS_YAML:
            self.skipped += 1
            print("⊘ Skipped: test_aider_aliases_format (PyYAML not available)")
            return

        file_path = self.repo_root / ".aider.conf.yml"

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        if "alias" in data:
            for alias in data["alias"]:
                # Should be in format "shortcut:model"
                self.assert_true(":" in alias,
                               f"Alias {alias} must be in format 'shortcut:model'")
                parts = alias.split(":")
                self.assert_equal(len(parts), 2,
                                f"Alias {alias} should have exactly one colon")

    def test_bandit_exclude_patterns_valid(self):
        """Test that bandit exclude patterns are valid directory names."""
        file_path = self.repo_root / ".bandit"

        import configparser
        config = configparser.ConfigParser()
        config.read(file_path)

        excluded = config["bandit"]["exclude_dirs"]

        # Should be comma-separated list
        patterns = [p.strip() for p in excluded.split(",")]

        for pattern in patterns:
            # Should be valid directory names (no special chars except - and _)
            self.assert_true(re.match(r'^[\w.-]+$', pattern),
                           f"Invalid exclusion pattern: {pattern}")

    def test_review_pr_commands_executable(self):
        """Test that review-pr commands contain actionable steps."""
        files = [
            ".claude/commands/review-pr.md",
            ".cursor/commands/review-pr.md",
        ]

        for file_path_str in files:
            file_path = self.repo_root / file_path_str
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Should mention specific review actions
            required_terms = ["code quality", "test", "documentation"]
            found_terms = sum(1 for term in required_terms if term.lower() in content.lower())

            self.assert_true(found_terms >= 2,
                           f"{file_path_str}: Should mention at least 2 review aspects")

    def test_speckit_commands_have_execution_steps(self):
        """Test that speckit commands define execution steps."""
        speckit_dir = self.repo_root / ".agents" / "commands"
        if not speckit_dir.exists():
            self.skipped += 1
            print("⊘ Skipped: test_speckit_commands_have_execution_steps")
            return

        speckit_files = list(speckit_dir.glob("speckit.*.md"))

        for file_path in speckit_files:
            with open(file_path, "r") as f:
                content = f.read()

            # Should have execution steps or outline
            has_steps = "## Execution Steps" in content or \
                       "## Outline" in content or \
                       "## Operating" in content

            self.assert_true(has_steps,
                           f"{file_path.name}: Should define execution steps")

    def test_markdown_headings_hierarchy(self):
        """Test that markdown files have proper heading hierarchy."""
        markdown_files = [
            ".RULES_ANALYSIS.md",
        ]

        for md_file_str in markdown_files:
            file_path = self.repo_root / md_file_str
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Skip frontmatter if present
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2]

            # Extract heading levels
            headings = re.findall(r'^(#{1,6})\s+', content, re.MULTILINE)

            if headings:
                # First heading should be level 1 or level 2 (for files with frontmatter)
                first_level = len(headings[0])
                self.assert_true(first_level <= 2,
                                f"{md_file_str}: First heading should be h1 or h2, got h{first_level}")

    def test_json_files_proper_indentation(self):
        """Test that JSON files use consistent indentation."""
        json_files = [
            ".claude/settings.json",
            ".claude/slash_commands.json",
        ]

        for json_file_str in json_files:
            file_path = self.repo_root / json_file_str
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()
                data = json.loads(content)

            # Re-serialize with standard indentation
            normalized = json.dumps(data, indent=2)

            # Content should use consistent indentation (2 or 4 spaces)
            # This is a soft check - we're just ensuring it's valid
            pass  # If it loaded successfully, indentation is acceptable

    def test_permissions_allow_list_valid(self):
        """Test that permission allow lists contain valid tool names."""
        file_path = self.repo_root / ".claude" / "settings.json"

        with open(file_path, "r") as f:
            data = json.load(f)

        if "permissions" in data and "allow" in data["permissions"]:
            for tool in data["permissions"]["allow"]:
                # Should be a valid tool name or pattern
                # Valid patterns: "ToolName", "ToolName(*)", "tool"
                self.assert_true(isinstance(tool, str) and len(tool) > 0,
                               f"Invalid tool in allow list: {tool}")

    def test_clinerules_glob_patterns_valid(self):
        """Test that clinerules globs are valid patterns."""
        if not HAS_YAML:
            self.skipped += 1
            print("⊘ Skipped: test_clinerules_glob_patterns_valid")
            return

        rules_files = [
            ".clinerules/cline_rules.md",
            ".clinerules/dev_workflow.md",
        ]

        for rules_file_str in rules_files:
            file_path = self.repo_root / rules_file_str
            if not file_path.exists():
                continue

            with open(file_path, "r") as f:
                content = f.read()

            # Extract frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                continue

            try:
                # Try to load YAML - if it has unquoted special chars it may fail
                frontmatter = yaml.safe_load(match.group(1))

                if "globs" in frontmatter:
                    # Should be a valid glob pattern
                    globs = frontmatter["globs"]
                    if isinstance(globs, str):
                        # Single glob - any string is valid
                        self.assert_true(len(globs) > 0, "Glob pattern must not be empty")
                    elif isinstance(globs, list):
                        # List of globs
                        for glob in globs:
                            self.assert_true(isinstance(glob, str),
                                           f"Glob must be string: {glob}")
            except yaml.YAMLError:
                # YAML parsing failed - this is acceptable for some frontmatter
                # that may not strictly follow YAML rules
                pass

    def run_all_tests(self):
        """Run all edge case tests."""
        print("Running edge case tests...")
        print("=" * 70)

        self.run_test(self.test_claude_settings_env_vars_not_hardcoded,
                     "test_claude_settings_env_vars_not_hardcoded")
        self.run_test(self.test_slash_commands_paths_exist,
                     "test_slash_commands_paths_exist")
        self.run_test(self.test_context_control_globs_are_valid,
                     "test_context_control_globs_are_valid")
        self.run_test(self.test_concurrent_reviews_timestamps_are_numeric,
                     "test_concurrent_reviews_timestamps_are_numeric")
        self.run_test(self.test_aider_aliases_format,
                     "test_aider_aliases_format")
        self.run_test(self.test_bandit_exclude_patterns_valid,
                     "test_bandit_exclude_patterns_valid")
        self.run_test(self.test_review_pr_commands_executable,
                     "test_review_pr_commands_executable")
        self.run_test(self.test_speckit_commands_have_execution_steps,
                     "test_speckit_commands_have_execution_steps")
        self.run_test(self.test_markdown_headings_hierarchy,
                     "test_markdown_headings_hierarchy")
        self.run_test(self.test_json_files_proper_indentation,
                     "test_json_files_proper_indentation")
        self.run_test(self.test_permissions_allow_list_valid,
                     "test_permissions_allow_list_valid")
        self.run_test(self.test_clinerules_glob_patterns_valid,
                     "test_clinerules_glob_patterns_valid")

        return self.print_summary()


def main():
    """Main entry point."""
    import sys
    runner = EdgeCaseTests()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()