from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import CSV_PATH, PLOT_PATH, ensure_dirs, setup_logging

logger = setup_logging()


def plot_temperature(df: pd.DataFrame, out=PLOT_PATH) -> Path:
    ensure_dirs()
    times = pd.to_datetime(df["Time"])
    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f7f9fb")

    ax.plot(times, df["Temperature"], color="#2f6690", linewidth=1.6, label="Temperature")

    warn = df["Status"] == "Warning"
    crit = df["Status"] == "Critical"
    ax.scatter(times[warn], df.loc[warn, "Temperature"], color="#e0a537", s=28, zorder=3, label="Warning")
    ax.scatter(times[crit], df.loc[crit, "Temperature"], color="#d1495b", s=36, zorder=4, label="Critical")

    ax.axhline(30, color="#9aa5b1", linestyle="--", linewidth=0.8, alpha=0.8)
    ax.axhline(35, color="#d1495b", linestyle="--", linewidth=0.8, alpha=0.8)

    ax.set_title("Environment temp. over time", color="#1f2937", pad=12)
    ax.set_xlabel("Time", color="#374151")
    ax.set_ylabel("Temperature (°C)", color="#374151")
    ax.tick_params(colors="#374151")
    for spine in ax.spines.values():
        spine.set_color("#d1d5db")
    ax.legend(facecolor="#ffffff", edgecolor="#d1d5db", labelcolor="#1f2937")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    logger.info("Plot saved to %s", out)
    return out


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV not found: {CSV_PATH}. Run 01_generate_and_label.py first.")
    df = pd.read_csv(CSV_PATH)
    path = plot_temperature(df)
    print(f"Plot written: {path}")


if __name__ == "__main__":
    main()
