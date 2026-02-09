import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class SalesAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        
    def sales_trends_analysis(self):
        """Analyze sales trends over time"""
        monthly_sales = self.df.groupby(self.df['date'].dt.to_period('M'))['total_sales'].sum()
        
        plt.figure(figsize=(12, 6))
        monthly_sales.plot(kind='line', marker='o')
        plt.title('Monthly Sales Trends')
        plt.xlabel('Month')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('results/monthly_trends.png')
        plt.show()
        
        return monthly_sales
    
    def category_analysis(self):
        """Analyze performance by category"""
        category_metrics = self.df.groupby('category').agg({
            'total_sales': ['sum', 'mean', 'count'],
            'customer_rating': 'mean',
            'quantity': 'sum'
        }).round(2)
        
        # Flatten column names
        category_metrics.columns = ['total_sales', 'avg_order_value', 'order_count', 'avg_rating', 'total_quantity']
        
        # Visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Total sales by category
        category_metrics['total_sales'].plot(kind='bar', ax=ax1)
        ax1.set_title('Total Sales by Category')
        ax1.set_ylabel('Total Sales ($)')
        
        # Average order value
        category_metrics['avg_order_value'].plot(kind='bar', ax=ax2, color='orange')
        ax2.set_title('Average Order Value by Category')
        ax2.set_ylabel('AOV ($)')
        
        # Customer ratings
        category_metrics['avg_rating'].plot(kind='bar', ax=ax3, color='green')
        ax3.set_title('Average Customer Rating by Category')
        ax3.set_ylabel('Rating (1-5)')
        
        # Order count
        category_metrics['order_count'].plot(kind='bar', ax=ax4, color='red')
        ax4.set_title('Number of Orders by Category')
        ax4.set_ylabel('Order Count')
        
        plt.tight_layout()
        plt.savefig('results/category_analysis.png')
        plt.show()
        
        return category_metrics
    
    def regional_analysis(self):
        """Analyze performance by region"""
        regional_data = self.df.groupby('region').agg({
            'total_sales': 'sum',
            'order_id': 'count',
            'customer_rating': 'mean'
        }).round(2)
        
        regional_data.columns = ['total_sales', 'order_count', 'avg_rating']
        
        # Create pie chart for sales distribution
        plt.figure(figsize=(10, 5))
        
        plt.subplot(1, 2, 1)
        plt.pie(regional_data['total_sales'], labels=regional_data.index, autopct='%1.1f%%')
        plt.title('Sales Distribution by Region')
        
        plt.subplot(1, 2, 2)
        regional_data['avg_rating'].plot(kind='bar')
        plt.title('Average Rating by Region')
        plt.ylabel('Rating')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('results/regional_analysis.png')
        plt.show()
        
        return regional_data
    
    def sales_rep_performance(self):
        """Analyze sales representative performance"""
        rep_performance = self.df.groupby('sales_rep').agg({
            'total_sales': 'sum',
            'order_id': 'count',
            'customer_rating': 'mean'
        }).round(2)
        
        rep_performance.columns = ['total_sales', 'orders', 'avg_rating']
        rep_performance = rep_performance.sort_values('total_sales', ascending=False)
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        rep_performance['total_sales'].plot(kind='bar')
        plt.title('Sales Performance by Sales Representative')
        plt.ylabel('Total Sales ($)')
        
        plt.subplot(2, 1, 2)
        rep_performance['avg_rating'].plot(kind='bar', color='green')
        plt.title('Average Customer Rating by Sales Rep')
        plt.ylabel('Rating')
        
        plt.tight_layout()
        plt.savefig('results/sales_rep_performance.png')
        plt.show()
        
        return rep_performance
    
    def generate_insights(self):
        """Generate key business insights"""
        insights = {
            'total_revenue': self.df['total_sales'].sum(),
            'total_orders': len(self.df),
            'avg_order_value': self.df['total_sales'].mean(),
            'best_category': self.df.groupby('category')['total_sales'].sum().idxmax(),
            'best_region': self.df.groupby('region')['total_sales'].sum().idxmax(),
            'best_sales_rep': self.df.groupby('sales_rep')['total_sales'].sum().idxmax(),
            'peak_month': self.df.groupby(self.df['date'].dt.month)['total_sales'].sum().idxmax(),
            'avg_rating': self.df['customer_rating'].mean()
        }
        
        return insights

if __name__ == "__main__":
    analyzer = SalesAnalyzer('data/processed/cleaned_sales_data.csv')
    
    print("Generating analysis...")
    trends = analyzer.sales_trends_analysis()
    category_metrics = analyzer.category_analysis()
    regional_data = analyzer.regional_analysis()
    rep_performance = analyzer.sales_rep_performance()
    insights = analyzer.generate_insights()
    
    print("\nKey Insights:")
    for key, value in insights.items():
        print(f"{key}: {value}")