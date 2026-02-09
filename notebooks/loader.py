import pandas as pd
import os
from config import FULL_PATH

def load_mission_data():
    if not os.path.exists(FULL_PATH):
        # Generate dummy data jika file tidak ditemukan untuk demo cepat
        print("Data not found. Initializing emergency data generation...")
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Sales': [x * 1.5 for x in range(100)],
            'Region': ['North', 'South', 'East', 'West'] * 25
        })
        os.makedirs(os.path.dirname(FULL_PATH), exist_ok=True)
        df.to_csv(FULL_PATH, index=False)
        return df
    return pd.read_csv(FULL_PATH)