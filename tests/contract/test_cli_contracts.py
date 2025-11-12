import pytest
import subprocess
import re
import os
from pathlib import Path

# Assuming the CLI entry point will be something like 'python -m src.cli.main'
CLI_COMMAND = ["python", "-m", "src.cli.main"]
CLI_CONTRACTS_PATH = Path(__file__).parent.parent.parent / "specs/003-unified-git-analysis/contracts/cli-contracts.md"

def parse_cli_contracts(contract_path):
    """
    Parses the CLI contracts Markdown file to extract expected commands and their usage.
    Returns a dictionary of commands with their arguments and options.
    """
    contracts = {}
    current_command = None
    
    content = contract_path.read_text()
    lines = content.splitlines()

    for i, line in enumerate(lines):
        # Detect sub-command headers (e.g., "### Sub-command: analyze")
        match_command = re.match(r"### Sub-command: `(.*)`", line)
        if match_command:
            current_command = match_command.group(1)
            contracts[current_command] = {"usage": "", "arguments": [], "options": []}
            continue

        if current_command:
            # Detect Usage section
            if "Usage" in line and "```bash" in lines[i+1]:
                contracts[current_command]["usage"] = lines[i+2].strip()
            
            # Detect Arguments section
            if "Arguments" in line and "---" in lines[i+2]:
                j = i + 3
                while j < len(lines) and lines[j].strip() and not lines[j].startswith("##"):
                    arg_match = re.match(r"- `(.*)`: (.*)", lines[j])
                    if arg_match:
                        contracts[current_command]["arguments"].append({"name": arg_match.group(1), "description": arg_match.group(2)})
                    j += 1
            
            # Detect Options section
            if "Options" in line and "---" in lines[i+2]:
                j = i + 3
                while j < len(lines) and lines[j].strip() and not lines[j].startswith("##"):
                    opt_match = re.match(r"- `(.*)`: (.*)", lines[j])
                    if opt_match:
                        contracts[current_command]["options"].append({"name": opt_match.group(1), "description": opt_match.group(2)})
                    j += 1
    return contracts

@pytest.fixture(scope="module")
def cli_contracts():
    return parse_cli_contracts(CLI_CONTRACTS_PATH)

class TestCliContracts:

    def test_cli_entry_point_exists(self):
        """Verify that the main CLI entry point script exists."""
        cli_script_path = Path("src/cli/main.py")
        assert cli_script_path.exists(), f"CLI entry point script not found at {cli_script_path}"

    def test_cli_help_output(self):
        """Verify that the main CLI command shows a help message."""
        result = subprocess.run(
            CLI_COMMAND + ["--help"],
            capture_output=True, text=True, check=True
        )
        assert "usage: git-verifier" in result.stdout
        # Check for presence of subcommand names instead of "Available commands:"
        assert "analyze" in result.stdout
        assert "detect-rebased" in result.stdout
        assert "verify" in result.stdout
        assert result.returncode == 0

    @pytest.mark.parametrize("command_name", ["analyze", "detect-rebased", "verify"])
    def test_subcommand_help_output(self, command_name):
        """Verify that each sub-command shows a help message."""
        result = subprocess.run(
            CLI_COMMAND + [command_name, "--help"],
            capture_output=True, text=True, check=True
        )
        assert f"usage: git-verifier {command_name}" in result.stdout
        assert "options:" in result.stdout # argparse uses "options:"
        assert result.returncode == 0

    def test_analyze_subcommand_contract(self, cli_contracts):
        """Validate 'analyze' subcommand arguments and options against contract."""
        contract = cli_contracts.get("analyze")
        assert contract is not None, "Analyze command contract not found."

        # Test --help output for arguments/options presence
        help_result = subprocess.run(
            CLI_COMMAND + ["analyze", "--help"],
            capture_output=True, text=True, check=True
        )
        help_output = help_result.stdout

        for arg in contract["arguments"]:
            # For argparse, positional arguments are listed without their backticks
            arg_name_in_output = arg["name"].replace("`", "")
            assert arg_name_in_output in help_output, f"Argument '{arg['name']}' not found in 'analyze --help' output."
        
        for opt in contract["options"]:
            # For options like --output-file <PATH>, check for both --option and its argument part
            opt_name_in_output = opt["name"].split(" ")[0] # Get just the --option part
            assert opt_name_in_output in help_output, f"Option '{opt['name']}' not found in 'analyze --help' output."
            if "<" in opt["name"] and ">" in opt["name"]:
                # Check for the argument part of the option as well
                arg_part = opt["name"].split(" ")[1].strip("<>")
                assert arg_part in help_output, f"Option argument '{arg_part}' not found in 'analyze --help' output for option '{opt['name']}'."


    def test_detect_rebased_subcommand_contract(self, cli_contracts):
        """Validate 'detect-rebased' subcommand arguments and options against contract."""
        contract = cli_contracts.get("detect-rebased")
        assert contract is not None, "Detect-rebased command contract not found."

        help_result = subprocess.run(
            CLI_COMMAND + ["detect-rebased", "--help"],
            capture_output=True, text=True, check=True
        )
        help_output = help_result.stdout

        for opt in contract["options"]:
            opt_name_in_output = opt["name"].split(" ")[0]
            assert opt_name_in_output in help_output, f"Option '{opt['name']}' not found in 'detect-rebased --help' output."
            if "<" in opt["name"] and ">" in opt["name"]:
                arg_part = opt["name"].split(" ")[1].strip("<>")
                assert arg_part in help_output, f"Option argument '{arg_part}' not found in 'detect-rebased --help' output for option '{opt['name']}'."

    def test_verify_subcommand_contract(self, cli_contracts):
        """Validate 'verify' subcommand arguments and options against contract."""
        contract = cli_contracts.get("verify")
        assert contract is not None, "Verify command contract not found."

        help_result = subprocess.run(
            CLI_COMMAND + ["verify", "--help"],
            capture_output=True, text=True, check=True
        )
        help_output = help_result.stdout

        for opt in contract["options"]:
            opt_name_in_output = opt["name"].split(" ")[0]
            assert opt_name_in_output in help_output, f"Option '{opt['name']}' not found in 'verify --help' output."
            if "<" in opt["name"] and ">" in opt["name"]:
                arg_part = opt["name"].split(" ")[1].strip("<>")
                assert arg_part in help_output, f"Option argument '{arg_part}' not found in 'verify --help' output for option '{opt['name']}'."

        # Check for required options specifically
        required_options = ["--report <INTENT_REPORT_PATH>", "--merged-branch <BRANCH_NAME>"]
        for req_opt in required_options:
            req_opt_name_in_output = req_opt.split(" ")[0]
            assert req_opt_name_in_output in help_output, f"Required option '{req_opt}' not found in 'verify --help' output."