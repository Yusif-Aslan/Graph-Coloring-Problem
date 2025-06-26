"""Parameter sweep experiments for Harmony Search and ACO."""

__author__ = "Yusif Lastname"

from __future__ import annotations

import csv
from itertools import product
from typing import Iterable

import matplotlib.pyplot as plt

from graph_coloring import random_graph
from benchmarks import run_harmony, run_aco


def tune_hs() -> None:
    """Explore Harmony Search parameters and save a plot."""
    graph = random_graph(20, 0.2)
    hms_values = [3, 5, 7]
    hmcr_values = [0.7, 0.9]
    par_values = [0.1, 0.3]
    rows: list[list[float]] = []
    for hms, hmcr, par in product(hms_values, hmcr_values, par_values):
        params = dict(max_colors=4, hms=hms, hmcr=hmcr, par=par, iterations=50)
        conflicts, ms = run_harmony(graph, params)
        rows.append([hms, hmcr, par, conflicts, ms])
    with open("hs_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hms", "hmcr", "par", "conflicts", "ms"])
        writer.writerows(rows)
    hms_list = [r[0] for r in rows if r[1] == 0.9 and r[2] == 0.3]
    conflicts_list = [r[3] for r in rows if r[1] == 0.9 and r[2] == 0.3]
    plt.plot(hms_list, conflicts_list, marker="o")
    plt.xlabel("HMS")
    plt.ylabel("Conflicts")
    plt.title("Harmony Search Parameter Sweep")
    plt.savefig("hs_plot.png")


def tune_aco() -> None:
    """Explore ACO parameters and save a plot."""
    graph = random_graph(20, 0.2)
    alpha_values = [0.5, 1.0, 1.5]
    beta_values = [1.0, 2.0]
    rho_values = [0.1, 0.3]
    rows: list[list[float]] = []
    for alpha, beta, rho in product(alpha_values, beta_values, rho_values):
        params = dict(
            max_colors=4,
            num_ants=10,
            alpha=alpha,
            beta=beta,
            rho=rho,
            iterations=50,
        )
        conflicts, ms = run_aco(graph, params)
        rows.append([alpha, beta, rho, conflicts, ms])
    with open("aco_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["alpha", "beta", "rho", "conflicts", "ms"])
        writer.writerows(rows)
    alpha_list = [r[0] for r in rows if r[1] == 2.0 and r[2] == 0.1]
    conflicts_list = [r[3] for r in rows if r[1] == 2.0 and r[2] == 0.1]
    plt.figure()
    plt.plot(alpha_list, conflicts_list, marker="o")
    plt.xlabel("alpha")
    plt.ylabel("Conflicts")
    plt.title("ACO Parameter Sweep")
    plt.savefig("aco_plot.png")


if __name__ == "__main__":
    tune_hs()
    tune_aco()
