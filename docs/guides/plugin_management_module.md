# Plugin Management Module Documentation

## Overview

The Plugin Management module provides a comprehensive plugin system for the Email Intelligence Platform, enabling extensible functionality through secure, sandboxed plugin execution with marketplace integration and lifecycle management.

## Architecture

### Key Components

#### 1. Plugin Base System (`src/core/plugin_base.py`)
Core interfaces, security mechanisms, and lifecycle management.

#### 2. Plugin Manager (`src/core/plugin_manager.py`)
Orchestration component handling plugin lifecycle, marketplace, and security.

#### 3. Plugin Routes (`src/core/plugin_routes.py`)
RESTful API endpoints for programmatic plugin management.

#### 4. Module Interface (`modules/plugin_management/__init__.py`)
Integration layer connecting plugin system with main application.

### Data Flow
```
Plugin Marketplace ←→ Plugin Manager ←→ Security Sandbox ←→ Plugin Instances
       ↓                    ↓                    ↓              ↓
   Download/Install    Lifecycle Mgmt       Execution        User Code
   (ZIP/Files)        (Load/Unload)       (Isolated)       (Hooks/Events)
```

### Integration Points
- **Security Module:** Path validation and sandboxing
- **Audit Logger:** Plugin operation logging
- **FastAPI:** REST API endpoint registration
- **Gradio UI:** Administrative plugin management interface
- **Marketplace:** External plugin repository integration

## Core Classes & Functions

### Plugin Base System

#### Plugin Metadata
```python
@dataclass
class PluginMetadata:
    """Metadata for plugin identification and management."""
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    license: str = "MIT"
    homepage: Optional[str] = None
    repository: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    security_level: PluginSecurityLevel = PluginSecurityLevel.STANDARD
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: __import__('time').time())
    checksum: Optional[str] = None
```

#### Plugin Interface
```python
class PluginInterface(abc.ABC):
    """Abstract base class for all plugins.

    Plugins must implement these methods to integrate with the platform.
    """

    @abc.abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass

    @abc.abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        pass

    @abc.abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the plugin and cleanup resources."""
        pass

    @abc.abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities/features."""
        pass

    @abc.abstractmethod
    def get_required_permissions(self) -> List[str]:
        """Return list of required permissions."""
        pass

    @abc.abstractmethod
    async def execute_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute a plugin hook with parameters."""
        pass
```

#### Plugin Security Levels
```python
class PluginSecurityLevel(Enum):
    """Security levels for plugin execution."""
    TRUSTED = "trusted"      # Full system access
    STANDARD = "standard"    # Limited API access
    SANDBOXED = "sandboxed"  # Isolated execution environment
```

### Plugin Manager

#### Main Class
```python
class PluginManager:
    """Comprehensive plugin management system with marketplace integration,
    security, and lifecycle management.
    """

    def __init__(self, plugins_dir: Optional[Path] = None):
        self.plugins_dir = plugins_dir or Path("./plugins")
        self.registry = PluginRegistry()
        self.marketplace_url = "https://api.emailintelligence.dev/plugins"
        self.security_manager = SecuritySandbox()
        self._initialized = False

    async def initialize(self):
        """Initialize the plugin manager and discover installed plugins."""
        if self._initialized:
            return

        # Create plugins directory
        self.plugins_dir.mkdir(exist_ok=True)

        # Discover and validate installed plugins
        await self._discover_plugins()

        # Initialize security sandbox
        await self.security_manager.initialize()

        self._initialized = True
        logger.info("PluginManager initialized successfully")
```

#### Plugin Discovery
```python
async def _discover_plugins(self):
    """Discover and validate all installed plugins."""
    if not self.plugins_dir.exists():
        return

    for plugin_dir in self.plugins_dir.iterdir():
        if plugin_dir.is_dir() and (plugin_dir / "__init__.py").exists():
            try:
                plugin_id = plugin_dir.name
                await self._load_plugin(plugin_id)
                logger.info(f"Discovered plugin: {plugin_id}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_id}: {e}")
                # Mark as error state but don't crash system
                await self.registry.update_plugin_status(plugin_id, PluginStatus.ERROR)
```

#### Plugin Installation
```python
async def install_plugin(self, plugin_id: str, version: Optional[str] = None) -> Dict[str, Any]:
    """Install a plugin from the marketplace."""
    try:
        # Get plugin information from marketplace
        plugin_info = await self._get_marketplace_plugin(plugin_id, version)
        if not plugin_info:
            raise ValueError(f"Plugin {plugin_id} not found in marketplace")

        # Download and validate plugin package
        plugin_path = await self._download_plugin(plugin_info)

        # Extract and install
        install_dir = self.plugins_dir / plugin_id
        await self._extract_plugin(plugin_path, install_dir)

        # Validate installation
        if not await self._validate_plugin_installation(install_dir):
            await self._cleanup_failed_installation(install_dir)
            raise ValueError(f"Plugin installation validation failed: {plugin_id}")

        # Register plugin
        await self.registry.register_plugin(plugin_id, install_dir)

        # Mark as installed
        await self.registry.update_plugin_status(plugin_id, PluginStatus.INSTALLED)

        return {
            "plugin_id": plugin_id,
            "status": "installed",
            "version": plugin_info.version,
            "capabilities": plugin_info.capabilities
        }

    except Exception as e:
        logger.error(f"Failed to install plugin {plugin_id}: {e}")
        raise
```

#### Plugin Loading
```python
async def load_plugin(self, plugin_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Load and initialize a plugin."""
    try:
        # Validate plugin exists and is in correct state
        if not await self.registry.plugin_exists(plugin_id):
            raise ValueError(f"Plugin {plugin_id} not found")

        status = await self.registry.get_plugin_status(plugin_id)
        if status != PluginStatus.INSTALLED and status != PluginStatus.DISABLED:
            raise ValueError(f"Plugin {plugin_id} is not in installable state: {status}")

        # Load plugin module
        plugin_module = await self._load_plugin_module(plugin_id)

        # Create plugin instance
        plugin_instance = await self._create_plugin_instance(plugin_module, config or {})

        # Validate security permissions
        await self._validate_plugin_security(plugin_instance)

        # Initialize plugin in sandbox
        success = await self.security_manager.execute_plugin_init(
            plugin_instance, config or {}
        )

        if not success:
            raise RuntimeError(f"Plugin initialization failed: {plugin_id}")

        # Register with hook system
        await self._register_plugin_hooks(plugin_instance)

        # Update status
        await self.registry.update_plugin_status(plugin_id, PluginStatus.ENABLED)

        return {
            "plugin_id": plugin_id,
            "status": "loaded",
            "capabilities": plugin_instance.get_capabilities(),
            "security_level": plugin_instance.metadata.security_level.value
        }

    except Exception as e:
        logger.error(f"Failed to load plugin {plugin_id}: {e}")
        await self.registry.update_plugin_status(plugin_id, PluginStatus.ERROR)
        raise
```

### Security Sandbox

#### Execution Environment
```python
class SecuritySandbox:
    """Isolated execution environment for plugin security."""

    def __init__(self):
        self._active_plugins: Dict[str, PluginInstance] = {}
        self._security_contexts: Dict[str, SecurityContext] = {}

    async def execute_plugin_init(self, plugin: PluginInstance, config: Dict[str, Any]) -> bool:
        """Initialize plugin in secure sandbox environment."""
        try:
            # Create security context
            context = await self._create_security_context(plugin.metadata)

            # Validate configuration against security policies
            await self._validate_config_security(config, plugin.metadata)

            # Execute initialization in sandbox
            async with self._secure_execution_context(context):
                success = await plugin.initialize(config)

            if success:
                self._active_plugins[plugin.metadata.plugin_id] = plugin
                self._security_contexts[plugin.metadata.plugin_id] = context

            return success

        except Exception as e:
            logger.error(f"Plugin initialization failed in sandbox: {e}")
            return False

    async def execute_plugin_hook(self, plugin_id: str, hook_name: str, *args, **kwargs) -> Any:
        """Execute plugin hook in secure environment."""
        if plugin_id not in self._active_plugins:
            raise ValueError(f"Plugin {plugin_id} not active")

        plugin = self._active_plugins[plugin_id]
        context = self._security_contexts[plugin_id]

        # Execute hook in sandbox
        async with self._secure_execution_context(context):
            result = await plugin.execute_hook(hook_name, *args, **kwargs)

        return result
```

## Configuration

### Environment Variables
```bash
# Plugin directories
PLUGINS_DIR=./plugins
PLUGIN_DATA_DIR=./data/plugins

# Security settings
PLUGIN_SECURITY_LEVEL=standard
PLUGIN_SANDBOX_ENABLED=true
PLUGIN_TIMEOUT_SECONDS=30

# Marketplace settings
PLUGIN_MARKETPLACE_URL=https://api.emailintelligence.dev/plugins
PLUGIN_AUTO_UPDATE=false
PLUGIN_UPDATE_CHECK_INTERVAL=86400

# Resource limits
PLUGIN_MAX_MEMORY_MB=100
PLUGIN_MAX_EXECUTION_TIME=10
PLUGIN_MAX_FILE_SIZE_MB=50
```

### Runtime Configuration
```python
from src.core.plugin_manager import PluginManager
from src.core.plugin_base import PluginSecurityLevel

# Initialize plugin manager with custom configuration
plugin_manager = PluginManager(
    plugins_dir=Path("./custom_plugins")
)

# Configure security settings
plugin_manager.security_level = PluginSecurityLevel.SANDBOXED
plugin_manager.enable_sandbox = True
plugin_manager.max_execution_time = 15  # seconds

# Configure marketplace
plugin_manager.marketplace_url = "https://custom-marketplace.com/api/plugins"
plugin_manager.auto_update_enabled = False

# Initialize
await plugin_manager.initialize()
```

### Plugin Directory Structure
```
plugins/
├── example_plugin/
│   ├── __init__.py          # Plugin entry point
│   ├── plugin.json          # Plugin metadata
│   ├── requirements.txt     # Python dependencies
│   ├── config/
│   │   └── default.json     # Default configuration
│   └── data/                # Plugin-specific data
│       └── cache/
│       └── logs/
├── security_plugin/
│   ├── __init__.py
│   └── plugin.json
└── marketplace_cache.json   # Cached marketplace data
```

## Usage Examples

### Basic Plugin Management

```python
import asyncio
from src.core.plugin_manager import PluginManager

async def main():
    # Initialize plugin manager
    manager = PluginManager()
    await manager.initialize()

    # List installed plugins
    plugins = await manager.list_plugins()
    print(f"Installed plugins: {len(plugins)}")

    # Install a plugin from marketplace
    result = await manager.install_plugin("email_filter_plugin", "1.0.0")
    print(f"Plugin installed: {result}")

    # Load the plugin
    load_result = await manager.load_plugin("email_filter_plugin")
    print(f"Plugin loaded: {load_result}")

    # Execute plugin hook
    filtered_email = await manager.execute_plugin_hook(
        "email_filter_plugin",
        "filter_email",
        email_content="Spam content here"
    )
    print(f"Filtered email: {filtered_email}")

    # Unload plugin
    await manager.unload_plugin("email_filter_plugin")
    print("Plugin unloaded")

asyncio.run(main())
```

### Creating a Custom Plugin

```python
# plugin_example/__init__.py
from src.core.plugin_base import PluginInterface, PluginMetadata, PluginSecurityLevel
import logging

class EmailFilterPlugin(PluginInterface):
    """Example plugin that filters spam emails."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._filter_rules = []

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            plugin_id="email_filter_plugin",
            name="Email Filter Plugin",
            version="1.0.0",
            author="EmailIntelligence Team",
            description="Advanced email filtering and spam detection",
            license="MIT",
            homepage="https://github.com/emailintelligence/plugins",
            dependencies=["scikit-learn>=1.0.0"],
            permissions=["read:emails", "write:emails"],
            security_level=PluginSecurityLevel.STANDARD,
            tags=["filtering", "spam", "security"]
        )

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        try:
            self._filter_rules = config.get("filter_rules", [])
            self.logger.info("Email filter plugin initialized")
            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False

    async def shutdown(self) -> bool:
        """Shutdown the plugin and cleanup resources."""
        self._filter_rules = []
        self.logger.info("Email filter plugin shutdown")
        return True

    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities."""
        return [
            "email_filtering",
            "spam_detection",
            "content_analysis"
        ]

    def get_required_permissions(self) -> List[str]:
        """Return list of required permissions."""
        return ["read:emails", "write:emails"]

    async def execute_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute a plugin hook."""
        if hook_name == "filter_email":
            return await self._filter_email(kwargs.get("email_content", ""))
        elif hook_name == "analyze_content":
            return await self._analyze_content(kwargs.get("content", ""))
        else:
            raise ValueError(f"Unknown hook: {hook_name}")

    async def _filter_email(self, content: str) -> Dict[str, Any]:
        """Filter email content for spam."""
        # Simple spam detection logic
        spam_indicators = ["lottery", "winner", "free money", "urgent"]
        spam_score = sum(1 for indicator in spam_indicators
                        if indicator.lower() in content.lower())

        is_spam = spam_score > 2

        return {
            "is_spam": is_spam,
            "spam_score": spam_score,
            "filtered_content": "[FILTERED]" if is_spam else content
        }

    async def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze email content."""
        return {
            "word_count": len(content.split()),
            "character_count": len(content),
            "sentiment_score": 0.5,  # Placeholder
            "language": "en"
        }

# Factory function for plugin creation
def create_plugin() -> PluginInterface:
    """Create and return plugin instance."""
    return EmailFilterPlugin()
```

### Plugin Configuration

```json
{
  "email_filter_plugin": {
    "enabled": true,
    "config": {
      "filter_rules": [
        {
          "type": "keyword",
          "pattern": "lottery|winner",
          "action": "flag_spam"
        },
        {
          "type": "sender_domain",
          "pattern": "@suspicious.com",
          "action": "block"
        }
      ],
      "sensitivity": "medium",
      "log_filtered_emails": true
    }
  }
}
```

## API Reference

### Plugin Management Endpoints

#### List Plugins
**GET** `/api/plugins/`

Returns a list of all installed plugins with their status and metadata.

**Parameters:**
- `status` (str, optional): Filter by plugin status (installed, enabled, disabled, error)
- `security_level` (str, optional): Filter by security level
- `include_metadata` (bool, optional): Include full plugin metadata (default: true)

**Response:**
```json
[
  {
    "id": "email_filter_plugin",
    "name": "Email Filter Plugin",
    "version": "1.0.0",
    "author": "EmailIntelligence Team",
    "description": "Advanced email filtering and spam detection",
    "status": "enabled",
    "security_level": "standard",
    "loaded": true,
    "loaded_at": 1638460000.0,
    "capabilities": ["email_filtering", "spam_detection"]
  }
]
```

#### Get Plugin Details
**GET** `/api/plugins/{plugin_id}`

Returns detailed information about a specific plugin.

**Response:**
```json
{
  "id": "email_filter_plugin",
  "metadata": {
    "plugin_id": "email_filter_plugin",
    "name": "Email Filter Plugin",
    "version": "1.0.0",
    "author": "EmailIntelligence Team",
    "description": "Advanced email filtering and spam detection",
    "license": "MIT",
    "dependencies": ["scikit-learn>=1.0.0"],
    "permissions": ["read:emails", "write:emails"],
    "security_level": "standard",
    "tags": ["filtering", "spam", "security"],
    "created_at": 1638360000.0
  },
  "status": "enabled",
  "loaded_at": 1638460000.0,
  "config": {
    "filter_rules": [...],
    "sensitivity": "medium"
  },
  "capabilities": ["email_filtering", "spam_detection"],
  "hooks": ["filter_email", "analyze_content"]
}
```

#### Install Plugin
**POST** `/api/plugins/install`

Installs a plugin from the marketplace.

**Request Body:**
```json
{
  "plugin_id": "email_filter_plugin",
  "version": "1.0.0"
}
```

**Response:**
```json
{
  "plugin_id": "email_filter_plugin",
  "status": "installed",
  "version": "1.0.0",
  "capabilities": ["email_filtering", "spam_detection"]
}
```

#### Load Plugin
**POST** `/api/plugins/{plugin_id}/load`

Loads and enables a plugin.

**Request Body:**
```json
{
  "config": {
    "filter_rules": [...],
    "sensitivity": "high"
  }
}
```

**Response:**
```json
{
  "plugin_id": "email_filter_plugin",
  "status": "loaded",
  "capabilities": ["email_filtering", "spam_detection"],
  "security_level": "standard"
}
```

#### Execute Plugin Hook
**POST** `/api/plugins/{plugin_id}/hooks/{hook_name}`

Executes a specific plugin hook with parameters.

**Request Body:**
```json
{
  "email_content": "Check out this amazing offer!",
  "metadata": {
    "sender": "spam@example.com",
    "subject": "You won a lottery!"
  }
}
```

**Response:**
```json
{
  "hook_name": "filter_email",
  "result": {
    "is_spam": true,
    "spam_score": 3,
    "filtered_content": "[FILTERED]"
  },
  "execution_time_ms": 45
}
```

#### Unload Plugin
**POST** `/api/plugins/{plugin_id}/unload`

Unloads and disables a plugin.

**Response:**
```json
{
  "plugin_id": "email_filter_plugin",
  "status": "unloaded"
}
```

#### Update Plugin Configuration
**PUT** `/api/plugins/{plugin_id}/config`

Updates plugin configuration.

**Request Body:**
```json
{
  "config": {
    "sensitivity": "low",
    "log_filtered_emails": false
  }
}
```

**Response:**
```json
{
  "plugin_id": "email_filter_plugin",
  "status": "configuration_updated",
  "config": {
    "sensitivity": "low",
    "log_filtered_emails": false
  }
}
```

### Marketplace Endpoints

#### Get Marketplace Plugins
**GET** `/api/plugins/marketplace`

Returns available plugins from the marketplace.

**Parameters:**
- `category` (str, optional): Filter by category (filtering, analysis, etc.)
- `tags` (List[str], optional): Filter by tags
- `limit` (int, optional): Maximum number of results (default: 50)

**Response:**
```json
[
  {
    "plugin_id": "email_filter_plugin",
    "name": "Email Filter Plugin",
    "version": "1.0.0",
    "author": "EmailIntelligence Team",
    "description": "Advanced email filtering and spam detection",
    "download_url": "https://api.emailintelligence.dev/plugins/email_filter_plugin-1.0.0.zip",
    "checksum": "a1b2c3d4...",
    "tags": ["filtering", "spam", "security"],
    "rating": 4.5,
    "downloads": 1250,
    "last_updated": 1638460000.0
  }
]
```

## Performance Considerations

### Resource Management
- **Memory Limits:** Configurable per-plugin memory limits
- **Execution Timeouts:** Prevent long-running plugin operations
- **Concurrent Execution:** Controlled parallel plugin execution
- **Resource Cleanup:** Automatic cleanup of plugin resources

### Optimization Strategies
```python
# Plugin performance configuration
performance_config = {
    "max_concurrent_plugins": 5,
    "plugin_timeout_seconds": 30,
    "memory_limit_mb": 100,
    "cpu_limit_percent": 50,
    "io_timeout_seconds": 10
}

# Caching and optimization
plugin_cache = {
    "enabled": True,
    "ttl_seconds": 3600,
    "max_cache_size_mb": 50,
    "compression_enabled": True
}
```

## Security Considerations

### Plugin Sandboxing
- **Security Levels:** Trusted, Standard, Sandboxed execution
- **Permission System:** Granular permission controls
- **Resource Limits:** Memory, CPU, and I/O restrictions
- **Code Validation:** Plugin code validation before execution

### Safe Plugin Development
```python
# Security best practices for plugin development
class SecurePlugin(PluginInterface):
    """Example of secure plugin implementation."""

    def get_required_permissions(self) -> List[str]:
        """Explicitly declare required permissions."""
        return [
            "read:emails",      # Read email data
            "write:logs",       # Write to logs
            # Avoid broad permissions like "read:all"
        ]

    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Secure initialization with input validation."""
        # Validate configuration
        required_keys = ["api_key", "timeout"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config: {key}")

        # Sanitize inputs
        self.api_key = self._sanitize_api_key(config["api_key"])
        self.timeout = min(config.get("timeout", 30), 300)  # Max 5 minutes

        return True

    def _sanitize_api_key(self, api_key: str) -> str:
        """Sanitize API key input."""
        if not isinstance(api_key, str) or len(api_key) < 10:
            raise ValueError("Invalid API key format")
        return api_key.strip()
```

## Troubleshooting

### Common Issues

#### Plugin Loading Failures
```
Symptoms: Plugin fails to load with import errors
```

**Diagnosis:**
```python
# Check plugin structure
plugin_dir = Path("./plugins/email_filter_plugin")
print(f"Plugin dir exists: {plugin_dir.exists()}")
print(f"__init__.py exists: {(plugin_dir / '__init__.py').exists()}")
print(f"plugin.json exists: {(plugin_dir / 'plugin.json').exists()}")

# Check imports
try:
    import sys
    sys.path.append(str(plugin_dir))
    import email_filter_plugin
    print("Plugin imports successfully")
except ImportError as e:
    print(f"Import error: {e}")
```

**Solutions:**
```python
# Fix plugin structure
plugin_structure = {
    "email_filter_plugin": {
        "__init__.py": "Plugin entry point",
        "plugin.json": "Metadata file",
        "requirements.txt": "Dependencies"
    }
}

# Reinstall plugin
await plugin_manager.reinstall_plugin("email_filter_plugin")

# Check dependencies
await plugin_manager.validate_plugin_dependencies("email_filter_plugin")
```

#### Permission Denied Errors
```
Symptoms: Plugin operations fail with permission errors
```

**Diagnosis:**
```python
# Check plugin permissions
plugin = await plugin_manager.get_plugin("email_filter_plugin")
permissions = plugin.get_required_permissions()
print(f"Required permissions: {permissions}")

# Check current user permissions
current_permissions = await security_manager.get_current_permissions()
print(f"Current permissions: {current_permissions}")

# Find missing permissions
missing = set(permissions) - set(current_permissions)
print(f"Missing permissions: {missing}")
```

**Solutions:**
```python
# Grant missing permissions
for permission in missing:
    await security_manager.grant_permission("email_filter_plugin", permission)

# Update plugin configuration
await plugin_manager.update_plugin_config("email_filter_plugin", {
    "permissions": list(set(permissions) | set(current_permissions))
})

# Restart plugin
await plugin_manager.reload_plugin("email_filter_plugin")
```

#### Marketplace Connection Issues
```
Symptoms: Cannot install plugins from marketplace
```

**Diagnosis:**
```python
# Test marketplace connectivity
import requests
try:
    response = requests.get("https://api.emailintelligence.dev/plugins", timeout=10)
    print(f"Marketplace status: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

# Check proxy settings
import os
proxy = os.environ.get("HTTPS_PROXY")
print(f"Proxy configured: {proxy is not None}")
```

**Solutions:**
```python
# Configure marketplace URL
plugin_manager.marketplace_url = "https://api.emailintelligence.dev/plugins"

# Set proxy if needed
plugin_manager.proxy_config = {
    "https": "http://proxy.company.com:8080"
}

# Test connection
await plugin_manager.test_marketplace_connection()

# Clear marketplace cache
await plugin_manager.clear_marketplace_cache()
```

### Debug Mode

```python
# Enable plugin debugging
import logging

# Set debug logging for plugin system
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable plugin manager debugging
plugin_manager.debug_mode = True
plugin_manager.verbose_logging = True

# Debug specific plugin
await plugin_manager.enable_plugin_debugging("email_filter_plugin")

# Monitor plugin execution
with plugin_manager.debug_context("email_filter_plugin"):
    result = await plugin_manager.execute_plugin_hook(
        "email_filter_plugin", "filter_email", email_content="test"
    )
    print(f"Debug result: {result}")
```

## Development Notes

### Testing

```bash
# Run plugin management tests
pytest tests/core/test_plugin_manager.py -v
pytest tests/core/test_plugin_base.py -v
pytest tests/core/test_plugin_routes.py -v

# Test plugin security
pytest tests/security/test_plugin_sandbox.py -v

# Integration tests
pytest tests/integration/test_plugin_system.py -v

# Marketplace tests
pytest tests/integration/test_plugin_marketplace.py -v
```

### Plugin Development Guidelines

#### Structure Requirements
```python
# Required plugin structure
plugin_template = {
    "plugin_directory/": {
        "__init__.py": "Main plugin class implementing PluginInterface",
        "plugin.json": "Plugin metadata and configuration",
        "requirements.txt": "Python dependencies",
        "README.md": "Plugin documentation",
        "tests/": "Plugin-specific tests",
        "config/": "Default configuration files",
        "data/": "Plugin data storage"
    }
}
```

#### Code Quality Standards
```python
# Plugin development best practices
class PluginDevelopmentStandards:
    """Standards for plugin development."""

    # Error handling
    async def robust_operation(self) -> Any:
        """Always include proper error handling."""
        try:
            result = await self._perform_operation()
            return result
        except Exception as e:
            self.logger.error(f"Operation failed: {e}")
            await self._cleanup_partial_state()
            raise PluginError(f"Operation failed: {str(e)}") from e

    # Resource management
    async def __aenter__(self):
        """Support async context manager."""
        await self.initialize(self.config)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure proper cleanup."""
        await self.shutdown()

    # Logging standards
    def log_operation(self, operation: str, details: dict):
        """Consistent logging format."""
        self.logger.info(f"Plugin operation: {operation}", extra={
            "plugin_id": self.metadata.plugin_id,
            "operation": operation,
            "details": details
        })
```

### Contributing

1. **Plugin Submission:** Submit plugins to marketplace repository
2. **Code Review:** All plugins undergo security and code review
3. **Documentation:** Include comprehensive README and examples
4. **Testing:** Provide unit and integration tests
5. **Licensing:** Compatible open source license required

### Version Compatibility

- **Framework Version:** Compatible with EmailIntelligence v2.0+
- **Python Version:** 3.11+ required
- **Plugin API Version:** v1.0 (current)
- **Security Framework:** Sandboxed execution environment

## Migration Guide

### From Legacy Plugin System

#### API Changes
```python
# Legacy plugin loading
from old_plugin_system import PluginLoader
loader = PluginLoader()
plugin = loader.load("my_plugin")

# New plugin system
from src.core.plugin_manager import PluginManager
manager = PluginManager()
await manager.initialize()
result = await manager.load_plugin("my_plugin")
```

#### Configuration Migration
```python
# Old plugin config
plugin_config = {
    "name": "My Plugin",
    "version": "1.0.0",
    "enabled": True
}

# New plugin metadata
plugin_metadata = PluginMetadata(
    plugin_id="my_plugin",
    name="My Plugin",
    version="1.0.0",
    author="Developer Name",
    description="Plugin description",
    security_level=PluginSecurityLevel.STANDARD
)
```

#### Security Updates
```python
# Old security (no sandboxing)
plugin.execute_function(data)

# New security (sandboxed execution)
result = await plugin_manager.execute_plugin_hook(
    "my_plugin", "execute_function", data=data
)
```

## Changelog

### Version 2.0.0
- **Added:** Comprehensive plugin management system
- **Added:** Security sandboxing with multiple trust levels
- **Added:** Plugin marketplace integration
- **Added:** RESTful API for plugin operations
- **Added:** Hook system for plugin extensibility
- **Added:** Comprehensive plugin lifecycle management

### Version 1.5.0
- **Added:** Plugin metadata validation
- **Added:** Security permission system
- **Improved:** Error handling and logging
- **Added:** Plugin configuration management

### Version 1.0.0
- **Added:** Basic plugin loading and execution
- **Added:** Plugin interface definition
- **Added:** Simple plugin registry

---

*Module Version: 2.0.0*
*Last Updated: 2025-10-31*
*API Version: v1*
*Security Levels: TRUSTED, STANDARD, SANDBOXED*
*Marketplace URL: https://api.emailintelligence.dev/plugins*
