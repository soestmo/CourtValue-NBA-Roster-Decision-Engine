from __future__ import annotations

import logging
import time
from typing import Any, Callable

import pandas as pd

LOGGER = logging.getLogger(__name__)

REQUEST_RETRIES = 3
REQUEST_SLEEP_SECONDS = 0.8
REQUEST_TIMEOUT_SECONDS = 30


def _call_endpoint(endpoint_factory: Callable[[], Any], result_index: int = 0) -> pd.DataFrame:
    last_error: Exception | None = None
    for attempt in range(1, REQUEST_RETRIES + 1):
        try:
            endpoint = endpoint_factory()
            data_frames = endpoint.get_data_frames()
            if not data_frames:
                return pd.DataFrame()
            return data_frames[result_index]
        except Exception as exc:  # pragma: no cover - external API behavior
            last_error = exc
            LOGGER.warning("nba_api request failed attempt %s/%s: %s", attempt, REQUEST_RETRIES, exc)
            time.sleep(REQUEST_SLEEP_SECONDS * attempt)
    LOGGER.error("nba_api request failed after retries: %s", last_error)
    return pd.DataFrame()


def fetch_league_player_stats(season: str) -> pd.DataFrame:
    from nba_api.stats.endpoints import LeagueDashPlayerStats

    return _call_endpoint(
        lambda: LeagueDashPlayerStats(
            season=season,
            per_mode_detailed="PerGame",
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    )


def fetch_league_advanced_player_stats(season: str) -> pd.DataFrame:
    from nba_api.stats.endpoints import LeagueDashPlayerStats

    return _call_endpoint(
        lambda: LeagueDashPlayerStats(
            season=season,
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Advanced",
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    )


def fetch_team_stats(season: str) -> pd.DataFrame:
    from nba_api.stats.endpoints import LeagueDashTeamStats

    return _call_endpoint(
        lambda: LeagueDashTeamStats(
            season=season,
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Advanced",
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    )


def fetch_player_tracking_stats(season: str, pt_measure_type: str) -> pd.DataFrame:
    try:
        from nba_api.stats.endpoints import LeagueDashPtStats
    except Exception as exc:  # pragma: no cover - import dependent on nba_api version
        LOGGER.warning("LeagueDashPtStats unavailable: %s", exc)
        return pd.DataFrame()

    return _call_endpoint(
        lambda: LeagueDashPtStats(
            season=season,
            per_mode_simple="PerGame",
            pt_measure_type=pt_measure_type,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    )
