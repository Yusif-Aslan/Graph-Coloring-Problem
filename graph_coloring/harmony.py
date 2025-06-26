"""Harmony Search algorithm for graph coloring."""

from __future__ import annotations

__author__ = "Yusif Lastname"

import random
from typing import List, Tuple

from .utils import count_conflicts

Graph = List[List[int]]
Coloring = List[int]


def harmony_search_coloring(
    graph: Graph,
    max_colors: int,
    hms: int,
    hmcr: float,
    par: float,
    iterations: int
) -> Tuple[Coloring, int]:
    """Solve graph coloring using Harmony Search.

    :param graph: Adjacency list of the graph.
    :param max_colors: Maximum number of colors allowed.
    :param hms: Harmony memory size.
    :param hmcr: Harmony memory consideration rate.
    :param par: Pitch adjustment rate.
    :param iterations: Number of improvization iterations.
    :returns: tuple of best coloring and its conflict count.
    :complexity: Roughly O(iterations * (hms + V + E)).
    """
    num_vertices = len(graph)
    memory: List[Coloring] = [
        [random.randrange(max_colors) for _ in range(num_vertices)]
        for _ in range(hms)
    ]
    scores = [count_conflicts(graph, sol) for sol in memory]

    for _ in range(iterations):
        new_sol: Coloring = []
        for v in range(num_vertices):
            if random.random() < hmcr and memory:
                color = random.choice(memory)[v]
            else:
                color = random.randrange(max_colors)
            if random.random() < par:
                color = random.randrange(max_colors)
            new_sol.append(color)
        new_score = count_conflicts(graph, new_sol)
        worst_idx = max(range(hms), key=lambda i: scores[i])
        if new_score < scores[worst_idx]:
            memory[worst_idx] = new_sol
            scores[worst_idx] = new_score

    best_idx = min(range(hms), key=lambda i: scores[i])
    return memory[best_idx], scores[best_idx]
