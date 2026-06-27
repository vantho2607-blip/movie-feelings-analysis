# 🎬 Movie Feelings Analysis

> **Phân tích Cảm xúc Kịch bản Điện ảnh (1920–2024)**
> Đồ án môn ADY201m — FPT University

## Tổng quan

Dự án phân tích **50 loại cảm xúc** trong kịch bản điện ảnh qua hơn 100 năm lịch sử, trả lời 3 câu hỏi nghiên cứu:

| RQ | Câu hỏi | Phương pháp |
|----|---------|-------------|
| **RQ1** | Cấu trúc cảm xúc & Bất đối xứng khẩu vị (Khán giả vs Nhà phê bình) | Pearson Correlation |
| **RQ2** | Đa dạng cảm xúc & Điểm bão hòa | Shannon Entropy + ANOVA |
| **RQ3** | Xu hướng lịch sử & Dự báo quỹ đạo tương lai | 5 mô hình ML so sánh |

## Cấu trúc dự án

```
├── main.py                          # Pipeline runner (chạy 5 stage tuần tự)
├── requirements.txt                 # Dependencies
│
├── src/
│   ├── algorithms/
│   │   ├── config.py                # Cấu hình chung (paths, columns, eras)
│   │   ├── data_cleaning.py         # Stage 1: Làm sạch dữ liệu
│   │   ├── feature_engineering.py   # Stage 2: Tạo features (entropy, era, taste_gap)
│   │   ├── sql_analysis.py          # Stage 3: 9 SQL queries (EDA)
│   │   ├── sql_queries.sql          # File SQL queries
│   │   ├── statistical_tests.py     # Stage 4: Pearson + ANOVA
│   │   └── ml_models.py            # Stage 5: 5 mô hình ML + PCA/KMeans
│   └── charts/
│       ├── chart_rq1.ipynb          # Biểu đồ RQ1
│       ├── chart_rq2.ipynb          # Biểu đồ RQ2
│       ├── chart_rq3.ipynb          # Biểu đồ RQ3
│       └── chart_advanced.ipynb     # Biểu đồ nâng cao (Heatmap, Radar, PCA)
│
├── data/
│   ├── raw/                         # Dataset gốc (movie_feelings_dataset.csv)
│   ├── clean/                       # Dữ liệu đã làm sạch
│   └── feature/                     # Dữ liệu đã feature engineering
│
├── output/
│   ├── sql/                         # Kết quả 9 SQL queries (CSV)
│   ├── charts/                      # Biểu đồ xuất ra (PNG)
│   ├── anova_results.csv            # Kết quả ANOVA
│   └── model_metrics.csv            # So sánh 5 mô hình ML
│
├── paper/                           # Papers tham khảo (PDF/TXT)
├── references.json                  # Danh sách paper đã xác minh
├── literature_review.md             # Tổng quan tài liệu
├── human_misconceptions.md          # Nhật ký phản biện giả thuyết
├── missing_metascores.txt           # Điểm Metascore điền thủ công
└── AI_AuditLog_Template_ADY201m.xlsx
```

## Cài đặt & Chạy

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Chạy toàn bộ pipeline (5 stages)
python main.py

# 3. Mở notebooks để xem biểu đồ
jupyter notebook src/charts/
```

## Pipeline

```
Stage 1: Data Cleaning       → data/clean/movies_clean.csv
Stage 2: Feature Engineering  → data/feature/movies_features.csv
Stage 3: SQL Analysis         → output/sql/ (9 CSV files)
Stage 4: Statistical Tests    → output/anova_results.csv
Stage 5: ML Models + PCA      → output/model_metrics.csv
```

## 5 Mô hình Dự báo (RQ3)

| # | Mô hình | Mô tả |
|---|---------|-------|
| 1 | Linear Regression | Baseline tuyến tính |
| 2 | Ridge Regression | Regularized (alpha=1.0) |
| 3 | Polynomial (bậc 2) | Phi tuyến |
| 4 | Random Forest | Ensemble 100 cây |
| 5 | SVR (RBF) | Support Vector Regression |

## Tech Stack

- **Python 3.10+** — pandas, numpy, scipy, scikit-learn
- **Visualization** — matplotlib, seaborn, Jupyter Notebooks
- **Database** — SQLite (in-memory cho SQL analysis)
