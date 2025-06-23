# Graph Coloring with Harmony Search and ACO

This package provides two metaheuristic algorithms for solving the
undirected graph coloring problem: **Harmony Search** and
**Ant Colony Optimization (ACO)**. The implementation targets
Python 3.8+ and includes simple utilities and tests.

## Installation

```bash
pip install -r requirements.txt
```

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

## Running Tests

```bash
pytest
```

