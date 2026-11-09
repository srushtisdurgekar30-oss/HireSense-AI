
import ast
import sys
from pathlib import Path

import pandas as pd

# Get the main project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root and src folder to Python's import path
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Import modules directly from src
from matching_engine import calculate_final_score
from job_description import process_job_description


def parse_skills(value):
    if isinstance(value, list):
        return value

    if not isinstance(value, str) or not value.strip():
        return []

    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, list) else []
    except (ValueError, SyntaxError):
        return []


def generate_dynamic_ranking(resumes_df, job_description):

    if resumes_df.empty:
        raise ValueError("Resume dataset is empty.")

    if not isinstance(job_description, str) or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    required_columns = {
        "ID",
        "Category",
        "cleaned_resume",
        "extracted_skills"
    }

    missing_columns = required_columns - set(resumes_df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    jd_result = process_job_description(job_description)

    required_skills = jd_result["required_skills"]
    preferred_skills = jd_result["preferred_skills"]

    if not required_skills and not preferred_skills:
        raise ValueError("No recognizable skills found in job description.")

    results = []

    print("Evaluating candidates...")

    for _, row in resumes_df.iterrows():

        resume_text = str(row["cleaned_resume"])
        candidate_skills = parse_skills(row["extracted_skills"])

        score = calculate_final_score(
            resume_text,
            job_description,
            candidate_skills,
            required_skills,
            preferred_skills
        )

        results.append({
            "ID": row["ID"],
            "Category": row["Category"],
            "final_score": score["final_score"],
            "text_similarity": score["text_similarity"],
            "skill_score": score["skill_score"],
            "required_score": score["required_score"],
            "preferred_score": score["preferred_score"],
            "matched_required": ", ".join(score["matched_required"]),
            "missing_required": ", ".join(score["missing_required"]),
            "matched_preferred": ", ".join(score["matched_preferred"]),
            "missing_preferred": ", ".join(score["missing_preferred"])
        })

    ranked_df = pd.DataFrame(results)

    ranked_df = ranked_df.sort_values(
        by="final_score",
        ascending=False
    ).reset_index(drop=True)

    ranked_df.insert(0, "Rank", range(1, len(ranked_df) + 1))

    return ranked_df


if __name__ == "__main__":

    DATA_FILE = PROJECT_ROOT / "data" / "resumes_with_skills.csv"

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    resumes_df = pd.read_csv(DATA_FILE, encoding="latin-1")

    sample_jd = """
    Job Title: Python Developer

    Required skills:
    Python, SQL, Django, Flask, Git.

    Preferred skills:
    AWS, Docker, REST API.
    """

    print("\nGenerating dynamic candidate rankings...")

    results = generate_dynamic_ranking(resumes_df, sample_jd)

    print("\n========== DYNAMIC RANKING COMPLETED ==========")
    print(f"Candidates evaluated: {len(results)}")

    print("\nTOP 10 CANDIDATES:\n")

    print(
        results[
            ["Rank", "ID", "Category", "final_score"]
        ].head(10).to_string(index=False)
    )

    output_path = PROJECT_ROOT / "outputs" / "dynamic_ranked_candidates.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    results.to_csv(output_path, index=False)

    print(f"\nResults saved to: {output_path}")

