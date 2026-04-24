from __future__ import annotations

import numpy as np
import pandas as pd

CANONICAL_PLAYER_COLUMNS = [
    "player_id",
    "player_name",
    "season",
    "team",
    "age",
    "games_played",
    "minutes_per_game",
    "usage_rate",
    "true_shooting_pct",
    "effective_fg_pct",
    "assist_pct",
    "rebound_pct",
    "steal_pct",
    "block_pct",
    "turnover_pct",
    "three_point_attempt_rate",
    "free_throw_rate",
    "bpm_proxy",
    "on_off_net_proxy",
    "salary",
    "years_remaining",
    "contract_type",
    "primary_role",
    "source_stats",
    "source_contracts",
]


def _pick(df: pd.DataFrame, names: list[str], default: float | str | int | None = np.nan) -> pd.Series:
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series([default] * len(df), index=df.index)


def _infer_primary_role(row: pd.Series) -> str:
    usage = float(row.get("usage_rate") or 0)
    ast = float(row.get("assist_pct") or 0)
    reb = float(row.get("rebound_pct") or 0)
    blk = float(row.get("block_pct") or 0)
    tpar = float(row.get("three_point_attempt_rate") or 0)
    if blk >= 2.0 and reb >= 14:
        return "rim_big"
    if ast >= 24 and usage >= 22:
        return "primary_creator"
    if tpar >= 0.45 and usage < 24:
        return "spacing_wing"
    return "balanced"


def _infer_contract_type(salary: float | None) -> str | None:
    if salary is None or pd.isna(salary):
        return None
    if salary < 5:
        return "minimum_or_two_way"
    if salary < 15:
        return "rotation_value"
    if salary < 30:
        return "starter_tier"
    return "max_tier"


def canonicalize_player_stats(raw_df: pd.DataFrame, season: str, source: str) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=CANONICAL_PLAYER_COLUMNS)

    out = pd.DataFrame()
    out["player_id"] = _pick(raw_df, ["PLAYER_ID", "player_id", "id"])
    out["player_name"] = _pick(raw_df, ["PLAYER_NAME", "player_name", "player"])
    out["season"] = season
    out["team"] = _pick(raw_df, ["TEAM_ABBREVIATION", "team", "team_code"])
    out["age"] = _pick(raw_df, ["AGE", "age"])
    out["games_played"] = _pick(raw_df, ["GP", "games_played", "games"])
    out["minutes_per_game"] = _pick(raw_df, ["MIN", "minutes_per_game", "min"])
    out["usage_rate"] = _pick(raw_df, ["USG_PCT", "usage_rate"])
    out["true_shooting_pct"] = _pick(raw_df, ["TS_PCT", "true_shooting_pct"])
    out["effective_fg_pct"] = _pick(raw_df, ["EFG_PCT", "effective_fg_pct"])
    out["assist_pct"] = _pick(raw_df, ["AST_PCT", "assist_pct"])
    out["rebound_pct"] = _pick(raw_df, ["REB_PCT", "rebound_pct"])
    out["steal_pct"] = _pick(raw_df, ["STL_PCT", "steal_pct"])
    out["block_pct"] = _pick(raw_df, ["BLK_PCT", "block_pct"])
    out["turnover_pct"] = _pick(raw_df, ["TM_TOV_PCT", "TOV_PCT", "turnover_pct"])
    out["three_point_attempt_rate"] = _pick(raw_df, ["FG3A_RATE", "three_point_attempt_rate"])
    out["free_throw_rate"] = _pick(raw_df, ["FTA_RATE", "free_throw_rate"])
    out["bpm_proxy"] = _pick(raw_df, ["PIE", "bpm_proxy"])
    out["on_off_net_proxy"] = _pick(raw_df, ["PLUS_MINUS", "on_off_net_proxy"])
    out["salary"] = np.nan
    out["years_remaining"] = np.nan
    out["contract_type"] = None
    out["primary_role"] = out.apply(_infer_primary_role, axis=1)
    out["source_stats"] = source
    out["source_contracts"] = None
    return out[CANONICAL_PLAYER_COLUMNS]


def canonicalize_team_stats(raw_df: pd.DataFrame, season: str, source: str) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=["team", "season", "off_rating", "def_rating", "net_rating", "pace", "source_stats"])
    out = pd.DataFrame()
    out["team"] = _pick(raw_df, ["TEAM_ABBREVIATION", "team", "abbreviation"])
    out["season"] = season
    out["off_rating"] = _pick(raw_df, ["OFF_RATING", "off_rating"])
    out["def_rating"] = _pick(raw_df, ["DEF_RATING", "def_rating"])
    out["net_rating"] = _pick(raw_df, ["NET_RATING", "net_rating"])
    out["pace"] = _pick(raw_df, ["PACE", "pace"])
    out["source_stats"] = source
    return out


def canonicalize_contracts(raw_df: pd.DataFrame, season: str, source: str) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame(columns=["player_id", "player_name", "season", "team", "salary", "years_remaining", "contract_type", "source_contracts"])
    out = pd.DataFrame()
    out["player_id"] = _pick(raw_df, ["player_id", "PLAYER_ID", "id"])
    first = _pick(raw_df, ["first_name"], "")
    last = _pick(raw_df, ["last_name"], "")
    fallback_name = _pick(raw_df, ["player_name", "PLAYER_NAME", "player"])
    built_name = (first.fillna("") + " " + last.fillna("")).str.strip()
    out["player_name"] = built_name.where(built_name != "", fallback_name)
    out["season"] = season
    out["team"] = _pick(raw_df, ["team", "TEAM_ABBREVIATION"])
    out["salary"] = _pick(raw_df, ["salary", "amount"])
    out["years_remaining"] = _pick(raw_df, ["years_remaining", "years_left"], np.nan)
    out["contract_type"] = out["salary"].apply(_infer_contract_type)
    out["source_contracts"] = source
    return out


def merge_canonical_tables(player_stats: pd.DataFrame, contracts: pd.DataFrame, team_stats: pd.DataFrame) -> pd.DataFrame:
    merged = player_stats.copy()
    if not contracts.empty:
        merged = merged.drop(columns=["salary", "years_remaining", "contract_type", "source_contracts"], errors="ignore")
        merged = merged.merge(
            contracts[["player_id", "season", "salary", "years_remaining", "contract_type", "source_contracts"]],
            on=["player_id", "season"],
            how="left",
        )
    else:
        merged["salary"] = np.nan
        merged["years_remaining"] = np.nan
        merged["contract_type"] = None
        merged["source_contracts"] = None

    if not team_stats.empty:
        merged = merged.merge(team_stats[["team", "season", "net_rating"]], on=["team", "season"], how="left")
        merged["on_off_net_proxy"] = merged["on_off_net_proxy"].fillna(merged["net_rating"])
        merged = merged.drop(columns=["net_rating"])

    for col in CANONICAL_PLAYER_COLUMNS:
        if col not in merged.columns:
            merged[col] = np.nan
    return merged[CANONICAL_PLAYER_COLUMNS]
