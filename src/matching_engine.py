
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate textual similarity between a resume and job description.
    """
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(float(score) * 100, 2)
    except ValueError:
        return 0.0


def calculate_skill_match(candidate_skills, required_skills, preferred_skills):
    """
    Calculate required and preferred skill coverage.
    """
    candidate_skills = set(candidate_skills)
    required_skills = set(required_skills)
    preferred_skills = set(preferred_skills)

    matched_required = candidate_skills & required_skills
    matched_preferred = candidate_skills & preferred_skills

    missing_required = required_skills - candidate_skills
    missing_preferred = preferred_skills - candidate_skills

    if required_skills:
        required_score = (
            len(matched_required) / len(required_skills)
        ) * 100
    else:
        required_score = 100.0

    if preferred_skills:
        preferred_score = (
            len(matched_preferred) / len(preferred_skills)
        ) * 100
    else:
        preferred_score = 100.0

    # Required skills have greater weight than preferred skills.
    final_skill_score = (
        required_score * 0.8 +
        preferred_score * 0.2
    )

    return {
        "skill_score": round(final_skill_score, 2),
        "required_score": round(required_score, 2),
        "preferred_score": round(preferred_score, 2),
        "matched_required": sorted(matched_required),
        "matched_preferred": sorted(matched_preferred),
        "missing_required": sorted(missing_required),
        "missing_preferred": sorted(missing_preferred)
    }


def calculate_final_score(resume_text, job_description,
                          candidate_skills, required_skills,
                          preferred_skills):
    """
    Combine text similarity and skill match into a final score.
    """
    text_score = calculate_similarity(
        resume_text, job_description
    )

    skill_result = calculate_skill_match(
        candidate_skills,
        required_skills,
        preferred_skills
    )

    final_score = (
        text_score * 0.3 +
        skill_result["skill_score"] * 0.7
    )

    return {
        "final_score": round(final_score, 2),
        "text_similarity": text_score,
        **skill_result
    }


if __name__ == "__main__":
    sample_resume = """
    Python SQL Machine Learning Deep Learning
    TensorFlow Scikit-learn Natural Language Processing
    Data Analysis Computer Vision
    """

    sample_jd = """
    Python SQL Machine Learning Deep Learning
    TensorFlow Scikit-learn Natural Language Processing
    Computer Vision OpenCV Data Analysis PyTorch
    """

    candidate_skills = [
        "Python", "SQL", "Machine Learning",
        "Deep Learning", "TensorFlow",
        "Scikit-learn", "Natural Language Processing",
        "Data Analysis", "Computer Vision"
    ]

    required = [
        "Python", "SQL", "Machine Learning",
        "Deep Learning", "TensorFlow",
        "Scikit-learn", "Natural Language Processing"
    ]

    preferred = [
        "Computer Vision", "OpenCV",
        "Data Analysis", "PyTorch"
    ]

    result = calculate_final_score(
        sample_resume,
        sample_jd,
        candidate_skills,
        required,
        preferred
    )

    print("\n--- RESUME MATCHING RESULT ---")
    for key, value in result.items():
        print(f"{key}: {value}")
