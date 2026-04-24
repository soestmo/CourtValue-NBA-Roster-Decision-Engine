from pathlib import Path

import pandas as pd

from services.data_quality import (
    flag_suspicious_values,
    summarize_missingness,
    validate_required_columns,
    write_data_quality_report,
)


def test_validate_required_columns() -> None:
    df = pd.DataFrame([{"a": 1, "b": 2}])
    ok, missing = validate_required_columns(df, ["a", "b", "c"])
    assert not ok
    assert missing == ["c"]


def test_missingness_and_flags() -> None:
    df = pd.DataFrame([{"age": 17, "true_shooting_pct": 1.2, "minutes_per_game": 50}, {"age": 25, "true_shooting_pct": None, "minutes_per_game": 20}])
    missingness = summarize_missingness(df)
    flags = flag_suspicious_values(df)
    assert "missing_pct" in missingness.columns
    assert not flags.empty


def test_write_data_quality_report(tmp_path: Path) -> None:
    path = tmp_path / "report.md"
    write_data_quality_report(pd.DataFrame([{"age": 20}]), path)
    assert path.exists()
