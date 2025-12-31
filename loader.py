import pandas as pd
from pathlib import Path

def load_all_datasets():
    datasets = {}

    # 1) Racine du repo (là où il y a app.py et tes CSV premium_*.csv)
    root = Path(".")

    # Chercher tous les CSV à la racine qui commencent par "premium_"
    root_csv = list(root.glob("premium_*.csv"))

    # 2) Éventuel dossier Talent Datasets-premium (optionnel)
    data_dir = root / "Talent Datasets-premium"
    dir_csv = list(data_dir.glob("*.csv")) if data_dir.exists() else []

    all_csv = root_csv + dir_csv

    if not all_csv:
        # Aucun fichier trouvé → le message "No datasets detected" sera affiché par app.py
        return datasets

    for csv_path in all_csv:
        try:
            df = pd.read_csv(csv_path)
            if not df.empty:
                datasets[csv_path.stem] = df
        except Exception:
            # On ignore les fichiers invalides pour ne pas casser l'app
            continue

    return datasets
