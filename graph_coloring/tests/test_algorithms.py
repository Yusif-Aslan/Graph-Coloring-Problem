import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import random
from graph_coloring import (
    harmony_search_coloring,
    aco_coloring,
    random_graph,
    count_conflicts,
)


def test_empty_graph():
    graph = []
    coloring, conflicts = harmony_search_coloring(graph, 3, 2, 0.9, 0.3, 10)
    assert coloring == []
    assert conflicts == 0
    coloring, conflicts = aco_coloring(graph, 3, 2, 1.0, 2.0, 0.1, 10)
    assert coloring == []
    assert conflicts == 0


def test_single_node_graph():
    graph = [[]]
    coloring, conflicts = harmony_search_coloring(graph, 3, 2, 0.9, 0.3, 10)
    assert len(coloring) == 1
    assert conflicts == 0
    coloring, conflicts = aco_coloring(graph, 3, 2, 1.0, 2.0, 0.1, 10)
    assert len(coloring) == 1
    assert conflicts == 0


def test_random_graphs():
    rng = random.Random(0)
    for _ in range(3):
        graph = random_graph(15, 0.2, rng)
        coloring, conflicts = harmony_search_coloring(
            graph,
            max_colors=4,
            hms=5,
            hmcr=0.9,
            par=0.3,
            iterations=10,
        )
        assert len(coloring) == len(graph)
        assert conflicts == count_conflicts(graph, coloring)
        coloring, conflicts = aco_coloring(
            graph,
            max_colors=4,
            num_ants=5,
            alpha=1.0,
            beta=2.0,
            rho=0.1,
            iterations=5,
        )
        assert len(coloring) == len(graph)
        assert conflicts == count_conflicts(graph, coloring)
