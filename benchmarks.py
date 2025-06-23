# benchmarks.py

import os, time, random, csv
from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import harmony_search_coloring, aco_coloring
from tqdm import tqdm

INST_DIR = "instances"
MAX_COLORS = 20
HS_PARAMS = dict(hms=10, hmcr=0.9, par=0.3, iterations=500)
ACO_PARAMS = dict(num_ants=20, alpha=1.0, beta=2.0, rho=0.1, iterations=500)
RUNS = 30

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
    with open("benchmark_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instance","algorithm","run","V","K","conflicts","time_ms"])
        for fname in sorted(os.listdir(INST_DIR)):
            if not fname.endswith(".col"): continue
            path = os.path.join(INST_DIR, fname)
            print(f"Running {fname}…")
            run_bench(path, w)

if __name__ == "__main__":
    main()
