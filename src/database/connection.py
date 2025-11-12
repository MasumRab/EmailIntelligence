"""
Neo4j database connection and session management
"""

import logging
from typing import Optional, Dict, Any, List
from neo4j import AsyncDriver, GraphDatabase
from contextlib import asynccontextmanager
import structlog
from ..config.settings import settings

logger = structlog.get_logger()


class Neo4jConnectionManager:
    """Neo4j connection manager with connection pooling and error handling"""
    
    def __init__(self):
        self._driver: Optional[AsyncDriver] = None
        self._connection_pool = {}
    
    async def connect(self) -> None:
        """Initialize Neo4j connection"""
        try:
            self._driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
                max_connection_lifetime=300,
                max_connection_pool_size=50,
                connection_acquisition_timeout=60
            )
            
            # Test connection
            await self._driver.verify_connectivity()
            logger.info("Neo4j connection established", uri=settings.neo4j_uri)
            
        except Exception as e:
            logger.error("Failed to connect to Neo4j", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Close Neo4j connection"""
        if self._driver:
            await self._driver.close()
            logger.info("Neo4j connection closed")
    
    @asynccontextmanager
    async def get_session(self, database: str = "neo4j"):
        """Get async session with proper error handling"""
        if not self._driver:
            await self.connect()
        
        session = self._driver.session(database=database)
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()
    
    async def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None,
        database: str = "neo4j"
    ) -> List[Dict[str, Any]]:
        """Execute Cypher query and return results"""
        async with self.get_session(database) as session:
            try:
                result = await session.run(query, parameters or {})
                records = await result.data()
                logger.debug("Query executed", query=query, records=len(records))
                return records
            except Exception as e:
                logger.error("Query execution failed", query=query, error=str(e))
                raise
    
    async def execute_write_transaction(
        self, 
        tx_function,
        *args, 
        database: str = "neo4j"
    ) -> Any:
        """Execute write transaction with retry logic"""
        async with self.get_session(database) as session:
            try:
                return await session.execute_write(tx_function, *args)
            except Exception as e:
                logger.error("Write transaction failed", error=str(e))
                raise
    
    async def health_check(self) -> bool:
        """Check Neo4j connection health"""
        try:
            async with self.get_session() as session:
                result = await session.run("RETURN 1 as test")
                record = await result.single()
                return record["test"] == 1
        except Exception as e:
            logger.error("Neo4j health check failed", error=str(e))
            return False


# Global connection manager instance
connection_manager = Neo4jConnectionManager()


# Utility functions for common operations
async def create_constraint(constraint_type: str, property_name: str, node_label: str) -> None:
    """Create database constraint"""
    query = f"""
    CREATE CONSTRAINT {constraint_type}_{node_label}_{property_name} 
    IF NOT EXISTS 
    FOR (n:{node_label}) 
    REQUIRE n.{property_name} IS UNIQUE
    """
    await connection_manager.execute_query(query)
    logger.info("Constraint created", type=constraint_type, property=property_name, label=node_label)


async def create_index(index_name: str, property_name: str, node_label: str) -> None:
    """Create database index"""
    query = f"""
    CREATE INDEX {index_name}_{node_label}_{property_name} 
    IF NOT EXISTS 
    FOR (n:{node_label}) 
    ON (n.{property_name})
    """
    await connection_manager.execute_query(query)
    logger.info("Index created", name=index_name, property=property_name, label=node_label)


async def initialize_database_schema() -> None:
    """Initialize database schema with constraints and indexes"""
    logger.info("Initializing database schema")
    
    # Create constraints for unique identifiers
    constraints = [
        ("unique", "id", "PullRequest"),
        ("unique", "id", "Commit"),
        ("unique", "id", "File"),
        ("unique", "id", "Developer"),
        ("unique", "id", "Issue"),
        ("unique", "id", "Conflict"),
        ("unique", "id", "PRResolution"),
        ("unique", "id", "ConflictResolution"),
        ("unique", "id", "AIAnalysis"),
    ]
    
    for constraint_type, property_name, node_label in constraints:
        try:
            await create_constraint(constraint_type, property_name, node_label)
        except Exception as e:
            logger.warning("Constraint creation failed", 
                         type=constraint_type, property=property_name,
                         label=node_label, error=str(e))
    
    # Create indexes for performance
    indexes = [
        ("pr_status", "status", "PullRequest"),
        ("pr_created", "created_at", "PullRequest"),
        ("conflict_severity", "severity", "Conflict"),
        ("developer_expertise", "expertise", "Developer"),
        ("file_language", "language", "File"),
    ]
    
    for index_name, property_name, node_label in indexes:
        try:
            await create_index(index_name, property_name, node_label)
        except Exception as e:
            logger.warning("Index creation failed", 
                         name=index_name, property=property_name,
                         label=node_label, error=str(e))
    
    logger.info("Database schema initialization completed")