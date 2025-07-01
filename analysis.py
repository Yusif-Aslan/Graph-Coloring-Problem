#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt

# 1) Load data
df = pd.read_csv("benchmark_results.csv")

# 2) Descriptive summary
summary = (
    df.groupby(["instance", "algorithm"])
      .agg(
        mean_conflicts = ("conflicts", "mean"),
        std_conflicts  = ("conflicts", "std"),
        mean_time_ms   = ("time_ms", "mean"),
        std_time_ms    = ("time_ms", "std")
      )
      .reset_index()
)
summary.to_csv("conflict_summary.csv", index=False)

# 3) Wilcoxon signed-rank test per instance
rows = []
for inst, group in df.groupby("instance"):
    hs = group[group.algorithm=="HarmonySearch"].sort_values("run").conflicts.values
    ac = group[group.algorithm=="AntColony"   ].sort_values("run").conflicts.values
    if np.var(hs - ac) == 0:
        p = np.nan
    else:
        _, p = wilcoxon(hs, ac)
    rows.append({"instance": inst, "wilcoxon_p": p})
pd.DataFrame(rows).to_csv("wilcoxon_results.csv", index=False)

# 4) Boxplots
plt.figure()
df.boxplot(column="conflicts", by="algorithm")
plt.title("Conflicts by Algorithm")
plt.suptitle("")
plt.xlabel("Algorithm")
plt.ylabel("Conflicts")
plt.tight_layout()
plt.savefig("conflicts_boxplot.png")
plt.close()

plt.figure()
df.boxplot(column="time_ms", by="algorithm")
plt.title("Runtime (ms) by Algorithm")
plt.suptitle("")
plt.xlabel("Algorithm")
plt.ylabel("Time (ms)")
plt.tight_layout()
plt.savefig("time_ms_boxplot.png")
plt.close()

print("Analysis complete → conflict_summary.csv, wilcoxon_results.csv, and boxplots saved.")
