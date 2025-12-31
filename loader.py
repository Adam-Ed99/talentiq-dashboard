import pandas as pd
from pathlib import Path
import os

print("=== LOADER DEBUG ===")
print(f"Working directory: {os.getcwd()}")
print(f"Files in root: {os.listdir('.')}")

# Dossier racine de tes datasets
DATA_ROOT = Path("Talent Datasets-premium")
print(f"DATA_ROOT path: {DATA_ROOT}")
print(f"DATA_ROOT exists: {DATA_ROOT.exists()}")
print(f"DATA_ROOT is dir: {DATA_ROOT.is_dir()}")

if DATA_ROOT.exists():
    print(f"Files in DATA_ROOT: {os.listdir(DATA_ROOT)}")
    csv_files = list(DATA_ROOT.glob("*.csv"))
    print(f"CSV files found: {[f.name for f in csv_files]}")

def load_all_datasets():
    print("=== load_all_datasets START ===")
    datasets = {}
    
    if not DATA_ROOT.exists():
        print(f"ERROR: DATA_ROOT does not exist: {DATA_ROOT}")
        return datasets
        
    print(f"Scanning {DATA_ROOT} for CSV files...")
    csv_files = list(DATA_ROOT.rglob("*.csv"))
    print(f"Found {len(csv_files)} CSV files: {[f.name for f in csv_files]}")
    
    for csv in csv_files:
        try:
            print(f"Loading {csv}...")
            df = pd.read_csv(csv)
            print(f"  -> Loaded {len(df)} rows")
            if not df.empty:
                datasets[csv.stem] = df
            else:
                print(f"  -> Empty dataset skipped")
        except Exception as e:
            print(f"ERROR loading {csv}: {e}")
    
    print(f"Final datasets: {list(datasets.keys())}")
    print("=== load_all_datasets END ===")
    return datasets
