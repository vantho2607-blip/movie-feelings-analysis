"""
ml_models.py — Stage 5: Train 5 regression models and run PCA/KMeans clustering.

Part A — 5 Regression Models (predict imdb_rating from 50 emotion features):
  1. Linear Regression   — simple baseline
  2. Ridge Regression    — regularized linear (prevents overfitting, alpha=1.0)
  3. Polynomial deg-2    — captures non-linear relationships
  4. Random Forest       — ensemble of 100 decision trees
  5. SVR (RBF kernel)    — support vector regression for high-dimensional data

Part B — PCA + KMeans (Advanced EDA — NOT preprocessing for the models above):
  - Reduces 50 emotion dimensions to 2 principal components for visualization.
  - KMeans clusters films into 3 groups to discover natural "movie types".
  - Output: scatter plot saved to output/charts/adv_pca_clusters.png

Output:
  output/model_metrics.csv  — columns: [model_name, r2, mse, rmse, notes]
  Console: ranked model comparison table

Run independently:
    python src/algorithms/ml_models.py
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model    import LinearRegression, Ridge
from sklearn.preprocessing   import PolynomialFeatures
from sklearn.pipeline        import make_pipeline
from sklearn.ensemble        import RandomForestRegressor
from sklearn.svm             import SVR
from sklearn.metrics         import r2_score, mean_squared_error
from sklearn.cluster         import KMeans
from sklearn.decomposition   import PCA

warnings.filterwarnings("ignore")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    FEAT_DATA_PATH, OUTPUT_DIR, OUTPUT_CHART_DIR,
    F1_COLS, EMOTION_NAMES, AUDIENCE_COL
)

METRICS_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "model_metrics.csv")


def train_regression_models(df: pd.DataFrame) -> pd.DataFrame:
    """
    Train all 5 regression models to predict imdb_rating from 50 emotion features.
    Returns a DataFrame with performance metrics for each model.
    """
    X = df[F1_COLS].fillna(0).values
    y = df[AUDIENCE_COL].values

    models = {
        "Linear Regression":   LinearRegression(),
        "Ridge Regression":    Ridge(alpha=1.0),
        "Polynomial (deg-2)":  make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
        "Random Forest":       RandomForestRegressor(n_estimators=100, random_state=42),
        "SVR (RBF)":           SVR(kernel="rbf", C=1.0, epsilon=0.1),
    }

    rows = []
    for name, model in models.items():
        model.fit(X, y)
        y_pred = model.predict(X)
        r2   = r2_score(y, y_pred)
        mse  = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        rows.append({
            "model_name": name,
            "r2":         round(r2, 4),
            "mse":        round(mse, 6),
            "rmse":       round(rmse, 4),
            "notes":      "Train set performance (in-sample)",
        })

    metrics_df = pd.DataFrame(rows).sort_values("r2", ascending=False).reset_index(drop=True)
    return metrics_df


def run_pca_clustering(df: pd.DataFrame):
    """
    PCA + KMeans Advanced EDA:
    Reduces 50 emotion dimensions to 2 components for visualization.
    Clusters films into 3 groups. Saves scatter plot to output/charts/.

    NOTE: This is purely exploratory — the clusters are NOT used as input
    to any of the 5 regression models above.
    """
    X = df[F1_COLS].fillna(0).values

    # KMeans: discover 3 natural film clusters based on emotion profile
    kmeans   = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # PCA: compress 50D → 2D for plotting
    pca   = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(
        X_pca[:, 0], X_pca[:, 1],
        c=clusters, cmap="viridis", alpha=0.6, s=20
    )
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)", fontsize=12)
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)", fontsize=12)
    ax.set_title("Film Clusters Based on 50 Emotion Features (KMeans + PCA)", fontsize=14)
    handles, _ = scatter.legend_elements()
    ax.legend(handles, ["Cluster 1", "Cluster 2", "Cluster 3"], title="Clusters")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_CHART_DIR, "adv_pca_clusters.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  PCA cluster plot saved: {out_path}")

    total_variance = sum(pca.explained_variance_ratio_[:2]) * 100
    print(f"  PCA explains {total_variance:.1f}% of total variance (PC1 + PC2)")
    return clusters, X_pca


def run():
    """Entry point for Stage 5. Trains models, saves metrics, runs PCA/KMeans."""
    df = pd.read_csv(FEAT_DATA_PATH)

    print("=" * 60)
    print("  STAGE 5: ML MODELS & ADVANCED EDA")
    print("=" * 60)

    # Part A: Train 5 regression models
    print("\n  [1/2] Training 5 Regression Models...")
    metrics_df = train_regression_models(df)

    print(f"\n  {'Model':<25s}  {'R²':>8}  {'MSE':>10}  {'RMSE':>8}")
    print("  " + "-" * 55)
    for _, row in metrics_df.iterrows():
        best_marker = " ← BEST" if row.name == 0 else ""
        print(f"  {row['model_name']:<25s}  {row['r2']:>+8.4f}  {row['mse']:>10.6f}  {row['rmse']:>8.4f}{best_marker}")

    metrics_df.to_csv(METRICS_OUTPUT_PATH, index=False)
    print(f"\n  Model metrics saved to: {METRICS_OUTPUT_PATH}")

    # Part B: PCA + KMeans (Advanced EDA)
    print("\n  [2/2] Running PCA + KMeans Clustering (Advanced EDA)...")
    run_pca_clustering(df)

    print("=" * 60)


if __name__ == "__main__":
    run()
