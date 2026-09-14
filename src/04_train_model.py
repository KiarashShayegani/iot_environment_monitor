from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import CSV_PATH, MODEL_PATH, ensure_dirs, setup_logging

logger = setup_logging()

NEW_SAMPLE = {"Temperature": 33.0, "Humidity": 42.0}


def train(df: pd.DataFrame):
    x = df[["Temperature", "Humidity"]]
    y = df["Status"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y if y.nunique() > 1 else None
    )
    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    return model, acc, y_test, y_pred


def save_model(model) -> None:
    ensure_dirs()
    joblib.dump(model, MODEL_PATH)
    logger.info("Saved model to %s", MODEL_PATH)


def load_model():
    return joblib.load(MODEL_PATH)


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV not found: {CSV_PATH}. Run 01_generate_and_label.py first.")
    df = pd.read_csv(CSV_PATH)
    model, acc, y_test, y_pred = train(df)
    save_model(model)
    print(f"\nDecision Tree test accuracy: {acc:.2%}")
    print(classification_report(y_test, y_pred, zero_division=0))

    sample = pd.DataFrame([NEW_SAMPLE])
    pred = model.predict(sample)[0]
    print(
        f"Prediction for Temperature={NEW_SAMPLE['Temperature']}, "
        f"Humidity={NEW_SAMPLE['Humidity']}  →  {pred}"
    )
    logger.info("Predicted %s for sample %s (accuracy=%.3f)", pred, NEW_SAMPLE, acc)


if __name__ == "__main__":
    main()
