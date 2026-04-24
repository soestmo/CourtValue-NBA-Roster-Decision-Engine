from __future__ import annotations

import pandas as pd


FEATURE_COLUMNS = [
    "age",
    "age_squared",
    "minutes_per_game",
    "games_played",
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
]

BASE_DEFAULTS = {
    "age": 27.0,
    "minutes_per_game": 0.0,
    "games_played": 0.0,
    "usage_rate": 0.0,
    "true_shooting_pct": 0.5,
    "effective_fg_pct": 0.5,
    "assist_pct": 0.0,
    "rebound_pct": 0.0,
    "steal_pct": 0.0,
    "block_pct": 0.0,
    "turnover_pct": 0.0,
    "three_point_attempt_rate": 0.0,
    "free_throw_rate": 0.0,
    "bpm_proxy": 0.0,
    "on_off_net_proxy": 0.0,
    "salary": 0.0,
    "years_remaining": 0.0,
}


def _with_required_columns(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    for column, default in BASE_DEFAULTS.items():
        if column not in df.columns:
            df[column] = default
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(default)
    return df


def build_feature_frame(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = _with_required_columns(raw_df)
    df["age_squared"] = df["age"] ** 2
    return df[FEATURE_COLUMNS]


def build_future_impact_proxy(raw_df: pd.DataFrame) -> pd.Series:
    df = _with_required_columns(raw_df)
    age_term = -0.12 * (df["age"] - 27).pow(2) + 10
    target = (
        3.2 * df["bpm_proxy"]
        + 1.5 * df["on_off_net_proxy"]
        + 0.45 * df["minutes_per_game"]
        + 70.0 * (df["true_shooting_pct"] - 0.5)
        + 0.08 * df["games_played"]
        + age_term
    )
    return target
