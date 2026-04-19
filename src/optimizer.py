import pandas as pd

def get_item_catalog(data_path='data/raw_sales.csv'):
    """Fetches unique items from our 'database'."""
    try:
        df = pd.read_csv(data_path)
        # Returns a sorted list of unique product IDs
        return sorted(df['product_id'].unique().tolist())
    except Exception as e:
        print(f"Catalog Error: {e}")
        return ["Item_A", "Item_B", "Item_C"] # Fallback if data isn't found

def calculate_inventory_metrics(forecast_value, lead_time=3):
    """Business logic for safety stock and ROP."""
    safety_stock = int(forecast_value * 0.2)
    reorder_point = (forecast_value * lead_time) + safety_stock
    return safety_stock, reorder_point