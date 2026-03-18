import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'resume_analyzer.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# ─── Job Role Definitions ────────────────────────────────────────────────────
JOB_ROLES = {
    "Software Developer": {
        "required_skills": [
            "python", "java", "c++", "c#", "javascript", "typescript",
            "data structures", "algorithms", "oop", "design patterns",
            "git", "github", "rest api", "unit testing", "agile", "scrum",
            "sql", "linux", "docker", "ci/cd", "problem solving",
            "microservices", "nosql", "mongodb", "redis", "kubernetes"
        ],
        "icon": "💻"
    },
    "Data Scientist": {
        "required_skills": [
            "python", "r", "machine learning", "deep learning", "tensorflow",
            "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
            "seaborn", "sql", "statistics", "probability", "data visualization",
            "feature engineering", "nlp", "computer vision", "big data",
            "spark", "hadoop", "tableau", "power bi", "jupyter", "keras",
            "data wrangling", "a/b testing", "regression", "classification"
        ],
        "icon": "📊"
    },
    "Web Developer": {
        "required_skills": [
            "html", "css", "javascript", "typescript", "react", "angular",
            "vue.js", "node.js", "express.js", "rest api", "graphql",
            "webpack", "git", "responsive design", "sass", "bootstrap",
            "sql", "mongodb", "php", "docker", "nginx", "aws",
            "next.js", "tailwind css", "redux", "jest", "accessibility"
        ],
        "icon": "🌐"
    },
    "Java Developer": {
        "required_skills": [
            "java", "spring boot", "spring framework", "hibernate", "maven",
            "gradle", "jpa", "junit", "rest api", "microservices",
            "sql", "mysql", "postgresql", "git", "docker", "kubernetes",
            "design patterns", "oop", "multithreading", "jdbc", "kafka",
            "redis", "aws", "ci/cd", "jenkins", "agile", "jira"
        ],
        "icon": "☕"
    },
    "DevOps Engineer": {
        "required_skills": [
            "docker", "kubernetes", "jenkins", "ci/cd", "git", "github",
            "linux", "bash", "ansible", "terraform", "aws", "azure", "gcp",
            "nginx", "monitoring", "prometheus", "grafana", "helm",
            "python", "shell scripting", "networking", "security", "agile"
        ],
        "icon": "⚙️"
    },
    "Machine Learning Engineer": {
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "mlops", "model deployment",
            "docker", "kubernetes", "rest api", "sql", "nosql", "spark",
            "feature engineering", "nlp", "computer vision", "keras",
            "git", "statistics", "data pipelines", "aws", "azure"
        ],
        "icon": "🤖"
    }
}

# ─── Scoring Weights ──────────────────────────────────────────────────────────
SCORE_WEIGHTS = {
    "skills_match": 50,      # 50% — skill match ratio
    "experience": 20,         # 20 — work experience
    "education": 15,          # 15 — education
    "certifications": 10,     # 10 — certifications
    "contact_info": 5         # 5  — completeness of contact info
}

# ─── Skill Learning Resources ─────────────────────────────────────────────────
SKILL_RESOURCES = {
    "python": {"resource": "Python.org, Automate the Boring Stuff", "time": "4-8 weeks"},
    "java": {"resource": "Oracle Java Docs, Udemy Java Masterclass", "time": "6-10 weeks"},
    "javascript": {"resource": "MDN Web Docs, JavaScript.info", "time": "4-8 weeks"},
    "react": {"resource": "React official docs, Scrimba React Course", "time": "4-6 weeks"},
    "machine learning": {"resource": "Coursera ML Specialization, Fast.ai", "time": "3-6 months"},
    "deep learning": {"resource": "deeplearning.ai, fast.ai", "time": "3-6 months"},
    "sql": {"resource": "SQLZoo, Mode Analytics SQL Tutorial", "time": "2-4 weeks"},
    "docker": {"resource": "Docker official docs, Play with Docker", "time": "2-3 weeks"},
    "kubernetes": {"resource": "Kubernetes.io docs, KodeKloud", "time": "4-6 weeks"},
    "aws": {"resource": "AWS Free Tier + official training, A Cloud Guru", "time": "4-8 weeks"},
    "spring boot": {"resource": "Baeldung, Spring official docs", "time": "4-6 weeks"},
    "tensorflow": {"resource": "TensorFlow tutorials, DeepLearning.AI", "time": "6-10 weeks"},
    "pytorch": {"resource": "PyTorch official tutorials, Fast.ai", "time": "4-8 weeks"},
    "git": {"resource": "Pro Git Book (free), GitHub Skills", "time": "1-2 weeks"},
    "pandas": {"resource": "Pandas docs, Kaggle Pandas course", "time": "2-3 weeks"},
    "numpy": {"resource": "NumPy docs, freeCodeCamp NumPy tutorial", "time": "1-2 weeks"},
    "typescript": {"resource": "TypeScript Handbook, Execute Program", "time": "2-4 weeks"},
    "node.js": {"resource": "Node.js docs, The Odin Project", "time": "4-6 weeks"},
    "mongodb": {"resource": "MongoDB University (free), official docs", "time": "2-3 weeks"},
    "ci/cd": {"resource": "GitHub Actions docs, Jenkins tutorials", "time": "2-4 weeks"},
    "microservices": {"resource": "Microservices.io, Udemy Microservices", "time": "6-8 weeks"},
    "agile": {"resource": "Scrum.org resources, Atlassian Agile Guide", "time": "1-2 weeks"},
    "django": {"resource": "Django official docs, Django Girls Tutorial", "time": "4-6 weeks"},
    "flask": {"resource": "Flask Mega-Tutorial, official docs", "time": "2-3 weeks"},
    "scikit-learn": {"resource": "scikit-learn docs, Kaggle ML courses", "time": "4-6 weeks"},
    "data structures": {"resource": "GeeksforGeeks, LeetCode, CTCI book", "time": "6-12 weeks"},
    "algorithms": {"resource": "GeeksforGeeks, LeetCode, MIT OCW", "time": "6-12 weeks"},
}
