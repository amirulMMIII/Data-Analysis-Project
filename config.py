import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append('..') # Benarkan notebook akses folder utama
from config import DATA_PATH 

df = pd.read_csv(f"../{DATA_PATH}")