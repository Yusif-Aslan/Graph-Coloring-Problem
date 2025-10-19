#!/usr/bin/env python3
import os
import time
import random
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import harmony_search_coloring, aco_coloring
from tqdm import tqdm

# === CONFIGURATION ===
INST_DIR    = "instances"          
K           = 20
RUNS        = 10                   
ITER        = 50                   
HS_PARAMS   = dict(hms=10, hmcr=0.9, par=0.3, iterations=ITER)
ACO_PARAMS  = dict(num_ants=20, alpha=1.0, beta=2.0, rho=0.1, iterations=ITER)


INSTANCES = sorted(f for f in os.listdir(INST_DIR) if f.endswith(".col"))

def _run_instance_alg(args):
    fname, alg = args
    graph = read_dimacs_graph(os.path.join(INST_DIR, fname))
    rows = []
    for run in range(RUNS):
        # deterministic seed per (file, run)
        random.seed(hash(fname) ^ run)
        t0 = time.perf_counter()
        if alg == "HS":
            _, conflicts = harmony_search_coloring(graph, K, **HS_PARAMS)
            alg_name = "HarmonySearch"
        else:
            _, conflicts = aco_coloring(graph, K, **ACO_PARAMS)
            alg_name = "AntColony"
        t1 = time.perf_counter()
        rows.append([
            fname,
            alg_name,
            run,
            len(graph),
            K,
            conflicts,
            (t1 - t0) * 1000.0
        ])
    return rows

def main():
    # open CSV once
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "instance", "algorithm", "run",
            "num_vertices", "max_colors",
            "conflicts", "time_ms"
        ])

        tasks = [(fname, alg) for fname in INSTANCES for alg in ("HS", "ACO")]

        # parallel execution
        with ProcessPoolExecutor() as exe:
            futures = {exe.submit(_run_instance_alg, t): t for t in tasks}
            for future in tqdm(as_completed(futures),
                               total=len(futures),
                               desc="Benchmarking"):
                for row in future.result():
                    writer.writerow(row)

    print("Benchmarking complete → benchmark_results.csv")

if __name__ == "__main__":
    main()
