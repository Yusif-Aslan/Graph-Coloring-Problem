#!/usr/bin/env python3
import os
import csv
import time
import random
import statistics
from concurrent.futures import ProcessPoolExecutor, as_completed

from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import aco_coloring
from tqdm import tqdm

# === CONFIG ===
INST_DIR = "instances"
INSTANCES = [
    "queen9_9.col",
    "flat300_20_0.col",
    "DSJC500.5.col",
]
OUTPUT = "aco_tuning_fast.csv"
RUNS = 5         
ITER = 50         
K = 20

ANTS_LIST = [10, 30]
ALPHAS    = [1.0, 2.0]
BETAS     = [2.0, 5.0]
RHOST     = [0.1, 0.3]

tasks = []
for fname in INSTANCES:
    graph = read_dimacs_graph(os.path.join(INST_DIR, fname))
    for m in ANTS_LIST:
        for a in ALPHAS:
            for b in BETAS:
                for rho in RHOST:
                    tasks.append((fname, graph, m, a, b, rho))

def tune_one(params):
    fname, graph, m, a, b, rho = params
    times, confs = [], []
    for run in range(RUNS):
        random.seed(run + 2000)
        t0 = time.perf_counter()
        _, c = aco_coloring(
            graph,
            max_colors=K,
            num_ants=m,
            alpha=a,
            beta=b,
            rho=rho,
            iterations=ITER
        )
        times.append((time.perf_counter() - t0) * 1000)
        confs.append(c)
    return {
        "instance": fname,
        "ants": m,
        "alpha": a,
        "beta": b,
        "rho": rho,
        "mean_conflicts": round(statistics.mean(confs),2),
        "std_conflicts":   round(statistics.pstdev(confs),2),
        "mean_time_ms":    round(statistics.mean(times),2),
        "std_time_ms":     round(statistics.pstdev(times),2),
    }

def main():
    # Open CSV and write header
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "instance","ants","alpha","beta","rho",
            "mean_conflicts","std_conflicts",
            "mean_time_ms","std_time_ms"
        ])

        # Parallel execution
        with ProcessPoolExecutor() as exe:
            futures = {exe.submit(tune_one, task): task for task in tasks}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Tuning ACO"):
                result = future.result()
                writer.writerow([
                    result["instance"],
                    result["ants"],
                    result["alpha"],
                    result["beta"],
                    result["rho"],
                    result["mean_conflicts"],
                    result["std_conflicts"],
                    result["mean_time_ms"],
                    result["std_time_ms"],
                ])

    print("Fast ACO tuning complete →", OUTPUT)

if __name__ == "__main__":
    main()
