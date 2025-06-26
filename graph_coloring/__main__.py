"""Command-line demonstration for graph coloring algorithms."""

from __future__ import annotations

__author__ = "Yusif Lastname"

from . import harmony_search_coloring, aco_coloring, Timer

Graph = list[list[int]]


def main() -> None:
    triangle: Graph = [[1, 2], [0, 2], [0, 1]]
    path: Graph = [[1], [0, 2], [1, 3], [2]]

    print("Harmony Search on triangle")
    with Timer() as t:
        coloring, conflicts = harmony_search_coloring(
            triangle,
            max_colors=3,
            hms=5,
            hmcr=0.9,
            par=0.3,
            iterations=100,
        )
    print(
        "Coloring: {}, conflicts: {}, time: {:.2f} ms".format(
            coloring,
            conflicts,
            t.elapsed_ms,
        )
    )

    print("ACO on path")
    with Timer() as t:
        coloring, conflicts = aco_coloring(
            path,
            max_colors=3,
            num_ants=5,
            alpha=1.0,
            beta=2.0,
            rho=0.1,
            iterations=100,
        )
    print(
        "Coloring: {}, conflicts: {}, time: {:.2f} ms".format(
            coloring,
            conflicts,
            t.elapsed_ms,
        )
    )


if __name__ == "__main__":
    main()
