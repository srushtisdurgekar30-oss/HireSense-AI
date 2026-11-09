
import pandas as pd
import json
from pathlib import Path

from src.skill_extractor import extract_skills

print("=" * 55)
print("HIRESENSE AI - BULK SKILL EXTRACTION")
print("=" * 55)

# Load cleaned dataset
input_path = Path("data/cleaned_resumes.csv")

if not input_path.exists():
    raise FileNotFoundError(
        "Cleaned dataset not found. Run preprocess_dataset.py first."
    )

df = pd.read_csv(input_path, encoding="utf-8")

print("\nTotal resumes loaded:", len(df))

# Extract skills from every resume
df["extracted_skills"] = df["cleaned_resume"].apply(
    extract_skills
)

# Count extracted skills
df["skill_count"] = df["extracted_skills"].apply(len)

# Store skills as JSON strings in CSV
df["extracted_skills"] = df["extracted_skills"].apply(
    json.dumps
)

# Save results
output_path = Path("data/resumes_with_skills.csv")

df.to_csv(output_path, index=False, encoding="utf-8")

print("\nSKILL EXTRACTION RESULTS")

print("Total resumes:", len(df))

print(
    "Resumes with recognized skills:",
    (df["skill_count"] > 0).sum()
)

print(
    "Resumes without recognized skills:",
    (df["skill_count"] == 0).sum()
)

print(
    "Average skills per resume:",
    round(df["skill_count"].mean(), 2)
)

print("\nTop 10 recognized skills:")

# Count how many resumes contain each skill
skill_frequency = {}

for skills_json in df["extracted_skills"]:

    skills = json.loads(skills_json)

    for skill in skills:
        skill_frequency[skill] = (
            skill_frequency.get(skill, 0) + 1
        )

top_skills = sorted(
    skill_frequency.items(),
    key=lambda item: item[1],
    reverse=True
)[:10]

for skill, count in top_skills:
    print(f"{skill}: {count} resumes")

print("\nSample candidate:")

sample = df.iloc[0]

print("Candidate ID:", sample["ID"])
print("Category:", sample["Category"])
print(
    "Skills:",
    json.loads(sample["extracted_skills"])
)

print("\nSaved to:", output_path)

print("\nBULK SKILL EXTRACTION COMPLETED!")
