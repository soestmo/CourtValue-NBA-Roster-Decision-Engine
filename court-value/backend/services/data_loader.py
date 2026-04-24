from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd

from config import DATA_DIR, PROCESSED_DATA_DIR, get_settings
from data_sources.source_registry import build_source_registry
from services.data_quality import flag_suspicious_values, summarize_missingness

SAMPLE_DATA_DIR = DATA_DIR


class DataLoadError(RuntimeError):
    pass


def _processed_players_path() -> Path:
    return PROCESSED_DATA_DIR / "player_season_canonical.parquet"


def _processed_teams_path() -> Path:
    return PROCESSED_DATA_DIR / "team_season_canonical.parquet"


def _real_available() -> bool:
    return _processed_players_path().exists()


def _load_sample_players() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_DIR / "sample_players.csv")


def _load_sample_contracts() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_DIR / "sample_contracts.csv")


def _load_sample_team_contexts() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_DIR / "sample_team_context.csv")


def _load_real_players() -> pd.DataFrame:
    df = pd.read_parquet(_processed_players_path())
    for col in ["salary", "years_remaining", "on_off_net_proxy"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    df["contract_type"] = df.get("contract_type", pd.Series(["unknown"] * len(df))).fillna("unknown")
    df["primary_role"] = df.get("primary_role", pd.Series(["balanced"] * len(df))).fillna("balanced")
    return df


def load_players() -> pd.DataFrame:
    settings = get_settings()
    mode = settings.data_mode
    if mode == "sample":
        return _load_sample_players()

    if _real_available():
        return _load_real_players()

    if mode == "real":
        raise DataLoadError("COURTVALUE_DATA_MODE=real but processed canonical parquet was not found.")
    return _load_sample_players()


def load_contracts() -> pd.DataFrame:
    settings = get_settings()
    mode = settings.data_mode
    contracts_path = PROCESSED_DATA_DIR / "contracts_canonical.parquet"
    if mode != "sample" and contracts_path.exists():
        return pd.read_parquet(contracts_path)
    return _load_sample_contracts()


def load_team_contexts() -> pd.DataFrame:
    return _load_sample_team_contexts()


def get_player_row(players_df: pd.DataFrame, player_id: int) -> pd.Series | None:
    filtered = players_df[players_df["player_id"] == player_id]
    if filtered.empty:
        return None
    return filtered.iloc[0]


def get_team_context(team_context_df: pd.DataFrame, team_code: str) -> pd.Series | None:
    filtered = team_context_df[team_context_df["team_code"] == team_code]
    if filtered.empty:
        return None
    return filtered.iloc[0]


def get_data_status(players_df: pd.DataFrame | None = None) -> dict[str, Any]:
    settings = get_settings()
    players = players_df if players_df is not None else load_players()
    using_real_data = bool(settings.data_mode != "sample" and _real_available())
    seasons = sorted({str(value) for value in players.get("season", pd.Series([], dtype=str)).dropna().unique().tolist()})
    return {
        "data_mode": settings.data_mode,
        "using_real_data": using_real_data,
        "available_sources": build_source_registry(bool(os.getenv("BALLDONTLIE_API_KEY")), settings.kaggle_nba_sqlite_path),
        "canonical_row_counts": {
            "player_season_canonical": int(len(players)) if using_real_data else 0,
            "team_season_canonical": int(len(pd.read_parquet(_processed_teams_path()))) if using_real_data and _processed_teams_path().exists() else 0,
            "contracts_canonical": int(len(load_contracts())) if using_real_data else 0,
        },
        "latest_seasons_available": seasons[-4:] if seasons else [],
    }


def get_data_quality_snapshot(players_df: pd.DataFrame | None = None) -> dict[str, Any]:
    players = players_df if players_df is not None else load_players()
    missingness = summarize_missingness(players)
    suspicious = flag_suspicious_values(players)
    report_path = PROCESSED_DATA_DIR / "data_quality_report.md"
    source_report_path = DATA_DIR / "raw" / "source_availability_report.json"
    source_coverage: dict[str, Any] = {}
    if source_report_path.exists():
        source_coverage = json.loads(source_report_path.read_text(encoding="utf-8"))
    return {
        "missingness_summary": missingness.to_dict(orient="records"),
        "suspicious_value_flags": suspicious.to_dict(orient="records"),
        "source_coverage": source_coverage,
        "quality_report_exists": report_path.exists(),
    }
