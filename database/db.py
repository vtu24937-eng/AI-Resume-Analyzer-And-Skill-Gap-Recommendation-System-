import sqlite3
import json
import os
from config import DATABASE_PATH


def get_db_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS resumes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT NOT NULL,
            upload_time TEXT NOT NULL DEFAULT (datetime('now')),
            raw_text    TEXT
        );

        CREATE TABLE IF NOT EXISTS analyses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id       INTEGER NOT NULL,
            job_role        TEXT NOT NULL,
            candidate_name  TEXT,
            email           TEXT,
            phone           TEXT,
            education       TEXT,
            skills          TEXT,
            experience      TEXT,
            certifications  TEXT,
            matching_skills TEXT,
            missing_skills  TEXT,
            recommendations TEXT,
            score           REAL DEFAULT 0,
            created_at      TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (resume_id) REFERENCES resumes(id)
        );
    ''')
    conn.commit()
    conn.close()


def save_resume(filename, raw_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO resumes (filename, raw_text) VALUES (?, ?)',
        (filename, raw_text)
    )
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return resume_id


def save_analysis(resume_id, job_role, parsed_data, matching_skills,
                  missing_skills, recommendations, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses
            (resume_id, job_role, candidate_name, email, phone,
             education, skills, experience, certifications,
             matching_skills, missing_skills, recommendations, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_id,
        job_role,
        parsed_data.get('name', ''),
        parsed_data.get('email', ''),
        parsed_data.get('phone', ''),
        json.dumps(parsed_data.get('education', [])),
        json.dumps(parsed_data.get('skills', [])),
        json.dumps(parsed_data.get('experience', [])),
        json.dumps(parsed_data.get('certifications', [])),
        json.dumps(matching_skills),
        json.dumps(missing_skills),
        json.dumps(recommendations),
        score
    ))
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return analysis_id


def get_analysis(analysis_id):
    conn = get_db_connection()
    row = conn.execute(
        'SELECT * FROM analyses WHERE id = ?', (analysis_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    for field in ['education', 'skills', 'experience', 'certifications',
                  'matching_skills', 'missing_skills', 'recommendations']:
        try:
            data[field] = json.loads(data[field]) if data[field] else []
        except (json.JSONDecodeError, TypeError):
            data[field] = []
    return data


def get_all_analyses():
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT a.id, a.candidate_name, a.job_role, a.score, a.created_at, r.filename '
        'FROM analyses a JOIN resumes r ON a.resume_id = r.id '
        'ORDER BY a.created_at DESC'
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
