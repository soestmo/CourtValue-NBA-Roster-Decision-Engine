import pandas as pd

from services.feature_pipeline import FEATURE_COLUMNS, build_feature_frame, build_future_impact_proxy


def test_feature_frame_contains_expected_columns() -> None:
    raw = pd.DataFrame(
        [
            {
                "age": 26,
                "minutes_per_game": 30,
                "games_played": 75,
                "usage_rate": 24,
                "true_shooting_pct": 0.59,
                "effective_fg_pct": 0.55,
                "assist_pct": 21,
                "rebound_pct": 12,
                "steal_pct": 1.8,
                "block_pct": 1.2,
                "turnover_pct": 12,
                "three_point_attempt_rate": 0.42,
                "free_throw_rate": 0.24,
                "bpm_proxy": 2.1,
                "on_off_net_proxy": 3.0,
                "salary": 18,
                "years_remaining": 3,
            }
        ]
    )
    features = build_feature_frame(raw)
    assert list(features.columns) == FEATURE_COLUMNS
    assert features.iloc[0]["age_squared"] == 676


def test_future_impact_proxy_returns_series() -> None:
    raw = pd.DataFrame(
        [
            {
                "age": 27,
                "minutes_per_game": 30,
                "games_played": 70,
                "true_shooting_pct": 0.6,
                "bpm_proxy": 2.0,
                "on_off_net_proxy": 1.0,
            }
        ]
    )
    proxy = build_future_impact_proxy(raw)
    assert proxy.shape[0] == 1
    assert proxy.iloc[0] > 0
