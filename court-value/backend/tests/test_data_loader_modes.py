from pathlib import Path

import pandas as pd

import services.data_loader as data_loader


def test_sample_mode_loads_sample(monkeypatch) -> None:
    monkeypatch.setenv("COURTVALUE_DATA_MODE", "sample")
    players = data_loader.load_players()
    assert not players.empty
    assert "player_id" in players.columns


def test_auto_mode_falls_back_without_processed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("COURTVALUE_DATA_MODE", "auto")
    monkeypatch.setattr(data_loader, "PROCESSED_DATA_DIR", tmp_path)
    players = data_loader.load_players()
    assert not players.empty


def test_real_mode_raises_without_processed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("COURTVALUE_DATA_MODE", "real")
    monkeypatch.setattr(data_loader, "PROCESSED_DATA_DIR", tmp_path)
    try:
        data_loader.load_players()
        assert False, "Expected DataLoadError"
    except data_loader.DataLoadError:
        assert True


def test_real_mode_reads_processed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("COURTVALUE_DATA_MODE", "real")
    monkeypatch.setattr(data_loader, "PROCESSED_DATA_DIR", tmp_path)
    canonical_path = tmp_path / "player_season_canonical.parquet"
    pd.DataFrame([{"player_id": 1, "player_name": "A", "age": 25, "minutes_per_game": 30, "games_played": 70, "usage_rate": 20, "true_shooting_pct": 0.6, "effective_fg_pct": 0.55, "assist_pct": 10, "rebound_pct": 10, "steal_pct": 1, "block_pct": 1, "turnover_pct": 10, "three_point_attempt_rate": 0.4, "free_throw_rate": 0.2, "bpm_proxy": 1, "on_off_net_proxy": None, "salary": None, "years_remaining": None}]).to_parquet(canonical_path, index=False)
    players = data_loader.load_players()
    assert len(players) == 1
    assert float(players.iloc[0]["salary"]) == 0.0
