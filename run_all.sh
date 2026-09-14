#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 src/01_generate_and_label.py
python3 src/02_analysis.py
python3 src/03_plotting.py
python3 src/04_train_model.py
