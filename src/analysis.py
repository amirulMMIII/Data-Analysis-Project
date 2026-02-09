import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class SalesAnalyzer:
    def __init__(self, data_path):
        # RALAT 1: Pengecekan keberadaan file agar tidak crash di <module>
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Kritikal: File '{data_path}' tidak ditemukan!")
            
        self.df = pd.read_csv(data_path)
        
        # RALAT 2: Penanganan kolom 'date' (Case-sensitivity & Data types)
        # Mengubah semua nama kolom ke lowercase untuk konsistensi
        self.df.columns = [col.lower() for col in self.df.columns]
        
        if 'date' not in self.df.columns:
            raise KeyError("Kolom 'date' tidak ditemukan. Pastikan CSV memiliki kolom tanggal.")
            
        # Konversi ke datetime dengan errors='coerce' (menghindari ralat data rusak)
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        # Hapus baris jika ada tanggal yang gagal dikonversi (NaT)
        self.df = self.df.dropna(subset=['date'])

    def sales_trends_analysis(self):
        """Analyze sales trends over time"""
        # RALAT 3: Pastikan folder 'results' ada sebelum savefig
        os.makedirs('results', exist_ok=True)
        
        monthly_sales = self.df.groupby(self.df['date'].dt.to_period('M'))['total_sales'].sum()
        
        plt.figure(figsize=(12, 6))
        # Convert index ke string untuk plotting yang lebih stabil
        monthly_sales.index = monthly_sales.index.astype(str)
        monthly_sales.plot(kind='line', marker='o')
        plt.title('Monthly Sales Trends')
        plt.xlabel('Month')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('results/monthly_trends.png')
        plt.close() # Menutup plot agar hemat memori
        return monthly_sales

    def category_analysis(self):
        """Analyze performance by category"""
        os.makedirs('results', exist_ok=True)
        category_metrics = self.df.groupby('category').agg({
            'total_sales': ['sum', 'mean', 'count'],
            'customer_rating': 'mean',
            'quantity': 'sum'
        }).round(2)
        
        category_metrics.columns = ['total_sales', 'avg_order_value', 'order_count', 'avg_rating', 'total_quantity']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        category_metrics['total_sales'].plot(kind='bar', ax=ax1)
        ax1.set_title('Total Sales by Category')
        category_metrics['avg_order_value'].plot(kind='bar', ax=ax2, color='orange')
        ax2.set_title('Average Order Value by Category')
        category_metrics['avg_rating'].plot(kind='bar', ax=ax3, color='green')
        ax3.set_title('Average Customer Rating by Category')
        category_metrics['order_count'].plot(kind='bar', ax=ax4, color='red')
        ax4.set_title('Number of Orders by Category')
        
        plt.tight_layout()
        plt.savefig('results/category_analysis.png')
        plt.close()
        return category_metrics

    # ... (fungsi regional_analysis & sales_rep_performance tetap sama, pastikan os.makedirs ada)

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
    # RALAT 4: Gunakan path relatif yang aman
    DATA_FILE = os.path.join('data', 'processed', 'cleaned_sales_data.csv')
    
    try:
        analyzer = SalesAnalyzer(DATA_FILE)
        print("🚀 Memulai Analisis Strategis...")
        
        trends = analyzer.sales_trends_analysis()
        category_metrics = analyzer.category_analysis()
        # analyzer.regional_analysis() # Panggil jika ingin generate pie chart
        insights = analyzer.generate_insights()
        
        print("\n✅ Key Insights Berhasil Diekstrak:")
        for key, value in insights.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
                
    except Exception as e:
        print(f"❌ MISI GAGAL: {e}")