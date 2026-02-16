# config.py - Singleton Configuration Node
import os

# Definisikan path secara absolut/relatif yang stabil
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = "data/sales_data.csv" # Pastikan folder data ada
FULL_PATH = os.path.join(BASE_DIR, DATA_PATH)

# Parameter Visualisasi (Optimization)
THEME_COLOR = "#2E86C1"
CHART_STYLE = "whitegrid"
