import pandas as pd
import xgboost as xgb
import joblib
import os

def train_sales_model(data_path='data/raw_sales.csv'):
    # 1. Load Data
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found. Run data_loader.py first!")
        return

    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['prev_day_sales'] = df.groupby('product_id')['sales'].shift(1)
    df = df.dropna() 
    
    # 3. Prepare Features
    X = df[['day_of_week', 'month', 'prev_day_sales', 'price']]
    y = df['sales']
    
    # 4. Train Model
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
    model.fit(X, y)
    
    # 5. Create folder if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # 6. Save the model
    joblib.dump(model, 'models/sales_model.pkl')
    print("✅ Model Trained and Saved to /models/sales_model.pkl")

if __name__ == "__main__":
    train_sales_model()