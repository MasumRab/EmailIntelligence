"""
API Routes for Plugin Management.

This module provides REST API endpoints for managing plugins,
including installation, configuration, and marketplace integration.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field

from .plugin_manager import PluginManager
from .plugin_base import PluginSecurityLevel

logger = logging.getLogger(__name__)

# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None

async def get_plugin_manager() -> PluginManager:
    """Dependency to get the plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
        await _plugin_manager.initialize()
    return _plugin_manager

# Pydantic models for API
class PluginInfo(BaseModel):
    """Plugin information response."""
    id: str
    name: str
    version: str
    author: str
    description: str
    status: str
    security_level: str
    loaded: bool
    loaded_at: Optional[float] = None
    capabilities: Optional[List[str]] = None

class PluginInstallation(BaseModel):
    """Plugin installation request."""
    plugin_id: str = Field(..., description="Plugin ID to install")
    version: Optional[str] = Field(None, description="Specific version to install")

class PluginConfiguration(BaseModel):
    """Plugin configuration update."""
    config: dict = Field(..., description="Configuration updates")

class MarketplacePlugin(BaseModel):
    """Marketplace plugin information."""
    id: str
    name: str
    version: str
    author: str
    description: str
    tags: List[str]
    rating: float
    downloads: int
    installed: bool
    installed_version: Optional[str] = None
    update_available: bool = False

class SystemStatus(BaseModel):
    """Plugin system status."""
    total_plugins: int
    loaded_plugins: int
    enabled_plugins: int
    marketplace_available: bool
    background_tasks_active: int
    plugins_dir: str
    security_levels: dict

# Create router
router = APIRouter(prefix="/api/plugins", tags=["Plugin Management"])

@router.get("/", response_model=List[PluginInfo])
async def list_plugins(
    manager: PluginManager = Depends(get_plugin_manager)
):
    """List all installed plugins with their status."""
    try:
        plugins = manager.list_plugins()
        return [PluginInfo(**plugin) for plugin in plugins]
    except Exception as e:
        logger.error(f"Error listing plugins: {e}")
        raise HTTPException(status_code=500, detail="Failed to list plugins")

@router.get("/{plugin_id}", response_model=PluginInfo)
async def get_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Get detailed information about a specific plugin."""
    try:
        plugin_info = await manager.get_plugin_info(plugin_id)
        if not plugin_info:
            raise HTTPException(status_code=404, detail=f"Plugin {plugin_id} not found")
        return PluginInfo(**plugin_info)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get plugin information")

@router.post("/{plugin_id}/load")
async def load_plugin(
    plugin_id: str,
    background_tasks: BackgroundTasks,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Load a plugin into memory."""
    try:
        background_tasks.add_task(manager.load_plugin, plugin_id)
        return {"message": f"Loading plugin {plugin_id}", "status": "initiated"}
    except Exception as e:
        logger.error(f"Error initiating load for plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate plugin loading")

@router.post("/{plugin_id}/unload")
async def unload_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Unload a plugin from memory."""
    try:
        success = await manager.unload_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=400, detail=f"Failed to unload plugin {plugin_id}")
        return {"message": f"Plugin {plugin_id} unloaded successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unloading plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unload plugin")

@router.post("/{plugin_id}/enable")
async def enable_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Enable a plugin."""
    try:
        success = await manager.enable_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=400, detail=f"Failed to enable plugin {plugin_id}")
        return {"message": f"Plugin {plugin_id} enabled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to enable plugin")

@router.post("/{plugin_id}/disable")
async def disable_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Disable a plugin."""
    try:
        success = await manager.disable_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=400, detail=f"Failed to disable plugin {plugin_id}")
        return {"message": f"Plugin {plugin_id} disabled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to disable plugin")

@router.post("/install")
async def install_plugin(
    installation: PluginInstallation,
    background_tasks: BackgroundTasks,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Install a plugin from the marketplace."""
    try:
        background_tasks.add_task(
            manager.install_plugin,
            installation.plugin_id,
            installation.version
        )
        version_msg = f" version {installation.version}" if installation.version else ""
        return {
            "message": f"Installing plugin {installation.plugin_id}{version_msg}",
            "status": "initiated"
        }
    except Exception as e:
        logger.error(f"Error initiating install for plugin {installation.plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate plugin installation")

@router.delete("/{plugin_id}")
async def uninstall_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Uninstall a plugin completely."""
    try:
        success = await manager.uninstall_plugin(plugin_id)
        if not success:
            raise HTTPException(status_code=400, detail=f"Failed to uninstall plugin {plugin_id}")
        return {"message": f"Plugin {plugin_id} uninstalled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uninstalling plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to uninstall plugin")

@router.post("/{plugin_id}/update")
async def update_plugin(
    plugin_id: str,
    background_tasks: BackgroundTasks,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Update a plugin to the latest version."""
    try:
        background_tasks.add_task(manager.update_plugin, plugin_id)
        return {"message": f"Updating plugin {plugin_id}", "status": "initiated"}
    except Exception as e:
        logger.error(f"Error initiating update for plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate plugin update")

@router.get("/{plugin_id}/validate")
async def validate_plugin(
    plugin_id: str,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Validate a plugin's integrity and security."""
    try:
        validation = await manager.validate_plugin(plugin_id)
        return validation
    except Exception as e:
        logger.error(f"Error validating plugin {plugin_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate plugin")

@router.put("/{plugin_id}/config")
async def update_plugin_config(
    plugin_id: str,
    config_update: PluginConfiguration,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Update configuration for a plugin."""
    # This would need implementation in the plugin manager
    raise HTTPException(status_code=501, detail="Plugin configuration update not yet implemented")

@router.get("/marketplace/", response_model=List[MarketplacePlugin])
async def get_marketplace_plugins(
    refresh: bool = Query(False, description="Force refresh marketplace cache"),
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Get available plugins from the marketplace."""
    try:
        plugins = await manager.get_marketplace_plugins(refresh=refresh)
        return [MarketplacePlugin(**plugin) for plugin in plugins]
    except Exception as e:
        logger.error(f"Error getting marketplace plugins: {e}")
        raise HTTPException(status_code=500, detail="Failed to get marketplace plugins")

@router.get("/status", response_model=SystemStatus)
async def get_plugin_system_status(
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Get comprehensive plugin system status."""
    try:
        return SystemStatus(**manager.get_system_status())
    except Exception as e:
        logger.error(f"Error getting plugin system status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system status")

@router.post("/{plugin_id}/execute/{method_name}")
async def execute_plugin_method(
    plugin_id: str,
    method_name: str,
    params: dict = None,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Execute a method on a loaded plugin (advanced feature)."""
    try:
        if params is None:
            params = {}

        # This is a security-sensitive operation
        # In production, this should have strict access controls
        result = await manager.execute_plugin_method(
            plugin_id, method_name, **params
        )

        return {"result": result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing plugin method {plugin_id}.{method_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute plugin method")

# Hook system endpoints
@router.get("/hooks/registered")
async def get_registered_hooks(
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Get information about registered hooks."""
    try:
        hook_system = manager.get_hook_system()
        registered_hooks = hook_system.get_registered_hooks()
        return {"hooks": registered_hooks}
    except Exception as e:
        logger.error(f"Error getting registered hooks: {e}")
        raise HTTPException(status_code=500, detail="Failed to get registered hooks")

@router.post("/hooks/trigger")
async def trigger_hook(
    hook_name: str,
    data: dict = None,
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Trigger a hook manually (for testing/debugging)."""
    try:
        if data is None:
            data = {}

        hook_system = manager.get_hook_system()
        results = await hook_system.trigger_hook(hook_name, **data)

        return {
            "hook_name": hook_name,
            "results_count": len(results),
            "results": results
        }

    except Exception as e:
        logger.error(f"Error triggering hook {hook_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger hook")

# Security endpoints
@router.get("/security/check")
async def check_security_sandbox(
    module_name: str = Query(..., description="Module name to check"),
    security_level: PluginSecurityLevel = Query(PluginSecurityLevel.STANDARD, description="Security level"),
    manager: PluginManager = Depends(get_plugin_manager)
):
    """Check if a module import is allowed for a security level."""
    try:
        sandbox = manager.get_security_sandbox()
        allowed = sandbox.validate_import(module_name, security_level)

        return {
            "module": module_name,
            "security_level": security_level.value,
            "allowed": allowed
        }

    except Exception as e:
        logger.error(f"Error checking security sandbox: {e}")
        raise HTTPException(status_code=500, detail="Failed to check security sandbox")
