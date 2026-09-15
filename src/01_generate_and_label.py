from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import (
    CSV_PATH,
    HUM_MAX,
    HUM_MIN,
    NUM_SAMPLES,
    TEMP_MAX,
    TEMP_MIN,
    classify_status,
    ensure_dirs,
    setup_logging,
    status_alert,
)

logger = setup_logging()


def generate_series(n: int, seed: int = 42) -> pd.DataFrame:
    """Random-walk temperature/humidity so the time series looks like a real room."""
    rng = np.random.default_rng(seed)
    temp = 26.5
    hum = 48.0
    rows = []
    start = datetime.now().replace(microsecond=0) - timedelta(minutes=5 * n)

    for i in range(n):
        temp += float(rng.normal(0, 0.55))
        hum += float(rng.normal(0, 2.2))
        if rng.random() < 0.05:
            temp += float(rng.uniform(3.5, 9.0))
        if rng.random() < 0.03:
            temp -= float(rng.uniform(2.0, 5.0))
        temp = float(np.clip(temp, TEMP_MIN, TEMP_MAX))
        hum = float(np.clip(hum, HUM_MIN, HUM_MAX))

        t = start + timedelta(minutes=5 * i)
        status = classify_status(temp, hum)
        rows.append(
            {
                "Time": t.strftime("%Y-%m-%d %H:%M:%S"),
                "Temperature": round(temp, 2),
                "Humidity": round(hum, 2),
                "Status": status,
            }
        )
    return pd.DataFrame(rows)


def save_csv(df: pd.DataFrame, path=CSV_PATH) -> None:
    ensure_dirs()
    df.to_csv(path, index=False)
    logger.info("Saved %d records to %s", len(df), path)


def load_csv(path=CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    logger.info("Reloaded %d records from %s", len(df), path)
    return df


def print_alerts(df: pd.DataFrame) -> None:
    alerts = []
    for _, row in df.iterrows():
        msg = status_alert(row["Status"], float(row["Temperature"]), str(row["Time"]))
        if msg:
            alerts.append(msg)
            logger.warning(msg)
    logger.info("Alert count: %d of %d records", len(alerts), len(df))


def main() -> None:
    n = NUM_SAMPLES
    logger.info("Generating %d labelled sensor records", n)
    df = generate_series(n)
    save_csv(df)
    reloaded = load_csv()
    print(reloaded.head(8).to_string(index=False))
    print("...")
    print(reloaded.tail(3).to_string(index=False))
    print_alerts(reloaded)
    print(f"\nCSV columns: {list(reloaded.columns)}")
    print(f"Status mix:\n{reloaded['Status'].value_counts().to_string()}")


if __name__ == "__main__":
    main()
