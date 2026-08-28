# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:09:33 2026

@author: fatemeh
"""

import os
import zipfile
from pathlib import Path

# Set the directory where your ZIP files are
RAW_DIR = r"C:\Users\fatemeh\OneDrive\Desktop\codes_tutorial_uni\cfo-cockpit\data\raw"

def extract_all_zips():
    """
    Extract every ZIP file in RAW_DIR into a folder named after the ZIP file.
    Skips extraction if the folder already exists.
    """
    # Change to the raw directory
    os.chdir(RAW_DIR)
    
    # Get all ZIP files
    zip_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.zip')]
    
    print(f"📦 Found {len(zip_files)} ZIP files")
    
    for zip_file in zip_files:
        # Create folder name (remove .zip extension)
        folder_name = zip_file.replace('.zip', '')
        folder_path = os.path.join(RAW_DIR, folder_name)
        
        # Skip if folder already exists
        if os.path.exists(folder_path):
            print(f"⏭️  Skipping {zip_file} – folder already exists")
            continue
        
        # Extract
        print(f"📂 Extracting {zip_file}...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            print(f"✅ Extracted to {folder_name}/")
        except Exception as e:
            print(f"❌ Error extracting {zip_file}: {e}")

if __name__ == "__main__":
    extract_all_zips()