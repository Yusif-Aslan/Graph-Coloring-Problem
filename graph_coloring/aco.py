
from __future__ import annotations


import math
import random
from typing import List, Tuple

from .utils import count_conflicts

Graph = List[List[int]]
Coloring = List[int]


def aco_coloring(
    graph: Graph,
    max_colors: int,
    num_ants: int,
    alpha: float,
    beta: float,
    rho: float,
    iterations: int
) -> Tuple[Coloring, int]:
    """Solve graph coloring using Ant Colony Optimization.

    :param graph: Adjacency list of the graph.
    :param max_colors: Maximum number of colors allowed.
    :param num_ants: Number of ants per iteration.
    :param alpha: Influence of pheromone.
    :param beta: Influence of heuristic information.
    :param rho: Pheromone evaporation rate.
    :param iterations: Number of iterations.
    :returns: tuple of best coloring and its conflict count.
    :complexity: Roughly O(iterations * num_ants * (V + E)).
    """
    num_vertices = len(graph)
    tau = [[1.0 for _ in range(max_colors)] for _ in range(num_vertices)]
    best_coloring: Coloring | None = None
    best_score = math.inf

    for _ in range(iterations):
        iteration_best: Coloring | None = None
        iteration_score = math.inf
        for _ in range(num_ants):
            coloring: Coloring = []
            for v in range(num_vertices):
                probs = []
                for c in range(max_colors):
                    conflicts = 0
                    for u in graph[v]:
                        if u < v and coloring[u] == c:
                            conflicts += 1
                    heuristic = 1.0 / (1 + conflicts)
                    probs.append((tau[v][c] ** alpha) * (heuristic ** beta))
                total = sum(probs)
                if total == 0:
                    color = random.randrange(max_colors)
                else:
                    r = random.random() * total
                    acc = 0.0
                    color = 0
                    for idx, p in enumerate(probs):
                        acc += p
                        if r <= acc:
                            color = idx
                            break
                coloring.append(color)
            score = count_conflicts(graph, coloring)
            if score < iteration_score:
                iteration_score = score
                iteration_best = coloring
            if score < best_score:
                best_score = score
                best_coloring = coloring
        for v in range(num_vertices):
            for c in range(max_colors):
                tau[v][c] *= (1 - rho)
        if iteration_best is not None:
            for v, color in enumerate(iteration_best):
                tau[v][color] += 1.0 / (1 + iteration_score)

    return best_coloring or [0] * num_vertices, int(best_score)
