from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_players() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sample_players.csv")


def load_contracts() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sample_contracts.csv")


def load_team_contexts() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sample_team_context.csv")


def get_player_row(players_df: pd.DataFrame, player_id: int) -> pd.Series | None:
    filtered = players_df[players_df["player_id"] == player_id]
    if filtered.empty:
        return None
    return filtered.iloc[0]


def get_team_context(team_context_df: pd.DataFrame, team_code: str) -> pd.Series | None:
    filtered = team_context_df[team_context_df["team_code"] == team_code]
    if filtered.empty:
        return None
    return filtered.iloc[0]
