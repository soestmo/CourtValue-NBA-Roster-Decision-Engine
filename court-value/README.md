# CourtValue: NBA Roster Decision Engine

## Project Description
CourtValue is a local, reproducible roster decision-support application for evaluating NBA-style players using statistical performance, contract context, projected contribution modeling, deterministic value scoring, and deterministic roster fit scoring.

> Note: all player/team records in V1 are illustrative fictional data for portfolio demonstration.

## Why This Exists
Basketball operations decisions require balancing expected impact, financial flexibility, and contextual roster fit. This project demonstrates how to structure a practical decision engine that combines:
- machine learning for projected contribution (XGBoost),
- deterministic business logic for cap/value trade-offs,
- deterministic basketball fit heuristics,
- transparent explainability (global feature importance + local SHAP drivers).

## Architecture
- **Backend**: FastAPI + pandas/numpy + xgboost + shap.
- **Data**: local CSV files in `backend/data`.
- **Modeling**: XGBoost regressor trained on a synthetic `future_impact_proxy` target.
- **Frontend**: Vite + React + TypeScript + Recharts.
- **No agents in V1**.

## Install Instructions
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
- `GET /health`
- `GET /players`
- `GET /players/{player_id}`
- `GET /evaluate/{player_id}?team_context=SAC`
- `GET /compare?player_ids=1,2,3&team_context=SAC`
- `GET /model/feature-importance`
- `GET /explain/{player_id}`

## Modeling Approach
- Feature pipeline includes age, workload, efficiency, playmaking/defense, and contract variables.
- Synthetic `future_impact_proxy` target blends BPM proxy, on/off net proxy, minutes, shooting, age curve, and games played.
- XGBoost predicts contribution signal and derives:
  - projected years 1-3,
  - uncertainty band,
  - 0-100 projected contribution score.

## Explainability Approach
- **Global**: XGBoost gain feature importance.
- **Local**: SHAP TreeExplainer top positive/negative drivers with deterministic natural-language interpretations.

## Limitations
- V1 uses synthetic illustrative data.
- No injury history feed or play-by-play granularity.
- Team context is intentionally simplified for reproducibility.
- Scores are decision support signals, not final decision makers.

## Next Steps
- Add scenario simulations for trade packages.
- Add role/lineup interaction modeling.
- Add richer context packs for multiple teams.
- Calibrate with historical outcome labels when real data is integrated.
