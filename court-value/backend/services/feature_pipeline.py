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


def build_feature_frame(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df["age_squared"] = df["age"] ** 2
    return df[FEATURE_COLUMNS]


def build_future_impact_proxy(raw_df: pd.DataFrame) -> pd.Series:
    age_term = -0.12 * (raw_df["age"] - 27).pow(2) + 10
    target = (
        3.2 * raw_df["bpm_proxy"]
        + 1.5 * raw_df["on_off_net_proxy"]
        + 0.45 * raw_df["minutes_per_game"]
        + 70.0 * (raw_df["true_shooting_pct"] - 0.5)
        + 0.08 * raw_df["games_played"]
        + age_term
    )
    return target
