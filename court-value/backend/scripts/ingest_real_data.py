from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from config import get_settings
from data_sources.balldontlie_client import fetch_salaries_or_contracts
from data_sources.kaggle_sqlite_loader import load_kaggle_sqlite_tables
from data_sources.nba_api_client import (
    fetch_league_advanced_player_stats,
    fetch_league_player_stats,
    fetch_team_stats,
)
from data_sources.source_registry import build_source_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest real NBA data sources")
    parser.add_argument("--seasons", nargs="+", required=True)
    parser.add_argument("--mode", choices=["auto", "real", "sample"], default="auto")
    parser.add_argument("--output-dir", default="backend/data/raw")
    return parser.parse_args()




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
    settings = get_settings()
    mode = args.mode or settings.data_mode
    output_dir = _normalize_repo_relative(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if mode == "sample":
        print("mode=sample; skipping real ingestion")
        return 0

    any_real_data = False
    for season in args.seasons:
        basic = fetch_league_player_stats(season)
        advanced = fetch_league_advanced_player_stats(season)
        team = fetch_team_stats(season)
        if not basic.empty:
            basic.to_parquet(output_dir / f"nba_api_player_basic_{season}.parquet", index=False)
            any_real_data = True
        if not advanced.empty:
            advanced.to_parquet(output_dir / f"nba_api_player_advanced_{season}.parquet", index=False)
            any_real_data = True
        if not team.empty:
            team.to_parquet(output_dir / f"nba_api_team_advanced_{season}.parquet", index=False)
            any_real_data = True

        try:
            season_year = int(season.split("-")[0])
        except Exception:
            season_year = None
        contracts = fetch_salaries_or_contracts(season_year)
        if not contracts.empty:
            contracts.to_parquet(output_dir / f"balldontlie_contracts_{season}.parquet", index=False)
            any_real_data = True

    kaggle_path = settings.kaggle_nba_sqlite_path
    if kaggle_path and Path(kaggle_path).exists():
        tables = load_kaggle_sqlite_tables(kaggle_path)
        for name, df in tables.items():
            if not df.empty:
                df.to_parquet(output_dir / f"kaggle_{name}.parquet", index=False)
                any_real_data = True

    report = {
        "mode": mode,
        "seasons": args.seasons,
        "sources": build_source_registry(bool(os.getenv("BALLDONTLIE_API_KEY")), kaggle_path),
        "any_real_data": any_real_data,
    }
    (output_dir / "source_availability_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    if mode == "real" and not any_real_data:
        raise RuntimeError("mode=real but no real source data was ingested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
