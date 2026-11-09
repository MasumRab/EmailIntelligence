import json
import os
import argparse
from pathlib import Path

def deep_merge(source, destination):
    """
    Recursively merges source dict into destination dict.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value
    return destination

class ConfigManager:
    def __init__(self, project_root):
        self.project_root = Path(project_root).resolve()
        self.global_config_path = Path.home() / ".config" / "email-intelligence" / "config.json"
        self.project_config_path = self.project_root / "agent-config.json"
        self.local_config_path = self.project_root / "agent-config.local.json"
        self.merged_config = {}

    def load_config(self):
        """
        Loads and merges configs in the correct order of precedence:
        Global -> Project -> Local
        """
        # 1. Load Global Config (lowest precedence)
        if self.global_config_path.exists():
            try:
                with open(self.global_config_path, "r") as f:
                    global_config = json.load(f)
                    deep_merge(global_config, self.merged_config)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse global config file: {self.global_config_path}", file=os.stderr)

        # 2. Load Project Config (overrides Global)
        if self.project_config_path.exists():
            try:
                with open(self.project_config_path, "r") as f:
                    project_config = json.load(f)
                    deep_merge(project_config, self.merged_config)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse project config file: {self.project_config_path}", file=os.stderr)

        # 3. Load Local Config (highest precedence)
        if self.local_config_path.exists():
            try:
                with open(self.local_config_path, "r") as f:
                    local_config = json.load(f)
                    deep_merge(local_config, self.merged_config)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse local config file: {self.local_config_path}", file=os.stderr)

        # Prioritize environment variables for API keys
        if "api_keys" in self.merged_config:
            for key_name, _ in self.merged_config["api_keys"].items():
                env_var_name = f"{key_name.upper()}_API_KEY"
                if env_var_name in os.environ:
                    self.merged_config["api_keys"][key_name] = os.environ[env_var_name]

        return self.merged_config

    def output_env_vars(self):
        """
        Prints export commands for environment variables based on the merged config.
        """
        env_vars_to_export = {}

        # API Keys
        if "api_keys" in self.merged_config:
            for key_name, value in self.merged_config["api_keys"].items():
                if value and not key_name.startswith("_"): # Ignore comments
                    env_var_name = f"{key_name.upper()}_API_KEY"
                    env_vars_to_export[env_var_name] = value

        # Other top-level settings that might be useful as env vars
        # Add more as needed based on your CLI tools' requirements
        if "models" in self.merged_config:
            for model_type, model_name in self.merged_config["models"].items():
                if not model_type.startswith("_"): # Ignore comments
                    env_vars_to_export[f"{model_type.upper()}_MODEL"] = model_name

        for var_name, var_value in env_vars_to_export.items():
            print(f"export {var_name}='{var_value}'")

    def generate_tool_configs(self):
        """
        Generates tool-specific configuration files based on the merged config.
        """
        # Example for Gemini CLI config
        if "agents" in self.merged_config and "gemini" in self.merged_config["agents"]:
            gemini_config_dir = self.project_root / ".gemini"
            gemini_config_dir.mkdir(parents=True, exist_ok=True)
            gemini_config_path = gemini_config_dir / "config.json"
            with open(gemini_config_path, "w") as f:
                json.dump(self.merged_config["agents"]["gemini"], f, indent=2)
            print(f"Generated Gemini tool config: {gemini_config_path}", file=os.stderr)

        # Example for Claude CLI config
        if "agents" in self.merged_config and "claude" in self.merged_config["agents"]:
            claude_config_dir = self.project_root / ".claude"
            claude_config_dir.mkdir(parents=True, exist_ok=True)
            claude_settings_path = claude_config_dir / "settings.json"
            with open(claude_settings_path, "w") as f:
                json.dump(self.merged_config["agents"]["claude"], f, indent=2)
            print(f"Generated Claude tool config: {claude_settings_path}", file=os.stderr)

        # Example for MCP servers (if they need a specific config file)
        if "mcp_servers" in self.merged_config:
            # This assumes MCP servers might need a .mcp.json in the project root
            # The structure here should match what the MCP server expects
            mcp_config_path = self.project_root / ".mcp.json"
            with open(mcp_config_path, "w") as f:
                json.dump({"mcpServers": self.merged_config["mcp_servers"]}, f, indent=2)
            print(f"Generated MCP server config: {mcp_config_path}", file=os.stderr)


def main():
    parser = argparse.ArgumentParser(description="Manage agent configurations.")
    parser.add_argument("--project-root", type=str, default=".",
                        help="The root directory of the project.")
    parser.add_argument("--output-env", action="store_true",
                        help="Output environment variables as 'export' commands.")
    parser.add_argument("--generate-tool-configs", action="store_true",
                        help="Generate tool-specific configuration files.")
    parser.add_argument("--show-merged-config", action="store_true",
                        help="Print the final merged configuration.")

    args = parser.parse_args()

    manager = ConfigManager(args.project_root)
    merged_config = manager.load_config()

    if args.output_env:
        manager.output_env_vars()
    if args.generate_tool_configs:
        manager.generate_tool_configs()
    if args.show_merged_config:
        print(json.dumps(merged_config, indent=2))

if __name__ == "__main__":
    main()
