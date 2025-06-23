import pandas as pd
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt

# Load full results
df = pd.read_csv("benchmark_results.csv")

# 1) Descriptive summary
summary = df.groupby(["instance","algorithm"]).conflicts.agg(["mean","std"])
summary.to_csv("conflict_summary.csv")

# 2) Wilcoxon tests per instance
results = []
for inst in df.instance.unique():
    sub = df[df.instance==inst]
    hs = sub[sub.algorithm=="HarmonySearch"].sort_values("run").conflicts
    ac = sub[sub.algorithm=="AntColony"].sort_values("run").conflicts
    stat, p = wilcoxon(hs, ac)
    results.append({"instance":inst, "p_value":p})
pd.DataFrame(results).to_csv("wilcoxon_results.csv", index=False)

# 3) Boxplot figures
for metric in ["conflicts","time_ms"]:
    plt.figure()
    df.boxplot(column=metric, by="algorithm")
    plt.title(f"{metric} by Algorithm")
    plt.suptitle("")
    plt.savefig(f"{metric}_boxplot.png")
