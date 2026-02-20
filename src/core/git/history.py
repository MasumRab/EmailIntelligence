from typing import List, Dict, Set
from src.core.git.plumbing import GitPlumbing
from src.core.models.history import CommitNode, HistoryPlan

class DAGBuilder:
    """Builds a directed acyclic graph from git history."""
    
    def __init__(self, plumbing: GitPlumbing):
        self.plumbing = plumbing

    def build(self, base: str, head: str) -> Dict[str, CommitNode]:
        """Parse git rev-list into a DAG."""
        # Get commits between base and head
        # Format: <sha> <parent1> <parent2> ...
        result = self.plumbing._run(["rev-list", "--parents", f"{base}..{head}"])
        
        dag = {}
        for line in result.stdout.splitlines():
            parts = line.split()
            if not parts: continue
            
            oid = parts[0]
            parents = parts[1:]
            
            # Fetch message and author for completeness
            info = self.plumbing._run(["show", "-s", "--format=%an|%ct|%s", oid])
            author, timestamp, message = info.stdout.strip().split("|", 2)
            
            dag[oid] = CommitNode(
                oid=oid,
                parents=parents,
                message=message,
                author=author,
                timestamp=int(timestamp),
                is_merge=len(parents) > 1
            )
        return dag

class HistoryService:
    """Manages git history analysis and transformation."""
    
    def __init__(self, dag_builder: DAGBuilder):
        self.dag_builder = dag_builder

    def plan_rebase(self, base: str, head: str) -> HistoryPlan:
        """Generate a topologically sorted rebase plan."""
        dag = self.dag_builder.build(base, head)
        
        # In-degree calculation
        in_degree = {oid: 0 for oid in dag}
        for oid, node in dag.items():
            for parent in node.parents:
                if parent in in_degree:
                    in_degree[oid] += 1 # Wait, this is wrong. 
                    # Kahn's usually works on edges from parent to child.
        
        # Let's rebuild the logic correctly.
        # Nodes: commits. Edges: parents -> child.
        children = {oid: set() for oid in dag}
        in_degree = {oid: 0 for oid in dag}
        
        for oid, node in dag.items():
            for parent in node.parents:
                if parent in dag:
                    children[parent].add(oid)
                    in_degree[oid] += 1
        
        # Queue of nodes with in-degree 0 (roots of our subgraph)
        queue = [oid for oid, degree in in_degree.items() if degree == 0]
        sorted_oids = []
        
        while queue:
            # Sort by timestamp to preserve chronological order where possible
            queue.sort(key=lambda x: dag[x].timestamp)
            u = queue.pop(0)
            sorted_oids.append(u)
            
            for v in children[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        if len(sorted_oids) != len(dag):
            raise ValueError("Cycle detected in git history DAG (impossible in standard git).")
            
        # commits should be in reverse order for rebase (oldest first)
        # sorted_oids currently has youngest first (in-degree 0) 
        # because we worked from head towards base.
        # Actually, in-degree 0 are the ones with NO parents in the set (the oldest ones).
        
        return HistoryPlan(
            commits=[dag[oid] for oid in sorted_oids],
            base_oid=base,
            target_oid=head
        )
