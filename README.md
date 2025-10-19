# Graph Coloring with Harmony Search and ACO

__author__  "Yusif-Aslan Mammadov"

This package provides two metaheuristic algorithms for solving the
undirected graph coloring problem: **Harmony Search** and
**Ant Colony Optimization (ACO)**. The implementation targets
Python 3.8+ and includes simple utilities and tests.

## Installation

```bash
pip install -r requirements.txt
```

## Problem Description

Input graphs use the DIMACS ``.col`` format. A header ``p edge N M``
declares ``N`` vertices and ``M`` edges. Each edge is listed on a line
``e u v`` with vertices numbered from ``1``. A solution is an array of
color indices ``List[int]`` where ``coloring[v]`` stores the color of
vertex ``v``. The fitness function counts the number of conflicting
edges—edges whose endpoints share the same color. Evaluating conflicts is
``O(E)`` for ``E`` edges.

The goal is to assign a fixed set of ``k`` colors while minimizing the
conflict count.

## Algorithm Details

### Harmony Search

The harmony memory stores ``hms`` random solutions. Each iteration a new
harmony is improvised by selecting existing colors with probability
``hmcr`` and adjusting them with probability ``par``. The new solution's
conflict count is computed and, if better than the worst in memory,
replaces it.

### Ant Colony Optimization

ACO keeps a pheromone matrix ``tau[v][c]`` for vertex ``v`` and color
``c``. Ants construct colorings by choosing colors with probability
``(tau**alpha) * (heuristic**beta)`` where the heuristic is inversely
proportional to the conflicts caused. After each iteration pheromones
evaporate by ``(1 - rho)`` and the best ant reinforces its choices.

## Usage

The main API is exposed through the `graph_coloring` module.

```python
from graph_coloring import harmony_search_coloring, aco_coloring, random_graph

# generate a random graph
graph = random_graph(10, 0.3)

# Harmony Search
coloring, conflicts = harmony_search_coloring(
    graph,
    max_colors=4,
    hms=5,
    hmcr=0.9,
    par=0.3,
    iterations=100,
)

# Ant Colony Optimization
coloring, conflicts = aco_coloring(
    graph,
    max_colors=4,
    num_ants=10,
    alpha=1.0,
    beta=2.0,
    rho=0.1,
    iterations=100,
)
```

Run the demo script:

```bash
python -m graph_coloring
```

## Parameter Tuning & Experiments

Scripts ``benchmarks.py`` and ``analysis.py`` provide helpers to sweep
Harmony Search and ACO parameters. Running ``python analysis.py`` writes
CSV files with conflict counts and runtimes and produces matplotlib
plots. These experiments helped identify good defaults for ``hms``,
``hmcr``, ``par`` and for the ACO parameters ``alpha``, ``beta``,
``rho`` and ``num_ants``.

## Running Tests

```bash
pytest
```
