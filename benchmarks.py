# benchmarks.py

import os, time, random, csv
from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import harmony_search_coloring, aco_coloring
from tqdm import tqdm

INST_DIR = "instances"
MAX_COLORS = 20
HS_PARAMS = dict(hms=10, hmcr=0.9, par=0.3, iterations=80)
ACO_PARAMS = dict(num_ants=20, alpha=1.0, beta=2.0, rho=0.1, iterations=80)
RUNS = 2

def run_bench(instance_path: str, writer: csv.writer):
    name = os.path.basename(instance_path)
    graph = read_dimacs_graph(instance_path)
    n = len(graph)
    for alg, func, params in [
        ("HarmonySearch", harmony_search_coloring, HS_PARAMS),
        ("AntColony",   aco_coloring,          ACO_PARAMS),
    ]:
        for i in tqdm(range(RUNS), desc=f"{alg} on {name}", leave=False):
            seed = n*1000 + i
            random.seed(seed)
            t0 = time.perf_counter()
            coloring, confs = func(graph, MAX_COLORS, **params)
            t1 = time.perf_counter()
            writer.writerow([
                name, alg, i, n, MAX_COLORS, confs, (t1 - t0)*1000
            ])

def main():
    # Prepare CSV output
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "instance", "algorithm", "run",
            "num_vertices", "max_colors",
            "conflicts", "time_ms"
        ])

        # Gather all .col files
        col_files = [f for f in os.listdir(INST_DIR) if f.endswith(".col")]
        paths = [os.path.join(INST_DIR, f) for f in col_files]

        # Read each graph once to get its size, then sort by |V|
        sized = []
        for path in paths:
            graph = read_dimacs_graph(path)
            sized.append((len(graph), path))
        sized.sort(key=lambda x: x[0])  # ascending by number of vertices

        # Run benchmarks smallest → largest
        for num_vertices, path in sized:
            fname = os.path.basename(path)
            print(f"Benchmarking {fname} (|V|={num_vertices}) …")
            run_bench(path, writer)


if __name__ == "__main__":
    main()
