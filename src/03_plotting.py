from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import CSV_PATH, PLOT_PATH, ensure_dirs, setup_logging  # noqa: E402

logger = setup_logging()


def plot_temperature(df: pd.DataFrame, out=PLOT_PATH) -> Path:
    ensure_dirs()
    times = pd.to_datetime(df["Time"])
    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.patch.set_facecolor("#0b0d10")
    ax.set_facecolor("#14181d")

    ax.plot(times, df["Temperature"], color="#8ba4b8", linewidth=1.6, label="Temperature")

    warn = df["Status"] == "Warning"
    crit = df["Status"] == "Critical"
    ax.scatter(times[warn], df.loc[warn, "Temperature"], color="#d4a054", s=28, zorder=3, label="Warning")
    ax.scatter(times[crit], df.loc[crit, "Temperature"], color="#c45c4a", s=36, zorder=4, label="Critical")

    ax.axhline(30, color="#6b7280", linestyle="--", linewidth=0.8, alpha=0.7)
    ax.axhline(35, color="#c45c4a", linestyle="--", linewidth=0.8, alpha=0.7)

    ax.set_title("Server-room temperature over time", color="#e8ecef", pad=12)
    ax.set_xlabel("Time", color="#a8b0b8")
    ax.set_ylabel("Temperature (°C)", color="#a8b0b8")
    ax.tick_params(colors="#a8b0b8")
    for spine in ax.spines.values():
        spine.set_color("#2a3038")
    ax.legend(facecolor="#1a1f26", edgecolor="#2a3038", labelcolor="#e8ecef")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out, dpi=140)
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
