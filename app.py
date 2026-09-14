from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from utils import CSV_PATH, MODEL_PATH, classify_status

st.set_page_config(page_title="RackSense", layout="wide")
st.title("RackSense — server-room monitor")

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
st.line_chart(df.set_index("Time")["Temperature"])

st.subheader("Records")
st.dataframe(df, use_container_width=True)

st.subheader("Predict a new reading")
t = st.number_input("Temperature (°C)", value=33.0, min_value=15.0, max_value=40.0)
h = st.number_input("Humidity (%)", value=42.0, min_value=20.0, max_value=90.0)
rule = classify_status(t, h)
st.write(f"Rule-based status: **{rule}**")

if MODEL_PATH.exists():
    import joblib

    model = joblib.load(MODEL_PATH)
    pred = model.predict(pd.DataFrame([{"Temperature": t, "Humidity": h}]))[0]
    st.write(f"Decision-tree status: **{pred}**")
else:
    st.info("Train the model first: python src/04_train_model.py")
