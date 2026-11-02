# 💼 Gemini Job Agent

**An AI-powered job analysis application built with Python, Streamlit, Pydantic and Google Gemini.**

Gemini Job Agent is a personal software development project designed to help job seekers evaluate opportunities by comparing job requirements with their technical skills, professional experience and portfolio projects.

The application explores how generative AI can transform job descriptions into structured, actionable career insights.

### 🚀 Live Demo

**[Try the Interactive Demo](https://gemini-job-agent-01.streamlit.app/)**

The public demo showcases the job analysis interface using a fictional job posting and a predefined sample assessment.

**Demo mode:** Live Gemini API requests are disabled to keep the application publicly accessible without API costs. Compatibility scores and recommendations are illustrative rather than generated in real time.

### ✨ Key Features

The original AI-powered application was developed to provide:

- **AI Job Analysis:** Analyse job descriptions using Google's Gemini API.
- **Compatibility Scoring:** Evaluate how closely a candidate's skills match a job's requirements.
- **Skill Gap Identification:** Highlight matching skills, missing requirements and potential blockers.
- **Portfolio Matching:** Identify relevant software projects that support a candidate's application.
- **Transferable Skills:** Recognise valuable experience gained outside the technology industry.
- **Application Recommendations:** Suggest practical next steps based on the assessment.
- **Application Tracking:** Store job analyses, update application statuses and manage notes using SQLite.

### 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-powered analysis in the original application |
| Pydantic | Structured data models and validation |
| SQLite | Local data storage and application tracking |
| Git & GitHub | Version control |
| Streamlit Community Cloud | Public demo deployment |

### 🖥️ How to Try the Demo

1. Open the [Live Demo](https://gemini-job-agent-01.streamlit.app/).
2. Expand **View fictional job description** to review the example job posting.
3. Click **Try Demo**.
4. Explore the sample compatibility score, recommendation, matching requirements, missing skills, relevant portfolio projects and suggested next steps.

The public demo is read-only and does not require an API key.

### 📂 Project Structure

```text
Gemini-job-agent/
├── agents/                 # Original AI analysis logic
├── app.py                  # Public Streamlit demo
├── demo_data.py            # Fictional sample analysis
├── candidate_profile.py    # Candidate profile for AI matching
├── config.py               # Gemini API configuration
├── database.py             # SQLite persistence
├── models.py               # Pydantic data models
├── requirements.txt        # Python dependencies
└── README.md
```

### ⚙️ Run the Public Demo Locally

**1. Clone the repository**

```bash
git clone https://github.com/Saretta1194/Gemini-job-agent.git
cd Gemini-job-agent
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install the demo dependencies**

```bash
python -m pip install streamlit pydantic
```

**4. Start the application**

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### 🧠 AI Integration

The original project integrates the Google Gemini API to analyse job descriptions against a structured candidate profile.

It uses Pydantic to validate the resulting analysis, including compatibility scores, recommendations, matching requirements, missing skills and suggested actions.

The public deployment currently uses predefined demonstration data instead of live AI inference. The original agent implementation remains available in the repository for code review and further development.

### 🔮 Future Improvements

- Restore optional live AI analysis with controlled API usage.
- Support additional job-search sources.
- Add configurable candidate profiles.
- Improve application tracking and reporting.
- Introduce automated tests and deployment checks.

### 👩‍💻 About the Developer

**Sara Rosati — Full Stack Software Developer**

I am transitioning into software development after several years of professional experience in hospitality. Through my Full Stack Software Development studies and independent projects, I have developed practical skills in Python, Django, JavaScript, SQL and web application development.

I built this project to combine my interest in AI with a real-world challenge: making job opportunities easier to evaluate through structured analysis.

**Portfolio:** https://rosatisara.com

**GitHub:** https://github.com/Saretta1194

**Repository:** https://github.com/Saretta1194/Gemini-job-agent

### 📌 Disclaimer

This is a portfolio and educational project. Demo scores and recommendations are illustrative and do not represent live AI-generated assessments or guarantees of employment.
