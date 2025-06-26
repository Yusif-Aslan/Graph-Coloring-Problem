"""Benchmark helpers for graph coloring experiments."""

__author__ = "Yusif Lastname"

from __future__ import annotations

from typing import Any, Dict, Tuple
from graph_coloring import (
    harmony_search_coloring,
    aco_coloring,
    random_graph,
    Timer,
)

Graph = list[list[int]]


def run_harmony(graph: Graph, params: Dict[str, Any]) -> Tuple[int, float]:
    """Run Harmony Search and return (conflicts, ms)."""
    with Timer() as t:
        _, conflicts = harmony_search_coloring(graph, **params)
    return conflicts, t.elapsed_ms


def run_aco(graph: Graph, params: Dict[str, Any]) -> Tuple[int, float]:
    """Run Ant Colony Optimization and return (conflicts, ms)."""
    with Timer() as t:
        _, conflicts = aco_coloring(graph, **params)
    return conflicts, t.elapsed_ms
