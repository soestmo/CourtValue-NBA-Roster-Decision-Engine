from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class SourceStatus:
    name: str
    available: bool
    required_credentials: list[str]
    expected_fields: list[str]
    status: str


EXPECTED_FIELDS = {
    "nba_api": ["PLAYER_ID", "PLAYER_NAME", "TEAM_ABBREVIATION", "USG_PCT", "TS_PCT"],
    "balldontlie": ["player_id", "salary", "team"],
    "kaggle_sqlite": ["players", "teams", "games", "box_scores"],
}


def build_source_registry(has_balldontlie_key: bool, kaggle_path: str | None) -> list[dict]:
    kaggle_available = bool(kaggle_path and Path(kaggle_path).exists())
    statuses = [
        SourceStatus(
            name="nba_api",
            available=True,
            required_credentials=[],
            expected_fields=EXPECTED_FIELDS["nba_api"],
            status="primary source for player/team stats",
        ),
        SourceStatus(
            name="balldontlie",
            available=has_balldontlie_key,
            required_credentials=["BALLDONTLIE_API_KEY"],
            expected_fields=EXPECTED_FIELDS["balldontlie"],
            status="optional salary/contracts source",
        ),
        SourceStatus(
            name="kaggle_sqlite",
            available=kaggle_available,
            required_credentials=["KAGGLE_NBA_SQLITE_PATH"],
            expected_fields=EXPECTED_FIELDS["kaggle_sqlite"],
            status="optional historical backfill source",
        ),
    ]
    return [asdict(item) for item in statuses]
