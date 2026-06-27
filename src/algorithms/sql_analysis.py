"""
sql_analysis.py — Stage 3: Run 9 SQL queries against the cleaned dataset.

Method:
  - Loads data/clean/movies_clean.csv into an in-memory SQLite database.
  - Reads and executes all 9 queries from sql_queries.sql.
  - Saves each query result as a separate CSV file in output/sql/.

Queries:
  EDA (1-7): Data understanding and exploration
  RQ-tagged (8-9): Surface-level aggregation linked to research questions

Output: 9 CSV files in output/sql/

Run independently:
    python src/algorithms/sql_analysis.py
"""

import re
import sqlite3
import warnings
import pandas as pd

warnings.filterwarnings("ignore")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CLEAN_DATA_PATH, OUTPUT_SQL_DIR, SQL_QUERIES_PATH


# Map each query block to its output filename
QUERY_OUTPUT_MAP = [
    "eda_01_film_count_by_decade.csv",
    "eda_02_imdb_rating_stats.csv",
    "eda_03_metascore_stats.csv",
    "eda_04_missing_values_count.csv",
    "eda_05_top10_emotions.csv",
    "eda_06_film_count_by_era.csv",
    "eda_07_rating_distribution.csv",
    "rq1_taste_gap_top20.csv",
    "rq3_avg_score_by_era.csv",
]


def parse_queries(sql_path: str) -> list:
    """
    Read the .sql file and split it into individual query strings.
    Each query is separated by a blank line between SELECT blocks.
    Returns a list of SQL strings.
    """
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on SELECT statements (after comments)
    raw_blocks = re.split(r"\n(?=SELECT)", content)

    queries = []
    for block in raw_blocks:
        # Strip comment lines and whitespace, keep only the SELECT...;
        lines = block.strip().split("\n")
        sql_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("--") or stripped == "":
                continue
            sql_lines.append(line)
        sql = "\n".join(sql_lines).strip()
        if sql.upper().startswith("SELECT"):
            queries.append(sql)

    return queries


def run():
    """
    Entry point for Stage 3.
    Loads cleaned data into SQLite and runs all 9 queries.
    """
    # Load cleaned CSV into in-memory SQLite
    df = pd.read_csv(CLEAN_DATA_PATH)
    conn = sqlite3.connect(":memory:")
    df.to_sql("movies", conn, index=False, if_exists="replace")

    print("=" * 60)
    print("  STAGE 3: SQL ANALYSIS")
    print("=" * 60)
    print(f"  Loaded {len(df)} films into in-memory SQLite.")

    queries = parse_queries(SQL_QUERIES_PATH)

    if len(queries) != len(QUERY_OUTPUT_MAP):
        print(f"  WARNING: Expected {len(QUERY_OUTPUT_MAP)} queries, found {len(queries)}.")

    for i, (sql, filename) in enumerate(zip(queries, QUERY_OUTPUT_MAP), start=1):
        try:
            result_df = pd.read_sql_query(sql, conn)
            out_path  = os.path.join(OUTPUT_SQL_DIR, filename)
            result_df.to_csv(out_path, index=False)
            print(f"  [Query {i:2d}] {filename:<45s} -> {len(result_df)} rows")
        except Exception as e:
            print(f"  [Query {i:2d}] ERROR — {filename}: {e}")

    conn.close()
    print(f"  All results saved to: {OUTPUT_SQL_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    run()
