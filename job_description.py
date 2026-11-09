
import re

from src.skill_extractor import extract_skills


# Words that indicate preferred or optional skills
PREFERRED_KEYWORDS = [
    "preferred",
    "preferably",
    "nice to have",
    "good to have",
    "bonus",
    "desirable",
    "plus",
    "optional",
    "an added advantage"
]


def process_job_description(job_description):
    """
    Extract and classify skills from a job description.

    Skills in sentences containing preferred indicators
    are classified as preferred.
    Other recognized skills are classified as required.
    """

    if not isinstance(job_description, str):
        raise ValueError("Job description must be text.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    # Split description into sentences
    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        job_description
    )

    required_skills = set()
    preferred_skills = set()

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # Extract skills from the sentence
        skills = extract_skills(sentence)

        # Check whether sentence indicates preferred skills
        is_preferred = any(
            keyword in sentence.lower()
            for keyword in PREFERRED_KEYWORDS
        )

        if is_preferred:
            preferred_skills.update(skills)
        else:
            required_skills.update(skills)

    # A skill mentioned as required takes priority
    preferred_skills -= required_skills

    return {
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
        "total_skills": len(required_skills | preferred_skills)
    }


if __name__ == "__main__":

    sample_jd = """
    We are looking for a Machine Learning Engineer.

    Required skills include Python, SQL, TensorFlow,
    Scikit-learn, Deep Learning and NLP.

    Experience with Data Analysis and Computer Vision
    is preferred.
    """

    result = process_job_description(sample_jd)

    print("=" * 50)
    print("HIRESENSE AI - JOB DESCRIPTION ANALYSIS")
    print("=" * 50)

    print("\nREQUIRED SKILLS:")

    for skill in result["required_skills"]:
        print("-", skill)

    print("\nPREFERRED SKILLS:")

    for skill in result["preferred_skills"]:
        print("-", skill)

    print("\nTOTAL IDENTIFIED SKILLS:")
    print(result["total_skills"])

    print("\nJOB DESCRIPTION ANALYSIS COMPLETED!")

