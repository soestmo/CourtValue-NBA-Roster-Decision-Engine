from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> tuple[bool, list[str]]:
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing


def summarize_missingness(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["column", "missing_count", "missing_pct"])
    summary = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        }
    )
    return summary.sort_values("missing_pct", ascending=False).reset_index(drop=True)


def flag_suspicious_values(df: pd.DataFrame) -> pd.DataFrame:
    flags: list[dict] = []
    checks = {
        "true_shooting_pct": (0, 1),
        "effective_fg_pct": (0, 1),
        "three_point_attempt_rate": (0, 1),
        "age": (18, 45),
        "games_played": (0, 100),
        "minutes_per_game": (0, 48),
    }
    for column, (low, high) in checks.items():
        if column not in df.columns:
            continue
        out_of_range = (~df[column].isna()) & ((df[column] < low) | (df[column] > high))
        count = int(out_of_range.sum())
        if count > 0:
            flags.append({"column": column, "issue": f"outside [{low}, {high}]", "count": count})
    return pd.DataFrame(flags)


def write_data_quality_report(df: pd.DataFrame, output_path: str | Path) -> None:
    missingness = summarize_missingness(df)
    suspicious = flag_suspicious_values(df)
    output = ["# Data Quality Report", "", "## Missingness", ""]
    output.append(missingness.to_markdown(index=False) if not missingness.empty else "No data available.")
    output.extend(["", "## Suspicious Values", ""])
    output.append(suspicious.to_markdown(index=False) if not suspicious.empty else "No suspicious values detected.")
    Path(output_path).write_text("\n".join(output), encoding="utf-8")
