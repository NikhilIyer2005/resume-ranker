# 📊 Resume Ranker — AI-Powered Job Match Scoring

An intelligent Streamlit app that compares multiple resumes against any job description using:

- Cosine text similarity (semantic text matching)
- Keyword-based skill extraction
- Weighted scoring (text relevance + skills relevance)
- Interactive Streamlit interface

Upload one or more resumes (.txt or .pdf), paste a job description, and instantly see:

✔ Ranked candidates
✔ Matched & missing skills
✔ Final score breakdown
✔ Beautiful, clean UI

Ideal for hiring managers, recruiters, or job seekers optimizing resumes.

----------------------------------------------------------------------------------------------------

## ✨ Features

### 🔍 1. Resume Ranking
Ranks each resume based on:
- Text similarity to the job description (TF-IDF + Cosine Similarity)
- Skills Match Score
- Final Weighted Score

### 🧠 2. Skill Extraction & Insights
For each resume:
- Matched Skills (blue tags)
- Missing Skills (green tags)
- Skills match percentage

### 🎨 3. Clean Modern UI
Built with Streamlit:
- Two-column layout  
- Job description on left  
- File uploader on right  
- Highlighted “Top match” banner  
- Tag-style skill visuals 

### 📄 4. PDF + TXT Resume Support
Reads resumes in:
- .txt
- .pdf (via PyPDF2)

---------------------------------------------------------------------------

## 🛠️ Tech Stack
1.      UI         ->  Streamlit
2. Text Processing ->  Scikit-learn (TF-IDF, Cosine Similarity)
3. File Handling   ->  PyPDF2
4.      Data       ->  Python
5.   Deployment    ->  Streamlit Cloud / GitHub

---------------------------------------------------------------------------

## 📂 Project Structure
    resume-ranker/
    │
    ├── app.py               # Main Streamlit application
    ├── README.md            # Project documentation
    ├── requirements.txt     # Python dependencies
    ├── sample_resume.txt    # Example resume file
    └── MIT LICENSE          # Open-source license
---------------------------------------------------------------------------

## 📦 Installation
1.  Clone the repository
    git clone https://github.com/NikhilIyer2005/resume-ranker.git
    
    cd resume-ranker
2.  Install Dependencies
    pip install -r requirements.txt
3.  Run the Application
    streamlit run app.py

---------------------------------------------------------------------------

## 🧪 Usage
1. Paste a job description in the left text area
2. Upload one or more resumes (.pdf or .txt)
3. Click Rank Resumes
4. View:
    - Final score
    - Text match
    - Skills match
    - Matched & missing skills
    - Ranking order (if multiple resumes are uploaded)

---------------------------------------------------------------------------

## 📊 Scoring Formula
final_score = 0.6 * score + 0.4 * skills_score

Weights are adjustable in the code.

---------------------------------------------------------------------------

## 🔧 Customization
✏️ Edit skills in app.py:

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

➕ You can extend the skill list for roles such as:
    - Data Science
    - Cybersecurity
    - Product Management
    - Marketing
    - Finance
    - And more...

---------------------------------------------------------------------------

## 🛣️ Roadmap / Future Enhancements
- Auto-skill extraction using LLMs or embeddings
- Improve UI with animations & templates
- Add resume rewriting suggestions
- Add job-specific skill auto-extraction
- Compare candidates head-to-head
- Export ranking as PDF

---------------------------------------------------------------------------

## 🧑‍💻 Author
Nikhil Iyer

## 📄 License  
This project is licensed under the MIT License.