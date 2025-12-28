import pandas as pd
from pathlib import Path

# Dossier racine de tes datasets
DATA_ROOT = Path("Talent Datasets-premium")

def load_all_datasets():
    datasets = {}
    if not DATA_ROOT.exists():
        return datasets
        
    for csv in DATA_ROOT.rglob("*.csv"):
        try:
            df = pd.read_csv(csv)
            if not df.empty:
                datasets[csv.stem] = df
        except Exception as e:
            print(f"Error loading {csv}: {e}")
    return datasets
