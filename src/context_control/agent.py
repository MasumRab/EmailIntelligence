"""Agent behavior adaptation based on project configuration."""

from typing import Dict, Any, Optional, List
import inspect

from .models import AgentContext, ProjectConfig
from .logging import get_context_logger
from .project import load_project_config


logger = get_context_logger()


class AgentAdapter:
    """Adapts agent behavior based on project and context configuration."""

    def __init__(self, context: AgentContext):
        """Initialize the agent adapter.

        Args:
            context: The agent context to adapt to
        """
        self.context = context
        self.project_config = self._load_project_config()
        logger.info(f"Agent adapter initialized for agent '{context.agent_id}'")

    def _load_project_config(self) -> Optional[ProjectConfig]:
        """Load project configuration for the current context.

        Returns:
            ProjectConfig or None
        """
        # Try to load from context profile first
        if self.context.profile_config:
            return self.context.profile_config

        # Fallback to loading from current directory
        return load_project_config()

    def get_agent_settings(self) -> Dict[str, Any]:
        """Get the complete agent settings combining context and project config.

        Returns:
            Dictionary of agent settings
        """
        settings = {}

        # Start with general agent settings from context
        settings.update(self.context.agent_settings)

        # Apply project configuration settings
        if self.project_config:
            project_settings = self._extract_agent_relevant_settings(self.project_config)
            settings.update(project_settings)

        # Add agent-specific settings (these override everything)
        if self.context.agent_id in self.context.agent_settings:
            agent_specific = self.context.agent_settings[self.context.agent_id]
            if isinstance(agent_specific, dict):
                settings.update(agent_specific)

        return settings

    def _extract_agent_relevant_settings(self, project_config: ProjectConfig) -> Dict[str, Any]:
        """Extract agent-relevant settings from project configuration.

        Args:
            project_config: Project configuration

        Returns:
            Dictionary of agent-relevant settings
        """
        settings = {}

        # Map project config to agent settings
        settings['max_context_length'] = project_config.max_context_length
        settings['enable_code_execution'] = project_config.enable_code_execution
        settings['enable_file_writing'] = project_config.enable_file_writing
        settings['enable_shell_commands'] = project_config.enable_shell_commands
        settings['preferred_models'] = project_config.preferred_models

        # Add custom settings
        settings.update(project_config.custom_settings)

        return settings

    def can_execute_code(self) -> bool:
        """Check if the agent can execute code.

        Returns:
            True if code execution is allowed
        """
        settings = self.get_agent_settings()
        return settings.get('enable_code_execution', False)

    def can_write_files(self) -> bool:
        """Check if the agent can write files.

        Returns:
            True if file writing is allowed
        """
        settings = self.get_agent_settings()
        return settings.get('enable_file_writing', False)

    def can_run_shell_commands(self) -> bool:
        """Check if the agent can run shell commands.

        Returns:
            True if shell commands are allowed
        """
        settings = self.get_agent_settings()
        return settings.get('enable_shell_commands', False)

    def get_max_context_length(self) -> int:
        """Get the maximum context length for the agent.

        Returns:
            Maximum context length
        """
        settings = self.get_agent_settings()
        return settings.get('max_context_length', 4096)

    def get_preferred_models(self) -> List[str]:
        """Get the preferred AI models for the agent.

        Returns:
            List of preferred model names
        """
        settings = self.get_agent_settings()
        return settings.get('preferred_models', ['gpt-4', 'claude-3'])

    def adapt_function_call(self, func_name: str, *args, **kwargs) -> tuple:
        """Adapt a function call based on agent permissions.

        Args:
            func_name: Name of the function being called
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tuple of (adapted_args, adapted_kwargs) or raises exception if not allowed
        """
        # Check permissions based on function type
        if self._is_code_execution_function(func_name):
            if not self.can_execute_code():
                raise PermissionError(f"Agent '{self.context.agent_id}' is not allowed to execute code")

        if self._is_file_writing_function(func_name):
            if not self.can_write_files():
                raise PermissionError(f"Agent '{self.context.agent_id}' is not allowed to write files")

        if self._is_shell_function(func_name):
            if not self.can_run_shell_commands():
                raise PermissionError(f"Agent '{self.context.agent_id}' is not allowed to run shell commands")

        # Apply context length limits if applicable
        if self._is_context_sensitive_function(func_name):
            max_length = self.get_max_context_length()
            adapted_kwargs = self._limit_context_length(kwargs, max_length)
            return args, adapted_kwargs

        return args, kwargs

    def _is_code_execution_function(self, func_name: str) -> bool:
        """Check if a function involves code execution.

        Args:
            func_name: Function name

        Returns:
            True if function involves code execution
        """
        code_functions = [
            'exec', 'eval', 'compile', 'run_code', 'execute_code',
            'run_python', 'run_script', 'subprocess', 'os.system'
        ]
        return any(pattern in func_name.lower() for pattern in code_functions)

    def _is_file_writing_function(self, func_name: str) -> bool:
        """Check if a function involves file writing.

        Args:
            func_name: Function name

        Returns:
            True if function involves file writing
        """
        write_functions = [
            'write_file', 'save_file', 'create_file', 'open',
            'write', 'save', 'dump', 'export'
        ]
        return any(pattern in func_name.lower() for pattern in write_functions)

    def _is_shell_function(self, func_name: str) -> bool:
        """Check if a function involves shell commands.

        Args:
            func_name: Function name

        Returns:
            True if function involves shell commands
        """
        shell_functions = [
            'run_command', 'shell', 'bash', 'sh', 'system',
            'popen', 'call', 'run', 'subprocess'
        ]
        return any(pattern in func_name.lower() for pattern in shell_functions)

    def _is_context_sensitive_function(self, func_name: str) -> bool:
        """Check if a function is sensitive to context length.

        Args:
            func_name: Function name

        Returns:
            True if function is context-sensitive
        """
        context_functions = [
            'generate', 'complete', 'chat', 'ask', 'query',
            'analyze', 'summarize', 'translate'
        ]
        return any(pattern in func_name.lower() for pattern in context_functions)

    def _limit_context_length(self, kwargs: Dict[str, Any], max_length: int) -> Dict[str, Any]:
        """Limit context length in function arguments.

        Args:
            kwargs: Keyword arguments
            max_length: Maximum allowed length

        Returns:
            Modified kwargs with limited context
        """
        adapted_kwargs = kwargs.copy()

        # Look for common context parameters
        context_keys = ['prompt', 'message', 'text', 'input', 'query', 'context']

        for key in context_keys:
            if key in adapted_kwargs and isinstance(adapted_kwargs[key], str):
                original_length = len(adapted_kwargs[key])
                if original_length > max_length:
                    adapted_kwargs[key] = adapted_kwargs[key][:max_length]
                    logger.warning(
                        f"Limited {key} from {original_length} to {max_length} characters "
                        f"for agent '{self.context.agent_id}'"
                    )

        return adapted_kwargs

    def get_behavior_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's adapted behavior.

        Returns:
            Dictionary with behavior settings
        """
        settings = self.get_agent_settings()

        return {
            'agent_id': self.context.agent_id,
            'can_execute_code': self.can_execute_code(),
            'can_write_files': self.can_write_files(),
            'can_run_shell_commands': self.can_run_shell_commands(),
            'max_context_length': self.get_max_context_length(),
            'preferred_models': self.get_preferred_models(),
            'project_name': self.project_config.project_name if self.project_config else None,
            'project_type': self.project_config.project_type if self.project_config else None,
        }