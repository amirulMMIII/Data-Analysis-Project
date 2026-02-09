import streamlit as st
import pandas as pd
import plotly.express as px
from config import FULL_PATH

st.set_page_config(page_title="Sales Shadow Dashboard", layout="wide")

st.title("🔥 Sales Performance Analytics")
st.markdown("---")

# Load Data
df = pd.read_csv(FULL_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar Filters
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
filtered_df = df[df['Region'].isin(region)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Avg Sale", f"${filtered_df['Sales'].mean():,.2f}")
col3.metric("Total Transactions", len(filtered_df))

# Visuals
fig = px.line(filtered_df, x='Date', y='Sales', title="Sales Trend Over Time")
st.plotly_chart(fig, use_container_width=True)