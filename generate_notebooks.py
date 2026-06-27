"""
generate_notebooks.py — Helper script to create 4 Jupyter Notebooks for the charts.
Run once: python generate_notebooks.py
"""
import json, os

def make_nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"}
        },
        "cells": cells
    }

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def code(src):
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None}


# ─────────────────────────────────────────────────────────────────────────────
# chart_rq1.ipynb
# ─────────────────────────────────────────────────────────────────────────────
nb1_setup = """import sys, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

PROJECT = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT, "src", "algorithms"))
from config import FEAT_DATA_PATH, OUTPUT_CHART_DIR, F1_COLS, EMOTION_NAMES, AUDIENCE_COL, CRITICS_COL

df = pd.read_csv(FEAT_DATA_PATH)
print(f"Loaded {len(df)} films")"""

nb1_chart1 = """emotion_means = df[F1_COLS].mean().sort_values(ascending=False)
emotion_means.index = EMOTION_NAMES
top10 = emotion_means.head(10)

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(top10.index[::-1], top10.values[::-1], color=sns.color_palette("viridis", 10))
ax.set_xlabel("Average Emotion Intensity (f1 score)", fontsize=12)
ax.set_title("Top 10 Most Prevalent Emotions in Cinema (1920-2024)", fontsize=14)
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "rq1_top10_emotions.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved: {out}")"""

nb1_chart2 = """df_critics = df.dropna(subset=[CRITICS_COL])
aud_corr, cri_corr = {}, {}
for col, name in zip(F1_COLS, EMOTION_NAMES):
    r_a, _ = pearsonr(df[col].fillna(0), df[AUDIENCE_COL])
    r_c, _ = pearsonr(df_critics[col].fillna(0), df_critics[CRITICS_COL])
    aud_corr[name] = r_a
    cri_corr[name] = r_c

import pandas as pd
corr_df = pd.DataFrame({"Audience (IMDb)": aud_corr, "Critics (Metascore)": cri_corr})
corr_df = corr_df.sort_values("Audience (IMDb)", ascending=False)

fig, ax = plt.subplots(figsize=(10, 14))
x = range(len(corr_df))
ax.barh(x, corr_df["Audience (IMDb)"], alpha=0.75, label="Audience (IMDb)", color="#4C72B0")
ax.barh([i+0.4 for i in x], corr_df["Critics (Metascore)"],
        alpha=0.75, label="Critics (Metascore)", color="#DD8452", height=0.4)
ax.set_yticks([i+0.2 for i in x])
ax.set_yticklabels(corr_df.index, fontsize=8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Pearson Correlation Coefficient (r)", fontsize=12)
ax.set_title("Taste Asymmetry: Emotion Correlation with Ratings (RQ1)", fontsize=13)
ax.legend(fontsize=11)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "rq1_audience_vs_critics.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved: {out}")"""

nb1 = make_nb([
    md("# RQ1 Charts\n**Top 10 Emotions & Audience vs Critics Correlation**\n\nReads from `data/feature/movies_features.csv`."),
    code(nb1_setup),
    md("## Chart 1 — Top 10 Most Prevalent Emotions"),
    code(nb1_chart1),
    md("## Chart 2 — Pearson Correlation: Audience vs Critics"),
    code(nb1_chart2),
])


# ─────────────────────────────────────────────────────────────────────────────
# chart_rq2.ipynb
# ─────────────────────────────────────────────────────────────────────────────
nb2_setup = """import sys, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT, "src", "algorithms"))
from config import FEAT_DATA_PATH, OUTPUT_DIR, OUTPUT_CHART_DIR, AUDIENCE_COL, CRITICS_COL

df = pd.read_csv(FEAT_DATA_PATH)
anova_df = pd.read_csv(os.path.join(OUTPUT_DIR, "anova_results.csv"))
print(f"Loaded {len(df)} films")
print(anova_df)"""

nb2_chart1 = """ERA_ORDER = ["Low (Q1)", "Medium (Q2)", "High (Q3)", "Very High (Q4)"]
row_aud = anova_df[anova_df["group"].str.contains("Audience")].iloc[0]
row_cri = anova_df[anova_df["group"].str.contains("Critics")].iloc[0]
f_aud, p_aud = row_aud["f_stat"], row_aud["p_value"]
f_cri, p_cri = row_cri["f_stat"], row_cri["p_value"]

df_cri = df.dropna(subset=[CRITICS_COL])

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

sns.boxplot(data=df, x="diversity_group", y=AUDIENCE_COL, ax=axes[0],
            palette="Blues", order=ERA_ORDER)
axes[0].set_title("Emotional Diversity vs Audience Score (IMDb)", fontsize=12)
axes[0].set_xlabel("Emotional Diversity Group (Shannon Entropy)")
axes[0].set_ylabel("IMDb Rating")
axes[0].annotate(f"ANOVA: F={f_aud:.2f}, p={p_aud:.4f}",
                 xy=(0.02, 0.97), xycoords="axes fraction", fontsize=9, va="top",
                 color="red" if p_aud < 0.05 else "gray")

sns.boxplot(data=df_cri, x="diversity_group", y=CRITICS_COL, ax=axes[1],
            palette="Oranges", order=ERA_ORDER)
axes[1].set_title("Emotional Diversity vs Critic Score (Metascore)", fontsize=12)
axes[1].set_xlabel("Emotional Diversity Group (Shannon Entropy)")
axes[1].set_ylabel("Metascore")
axes[1].annotate(f"ANOVA: F={f_cri:.2f}, p={p_cri:.4f}",
                 xy=(0.02, 0.97), xycoords="axes fraction", fontsize=9, va="top",
                 color="red" if p_cri < 0.05 else "gray")

plt.suptitle("RQ2: Emotional Diversity and Film Rating Scores", fontsize=14, y=1.02)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "rq2_diversity_boxplot.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out}")"""

nb2 = make_nb([
    md("# RQ2 Charts\n**Emotional Diversity Boxplots & ANOVA Visualization**\n\nReads from `data/feature/movies_features.csv` and `output/anova_results.csv`."),
    code(nb2_setup),
    md("## Chart 1 — Diversity Boxplots (Audience & Critics)"),
    code(nb2_chart1),
])


# ─────────────────────────────────────────────────────────────────────────────
# chart_rq3.ipynb
# ─────────────────────────────────────────────────────────────────────────────
nb3_setup = """import sys, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score

PROJECT = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT, "src", "algorithms"))
from config import FEAT_DATA_PATH, OUTPUT_DIR, OUTPUT_CHART_DIR, F1_COLS, EMOTION_NAMES, ERAS

df = pd.read_csv(FEAT_DATA_PATH)
metrics_df = pd.read_csv(os.path.join(OUTPUT_DIR, "model_metrics.csv"))
print(f"Loaded {len(df)} films")
print(metrics_df[["model_name","r2","rmse"]])"""

nb3_chart1 = """era_order = list(ERAS.keys())
era_means = df.groupby("era")[F1_COLS].mean()
era_means = era_means.reindex([e for e in era_order if e in era_means.index])
era_means.columns = EMOTION_NAMES

year_means = df.groupby("year")[F1_COLS].mean()
year_means.columns = EMOTION_NAMES
top8 = year_means.std().sort_values(ascending=False).head(8).index.tolist()

fig, ax = plt.subplots(figsize=(14, 8))
x_pos = range(len(era_means))
colors = sns.color_palette("tab10", len(top8))
for i, emo in enumerate(top8):
    if emo in era_means.columns:
        ax.plot(x_pos, era_means[emo].values, marker="o", label=emo, color=colors[i], linewidth=2)
ax.set_xticks(list(x_pos))
ax.set_xticklabels(list(era_means.index), fontsize=9)
ax.set_xlabel("Cinema Era", fontsize=12)
ax.set_ylabel("Average Emotion Score (f1)", fontsize=12)
ax.set_title("RQ3: Emotion Shifts Across 4 Cinema Eras", fontsize=14)
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "rq3_era_trend_line.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out}")"""

nb3_chart2 = """EMOTIONS_TO_FORECAST = ["nostalgia", "catharsis", "anger"]
future_years = np.arange(2025, 2036)

models_dict = {
    "Linear Regression":  LinearRegression(),
    "Ridge Regression":   Ridge(alpha=1.0),
    "Polynomial (deg-2)": make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
    "Random Forest":      RandomForestRegressor(n_estimators=100, random_state=42),
    "SVR (RBF)":          SVR(kernel="rbf", C=1.0, epsilon=0.1),
}

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, emo in zip(axes, EMOTIONS_TO_FORECAST):
    if emo not in year_means.columns:
        continue
    series = year_means[emo].dropna()
    emo_years = np.array(series.index)
    values = series.values
    all_years = np.concatenate([emo_years, future_years])

    ax.scatter(emo_years, values, alpha=0.4, s=15, color="gray", label="Original data")
    colors5 = sns.color_palette("muted", 5)
    best_r2, best_name, best_model = -999, "", None

    for i, (name, model) in enumerate(models_dict.items()):
        model.fit(emo_years.reshape(-1, 1), values)
        y_all = model.predict(all_years.reshape(-1, 1))
        r2 = r2_score(values, model.predict(emo_years.reshape(-1, 1)))
        ax.plot(all_years, y_all, alpha=0.35, linewidth=1, color=colors5[i], linestyle="--")
        if r2 > best_r2:
            best_r2, best_name, best_model = r2, name, model

    y_best = best_model.predict(all_years.reshape(-1, 1))
    ax.plot(all_years, y_best, linewidth=2.5, color="crimson",
            label=f"Best: {best_name}")
    ax.axvline(2024.5, color="black", linestyle=":", linewidth=1.2, label="Year 2024")
    ax.set_title(f"Emotion: {emo.capitalize()}", fontsize=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg f1 Score")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

plt.suptitle("RQ3: 5-Model Forecast of Emotion Trajectories (2025-2035)", fontsize=14)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "rq3_5models_forecast.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out}")"""

nb3 = make_nb([
    md("# RQ3 Charts\n**Era Trend Lines & 5-Model Forecast Comparison**\n\nReads from `data/feature/movies_features.csv` and `output/model_metrics.csv`."),
    code(nb3_setup),
    md("## Chart 1 — Era Trend Lines (Top 8 Volatile Emotions)"),
    code(nb3_chart1),
    md("## Chart 2 — 5-Model Forecast Comparison"),
    code(nb3_chart2),
])


# ─────────────────────────────────────────────────────────────────────────────
# chart_advanced.ipynb
# ─────────────────────────────────────────────────────────────────────────────
nb4_setup = """import sys, os
from math import pi
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

PROJECT = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT, "src", "algorithms"))
from config import FEAT_DATA_PATH, NORM_DATA_PATH, OUTPUT_CHART_DIR, F1_COLS, EMOTION_NAMES, ERAS

df = pd.read_csv(FEAT_DATA_PATH)
df_norm = pd.read_csv(NORM_DATA_PATH)
print(f"Loaded {len(df)} films")"""

nb4_heatmap = """top15_cols = df[F1_COLS].mean().sort_values(ascending=False).head(15).index
corr = df[top15_cols].corr()
labels = [c.replace("f1_", "") for c in top15_cols]

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            xticklabels=labels, yticklabels=labels, ax=ax)
ax.set_title("Emotion Correlation Matrix (Top 15 Most Common Emotions)", fontsize=15)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "adv_emotion_heatmap.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved: {out}")"""

nb4_radar = """era1_key = [k for k in ERAS if "1920" in k][0]
era4_key = [k for k in ERAS if "2001" in k][0]
era_means = df.groupby("era")[F1_COLS].mean()
top8_cols = df[F1_COLS].mean().sort_values(ascending=False).head(8).index
categories = [c.replace("f1_", "") for c in top8_cols]
N = len(categories)

if era1_key in era_means.index and era4_key in era_means.index:
    v1 = era_means.loc[era1_key, top8_cols].values.flatten().tolist()
    v4 = era_means.loc[era4_key, top8_cols].values.flatten().tolist()
    v1 += v1[:1]
    v4 += v4[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, v1, linewidth=2, label="Era 1 (Classic 1920-1950)")
    ax.fill(angles, v1, alpha=0.25)
    ax.plot(angles, v4, linewidth=2, label="Era 4 (Modern 2001-2024)")
    ax.fill(angles, v4, alpha=0.25)
    plt.xticks(angles[:-1], categories, size=11)
    ax.set_title("Emotional DNA: Classic vs Modern Cinema", size=15, y=1.1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    out = os.path.join(OUTPUT_CHART_DIR, "adv_radar_chart.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved: {out}")
else:
    print("Era data not found. Check movies_features.csv era column values.")
    print("Available eras:", list(era_means.index))"""

nb4_pca = """X = df_norm[F1_COLS].fillna(0).values
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)

var1 = round(pca.explained_variance_ratio_[0] * 100, 1)
var2 = round(pca.explained_variance_ratio_[1] * 100, 1)

fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap="viridis", alpha=0.6, s=20)
ax.set_xlabel(f"PC1 ({var1}% variance)", fontsize=12)
ax.set_ylabel(f"PC2 ({var2}% variance)", fontsize=12)
ax.set_title("Film Clusters Based on 50 Emotion Features (KMeans + PCA)", fontsize=14)
handles, _ = scatter.legend_elements()
ax.legend(handles, ["Cluster 1", "Cluster 2", "Cluster 3"], title="Clusters")
ax.grid(alpha=0.3)
plt.tight_layout()
out = os.path.join(OUTPUT_CHART_DIR, "adv_pca_clusters.png")
fig.savefig(out, dpi=150)
plt.close(fig)
print(f"Saved: {out}")
print(f"Total variance explained: {var1 + var2}%")"""

nb4 = make_nb([
    md("# Advanced Charts\n**Emotion Heatmap | Radar Chart (Era 1 vs Era 4) | PCA Clusters**\n\nReads from `data/feature/movies_features.csv` and `data/feature/movies_normalized.csv`."),
    code(nb4_setup),
    md("## Chart 1 — Top 15 Emotion Correlation Heatmap"),
    code(nb4_heatmap),
    md("## Chart 2 — Radar Chart: Era 1 vs Era 4 Emotional DNA"),
    code(nb4_radar),
    md("## Chart 3 — PCA Cluster Scatter (from normalized emotion data)"),
    code(nb4_pca),
])


# ─────────────────────────────────────────────────────────────────────────────
# Write all notebooks
# ─────────────────────────────────────────────────────────────────────────────
notebooks = [
    ("src/charts/chart_rq1.ipynb",      nb1),
    ("src/charts/chart_rq2.ipynb",      nb2),
    ("src/charts/chart_rq3.ipynb",      nb3),
    ("src/charts/chart_advanced.ipynb", nb4),
]

for path, nb in notebooks:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Created: {path}")

print("All 4 notebooks created successfully.")
