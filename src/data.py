# src/data_yfinance.py
import yfinance as yf
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')

def fetch_revenue_from_yfinance(ticker="AAPL"):
    """
    Fetch revenue data from Yahoo Finance.
    Returns a Prophet-ready DataFrame with 'ds' and 'y' columns.
    """
    print(f"📊 Fetching revenue for {ticker} from Yahoo Finance...")
    
    stock = yf.Ticker(ticker)
    
    # Get income statement (quarterly or annual)
    # Try annual first, then quarterly
    try:
        income = stock.financials  # Annual income statement
    except:
        income = stock.quarterly_financials  # Quarterly fallback
    
    if income is None or income.empty:
        print("❌ No income statement found.")
        return None
    
    # Find the revenue column
    revenue_col = None
    for col in income.index:
        if 'Total Revenue' in col or 'Revenue' in col:
            revenue_col = col
            break
    
    if revenue_col is None:
        print("⚠️ Could not find 'Revenue' column. Available columns:")
        print(income.index.tolist())
        return None
    
    # Extract revenue series (columns are dates)
    revenue_series = income.loc[revenue_col]
    
    # Convert to Prophet format
    df_prophet = revenue_series.reset_index()
    df_prophet.columns = ['ds', 'y']
    
    # Ensure ds is datetime
    df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
    df_prophet = df_prophet.sort_values('ds')
    
    # Save raw data
    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    filepath = os.path.join(DATA_RAW_PATH, f"{ticker}_revenue.csv")
    df_prophet.to_csv(filepath, index=False)
    print(f"💾 Saved revenue data to {filepath}")
    
    return df_prophet

if __name__ == "__main__":
    ticker = input("Enter ticker (default: AAPL): ") or "AAPL"
    df = fetch_revenue_from_yfinance(ticker)
    
    if df is not None:
        print("\n📋 Revenue data ready:")
        print(df.head())
        print(f"Shape: {df.shape}")
        print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")