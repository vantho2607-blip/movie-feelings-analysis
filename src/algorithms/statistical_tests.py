"""
statistical_tests.py — Stage 4: Run Pearson correlation and ANOVA tests.

Tests performed:
  1. Pearson Correlation: each of the 50 emotions vs audience score (imdb_rating)
     and vs critic score (metascore). Identifies which emotions most strongly
     predict ratings.
  2. One-Way ANOVA: compare audience and critic scores across the 4 emotional
     diversity groups (Low / Medium / High / Very High). Determines whether
     emotional diversity actually affects ratings in a statistically meaningful way.

Output:
  output/anova_results.csv  — columns: [group, f_stat, p_value, significant]
  Console: full Pearson correlation table

Run independently:
    python src/algorithms/statistical_tests.py
"""

import warnings
import pandas as pd
from scipy.stats import pearsonr, f_oneway

warnings.filterwarnings("ignore")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    FEAT_DATA_PATH, OUTPUT_DIR,
    F1_COLS, EMOTION_NAMES, AUDIENCE_COL, CRITICS_COL
)

ANOVA_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "anova_results.csv")


def run_pearson_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Pearson r between each emotion and audience/critic scores.
    Returns a DataFrame with columns [emotion, r_audience, r_critics, taste_gap_r].
    """
    df_critics = df.dropna(subset=[CRITICS_COL])
    rows = []

    for col, name in zip(F1_COLS, EMOTION_NAMES):
        r_aud, p_aud = pearsonr(df[col].fillna(0), df[AUDIENCE_COL])
        r_cri, p_cri = pearsonr(df_critics[col].fillna(0), df_critics[CRITICS_COL])
        rows.append({
            "emotion":        name,
            "r_audience":     round(r_aud, 4),
            "p_audience":     round(p_aud, 4),
            "r_critics":      round(r_cri, 4),
            "p_critics":      round(p_cri, 4),
            "taste_gap_r":    round(abs(r_aud - r_cri), 4),
        })

    return pd.DataFrame(rows).sort_values("r_audience", ascending=False)


def run_anova(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-way ANOVA comparing rating scores across 4 diversity groups.
    Returns a DataFrame with columns [group, f_stat, p_value, significant].
    """
    results = []

    for score_col, label in [(AUDIENCE_COL, "Audience (IMDb)"),
                              (CRITICS_COL,  "Critics (Metascore)")]:
        df_sub = df.dropna(subset=[score_col, "diversity_group"])
        groups = [
            grp[score_col].dropna().values
            for _, grp in df_sub.groupby("diversity_group", observed=True)
        ]
        f_stat, p_value = f_oneway(*groups)
        results.append({
            "group":       label,
            "f_stat":      round(f_stat, 4),
            "p_value":     round(p_value, 6),
            "significant": p_value < 0.05,
        })

    return pd.DataFrame(results)


def run():
    """Entry point for Stage 4. Runs Pearson and ANOVA tests, saves results."""
    df = pd.read_csv(FEAT_DATA_PATH)

    print("=" * 60)
    print("  STAGE 4: STATISTICAL TESTS")
    print("=" * 60)

    # ── Pearson Correlation ─────────────────────────────────────────────────────
    print("\n  [1/2] Pearson Correlation — Emotions vs Ratings")
    corr_df = run_pearson_correlation(df)

    print(f"\n  Top 5 emotions correlated with AUDIENCE score:")
    for _, row in corr_df.head(5).iterrows():
        print(f"    {row['emotion']:<20s}  r = {row['r_audience']:+.4f}")

    print(f"\n  Top 5 emotions correlated with CRITICS score:")
    top_critics = corr_df.sort_values("r_critics", ascending=False).head(5)
    for _, row in top_critics.iterrows():
        print(f"    {row['emotion']:<20s}  r = {row['r_critics']:+.4f}")

    print(f"\n  Top 5 emotions with largest TASTE GAP (audience != critics):")
    top_gap = corr_df.sort_values("taste_gap_r", ascending=False).head(5)
    for _, row in top_gap.iterrows():
        print(f"    {row['emotion']:<20s}  |Delta r| = {row['taste_gap_r']:.4f}")

    # ── ANOVA ───────────────────────────────────────────────────────────────────
    print("\n  [2/2] ANOVA — Diversity Groups vs Ratings")
    anova_df = run_anova(df)

    for _, row in anova_df.iterrows():
        sig_label = "SIGNIFICANT (p < 0.05)" if row["significant"] else "not significant"
        print(f"    {row['group']:<25s}  F = {row['f_stat']:.4f},  p = {row['p_value']:.6f}  → {sig_label}")

    anova_df.to_csv(ANOVA_OUTPUT_PATH, index=False)
    print(f"\n  ANOVA results saved to: {ANOVA_OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    run()
