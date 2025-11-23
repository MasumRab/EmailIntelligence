"""
Core graph traversal algorithms for PR conflict detection
"""

import time
from collections import deque
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import structlog

from ...database.connection import connection_manager

logger = structlog.get_logger()


class TraversalStrategy(Enum):
    """Graph traversal strategies"""

    BFS = "breadth_first"
    DFS = "depth_first"
    BIDIRECTIONAL = "bidirectional"
    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"


class TraversalDirection(Enum):
    """Traversal direction options"""

    FORWARD = "forward"
    BACKWARD = "backward"
    BIDIRECTIONAL = "bidirectional"


class GraphNode:
    """Represents a node in the graph traversal"""

    def __init__(self, node_id: str, node_type: str, properties: Dict[str, Any]):
        self.id = node_id
        self.type = node_type
        self.properties = properties
        self.visited = False
        self.distance = float("inf")
        self.parent = None
        self.timestamp = datetime.utcnow()

    def __repr__(self) -> str:
        return f"GraphNode(id={self.id}, type={self.type})"


class TraversalResult:
    """Result of graph traversal operation"""

    def __init__(self):
        self.visited_nodes: List[GraphNode] = []
        self.paths: List[List[GraphNode]] = []
        self.cycles: List[List[GraphNode]] = []
        self.subgraphs: List[Set[GraphNode]] = []
        self.metadata: Dict[str, Any] = {}
        self.execution_time: float = 0.0
        self.nodes_visited: int = 0
        self.edges_traversed: int = 0

    def add_visited_node(self, node: GraphNode):
        """Add a visited node to the result"""
        if node not in self.visited_nodes:
            self.visited_nodes.append(node)
            self.nodes_visited += 1

    def add_path(self, path: List[GraphNode]):
        """Add a discovered path"""
        self.paths.append(path)
        self.edges_traversed += len(path) - 1 if len(path) > 1 else 0

    def add_cycle(self, cycle: List[GraphNode]):
        """Add a detected cycle"""
        self.cycles.append(cycle)

    def add_subgraph(self, subgraph: Set[GraphNode]):
        """Add a discovered subgraph"""
        self.subgraphs.append(subgraph)


class GraphTraversalEngine:
    """
    Sophisticated graph traversal engine for conflict detection
    Supports multiple algorithms and optimization strategies
    """

    def __init__(self):
        self.node_cache: Dict[str, GraphNode] = {}
        self.adjacency_cache: Dict[str, List[Tuple[str, str]]] = {}
        self.query_cache: Dict[str, Any] = {}
        self.performance_stats = {"total_traversals": 0, "avg_execution_time": 0.0, "cache_hits": 0, "cache_misses": 0}

    async def clear_cache(self):
        """Clear traversal caches"""
        self.node_cache.clear()
        self.adjacency_cache.clear()
        self.query_cache.clear()
        logger.info("Graph traversal cache cleared")

    async def get_node(self, node_id: str, node_type: str) -> Optional[GraphNode]:
        """Get node from cache or database"""
        cache_key = f"{node_type}:{node_id}"

        if cache_key in self.node_cache:
            return self.node_cache[cache_key]

        query = f"""
        MATCH (n:{node_type} {{id: $node_id}})
        RETURN n
        """

        try:
            records = await connection_manager.execute_query(query, {"node_id": node_id})
            if records:
                node_data = records[0]["n"]
                node = GraphNode(node_id, node_type, dict(node_data))
                self.node_cache[cache_key] = node
                return node
        except Exception as e:
            logger.error("Failed to fetch node", node_id=node_id, node_type=node_type, error=str(e))

        return None

    async def get_adjacent_nodes(
        self,
        node_id: str,
        relationship_types: List[str] = None,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> List[Tuple[str, str]]:
        """Get adjacent nodes with relationship types"""
        cache_key = f"adj:{node_id}:{direction.value}:{','.join(relationship_types or [])}"

        if cache_key in self.adjacency_cache:
            return self.adjacency_cache[cache_key]

        rel_pattern = "[:"
        if relationship_types:
            rel_pattern += "|".join(relationship_types)
        rel_pattern += "]"

        if direction == TraversalDirection.FORWARD:
            query = f"""
            MATCH (n {{id: $node_id}})-{rel_pattern}->(neighbor)
            RETURN neighbor.id as neighbor_id, 
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """
        elif direction == TraversalDirection.BACKWARD:
            query = f"""
            MATCH (neighbor)-{rel_pattern}->(n {{id: $node_id}})
            RETURN neighbor.id as neighbor_id,
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """
        else:  # BIDIRECTIONAL
            query = f"""
            MATCH (n {{id: $node_id}})-{rel_pattern}-(neighbor)
            RETURN neighbor.id as neighbor_id,
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """

        try:
            records = await connection_manager.execute_query(query, {"node_id": node_id})
            adjacent_nodes = [(record["neighbor_id"], record["rel_type"]) for record in records]
            self.adjacency_cache[cache_key] = adjacent_nodes
            return adjacent_nodes
        except Exception as e:
            logger.error("Failed to fetch adjacent nodes", node_id=node_id, error=str(e))
            return []

    async def breadth_first_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: Optional[str] = None,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> TraversalResult:
        """Breadth-First Search implementation"""
        start_time = time.time()
        result = TraversalResult()

        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            logger.error("Start node not found", node_id=start_node_id, node_type=start_node_type)
            return result

        queue = deque([start_node])
        visited = {start_node_id}
        start_node.visited = True
        start_node.distance = 0
        result.add_visited_node(start_node)

        logger.info("Starting BFS traversal", start_node=start_node_id, target=target_node_id, max_depth=max_depth)

        while queue and start_node.distance < max_depth:
            current_node = queue.popleft()

            adjacent = await self.get_adjacent_nodes(current_node.id, relationship_types, direction)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)

                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                    if not neighbor_node:
                        continue

                    neighbor_node.visited = True
                    neighbor_node.distance = current_node.distance + 1
                    neighbor_node.parent = current_node
                    result.add_visited_node(neighbor_node)

                    if target_node_id and neighbor_id == target_node_id:
                        path = self._reconstruct_path(neighbor_node)
                        result.add_path(path)
                        logger.info("BFS target found", path_length=len(path))

                    queue.append(neighbor_node)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.BFS.value,
            "max_depth_reached": max(node.distance for node in result.visited_nodes),
            "found_target": target_node_id is not None and any(p.id == target_node_id for p in result.visited_nodes),
        }

        self.performance_stats["total_traversals"] += 1
        self.performance_stats["avg_execution_time"] = (
            self.performance_stats["avg_execution_time"] * (self.performance_stats["total_traversals"] - 1)
            + result.execution_time
        ) / self.performance_stats["total_traversals"]

        logger.info("BFS traversal completed", nodes_visited=result.nodes_visited, execution_time=result.execution_time)

        return result

    async def depth_first_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: Optional[str] = None,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> TraversalResult:
        """Depth-First Search implementation"""
        start_time = time.time()
        result = TraversalResult()

        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            return result

        visited = set()

        logger.info("Starting DFS traversal", start_node=start_node_id, target=target_node_id, max_depth=max_depth)

        async def dfs_recursive(node: GraphNode, depth: int):
            if depth > max_depth or node.id in visited:
                return

            visited.add(node.id)
            node.visited = True
            result.add_visited_node(node)

            if target_node_id and node.id == target_node_id:
                path = self._reconstruct_path(node)
                result.add_path(path)
                return True

            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, direction)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in visited:
                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                    if neighbor_node and await dfs_recursive(neighbor_node, depth + 1):
                        return True

            return False

        await dfs_recursive(start_node, 0)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.DFS.value,
            "max_depth_reached": max(node.distance for node in result.visited_nodes),
            "found_target": target_node_id is not None and any(p.id == target_node_id for p in result.visited_nodes),
        }

        self.performance_stats["total_traversals"] += 1

        logger.info("DFS traversal completed", nodes_visited=result.nodes_visited, execution_time=result.execution_time)

        return result

    async def bidirectional_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 5,
    ) -> TraversalResult:
        """Bidirectional Search implementation"""
        start_time = time.time()
        result = TraversalResult()

        forward_queue = deque()
        backward_queue = deque()
        forward_visited = set()
        backward_visited = set()
        forward_parents = {}
        backward_parents = {}

        start_node = await self.get_node(start_node_id, start_node_type)
        target_node = await self.get_node(target_node_id, "PullRequest")

        if not start_node or not target_node:
            return result

        forward_queue.append(start_node)
        backward_queue.append(target_node)
        forward_visited.add(start_node_id)
        backward_visited.add(target_node_id)

        logger.info(
            "Starting bidirectional search", start_node=start_node_id, target_node=target_node_id, max_depth=max_depth
        )

        current_depth = 0
        while forward_queue and backward_queue and current_depth < max_depth:
            if forward_queue:
                current_level_size = len(forward_queue)
                for _ in range(current_level_size):
                    current_node = forward_queue.popleft()
                    result.add_visited_node(current_node)

                    adjacent = await self.get_adjacent_nodes(
                        current_node.id, relationship_types, TraversalDirection.FORWARD
                    )

                    for neighbor_id, rel_type in adjacent:
                        if neighbor_id not in forward_visited:
                            forward_visited.add(neighbor_id)
                            forward_parents[neighbor_id] = current_node.id

                            neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                            if neighbor_node:
                                forward_queue.append(neighbor_node)

                                if neighbor_id in backward_visited:
                                    path = self._reconstruct_bidirectional_path(
                                        neighbor_id, forward_parents, backward_parents
                                    )
                                    result.add_path(path)
                                    logger.info("Bidirectional search found path", path_length=len(path))
                                    return result

            if backward_queue:
                current_level_size = len(backward_queue)
                for _ in range(current_level_size):
                    current_node = backward_queue.popleft()
                    result.add_visited_node(current_node)

                    adjacent = await self.get_adjacent_nodes(
                        current_node.id, relationship_types, TraversalDirection.BACKWARD
                    )

                    for neighbor_id, rel_type in adjacent:
                        if neighbor_id not in backward_visited:
                            backward_visited.add(neighbor_id)
                            backward_parents[neighbor_id] = current_node.id

                            neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                            if neighbor_node:
                                backward_queue.append(neighbor_node)

                                if neighbor_id in forward_visited:
                                    path = self._reconstruct_bidirectional_path(
                                        neighbor_id, forward_parents, backward_parents
                                    )
                                    result.add_path(path)
                                    logger.info("Bidirectional search found path", path_length=len(path))
                                    return result

            current_depth += 1

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.BIDIRECTIONAL.value,
            "max_depth_reached": current_depth,
            "found_target": False,
        }

        self.performance_stats["total_traversals"] += 1

        logger.info(
            "Bidirectional search completed without finding target",
            nodes_visited=result.nodes_visited,
            execution_time=result.execution_time,
        )

        return result

    async def detect_cycles(
        self, start_node_id: str, start_node_type: str, relationship_types: List[str] = None
    ) -> TraversalResult:
        """Cycle detection using DFS with backtracking"""
        start_time = time.time()
        result = TraversalResult()

        visited = set()
        recursion_stack = set()

        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            return result

        logger.info("Starting cycle detection", start_node=start_node_id)

        async def dfs_cycle_detection(node: GraphNode, path: List[str]):
            if node.id in recursion_stack:
                cycle_start_idx = path.index(node.id)
                cycle_path = path[cycle_start_idx:] + [node.id]
                result.add_cycle([await self.get_node(node_id, "PullRequest") for node_id in cycle_path])
                return

            if node.id in visited:
                return

            visited.add(node.id)
            recursion_stack.add(node.id)
            path.append(node.id)

            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, TraversalDirection.FORWARD)

            for neighbor_id, rel_type in adjacent:
                neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                if neighbor_node:
                    await dfs_cycle_detection(neighbor_node, path.copy())

            recursion_stack.remove(node.id)

        await dfs_cycle_detection(start_node, [])

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": "cycle_detection",
            "cycles_found": len(result.cycles),
            "total_cycles": sum(len(cycle) for cycle in result.cycles),
        }

        logger.info("Cycle detection completed", cycles_found=len(result.cycles), execution_time=result.execution_time)

        return result

    def _reconstruct_path(self, end_node: GraphNode) -> List[GraphNode]:
        """Reconstruct path from start to end node"""
        path = []
        current = end_node
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    def _reconstruct_bidirectional_path(
        self, meeting_node_id: str, forward_parents: Dict[str, str], backward_parents: Dict[str, str]
    ) -> List[GraphNode]:
        """Reconstruct path found by bidirectional search"""
        return []  # Placeholder for actual implementation

    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get traversal engine performance statistics"""
        return {
            **self.performance_stats,
            "cache_size": len(self.node_cache) + len(self.adjacency_cache),
            "queries_cached": len(self.query_cache),
        }

    async def find_shortest_path(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 10,
    ) -> TraversalResult:
        """Find shortest path between two nodes using bidirectional BFS"""
        return await self.bidirectional_search(
            start_node_id, start_node_type, target_node_id, relationship_types, max_depth
        )

    async def find_all_paths(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        max_paths: int = 100,
    ) -> TraversalResult:
        """Find all paths between two nodes (with limits to prevent explosion)"""
        start_time = time.time()
        result = TraversalResult()

        start_node = await self.get_node(start_node_id, start_node_type)
        target_node = await self.get_node(target_node_id, "PullRequest")

        if not start_node or not target_node:
            return result

        paths_found = 0
        visited_paths = set()

        async def dfs_all_paths(node: GraphNode, current_path: List[str], depth: int):
            nonlocal paths_found

            if depth > max_depth or paths_found >= max_paths:
                return

            current_path_str = ":".join(current_path)
            if current_path_str in visited_paths:
                return

            visited_paths.add(current_path_str)

            if node.id == target_node_id and len(current_path) > 1:
                full_path = []
                for node_id in current_path:
                    path_node = await self.get_node(node_id, "PullRequest")
                    if path_node:
                        full_path.append(path_node)

                result.add_path(full_path)
                paths_found += 1
                return

            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, TraversalDirection.FORWARD)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in current_path:
                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                    if neighbor_node:
                        new_path = current_path + [neighbor_id]
                        await dfs_all_paths(neighbor_node, new_path, depth + 1)

        await dfs_all_paths(start_node, [start_node_id], 0)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": "all_paths",
            "max_depth": max_depth,
            "max_paths": max_paths,
            "paths_found": len(result.paths),
        }

        return result


# Global traversal engine instance
traversal_engine = GraphTraversalEngine()
"""
Core graph traversal algorithms for PR conflict detection
"""

import time
from collections import deque
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import structlog

from ...database.connection import connection_manager

logger = structlog.get_logger()


class TraversalStrategy(Enum):
    """Graph traversal strategies"""

    BFS = "breadth_first"
    DFS = "depth_first"
    BIDIRECTIONAL = "bidirectional"
    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"


class TraversalDirection(Enum):
    """Traversal direction options"""

    FORWARD = "forward"
    BACKWARD = "backward"
    BIDIRECTIONAL = "bidirectional"


class GraphNode:
    """Represents a node in the graph traversal"""

    def __init__(self, node_id: str, node_type: str, properties: Dict[str, Any]):
        self.id = node_id
        self.type = node_type
        self.properties = properties
        self.visited = False
        self.distance = float("inf")
        self.parent = None
        self.timestamp = datetime.utcnow()

    def __repr__(self) -> str:
        return f"GraphNode(id={self.id}, type={self.type})"


class TraversalResult:
    """Result of graph traversal operation"""

    def __init__(self):
        self.visited_nodes: List[GraphNode] = []
        self.paths: List[List[GraphNode]] = []
        self.cycles: List[List[GraphNode]] = []
        self.subgraphs: List[Set[GraphNode]] = []
        self.metadata: Dict[str, Any] = {}
        self.execution_time: float = 0.0
        self.nodes_visited: int = 0
        self.edges_traversed: int = 0

    def add_visited_node(self, node: GraphNode):
        """Add a visited node to the result"""
        if node not in self.visited_nodes:
            self.visited_nodes.append(node)
            self.nodes_visited += 1

    def add_path(self, path: List[GraphNode]):
        """Add a discovered path"""
        self.paths.append(path)
        self.edges_traversed += len(path) - 1 if len(path) > 1 else 0

    def add_cycle(self, cycle: List[GraphNode]):
        """Add a detected cycle"""
        self.cycles.append(cycle)

    def add_subgraph(self, subgraph: Set[GraphNode]):
        """Add a discovered subgraph"""
        self.subgraphs.append(subgraph)


class GraphTraversalEngine:
    """
    Sophisticated graph traversal engine for conflict detection
    Supports multiple algorithms and optimization strategies
    """

    def __init__(self):
        self.node_cache: Dict[str, GraphNode] = {}
        self.adjacency_cache: Dict[str, List[Tuple[str, str]]] = {}  # node_id -> [(neighbor_id, relationship_type)]
        self.query_cache: Dict[str, Any] = {}
        self.performance_stats = {"total_traversals": 0, "avg_execution_time": 0.0, "cache_hits": 0, "cache_misses": 0}

    async def clear_cache(self):
        """Clear traversal caches"""
        self.node_cache.clear()
        self.adjacency_cache.clear()
        self.query_cache.clear()
        logger.info("Graph traversal cache cleared")

    async def get_node(self, node_id: str, node_type: str) -> Optional[GraphNode]:
        """Get node from cache or database"""
        cache_key = f"{node_type}:{node_id}"

        if cache_key in self.node_cache:
            return self.node_cache[cache_key]

        # Query database for node
        query = f"""
        MATCH (n:{node_type} {{id: $node_id}})
        RETURN n
        """

        try:
            records = await connection_manager.execute_query(query, {"node_id": node_id})
            if records:
                node_data = records[0]["n"]
                node = GraphNode(node_id, node_type, dict(node_data))
                self.node_cache[cache_key] = node
                return node
        except Exception as e:
            logger.error("Failed to fetch node", node_id=node_id, node_type=node_type, error=str(e))

        return None

    async def get_adjacent_nodes(
        self,
        node_id: str,
        relationship_types: List[str] = None,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> List[Tuple[str, str]]:
        """Get adjacent nodes with relationship types"""
        cache_key = f"adj:{node_id}:{direction.value}:{','.join(relationship_types or [])}"

        if cache_key in self.adjacency_cache:
            return self.adjacency_cache[cache_key]

        # Build relationship pattern
        rel_pattern = "[:"
        if relationship_types:
            rel_pattern += "|".join(relationship_types)
        rel_pattern += "]"

        # Determine direction
        if direction == TraversalDirection.FORWARD:
            query = f"""
            MATCH (n {{id: $node_id}})-{rel_pattern}->(neighbor)
            RETURN neighbor.id as neighbor_id, 
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """
        elif direction == TraversalDirection.BACKWARD:
            query = f"""
            MATCH (neighbor)-{rel_pattern}->(n {{id: $node_id}})
            RETURN neighbor.id as neighbor_id,
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """
        else:  # BIDIRECTIONAL
            query = f"""
            MATCH (n {{id: $node_id}})-{rel_pattern}-(neighbor)
            RETURN neighbor.id as neighbor_id,
                   labels(neighbor)[0] as neighbor_type,
                   type(relationship) as rel_type
            """

        try:
            records = await connection_manager.execute_query(query, {"node_id": node_id})
            adjacent_nodes = [(record["neighbor_id"], record["rel_type"]) for record in records]
            self.adjacency_cache[cache_key] = adjacent_nodes
            return adjacent_nodes
        except Exception as e:
            logger.error("Failed to fetch adjacent nodes", node_id=node_id, error=str(e))
            return []

    async def breadth_first_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: Optional[str] = None,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> TraversalResult:
        """
        Breadth-First Search implementation
        Time Complexity: O(V + E) where V is vertices, E is edges
        Space Complexity: O(V)
        """
        start_time = time.time()
        result = TraversalResult()

        # Get start node
        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            logger.error("Start node not found", node_id=start_node_id, node_type=start_node_type)
            return result

        # Initialize BFS
        queue = deque([start_node])
        visited = {start_node_id}
        start_node.visited = True
        start_node.distance = 0
        result.add_visited_node(start_node)

        logger.info("Starting BFS traversal", start_node=start_node_id, target=target_node_id, max_depth=max_depth)

        while queue and start_node.distance < max_depth:
            current_node = queue.popleft()

            # Get adjacent nodes
            adjacent = await self.get_adjacent_nodes(current_node.id, relationship_types, direction)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)

                    # Get neighbor node
                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")  # Default to PR type
                    if not neighbor_node:
                        continue

                    neighbor_node.visited = True
                    neighbor_node.distance = current_node.distance + 1
                    neighbor_node.parent = current_node
                    result.add_visited_node(neighbor_node)

                    # Reconstruct path if target found
                    if target_node_id and neighbor_id == target_node_id:
                        path = self._reconstruct_path(neighbor_node)
                        result.add_path(path)
                        logger.info("BFS target found", path_length=len(path))

                    queue.append(neighbor_node)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.BFS.value,
            "max_depth_reached": max(start_node.distance for start_node in result.visited_nodes),
            "found_target": target_node_id is not None and any(p.id == target_node_id for p in result.visited_nodes),
        }

        self.performance_stats["total_traversals"] += 1
        self.performance_stats["avg_execution_time"] = (
            self.performance_stats["avg_execution_time"] * (self.performance_stats["total_traversals"] - 1)
            + result.execution_time
        ) / self.performance_stats["total_traversals"]

        logger.info("BFS traversal completed", nodes_visited=result.nodes_visited, execution_time=result.execution_time)

        return result

    async def depth_first_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: Optional[str] = None,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        direction: TraversalDirection = TraversalDirection.FORWARD,
    ) -> TraversalResult:
        """
        Depth-First Search implementation
        Time Complexity: O(V + E)
        Space Complexity: O(V) for recursion stack
        """
        start_time = time.time()
        result = TraversalResult()

        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            return result

        visited = set()

        logger.info("Starting DFS traversal", start_node=start_node_id, target=target_node_id, max_depth=max_depth)

        async def dfs_recursive(node: GraphNode, depth: int):
            if depth > max_depth or node.id in visited:
                return

            visited.add(node.id)
            node.visited = True
            result.add_visited_node(node)

            if target_node_id and node.id == target_node_id:
                path = self._reconstruct_path(node)
                result.add_path(path)
                return True

            # Get adjacent nodes
            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, direction)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in visited:
                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                    if neighbor_node and await dfs_recursive(neighbor_node, depth + 1):
                        return True

            return False

        # Start DFS
        await dfs_recursive(start_node, 0)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.DFS.value,
            "max_depth_reached": max(node.distance for node in result.visited_nodes),
            "found_target": target_node_id is not None and any(p.id == target_node_id for p in result.visited_nodes),
        }

        self.performance_stats["total_traversals"] += 1

        logger.info("DFS traversal completed", nodes_visited=result.nodes_visited, execution_time=result.execution_time)

        return result

    async def bidirectional_search(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 5,
    ) -> TraversalResult:
        """
        Bidirectional Search implementation
        Time Complexity: O(b^(d/2)) where b is branching factor, d is depth
        More efficient than BFS for finding shortest paths
        """
        start_time = time.time()
        result = TraversalResult()

        # Initialize both directions
        forward_queue = deque()
        backward_queue = deque()
        forward_visited = set()
        backward_visited = set()
        forward_parents = {}
        backward_parents = {}

        # Get start and target nodes
        start_node = await self.get_node(start_node_id, start_node_type)
        target_node = await self.get_node(target_node_id, "PullRequest")  # Assuming PR target

        if not start_node or not target_node:
            return result

        # Initialize both searches
        forward_queue.append(start_node)
        backward_queue.append(target_node)
        forward_visited.add(start_node_id)
        backward_visited.add(target_node_id)

        logger.info(
            "Starting bidirectional search", start_node=start_node_id, target_node=target_node_id, max_depth=max_depth
        )

        # Alternate between forward and backward search
        current_depth = 0
        while forward_queue and backward_queue and current_depth < max_depth:
            # Forward search step
            if forward_queue:
                current_level_size = len(forward_queue)
                for _ in range(current_level_size):
                    current_node = forward_queue.popleft()
                    result.add_visited_node(current_node)

                    adjacent = await self.get_adjacent_nodes(
                        current_node.id, relationship_types, TraversalDirection.FORWARD
                    )

                    for neighbor_id, rel_type in adjacent:
                        if neighbor_id not in forward_visited:
                            forward_visited.add(neighbor_id)
                            forward_parents[neighbor_id] = current_node.id

                            neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                            if neighbor_node:
                                forward_queue.append(neighbor_node)

                                # Check if found in backward search
                                if neighbor_id in backward_visited:
                                    # Reconstruct path
                                    path = self._reconstruct_bidirectional_path(
                                        neighbor_id, forward_parents, backward_parents
                                    )
                                    result.add_path(path)
                                    logger.info("Bidirectional search found path", path_length=len(path))
                                    return result

            # Backward search step
            if backward_queue:
                current_level_size = len(backward_queue)
                for _ in range(current_level_size):
                    current_node = backward_queue.popleft()
                    result.add_visited_node(current_node)

                    adjacent = await self.get_adjacent_nodes(
                        current_node.id, relationship_types, TraversalDirection.BACKWARD
                    )

                    for neighbor_id, rel_type in adjacent:
                        if neighbor_id not in backward_visited:
                            backward_visited.add(neighbor_id)
                            backward_parents[neighbor_id] = current_node.id

                            neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                            if neighbor_node:
                                backward_queue.append(neighbor_node)

                                # Check if found in forward search
                                if neighbor_id in forward_visited:
                                    # Reconstruct path
                                    path = self._reconstruct_bidirectional_path(
                                        neighbor_id, forward_parents, backward_parents
                                    )
                                    result.add_path(path)
                                    logger.info("Bidirectional search found path", path_length=len(path))
                                    return result

            current_depth += 1

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": TraversalStrategy.BIDIRECTIONAL.value,
            "max_depth_reached": current_depth,
            "found_target": False,
        }

        self.performance_stats["total_traversals"] += 1

        logger.info(
            "Bidirectional search completed without finding target",
            nodes_visited=result.nodes_visited,
            execution_time=result.execution_time,
        )

        return result

    async def detect_cycles(
        self, start_node_id: str, start_node_type: str, relationship_types: List[str] = None
    ) -> TraversalResult:
        """
        Cycle detection using DFS with backtracking
        Finds all cycles in the graph starting from given node
        """
        start_time = time.time()
        result = TraversalResult()

        visited = set()
        recursion_stack = set()

        start_node = await self.get_node(start_node_id, start_node_type)
        if not start_node:
            return result

        logger.info("Starting cycle detection", start_node=start_node_id)

        async def dfs_cycle_detection(node: GraphNode, path: List[str]):
            if node.id in recursion_stack:
                # Found a cycle
                cycle_start_idx = path.index(node.id)
                cycle_path = path[cycle_start_idx:] + [node.id]
                result.add_cycle([await self.get_node(node_id, "PullRequest") for node_id in cycle_path])
                return

            if node.id in visited:
                return

            visited.add(node.id)
            recursion_stack.add(node.id)
            path.append(node.id)

            # Explore adjacent nodes
            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, TraversalDirection.FORWARD)

            for neighbor_id, rel_type in adjacent:
                neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                if neighbor_node:
                    await dfs_cycle_detection(neighbor_node, path.copy())

            recursion_stack.remove(node.id)

        # Start cycle detection
        await dfs_cycle_detection(start_node, [])

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": "cycle_detection",
            "cycles_found": len(result.cycles),
            "total_cycles": sum(len(cycle) for cycle in result.cycles),
        }

        logger.info("Cycle detection completed", cycles_found=len(result.cycles), execution_time=result.execution_time)

        return result

    def _reconstruct_path(self, end_node: GraphNode) -> List[GraphNode]:
        """Reconstruct path from start to end node"""
        path = []
        current = end_node
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    def _reconstruct_bidirectional_path(
        self, meeting_node_id: str, forward_parents: Dict[str, str], backward_parents: Dict[str, str]
    ) -> List[GraphNode]:
        """Reconstruct path found by bidirectional search"""
        # This is a simplified version - in practice, you'd need to trace both directions
        # and combine the paths properly
        return []  # Placeholder for actual implementation

    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get traversal engine performance statistics"""
        return {
            **self.performance_stats,
            "cache_size": len(self.node_cache) + len(self.adjacency_cache),
            "queries_cached": len(self.query_cache),
        }

    async def find_shortest_path(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 10,
    ) -> TraversalResult:
        """
        Find shortest path between two nodes using bidirectional BFS
        """
        return await self.bidirectional_search(
            start_node_id, start_node_type, target_node_id, relationship_types, max_depth
        )

    async def find_all_paths(
        self,
        start_node_id: str,
        start_node_type: str,
        target_node_id: str,
        relationship_types: List[str] = None,
        max_depth: int = 10,
        max_paths: int = 100,
    ) -> TraversalResult:
        """
        Find all paths between two nodes (with limits to prevent explosion)
        """
        start_time = time.time()
        result = TraversalResult()

        start_node = await self.get_node(start_node_id, start_node_type)
        target_node = await self.get_node(target_node_id, "PullRequest")

        if not start_node or not target_node:
            return result

        paths_found = 0
        visited_paths = set()

        async def dfs_all_paths(node: GraphNode, current_path: List[str], depth: int):
            nonlocal paths_found

            if depth > max_depth or paths_found >= max_paths:
                return

            current_path_str = ":".join(current_path)
            if current_path_str in visited_paths:
                return

            visited_paths.add(current_path_str)

            if node.id == target_node_id and len(current_path) > 1:
                # Reconstruct full path
                full_path = []
                for node_id in current_path:
                    path_node = await self.get_node(node_id, "PullRequest")
                    if path_node:
                        full_path.append(path_node)

                result.add_path(full_path)
                paths_found += 1
                return

            # Explore adjacent nodes
            adjacent = await self.get_adjacent_nodes(node.id, relationship_types, TraversalDirection.FORWARD)

            for neighbor_id, rel_type in adjacent:
                if neighbor_id not in current_path:  # Avoid cycles
                    neighbor_node = await self.get_node(neighbor_id, "PullRequest")
                    if neighbor_node:
                        new_path = current_path + [neighbor_id]
                        await dfs_all_paths(neighbor_node, new_path, depth + 1)

        await dfs_all_paths(start_node, [start_node_id], 0)

        result.execution_time = time.time() - start_time
        result.metadata = {
            "strategy": "all_paths",
            "max_depth": max_depth,
            "max_paths": max_paths,
            "paths_found": len(result.paths),
        }

        return result


# Global traversal engine instance
traversal_engine = GraphTraversalEngine()
