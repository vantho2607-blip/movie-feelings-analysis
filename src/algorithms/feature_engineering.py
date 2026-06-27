"""
feature_engineering.py — Stage 2: Create new features from the cleaned dataset.

New columns created:
  - entropy        : Shannon Entropy of the 50 emotion columns (measures emotional diversity)
  - era            : Cinema era label based on release year (Era 1–4)
  - taste_gap      : Difference between critic score and audience score (metascore/10 - imdb_rating)
  - diversity_group: Quartile group based on entropy (Low / Medium / High / Very High)

Also produces:
  - movies_normalized.csv: F1 emotion columns scaled with StandardScaler

Output:
  data/feature/movies_features.csv
  data/feature/movies_normalized.csv

Run independently:
    python src/algorithms/feature_engineering.py
"""

import warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    CLEAN_DATA_PATH, FEAT_DATA_PATH, NORM_DATA_PATH,
    F1_COLS, ERAS, AUDIENCE_COL, CRITICS_COL
)


def _shannon_entropy(row: pd.Series) -> float:
    """Compute Shannon Entropy for one row of emotion values."""
    vals = row.values.astype(float)
    total = vals.sum()
    if total == 0:
        return 0.0
    probs = vals / total
    probs = probs[probs > 0]   # Exclude zeros to avoid log(0)
    return float(-np.sum(probs * np.log2(probs)))


def _assign_era(year: int) -> str:
    """Return the era label for a given release year."""
    for label, (start, end) in ERAS.items():
        if start <= year <= end:
            return label
    return "Unknown"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived feature columns to the cleaned dataframe.
    Returns an enriched copy of the dataframe.
    """
    df = df.copy()

    # Feature 1: Shannon Entropy — measures how emotionally diverse each film is
    df["entropy"] = df[F1_COLS].apply(_shannon_entropy, axis=1)

    # Feature 2: Era label — which historical cinema era the film belongs to
    df["era"] = df["year"].apply(_assign_era)

    # Feature 3: Taste Gap — how far critics and audience diverge on a film
    # Positive = critics rate higher than audience; Negative = audience rates higher
    df["taste_gap"] = (df[CRITICS_COL] / 10.0) - df[AUDIENCE_COL]

    # Feature 4: Diversity Group — quartile bucket of emotional diversity
    df["diversity_group"] = pd.qcut(
        df["entropy"],
        q=4,
        labels=["Low (Q1)", "Medium (Q2)", "High (Q3)", "Very High (Q4)"]
    )

    return df


def run():
    """
    Entry point for Stage 2.
    Saves features CSV and normalized CSV to data/feature/.
    """
    df_clean = pd.read_csv(CLEAN_DATA_PATH)
    df_feat  = engineer_features(df_clean)

    # Save feature-enriched dataset
    df_feat.to_csv(FEAT_DATA_PATH, index=False)

    # Build normalized version: apply StandardScaler to F1 emotion columns only
    df_norm = df_feat.copy()
    scaler  = StandardScaler()
    df_norm[F1_COLS] = scaler.fit_transform(df_norm[F1_COLS].fillna(0))
    df_norm.to_csv(NORM_DATA_PATH, index=False)

    print("=" * 60)
    print("  STAGE 2: FEATURE ENGINEERING RESULTS")
    print("=" * 60)
    print(f"  Films processed             : {len(df_feat)}")
    print(f"  Entropy range               : {df_feat['entropy'].min():.3f} – {df_feat['entropy'].max():.3f}")
    print(f"  Taste Gap range             : {df_feat['taste_gap'].min():.2f} – {df_feat['taste_gap'].max():.2f}")
    print(f"  Era distribution:")
    for era, count in df_feat["era"].value_counts().sort_index().items():
        print(f"    {era:<40s}: {count} films")
    print(f"  Saved features CSV          : {FEAT_DATA_PATH}")
    print(f"  Saved normalized CSV        : {NORM_DATA_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    run()
