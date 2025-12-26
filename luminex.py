import streamlit as st
import PyPDF2, io, sqlite3
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from datetime import datetime




st.set_page_config(page_title="LUMINEX", layout="wide")




conn = sqlite3.connect("signals.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    skill_vector TEXT,
    mcq_score INTEGER,
    roadmap_downloaded INTEGER,
    timestamp TEXT
)
""")
conn.commit()

def get_role_insights(role):
    cur.execute("SELECT skill_vector FROM signals WHERE role=?", (role,))
    rows = cur.fetchall()
    if len(rows) < 3: return None
    vectors = np.array([eval(r[0]) for r in rows])
    return np.mean(vectors, axis=0)




if "page" not in st.session_state: st.session_state.page = "home"
if "selected_role" not in st.session_state: st.session_state.selected_role = None



st.markdown(f"""
<style>
    :root {{
        --bg-dark: #213448;
        --accent-blue: #547792;
        --light-blue: #94B4C1;
        --cream: #EAEOCF;
    }}
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: var(--bg-dark);
        color: var(--cream);
    }}
    .logo-text {{ font-size: 4rem !important; font-weight: 900; color: var(--light-blue) !important; margin: 0; padding-top: 0; }}
    
    div.stButton > button {{ border-radius: 10px; border: 1px solid var(--light-blue); background-color: var(--accent-blue); color: var(--cream) !important; transition: 0.3s; }}
    
    [data-testid="column"] div.stButton > button {{ 
        height: 350px; 
        font-size: 2.2rem !important; 
        font-weight: 800; 
        text-transform: uppercase; 
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .sub-title-text {{ font-size: 4.5rem; font-weight: 700; margin-bottom: 0px; }}
    .your-future-text {{ font-size: 2.5rem; color: var(--light-blue); margin-top: -10px; margin-bottom: 40px; }}
    
    hr {{ border: 0; border-top: 2px solid var(--accent-blue); margin-top: -10px; margin-bottom: 30px; }}
    .content-section {{ background: rgba(84, 119, 146, 0.15); padding: 30px; border-radius: 20px; margin-bottom: 20px; border: 1px solid rgba(148, 180, 193, 0.3); }}
    .ats-advice {{ font-style: italic; color: var(--light-blue); padding: 15px; border-left: 5px solid var(--cream); margin-top: 15px; background: rgba(234, 224, 207, 0.1); border-radius: 0 10px 10px 0; }}
    
    .score-container {{
        display: flex;
        justify-content: space-around;
        padding: 20px;
        background: rgba(148, 180, 193, 0.1);
        border-radius: 15px;
        margin-top: 20px;
    }}
    .score-card {{ text-align: center; }}
    .score-val {{ font-size: 2.5rem; font-weight: bold; color: var(--light-blue); }}
</style>
""", unsafe_allow_html=True)




roles = {
    "Business Analyst": ["Excel","SQL","Business Analysis","Communication"],
    "Data Analyst": ["Python","Statistics","SQL","Data Visualization"],
    "Frontend Developer": ["HTML","CSS","JavaScript","React"],
    "Backend Developer": ["Python","SQL","APIs","Databases"]
}

role_info = {
    "Business Analyst": "Bridge the gap between IT and business using data to determine requirements.",
    "Data Analyst": "Transform raw data into meaningful insights through cleaning and visualization.",
    "Frontend Developer": "Create the visual and interactive elements of websites users interact with.",
    "Backend Developer": "Build and maintain the server-side logic and database management."
}

courses = {
    "Python":["Python for Data Science (IBM)","Automate the Boring Stuff"],
    "Statistics":["StatQuest by Josh Starmer","Intro to Descriptive Statistics"],
    "SQL":["SQL for Data Analytics (Udacity)","Mode SQL Tutorial"],
    "Data Visualization":["Tableau Desktop Specialist","Data Viz with Matplotlib"],
    "HTML":["MDN Web Docs","freeCodeCamp Responsive Design"],
    "CSS":["CSS Layout Mastery","Flexbox Froggy"],
    "JavaScript":["Eloquent JavaScript","Javascript.info"],
    "React":["React Official Docs","Epic React by Kent C. Dodds"],
    "APIs":["Postman API Essentials","RESTful API Design"],
    "Databases":["Database Design (Coursera)","PostgreSQL for Beginners"],
    "Excel":["Excel Skills for Business (Macquarie)","Data Analysis with Excel"],
    "Business Analysis":["BA Fundamentals (Udemy)","IIBA Entry Certificate"],
    "Communication":["Public Speaking Foundations","Business Writing Skills"]
}

mcq_bank = {
    "Data Analyst": {
        "Basic": [
            ("Which library is used for dataframes in Python?", ["Pandas", "NumPy", "Matplotlib", "Seaborn"], 0),
            ("SQL: Which clause sorts data in descending order?", ["ASC", "DESC", "ORDER", "SORT"], 1),
            ("What is the average of 10, 20, 30?", ["15", "20", "25", "30"], 1),
            ("Which chart shows trends over time?", ["Pie", "Bar", "Line", "Scatter"], 2),
            ("SQL: Which keyword removes duplicates?", ["UNIQUE", "DISTINCT", "CLEAN", "SOLO"], 1),
            ("Excel formulas always start with:", ["+", "-", "=", "/"], 2),
            ("What type of data is '3.14'?", ["Int", "String", "Float", "Bool"], 2),
            ("Which tool is for Business Intelligence?", ["Tableau", "Photoshop", "Notepad", "PyCharm"], 0),
            ("Python lists are defined with which brackets?", ["()", "{}", "[]", "<>"], 2),
            ("What does SQL stand for?", ["Simple Query Language", "Structured Query Language", "System Query Logic", "None"], 1)
        ],
        "Intermediate": [
            ("What is a p-value < 0.05 indicative of?", ["Significance", "Error", "Insignificant", "Randomness"], 0),
            ("Which SQL join returns all left table records?", ["INNER", "LEFT", "RIGHT", "OUTER"], 1),
            ("What is a primary key?", ["Unique ID", "Foreign Link", "Null Value", "Text String"], 0),
            ("Which Python method handles missing values?", ["dropna()", "clean()", "remove()", "stop()"], 0),
            ("Normal distribution is also known as:", ["Bell Curve", "S-Curve", "Z-Curve", "Flat Curve"], 0),
            ("SQL: Which clause filters grouped rows?", ["WHERE", "HAVING", "LIMIT", "ORDER"], 1),
            ("What is correlation?", ["Cause", "Relation", "Difference", "Sum"], 1),
            ("Boxplots are great for seeing:", ["Outliers", "Pie slices", "Logic", "Colors"], 0),
            ("Which command creates a table in SQL?", ["MAKE", "NEW", "CREATE", "ADD"], 2),
            ("What is 'Broadcasting' in NumPy?", ["Scaling arrays", "Deleting data", "Printing data", "Sorting"], 0)
        ]
    }
}




h_col1, h_col2, h_col3, h_col4 = st.columns([4.5, 1, 1, 1])
with h_col1: st.markdown('<p class="logo-text">LUMINEX</p>', unsafe_allow_html=True)
with h_col2: 
    if st.button("Home", use_container_width=True): 
        st.session_state.page = "home"
        st.session_state.selected_role = None
with h_col3: 
    if st.button("Careers", use_container_width=True): st.session_state.page = "careers"
with h_col4: 
    if st.button("About Us", use_container_width=True): st.session_state.page = "about"
st.markdown("<hr>", unsafe_allow_html=True)




if st.session_state.page == "about":
    st.markdown("<p class='sub-title-text'>About Us</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='content-section'><p style='font-size:1.2rem;'>Welcome to LUMINEX, an intelligent career navigation system designed to bridge the gap between where you are and where you want to be. In the fast-evolving world of technology, understanding your own skill set is the first step toward professional growth.<br><br>Our platform utilizes a multi-layered assessment model to provide a clear, data-driven picture of your readiness for key industry roles. By integrating Natural Language Processing (NLP) to parse resumes and cross-referencing that data with subjective self-assessments, LUMINEX generates a unique 'Skill Vector' for every user.</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "careers":
    st.markdown("<p class='sub-title-text'>Career Paths</p>", unsafe_allow_html=True)
    for r, info in role_info.items():
        st.markdown(f"<div class='content-section'><h2>{r}</h2><p>{info}</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "home" and st.session_state.selected_role is None:
    st.markdown("<p class='sub-title-text'>Select Your Target Career Path</p>", unsafe_allow_html=True)
    st.markdown("<p class='your-future-text'>The Future Awaits You!!</p>", unsafe_allow_html=True)
    cols = st.columns(4)
    role_list = list(roles.keys())
    for i in range(4):
        with cols[i]:
            if st.button(role_list[i], key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_role = role_list[i]




if st.session_state.selected_role:
    role = st.session_state.selected_role
    skills = roles[role]
    st.markdown(f"<p class='sub-title-text'>Assessment: {role}</p>", unsafe_allow_html=True)
    
    method = st.multiselect("Select Assessment Mode", ["Resume", "Questionnaire"], default=[])
    resume_text = ""
    resume_ratings = {}
    ats_val = 0

    if "Resume" in method:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        pdf = st.file_uploader("Upload Resume (PDF)", type="pdf")
        if pdf:
            reader = PyPDF2.PdfReader(pdf)
            resume_text = "".join(p.extract_text().lower() for p in reader.pages)
            
            keyword_match_count = sum(s.lower() in resume_text for s in skills)
            keyword_score = (keyword_match_count / len(skills)) * 60
            section_score = 20 if all(k in resume_text for k in ["skills","experience","project"]) else 10
            ats_val = round(keyword_score + section_score + 20)
            
            st.write(f"### 📊 ATS Resume Score: **{ats_val}%**")
            
            st.markdown("<div class='ats-advice'>", unsafe_allow_html=True)
            missing_skills = [s for s in skills if s.lower() not in resume_text]
            if ats_val < 50:
                st.write(f"⚠️ **Critical Advice:** Your resume is missing core keywords like: **{', '.join(missing_skills)}**. Use a standard single-column format to improve readability for ATS scanners.")
            elif ats_val < 80:
                st.write(f"📈 **Improvement Tip:** Good foundation! To increase your score, ensure you quantify your achievements and add a dedicated 'Skills' section featuring missing core components.")
            else:
                st.write("✅ **Excellent Alignment:** Your resume is well-optimized for this role!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Skill Ratings from Resume")
            for s in skills:
                rating = 4 if s.lower() in resume_text else 1
                resume_ratings[s] = rating
                st.write(f"**{s}:** {'⭐' * rating} ({'Match Found' if rating==4 else 'No Match Found'})")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-section'><h3>Self-Skill Assessment</h3>", unsafe_allow_html=True)
    q_signal = {}
    for s in skills:
        c1, c2 = st.columns(2)
        with c1: k = st.slider(f"{s}: Theory", 0, 5, 2, key=f"k_{s}")
        with c2: p = st.slider(f"{s}: Practical", 0, 5, 2, key=f"p_{s}")
        q_signal[s] = (k+p)/2
    st.markdown("</div>", unsafe_allow_html=True)

    self_avg = round(np.mean(list(q_signal.values())), 2)


    def generate_roadmap_ui():
        gaps = [s for s in skills if q_signal[s] < 3.5 or (resume_ratings.get(s, 1) < 3)]
        if gaps:
            st.subheader("🛣 Personalized Roadmap")
            for g in gaps:
                st.write(f"**Step: Master {g}**")
                for c in courses.get(g, ["General Documentation"]): st.write(f"• {c}")
            
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4)
            styles = getSampleStyleSheet()
            content = [Paragraph(f"LUMINEX {role} Roadmap", styles['Title']), Spacer(1, 20)]
            for g in gaps:
                content.append(Paragraph(f"Focus: {g}", styles['Heading2']))
                for c in courses.get(g, ["General Documentation"]):
                    content.append(Paragraph(f"- {c}", styles['Normal']))
            doc.build(content)
            st.download_button("📥 Download PDF Roadmap", buf.getvalue(), "Luminex_Roadmap.pdf")

    if "Questionnaire" in method:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        level = "Basic" if self_avg <= 2.5 else "Intermediate"
        
        q_list = mcq_bank.get(role, mcq_bank["Data Analyst"]).get(level)
        
        st.subheader(f"Technical MCQs ({level})")
        correct = 0
        for i, (q, o, a) in enumerate(q_list):
            ans = st.radio(f"Q{i+1}: {q}", o, index=None, key=f"mcq_{i}")
            if ans and o.index(ans) == a: correct += 1
        
        if st.button("📊 Final Skill Evaluation"):
            mcq_final = round((correct/10)*5, 2)
            
            st.markdown(f"""
            <div class='score-container'>
                <div class='score-card'><p>Self-Assessment</p><p class='score-val'>{self_avg}/5</p></div>
                <div class='score-card'><p>MCQ Validated</p><p class='score-val'>{mcq_final}/5</p></div>
            </div>
            """, unsafe_allow_html=True)

            diff = mcq_final - self_avg
            if diff < -1: st.error("💡 **Verdict:** You are **overestimating** your skills. Focus more on fundamentals.")
            elif diff > 1: st.warning("💡 **Verdict:** You are **underestimating** your skills. You have more potential than you think!")
            else: st.success("💡 **Verdict:** You are **correctly estimating** your skill level. Great self-awareness!")

            generate_roadmap_ui()
            
           
            cur.execute("INSERT INTO signals (role, skill_vector, mcq_score, roadmap_downloaded, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (role, str(list(q_signal.values())), correct, 1, datetime.now().isoformat()))
            conn.commit()
        st.markdown("</div>", unsafe_allow_html=True)
    
   
    elif "Resume" in method and resume_text:
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        generate_roadmap_ui()
        st.markdown("</div>", unsafe_allow_html=True)
