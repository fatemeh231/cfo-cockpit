import pandas as pd
import os
import glob
from pathlib import Path
import time
import logging
from datetime import datetime

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

CIK_FILE = PROCESSED_DATA_DIR / 'company_ciks.csv'

# Revenue tags to look for
REVENUE_TAGS = [
    'Revenues',
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'Revenue',
    'TotalRevenue',
    'SalesRevenueNet'
]

# -------------------------------------------------------------------
# Core extraction function
# -------------------------------------------------------------------
def extract_company_revenue(ticker, cik, company_name):
    """
    Extract and clean revenue data for a single company from all quarters.
    
    Parameters:
        ticker (str): Stock ticker (e.g., 'AAPL')
        cik (str): SEC CIK number
        company_name (str): Full company name
    
    Returns:
        pd.DataFrame: Cleaned data with columns [ds, y, ticker, company_name]
    """
    logger.info(f"Processing {ticker} ({company_name})...")
    
    cik_str = str(cik).zfill(10)
    all_rows = []
    
    # Get all quarter folders
    quarter_folders = sorted(glob.glob(str(RAW_DATA_DIR / '20*')))
    if not quarter_folders:
        logger.error("No quarter folders found in %s", RAW_DATA_DIR)
        return None
    
    for folder in quarter_folders:
        quarter_name = os.path.basename(folder)
        sub_file = os.path.join(folder, 'sub.txt')
        num_file = os.path.join(folder, 'num.txt')
        
        if not os.path.exists(sub_file) or not os.path.exists(num_file):
            continue
        
        try:
            # 1. Load sub.txt and find company
            df_sub = pd.read_csv(sub_file, sep='\t', low_memory=False, dtype=str)
            company_sub = df_sub[df_sub['cik'].astype(str).str.zfill(10) == cik_str]
            if company_sub.empty:
                continue
            
            adsh = company_sub['adsh'].iloc[0]
            
            # 2. Load num.txt and filter for this submission
            df_num = pd.read_csv(num_file, sep='\t', low_memory=False, dtype=str)
            company_num = df_num[df_num['adsh'] == adsh]
            if company_num.empty:
                continue
            
            # 3. Find revenue rows
            revenue_data = company_num[company_num['tag'].isin(REVENUE_TAGS)]
            if revenue_data.empty:
                # Try partial match
                revenue_data = company_num[company_num['tag'].str.contains('Revenue', case=False, na=False)]
                if revenue_data.empty:
                    continue
            
            # 4. Extract values
            for _, row in revenue_data.iterrows():
                date_str = row.get('ddate')
                if pd.isna(date_str):
                    continue
                date = pd.to_datetime(str(date_str), format='%Y%m%d', errors='coerce')
                if pd.isna(date):
                    continue
                
                value_str = row.get('value')
                if pd.isna(value_str) or value_str == '':
                    continue
                try:
                    value = float(value_str)
                except:
                    continue
                if value == 0:
                    continue
                
                all_rows.append({
                    'ticker': ticker,
                    'company_name': company_name,
                    'date': date,
                    'tag': row['tag'],
                    'value_raw': value,
                    'quarter': quarter_name,
                    'uom': row.get('uom', 'USD')
                })
        except Exception as e:
            # Skip problematic quarters silently
            continue
    
    if not all_rows:
        logger.warning(f"No revenue data found for {ticker}")
        return None
    
    # -------------------------------------------------------------------
    # Clean: deduplicate, detect unit, convert to billions
    # -------------------------------------------------------------------
    df = pd.DataFrame(all_rows)
    
    # Keep only the most recent value per date
    df = df.sort_values('date').drop_duplicates(subset=['date', 'ticker'], keep='last')
    
    # Detect unit from the values
    sample_vals = df['value_raw'].head(100).tolist()
    avg_val = sum(sample_vals) / len(sample_vals) if sample_vals else 0
    
    if avg_val > 1_000_000_000:
        # Values are in actual dollars → divide by 1,000,000,000 to get billions
        df['y'] = (df['value_raw'] / 1_000_000_000).round(2)
        logger.info(f"   Detected: actual dollars (÷1e9)")
    elif avg_val > 1_000_000:
        # Values are in thousands → divide by 1,000,000 to get billions
        df['y'] = (df['value_raw'] / 1_000_000).round(2)
        logger.info(f"   Detected: thousands (÷1e6)")
    else:
        # Values are already in billions or millions
        df['y'] = df['value_raw'].round(2)
        logger.info(f"   Detected: already in billions/millions")
    
    # Remove outliers (revenue below 0.01B or above 10,000B is impossible)
    df = df[(df['y'] > 0.01) & (df['y'] < 10000)]
    
    # Prepare for Prophet
    df_prophet = df[['date', 'y']].copy()
    df_prophet.columns = ['ds', 'y']
    df_prophet = df_prophet.sort_values('ds')
    df_prophet['ticker'] = ticker
    df_prophet['company_name'] = company_name
    df_prophet = df_prophet.dropna(subset=['ds', 'y'])
    
    if df_prophet.empty:
        logger.warning(f"No valid data after cleaning for {ticker}")
        return None
    
    # Save individual CSV
    out_file = PROCESSED_DATA_DIR / f'{ticker}_revenue.csv'
    df_prophet.to_csv(out_file, index=False)
    logger.info(f"✅ {ticker}: {len(df_prophet)} records saved")
    
    return df_prophet


# -------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------
def main():
    """Main function to extract revenue for all companies."""
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting revenue extraction for all companies")
    logger.info("=" * 60)
    
    # Load CIK mappings
    if not CIK_FILE.exists():
        logger.error(f"CIK file not found: {CIK_FILE}")
        logger.error("Please run extract_ciks_from_files.py first.")
        return
    
    df_ciks = pd.read_csv(CIK_FILE)
    logger.info(f"Loaded {len(df_ciks)} companies from {CIK_FILE}")
    
    # Extract each company
    results = {}
    for idx, row in df_ciks.iterrows():
        ticker = row['ticker']
        cik = row['cik']
        name = row['company_name']
        
        df = extract_company_revenue(ticker, cik, name)
        if df is not None:
            results[ticker] = df
        
        # Polite delay to avoid overloading disk
        time.sleep(0.2)
    
    # -------------------------------------------------------------------
    # Combine all results into one master CSV
    # -------------------------------------------------------------------
    if results:
        all_dfs = []
        for ticker, df in results.items():
            all_dfs.append(df[['ticker', 'company_name', 'ds', 'y']])
        
        combined = pd.concat(all_dfs, ignore_index=True)
        combined = combined.sort_values(['ticker', 'ds'])
        
        out_combined = PROCESSED_DATA_DIR / 'all_companies_revenue.csv'
        combined.to_csv(out_combined, index=False)
        logger.info(f"\n✅ Combined data saved to {out_combined}")
        
        # Summary statistics
        summary = combined.groupby('ticker').agg({
            'y': ['count', 'min', 'max', 'mean']
        })
        logger.info("\n📊 Summary per company:")
        logger.info(summary)
        
        elapsed = datetime.now() - start_time
        logger.info(f"\n✅ Completed in {elapsed.total_seconds():.1f} seconds")
        logger.info(f"   Total companies processed: {len(results)} / {len(df_ciks)}")
        
        # List missing companies
        missing = set(df_ciks['ticker']) - set(results.keys())
        if missing:
            logger.info(f"   Missing: {', '.join(missing)}")
    else:
        logger.error("No data extracted for any company.")


if __name__ == "__main__":
    main()
    
    