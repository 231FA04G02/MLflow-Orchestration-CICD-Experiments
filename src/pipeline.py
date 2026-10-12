from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from src.train import train, DATA, FEATURES, TARGET

def validate_data(path=DATA):
    df = pd.read_csv(path)
    required = set(FEATURES + [TARGET])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset is empty")
    if not set(df[TARGET].dropna().unique()).issubset({0, 1}):
        raise ValueError("Target must be binary 0/1")
    print(f"Data validation passed: {len(df)} rows")
    return True

def run_pipeline():
    validate_data()
    return train()

if __name__ == "__main__":
    run_pipeline()
