from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

DataMode = Literal["sample", "real", "auto"]


@dataclass(frozen=True)
class Settings:
    data_mode: DataMode = "auto"
    balldontlie_api_key: str | None = None
    kaggle_nba_sqlite_path: str | None = None


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


def get_settings() -> Settings:
    requested_mode = (os.getenv("COURTVALUE_DATA_MODE", "auto") or "auto").lower()
    mode: DataMode = "auto" if requested_mode not in {"sample", "real", "auto"} else requested_mode  # type: ignore[assignment]
    return Settings(
        data_mode=mode,
        balldontlie_api_key=os.getenv("BALLDONTLIE_API_KEY") or None,
        kaggle_nba_sqlite_path=os.getenv("KAGGLE_NBA_SQLITE_PATH") or None,
    )
