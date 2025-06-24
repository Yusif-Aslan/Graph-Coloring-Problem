import os
import time
import random
import csv
from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import harmony_search_coloring, aco_coloring
from tqdm import tqdm

# Directory of .col files
INST_DIR = os.path.join(os.path.dirname(__file__),
                        "graph_coloring", "instances")

# Experiment settings
MAX_COLORS = 30
RUNS = 2
HS_PARAMS = dict(hms=10, hmcr=0.9, par=0.3, iterations=500)
ACO_PARAMS = dict(num_ants=20, alpha=1.0, beta=2.0, rho=0.1, iterations=500)


def run_bench(instance_path: str, writer: csv.writer):
    """Run both HS and ACO on one instance for RUNS repetitions."""
    name = os.path.basename(instance_path)
    graph = read_dimacs_graph(instance_path)
    n = len(graph)

    for alg, func, params in [
        ("HarmonySearch", harmony_search_coloring, HS_PARAMS),
        ("AntColony",    aco_coloring,          ACO_PARAMS),
    ]:
        for i in tqdm(range(RUNS), desc=f"{alg} on {name}", leave=False):
            seed = n * 1000 + i
            random.seed(seed)

            t0 = time.perf_counter()
            coloring, conflicts = func(graph, MAX_COLORS, **params)
            t1 = time.perf_counter()

            writer.writerow([
                name, alg, i, n, MAX_COLORS,
                conflicts, (t1 - t0) * 1000.0
            ])


def main():
    # Prepare output CSV
    out_path = os.path.join(os.path.dirname(__file__), "benchmark_results.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "instance", "algorithm", "run",
            "num_vertices", "max_colors",
            "conflicts", "time_ms"
        ])

        col_files = [
            f for f in os.listdir(INST_DIR)
            if f.endswith(".col")
        ]
        sized = []
        for f in col_files:
            path = os.path.join(INST_DIR, f)
            g = read_dimacs_graph(path)
            sized.append((len(g), path))
        sized.sort(key=lambda x: x[0])

        for num_vertices, path in sized:
            fname = os.path.basename(path)
            print(f"Benchmarking {fname} (|V|={num_vertices}) …")
            run_bench(path, writer)


if __name__ == "__main__":
    main()
