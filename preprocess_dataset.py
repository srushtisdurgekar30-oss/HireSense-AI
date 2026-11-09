
import pandas as pd
from pathlib import Path

from src.preprocessing import clean_resume

print("=" * 50)
print("HIRESENSE AI - RESUME PREPROCESSING")
print("=" * 50)

# Find dataset
csv_files = list(Path("data").glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV found inside data folder!")

df = pd.read_csv(csv_files[0], encoding="latin-1")

# Verify columns
required_columns = ["ID", "Resume_str", "Category"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

print("\nOriginal dataset:", df.shape)

# Clean resume text
df["cleaned_resume"] = df["Resume_str"].apply(clean_resume)

# Remove empty resumes
df = df[df["cleaned_resume"].str.strip() != ""].copy()

# Save processed dataset
output_path = Path("data/cleaned_resumes.csv")

df.to_csv(output_path, index=False, encoding="utf-8")

print("\nPREPROCESSING RESULTS")
print("Processed resumes:", len(df))
print("Empty resumes:", (df["cleaned_resume"].str.strip() == "").sum())

print("\nSample cleaned resume:")
print(df["cleaned_resume"].iloc[0][:500])

print("\nSaved to:", output_path)

print("\nPREPROCESSING COMPLETED SUCCESSFULLY!")
