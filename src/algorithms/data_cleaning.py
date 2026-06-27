"""
data_cleaning.py — Stage 1: Load and clean the raw movie feelings dataset.

Process:
  1. Drop films missing all 50 emotion columns
  2. Drop films missing imdb_rating or year
  3. Fill metascore manually from missing_metascores.txt
  4. Impute remaining metascore using linear regression from tomatometer
  5. Drop films still missing metascore after imputation

Output: data/clean/movies_clean.csv

Run independently:
    python src/algorithms/data_cleaning.py
"""

import re
import warnings
import pandas as pd
from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")

# Import shared config
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    RAW_DATA_PATH, CLEAN_DATA_PATH, MANUAL_SCORES_PATH,
    F1_COLS, AUDIENCE_COL, CRITICS_COL, CRITICS_ALT
)


def load_and_clean() -> pd.DataFrame:
    """
    Load raw data and apply hybrid imputation cleaning pipeline.
    Returns the cleaned DataFrame.
    """
    df = pd.read_csv(RAW_DATA_PATH, encoding="utf-8")
    original_len = len(df)

    # Step 1: Drop films missing ALL 50 emotion columns
    df = df.dropna(subset=F1_COLS, how="all")
    dropped_emotions = original_len - len(df)

    # Step 2: Drop films missing audience score or release year
    df = df.dropna(subset=[AUDIENCE_COL, "year"])
    df["year"] = df["year"].astype(int)

    # Step 3: Fill metascore manually from missing_metascores.txt
    manual_count = 0
    if os.path.exists(MANUAL_SCORES_PATH):
        with open(MANUAL_SCORES_PATH, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r"Index:\s*(\d+).*?Metascore:\s*(\d+|N/A|___)", line)
                if match:
                    idx = int(match.group(1))
                    val = match.group(2)
                    if val.isdigit() and idx in df.index:
                        df.loc[idx, CRITICS_COL] = float(val)
                        manual_count += 1

    # Step 4: Impute missing metascore using linear regression from tomatometer
    imputed_count = 0
    train_df = df.dropna(subset=[CRITICS_COL, CRITICS_ALT])
    if not train_df.empty:
        reg = LinearRegression().fit(train_df[[CRITICS_ALT]], train_df[CRITICS_COL])
        mask = df[CRITICS_COL].isna() & df[CRITICS_ALT].notna()
        imputed_count = mask.sum()
        if imputed_count > 0:
            df.loc[mask, CRITICS_COL] = reg.predict(df.loc[mask, [CRITICS_ALT]])
            df[CRITICS_COL] = df[CRITICS_COL].round(0)

    # Step 5: Drop films still missing metascore (missing both metascore and tomatometer)
    len_before = len(df)
    df = df.dropna(subset=[CRITICS_COL])
    dropped_both = len_before - len(df)

    # Print cleaning summary
    print("=" * 60)
    print("  STAGE 1: DATA CLEANING RESULTS")
    print("=" * 60)
    print(f"  Original dataset size       : {original_len} films")
    print(f"  Dropped (missing emotions)  : {dropped_emotions} films")
    print(f"  Manually filled metascore   : {manual_count} films")
    print(f"  Imputed via regression      : {imputed_count} films")
    print(f"  Dropped (no score at all)   : {dropped_both} films")
    print(f"  Clean dataset size          : {len(df)} films ({df['year'].min()}–{df['year'].max()})")
    print("=" * 60)

    return df


def run():
    """Entry point for Stage 1. Saves cleaned data to data/clean/movies_clean.csv."""
    df = load_and_clean()
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"  Saved clean data to         : {CLEAN_DATA_PATH}")


if __name__ == "__main__":
    run()
