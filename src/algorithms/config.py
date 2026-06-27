"""
config.py — Shared configuration constants for the Movie Feelings Analysis pipeline.
All algorithm modules import from this file.
"""

import os

# ── File Paths ─────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

RAW_DATA_PATH    = os.path.join(PROJECT_DIR, "data", "raw",     "movie_feelings_dataset.csv")
CLEAN_DATA_PATH  = os.path.join(PROJECT_DIR, "data", "clean",   "movies_clean.csv")
FEAT_DATA_PATH   = os.path.join(PROJECT_DIR, "data", "feature", "movies_features.csv")
NORM_DATA_PATH   = os.path.join(PROJECT_DIR, "data", "feature", "movies_normalized.csv")

OUTPUT_DIR       = os.path.join(PROJECT_DIR, "output")
OUTPUT_SQL_DIR   = os.path.join(PROJECT_DIR, "output", "sql")
OUTPUT_CHART_DIR = os.path.join(PROJECT_DIR, "output", "charts")

MANUAL_SCORES_PATH = os.path.join(PROJECT_DIR, "missing_metascores.txt")
SQL_QUERIES_PATH   = os.path.join(BASE_DIR, "sql_queries.sql")

# Create output directories if they don't exist
for _dir in [OUTPUT_DIR, OUTPUT_SQL_DIR, OUTPUT_CHART_DIR,
             os.path.join(PROJECT_DIR, "data", "clean"),
             os.path.join(PROJECT_DIR, "data", "feature")]:
    os.makedirs(_dir, exist_ok=True)

# ── Rating Column Names ────────────────────────────────────────────────────────
AUDIENCE_COL = "imdb_rating"   # Audience score
CRITICS_COL  = "metascore"     # Primary critic score
CRITICS_ALT  = "tomatometer"   # Secondary critic score (used for imputation)

# ── 50 Emotion Feature Columns ─────────────────────────────────────────────────
F1_COLS = [
    "f1_skepticism", "f1_serenity",    "f1_fear",         "f1_disgust",     "f1_solidarity",
    "f1_elation",    "f1_envy",        "f1_puzzlement",   "f1_recklessness","f1_loyalty",
    "f1_trust",      "f1_sadness",     "f1_shame",        "f1_catharsis",   "f1_unease",
    "f1_introspection","f1_excitement","f1_riskiness",    "f1_mischief",    "f1_enlightenment",
    "f1_love",       "f1_tension",     "f1_sarcasm",      "f1_frustration", "f1_longing",
    "f1_awe",        "f1_defiance",    "f1_amusement",    "f1_vulnerability","f1_surprise",
    "f1_compassion", "f1_resentment",  "f1_triumph",      "f1_happiness",   "f1_acceptance",
    "f1_bravery",    "f1_hope",        "f1_conflict",     "f1_exhilaration","f1_inspiration",
    "f1_curiosity",  "f1_regret",      "f1_nostalgia",    "f1_irony",       "f1_despair",
    "f1_resignation","f1_closeness",   "f1_adrenaline",   "f1_belonging",   "f1_anger",
]

EMOTION_NAMES = [c.replace("f1_", "") for c in F1_COLS]

# ── Cinema Eras ────────────────────────────────────────────────────────────────
ERAS = {
    "Era 1 (1920-1950) Classic":      (1920, 1950),
    "Era 2 (1951-1975) Transition":   (1951, 1975),
    "Era 3 (1976-2000) Blockbuster":  (1976, 2000),
    "Era 4 (2001-2024) Modern":       (2001, 2024),
}
