# RackSense — IoT server-room environment monitor

Practical exam project: simulate temperature/humidity sensors, store them in CSV,
classify the room, analyse, plot, and train a Decision Tree.

## Project tree

```
iot_environment_monitor/
├── data/
│   └── sensor_data.csv          # Time | Temperature | Humidity | Status
├── models/
│   └── decision_tree_model.joblib
├── plots/
│   └── temperature_over_time.png
├── logs/
│   └── run.log
├── src/
│   ├── utils.py                 # thresholds + classify_status (professor changes here)
│   ├── 01_generate_and_label.py # Sections 1–3
│   ├── 02_analysis.py           # Section 4
│   ├── 03_plotting.py           # Section 5
│   └── 04_train_model.py        # Section 6
├── app.py                       # optional Streamlit dashboard
├── requirements.txt
├── run_all.sh
└── README.md
```

## Run order

```bash
pip install -r requirements.txt
python src/01_generate_and_label.py   # ≥200 rows + Status, save/reload CSV
python src/02_analysis.py             # mean / min / max / status counts
python src/03_plotting.py             # temperature vs time (Warning/Critical marked)
python src/04_train_model.py          # Decision Tree, accuracy, predict 33°C / 42%
```

Or all at once:

```bash
bash run_all.sh
```

Optional Streamlit UI:

```bash
streamlit run app.py
```

## Exam mapping

| Section | Script | What it does |
|--------|--------|--------------|
| 1 Data generation | `01_generate_and_label.py` | ≥200 samples, Temp 15–40, Humidity 20–90, timestamps |
| 2 CSV save/load | same | columns `Time \| Temperature \| Humidity \| Status` |
| 3 Status rules | `utils.classify_status` | Normal ≤30, Warning ≤35, Critical >35 + alerts |
| 4 Analysis | `02_analysis.py` | mean/min/max temp, mean humidity, status counts |
| 5 Plot | `03_plotting.py` | temp vs time + Warning/Critical markers |
| 6 ML | `04_train_model.py` | Decision Tree, train/test, accuracy, predict 33/42 |
| 7 Professor change | edit `src/utils.py` only | thresholds, humidity rule, None, etc. |

## Where the professor-change lives

Status rules are **only** in `src/utils.py`:

- `NUM_SAMPLES`
- `THRESHOLD_WARNING` / `THRESHOLD_CRITICAL`
- `classify_status()` — add humidity, handle `None`, consecutive Critical, etc.

Every other script imports that function, so a threshold change is one edit.

## Deliverables checklist

- [x] Python `.py` files
- [x] `data/sensor_data.csv`
- [x] Plot image under `plots/`
- [x] Trained model under `models/`
- [x] README explaining each part
