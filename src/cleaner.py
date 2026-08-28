# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:20:17 2026

@author: fatemeh
"""

import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

def load_raw_revenue():
    """Load the raw extracted revenue data from all quarters."""
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'apple_revenue_quarterly.csv'))
    df['ds'] = pd.to_datetime(df['ds'])
    return df

def clean_revenue_data(df):
    """
    Clean the revenue data:
    - Remove outliers (values below 10,000 million)
    - Convert to billions consistently
    - Remove duplicates
    - Keep only the most recent revenue for each date
    """
    
    # The SEC data is reported in thousands
    # Convert to billions (divide by 1,000,000)
    df['y_billions'] = df['y'] / 1_000_000
    
    print(f"📊 Raw data: {len(df)} rows")
    print(f"   Revenue range: {df['y_billions'].min():.2f}B to {df['y_billions'].max():.2f}B")
    
    # Remove rows with revenue below $10B (likely not total revenue)
    # Apple's quarterly revenue is typically $80B+
    df_clean = df[df['y_billions'] > 10].copy()
    print(f"   Removed {len(df) - len(df_clean)} rows with revenue < $10B")
    
    # Remove duplicates (keep the most recent entry per date)
    df_clean = df_clean.sort_values('ds')
    df_clean = df_clean.drop_duplicates(subset=['ds'], keep='last')
    print(f"   After removing duplicates: {len(df_clean)} rows")
    
    # Prepare for Prophet (use billions)
    df_prophet = df_clean[['ds', 'y_billions']].copy()
    df_prophet.columns = ['ds', 'y']
    
    # Round to 2 decimal places (billions)
    df_prophet['y'] = df_prophet['y'].round(2)
    
    # Sort by date
    df_prophet = df_prophet.sort_values('ds')
    
    return df_prophet

def save_cleaned_data(df):
    """Save the cleaned data for Prophet."""
    output_path = os.path.join(PROCESSED_DIR, 'apple_revenue_quarterly_clean.csv')
    df.to_csv(output_path, index=False)
    print(f"💾 Saved cleaned data to: {output_path}")
    return output_path

def show_summary(df):
    """Display a summary of the cleaned data."""
    print("\n📋 Cleaned Revenue Data Summary:")
    print(f"   Total quarters: {len(df)}")
    print(f"   Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"   Revenue range: ${df['y'].min():.2f}B to ${df['y'].max():.2f}B")
    
    print("\n📈 Most recent 5 quarters (in $Billions):")
    print(df.tail(5))
    
    # Calculate growth
    if len(df) > 1:
        first = df['y'].iloc[0]
        last = df['y'].iloc[-1]
        growth = ((last - first) / first) * 100
        print(f"\n📊 Revenue growth (from {df['ds'].min().year} to {df['ds'].max().year}): {growth:.2f}%")

if __name__ == "__main__":
    # Load raw data
    df_raw = load_raw_revenue()
    
    # Clean
    df_clean = clean_revenue_data(df_raw)
    
    # Save
    save_cleaned_data(df_clean)
    
    # Show summary
    show_summary(df_clean)