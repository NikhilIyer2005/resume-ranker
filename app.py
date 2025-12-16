from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import PyPDF2
import joblib

vectorizer = joblib.load("vectorizer.joblib")

st.set_page_config(page_title="Resume Ranker", page_icon="📄", layout="wide")
st.markdown(
    """
    <style>
    .score-card {
        padding: 1rem 1.2rem;
        border-radius: 0.8rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;

        background: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.25);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .score-title{
        font-weight: 600;
        font-size: 1.05rem;
    }
    .score-meta {
        font-size: 0.9rem;
        color: #666666;
        margin-bottom: 0.4rem
    }
    .pill {
        display: inline-block;
        padding: 0.12rem 0.55rem;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-right: 0.3rem;
        margin-bottom: 0.2rem;
        background-color: #f1f3f4;
        color: #333333;
    }
    .pill-missing {
        background-color: #e6f4ea;
        color: #137333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

SKILL_KEYWORDS = [
    # Languages
    "python", "java", "c++", "javascript", "typescript", "c#", "go", "rust",
    # Backend / APIs / frameworks
    "rest", "rest apis", "graphql", "django", "flask", "spring boot",
    "node.js", "express.js", "fastapi",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis",
    # Cloud / devops
    "aws", "azure", "gcp", "docker", "kubernetes", "linux",
    # Data / ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "data analysis",
    # General SWE / process
    "system design", "unit testing", "integration testing",
    "continuous integration", "continuous deployment",
    "git", "agile", "scrum",
]

def extract_skills(text: str) -> set[str]:
    """
    Very simple keyword-based skill extractor:
    returns all skills from SKILL_KEYWORDS that appear in the text.
    """
    text_lower = text.lower()
    found = set()

    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.add(skill)
    return found

def main():
    st.title("📄Resume Ranker")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        jd_text = st.text_area("Paste job description here:", height=260, placeholder="Paste the job description or roleposting here...")
    
    with col_right:
        uploaded_files = st.file_uploader("Upload one or more resumes (.txt or .pdf)", type=["txt", "pdf"], accept_multiple_files=True)

        if uploaded_files:
            st.write("**Uploaded Files:**")
            for f in uploaded_files:
                st.write(f"- {f.name}")
    st.markdown("---")

    # Button to trigger ranking
    run_ranking = st.button("Rank Resumes")


    results = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            filename = uploaded_file.name.lower()

            if filename.endswith(".txt"):
                file_bytes = uploaded_file.read()
                file_text = file_bytes.decode("utf-8", errors="ignore")
            elif filename.endswith(".pdf"):
                reader = PyPDF2.PdfReader(uploaded_file)
                text_chunks = []
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    text_chunks.append(page_text)
                file_text = "\n".join(text_chunks)
            else:
                st.error("Unsupported file type. Please upload a .txt or .pdf file.")
                continue
            if not file_text.strip():
                st.warning("Could not extract any text from this file.")
                continue
                
            results.append({"filename" : filename, "text" : file_text})
    
    if run_ranking:
        if not jd_text.strip():
            st.warning("Please paste a job description first.")
            return
        
        if not results:
            st.warning("Please upload at least one resume with readable text.")
            return
        
        # TF-IDF vector for job description
        jd_vec = vectorizer.transform([jd_text])
        jd_skills = extract_skills(jd_text)
        scored = []

        for item in results:
            # Text similarity
            res_vec = vectorizer.transform([item["text"]])
            score = cosine_similarity(jd_vec, res_vec)[0][0]

            # Keyword-based skills
            resume_skills = extract_skills(item["text"])
            overlap = resume_skills & jd_skills
            skills_score = (len(overlap)/len(jd_skills) if jd_skills else 0.0)

            # Final weighted score
            final_score = 0.6 * score + 0.4 * skills_score
            scored.append({"filename" : item["filename"], "score" : score, "skills_score" : skills_score, 
                           "final_score" : final_score, "jd_skills" : jd_skills, 
                           "resume_skills" : resume_skills, "overlap" : overlap})

        # Sort by final score, highest first    
        scored.sort(key=lambda x: (x["final_score"]), reverse=True)

        # ---------- Display results ----------
        st.subheader("📊Ranking vs Job Description")

        if scored:
            best = scored[0]
            st.info(
                f"Top match: **{best['filename']}** "
                f"(Final Score: {best['final_score']:.3f}, "
                f"Text Match: {best['score']:.3f}, "
                f"Skills Match: {best['skills_score']*100:.1f}%)"
                )
            
        for i, item in enumerate(scored, start=1):
            jd_skills = item["jd_skills"]
            resume_skills = item["resume_skills"]
            overlap = item["overlap"]

            matched_skills = sorted(overlap)
            missing_skills = sorted(jd_skills - resume_skills) if jd_skills else []

            col_rank, col_card = st.columns([0.12, 0.88])

            with col_rank:
                st.markdown(f"### #{i}")
            
            with col_card:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="score-title">{item['filename']}</div>
                    <div class="score-meta">
                        Final Score: <b>{item['final_score']:.3f}</b> &nbsp;•&nbsp;
                        Text Match: <b>{item['score']:.3f}</b> &nbsp;•&nbsp;
                        Skills Match: <b>{item['skills_score']*100:.1f}%</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                c1, c2 = st.columns(2)

                # Matched skills
                with c1:
                    st.markdown("**Matched Skills**")
                    if matched_skills:
                        pills = " ".join(
                            f'<span class="pill pill-matched">{s}</span>'
                            for s in matched_skills
                        )
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.write("_None_")
                
                # Missing skills
                with c2:
                    st.markdown("**Missing Skills**")
                    if jd_skills:
                        if missing_skills:
                            pills = " ".join(
                                f'<span class="pill pill-missing">{s}</span>'
                                for s in missing_skills
                            )
                            st.markdown(pills, unsafe_allow_html=True)
                        else:
                            st.write("_None_")
                    else:
                        st.write("_No skills detected in job description_")
                st.markdown("</div>", unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()