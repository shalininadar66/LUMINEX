# LUMINEX: Intelligent Career Navigator

LUMINEX is a career transition engine that uses data-driven "Skill Vectors" to bridge the gap between your current profile and your dream role.

---

##  Technical Architecture

Our model is designed for high-speed processing and precision:

* **Stack**: Built with Python, using **Streamlit** for the frontend and **SQLite3** for data persistence.
* **NLP Layer**: Employs **Spacy/NLTK** for Named Entity Recognition (NER) to extract skills from resumes.
* **The Model**: Measures skill gaps using **Cosine Similarity**, comparing user skill vectors against industry benchmarks.
* **Validation**: Uses **Scikit-learn** for classification and cross-references self-assessments with technical MCQ scores to eliminate bias.

---

##  Key Features

* **ATS Analysis**: Provides an instant resume score and keyword optimization advice.
* **Dual Assessment**: Combines subjective self-rating sliders with objective technical MCQs.
* **Personalized Roadmaps**: Dynamically generates a PDF guide targeting your specific skill gaps.

---

##  Setup

1. **Install**: `pip install streamlit PyPDF2 numpy reportlab spacy`.
3. **Launch**: `streamlit run luminex.py`.
