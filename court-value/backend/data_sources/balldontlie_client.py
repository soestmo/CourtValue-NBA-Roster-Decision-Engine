from __future__ import annotations

import logging
import os
from typing import Any

import pandas as pd
import requests

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://api.balldontlie.io/v1"
TIMEOUT_SECONDS = 20


def _api_key() -> str | None:
    return os.getenv("BALLDONTLIE_API_KEY") or None


def _paged_get(path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    key = _api_key()
    if not key:
        LOGGER.warning("BALLDONTLIE_API_KEY not set; skipping %s", path)
        return []

    headers = {"Authorization": key}
    cursor: int | None = None
    rows: list[dict[str, Any]] = []

    while True:
        query = dict(params or {})
        if cursor is not None:
            query["cursor"] = cursor
        response = requests.get(f"{BASE_URL}/{path}", headers=headers, params=query, timeout=TIMEOUT_SECONDS)
        if response.status_code >= 400:
            LOGGER.warning("BALLDONTLIE request failed for %s: %s", path, response.text)
            return rows
        payload = response.json()
        rows.extend(payload.get("data", []))
        next_cursor = payload.get("meta", {}).get("next_cursor")
        if next_cursor in (None, 0):
            break
        cursor = int(next_cursor)
    return rows


def fetch_players() -> pd.DataFrame:
    rows = _paged_get("players", {"per_page": 100})
    if not rows:
        return pd.DataFrame()
    df = pd.json_normalize(rows)
    return df.rename(columns={"id": "player_id", "team.abbreviation": "team"})


def fetch_teams() -> pd.DataFrame:
    rows = _paged_get("teams", {"per_page": 100})
    if not rows:
        return pd.DataFrame()
    df = pd.json_normalize(rows)
    return df.rename(columns={"id": "team_id", "abbreviation": "team"})


def fetch_salaries_or_contracts(season: int | None = None) -> pd.DataFrame:
    # Free/public BALLDONTLIE plans may not expose salaries. We attempt gracefully.
    params: dict[str, Any] = {"per_page": 100}
    if season is not None:
        params["season"] = season
    rows = _paged_get("salaries", params)
    if not rows:
        return pd.DataFrame()
    df = pd.json_normalize(rows)
    rename_map = {
        "player.id": "player_id",
        "player.first_name": "first_name",
        "player.last_name": "last_name",
        "team.abbreviation": "team",
        "amount": "salary",
    }
    return df.rename(columns=rename_map)
