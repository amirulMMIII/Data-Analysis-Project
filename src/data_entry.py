import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataEntrySystem:
    def __init__(self):
        self.data = []
    
    def generate_sample_data(self, num_records=1000):
        """Generate sample sales data for demonstration"""
        
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        regions = ['North', 'South', 'East', 'West', 'Central']
        sales_reps = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown']
        
        start_date = datetime(2023, 1, 1)
        
        for i in range(num_records):
            record = {
                'order_id': f'ORD-{1000 + i}',
                'date': start_date + timedelta(days=random.randint(0, 365)),
                'category': random.choice(categories),
                'product_name': f'Product {random.randint(1, 100)}',
                'quantity': random.randint(1, 10),
                'unit_price': round(random.uniform(10, 500), 2),
                'region': random.choice(regions),
                'sales_rep': random.choice(sales_reps),
                'customer_rating': random.randint(1, 5)
            }
            record['total_sales'] = record['quantity'] * record['unit_price']
            self.data.append(record)
        
        return pd.DataFrame(self.data)
    
    def manual_entry(self):
        """Function for manual data entry"""
        print("=== Sales Data Entry System ===")
        
        while True:
            try:
                order_id = input("Order ID (or 'quit' to exit): ")
                if order_id.lower() == 'quit':
                    break
                
                date = input("Date (YYYY-MM-DD): ")
                category = input("Category: ")
                product_name = input("Product Name: ")
                quantity = int(input("Quantity: "))
                unit_price = float(input("Unit Price: "))
                region = input("Region: ")
                sales_rep = input("Sales Rep: ")
                rating = int(input("Customer Rating (1-5): "))
                
                record = {
                    'order_id': order_id,
                    'date': pd.to_datetime(date),
                    'category': category,
                    'product_name': product_name,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_sales': quantity * unit_price,
                    'region': region,
                    'sales_rep': sales_rep,
                    'customer_rating': rating
                }
                
                self.data.append(record)
                print("Record added successfully!\n")
                
            except (ValueError, KeyboardInterrupt):
                print("Invalid input or operation cancelled.\n")
    
    def save_data(self, filename='data/raw/sales_data.csv'):
        """Save data to CSV file"""
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save")

if __name__ == "__main__":
    data_entry = DataEntrySystem()
    # Generate sample data
    df = data_entry.generate_sample_data(1000)
    data_entry.save_data()
    print("Sample data generated and saved!")