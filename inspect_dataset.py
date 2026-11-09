
import pandas as pd
from pathlib import Path

print("HIRESENSE AI - DATASET INSPECTION")

data_folder = Path("data")
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    print("ERROR: No CSV file found in data folder!")
    raise SystemExit

file_path = csv_files[0]

df = pd.read_csv(file_path, encoding="latin-1")

print("\nDataset:", file_path.name)

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Columns:")
print(df.columns.tolist())

print("\n3. First Five Records:")
print(df.head())

print("\n4. Missing Values:")
print(df.isnull().sum())

print("\n5. Duplicate Records:")
print(df.duplicated().sum())

if "Category" in df.columns:
    print("\n6. Resume Categories:")
    print(df["Category"].value_counts())

print("\n7. Dataset Information:")
df.info()

print("\nDATASET INSPECTION COMPLETED!")
