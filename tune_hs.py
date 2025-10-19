#!/usr/bin/env python3
import os, csv, time, random, statistics
from graph_coloring.parsing import read_dimacs_graph
from graph_coloring import harmony_search_coloring

# === CONFIG ===
INST_DIR = "instances"   
INSTANCES = [
    "queen9_9.col",
    "flat300_20_0.col",
    "DSJC500.5.col",
]
OUTPUT = "hs_tuning.csv"
RUNS = 10
ITER = 100
K = 20

# Parameter grids
HMS_LIST  = [5, 10, 20]
HMCR_LIST = [0.7, 0.8, 0.9]
PAR_LIST  = [0.1, 0.3, 0.5]

# Open output once
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "instance","HMS","HMCR","PAR",
        "mean_conflicts","std_conflicts",
        "mean_time_ms","std_time_ms"
    ])

    for fname in INSTANCES:
        inst_path = os.path.join(INST_DIR, fname)
        graph = read_dimacs_graph(inst_path)
        print("Tuning HS on", fname)
        for hms in HMS_LIST:
            for hmcr in HMCR_LIST:
                for par in PAR_LIST:
                    times, confs = [], []
                    for run in range(RUNS):
                        random.seed(run + 1000)
                        t0 = time.perf_counter()
                        _, c = harmony_search_coloring(
                            graph, max_colors=K,
                            hms=hms, hmcr=hmcr, par=par,
                            iterations=ITER
                        )
                        t1 = time.perf_counter()
                        times.append((t1-t0)*1000)
                        confs.append(c)
                    writer.writerow([
                        fname, hms, hmcr, par,
                        round(statistics.mean(confs),2),
                        round(statistics.pstdev(confs),2),
                        round(statistics.mean(times),2),
                        round(statistics.pstdev(times),2),
                    ])
print("HS tuning complete →", OUTPUT)
