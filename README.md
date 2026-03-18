# 🎯 AI Resume Analyzer & Skill Gap Recommendation System

An AI-powered full-stack web application that analyzes resumes, extracts key information, identifies skill gaps relative to a target job role, and generates personalized learning recommendations. Built with Python, Flask, spaCy, and a modern dark-mode web UI.

---

## 📁 Folder Structure

```
resume_analyzer/
├── app.py                  ← Flask application (main entry point)
├── config.py               ← Job roles, skill lists, scoring weights
├── requirements.txt        ← All Python dependencies
├── setup.bat               ← One-click setup (Windows)
├── run.bat                 ← One-click run (Windows)
├── README.md
│
├── database/
│   ├── __init__.py
│   └── db.py               ← SQLite init, save, and query helpers
│
├── utils/
│   ├── __init__.py
│   ├── extractor.py        ← PDF / DOCX text extraction
│   ├── parser.py           ← NLP resume parsing (spaCy + regex)
│   ├── analyzer.py         ← Skill gap analysis & resume scoring
│   └── recommender.py      ← Learning recommendations engine
│
├── templates/
│   ├── index.html          ← Home page
│   ├── upload.html         ← Resume upload + job role selection
│   └── result.html         ← Analysis result dashboard
│
└── static/
    ├── css/
    │   └── styles.css      ← Dark glassmorphism UI styles
    └── js/
        └── main.js         ← Drag-drop, animations, score ring
```

---

## ⚙️ Prerequisites

- **Python 3.9 or higher** — Download from [python.org](https://www.python.org/downloads/)
  - ✅ During installation, check **"Add Python to PATH"**

---

## 🚀 Setup & Run (Windows — Recommended)

### Step 1 — One-click Setup
```
Double-click setup.bat
```
This will:
1. Check your Python installation
2. Create a virtual environment (`venv/`)
3. Install all libraries (Flask, PyMuPDF, python-docx, spaCy)
4. Download the spaCy English language model

### Step 2 — Start the Application
```
Double-click run.bat
```
Then open your browser and go to:
```
http://127.0.0.1:5000
```

---

## 🖥️ Manual Setup (Terminal)

```bash
# 1. Navigate to project folder
cd resume_analyzer

# 2. Create virtual environment
python -m venv venv

# 3. Activate it (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install Flask==3.0.0 PyMuPDF==1.23.8 python-docx==1.1.0 spacy==3.7.2 Werkzeug==3.0.1

# 5. Download spaCy English model
python -m spacy download en_core_web_sm

# 6. Start the app
python app.py
```

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Upload** | PDF and DOCX support, drag-and-drop UI |
| 🔍 **AI Extraction** | Name, email, phone, education, skills, experience, certifications |
| 🎯 **Job Role Targeting** | 6 roles: Software Dev, Data Scientist, Web Dev, Java Dev, DevOps, ML Engineer |
| ⚡ **Skill Gap Analysis** | Shows matching ✅ and missing ❌ skills side-by-side |
| 📊 **Resume Score** | Weighted 0–100% score with animated circular ring |
| 🗺️ **Learning Roadmap** | Per-skill resources, estimated time, priority levels |
| 💡 **Career Tips** | Role-specific + generic career improvement suggestions |
| 💬 **Resume Feedback** | Qualitative quality feedback for each section |
| 🖨️ **Print Report** | Print-optimized result page |
| 🗄️ **History** | All analyses stored in SQLite DB |

---

## 🔧 Supported Job Roles

- 💻 Software Developer
- 📊 Data Scientist
- 🌐 Web Developer
- ☕ Java Developer
- ⚙️ DevOps Engineer
- 🤖 Machine Learning Engineer

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9+, Flask 3.0 |
| NLP | spaCy 3.7 (en_core_web_sm) |
| PDF Parsing | PyMuPDF (fitz) |
| DOCX Parsing | python-docx |
| Database | SQLite3 (built-in) |
| Frontend | HTML5, CSS3 (custom), Vanilla JavaScript |
| Fonts | Google Fonts (Inter) |

---

## 📂 Database

SQLite database is auto-created at `database/resume_analyzer.db` on first run.

**Tables:**
- `resumes` — stores filename, upload time, raw extracted text
- `analyses` — stores all parsed data, matching/missing skills, score, recommendations

---

## 🎓 Final Year CS Project Notes

This project demonstrates:
- **Full-stack development** (Python backend + HTML/CSS/JS frontend)
- **NLP techniques** (named entity recognition, regex-based information extraction)
- **Database design** (SQLite with relational schema)
- **REST API design** (Flask routes, JSON responses)
- **AI recommendation systems** (rule-based skill gap analysis)
- **Modern UI design** (dark mode, glassmorphism, responsive grid, CSS animations)

---

## 📝 Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'fitz'`
**Solution:** `pip install PyMuPDF`

**Problem:** `OSError: [E050] Can't find model 'en_core_web_sm'`
**Solution:** `python -m spacy download en_core_web_sm`

**Problem:** Resume name shows "Unknown"
**Solution:** Ensure your name is the first item at the top of your resume in large text.

**Problem:** Very few skills detected
**Solution:** Add a dedicated "Skills" section to your resume listing all technical skills.

---

## 📄 License

Open Source — Free to use, modify, and distribute for educational purposes.
