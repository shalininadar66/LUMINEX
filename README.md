LUMINEX – Intelligent Career Assessment and Roadmap System

Project Overview
LUMINEX is an intelligent career guidance system developed using Python and Streamlit. The project is designed to help users evaluate their readiness for specific technology and analytics career roles by combining resume analysis, self-assessment, and technical knowledge validation. The system provides a personalized learning roadmap that helps users understand their skill gaps and plan targeted improvement.

The application uses a data-driven approach to bridge the gap between a user’s current skill set and industry expectations.

Objectives
The main objectives of the LUMINEX project are:
• To assess user skills using multiple evaluation methods
• To analyze resumes using ATS-style keyword matching
• To validate self-assessment through MCQ-based testing
• To identify skill gaps for a selected career role
• To generate a personalized learning roadmap in PDF format
• To store assessment data for analysis and future insights

Key Features

Career Role Selection
The system allows users to select a target career path such as Business Analyst, Data Analyst, Frontend Developer, or Backend Developer. Each role is mapped to a predefined set of core skills and role-specific information.

Resume-Based Skill Assessment
Users can upload their resume in PDF format. The system extracts text from the resume and evaluates it using keyword matching and section detection. An ATS-style resume score is generated based on skill relevance, structure, and completeness. Users also receive improvement suggestions to enhance resume alignment with industry standards.

Self-Skill Assessment
Users rate their theoretical knowledge and practical experience for each skill related to the selected role. These ratings are combined to form a self-assessed skill score, which reflects the user’s perceived proficiency level.

Technical MCQ Evaluation
The system presents role-specific multiple-choice questions. The difficulty level (Basic or Intermediate) is automatically selected based on the self-assessment score. MCQ results are used to validate actual knowledge and compare it with self-perception.

Skill Gap Analysis and Personalized Roadmap
Based on resume analysis, self-assessment, and MCQ performance, the system identifies skill gaps. A personalized learning roadmap is generated, recommending relevant courses and resources for each weak skill. The roadmap can be downloaded as a PDF document.

Data Storage and Analytics
All assessment data, including skill vectors, MCQ scores, and timestamps, are stored in an SQLite database. This enables tracking of user signals and supports future analysis and system improvement.

Technologies Used
Programming Language: Python
Web Framework: Streamlit
Database: SQLite
Resume Parsing: PyPDF2
Data Processing: NumPy
PDF Generation: ReportLab
Styling: Custom CSS

System Architecture
The system follows a modular architecture consisting of:
• User Interface Layer for interaction and navigation
• Assessment Layer for resume parsing, self-evaluation, and MCQs
• Analysis Layer for skill gap detection
• Recommendation Layer for roadmap generation
• Storage Layer for persistent data management

How to Run the Project

Install the required Python libraries

Run the application using Streamlit

Access the application through the local browser

Limitations
The resume analysis is keyword-based and does not use advanced NLP techniques. The MCQ bank is limited and can be expanded. The system is designed primarily for academic and learning purposes and does not include user authentication.

Future Enhancements
Future improvements may include advanced NLP-based resume analysis, user login and progress tracking, additional career paths, expanded MCQ sets, analytics dashboards, and cloud deployment.

Conclusion
LUMINEX successfully integrates skill assessment, resume analysis, and learning recommendations into a single intelligent system. The project demonstrates practical application of data science, programming, and system design concepts and serves as a strong academic and portfolio-ready project.

Author
Name: Shalini Nadar
Course: B.Sc. Data Science
Institution: SIES College
