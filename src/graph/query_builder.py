"""
Flexible graph query builder for complex traversals
"""

from typing import List, Dict, Optional, Any, Union
from enum import Enum
from datetime import datetime
import structlog
from dataclasses import dataclass
import json

from ...database.connection import connection_manager

logger = structlog.get_logger()


class QueryNodeType(Enum):
    """Types of nodes that can be queried"""
    PULL_REQUEST = "PullRequest"
    COMMIT = "Commit"
    FILE = "File"
    DEVELOPER = "Developer"
    CONFLICT = "Conflict"
    ISSUE = "Issue"
    PR_RESOLUTION = "PRResolution"
    CONFLICT_RESOLUTION = "ConflictResolution"
    AI_ANALYSIS = "AIAnalysis"


class QueryRelationshipType(Enum):
    """Types of relationships that can be traversed"""
    HAS_CONFLICT = "HAS_CONFLICT"
    AFFECTS = "AFFECTS"
    MODIFIES = "MODIFIES"
    AUTHORED_BY = "AUTHORED_BY"
    REVIEWED_BY = "REVIEWED_BY"
    DEPENDS_ON = "DEPENDS_ON"
    CONFLICTS_WITH = "CONFLICTS_WITH"
    RESOLVES = "RESOLVES"
    HAS_COMMIT = "HAS_COMMIT"
    CALLS = "CALLS"
    ACCESSES = "ACCESSES"
    USES = "USES"


class QueryOperator(Enum):
    """Query operators for filtering"""
    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT CONTAINS"
    IN = "IN"
    NOT_IN = "NOT IN"
    STARTS_WITH = "STARTS WITH"
    ENDS_WITH = "ENDS WITH"
    REGEX = "=~"


class QueryModifier(Enum):
    """Query modifiers for result manipulation"""
    ORDER_BY = "ORDER BY"
    LIMIT = "LIMIT"
    SKIP = "SKIP"
    DISTINCT = "DISTINCT"
    WITH = "WITH"
    RETURN = "RETURN"


@dataclass
class QueryCondition:
    """Represents a single query condition"""
    property_name: str
    operator: QueryOperator
    value: Any
    logical_operator: Optional[str] = None  # AND, OR


@dataclass
class QueryProperty:
    """Represents a property to return or use in query"""
    name: str
    alias: Optional[str] = None
    aggregation: Optional[str] = None  # COUNT, SUM, AVG, MIN, MAX


@dataclass
class QueryParameter:
    """Represents a query parameter"""
    name: str
    value: Any
    type: str = "string"  # string, int, float, bool, datetime


class GraphQueryBuilder:
    """
    Flexible builder for constructing complex graph queries
    """
    
    def __init__(self):
        self.select_clauses = []
        self.match_clauses = []
        self.where_clauses = []
        self.with_clauses = []
        self.order_by_clauses = []
        self.limit_clause = None
        self.skip_clause = None
        self.return_clauses = []
        self.parameters = {}
        self.query_type = "read"  # read, write
        self.with_statistics = False
        
    def select(
        self, 
        node_type: QueryNodeType, 
        alias: str,
        properties: Optional[List[QueryProperty]] = None
    ) -> 'GraphQueryBuilder':
        """Add SELECT clause"""
        self.select_clauses.append({
            "type": "select",
            "node_type": node_type.value,
            "alias": alias,
            "properties": properties or []
        })
        return self
    
    def match(
        self,
        pattern: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> 'GraphQueryBuilder':
        """Add MATCH clause"""
        self.match_clauses.append({
            "pattern": pattern,
            "parameters": parameters or {}
        })
        return self
    
    def where(self, condition: QueryCondition) -> 'GraphQueryBuilder':
        """Add WHERE condition"""
        self.where_clauses.append(condition)
        return self
    
    def where_raw(self, condition: str, parameters: Optional[Dict[str, Any]] = None) -> 'GraphQueryBuilder':
        """Add raw WHERE condition"""
        self.where_clauses.append({
            "type": "raw",
            "condition": condition,
            "parameters": parameters or {}
        })
        return self
    
    def with_clause(self, clause: str) -> 'GraphQueryBuilder':
        """Add WITH clause"""
        self.with_clauses.append(clause)
        return self
    
    def order_by(self, property_name: str, direction: str = "ASC") -> 'GraphQueryBuilder':
        """Add ORDER BY clause"""
        self.order_by_clauses.append({
            "property": property_name,
            "direction": direction
        })
        return self
    
    def limit(self, count: int) -> 'GraphQueryBuilder':
        """Add LIMIT clause"""
        self.limit_clause = count
        return self
    
    def skip(self, count: int) -> 'GraphQueryBuilder':
        """Add SKIP clause"""
        self.skip_clause = count
        return self
    
    def return_clause(
        self,
        items: List[Union[str, QueryProperty]],
        distinct: bool = False
    ) -> 'GraphQueryBuilder':
        """Add RETURN clause"""
        self.return_clauses.append({
            "items": items,
            "distinct": distinct
        })
        return self
    
    def with_statistics(self) -> 'GraphQueryBuilder':
        """Add statistics to query results"""
        self.with_statistics = True
        return self
    
    def parameter(self, name: str, value: Any, type: str = "string") -> 'GraphQueryBuilder':
        """Add query parameter"""
        self.parameters[name] = QueryParameter(name, value, type)
        return self
    
    def param(
        self, 
        name: str, 
        value: Any, 
        type: str = "string"
    ) -> 'GraphQueryBuilder':
        """Add query parameter (alias for parameter method)"""
        return self.parameter(name, value, type)
    
    def add_parameter(self, name: str, value: Any, type: str = "string") -> 'GraphQueryBuilder':
        """Add query parameter (alternative method name)"""
        return self.parameter(name, value, type)
    
    def build(self) -> str:
        """Build the complete query string"""
        query_parts = []
        
        # Build parameter declarations
        if self.parameters:
            param_declarations = []
            for param in self.parameters.values():
                if param.type == "datetime":
                    param_declarations.append(f":param {param.name} => datetime('{param.value}')")
                else:
                    param_declarations.append(f":param {param.name} => {param.value}")
            
            if param_declarations:
                query_parts.append("\n".join(param_declarations))
        
        # Build SELECT clauses
        for select in self.select_clauses:
            select_clause = f"MATCH (n:{select['node_type']})"
            if select['properties']:
                props = ", ".join([f"n.{prop.name} as {prop.alias or prop.name}" 
                                 for prop in select['properties']])
                select_clause += f" RETURN {props}"
            else:
                select_clause += " RETURN n"
            query_parts.append(select_clause)
        
        # Build MATCH clauses
        for match in self.match_clauses:
            query_parts.append(f"MATCH {match['pattern']}")
        
        # Build WITH clauses
        for with_clause in self.with_clauses:
            query_parts.append(f"WITH {with_clause}")
        
        # Build WHERE clauses
        where_conditions = []
        for condition in self.where_clauses:
            if isinstance(condition, dict) and condition.get("type") == "raw":
                where_conditions.append(condition["condition"])
            else:
                where_conditions.append(self._build_condition(condition))
        
        if where_conditions:
            query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        # Build ORDER BY clauses
        if self.order_by_clauses:
            order_parts = []
            for order in self.order_by_clauses:
                order_parts.append(f"{order['property']} {order['direction']}")
            query_parts.append(f"ORDER BY {', '.join(order_parts)}")
        
        # Build RETURN clauses
        if self.return_clauses:
            for return_clause in self.return_clauses:
                items = []
                for item in return_clause["items"]:
                    if isinstance(item, str):
                        items.append(item)
                    elif isinstance(item, QueryProperty):
                        prop_expr = item.name
                        if item.alias:
                            prop_expr += f" as {item.alias}"
                        if item.aggregation:
                            prop_expr = f"{item.aggregation}({prop_expr})"
                        items.append(prop_expr)
                
                return_text = "RETURN " + ", ".join(items)
                if return_clause["distinct"]:
                    return_text = "RETURN DISTINCT " + ", ".join(items)
                
                query_parts.append(return_text)
        
        # Build LIMIT and SKIP
        if self.skip_clause:
            query_parts.append(f"SKIP {self.skip_clause}")
        if self.limit_clause:
            query_parts.append(f"LIMIT {self.limit_clause}")
        
        return "\n".join(query_parts)
    
    def _build_condition(self, condition: QueryCondition) -> str:
        """Build a single condition string"""
        # Handle different value types
        if isinstance(condition.value, str):
            if condition.operator == QueryOperator.REGEX:
                value = f"/{condition.value}/"
            else:
                value = f"'{condition.value}'"
        elif isinstance(condition.value, (int, float)):
            value = str(condition.value)
        elif isinstance(condition.value, bool):
            value = str(condition.value).lower()
        elif isinstance(condition.value, list):
            if condition.operator in [QueryOperator.IN, QueryOperator.NOT_IN]:
                values = [f"'{v}'" if isinstance(v, str) else str(v) for v in condition.value]
                value = f"[{', '.join(values)}]"
            else:
                value = f"'{condition.value}'"
        else:
            value = f"'{condition.value}'"
        
        condition_str = f"{condition.property_name} {condition.operator.value} {value}"
        
        if condition.logical_operator:
            condition_str = f"{condition.logical_operator} {condition_str}"
        
        return condition_str
    
    def execute(self) -> List[Dict[str, Any]]:
        """Execute the built query"""
        query = self.build()
        param_dict = {param.name: param.value for param in self.parameters.values()}
        
        try:
            return connection_manager.execute_query(query, param_dict)
        except Exception as e:
            logger.error("Query execution failed", error=str(e), query=query)
            raise
    
    async def execute_async(self) -> List[Dict[str, Any]]:
        """Execute the built query asynchronously"""
        query = self.build()
        param_dict = {param.name: param.value for param in self.parameters.values()}
        
        try:
            return await connection_manager.execute_query(query, param_dict)
        except Exception as e:
            logger.error("Async query execution failed", error=str(e), query=query)
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert query builder to dictionary representation"""
        return {
            "select_clauses": self.select_clauses,
            "match_clauses": self.match_clauses,
            "where_clauses": [
                {
                    "property_name": c.property_name,
                    "operator": c.operator.value,
                    "value": c.value,
                    "logical_operator": c.logical_operator
                } if not isinstance(c, dict) else c
                for c in self.where_clauses
            ],
            "with_clauses": self.with_clauses,
            "order_by_clauses": self.order_by_clauses,
            "limit_clause": self.limit_clause,
            "skip_clause": self.skip_clause,
            "return_clauses": self.return_clauses,
            "parameters": [
                {
                    "name": p.name,
                    "value": p.value,
                    "type": p.type
                } for p in self.parameters.values()
            ],
            "query_type": self.query_type,
            "with_statistics": self.with_statistics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraphQueryBuilder':
        """Create query builder from dictionary representation"""
        builder = cls()
        
        builder.select_clauses = data.get("select_clauses", [])
        builder.match_clauses = data.get("match_clauses", [])
        
        # Rebuild where clauses
        for where_data in data.get("where_clauses", []):
            if isinstance(where_data, dict) and where_data.get("type") == "raw":
                builder.where_clauses.append(where_data)
            else:
                condition = QueryCondition(
                    property_name=where_data["property_name"],
                    operator=QueryOperator(where_data["operator"]),
                    value=where_data["value"],
                    logical_operator=where_data.get("logical_operator")
                )
                builder.where_clauses.append(condition)
        
        builder.with_clauses = data.get("with_clauses", [])
        builder.order_by_clauses = data.get("order_by_clauses", [])
        builder.limit_clause = data.get("limit_clause")
        builder.skip_clause = data.get("skip_clause")
        builder.return_clauses = data.get("return_clauses", [])
        builder.query_type = data.get("query_type", "read")
        builder.with_statistics = data.get("with_statistics", False)
        
        # Rebuild parameters
        for param_data in data.get("parameters", []):
            builder.parameters[param_data["name"]] = QueryParameter(
                name=param_data["name"],
                value=param_data["value"],
                type=param_data["type"]
            )
        
        return builder


class ConflictQueryBuilder(GraphQueryBuilder):
    """
    Specialized query builder for conflict-related queries
    """
    
    def find_conflicts_by_severity(self, severities: List[str]) -> 'ConflictQueryBuilder':
        """Find conflicts by severity level"""
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .where(QueryCondition("severity", QueryOperator.IN, severities))
                .return_clause(["conflict"]))
    
    def find_conflicts_by_type(self, conflict_types: List[str]) -> 'ConflictQueryBuilder':
        """Find conflicts by type"""
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .where(QueryCondition("type", QueryOperator.IN, conflict_types))
                .return_clause(["conflict"]))
    
    def find_conflicts_for_pr(self, pr_id: str) -> 'ConflictQueryBuilder':
        """Find conflicts affecting a specific PR"""
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .match("(pr {id: $pr_id})-[:HAS_CONFLICT]->(conflict)")
                .param("pr_id", pr_id)
                .return_clause(["conflict", "pr"]))
    
    def find_recent_conflicts(self, days: int = 7) -> 'ConflictQueryBuilder':
        """Find conflicts detected in the last N days"""
        cutoff_date = (datetime.utcnow()).isoformat()
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .where(QueryCondition("detected_at", QueryOperator.GREATER_THAN, cutoff_date))
                .order_by("detected_at", "DESC")
                .return_clause(["conflict"]))
    
    def find_unresolved_conflicts(self) -> 'ConflictQueryBuilder':
        """Find conflicts without resolutions"""
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .where(QueryCondition("resolution_id", QueryOperator.IS_NULL, None))
                .return_clause(["conflict"]))
    
    def find_conflicts_with_analysis(self) -> 'ConflictQueryBuilder':
        """Find conflicts that have AI analysis"""
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .select(QueryNodeType.AI_ANALYSIS, "analysis")
                .match("(conflict)-[:HAS_AI_ANALYSIS]->(analysis)")
                .return_clause(["conflict", "analysis"]))


class PRQueryBuilder(GraphQueryBuilder):
    """
    Specialized query builder for PR-related queries
    """
    
    def find_prs_by_status(self, statuses: List[str]) -> 'PRQueryBuilder':
        """Find PRs by status"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .where(QueryCondition("status", QueryOperator.IN, statuses))
                .return_clause(["pr"]))
    
    def find_prs_by_author(self, author_id: str) -> 'PRQueryBuilder':
        """Find PRs by author"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .where(QueryCondition("author_id", QueryOperator.EQUALS, author_id))
                .return_clause(["pr"]))
    
    def find_prs_with_conflicts(self) -> 'PRQueryBuilder':
        """Find PRs that have conflicts"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .select(QueryNodeType.CONFLICT, "conflict")
                .match("(pr)-[:HAS_CONFLICT]->(conflict)")
                .return_clause(["pr", "conflict"]))
    
    def find_complex_prs(self, min_complexity: float = 0.7) -> 'PRQueryBuilder':
        """Find complex PRs above threshold"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .where(QueryCondition("complexity", QueryOperator.GREATER_THAN, min_complexity))
                .order_by("complexity", "DESC")
                .return_clause(["pr"]))
    
    def find_pr_dependencies(self, pr_id: str) -> 'PRQueryBuilder':
        """Find dependencies of a specific PR"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .select(QueryNodeType.PULL_REQUEST, "dependency")
                .match("(pr {id: $pr_id})-[:DEPENDS_ON]->(dependency)")
                .param("pr_id", pr_id)
                .return_clause(["pr", "dependency"]))
    
    def find_similar_prs(self, pr_id: str, limit: int = 10) -> 'PRQueryBuilder':
        """Find PRs similar to a specific PR"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr1")
                .select(QueryNodeType.PULL_REQUEST, "pr2")
                .match("(pr1 {id: $pr_id})-[:SIMILAR_TO]-(pr2)")
                .param("pr_id", pr_id)
                .order_by("similarity_score", "DESC")
                .limit(limit)
                .return_clause(["pr2"]))


class AnalyticsQueryBuilder(GraphQueryBuilder):
    """
    Specialized query builder for analytics queries
    """
    
    def calculate_centrality(self, node_type: QueryNodeType) -> 'AnalyticsQueryBuilder':
        """Calculate centrality metrics for nodes"""
        return (self
                .select(node_type, "node")
                .with_clause("node, size((node)-[:DEPENDS_ON]->(:PullRequest)) as dependency_count")
                .return_clause([
                    QueryProperty("node", alias="id"),
                    QueryProperty("dependency_count", alias="centrality_score")
                ])
                .order_by("centrality_score", "DESC"))
    
    def find_communities(self) -> 'AnalyticsQueryBuilder':
        """Find communities of related PRs"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr1")
                .select(QueryNodeType.PULL_REQUEST, "pr2")
                .match("(pr1)-[:CONFLICTS_WITH|SIMILAR_TO]-(pr2)")
                .with_clause("pr1, pr2, count(*) as relationship_strength")
                .return_clause(["pr1", "pr2", "relationship_strength"])
                .order_by("relationship_strength", "DESC"))
    
    def analyze_conflict_trends(self, days: int = 30) -> 'AnalyticsQueryBuilder':
        """Analyze conflict trends over time"""
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        return (self
                .select(QueryNodeType.CONFLICT, "conflict")
                .where(QueryCondition("detected_at", QueryOperator.GREATER_THAN, cutoff_date))
                .with_clause("date(conflict.detected_at) as date, conflict.severity, count(*) as count")
                .return_clause([
                    QueryProperty("date", alias="date"),
                    QueryProperty("severity", alias="severity"),
                    QueryProperty("count", alias="conflict_count")
                ])
                .order_by("date", "ASC"))
    
    def find_bottleneck_prs(self) -> 'AnalyticsQueryBuilder':
        """Find PRs that are bottlenecks in the dependency chain"""
        return (self
                .select(QueryNodeType.PULL_REQUEST, "pr")
                .with_clause("pr, size((pr)<-[:DEPENDS_ON]-(:PullRequest)) as blocking_count")
                .where(QueryCondition("blocking_count", QueryOperator.GREATER_THAN, 2))
                .return_clause([
                    QueryProperty("pr", alias="id"),
                    QueryProperty("blocking_count", alias="bottleneck_score")
                ])
                .order_by("bottleneck_score", "DESC"))


class QueryTemplate:
    """
    Predefined query templates for common operations
    """
    
    @staticmethod
    def get_conflicts_by_severity(severity: str) -> str:
        """Template for getting conflicts by severity"""
        return """
        MATCH (c:Conflict {severity: $severity})
        OPTIONAL MATCH (c)-[:AFFECTS]-(pr:PullRequest)
        RETURN c, collect(pr) as affected_prs
        ORDER BY c.detected_at DESC
        LIMIT 100
        """
    
    @staticmethod
    def get_pr_complexity_analysis(pr_id: str) -> str:
        """Template for PR complexity analysis"""
        return """
        MATCH (pr:PullRequest {id: $pr_id})
        OPTIONAL MATCH (pr)-[:HAS_CONFLICT]->(c:Conflict)
        OPTIONAL MATCH (pr)-[:HAS_COMMIT]->(commit:Commit)-[:MODIFIES]->(file:File)
        WITH pr, 
             count(c) as conflict_count,
             count(file) as file_count,
             sum(file.size) as total_file_size
        RETURN pr,
               pr.complexity as base_complexity,
               conflict_count,
               file_count,
               total_file_size,
               conflict_count * 0.3 + file_count * 0.001 + total_file_size * 0.000001 as calculated_complexity
        """
    
    @staticmethod
    def get_dependency_chain(pr_id: str) -> str:
        """Template for dependency chain analysis"""
        return """
        MATCH path = (pr:PullRequest {id: $pr_id})<-[:DEPENDS_ON*1..10]-(dependency:PullRequest)
        WHERE all(node in nodes(path) WHERE node.complexity IS NOT NULL)
        RETURN path, 
               length(path) as distance,
               reduce(score = 0, node in nodes(path) | score + node.complexity) as total_complexity
        ORDER BY distance ASC, total_complexity DESC
        """
    
    @staticmethod
    def get_similarity_analysis(pr_id: str, threshold: float = 0.7) -> str:
        """Template for similarity analysis"""
        return """
        MATCH (pr:PullRequest {id: $pr_id})
        OPTIONAL MATCH (pr)-[:HAS_COMMIT]->(commit:Commit)-[:MODIFIES]->(file:File)
        WITH pr, collect(DISTINCT file.path) as pr_files
        MATCH (other:PullRequest)-[:HAS_COMMIT]->(other_commit:Commit)-[:MODIFIES]->(other_file:File)
        WHERE pr.id <> other.id
        WITH pr, other, pr_files, collect(DISTINCT other_file.path) as other_files
        WHERE size([f IN pr_files WHERE f IN other_files]) >= $threshold * size(pr_files)
        RETURN other,
               size([f IN pr_files WHERE f IN other_files]) as shared_files,
               size(pr_files) as pr_file_count,
               size(other_files) as other_file_count,
               size([f IN pr_files WHERE f IN other_files]) * 1.0 / size(pr_files + other_files - [f IN pr_files WHERE f IN other_files]) as similarity
        ORDER BY similarity DESC
        LIMIT 10
        """


class RealTimeQueryMonitor:
    """
    Monitors real-time graph changes and notifications
    """
    
    def __init__(self):
        self.subscribed_queries = {}
        self.notification_handlers = {}
        self.is_monitoring = False
    
    async def start_monitoring(self) -> bool:
        """Start real-time monitoring"""
        if self.is_monitoring:
            return True
        
        try:
            # Set up Neo4j change data capture
            await self._setup_change_capture()
            self.is_monitoring = True
            logger.info("Real-time query monitoring started")
            return True
        except Exception as e:
            logger.error("Failed to start real-time monitoring", error=str(e))
            return False
    
    async def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.is_monitoring = False
        logger.info("Real-time query monitoring stopped")
    
    async def subscribe_to_conflicts(self, handler: callable) -> str:
        """Subscribe to conflict notifications"""
        subscription_id = f"conflict_{datetime.utcnow().timestamp()}"
        self.notification_handlers[subscription_id] = handler
        
        # Set up conflict change notification
        query = """
        MATCH (c:Conflict)
        WHERE c.detected_at > datetime()
        RETURN c, labels(c)[0] as type
        """
        
        self.subscribed_queries[subscription_id] = {
            "query": query,
            "handler": handler,
            "type": "conflict"
        }
        
        return subscription_id
    
    async def subscribe_to_pr_changes(self, pr_id: str, handler: callable) -> str:
        """Subscribe to PR change notifications"""
        subscription_id = f"pr_change_{pr_id}_{datetime.utcnow().timestamp()}"
        self.notification_handlers[subscription_id] = handler
        
        query = """
        MATCH (pr:PullRequest {id: $pr_id})
        OPTIONAL MATCH (pr)-[:HAS_CONFLICT]->(c:Conflict)
        OPTIONAL MATCH (pr)-[:HAS_COMMIT]->(commit:Commit)
        WHERE pr.updated_at > datetime() OR c.detected_at > datetime() OR commit.timestamp > datetime()
        RETURN pr, collect(c) as conflicts, collect(commit) as commits
        """
        
        self.subscribed_queries[subscription_id] = {
            "query": query,
            "parameters": {"pr_id": pr_id},
            "handler": handler,
            "type": "pr_change"
        }
        
        return subscription_id
    
    async def _setup_change_capture(self):
        """Set up Neo4j change data capture"""
        # This would set up Neo4j's change data capture
        # For now, it's a placeholder
        pass
    
    async def check_for_changes(self):
        """Check for changes and notify handlers"""
        if not self.is_monitoring:
            return
        
        for subscription_id, query_info in self.subscribed_queries.items():
            try:
                results = await connection_manager.execute_query(
                    query_info["query"], 
                    query_info.get("parameters", {})
                )
                
                if results:
                    await query_info["handler"](results, subscription_id)
            except Exception as e:
                logger.error("Error checking for changes", 
                           subscription_id=subscription_id, 
                           error=str(e))
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return {
            "is_monitoring": self.is_monitoring,
            "active_subscriptions": len(self.subscribed_queries),
            "notification_handlers": len(self.notification_handlers)
        }


# Global instances
query_builder = GraphQueryBuilder()
conflict_query_builder = ConflictQueryBuilder()
pr_query_builder = PRQueryBuilder()
analytics_query_builder = AnalyticsQueryBuilder()
query_templates = QueryTemplate()
real_time_monitor = RealTimeQueryMonitor()