
"""Graph parsing utilities for graph_coloring package."""

from __future__ import annotations

from typing import List

Graph = List[List[int]]


def read_graph(path: str) -> Graph:
    """Read a simple adjacency‐list text file (one line per vertex).

    Each line contains space-separated neighbor indices for a vertex.
    Lines starting with '#' or empty lines denote vertices with no neighbors.
    """
    graph: Graph = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                graph.append([])
            else:
                graph.append([int(x) for x in stripped.split()])
    return graph


def write_graph(graph: Graph, path: str) -> None:
    """Write a graph to a file in adjacency‐list format."""
    with open(path, "w", encoding="utf-8") as file:
        for neighbors in graph:
            file.write(" ".join(map(str, neighbors)) + "\n")


def read_dimacs_graph(path: str) -> Graph:
    """
    Parse a DIMACS-format .col file (ASCII).
    Lines beginning with 'c' are comments;
    'p edge N M' declares number of vertices N and edges M;
    'e u v' defines an undirected edge (1-based indices).
    """
    graph: Graph = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if not parts or parts[0] == "c":
                continue
            if parts[0] == "p":
                n = int(parts[2])
                graph = [[] for _ in range(n)]
            elif parts[0] == "e":
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                graph[u].append(v)
                graph[v].append(u)
    return graph
