from config import SKILL_RESOURCES, JOB_ROLES


# ─── Career Improvement Tips (generic) ───────────────────────────────────────
CAREER_TIPS = [
    "Build 2–3 portfolio projects and upload them to GitHub to showcase practical experience.",
    "Contribute to open-source projects to demonstrate collaboration and real-world coding skills.",
    "Write technical blogs or LinkedIn articles to build your professional brand.",
    "Participate in competitive programming on LeetCode, HackerRank, or Codeforces.",
    "Pursue relevant certifications (AWS, Google, Microsoft) to boost credibility.",
    "Network actively on LinkedIn — connect with professionals and recruiters in your target field.",
    "Tailor your resume with keywords from each job description before applying.",
    "Practice for technical interviews using sites like LeetCode, InterviewBit, or Pramp.",
    "Join tech communities, hackathons, and meetups to expand your network.",
    "Keep your GitHub profile active with regular commits and well-documented projects.",
    "Consider building an online portfolio website to showcase your projects professionally.",
    "Follow industry leaders and tech blogs like Towards Data Science, CSS-Tricks, or Dev.to.",
]

# ─── Role-specific career advice ─────────────────────────────────────────────
ROLE_TIPS = {
    "Data Scientist": [
        "Participate in Kaggle competitions to build a competitive ML portfolio.",
        "Learn SQL deeply — data retrieval is fundamental for every data role.",
        "Master at least one visualization tool: Tableau, Power BI, or Plotly.",
        "Understand statistics and probability — these are the foundation of data science.",
        "Contribute to ML research by reading and implementing papers from arXiv."
    ],
    "Software Developer": [
        "Practice data structures and algorithms daily on LeetCode or HackerRank.",
        "Learn system design principles — highly valued at mid-to-senior levels.",
        "Master Git workflows (branching, PRs, rebasing) for collaborative development.",
        "Study clean code principles and SOLID design patterns.",
        "Build a side project with a full CRUD backend and deploy it on a free cloud platform."
    ],
    "Web Developer": [
        "Build and deploy at least 3 responsive websites to your portfolio.",
        "Learn web accessibility (WCAG) and SEO best practices.",
        "Understand Core Web Vitals and performance optimization techniques.",
        "Master JavaScript deeply before jumping to frameworks like React or Vue.",
        "Get comfortable with browser DevTools for debugging and performance profiling."
    ],
    "Java Developer": [
        "Deep dive into the Spring ecosystem — Spring Boot, Spring Security, Spring Data.",
        "Practice multithreading and concurrency concepts in Java.",
        "Learn Hibernate/JPA for ORM-based database interactions.",
        "Understand JVM internals and garbage collection for performance tuning.",
        "Build microservices with Spring Boot and deploy them using Docker."
    ],
    "DevOps Engineer": [
        "Get hands-on with a cloud provider: AWS Free Tier is a great start.",
        "Learn Infrastructure as Code with Terraform and configuration management with Ansible.",
        "Set up a CI/CD pipeline from scratch using GitHub Actions or Jenkins.",
        "Master container orchestration with Kubernetes — start with Minikube locally.",
        "Study SRE principles: SLOs, SLIs, error budgets, and incident management."
    ],
    "Machine Learning Engineer": [
        "Learn MLOps tools: MLflow, Kubeflow, or cloud-native ML pipelines.",
        "Deploy at least one ML model as a REST API using FastAPI or Flask.",
        "Understand model monitoring and drift detection in production.",
        "Study distributed training techniques for large-scale model training.",
        "Keep up with the latest research through arXiv, Papers With Code, and Hugging Face."
    ]
}


def get_recommendations(missing_skills: list, job_role: str) -> dict:
    """
    Build a structured recommendations payload:
      - skill_recommendations: per-missing-skill learning path
      - technologies_to_learn: grouped technology suggestions
      - career_tips: role-specific + generic career improvement advice
    """
    skill_recs = []
    for skill in missing_skills[:10]:  # cap to top 10
        resource_info = SKILL_RESOURCES.get(skill.lower(), {
            "resource": f"Search '{skill}' on Coursera, Udemy, or YouTube",
            "time": "2-6 weeks"
        })
        skill_recs.append({
            "skill": skill.title(),
            "resource": resource_info["resource"],
            "estimated_time": resource_info["time"],
            "priority": "High" if missing_skills.index(skill) < 3 else
                        "Medium" if missing_skills.index(skill) < 7 else "Low"
        })

    # Technologies grouped by category
    role_required = [s.lower() for s in JOB_ROLES.get(job_role, {}).get("required_skills", [])]
    tech_groups = {
        "Languages":    [s for s in missing_skills if s.lower() in [
            "python","java","javascript","typescript","c++","c#","ruby","php","go","rust","r","scala"
        ]],
        "Frameworks":   [s for s in missing_skills if s.lower() in [
            "react","angular","vue.js","node.js","spring boot","django","flask","fastapi",
            "express.js","next.js","keras","tensorflow","pytorch","scikit-learn"
        ]],
        "Databases":    [s for s in missing_skills if s.lower() in [
            "sql","mysql","postgresql","mongodb","redis","cassandra","elasticsearch","sqlite"
        ]],
        "DevOps/Cloud": [s for s in missing_skills if s.lower() in [
            "docker","kubernetes","aws","azure","gcp","ci/cd","jenkins","terraform","ansible"
        ]],
        "Tools":        [s for s in missing_skills if s.lower() in [
            "git","github","jira","agile","scrum","postman","jupyter","github","gitlab"
        ]],
    }
    tech_groups = {k: v for k, v in tech_groups.items() if v}  # remove empty

    # Career tips: role-specific first, then generic
    tips = ROLE_TIPS.get(job_role, []) + CAREER_TIPS[:5]

    return {
        "skill_recommendations": skill_recs,
        "technologies_to_learn": tech_groups,
        "career_tips": tips[:8]  # cap to 8 tips
    }
