#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Load HS tuning data and plot heatmap
hs = pd.read_csv("hs_tuning.csv")
flat300_hs = hs[(hs.instance == "flat300_20_0.col") & (hs.PAR == 0.3)]

# Pivot for heatmap: rows=HMS, cols=HMCR, values=mean_conflicts
pivot_hs = flat300_hs.pivot(index="HMS", columns="HMCR", values="mean_conflicts")

plt.figure(figsize=(6,5))
sns.heatmap(pivot_hs, annot=True, fmt=".1f", cmap="viridis")
plt.title("HS: mean conflicts on flat300_20_0 (PAR=0.3)")
plt.xlabel("HMCR")
plt.ylabel("HMS")
plt.savefig("hs_heatmap_flat300.png", dpi=300)
plt.close()

# 2) Load ACO tuning data and plot line chart
aco = pd.read_csv("aco_tuning.csv")
flat300_ac = aco[
    (aco.instance == "flat300_20_0.col") &
    (aco.alpha == 1.0) &
    (aco.beta == 2.0) &
    (aco.rho == 0.1)
]

plt.figure(figsize=(6,4))
sns.lineplot(
    data=flat300_ac,
    x="ants", y="mean_conflicts",
    marker="o", lw=2
)
plt.title("ACO: mean conflicts vs. #ants on flat300_20_0 (α=1, β=2, ρ=0.1)")
plt.xlabel("Number of Ants")
plt.ylabel("Mean Conflicts")
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("aco_line_flat300.png", dpi=300)
plt.close()

print("Tuning analysis complete: generated hs_heatmap_flat300.png and aco_line_flat300.png")
