import pandas as pd

from services.canonicalize import canonicalize_contracts, canonicalize_player_stats, merge_canonical_tables


def test_canonicalize_player_stats_minimal_frame() -> None:
    raw = pd.DataFrame(
        [{"PLAYER_ID": 1, "PLAYER_NAME": "Test One", "TEAM_ABBREVIATION": "SAC", "AGE": 25, "GP": 70, "MIN": 30, "USG_PCT": 24.0, "TS_PCT": 0.6, "EFG_PCT": 0.55}]
    )
    out = canonicalize_player_stats(raw, season="2024-25", source="nba_api")
    assert out.iloc[0]["player_id"] == 1
    assert out.iloc[0]["season"] == "2024-25"
    assert out.iloc[0]["source_stats"] == "nba_api"


def test_merge_canonical_tables_with_contracts() -> None:
    players = canonicalize_player_stats(
        pd.DataFrame([{"PLAYER_ID": 2, "PLAYER_NAME": "Test Two", "TEAM_ABBREVIATION": "LAL", "AGE": 28, "GP": 75, "MIN": 33}]),
        season="2024-25",
        source="nba_api",
    )
    contracts = canonicalize_contracts(
        pd.DataFrame([{"player_id": 2, "first_name": "Test", "last_name": "Two", "salary": 32.0}]),
        season="2024-25",
        source="balldontlie",
    )
    merged = merge_canonical_tables(players, contracts, pd.DataFrame())
    assert float(merged.iloc[0]["salary"]) == 32.0
    assert merged.iloc[0]["contract_type"] == "max_tier"
