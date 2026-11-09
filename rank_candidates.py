
import ast
from pathlib import Path

import pandas as pd

from job_description import process_job_description
from src.matching_engine import calculate_final_score


# File locations
DATA_FILE = Path("data/resumes_with_skills.csv")
JOB_FILE = Path("data/job_description.txt")
OUTPUT_DIR = Path("outputs")

OUTPUT_DIR.mkdir(exist_ok=True)


def load_candidate_skills(value):
    """Convert the saved skill list into a Python list."""
    if isinstance(value, list):
        return value

    if not isinstance(value, str) or not value.strip():
        return []

    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, list) else []
    except (ValueError, SyntaxError):
        return []


def rank_candidates():

    print("\nLoading resume dataset...")

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing file: {DATA_FILE}")

    if not JOB_FILE.exists():
        raise FileNotFoundError(f"Missing file: {JOB_FILE}")

    df = pd.read_csv(DATA_FILE, encoding="latin-1")

    required_columns = {
        "ID", "Category", "cleaned_resume", "extracted_skills"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")

    print(f"Total resumes loaded: {len(df)}")

    # Load and process job description
    job_text = JOB_FILE.read_text(encoding="utf-8")
    job_result = process_job_description(job_text)

    required_skills = job_result["required_skills"]
    preferred_skills = job_result["preferred_skills"]

    print(f"Required skills: {required_skills}")
    print(f"Preferred skills: {preferred_skills}")

    if not required_skills and not preferred_skills:
        raise ValueError(
            "No skills detected in the job description. "
            "Check your job description and skill dictionary."
        )

    results = []

    print("\nEvaluating candidates...")

    for _, row in df.iterrows():

        resume_text = str(row["cleaned_resume"])
        candidate_skills = load_candidate_skills(
            row["extracted_skills"]
        )

        score_result = calculate_final_score(
            resume_text,
            job_text,
            candidate_skills,
            required_skills,
            preferred_skills
        )

        results.append({
            "ID": row["ID"],
            "Category": row["Category"],
            "final_score": score_result["final_score"],
            "text_similarity": score_result["text_similarity"],
            "skill_score": score_result["skill_score"],
            "required_score": score_result["required_score"],
            "preferred_score": score_result["preferred_score"],
            "matched_required": ", ".join(
                score_result["matched_required"]
            ),
            "missing_required": ", ".join(
                score_result["missing_required"]
            ),
            "matched_preferred": ", ".join(
                score_result["matched_preferred"]
            ),
            "missing_preferred": ", ".join(
                score_result["missing_preferred"]
            )
        })

    ranked_df = pd.DataFrame(results)

    ranked_df = ranked_df.sort_values(
        by="final_score",
        ascending=False
    ).reset_index(drop=True)

    ranked_df.insert(0, "Rank", range(1, len(ranked_df) + 1))

    output_file = OUTPUT_DIR / "ranked_candidates.csv"
    ranked_df.to_csv(output_file, index=False)

    print("\n========== RANKING COMPLETED ==========")
    print(f"Candidates evaluated: {len(ranked_df)}")
    print(f"Results saved to: {output_file}")

    print("\nTOP 10 CANDIDATES:\n")

    print(
        ranked_df[
            ["Rank", "ID", "Category", "final_score"]
        ].head(10).to_string(index=False)
    )

    print("\n=======================================")


if __name__ == "__main__":
    rank_candidates()
