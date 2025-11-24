"""
Metadata storage implementation for EmailIntelligence CLI

This module provides the concrete implementations of IMetadataStore,
supporting both Neo4j (graph) and File-based (JSON) storage.
"""

import json
from typing import Optional, Dict, Any
from datetime import datetime

from ..core.interfaces import IMetadataStore
from ..core.models import Conflict, AnalysisResult
from ..core.config import settings
from ..core.exceptions import StorageError
from ..utils.logger import get_logger
from .file_handler import FileHandler

# Import Neo4j connection manager (if available)
try:
    from ..database.connection import connection_manager
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

logger = get_logger(__name__)


class Neo4jMetadataStore(IMetadataStore):
    """
    Neo4j-backed metadata storage.
    Stores conflicts and analysis results as graph nodes.
    """
    
    def __init__(self):
        if not NEO4J_AVAILABLE:
            raise StorageError("Neo4j driver not available")
    
    async def save_conflict(self, conflict: Conflict) -> str:
        """Save conflict to Neo4j"""
        query = """
        MERGE (c:Conflict {id: $id})
        SET c += $props, c.updated_at = datetime()
        WITH c
        UNWIND $files as file_path
        MERGE (f:File {path: file_path})
        MERGE (c)-[:AFFECTS]->(f)
        """
        
        # Convert model to dict and handle datetimes
        props = conflict.model_dump(exclude={"file_paths", "blocks"})
        props["created_at"] = props["created_at"].isoformat()
        
        try:
            await connection_manager.execute_query(
                query,
                {
                    "id": conflict.id,
                    "props": props,
                    "files": conflict.file_paths
                }
            )
            return conflict.id
        except Exception as e:
            logger.error("Failed to save conflict to Neo4j", id=conflict.id, error=str(e))
            raise StorageError(f"Neo4j save failed: {str(e)}") from e

    async def get_conflict(self, conflict_id: str) -> Optional[Conflict]:
        """Retrieve conflict from Neo4j"""
        query = """
        MATCH (c:Conflict {id: $id})
        OPTIONAL MATCH (c)-[:AFFECTS]->(f:File)
        RETURN c as props, collect(f.path) as files
        """
        
        try:
            results = await connection_manager.execute_query(query, {"id": conflict_id})
            if not results:
                return None
                
            record = results[0]
            props = record["props"]
            props["file_paths"] = record["files"]
            
            return Conflict(**props)
        except Exception as e:
            logger.error("Failed to get conflict from Neo4j", id=conflict_id, error=str(e))
            raise StorageError(f"Neo4j get failed: {str(e)}") from e

    async def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis to Neo4j"""
        query = """
        MATCH (c:Conflict {id: $conflict_id})
        MERGE (a:Analysis {id: $id})
        SET a += $props, a.timestamp = datetime()
        MERGE (c)-[:HAS_ANALYSIS]->(a)
        """
        
        props = analysis.model_dump(exclude={"conflict_id"})
        props["timestamp"] = props["timestamp"].isoformat()
        
        # Serialize complex dicts
        props["impact_analysis"] = json.dumps(props["impact_analysis"])
        
        try:
            await connection_manager.execute_query(
                query,
                {
                    "conflict_id": analysis.conflict_id,
                    "id": f"analysis-{analysis.conflict_id}",
                    "props": props
                }
            )
            return analysis.conflict_id
        except Exception as e:
            logger.error("Failed to save analysis to Neo4j", id=analysis.conflict_id, error=str(e))
            raise StorageError(f"Neo4j save failed: {str(e)}") from e

    async def get_analysis(self, conflict_id: str) -> Optional[AnalysisResult]:
        """Retrieve analysis from Neo4j"""
        query = """
        MATCH (c:Conflict {id: $conflict_id})-[:HAS_ANALYSIS]->(a:Analysis)
        RETURN a as props
        """
        
        try:
            results = await connection_manager.execute_query(query, {"conflict_id": conflict_id})
            if not results:
                return None
                
            props = results[0]["props"]
            props["conflict_id"] = conflict_id
            
            # Deserialize complex dicts
            if isinstance(props.get("impact_analysis"), str):
                props["impact_analysis"] = json.loads(props["impact_analysis"])
            
            return AnalysisResult(**props)
        except Exception as e:
            logger.error("Failed to get analysis from Neo4j", id=conflict_id, error=str(e))
            raise StorageError(f"Neo4j get failed: {str(e)}") from e


class FileMetadataStore(IMetadataStore):
    """
    File-backed metadata storage (JSON).
    Useful for development or when Neo4j is unavailable.
    """
    
    def __init__(self):
        self.base_path = settings.get_metadata_path("")
    
    def _get_path(self, type_prefix: str, id: str) -> str:
        return str(self.base_path.parent / f"{type_prefix}-{id}.json")
    
    async def save_conflict(self, conflict: Conflict) -> str:
        path = self._get_path("conflict", conflict.id)
        data = conflict.model_dump(mode="json")
        await FileHandler.write_json(path, data)
        return conflict.id

    async def get_conflict(self, conflict_id: str) -> Optional[Conflict]:
        path = self._get_path("conflict", conflict_id)
        try:
            data = await FileHandler.read_json(path)
            return Conflict(**data)
        except FileNotFoundError:
            return None
        except Exception as e:
            raise StorageError(f"File get failed: {str(e)}") from e

    async def save_analysis(self, analysis: AnalysisResult) -> str:
        path = self._get_path("analysis", analysis.conflict_id)
        data = analysis.model_dump(mode="json")
        await FileHandler.write_json(path, data)
        return analysis.conflict_id

    async def get_analysis(self, conflict_id: str) -> Optional[AnalysisResult]:
        path = self._get_path("analysis", conflict_id)
        try:
            data = await FileHandler.read_json(path)
            return AnalysisResult(**data)
        except FileNotFoundError:
            return None
        except Exception as e:
            raise StorageError(f"File get failed: {str(e)}") from e


def get_metadata_store() -> IMetadataStore:
    """Factory to get the configured metadata store"""
    backend = settings.metadata_storage_backend.lower()
    
    if backend == "neo4j" and NEO4J_AVAILABLE:
        return Neo4jMetadataStore()
    elif backend == "neo4j" and not NEO4J_AVAILABLE:
        logger.warning("Neo4j configured but not available, falling back to file storage")
        return FileMetadataStore()
    else:
        return FileMetadataStore()
