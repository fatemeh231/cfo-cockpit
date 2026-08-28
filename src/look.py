import pandas as pd
import os
import glob
from pathlib import Path

# Set paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'

# List of companies we want (search terms)
COMPANY_SEARCH_TERMS = [
    # Technology
    ('AAPL', 'APPLE INC'),
    ('MSFT', 'MICROSOFT'),
    ('GOOGL', 'ALPHABET'),
    ('AMZN', 'AMAZON'),
    ('META', 'META PLATFORMS'),
    ('NVDA', 'NVIDIA'),
    ('TSLA', 'TESLA'),
    ('AVGO', 'BROADCOM'),
    ('AMD', 'ADVANCED MICRO DEVICES'),
    ('ORCL', 'ORACLE'),
    ('INTC', 'INTEL'),
    ('CSCO', 'CISCO'),
    ('CRM', 'SALESFORCE'),
    ('IBM', 'IBM'),
    ('NFLX', 'NETFLIX'),
    
    # Financials
    ('JPM', 'JPMORGAN'),
    ('BAC', 'BANK OF AMERICA'),
    ('V', 'VISA'),
    ('MA', 'MASTERCARD'),
    ('WFC', 'WELLS FARGO'),
    ('C', 'CITIGROUP'),
    ('GS', 'GOLDMAN SACHS'),
    
    # Healthcare
    ('JNJ', 'JOHNSON & JOHNSON'),
    ('LLY', 'ELI LILLY'),
    ('PFE', 'PFIZER'),
    ('ABBV', 'ABBVIE'),
    ('MRK', 'MERCK'),
    ('UNH', 'UNITEDHEALTH'),
    
    # Energy
    ('XOM', 'EXXON MOBIL'),
    ('CVX', 'CHEVRON'),
    ('COP', 'CONOCOPHILLIPS'),
    
    # Retail & Consumer
    ('WMT', 'WALMART'),
    ('COST', 'COSTCO'),
    ('HD', 'HOME DEPOT'),
    ('MCD', "MCDONALD'S"),
    ('NKE', 'NIKE'),
    ('SBUX', 'STARBUCKS'),
    
    # Communications & Media
    ('DIS', 'WALT DISNEY'),
    ('T', 'AT&T'),
    ('VZ', 'VERIZON'),
    
    # Industrials
    ('GE', 'GENERAL ELECTRIC'),
    ('CAT', 'CATERPILLAR'),
    ('BA', 'BOEING'),
    
    # Other
    ('BRK.B', 'BERKSHIRE HATHAWAY'),
    ('PLTR', 'PALANTIR'),
    ('UBER', 'UBER'),
    ('SHOP', 'SHOPIFY')
]

def extract_ciks_from_sub():
    """
    Extract CIK numbers from sub.txt files for all companies.
    """
    # Find all quarter folders
    quarter_folders = sorted([f for f in os.listdir(RAW_DATA_DIR) 
                             if f.startswith('20') and os.path.isdir(os.path.join(RAW_DATA_DIR, f))])
    
    if not quarter_folders:
        print("❌ No quarter folders found.")
        return {}
    
    print(f"📂 Found {len(quarter_folders)} quarter folders")
    
    cik_map = {}
    
    # Use the most recent quarter (better chance of having all companies)
    for quarter in reversed(quarter_folders):  # Start from newest
        sub_file = os.path.join(RAW_DATA_DIR, quarter, 'sub.txt')
        
        if not os.path.exists(sub_file):
            continue
            
        print(f"\n📖 Searching in {quarter}...")
        
        # Load sub.txt
        df_sub = pd.read_csv(sub_file, sep='\t', low_memory=False, dtype=str)
        
        # Search for each company
        for ticker, search_term in COMPANY_SEARCH_TERMS:
            if ticker in cik_map:  # Already found
                continue
                
            # Search for the company name (case-insensitive)
            matches = df_sub[df_sub['name'].str.contains(search_term, case=False, na=False)]
            
            if not matches.empty:
                # Get the first match
                row = matches.iloc[0]
                cik = row['cik']
                full_name = row['name']
                cik_map[ticker] = {
                    'cik': cik,
                    'name': full_name,
                    'quarter': quarter
                }
                print(f"   ✅ {ticker}: CIK = {cik} ({full_name})")
        
        # If we found all companies, stop
        if len(cik_map) == len(COMPANY_SEARCH_TERMS):
            print("\n🎯 Found all companies!")
            break
    
    return cik_map

def save_cik_map(cik_map):
    """
    Save CIK mappings to CSV.
    """
    if not cik_map:
        print("❌ No CIK mappings found.")
        return
    
    data = []
    for ticker, info in cik_map.items():
        data.append({
            'ticker': ticker,
            'cik': info['cik'],
            'company_name': info['name'],
            'quarter_found': info['quarter']
        })
    
    df = pd.DataFrame(data)
    output_path = PROJECT_ROOT / 'data' / 'processed' / 'company_ciks.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Saved {len(data)} CIK mappings to {output_path}")
    
    return df

if __name__ == "__main__":
    print("🔍 Extracting CIK Numbers from SEC Data")
    print("="*50)
    
    cik_map = extract_ciks_from_sub()
    
    if cik_map:
        df = save_cik_map(cik_map)
        
        print(f"\n📊 Summary:")
        print(f"   Found {len(cik_map)} companies out of {len(COMPANY_SEARCH_TERMS)}")
        
        # Show companies that were NOT found
        found_tickers = set(cik_map.keys())
        all_tickers = set([t for t, _ in COMPANY_SEARCH_TERMS])
        missing = all_tickers - found_tickers
        if missing:
            print(f"\n⚠️ Companies NOT found:")
            for ticker in sorted(missing):
                print(f"   {ticker}")
    else:
        print("❌ No CIK mappings found.")