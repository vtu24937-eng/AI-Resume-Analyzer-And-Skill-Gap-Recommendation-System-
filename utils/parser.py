import re
import spacy

# Load spaCy English model (small)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

# ─── Comprehensive Skills Keyword List ───────────────────────────────────────
ALL_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby",
    "php", "swift", "kotlin", "go", "rust", "scala", "r", "matlab", "perl",
    "bash", "shell scripting", "powershell",
    # Web Frameworks & Libraries
    "react", "angular", "vue.js", "next.js", "nuxt.js", "svelte",
    "node.js", "express.js", "django", "flask", "fastapi", "spring boot",
    "spring framework", "asp.net", "laravel", "rails", "bootstrap",
    "tailwind css", "sass", "webpack", "vite", "redux", "graphql",
    # Data Science & ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "plotly", "jupyter", "sklearn",
    "transformers", "hugging face", "xgboost", "lightgbm",
    "feature engineering", "data wrangling", "a/b testing",
    "regression", "classification", "clustering", "neural network",
    # Databases
    "sql", "mysql", "postgresql", "sqlite", "oracle", "mongodb", "redis",
    "cassandra", "elasticsearch", "dynamodb", "firebase", "nosql",
    "mariadb", "mssql", "neo4j",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "jenkins", "ci/cd", "terraform", "ansible", "nginx", "apache",
    "linux", "unix", "git", "github", "gitlab", "bitbucket",
    "prometheus", "grafana", "helm", "vagrant", "chef", "puppet",
    # Mobile
    "android", "ios", "react native", "flutter", "xamarin",
    # Other Tools & Concepts
    "rest api", "soap", "microservices", "oop", "data structures",
    "algorithms", "design patterns", "agile", "scrum", "jira",
    "unit testing", "integration testing", "tdd", "bdd", "selenium",
    "junit", "pytest", "mocha", "jest", "postman", "swagger",
    "hadoop", "spark", "kafka", "airflow", "etl", "big data",
    "tableau", "power bi", "excel", "statistics", "probability",
    "maven", "gradle", "npm", "yarn", "pip", "virtual environment",
    "mvc", "mvvm", "api development", "socket.io", "websockets",
    "opencv", "arduino", "raspberry pi", "iot", "blockchain",
    "cybersecurity", "networking", "tcp/ip", "crud", "orm",
    "hibernate", "jpa", "jdbc", "spring security", "oauth", "jwt",
    "multithreading", "concurrency", "data analysis", "mlops"
]

# ─── Section Header Patterns ──────────────────────────────────────────────────
EDUCATION_HEADERS = re.compile(
    r'(education|academic|qualification|degree|university|college|school)',
    re.IGNORECASE
)
EXPERIENCE_HEADERS = re.compile(
    r'(experience|employment|work history|professional|internship|career)',
    re.IGNORECASE
)
CERT_HEADERS = re.compile(
    r'(certification|certificate|credential|license|achievement|award)',
    re.IGNORECASE
)

# ─── Degree Keywords ──────────────────────────────────────────────────────────
DEGREE_PATTERN = re.compile(
    r'\b(b\.?tech|b\.?e|b\.?sc|b\.?com|b\.?a|m\.?tech|m\.?sc|m\.?e|'
    r'mba|phd|ph\.d|bachelor|master|doctorate|associate|diploma|'
    r'b\.?s|m\.?s|undergraduate|postgraduate)\b',
    re.IGNORECASE
)


def extract_email(text: str) -> str:
    match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    # Matches common formats: +91-XXXXXXXXXX, (123) 456-7890, 10-digit etc.
    match = re.search(
        r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4,6}',
        text
    )
    if match:
        phone = match.group(0).strip()
        if len(re.sub(r'\D', '', phone)) >= 7:
            return phone
    return ""


def extract_name(text: str) -> str:
    """Try spaCy PERSON entity first, fallback to first non-empty line."""
    doc = nlp(text[:500])  # only scan the beginning
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if 2 <= len(name.split()) <= 5:
                return name

    # Fallback: first line that looks like a name (2-4 capitalized words)
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # Skip lines with @, digits, URL patterns
        if re.search(r'[@\d:/\\]', line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            return line
    return "Unknown"


def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        # Word boundary match
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return list(dict.fromkeys(found))  # preserve order, remove duplicates


def extract_education(text: str) -> list:
    education = []
    lines = text.split('\n')
    capture = False

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if EDUCATION_HEADERS.search(line_stripped):
            capture = True
            continue
        if capture:
            # Stop at next major section
            if any(h.search(line_stripped) for h in [EXPERIENCE_HEADERS, CERT_HEADERS]):
                break
            if DEGREE_PATTERN.search(line_stripped) or any(
                kw in line_stripped.lower() for kw in
                ['university', 'college', 'institute', 'school', 'academy']
            ):
                education.append(line_stripped)

    # Also find inline if section-based failed
    if not education:
        for line in lines:
            if DEGREE_PATTERN.search(line) and len(line.strip()) > 5:
                education.append(line.strip())

    return education[:5]  # cap at 5 entries


def extract_experience(text: str) -> list:
    experience = []
    lines = text.split('\n')
    capture = False
    buffer = []

    year_pattern = re.compile(r'\b(19|20)\d{2}\b')

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            if buffer:
                experience.append(' '.join(buffer))
                buffer = []
            continue
        if EXPERIENCE_HEADERS.search(line_stripped):
            capture = True
            continue
        if capture:
            if EDUCATION_HEADERS.search(line_stripped) or CERT_HEADERS.search(line_stripped):
                break
            if year_pattern.search(line_stripped) or any(
                kw in line_stripped.lower() for kw in
                ['developer', 'engineer', 'intern', 'analyst', 'manager',
                 'lead', 'architect', 'consultant', 'specialist', 'associate']
            ):
                if buffer:
                    experience.append(' '.join(buffer))
                    buffer = []
                buffer.append(line_stripped)
            elif buffer:
                buffer.append(line_stripped)

    if buffer:
        experience.append(' '.join(buffer))

    return experience[:6]


def extract_certifications(text: str) -> list:
    certs = []
    lines = text.split('\n')
    capture = False

    known_certs = [
        'aws certified', 'google certified', 'azure certified', 'oracle certified',
        'cisco', 'comptia', 'pmp', 'scrum master', 'cissp', 'ceh', 'ccna',
        'tensorflow developer', 'tensorflow certificate', 'coursera', 'udemy',
        'microsoft certified', 'red hat', 'databricks', 'snowflake',
        'professional certificate', 'nano degree', 'nanodegree'
    ]

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if CERT_HEADERS.search(line_stripped):
            capture = True
            continue
        if capture:
            if EDUCATION_HEADERS.search(line_stripped) or EXPERIENCE_HEADERS.search(line_stripped):
                break
            if len(line_stripped) > 5:
                certs.append(line_stripped)
        else:
            # Scan entire text for known cert patterns
            lower = line_stripped.lower()
            if any(cert in lower for cert in known_certs):
                if line_stripped not in certs:
                    certs.append(line_stripped)

    return certs[:8]


def parse_resume(text: str) -> dict:
    """Full resume parsing pipeline."""
    return {
        "name":           extract_name(text),
        "email":          extract_email(text),
        "phone":          extract_phone(text),
        "education":      extract_education(text),
        "skills":         extract_skills(text),
        "experience":     extract_experience(text),
        "certifications": extract_certifications(text),
    }
