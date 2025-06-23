"""Graph parsing utilities."""

from __future__ import annotations

from typing import List

Graph = List[List[int]]


def read_graph(path: str) -> Graph:
    """Read a graph from a file.

    Each line contains space-separated neighbor indices for a vertex.
    Empty lines are allowed and treated as vertices with no neighbors.
    """
    graph: Graph = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if not stripped:
                graph.append([])
            else:
                graph.append([int(x) for x in stripped.split()])
    return graph


def write_graph(graph: Graph, path: str) -> None:
    """Write a graph to a file as adjacency lists."""
    with open(path, "w", encoding="utf-8") as file:
        for neighbors in graph:
            file.write(" ".join(map(str, neighbors)) + "\n")
