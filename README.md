# Job AI Agent

An AI-powered job application assistant built with Python, Streamlit, Gemini and SQLite.

The application analyses job advertisements against a structured candidate profile, provides a realistic compatibility score and stores relevant opportunities in a local application tracker.

## Overview

Job searching can involve repeatedly reading long advertisements, comparing requirements and keeping track of applications.

Job AI Agent helps simplify this process by:

* comparing job advertisements with the candidate profile;
* calculating a realistic match score;
* identifying matched and missing requirements;
* detecting possible hard blockers;
* recommending whether the candidate should apply;
* highlighting relevant portfolio projects;
* storing job opportunities in a local database;
* tracking the status of each application.

The application is currently designed around the profile of a junior full-stack developer transitioning from hospitality into the technology sector in Switzerland.

## Features

### AI job analysis

The user can paste a complete job advertisement and optionally provide:

* job title;
* company name;
* job URL.

Gemini analyses the opportunity and returns structured information, including:

* compatibility score from 0 to 100;
* recommendation;
* matched requirements;
* missing requirements;
* hard blockers;
* transferable skills;
* relevant portfolio projects;
* salary and schedule information;
* risks and recommended next action.

### Application tracker

Relevant opportunities can be saved in a local SQLite database.

The user can:

* view saved jobs;
* update the application status;
* add notes;
* record submitted applications;
* delete archived opportunities.

### Candidate profile

The application uses a structured candidate profile containing:

* technical skills;
* education;
* portfolio projects;
* languages;
* work authorisation;
* professional background;
* transferable skills;
* location and schedule preferences.

## Technologies

* Python 3.12
* Streamlit
* Google Gemini API
* Google Gen AI Python SDK
* Pydantic
* SQLite
* python-dotenv

## Project structure

```text
job-agent/
├── agents/
│   ├── __init__.py
│   └── job_analyser.py
├── data/
├── .env.example
├── .gitignore
├── app.py
├── candidate_profile.py
├── config.py
├── database.py
├── models.py
├── README.md
└── requirements.txt
```

## Local installation

### 1. Clone the repository

```bash
git clone https://github.com/Saretta1194/job-agent.git
cd job-agent
```

### 2. Create a virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_api_key
GEMINI_MODEL=gemini-3.6-flash
```

The `.env` file is excluded from Git and must never be committed.

### 5. Start the application

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## How it works

The application follows this process:

```text
Job advertisement
        ↓
Candidate profile comparison
        ↓
Gemini structured analysis
        ↓
Pydantic validation
        ↓
Compatibility score and recommendation
        ↓
Optional SQLite storage
```

Gemini is instructed to avoid inventing experience or qualifications and to distinguish optional preferences from mandatory requirements.

The AI score is intended as decision support. It does not guarantee an interview or employment.

## Application statuses

Saved jobs can use the following statuses:

* Nuova
* Da valutare
* Da candidare
* Candidatura inviata
* Colloquio
* Rifiutata
* Offerta ricevuta
* Archiviata

## Security

Sensitive values are stored in environment variables.

The following files are excluded from Git:

* `.env`;
* virtual environments;
* local SQLite databases;
* Python cache files;
* Streamlit secrets.

Never commit a real Gemini API key.

## Current limitations

* Job advertisements must currently be pasted manually.
* The application does not submit applications automatically.
* Job analysis depends on the information included in the advertisement.
* The application uses a local SQLite database.
* The compatibility score is an AI-generated estimate.

## Planned features

* Extract job descriptions directly from URLs
* Detect duplicate job listings
* Generate personalised cover letters
* Generate answers for application questions
* Search approved job sources
* Rank opportunities by relevance
* Add filters for salary, location and schedule
* Add interview preparation
* Add follow-up reminders
* Deploy the application online

## Author

**Sara Rosati**

Junior Full Stack Developer based in the Zurich area.

* Portfolio: https://rosatisara.com
* GitHub: https://github.com/Saretta1194
* LinkedIn: https://linkedin.com/in/sararosati

## Disclaimer

This project provides AI-assisted job analysis for informational purposes. Decisions should always be reviewed by the user before applying or sharing personal information.
