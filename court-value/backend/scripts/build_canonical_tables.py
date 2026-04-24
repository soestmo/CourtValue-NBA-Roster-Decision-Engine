from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from services.canonicalize import (
    canonicalize_contracts,
    canonicalize_player_stats,
    canonicalize_team_stats,
    merge_canonical_tables,
)
from services.data_quality import write_data_quality_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build canonical processed tables from raw parquet")
    parser.add_argument("--raw-dir", default="backend/data/raw")
    parser.add_argument("--processed-dir", default="backend/data/processed")
    parser.add_argument("--seasons", nargs="+", required=True)
    return parser.parse_args()


def _read_if_exists(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()




def _normalize_repo_relative(path_value: str) -> Path:
    path = Path(path_value)
    if path.exists():
        return path
    cwd = Path.cwd()
    if cwd.name == "backend" and path.parts and path.parts[0] == "backend":
        return Path(*path.parts[1:])
    return path


def main() -> int:
    args = parse_args()
    raw_dir = _normalize_repo_relative(args.raw_dir)
    processed_dir = _normalize_repo_relative(args.processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    player_frames: list[pd.DataFrame] = []
    team_frames: list[pd.DataFrame] = []
    contract_frames: list[pd.DataFrame] = []

    for season in args.seasons:
        player_raw = _read_if_exists(raw_dir / f"nba_api_player_advanced_{season}.parquet")
        if player_raw.empty:
            player_raw = _read_if_exists(raw_dir / f"nba_api_player_basic_{season}.parquet")
        team_raw = _read_if_exists(raw_dir / f"nba_api_team_advanced_{season}.parquet")
        contracts_raw = _read_if_exists(raw_dir / f"balldontlie_contracts_{season}.parquet")

        player_frames.append(canonicalize_player_stats(player_raw, season, "nba_api"))
        team_frames.append(canonicalize_team_stats(team_raw, season, "nba_api"))
        contract_frames.append(canonicalize_contracts(contracts_raw, season, "balldontlie"))

    player_df = pd.concat(player_frames, ignore_index=True) if player_frames else pd.DataFrame()
    team_df = pd.concat(team_frames, ignore_index=True) if team_frames else pd.DataFrame()
    contracts_df = pd.concat(contract_frames, ignore_index=True) if contract_frames else pd.DataFrame()
    merged_df = merge_canonical_tables(player_df, contracts_df, team_df)

    merged_df.to_parquet(processed_dir / "player_season_canonical.parquet", index=False)
    team_df.to_parquet(processed_dir / "team_season_canonical.parquet", index=False)
    contracts_df.to_parquet(processed_dir / "contracts_canonical.parquet", index=False)
    write_data_quality_report(merged_df, processed_dir / "data_quality_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
