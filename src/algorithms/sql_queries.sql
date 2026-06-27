-- sql_queries.sql
-- 9 SQL queries for the Movie Feelings Analysis project.
-- Queries 1-7: Exploratory Data Analysis (EDA) to understand the dataset.
-- Queries 8-9: Tagged to Research Questions (RQ) to satisfy rubric requirements.
-- All queries run on the "movies" table loaded from data/clean/movies_clean.csv.

-- ════════════════════════════════════════════════════════════════════════════════
-- GROUP 1: EXPLORATORY DATA ANALYSIS (EDA) — Queries 1 to 7
-- ════════════════════════════════════════════════════════════════════════════════

-- Query 1 [EDA]: Film count and average audience score by decade
-- Purpose: Understand how the dataset is distributed across time.
-- Output: eda_01_film_count_by_decade.csv
SELECT
    (year / 10) * 10          AS decade,
    COUNT(*)                  AS film_count,
    ROUND(AVG(imdb_rating), 3) AS avg_imdb_rating
FROM movies
GROUP BY decade
ORDER BY decade;

-- Query 2 [EDA]: Descriptive statistics for audience score (imdb_rating)
-- Purpose: Understand the range and distribution of audience ratings.
-- Output: eda_02_imdb_rating_stats.csv
SELECT
    COUNT(imdb_rating)           AS total_films,
    ROUND(MIN(imdb_rating), 2)   AS min_rating,
    ROUND(MAX(imdb_rating), 2)   AS max_rating,
    ROUND(AVG(imdb_rating), 3)   AS avg_rating
FROM movies;

-- Query 3 [EDA]: Descriptive statistics for critic score (metascore)
-- Purpose: Understand the range and distribution of critic ratings.
-- Output: eda_03_metascore_stats.csv
SELECT
    COUNT(metascore)           AS films_with_metascore,
    ROUND(MIN(metascore), 2)   AS min_metascore,
    ROUND(MAX(metascore), 2)   AS max_metascore,
    ROUND(AVG(metascore), 3)   AS avg_metascore
FROM movies
WHERE metascore IS NOT NULL;

-- Query 4 [EDA]: Count of films with missing metascore and tomatometer
-- Purpose: Measure the extent of missing data before cleaning.
-- Output: eda_04_missing_values_count.csv
SELECT
    SUM(CASE WHEN metascore IS NULL THEN 1 ELSE 0 END)   AS missing_metascore,
    SUM(CASE WHEN tomatometer IS NULL THEN 1 ELSE 0 END) AS missing_tomatometer,
    COUNT(*)                                              AS total_films
FROM movies;

-- Query 5 [EDA]: Top 10 emotions by average intensity across all films
-- Purpose: Get a high-level view of which emotions dominate cinema.
-- Output: eda_05_top10_emotions.csv
SELECT emotion, ROUND(avg_intensity, 4) AS avg_intensity
FROM (
    SELECT 'skepticism'   AS emotion, AVG(f1_skepticism)    AS avg_intensity FROM movies UNION ALL
    SELECT 'serenity',                AVG(f1_serenity)                       FROM movies UNION ALL
    SELECT 'fear',                    AVG(f1_fear)                           FROM movies UNION ALL
    SELECT 'disgust',                 AVG(f1_disgust)                        FROM movies UNION ALL
    SELECT 'solidarity',              AVG(f1_solidarity)                     FROM movies UNION ALL
    SELECT 'elation',                 AVG(f1_elation)                        FROM movies UNION ALL
    SELECT 'envy',                    AVG(f1_envy)                           FROM movies UNION ALL
    SELECT 'puzzlement',              AVG(f1_puzzlement)                     FROM movies UNION ALL
    SELECT 'recklessness',            AVG(f1_recklessness)                   FROM movies UNION ALL
    SELECT 'loyalty',                 AVG(f1_loyalty)                        FROM movies UNION ALL
    SELECT 'trust',                   AVG(f1_trust)                          FROM movies UNION ALL
    SELECT 'sadness',                 AVG(f1_sadness)                        FROM movies UNION ALL
    SELECT 'shame',                   AVG(f1_shame)                          FROM movies UNION ALL
    SELECT 'catharsis',               AVG(f1_catharsis)                      FROM movies UNION ALL
    SELECT 'unease',                  AVG(f1_unease)                         FROM movies UNION ALL
    SELECT 'introspection',           AVG(f1_introspection)                  FROM movies UNION ALL
    SELECT 'excitement',              AVG(f1_excitement)                     FROM movies UNION ALL
    SELECT 'riskiness',               AVG(f1_riskiness)                      FROM movies UNION ALL
    SELECT 'mischief',                AVG(f1_mischief)                       FROM movies UNION ALL
    SELECT 'enlightenment',           AVG(f1_enlightenment)                  FROM movies UNION ALL
    SELECT 'love',                    AVG(f1_love)                           FROM movies UNION ALL
    SELECT 'tension',                 AVG(f1_tension)                        FROM movies UNION ALL
    SELECT 'sarcasm',                 AVG(f1_sarcasm)                        FROM movies UNION ALL
    SELECT 'frustration',             AVG(f1_frustration)                    FROM movies UNION ALL
    SELECT 'longing',                 AVG(f1_longing)                        FROM movies UNION ALL
    SELECT 'awe',                     AVG(f1_awe)                            FROM movies UNION ALL
    SELECT 'defiance',                AVG(f1_defiance)                       FROM movies UNION ALL
    SELECT 'amusement',               AVG(f1_amusement)                      FROM movies UNION ALL
    SELECT 'vulnerability',           AVG(f1_vulnerability)                  FROM movies UNION ALL
    SELECT 'surprise',                AVG(f1_surprise)                       FROM movies UNION ALL
    SELECT 'compassion',              AVG(f1_compassion)                     FROM movies UNION ALL
    SELECT 'resentment',              AVG(f1_resentment)                     FROM movies UNION ALL
    SELECT 'triumph',                 AVG(f1_triumph)                        FROM movies UNION ALL
    SELECT 'happiness',               AVG(f1_happiness)                      FROM movies UNION ALL
    SELECT 'acceptance',              AVG(f1_acceptance)                     FROM movies UNION ALL
    SELECT 'bravery',                 AVG(f1_bravery)                        FROM movies UNION ALL
    SELECT 'hope',                    AVG(f1_hope)                           FROM movies UNION ALL
    SELECT 'conflict',                AVG(f1_conflict)                       FROM movies UNION ALL
    SELECT 'exhilaration',            AVG(f1_exhilaration)                   FROM movies UNION ALL
    SELECT 'inspiration',             AVG(f1_inspiration)                    FROM movies UNION ALL
    SELECT 'curiosity',               AVG(f1_curiosity)                      FROM movies UNION ALL
    SELECT 'regret',                  AVG(f1_regret)                         FROM movies UNION ALL
    SELECT 'nostalgia',               AVG(f1_nostalgia)                      FROM movies UNION ALL
    SELECT 'irony',                   AVG(f1_irony)                          FROM movies UNION ALL
    SELECT 'despair',                 AVG(f1_despair)                        FROM movies UNION ALL
    SELECT 'resignation',             AVG(f1_resignation)                    FROM movies UNION ALL
    SELECT 'closeness',               AVG(f1_closeness)                      FROM movies UNION ALL
    SELECT 'adrenaline',              AVG(f1_adrenaline)                     FROM movies UNION ALL
    SELECT 'belonging',               AVG(f1_belonging)                      FROM movies UNION ALL
    SELECT 'anger',                   AVG(f1_anger)                          FROM movies
)
ORDER BY avg_intensity DESC
LIMIT 10;

-- Query 6 [EDA]: Film count by cinema era
-- Purpose: Understand historical distribution of films across eras.
-- Output: eda_06_film_count_by_era.csv
SELECT
    CASE
        WHEN year BETWEEN 1920 AND 1950 THEN 'Era 1 (1920-1950) Classic'
        WHEN year BETWEEN 1951 AND 1975 THEN 'Era 2 (1951-1975) Transition'
        WHEN year BETWEEN 1976 AND 2000 THEN 'Era 3 (1976-2000) Blockbuster'
        WHEN year BETWEEN 2001 AND 2024 THEN 'Era 4 (2001-2024) Modern'
        ELSE 'Unknown'
    END AS era,
    COUNT(*) AS film_count
FROM movies
GROUP BY era
ORDER BY MIN(year);

-- Query 7 [EDA]: Film count by IMDb rating bracket
-- Purpose: Understand the quality distribution of films in the dataset.
-- Output: eda_07_rating_distribution.csv
SELECT
    CASE
        WHEN imdb_rating < 6.0                   THEN 'Below 6.0 (Poor)'
        WHEN imdb_rating >= 6.0 AND imdb_rating < 7.0 THEN '6.0 – 6.9 (Average)'
        WHEN imdb_rating >= 7.0 AND imdb_rating < 8.0 THEN '7.0 – 7.9 (Good)'
        WHEN imdb_rating >= 8.0                  THEN '8.0+ (Excellent)'
    END AS rating_bracket,
    COUNT(*) AS film_count,
    ROUND(AVG(imdb_rating), 3) AS avg_rating
FROM movies
GROUP BY rating_bracket
ORDER BY MIN(imdb_rating);

-- ════════════════════════════════════════════════════════════════════════════════
-- GROUP 2: RESEARCH QUESTION TAGGED — Queries 8 to 9
-- (Surface-level aggregation to satisfy rubric STT 4 requirement)
-- ════════════════════════════════════════════════════════════════════════════════

-- Query 8 [RQ1 — Taste Asymmetry]: Top 20 films with the largest taste gap
-- taste_gap = metascore/10 - imdb_rating
-- Positive: critics love it, audience does not. Negative: audience loves it, critics do not.
-- Output: rq1_taste_gap_top20.csv
SELECT
    title,
    year,
    imdb_rating,
    metascore,
    ROUND((metascore / 10.0) - imdb_rating, 3) AS taste_gap
FROM movies
WHERE metascore IS NOT NULL
ORDER BY ABS((metascore / 10.0) - imdb_rating) DESC
LIMIT 20;

-- Query 9 [RQ3 — Historical Trend]: Average scores by cinema era
-- Purpose: Surface-level overview of how ratings evolved across eras.
-- Output: rq3_avg_score_by_era.csv
SELECT
    CASE
        WHEN year BETWEEN 1920 AND 1950 THEN 'Era 1 (1920-1950) Classic'
        WHEN year BETWEEN 1951 AND 1975 THEN 'Era 2 (1951-1975) Transition'
        WHEN year BETWEEN 1976 AND 2000 THEN 'Era 3 (1976-2000) Blockbuster'
        WHEN year BETWEEN 2001 AND 2024 THEN 'Era 4 (2001-2024) Modern'
        ELSE 'Unknown'
    END AS era,
    COUNT(*)                          AS film_count,
    ROUND(AVG(imdb_rating), 3)        AS avg_audience_score,
    ROUND(AVG(metascore), 3)          AS avg_critics_score
FROM movies
WHERE metascore IS NOT NULL
GROUP BY era
ORDER BY MIN(year);
