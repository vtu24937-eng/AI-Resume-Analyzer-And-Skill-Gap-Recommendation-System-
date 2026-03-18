from config import JOB_ROLES, SCORE_WEIGHTS


def analyze_skills(extracted_skills: list, job_role: str) -> tuple:
    """
    Compare extracted resume skills with required job role skills.
    Returns (matching_skills, missing_skills).
    """
    role_data = JOB_ROLES.get(job_role, {})
    required = [s.lower() for s in role_data.get("required_skills", [])]
    extracted_lower = [s.lower() for s in extracted_skills]

    matching = [s for s in required if s in extracted_lower]
    missing  = [s for s in required if s not in extracted_lower]

    return matching, missing


def calculate_score(matching_skills: list, missing_skills: list,
                    education: list, experience: list,
                    certifications: list, parsed_data: dict) -> float:
    """
    Weighted resume score (0–100):
      - 50% skills match ratio
      - 20% experience
      - 15% education
      - 10% certifications
      - 5%  contact info completeness
    """
    total_skills = len(matching_skills) + len(missing_skills)

    # 1. Skills match (50 pts)
    if total_skills > 0:
        skill_score = (len(matching_skills) / total_skills) * SCORE_WEIGHTS["skills_match"]
    else:
        skill_score = 0

    # 2. Experience (20 pts) — scaled by number of positions found
    exp_count = len(experience)
    exp_score = min(exp_count, 4) / 4 * SCORE_WEIGHTS["experience"]

    # 3. Education (15 pts)
    edu_score = min(len(education), 2) / 2 * SCORE_WEIGHTS["education"]

    # 4. Certifications (10 pts)
    cert_score = min(len(certifications), 3) / 3 * SCORE_WEIGHTS["certifications"]

    # 5. Contact info (5 pts) — name + email + phone
    contact_pts = 0
    if parsed_data.get("name") and parsed_data["name"] != "Unknown":
        contact_pts += 2
    if parsed_data.get("email"):
        contact_pts += 2
    if parsed_data.get("phone"):
        contact_pts += 1
    contact_score = (contact_pts / 5) * SCORE_WEIGHTS["contact_info"]

    total = skill_score + exp_score + edu_score + cert_score + contact_score
    return round(min(total, 100), 1)


def get_score_label(score: float) -> dict:
    """Return a label and color class for the score."""
    if score >= 80:
        return {"label": "Excellent", "color": "excellent"}
    elif score >= 60:
        return {"label": "Good", "color": "good"}
    elif score >= 40:
        return {"label": "Average", "color": "average"}
    else:
        return {"label": "Needs Improvement", "color": "poor"}


def get_resume_feedback(parsed_data: dict, score: float,
                        matching: list, missing: list) -> list:
    """Generate qualitative resume quality feedback."""
    feedback = []

    if not parsed_data.get("email"):
        feedback.append({"type": "warning", "msg": "Email address is missing. Add a professional email."})
    if not parsed_data.get("phone"):
        feedback.append({"type": "warning", "msg": "Phone number is missing. Recruiters need a contact number."})
    if parsed_data.get("name") == "Unknown":
        feedback.append({"type": "warning", "msg": "Name could not be detected. Ensure your name is clearly at the top."})
    if len(parsed_data.get("education", [])) == 0:
        feedback.append({"type": "warning", "msg": "Education section not found. Add your educational background."})
    if len(parsed_data.get("experience", [])) == 0:
        feedback.append({"type": "info", "msg": "No work experience detected. Add internships, projects, or freelance work."})
    if len(parsed_data.get("certifications", [])) == 0:
        feedback.append({"type": "info", "msg": "No certifications found. Certifications can boost your profile significantly."})
    if len(matching) >= 10:
        feedback.append({"type": "success", "msg": f"Great skill alignment! You match {len(matching)} required skills."})
    elif len(matching) >= 5:
        feedback.append({"type": "info", "msg": f"Moderate skill match ({len(matching)} skills). Work on covering more required skills."})
    else:
        feedback.append({"type": "warning", "msg": f"Low skill match ({len(matching)} skills). Focus on acquiring the missing skills."})
    if len(parsed_data.get("skills", [])) < 5:
        feedback.append({"type": "warning", "msg": "Too few skills listed. Explicitly list all technical skills in a dedicated Skills section."})
    if score >= 75:
        feedback.append({"type": "success", "msg": "Your resume score is strong! You are a competitive candidate for this role."})
    elif score >= 50:
        feedback.append({"type": "info", "msg": "Your resume is decent but has room for improvement."})
    else:
        feedback.append({"type": "warning", "msg": "Your resume needs significant improvements to be competitive for this role."})

    return feedback
