import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.cleaned_df = None
    
    def clean_data(self):
        """Comprehensive data cleaning process"""
        print("Starting data cleaning process...")
        
        # Make a copy for cleaning
        self.cleaned_df = self.df.copy()
        
        # Convert date column
        self.cleaned_df['date'] = pd.to_datetime(self.cleaned_df['date'])
        
        # Remove duplicates
        initial_count = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.drop_duplicates()
        print(f"Removed {initial_count - len(self.cleaned_df)} duplicates")
        
        # Handle missing values
        self.cleaned_df['category'].fillna('Unknown', inplace=True)
        self.cleaned_df['customer_rating'].fillna(self.cleaned_df['customer_rating'].median(), inplace=True)
        
        # Remove outliers (sales > 3 standard deviations)
        mean_sales = self.cleaned_df['total_sales'].mean()
        std_sales = self.cleaned_df['total_sales'].std()
        outlier_threshold = mean_sales + (3 * std_sales)
        
        outliers = len(self.cleaned_df[self.cleaned_df['total_sales'] > outlier_threshold])
        self.cleaned_df = self.cleaned_df[self.cleaned_df['total_sales'] <= outlier_threshold]
        print(f"Removed {outliers} outliers")
        
        # Create additional features
        self.cleaned_df['month'] = self.cleaned_df['date'].dt.month
        self.cleaned_df['quarter'] = self.cleaned_df['date'].dt.quarter
        self.cleaned_df['day_of_week'] = self.cleaned_df['date'].dt.day_name()
        
        return self.cleaned_df
    
    def get_data_summary(self):
        """Generate data quality summary"""
        summary = {
            'total_records': len(self.cleaned_df),
            'date_range': f"{self.cleaned_df['date'].min()} to {self.cleaned_df['date'].max()}",
            'total_sales': self.cleaned_df['total_sales'].sum(),
            'avg_order_value': self.cleaned_df['total_sales'].mean(),
            'categories': self.cleaned_df['category'].nunique(),
            'regions': self.cleaned_df['region'].nunique()
        }
        return summary
    
    def save_cleaned_data(self, filename='data/processed/cleaned_sales_data.csv'):
        """Save cleaned data"""
        if self.cleaned_df is not None:
            self.cleaned_df.to_csv(filename, index=False)
            print(f"Cleaned data saved to {filename}")

if __name__ == "__main__":
    cleaner = DataCleaner('data/raw/sales_data.csv')
    cleaned_data = cleaner.clean_data()
    summary = cleaner.get_data_summary()
    print("\nData Summary:", summary)
    cleaner.save_cleaned_data()