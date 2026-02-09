import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configure page
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    """Load and cache the cleaned data"""
    try:
        df = pd.read_csv('data/processed/cleaned_sales_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run data generation first.")
        return None

def main():
    st.title("📊 Sales Performance Dashboard")
    st.sidebar.title("Navigation")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[df['date'].min().date(), df['date'].max().date()],
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )
    
    # Category filter
    categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    
    # Region filter
    regions = st.sidebar.multiselect(
        "Select Regions",
        options=df['region'].unique(),
        default=df['region'].unique()
    )
    
    # Filter data
    filtered_df = df[
        (df['date'].dt.date >= date_range[0]) &
        (df['date'].dt.date <= date_range[1]) &
        (df['category'].isin(categories)) &
        (df['region'].isin(regions))
    ]
    
    # Main dashboard
    page = st.sidebar.selectbox("Choose Page", ["Overview", "Sales Trends", "Category Analysis", "Regional Analysis", "Sales Rep Performance"])
    
    if page == "Overview":
        show_overview(filtered_df)
    elif page == "Sales Trends":
        show_trends(filtered_df)
    elif page == "Category Analysis":
        show_category_analysis(filtered_df)
    elif page == "Regional Analysis":
        show_regional_analysis(filtered_df)
    elif page == "Sales Rep Performance":
        show_rep_performance(filtered_df)

def show_overview(df):
    st.header("📈 Overview")
    
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${df['total_sales'].sum():,.2f}",
            delta=f"{len(df)} orders"
        )
    
    with col2:
        st.metric(
            label="Average Order Value",
            value=f"${df['total_sales'].mean():.2f}",
            delta=f"{df['customer_rating'].mean():.1f}★ avg rating"
        )
    
    with col3:
        st.metric(
            label="Top Category",
            value=df.groupby('category')['total_sales'].sum().idxmax(),
            delta=f"${df.groupby('category')['total_sales'].sum().max():,.0f}"
        )
    
    with col4:
        st.metric(
            label="Top Region",
            value=df.groupby('region')['total_sales'].sum().idxmax(),
            delta=f"${df.groupby('region')['total_sales'].sum().max():,.0f}"
        )
    
    # Sales over time
    st.subheader("Sales Trend")
    daily_sales = df.groupby(df['date'].dt.date)['total_sales'].sum().reset_index()
    fig = px.line(daily_sales, x='date', y='total_sales', title="Daily Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

def show_trends(df):
    st.header("📊 Sales Trends")
    
    # Monthly trends
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_sales'].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_sales.index.astype(str),
        y=monthly_sales.values,
        mode='lines+markers',
        name='Monthly Sales'
    ))
    fig.update_layout(title="Monthly Sales Trends", xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Day of week analysis
    dow_sales = df.groupby('day_of_week')['total_sales'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    
    fig = px.bar(x=dow_sales.index, y=dow_sales.values, title="Sales by Day of Week")
    st.plotly_chart(fig, use_container_width=True)

def show_category_analysis(df):
    st.header("🏷️ Category Analysis")
    
    category_metrics = df.groupby('category').agg({
        'total_sales': 'sum',
        'order_id': 'count',
        'customer_rating': 'mean'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(values=category_metrics['total_sales'], names=category_metrics.index, 
                    title="Sales Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(x=category_metrics.index, y=category_metrics['customer_rating'], 
                    title="Average Rating by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Category Performance Table")
    st.dataframe(category_metrics, use_container_width=True)

def show_regional_analysis(df):
    st.header("🗺️ Regional Analysis")
    
    regional_data = df.groupby('region').agg({
        'total_sales': 'sum',
        'order_id': 'count',
        'customer_rating': 'mean'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(x=regional_data.index, y=regional_data['total_sales'], 
                    title="Total Sales by Region")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(x=regional_data['order_id'], y=regional_data['customer_rating'],
                        text=regional_data.index, title="Orders vs Rating by Region")
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

def show_rep_performance(df):
    st.header("👥 Sales Representative Performance")
    
    rep_performance = df.groupby('sales_rep').agg({
        'total_sales': 'sum',
        'order_id': 'count',
        'customer_rating': 'mean'
    }).round(2)
    
    rep_performance = rep_performance.sort_values('total_sales', ascending=True)
    
    fig = px.bar(x=rep_performance['total_sales'], y=rep_performance.index, 
                orientation='h', title="Sales Performance by Representative")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Performance Metrics")
    st.dataframe(rep_performance, use_container_width=True)

if __name__ == "__main__":
    main()