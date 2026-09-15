from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from utils import CSV_PATH, MODEL_PATH, PLOT_PATH, classify_status

st.set_page_config(page_title="IoT monitoring", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; color: #1f2937; }

    .rs-predict-box {
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.9rem;
        border: 1px solid #e5e7eb;
    }
    .rs-predict-label {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 0.25rem;
    }
    .rs-predict-value {
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .rs-status-normal   { background-color: #ecfdf3; border-color: #a7e3bd; }
    .rs-status-normal   .rs-predict-value { color: #15803d; }
    .rs-status-warning  { background-color: #fff8e6; border-color: #f0d489; }
    .rs-status-warning  .rs-predict-value { color: #b45309; }
    .rs-status-critical { background-color: #fdecec; border-color: #f0a8a8; }
    .rs-status-critical .rs-predict-value { color: #b91c1c; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("IoT environment monitoring")

if not CSV_PATH.exists():
    st.warning("No CSV yet. Run: python src/01_generate_and_label.py")
    st.stop()

df = pd.read_csv(CSV_PATH)
df["Time"] = pd.to_datetime(df["Time"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean temp", f"{df['Temperature'].mean():.1f} °C")
c2.metric("Min / Max", f"{df['Temperature'].min():.1f} / {df['Temperature'].max():.1f}")
c3.metric("Mean humidity", f"{df['Humidity'].mean():.1f} %")
c4.metric("Critical", int((df["Status"] == "Critical").sum()))

st.subheader("Temperature over time")
if PLOT_PATH.exists():
    st.image(str(PLOT_PATH), use_container_width=True)
else:
    st.warning("No plot yet. Run: python src/03_plotting.py")
    st.line_chart(df.set_index("Time")["Temperature"])

st.subheader("Records")
st.dataframe(df, use_container_width=True)

st.subheader("Predict a new reading")
t = st.number_input("Temperature (°C)", value=33.0, min_value=15.0, max_value=40.0)
h = st.number_input("Humidity (%)", value=42.0, min_value=20.0, max_value=90.0)


def status_card(label: str, status: str) -> None:
    status_class = {
        "Normal": "rs-status-normal",
        "Warning": "rs-status-warning",
        "Critical": "rs-status-critical",
    }.get(status, "rs-status-normal")
    st.markdown(
        f"""
        <div class="rs-predict-box {status_class}">
            <div class="rs-predict-label">{label}</div>
            <div class="rs-predict-value">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


col_rule, col_ml = st.columns(2)

with col_rule:
    rule = classify_status(t, h)
    status_card("Rule-based output:", rule)

with col_ml:
    if MODEL_PATH.exists():
        import joblib

        model = joblib.load(MODEL_PATH)
        pred = model.predict(pd.DataFrame([{"Temperature": t, "Humidity": h}]))[0]
        status_card("Decision-tree output:", pred)
    else:
        st.info("Train the model first: python src/04_train_model.py")
