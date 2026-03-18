import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, JOB_ROLES
from database.db import init_db, save_resume, save_analysis, get_analysis, get_all_analyses
from utils.extractor import extract_text
from utils.parser import parse_resume
from utils.analyzer import analyze_skills, calculate_score, get_score_label, get_resume_feedback
from utils.recommender import get_recommendations

app = Flask(__name__)
app.secret_key = 'resume_analyzer_secret_key_2024'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
with app.app_context():
    init_db()


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page."""
    recent = get_all_analyses()[:5]  # last 5 analyses for the history widget
    return render_template('index.html', recent=recent, job_roles=JOB_ROLES)


@app.route('/upload')
def upload():
    """Resume upload + job role selection page."""
    return render_template('upload.html', job_roles=JOB_ROLES)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle resume upload and run analysis pipeline."""
    # 1. Validate file
    if 'resume' not in request.files:
        flash('No file uploaded. Please select a PDF or DOCX file.', 'error')
        return redirect(url_for('upload'))

    file = request.files['resume']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('upload'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a PDF or DOCX file.', 'error')
        return redirect(url_for('upload'))

    # 2. Validate job role
    job_role = request.form.get('job_role', '').strip()
    if not job_role or job_role not in JOB_ROLES:
        flash('Please select a valid target job role.', 'error')
        return redirect(url_for('upload'))

    # 3. Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 4. Extract text
    raw_text = extract_text(filepath)
    if not raw_text or raw_text.startswith('[Error'):
        flash('Could not extract text from the uploaded file. Please try a different file.', 'error')
        return redirect(url_for('upload'))

    # 5. Parse resume
    parsed_data = parse_resume(raw_text)

    # 6. Skill gap analysis
    matching_skills, missing_skills = analyze_skills(parsed_data['skills'], job_role)

    # 7. Score
    score = calculate_score(
        matching_skills, missing_skills,
        parsed_data['education'], parsed_data['experience'],
        parsed_data['certifications'], parsed_data
    )

    # 8. Recommendations
    recommendations = get_recommendations(missing_skills, job_role)

    # 9. Feedback
    feedback = get_resume_feedback(parsed_data, score, matching_skills, missing_skills)

    # 10. Persist to DB
    resume_id = save_resume(filename, raw_text)
    analysis_id = save_analysis(
        resume_id, job_role, parsed_data,
        matching_skills, missing_skills,
        recommendations, score
    )

    # Clean up uploaded file (optional — keep for re-analysis)
    # os.remove(filepath)

    return redirect(url_for('result', analysis_id=analysis_id))


@app.route('/result/<int:analysis_id>')
def result(analysis_id):
    """Result dashboard for a specific analysis."""
    data = get_analysis(analysis_id)
    if not data:
        flash('Analysis not found.', 'error')
        return redirect(url_for('index'))

    score_info = get_score_label(data['score'])
    role_icon = JOB_ROLES.get(data['job_role'], {}).get('icon', '💼')

    # Rebuild recommendations from stored JSON
    recommendations = data.get('recommendations', {})

    # Rebuild feedback (compute fresh — doesn't need DB)
    feedback = get_resume_feedback(
        {
            "name": data.get('candidate_name', ''),
            "email": data.get('email', ''),
            "phone": data.get('phone', ''),
            "education": data.get('education', []),
            "experience": data.get('experience', []),
            "certifications": data.get('certifications', []),
            "skills": data.get('skills', [])
        },
        data['score'],
        data.get('matching_skills', []),
        data.get('missing_skills', [])
    )

    return render_template(
        'result.html',
        data=data,
        score_info=score_info,
        role_icon=role_icon,
        recommendations=recommendations,
        feedback=feedback
    )


@app.route('/history')
def history():
    """Analysis history page (JSON API used by index page)."""
    return jsonify(get_all_analyses())


@app.route('/api/roles')
def api_roles():
    """Return available job roles as JSON."""
    roles = [{"name": k, "icon": v["icon"]} for k, v in JOB_ROLES.items()]
    return jsonify(roles)


# ─── Error Handlers ───────────────────────────────────────────────────────────

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum allowed size is 16 MB.', 'error')
    return redirect(url_for('upload'))


@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', recent=[], job_roles=JOB_ROLES), 404


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        print("\n" + "="*60)
        print("  [AI] AI Resume Analyzer")
        print("  [OK] Running at: http://127.0.0.1:5000")
        print("="*60 + "\n")
    except UnicodeEncodeError:
        pass
    app.run(debug=False, port=5000)
