# CourtValue V2 Data Sources

## Source overview
- **nba_api**: primary player/team season stats source from NBA.com endpoints.
- **BALLDONTLIE**: optional players/teams/salary-contract style endpoint source.
- **Kaggle SQLite NBA DB**: optional historical backfill when local SQLite file is available.
- **Sample CSVs**: deterministic fallback used when real data is not available.

## Fields used
- Player stats: IDs, names, age, team, games, minutes, usage, shooting efficiency, playmaking/defense rates, proxy BPM, on/off proxy.
- Team stats: team identifier, season, ratings/pace where available.
- Contracts: player ID, salary, years remaining when available, inferred contract type by salary band.

## Credentials required
- `nba_api`: none
- `BALLDONTLIE`: `BALLDONTLIE_API_KEY` (optional)
- `Kaggle SQLite`: `KAGGLE_NBA_SQLITE_PATH` (optional local file)

## Limitations
- Source schemas can change; canonicalization handles missing columns defensively.
- BALLDONTLIE contract/salary availability can vary.
- Kaggle table naming varies by dump version.
- Tracking-grade vendor metrics are not included.

## Fallback behavior
- `COURTVALUE_DATA_MODE=sample`: sample CSV only.
- `COURTVALUE_DATA_MODE=real`: requires processed canonical parquet.
- `COURTVALUE_DATA_MODE=auto`: uses processed real parquet if present, else sample CSV.

## Canonical table definitions
- `player_season_canonical.parquet`: canonical player-season features used by model/feature pipeline.
- `team_season_canonical.parquet`: canonical team-season context metrics.
- `contracts_canonical.parquet`: canonical contract table.

## Reliability notes
- `nba_api`: generally reliable but rate-limited/network-dependent.
- `BALLDONTLIE`: reliable for basic resources; salary coverage account-dependent.
- Kaggle SQLite: stable once downloaded locally, but schema names differ across versions.
