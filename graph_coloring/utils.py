"""Utility functions for graph coloring algorithms."""

from __future__ import annotations

__author__ = "Yusif Lastname"

import random
import time
from typing import List, Iterable

Graph = List[List[int]]
Coloring = List[int]


def count_conflicts(graph: Graph, coloring: Coloring) -> int:
    """Return the number of conflicting edges in the coloring.

    Complexity: O(E), where E is the number of edges.
    """
    conflicts = 0
    for v, neighbors in enumerate(graph):
        color_v = coloring[v] if v < len(coloring) else None
        for u in neighbors:
            if u > v and u < len(coloring) and color_v == coloring[u]:
                conflicts += 1
    return conflicts


class Timer:
    """Simple timer context manager."""

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc_info: Iterable[object]) -> None:
        end = time.perf_counter()
        self.elapsed_ms = (end - self.start) * 1000


def random_graph(num_nodes: int, edge_prob: float, rng: random.Random | None = None) -> Graph:
    """Generate a random undirected graph using edge probability.

    Complexity: O(n^2)
    """
    rng = rng or random
    graph = [[] for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if rng.random() < edge_prob:
                graph[i].append(j)
                graph[j].append(i)
    return graph
