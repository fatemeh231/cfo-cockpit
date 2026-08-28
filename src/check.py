import pandas as pd
import os
from pathlib import Path

# Set project root (two levels up from this script)
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'

# Choose a quarter (e.g., 2026q2)
quarter = '2026q2'
sub_file = RAW_DATA_DIR / quarter / 'sub.txt'
num_file = RAW_DATA_DIR / quarter / 'num.txt'

print(f"📂 Reading: {sub_file}")
print(f"📂 Reading: {num_file}")

# Load sub.txt
df_sub = pd.read_csv(sub_file, sep='\t', low_memory=False, dtype=str)

# Find Apple
apple_sub = df_sub[df_sub['cik'].astype(str).str.zfill(10) == '0000320193']
print("\nApple submissions:")
print(apple_sub[['adsh', 'name', 'form', 'period']])

if not apple_sub.empty:
    adsh = apple_sub['adsh'].iloc[0]
    print(f"\nADSH: {adsh}")
    
    # Load num.txt
    df_num = pd.read_csv(num_file, sep='\t', low_memory=False, dtype=str)
    
    # Filter for Apple's submission
    apple_num = df_num[df_num['adsh'] == adsh]
    print(f"\nFound {len(apple_num)} financial rows for Apple")
    
    # Show the tags available
    tags = apple_num['tag'].value_counts().head(20)
    print("\nTop 20 tags:")
    print(tags)
    
    # Look specifically for revenue-related tags
    revenue_tags = apple_num[apple_num['tag'].str.contains('Revenue', case=False, na=False)]
    print(f"\nFound {len(revenue_tags)} revenue-related rows")
    
    if not revenue_tags.empty:
        print("\nRevenue rows (first 10):")
        print(revenue_tags[['tag', 'value', 'ddate', 'qtrs', 'uom']].head(10))
        
        # Show raw values and units
        print("\nValue and unit types:")
        print(revenue_tags[['value', 'uom']].drop_duplicates())