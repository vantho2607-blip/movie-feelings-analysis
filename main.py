"""
main.py — Master runner for the Movie Feelings Analysis pipeline.

Execution order (each stage can also run independently):
  Stage 1: data_cleaning.py       → data/clean/movies_clean.csv
  Stage 2: feature_engineering.py → data/feature/movies_features.csv
                                  → data/feature/movies_normalized.csv
  Stage 3: sql_analysis.py        → output/sql/ (9 CSV files)
  Stage 4: statistical_tests.py   → output/anova_results.csv
  Stage 5: ml_models.py           → output/model_metrics.csv

After running this file, open notebooks in src/charts/ to generate visualizations.

Usage:
    python main.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "algorithms"))

from data_cleaning      import run as run_cleaning
from feature_engineering import run as run_features
from sql_analysis        import run as run_sql
from statistical_tests   import run as run_stats
from ml_models           import run as run_models


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  MOVIE FEELINGS ANALYSIS — FULL PIPELINE")
    print("=" * 60)

    print("\n>>> STAGE 1: Data Cleaning")
    run_cleaning()

    print("\n>>> STAGE 2: Feature Engineering")
    run_features()

    print("\n>>> STAGE 3: SQL Analysis")
    run_sql()

    print("\n>>> STAGE 4: Statistical Tests")
    run_stats()

    print("\n>>> STAGE 5: ML Models & Advanced EDA")
    run_models()

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE!")
    print("  Next: open notebooks in src/charts/ to generate visualizations.")
    print("=" * 60)
