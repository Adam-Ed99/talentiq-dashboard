import streamlit as st
import pandas as pd
from pathlib import Path
import os

@st.cache_data
def load_all_datasets():
    st.write("🔍 Scanning for datasets...")
    
    # Scan TOUS les CSV du projet (racine + sous-dossiers)
    root = Path(".")
    all_csv = list(root.rglob("*.csv"))
    
    st.write(f"📁 Found {len(all_csv)} CSV files:")
    for csv in all_csv:
        st.write(f"  - {csv}")
    
    datasets = {}
    for csv in all_csv:
        try:
            df = pd.read_csv(csv)
            if len(df) > 0:
                name = csv.stem
                datasets[name] = df
                st.success(f"✅ Loaded {name} ({len(df)} rows)")
        except Exception as e:
            st.error(f"❌ Error {csv.name}: {e}")
    
    st.write(f"🎯 {len(datasets)} datasets ready!")
    return datasets

# Test direct
if __name__ == "__main__":
    datasets = load_all_datasets()
    print(list(datasets.keys()))
