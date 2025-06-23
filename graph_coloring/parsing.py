# graph_coloring/parsing.py

from __future__ import annotations
from typing import List

Graph = List[List[int]]

def read_graph(path: str) -> Graph:
    """Read a simple adjacency‐list text file (one line per vertex)."""
    graph: Graph = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                graph.append([])
            else:
                graph.append([int(x) for x in stripped.split()])
    return graph

def write_graph(graph: Graph, path: str) -> None:
    """Write an adjacency list to a file (one line per vertex)."""
    with open(path, "w", encoding="utf-8") as f:
        for nbrs in graph:
            f.write(" ".join(map(str, nbrs)) + "\n")

def read_dimacs_graph(path: str) -> Graph:
    """
    Parse a DIMACS-format .col file (ASCII).
    - Lines starting with 'c' are comments.
    - A line 'p edge N M' declares number of vertices (N) and edges (M).
    - Lines 'e u v' define an undirected edge (1-based indices).
    """
    graph: Graph = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if not parts or parts[0] == "c":
                continue
            if parts[0] == "p":
                # initialize adjacency list
                n = int(parts[2])
                graph = [[] for _ in range(n)]
            elif parts[0] == "e":
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                graph[u].append(v)
                graph[v].append(u)
    return graph
