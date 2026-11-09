
import re


# Technical skill dictionary
# Each skill has a canonical name and possible variations.

SKILL_DICTIONARY = {
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++"],
    "C#": ["c#"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "SQL": ["sql", "structured query language"],
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Django": ["django"],
    "Flask": ["flask"],
    "PHP": ["php"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Natural Language Processing": [
        "natural language processing",
        "nlp"
    ],
    "Computer Vision": ["computer vision"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Keras": ["keras"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "OpenCV": ["opencv"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Science": ["data science"],
    "Data Visualization": ["data visualization"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Statistics": ["statistics", "statistical analysis"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql"],
    "MongoDB": ["mongodb"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "Google Cloud": ["google cloud", "gcp"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "REST API": ["rest api", "restful api"],
    "Computer Networks": ["computer networks"],
    "Cybersecurity": ["cybersecurity", "cyber security"],
    "Arduino": ["arduino"],
    "ROS": ["ros", "robot operating system"],
}


def contains_skill(text, skill_variations):
    """
    Check whether any variation of a skill
    exists as a separate term in the text.
    """

    for variation in skill_variations:

        pattern = (
            r"(?<!\w)"
            + re.escape(variation)
            + r"(?!\w)"
        )

        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


def extract_skills(resume_text):
    """
    Extract recognized technical skills
    from a cleaned resume.
    """

    if not isinstance(resume_text, str):
        return []

    extracted = []

    for skill, variations in SKILL_DICTIONARY.items():

        if contains_skill(resume_text, variations):
            extracted.append(skill)

    return extracted


if __name__ == "__main__":

    sample_resume = """
    Experienced Python developer with knowledge of
    machine learning, SQL, TensorFlow, PyTorch,
    Pandas, NumPy and Computer Vision.
    """

    skills = extract_skills(sample_resume)

    print("HIRESENSE AI - SKILL EXTRACTION TEST")
    print("------------------------------------")

    print("\nSample resume:")
    print(sample_resume)

    print("\nExtracted skills:")

    for skill in skills:
        print("-", skill)

    print("\nTotal skills identified:", len(skills))
