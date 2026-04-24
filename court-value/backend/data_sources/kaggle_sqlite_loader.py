from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect

LOGGER = logging.getLogger(__name__)


def load_kaggle_sqlite_tables(db_path: str) -> dict[str, pd.DataFrame]:
    path = Path(db_path)
    if not path.exists():
        LOGGER.warning("Kaggle SQLite path does not exist: %s", db_path)
        return {}

    engine = create_engine(f"sqlite:///{path}")
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    likely_tables = [
        name
        for name in table_names
        if any(token in name.lower() for token in ["player", "team", "game", "box", "salary", "contract"])
    ]
    loaded: dict[str, pd.DataFrame] = {}
    for table in likely_tables:
        try:
            loaded[table] = pd.read_sql_table(table, con=engine)
        except Exception as exc:  # pragma: no cover - schema variance
            LOGGER.warning("Failed loading table %s from %s: %s", table, db_path, exc)
    return loaded


def _load_best_match(db_path: str, tokens: list[str]) -> pd.DataFrame:
    tables = load_kaggle_sqlite_tables(db_path)
    if not tables:
        return pd.DataFrame()
    for name, frame in tables.items():
        lname = name.lower()
        if all(token in lname for token in tokens):
            return frame
    for name, frame in tables.items():
        lname = name.lower()
        if any(token in lname for token in tokens):
            return frame
    return pd.DataFrame()


def load_player_box_scores(db_path: str) -> pd.DataFrame:
    return _load_best_match(db_path, ["box", "player"])


def load_players(db_path: str) -> pd.DataFrame:
    return _load_best_match(db_path, ["player"])


def load_teams(db_path: str) -> pd.DataFrame:
    return _load_best_match(db_path, ["team"])
