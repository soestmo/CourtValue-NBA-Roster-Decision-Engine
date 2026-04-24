# CourtValue: NBA Roster Decision Engine

## Project Description
CourtValue is a local, reproducible roster decision-support application for evaluating NBA players using statistical performance, contract context, projected contribution modeling, deterministic value scoring, and deterministic roster fit scoring.

## V2 Real Data Integration
V2 adds deterministic, local integration of free/public data sources with a strict fallback model:

1. `nba_api` (primary stats)
2. `BALLDONTLIE` (optional salary/contracts, requires key)
3. Kaggle SQLite NBA DB (optional backfill, requires local file)
4. Sample CSVs (always available fallback)

### Environment Variables
- `COURTVALUE_DATA_MODE` = `auto` (default), `real`, or `sample`
- `BALLDONTLIE_API_KEY` (optional)
- `KAGGLE_NBA_SQLITE_PATH` (optional local SQLite path)

Behavior:
- `sample`: only sample CSVs
- `real`: requires real canonical data, fails clearly if unavailable
- `auto`: tries real canonical data first, falls back to sample

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run real ingestion
```bash
cd backend
python scripts/ingest_real_data.py --mode auto --seasons 2021-22 2022-23 2023-24 2024-25
python scripts/build_canonical_tables.py --seasons 2021-22 2022-23 2023-24 2024-25
```

## Run backend
```bash
cd backend
uvicorn main:app --reload

cd backend
python -m uvicorn main:app --reload
```

## API Endpoints
- `GET /health`
- `GET /data/status`
- `GET /data/quality`
- `GET /players`
- `GET /players/{player_id}`
- `GET /evaluate/{player_id}?team_context=SAC`
- `GET /compare?player_ids=1,2,3&team_context=SAC`
- `GET /model/feature-importance`
- `GET /explain/{player_id}`

## Limitations
- Free/public sources can have missing fields and occasional endpoint instability.
- BALLDONTLIE salary/contract access may vary by account tier.
- Vendor-grade optical tracking is not included.
- Missing contract/on-off fields are preserved as null/default-safe values (not fabricated).
