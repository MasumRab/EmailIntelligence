"""
Data access layer for graph database operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import structlog
from ..database.connection import connection_manager
from ..models.graph_entities import (
    PullRequest, Conflict,
    PRStatus, ConflictType, ConflictSeverity
)

logger = structlog.get_logger()


class PRDataAccess:
    """Data access for Pull Request operations"""
    
    async def get_pr(self, pr_id: str) -> Optional[PullRequest]:
        """Get pull request by ID"""
        query = """
        MATCH (pr:PullRequest {id: $pr_id})
        OPTIONAL MATCH (pr)-[:HAS_CONFLICT]->(conflict:Conflict)
        RETURN pr, collect(conflict) as conflicts
        """
        records = await connection_manager.execute_query(query, {"pr_id": pr_id})
        if not records:
            return None
        
        record = records[0]
        pr_data = record["pr"]
        conflict_data = record["conflicts"]
        
        return PullRequest(
            id=pr_data["id"],
            title=pr_data["title"],
            description=pr_data.get("description"),
            source_branch=pr_data["source_branch"],
            target_branch=pr_data["target_branch"],
            status=pr_data["status"],
            complexity=pr_data.get("complexity", 0.0),
            estimated_resolution_time=pr_data.get("estimated_resolution_time", 0),
            author_id=pr_data["author_id"],
            reviewer_ids=pr_data.get("reviewer_ids", []),
            file_ids=pr_data.get("file_ids", []),
            commit_ids=pr_data.get("commit_ids", []),
            conflict_ids=[c["id"] for c in conflict_data if c],
            created_at=pr_data["created_at"],
            updated_at=pr_data["updated_at"]
        )
    
    async def get_all_prs(
        self, 
        status: Optional[PRStatus] = None,
        author_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[PullRequest]:
        """Get all pull requests with optional filtering"""
        conditions = []
        params = {"limit": limit, "offset": offset}
        
        if status:
            conditions.append("pr.status = $status")
            params["status"] = status
        
        if author_id:
            conditions.append("pr.author_id = $author_id")
            params["author_id"] = author_id
        
        where_clause = " AND ".join(conditions) if conditions else ""
        query = f"""
        MATCH (pr:PullRequest)
        {'WHERE ' + where_clause if where_clause else ''}
        RETURN pr
        ORDER BY pr.created_at DESC
        SKIP $offset
        LIMIT $limit
        """
        
        records = await connection_manager.execute_query(query, params)
        return [
            PullRequest(
                id=record["pr"]["id"],
                title=record["pr"]["title"],
                description=record["pr"].get("description"),
                source_branch=record["pr"]["source_branch"],
                target_branch=record["pr"]["target_branch"],
                status=record["pr"]["status"],
                complexity=record["pr"].get("complexity", 0.0),
                estimated_resolution_time=record["pr"].get("estimated_resolution_time", 0),
                author_id=record["pr"]["author_id"],
                reviewer_ids=record["pr"].get("reviewer_ids", []),
                file_ids=record["pr"].get("file_ids", []),
                commit_ids=record["pr"].get("commit_ids", []),
                conflict_ids=record["pr"].get("conflict_ids", []),
                created_at=record["pr"]["created_at"],
                updated_at=record["pr"]["updated_at"]
            )
            for record in records
        ]
    
    async def create_pr(self, pr_data: Dict[str, Any]) -> PullRequest:
        """Create a new pull request"""
        query = """
        CREATE (pr:PullRequest {
            id: $id,
            title: $title,
            description: $description,
            source_branch: $source_branch,
            target_branch: $target_branch,
            status: $status,
            complexity: $complexity,
            estimated_resolution_time: $estimated_resolution_time,
            author_id: $author_id,
            reviewer_ids: $reviewer_ids,
            file_ids: $file_ids,
            commit_ids: $commit_ids,
            conflict_ids: $conflict_ids,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN pr
        """
        
        pr_data["status"] = pr_data.get("status", PRStatus.OPEN)
        pr_data["complexity"] = pr_data.get("complexity", 0.0)
        pr_data["estimated_resolution_time"] = pr_data.get("estimated_resolution_time", 0)
        pr_data["reviewer_ids"] = pr_data.get("reviewer_ids", [])
        pr_data["file_ids"] = pr_data.get("file_ids", [])
        pr_data["commit_ids"] = pr_data.get("commit_ids", [])
        pr_data["conflict_ids"] = pr_data.get("conflict_ids", [])
        pr_data["created_at"] = datetime.utcnow()
        pr_data["updated_at"] = datetime.utcnow()
        
        records = await connection_manager.execute_query(query, pr_data)
        record = records[0]
        
        return PullRequest(
            id=record["pr"]["id"],
            title=record["pr"]["title"],
            description=record["pr"].get("description"),
            source_branch=record["pr"]["source_branch"],
            target_branch=record["pr"]["target_branch"],
            status=record["pr"]["status"],
            complexity=record["pr"]["complexity"],
            estimated_resolution_time=record["pr"]["estimated_resolution_time"],
            author_id=record["pr"]["author_id"],
            reviewer_ids=record["pr"]["reviewer_ids"],
            file_ids=record["pr"]["file_ids"],
            commit_ids=record["pr"]["commit_ids"],
            conflict_ids=record["pr"]["conflict_ids"],
            created_at=record["pr"]["created_at"],
            updated_at=record["pr"]["updated_at"]
        )
    
    async def update_pr_status(self, pr_id: str, status: PRStatus) -> PullRequest:
        """Update pull request status"""
        query = """
        MATCH (pr:PullRequest {id: $pr_id})
        SET pr.status = $status, pr.updated_at = $updated_at
        RETURN pr
        """
        
        params = {
            "pr_id": pr_id,
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        records = await connection_manager.execute_query(query, params)
        if not records:
            raise ValueError(f"Pull request {pr_id} not found")
        
        return self.get_pr(pr_id)
    
    async def get_pr_conflicts(self, pr_id: str) -> List[Conflict]:
        """Get conflicts for a pull request"""
        query = """
        MATCH (pr:PullRequest {id: $pr_id})-[:HAS_CONFLICT]->(conflict:Conflict)
        RETURN conflict
        ORDER BY conflict.detected_at DESC
        """
        
        records = await connection_manager.execute_query(query, {"pr_id": pr_id})
        return [
            Conflict(
                id=record["conflict"]["id"],
                type=record["conflict"]["type"],
                severity=record["conflict"]["severity"],
                description=record["conflict"]["description"],
                detected_at=record["conflict"]["detected_at"],
                affected_file_ids=record["conflict"].get("affected_file_ids", []),
                affected_commit_ids=record["conflict"].get("affected_commit_ids", []),
                resolution_id=record["conflict"].get("resolution_id"),
                ai_analysis_id=record["conflict"].get("ai_analysis_id"),
                created_at=record["conflict"]["created_at"],
                updated_at=record["conflict"]["updated_at"]
            )
            for record in records
        ]
    
    async def get_pr_dependencies(self, pr_id: str) -> List[PullRequest]:
        """Get dependencies for a pull request (PRs that must be merged first)"""
        query = """
        MATCH (pr:PullRequest {id: $pr_id})-[:DEPENDS_ON]->(dependency:PullRequest)
        RETURN dependency
        ORDER BY dependency.created_at DESC
        """
        
        records = await connection_manager.execute_query(query, {"pr_id": pr_id})
        dependencies = []
        for record in records:
            dep_pr = await self.get_pr(record["dependency"]["id"])
            if dep_pr:
                dependencies.append(dep_pr)
        return dependencies
    
    async def calculate_pr_complexity(self, pr_id: str) -> float:
        """Calculate PR complexity based on graph analysis"""
        query = """
        MATCH (pr:PullRequest {id: $pr_id})
        OPTIONAL MATCH (pr)-[:HAS_CONFLICT]->(conflict:Conflict)
        OPTIONAL MATCH (pr)-[:MODIFIES]->(file:File)
        
        WITH pr, 
             count(conflict) as conflict_count,
             count(file) as file_count,
             sum(file.size) as total_file_size
        
        // Calculate complexity score
        RETURN 
            CASE 
                WHEN conflict_count > 5 THEN 0.9
                WHEN conflict_count > 2 THEN 0.6
                WHEN conflict_count > 0 THEN 0.3
                ELSE 0.1
            END +
            CASE 
                WHEN file_count > 20 THEN 0.3
                WHEN file_count > 10 THEN 0.2
                WHEN file_count > 5 THEN 0.1
                ELSE 0.0
            END +
            CASE 
                WHEN total_file_size > 100000 THEN 0.2
                WHEN total_file_size > 50000 THEN 0.1
                ELSE 0.0
            END as complexity
        """
        
        records = await connection_manager.execute_query(query, {"pr_id": pr_id})
        if not records:
            return 0.0
        
        return min(1.0, max(0.0, records[0]["complexity"]))


class ConflictDataAccess:
    """Data access for Conflict operations"""
    
    async def get_conflicts(
        self,
        severity: Optional[ConflictSeverity] = None,
        conflict_type: Optional[ConflictType] = None,
        limit: int = 50
    ) -> List[Conflict]:
        """Get conflicts with optional filtering"""
        conditions = []
        params = {"limit": limit}
        
        if severity:
            conditions.append("c.severity = $severity")
            params["severity"] = severity
        
        if conflict_type:
            conditions.append("c.type = $type")
            params["type"] = conflict_type
        
        where_clause = " AND ".join(conditions) if conditions else ""
        query = f"""
        MATCH (c:Conflict)
        {'WHERE ' + where_clause if where_clause else ''}
        RETURN c
        ORDER BY c.detected_at DESC
        LIMIT $limit
        """
        
        records = await connection_manager.execute_query(query, params)
        return [
            Conflict(
                id=record["c"]["id"],
                type=record["c"]["type"],
                severity=record["c"]["severity"],
                description=record["c"]["description"],
                detected_at=record["c"]["detected_at"],
                affected_file_ids=record["c"].get("affected_file_ids", []),
                affected_commit_ids=record["c"].get("affected_commit_ids", []),
                resolution_id=record["c"].get("resolution_id"),
                ai_analysis_id=record["c"].get("ai_analysis_id"),
                created_at=record["c"]["created_at"],
                updated_at=record["c"]["updated_at"]
            )
            for record in records
        ]


# Global data access instances
pr_dao = PRDataAccess()
conflict_dao = ConflictDataAccess()