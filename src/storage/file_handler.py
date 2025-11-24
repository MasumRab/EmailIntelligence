"""
File handling utilities for EmailIntelligence CLI

This module provides safe, consistent file operations, particularly for
JSON handling and UTF-8 encoding.
"""

import json
import aiofiles
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
from ..core.exceptions import StorageError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FileHandler:
    """
    Handles file operations with consistent encoding and error handling.
    """
    
    @staticmethod
    async def read_json(path: Union[str, Path]) -> Union[Dict[str, Any], List[Any]]:
        """
        Read JSON file asynchronously.
        
        Args:
            path: Path to the JSON file
            
        Returns:
            Parsed JSON data (dict or list)
            
        Raises:
            StorageError: If file cannot be read or parsed
        """
        path_obj = Path(path)
        try:
            if not path_obj.exists():
                raise FileNotFoundError(f"File not found: {path}")
                
            async with aiofiles.open(path_obj, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", path=str(path), error=str(e))
            raise StorageError(f"Invalid JSON in {path}: {str(e)}") from e
        except Exception as e:
            logger.error("Failed to read file", path=str(path), error=str(e))
            raise StorageError(f"Failed to read {path}: {str(e)}") from e

    @staticmethod
    async def write_json(
        path: Union[str, Path], 
        data: Any, 
        indent: int = 2,
        ensure_dir: bool = True
    ) -> None:
        """
        Write data to JSON file asynchronously.
        
        Args:
            path: Target file path
            data: Data to serialize
            indent: JSON indentation level
            ensure_dir: Create parent directories if missing
            
        Raises:
            StorageError: If file cannot be written
        """
        path_obj = Path(path)
        try:
            if ensure_dir:
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                
            async with aiofiles.open(path_obj, mode='w', encoding='utf-8') as f:
                content = json.dumps(data, indent=indent, ensure_ascii=False, default=str)
                await f.write(content)
        except Exception as e:
            logger.error("Failed to write file", path=str(path), error=str(e))
            raise StorageError(f"Failed to write {path}: {str(e)}") from e

    @staticmethod
    async def read_text(path: Union[str, Path]) -> str:
        """Read text file asynchronously."""
        try:
            async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            raise StorageError(f"Failed to read {path}: {str(e)}") from e

    @staticmethod
    async def write_text(
        path: Union[str, Path], 
        content: str,
        ensure_dir: bool = True
    ) -> None:
        """Write text file asynchronously."""
        path_obj = Path(path)
        try:
            if ensure_dir:
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                
            async with aiofiles.open(path_obj, mode='w', encoding='utf-8') as f:
                await f.write(content)
        except Exception as e:
            raise StorageError(f"Failed to write {path}: {str(e)}") from e
