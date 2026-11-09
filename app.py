import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# PROJECT PATHS AND IMPORTS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dynamic_ranking import generate_dynamic_ranking

DATA_FILE = PROJECT_ROOT / "outputs" / "ranked_candidates.csv"
RESUME_DATA_FILE = PROJECT_ROOT / "data" / "resumes_with_skills.csv"

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="HireSense AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
/* ===== HireSense AI | Modern recruitment SaaS theme ===== */
:root {
    --hs-navy: #101C35;
    --hs-blue: #2563EB;
    --hs-blue-light: #EAF2FF;
    --hs-text: #17233C;
    --hs-muted: #64748B;
    --hs-border: #E2EAF5;
    --hs-bg: #F4F7FC;
}

.stApp { background: var(--hs-bg); color: var(--hs-text); }
.block-container { max-width: 1480px; padding-top: 1.6rem; padding-bottom: 3rem; }
[data-testid="stHeader"] { background: rgba(244,247,252,0.88); }

h1, h2, h3 { color: var(--hs-text) !important; font-weight: 750 !important; letter-spacing: -0.45px; }
h1 { letter-spacing: -1px; }
p, label, [data-testid="stMarkdownContainer"] { color: inherit; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101C35 0%, #172B4D 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #F1F5FF; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] small { color: #C7D6ED !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.16); }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 9px 12px;
    margin: 4px 0;
    transition: background .18s ease, border .18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(59,130,246,0.22);
    border-color: rgba(147,197,253,0.45);
}

/* Hero header */
.hero {
    background: radial-gradient(circle at 88% 18%, rgba(96,165,250,.30), transparent 28%),
                linear-gradient(118deg, #101C35 0%, #173D70 58%, #2563EB 100%);
    padding: 30px 34px;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px;
    color: white;
    margin: 0 0 28px 0;
    box-shadow: 0 14px 35px rgba(23, 61, 112, .16);
}
.hero .eyebrow { color: #BBD7FF; font-size: 11px; font-weight: 800; letter-spacing: 2px; margin-bottom: 9px; }
.hero h1 { color: #FFFFFF !important; font-size: clamp(28px, 3vw, 38px); margin: 0 0 7px 0; }
.hero p { color: #DCEAFF !important; font-size: 15px; margin: 0; }

/* Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--hs-border);
    padding: 18px 20px;
    border-radius: 15px;
    box-shadow: 0 5px 18px rgba(30,60,100,.045);
}
[data-testid="stMetricLabel"] { color: var(--hs-muted) !important; font-weight: 650; }
[data-testid="stMetricValue"] { color: #1D5FC7 !important; font-weight: 800; }
[data-testid="stMetricDelta"] { font-weight: 600; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(100deg, #1D5FC7, #3989F5);
    color: #FFFFFF !important;
    border: 0;
    border-radius: 10px;
    padding: .62rem 1.1rem;
    font-weight: 700;
    box-shadow: 0 5px 13px rgba(37,99,235,.15);
    transition: transform .16s ease, box-shadow .16s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(100deg, #174EA6, #2875DC);
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(37,99,235,.22);
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: #FFFFFF;
    border: 1px solid #D7E2F0;
    border-radius: 10px;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div { border-radius: 10px; }
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px dashed #8BB6EC;
    border-radius: 14px;
    padding: 12px;
}

/* Tables, alerts, expanders */
[data-testid="stDataFrame"] { border: 1px solid var(--hs-border); border-radius: 13px; overflow: hidden; }
[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stExpander"] { background: #FFFFFF; border: 1px solid var(--hs-border); border-radius: 12px; }
hr { border-color: var(--hs-border); }

/* Charts and captions */
[data-testid="stPlotlyChart"] { background: #FFFFFF; border: 1px solid var(--hs-border); border-radius: 15px; padding: 8px; }
[data-testid="stCaptionContainer"] { color: var(--hs-muted); }

/* Progress */
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #2563EB, #60A5FA); }

footer { visibility: hidden; }
@media (max-width: 700px) {
    .block-container { padding: 1rem 1rem 2rem 1rem; }
    .hero { padding: 23px 21px; border-radius: 15px; }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-POWERED RECRUITMENT INTELLIGENCE</div>
    <h1>🎯 HireSense AI</h1>
    <p>Intelligent Resume Screening &amp; Candidate Matching Platform</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD EXISTING RANKED DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

@st.cache_data
def load_resume_data():
    return pd.read_csv(RESUME_DATA_FILE, encoding="latin-1")

if not DATA_FILE.exists():
    st.error("Ranked candidates file not found.")
    st.info("Please run: python rank_candidates.py")
    st.stop()

df = load_data()

if df.empty:
    st.warning("No candidate records found.")
    st.stop()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown("""
<div style="padding: 8px 2px 14px 2px;">
    <div style="font-size: 12px; letter-spacing: 1.8px; color: #93C5FD; font-weight: 800;">
        HIRE<span style="color:#FFFFFF;">SENSE</span> AI
    </div>
    <div style="font-size: 12px; color: #C7D6ED; margin-top: 5px;">
        Recruitment Intelligence Workspace
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Dynamic Job Matcher",
        "Candidate Explorer",
        "Candidate Comparison",
        "Skill Analysis",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Powered by Python | NLP | Scikit-learn")

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.header("📊 Recruitment Dashboard")

    total_candidates = len(df)
    average_score = df["final_score"].mean()
    highest_score = df["final_score"].max()
    top_candidate = df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Candidates", f"{total_candidates:,}")
    col2.metric("Average Match", f"{average_score:.2f}%")
    col3.metric("Highest Match", f"{highest_score:.2f}%")
    col4.metric("Top Candidate", str(top_candidate["ID"]))

    st.divider()
    st.subheader("🏆 Top 10 Candidates")

    top10 = df.head(10)

    st.dataframe(
        top10[
            [
                "Rank", "ID", "Category", "final_score",
                "skill_score", "text_similarity"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📈 Candidate Matching Scores")

    fig = px.bar(
        top10,
        x="ID",
        y="final_score",
        color="final_score",
        hover_data=["Category"],
        title="Top 10 Candidates by Matching Score",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📂 Candidate Category Distribution")

    category_counts = df["Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Candidates"]

    fig2 = px.pie(
        category_counts,
        names="Category",
        values="Candidates",
        hole=0.45,
        title="Candidates by Resume Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.download_button(
        "⬇️ Download All Ranked Candidates",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="HireSense_Ranked_Candidates.csv",
        mime="text/csv",
        use_container_width=True
    )

# =====================================================
# DYNAMIC JOB MATCHER
# =====================================================

elif page == "Dynamic Job Matcher":

    st.header("⚡ Dynamic Job Description Matcher")

    st.write(
        "Enter a job description or upload a text file. "
        "HireSense AI will compare it with the resume dataset "
        "and generate a fresh candidate ranking."
    )

    st.info(
        "This page uses the existing skill-matching and TF-IDF "
        "similarity approach. It does not train a new model for each job."
    )

    with st.expander("📊 How Candidate Scoring Works", expanded=False):
        st.markdown("### 1. Skill Score")
        st.write(
            "The skill score evaluates how closely a candidate's extracted "
            "skills match the required and preferred skills in the job description."
        )
        st.latex(
            r"Skill\ Score = 0.8(Required\ Score) "
            r"+ 0.2(Preferred\ Score)"
        )

        st.markdown("### 2. Final Matching Score")
        st.write(
            "The final score combines the skill score with text similarity "
            "between the resume and the job description."
        )
        st.latex(
            r"Final\ Score = 0.7(Skill\ Score) "
            r"+ 0.3(Text\ Similarity)"
        )

        st.markdown("### 3. Score Breakdown")
        st.write(
            "- **80% of the skill score:** Required skill matching\n"
            "- **20% of the skill score:** Preferred skill matching\n"
            "- **70% of the final score:** Skill score contribution\n"
            "- **30% of the final score:** Resume/JD text similarity"
        )
        st.info(
            "The matching score is an AI-based decision-support indicator. "
            "It does not prove a candidate's actual ability or guarantee "
            "suitability. Human review is essential."
        )

    uploaded_file = st.file_uploader(
        "Upload Job Description (.txt)",
        type=["txt"],
        help="Upload a plain-text job description."
    )

    uploaded_text = ""
    if uploaded_file is not None:
        try:
            uploaded_text = uploaded_file.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            uploaded_text = uploaded_file.getvalue().decode(
                "latin-1", errors="replace"
            )

    default_jd = uploaded_text or """Job Title: Python Developer

Required skills:
Python, SQL, Django, Flask, Git.

Preferred skills:
AWS, Docker, REST API.

Candidates should have knowledge of software development,
debugging, and problem solving."""

    job_description = st.text_area(
        "Job Description",
        value=default_jd,
        height=240,
        help="You can edit the uploaded text or enter a job description manually."
    )

    run_matching = st.button(
        "🚀 Analyze & Rank Candidates",
        type="primary",
        use_container_width=True
    )

    if run_matching:

        if not job_description.strip():
            st.warning("Please enter a job description first.")
        elif not RESUME_DATA_FILE.exists():
            st.error(
                "Resume dataset with extracted skills was not found. "
                "Please check data/resumes_with_skills.csv."
            )
        else:
            try:
                with st.spinner(
                    "Analyzing resumes and calculating candidate scores..."
                ):
                    resumes_df = load_resume_data()
                    dynamic_results = generate_dynamic_ranking(
                        resumes_df,
                        job_description
                    )
                    st.session_state["dynamic_results"] = dynamic_results
                    st.session_state["dynamic_jd"] = job_description

                st.success(
                    f"Analysis complete! Evaluated "
                    f"{len(dynamic_results):,} candidates."
                )

            except Exception as error:
                st.error(f"Ranking failed: {error}")

    # Keep the most recent dynamic results visible across Streamlit reruns.
    if "dynamic_results" in st.session_state:

        dynamic_df = st.session_state["dynamic_results"]

        st.divider()
        st.subheader("🏆 Dynamic Candidate Ranking")

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric("Candidates Evaluated", f"{len(dynamic_df):,}")
        metric2.metric(
            "Highest Match",
            f"{dynamic_df['final_score'].max():.2f}%"
        )
        metric3.metric(
            "Average Match",
            f"{dynamic_df['final_score'].mean():.2f}%"
        )

        st.caption(
            "The ranking below corresponds to the most recently analyzed "
            "job description."
        )

        st.subheader("Top 10 Matching Candidates")

        st.dataframe(
            dynamic_df[
                ["Rank", "ID", "Category", "final_score",
                 "skill_score", "text_similarity"]
            ].head(10),
            use_container_width=True,
            hide_index=True
        )

        chart_df = dynamic_df.head(10).copy()
        chart_df["ID"] = chart_df["ID"].astype(str)

        ranking_chart = px.bar(
            chart_df,
            x="ID",
            y="final_score",
            color="final_score",
            hover_data=["Category", "skill_score", "text_similarity"],
            title="Top 10 Candidates for This Job Description",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(ranking_chart, use_container_width=True)

        st.divider()
        st.subheader("🔎 Inspect a Dynamically Ranked Candidate")

        selected_id = st.selectbox(
            "Select Candidate ID",
            dynamic_df["ID"].tolist(),
            key="dynamic_candidate_id"
        )

        selected_candidate = dynamic_df[
            dynamic_df["ID"] == selected_id
        ].iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Final Match Score", f"{selected_candidate['final_score']:.2f}%")
        c2.metric("Required Skill Match", f"{selected_candidate['required_score']:.2f}%")
        c3.metric("Preferred Skill Match", f"{selected_candidate['preferred_score']:.2f}%")

        left, right = st.columns(2)

        with left:
            st.markdown("**✅ Matched Required Skills**")
            if str(selected_candidate["matched_required"]).strip():
                st.success(selected_candidate["matched_required"])
            else:
                st.info("No required skills matched.")

            st.markdown("**⭐ Matched Preferred Skills**")
            if str(selected_candidate["matched_preferred"]).strip():
                st.success(selected_candidate["matched_preferred"])
            else:
                st.info("No preferred skills matched.")

        with right:
            st.markdown("**❌ Missing Required Skills**")
            if str(selected_candidate["missing_required"]).strip():
                st.warning(selected_candidate["missing_required"])
            else:
                st.success("No required skills are missing.")

            st.markdown("**📌 Missing Preferred Skills**")
            if str(selected_candidate["missing_preferred"]).strip():
                st.info(selected_candidate["missing_preferred"])
            else:
                st.success("No preferred skills are missing.")

        st.download_button(
            "⬇️ Download Dynamic Ranking CSV",
            data=dynamic_df.to_csv(index=False).encode("utf-8"),
            file_name="HireSense_Dynamic_Ranking.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.caption(
            "Decision-support notice: matching scores measure similarity "
            "to the supplied job description. They do not prove candidate "
            "ability or predict job performance. Human review is essential."
        )

# =====================================================
# CANDIDATE EXPLORER
# =====================================================

elif page == "Candidate Explorer":

    st.header("🔍 Candidate Explorer")

    candidate_id = st.selectbox(
        "Search / Select Candidate ID",
        df["ID"].tolist()
    )

    candidate = df[df["ID"] == candidate_id].iloc[0]

    st.divider()
    st.subheader(f"Candidate Profile: {candidate_id}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Final Match Score", f"{candidate['final_score']:.2f}%")
    col2.metric("Skill Match", f"{candidate['skill_score']:.2f}%")
    col3.metric("Text Similarity", f"{candidate['text_similarity']:.2f}%")

    st.write("**Resume Category:**", candidate["Category"])

    st.progress(min(max(float(candidate["final_score"]) / 100, 0), 1))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Required Skills")
        matched_required = str(candidate["matched_required"])

        if matched_required.strip():
            st.success(matched_required)
        else:
            st.info("No required skills matched.")

    with col2:
        st.subheader("❌ Missing Required Skills")
        missing_required = str(candidate["missing_required"])

        if missing_required.strip():
            st.warning(missing_required)
        else:
            st.success("No required skills are missing.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⭐ Matched Preferred Skills")
        matched_preferred = str(candidate["matched_preferred"])

        if matched_preferred.strip():
            st.success(matched_preferred)
        else:
            st.info("No preferred skills matched.")

    with col2:
        st.subheader("📌 Missing Preferred Skills")
        missing_preferred = str(candidate["missing_preferred"])

        if missing_preferred.strip():
            st.info(missing_preferred)
        else:
            st.success("All preferred skills matched.")

    st.divider()
    st.subheader("📄 Download Candidate Report")

    report = f"""
HIRE SENSE AI
CANDIDATE MATCH REPORT
====================================

Candidate ID: {candidate['ID']}
Resume Category: {candidate['Category']}

FINAL MATCH SCORE: {candidate['final_score']:.2f}%

------------------------------------
MATCHING BREAKDOWN

Text Similarity: {candidate['text_similarity']:.2f}%
Skill Match: {candidate['skill_score']:.2f}%
Required Skill Match: {candidate['required_score']:.2f}%
Preferred Skill Match: {candidate['preferred_score']:.2f}%

------------------------------------
MATCHED REQUIRED SKILLS

{candidate['matched_required']}

MISSING REQUIRED SKILLS

{candidate['missing_required']}

------------------------------------
MATCHED PREFERRED SKILLS

{candidate['matched_preferred']}

MISSING PREFERRED SKILLS

{candidate['missing_preferred']}

====================================
Generated by HireSense AI

Note: Scores represent similarity to the
provided job description, not validated
measures of candidate ability.
"""

    st.download_button(
        label="⬇️ Download Candidate Report",
        data=report,
        file_name=f"Candidate_{candidate['ID']}_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

# =====================================================
# CANDIDATE COMPARISON
# =====================================================

elif page == "Candidate Comparison":

    st.header("⚖️ Candidate Comparison")

    st.write(
        "Compare two candidates based on their "
        "job-description matching scores and skills."
    )

    candidate_ids = df["ID"].tolist()

    col1, col2 = st.columns(2)

    with col1:
        id1 = st.selectbox(
            "Select First Candidate",
            candidate_ids,
            key="compare_candidate_1"
        )

    with col2:
        id2 = st.selectbox(
            "Select Second Candidate",
            candidate_ids,
            index=1 if len(candidate_ids) > 1 else 0,
            key="compare_candidate_2"
        )

    if id1 == id2:
        st.warning("Please select two different candidates.")

    else:
        c1 = df[df["ID"] == id1].iloc[0]
        c2 = df[df["ID"] == id2].iloc[0]

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"👤 Candidate {id1}")
            st.metric("Final Match Score", f"{c1['final_score']:.2f}%")
            st.caption(f"Category: {c1['Category']}")

        with col2:
            st.subheader(f"👤 Candidate {id2}")
            st.metric("Final Match Score", f"{c2['final_score']:.2f}%")
            st.caption(f"Category: {c2['Category']}")

        comparison = pd.DataFrame({
            "Metric": [
                "Final Match Score",
                "Skill Match",
                "Text Similarity",
                "Required Skill Match",
                "Preferred Skill Match"
            ],
            f"Candidate {id1}": [
                c1["final_score"],
                c1["skill_score"],
                c1["text_similarity"],
                c1["required_score"],
                c1["preferred_score"]
            ],
            f"Candidate {id2}": [
                c2["final_score"],
                c2["skill_score"],
                c2["text_similarity"],
                c2["required_score"],
                c2["preferred_score"]
            ]
        })

        st.subheader("📊 Detailed Score Comparison")
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        chart_data = pd.DataFrame({
            "Candidate": [str(id1), str(id2)],
            "Final Score": [c1["final_score"], c2["final_score"]]
        })

        fig = px.bar(
            chart_data,
            x="Candidate",
            y="Final Score",
            color="Candidate",
            title="Candidate Matching Score Comparison",
            range_y=[0, 100],
            text="Final Score"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("🧠 Skill Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### Candidate {id1}")
            st.write("**Matched Required Skills**")
            st.success(c1["matched_required"] or "None")
            st.write("**Missing Required Skills**")
            st.warning(c1["missing_required"] or "None")
            st.write("**Matched Preferred Skills**")
            st.info(c1["matched_preferred"] or "None")

        with col2:
            st.markdown(f"### Candidate {id2}")
            st.write("**Matched Required Skills**")
            st.success(c2["matched_required"] or "None")
            st.write("**Missing Required Skills**")
            st.warning(c2["missing_required"] or "None")
            st.write("**Matched Preferred Skills**")
            st.info(c2["matched_preferred"] or "None")

        st.divider()

        st.download_button(
            "⬇️ Download Comparison Report",
            data=comparison.to_csv(index=False),
            file_name="HireSense_Candidate_Comparison.csv",
            mime="text/csv",
            use_container_width=True
        )

# =====================================================
# SKILL ANALYSIS
# =====================================================

elif page == "Skill Analysis":

    st.header("🧠 Candidate Skill Analysis")

    required_scores = df["required_score"].mean()
    preferred_scores = df["preferred_score"].mean()

    col1, col2 = st.columns(2)

    col1.metric("Average Required Skill Match", f"{required_scores:.2f}%")
    col2.metric("Average Preferred Skill Match", f"{preferred_scores:.2f}%")

    st.divider()

    skill_comparison = pd.DataFrame({
        "Skill Type": ["Required Skills", "Preferred Skills"],
        "Average Match": [required_scores, preferred_scores]
    })

    fig = px.bar(
        skill_comparison,
        x="Skill Type",
        y="Average Match",
        color="Skill Type",
        range_y=[0, 100],
        title="Average Skill Coverage"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Candidate Score Distribution")

    fig2 = px.histogram(
        df,
        x="final_score",
        nbins=20,
        title="Distribution of Candidate Matching Scores"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📊 Required Skill Match Distribution")

    fig3 = px.histogram(
        df,
        x="required_score",
        nbins=20,
        title="Required Skill Coverage Across Candidates"
    )
    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# ABOUT PROJECT
# =====================================================

elif page == "About Project":

    st.header("ℹ️ About HireSense AI")

    st.markdown("""
    ## 🎯 HireSense AI

    **Intelligent Resume Screening and Candidate Matching System**

    HireSense AI is a Python-based prototype that helps
    analyze resumes and compare candidate information
    against a given job description.

    ### 🚀 Key Features

    - Resume text preprocessing
    - NLP-based skill extraction
    - TF-IDF text similarity
    - Required and preferred skill matching
    - Weighted candidate scoring
    - Automatic candidate ranking
    - Dynamic job-description matching
    - Candidate comparison
    - Individual candidate reports
    - Interactive analytics dashboard

    ### 🛠️ Technologies Used

    - Python
    - Pandas
    - NumPy
    - Scikit-learn
    - NLP and Regular Expressions
    - Streamlit
    - Plotly

    ### 📊 Scoring Method

    - 70% Skill Matching
    - 30% Text Similarity

    ### ⚠️ Important Note

    This is a prototype decision-support tool.
    Matching scores indicate similarity to the supplied
    job description. They are not validated measures
    of candidate ability or future job performance.
    Human review is essential.
    """)

    st.divider()

    st.caption(
        "HireSense AI | Resume Screening & Candidate Matching"
    )
                  