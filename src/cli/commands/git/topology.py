"""
Topology Mapper Command Module

Implements the git-topology command for visualizing and analyzing commit relationships.
Uses NetworkX to model the repository as a Directed Acyclic Graph (DAG) and 
supports Git GraphQL for fetching pull request topology.
"""

import subprocess
import json
from argparse import Namespace
from typing import Any, Dict, List, Set, Tuple
from pathlib import Path

import networkx as nx

from ..interface import Command

class TopologyMapperCommand(Command):
    """
    Command for mapping and analyzing Git commit topology.
    
    Provides insights into branch divergence, merge bases, and "intent-drift"
    by analyzing the commit graph structure. Integrates with GitHub GraphQL API
    for remote PR dependency mapping.
    """

    def __init__(self):
        self._security_validator = None
        self._nlp = None

    @property
    def name(self) -> str:
        return "git-topology"

    @property
    def description(self) -> str:
        return "Map commit relationships, PR topology via GraphQL, and identify structural logic gaps"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--base", default="origin/main", help="Base branch for analysis")
        parser.add_argument("--head", default="HEAD", help="Head branch/commit to analyze")
        parser.add_argument("--limit", type=int, default=100, help="Max commits to traverse")
        parser.add_argument("--format", choices=["text", "json", "dot"], default="text")
        parser.add_argument("--use-graphql", action="store_true", help="Use GitHub GraphQL API for PR topology")

    def get_dependencies(self) -> Dict[str, Any]:
        return {
            "security_validator": "SecurityValidator",
            "nlp": "NLPService"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")
        self._nlp = dependencies.get("nlp")

    async def execute(self, args: Namespace) -> int:
        print(f"🕸️  Mapping Topology: {args.base} <-> {args.head}...")
        
        try:
            if args.use_graphql:
                graph = self._build_graphql_pr_graph(args.limit)
            else:
                graph = self._build_commit_graph(args.base, args.head, args.limit)
            
            if not graph:
                print("❌ Failed to build commit graph. Ensure branches are valid or gh CLI is authenticated.")
                return 1

            self._analyze_graph(graph, args.base, args.head)
            
            if args.format == "json":
                self._output_json(graph)
            
            return 0
        except Exception as e:
            print(f"Error mapping topology: {e}")
            return 1

    def _build_commit_graph(self, base: str, head: str, limit: int) -> nx.DiGraph:
        """Builds a NetworkX DAG from git rev-list."""
        G = nx.DiGraph()
        
        cmd = ["git", "rev-list", "--parents", f"--max-count={limit}", head]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        for line in result.stdout.strip().split("\n"):
            parts = line.split()
            if not parts: continue
            
            commit = parts[0]
            parents = parts[1:]
            
            G.add_node(commit)
            for p in parents:
                G.add_edge(commit, p) # Edges point from child to parent (history)
                
        return G

    def _build_graphql_pr_graph(self, limit: int) -> nx.DiGraph:
        """Builds a DAG of Pull Requests using GitHub's GraphQL API."""
        G = nx.DiGraph()
        query = f"""
        query {{
          repository(owner: "{self._get_repo_owner()}", name: "{self._get_repo_name()}") {{
            pullRequests(last: {limit}, states: OPEN) {{
              nodes {{
                number
                headRefName
                baseRefName
                title
              }}
            }}
          }}
        }}
        """
        cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            prs = data["data"]["repository"]["pullRequests"]["nodes"]
            
            for pr in prs:
                node_id = f"PR-{pr['number']}"
                G.add_node(node_id, title=pr["title"], head=pr["headRefName"], base=pr["baseRefName"])
                G.add_edge(node_id, pr["baseRefName"])
                
            print(f"Successfully fetched {len(prs)} PRs via GraphQL.")
        except Exception as e:
            print(f"GraphQL API error: {e}")
        
        return G

    def _get_repo_owner(self) -> str:
        # Fallback to some default or parse from `git remote -v`
        return "EmailIntelligence"

    def _get_repo_name(self) -> str:
        # Fallback
        return "EmailIntelligencePlatform"

    def _analyze_graph(self, G: nx.DiGraph, base: str, head: str):
        """Perform topological analysis."""
        nodes = G.number_of_nodes()
        edges = G.number_of_edges()
        print(f"✅ Graph built with {nodes} nodes and {edges} edges.")
        
        try:
            roots = [n for n, d in G.out_degree() if d == 0]
            print(f"📍 Detected {len(roots)} roots/merge bases in range.")
            
            if len(G.nodes) > 0 and nx.is_directed_acyclic_graph(G):
                longest_path = nx.dag_longest_path_length(G)
                print(f"📏 Max Depth: {longest_path} steps")
                
        except Exception as e:
            print(f"Warning during analysis: {e}")

    def _output_json(self, G: nx.DiGraph):
        data = nx.node_link_data(G)
        print(json.dumps(data, indent=2))
