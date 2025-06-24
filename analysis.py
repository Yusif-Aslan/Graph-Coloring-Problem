
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt

df = pd.read_csv("benchmark_results.csv")


conflict_summary = (
    df.groupby(["instance", "algorithm"])
      .conflicts.agg(["mean", "std"])
      .rename(columns={"mean": "mean_conflicts", "std": "std_conflicts"})
      .reset_index()
)
conflict_summary.to_csv("conflict_summary.csv", index=False)


wilcoxon_rows = []
for inst in df.instance.unique():
    sub = df[df.instance == inst]
    hs = sub[sub.algorithm == "HarmonySearch"].sort_values(
        "run").conflicts.values
    ac = sub[sub.algorithm == "AntColony"].sort_values("run").conflicts.values

    diffs = hs - ac
    if np.var(diffs) == 0:
        pval = np.nan
    else:
        _, pval = wilcoxon(hs, ac)
    wilcoxon_rows.append({"instance": inst, "wilcoxon_p": pval})

pd.DataFrame(wilcoxon_rows).to_csv("wilcoxon_results.csv", index=False)


for metric in ["conflicts", "time_ms"]:
    plt.figure()
    df.boxplot(column=metric, by="algorithm")
    plt.title(f"{metric.capitalize()} by Algorithm")
    plt.suptitle("")
    plt.xlabel("Algorithm")
    plt.ylabel(metric)
    plt.tight_layout()
    plt.savefig(f"{metric}_boxplot.png")
    plt.close()

print("Analysis complete. Tables and plots saved.")
