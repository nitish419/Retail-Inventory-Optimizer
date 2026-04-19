import pandas as pd
import numpy as np

def generate_mock_data():
    """Generates 2 years of synthetic retail data."""
    dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq='D')
    products = ['Item_A', 'Item_B', 'Item_C']
    data = []

    for prod in products:
        base_sales = np.random.randint(50, 100)
        for date in dates:
            # Add seasonality (higher sales on weekends)
            weekday_effect = 1.5 if date.weekday() >= 5 else 1.0
            # Add random noise
            noise = np.random.normal(0, 5)
            sales = max(0, int(base_sales * weekday_effect + noise))
            data.append([date, prod, sales, np.random.uniform(10, 50)])

    df = pd.DataFrame(data, columns=['date', 'product_id', 'sales', 'price'])
    df.to_csv('data/raw_sales.csv', index=False)
    print("✅ Synthetic Dataset Created in /data")

if __name__ == "__main__":
    generate_mock_data()