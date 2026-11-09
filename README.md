# HireSense AI – Intelligent Resume Screening & Candidate Matching System

An AI-powered resume screening and candidate matching platform that helps recruiters evaluate, rank, and compare candidates based on job requirements.

## Project Overview

HireSense AI automates important parts of the initial resume screening process. It analyzes candidate resumes against a given job description, extracts relevant skills, calculates matching scores, and dynamically ranks candidates.

The platform provides an interactive dashboard to explore candidate profiles, compare applicants, and understand skill matches.

## Key Features

- **Automated Resume Screening:** Processes and analyzes multiple resumes.
- **Skill Extraction:** Identifies relevant skills from candidate resumes.
- **Job Description Matching:** Compares candidate profiles with job requirements.
- **Dynamic Candidate Ranking:** Ranks candidates based on matching scores.
- **Candidate Explorer:** Displays individual candidate information and extracted skills.
- **Candidate Comparison:** Compares two candidates side by side.
- **Skill Analysis:** Visualizes required and preferred skill distributions.
- **Interactive Dashboard:** Presents ranking results and useful visualizations.
- **CSV Export:** Allows users to download ranking results.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF and text similarity |
| Streamlit | Interactive web application |
| Plotly | Data visualization |
| Regular Expressions | Skill extraction and text processing |

## Matching Methodology

The system calculates candidate scores using two main components:

**1. Skill Matching Score**

- Required skills: 80%
- Preferred skills: 20%

**2. Final Matching Score**

- Skill matching score: 70%
- TF-IDF text similarity: 30%

Final Score = (0.70 × Skill Score) + (0.30 × Text Similarity Score)

These scores are similarity indicators for decision support, not proof of candidate competence.

## Project Structure

```text
FUTURE_ML_TASK3/
│
├── app.py
├── train.py
├── inspect_dataset.py
├── preprocess_dataset.py
├── extract_skills_dataset.py
├── job_description.py
├── rank_candidates.py
│
├── data/
│   ├── Resume.csv
│   ├── cleaned_resumes.csv
│   ├── resumes_with_skills.csv
│   └── job_description.txt
│
├── src/
│   ├── preprocessing.py
│   ├── skill_extractor.py
│   ├── matching_engine.py
│   └── dynamic_ranking.py
│
├── models/
├── outputs/
│   ├── ranked_candidates.csv
│   └── dynamic_ranked_candidates.csv
│
├── assets/
├── requirements.txt
└── README.md
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/srushtisdurgekar30-oss/HireSense-AI.git
```

**2. Navigate to the project folder**

```bash
cd HireSense-AI
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the environment**

Windows:

```bash
.venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Run the application**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Application Modules

1. Dashboard – Overall candidate statistics and top-ranked candidates.
2. Dynamic Job Matcher – Matches candidates against a job description.
3. Candidate Explorer – Examines individual candidate profiles.
4. Candidate Comparison – Compares candidate matching results.
5. Skill Analysis – Analyzes skill distribution and matching scores.
6. About Project – Displays project information and methodology.

## Results

The system successfully evaluated 2,483 candidates and generated ranked candidate outputs.

Generated results:

- `outputs/ranked_candidates.csv`
- `outputs/dynamic_ranked_candidates.csv`

## Limitations and Responsible Use

- Matching scores do not guarantee candidate suitability.
- Skill extraction depends on the quality and wording of resume data.
- TF-IDF measures textual similarity rather than actual professional ability.
- Recruiters should review original resumes and make final decisions.
- The system should be used as a decision-support tool, not as an automated hiring decision-maker.
- Only datasets that are permitted for sharing should be published.

## Future Enhancements

- Integration with advanced NLP and transformer-based models.
- Improved semantic skill extraction.
- PDF and DOCX resume upload support.
- Explainable AI for candidate ranking.
- Secure recruiter authentication and data management.

## Author

**Srushti S. Durgekar**

B.Tech – Robotics and AI Engineering

## Project Repository

[HireSense AI – GitHub](https://github.com/srushtisdurgekar30-oss/HireSense-AI)
