# Intelligence Layer Progress

## Completed
- Defined canonical evaluation schema.
- Implemented XGBoost contribution projection.
- Implemented deterministic value + fit scoring.
- Implemented recommendation labels and risk flags.
- Implemented SHAP local explanation and global feature importance.
- Implemented V2 real-data source clients (`nba_api`, optional `BALLDONTLIE`, optional Kaggle SQLite).
- Implemented raw ingestion and canonical build scripts with parquet caching.
- Added canonicalization + data quality utilities.
- Added runtime data-mode switching (`sample` / `real` / `auto`) with fallback behavior.
- Added API endpoints `/data/status` and `/data/quality`.

## In Scope for Ongoing Iteration
- Expand contextual team templates.
- Add more rigorous target calibration once historical labels are available.
- Improve uncertainty handling with empirical residual analysis.
- Improve contract backfill coverage for seasons with sparse public salary data.
