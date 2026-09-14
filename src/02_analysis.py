from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import CSV_PATH, setup_logging  # noqa: E402

logger = setup_logging()


def analyze(df: pd.DataFrame) -> dict:
    stats = {
        "mean_temperature": float(df["Temperature"].mean()),
        "min_temperature": float(df["Temperature"].min()),
        "max_temperature": float(df["Temperature"].max()),
        "mean_humidity": float(df["Humidity"].mean()),
        "count_normal": int((df["Status"] == "Normal").sum()),
        "count_warning": int((df["Status"] == "Warning").sum()),
        "count_critical": int((df["Status"] == "Critical").sum()),
        "n": int(len(df)),
    }
    return stats


def print_stats(stats: dict) -> None:
    print("\n=== Environment analysis ===")
    print(f"Samples            : {stats['n']}")
    print(f"Mean temperature   : {stats['mean_temperature']:.2f} °C")
    print(f"Min temperature    : {stats['min_temperature']:.2f} °C")
    print(f"Max temperature    : {stats['max_temperature']:.2f} °C")
    print(f"Mean humidity      : {stats['mean_humidity']:.2f} %")
    print(f"Normal             : {stats['count_normal']}")
    print(f"Warning            : {stats['count_warning']}")
    print(f"Critical           : {stats['count_critical']}")
    logger.info("Analysis complete: %s", stats)


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV not found: {CSV_PATH}. Run 01_generate_and_label.py first.")
    df = pd.read_csv(CSV_PATH)
    stats = analyze(df)
    print_stats(stats)


if __name__ == "__main__":
    main()
