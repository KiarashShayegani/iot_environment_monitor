from __future__ import annotations

import logging
from pathlib import Path

# --- Project paths -----------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models"
PLOTS_DIR = ROOT / "plots"
LOGS_DIR = ROOT / "logs"
CSV_PATH = DATA_DIR / "sensor_data.csv"
MODEL_PATH = MODELS_DIR / "decision_tree_model.joblib"
PLOT_PATH = PLOTS_DIR / "temperature_over_time.png"
LOG_PATH = LOGS_DIR / "run.log"

# --- Tunable constants (professor-change friendly) ---------------------------
NUM_SAMPLES = 200  # change this number; must stay >= 50

TEMP_MIN = 15.0
TEMP_MAX = 60.0
HUM_MIN = 20.0
HUM_MAX = 98.0

# Normal  if temperature <= THRESHOLD_WARNING
# Warning if THRESHOLD_WARNING < temperature <= THRESHOLD_CRITICAL
# Critical if temperature > THRESHOLD_CRITICAL
THRESHOLD_WARNING = 30.0
THRESHOLD_CRITICAL = 40.0

HUM_THSH_WARNING = 50

VALID_STATUSES = ("Normal", "Warning", "Critical")


def ensure_dirs() -> None:
    for folder in (DATA_DIR, MODELS_DIR, PLOTS_DIR, LOGS_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def setup_logging(name: str = "racksense") -> logging.Logger:
    """Console + file logging. Safe to call from every script."""
    ensure_dirs()
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(fmt)
    file_h = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_h.setFormatter(fmt)
    logger.addHandler(stream)
    logger.addHandler(file_h)
    return logger


def classify_status(temperature: float | None, humidity: float | None = None) -> str:
    """
    Rule-based environment status.

    Humidity is accepted so the signature matches the ML model, but the
    exam rules only use temperature. Adding a humidity condition later
    (professor change) is a one-line edit here.
    """
    if temperature is None:
        return "Unknown"
    if (temperature < 0 or temperature > 100) or (humidity is not None and (humidity < 0 or humidity > 100)):
        return "Invalid"

    hum_high = humidity is not None and humidity > HUM_THSH_WARNING

    if temperature > THRESHOLD_CRITICAL and hum_high:
        return "Critical"
    if temperature > THRESHOLD_WARNING and hum_high:
        return "Warning"
    return "Normal"


def status_alert(status: str, temperature: float, time_str: str) -> str | None:
    """Return a human-readable warning, or None for Normal."""
    if status == "Warning":
        return (
            f"[WARNING] Temperature {temperature:.1f}°C at {time_str} "
            "is above the safe band. Check cooling."
        )
    if status == "Critical":
        return (
            f"[CRITICAL] Temperature {temperature:.1f}°C at {time_str} "
            "exceeds the critical limit. Immediate action required."
        )
    return None
