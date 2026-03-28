"""AI Ranking Engine — scores and ranks candidates for jobs."""
from typing import Dict, List, Tuple
from ai.skill_matcher import match_skills

# Weight configuration for scoring
WEIGHTS = {
    "skills": 0.40,      # 40% — skill match
    "cgpa": 0.25,        # 25% — academic performance
    "experience": 0.20,  # 20% — relevant experience
    "education": 0.15,   # 15% — education relevance
}


def score_cgpa(student_cgpa: float, min_cgpa: float) -> float:
    """
    Score CGPA on a 0-100 scale.
    Students above min_cgpa get proportional scores.
    Students below get penalized.
    """
    if student_cgpa <= 0:
        return 10.0  # Minimum score if no CGPA provided

    if min_cgpa <= 0:
        # No min requirement — score based on absolute CGPA
        return min(100.0, (student_cgpa / 10.0) * 100)

    if student_cgpa >= min_cgpa:
        # Above minimum: scale from 60-100 based on how far above
        base = 60.0
        extra = min(40.0, ((student_cgpa - min_cgpa) / (10.0 - min_cgpa)) * 40)
        return base + extra
    else:
        # Below minimum: scale from 0-59
        return max(0.0, (student_cgpa / min_cgpa) * 59)


def score_experience(student_exp: float, required_exp: float) -> float:
    """
    Score experience on a 0-100 scale.
    """
    if required_exp <= 0:
        # No requirement — any experience is a bonus
        return min(100.0, 50.0 + student_exp * 20)

    if student_exp >= required_exp:
        base = 70.0
        extra = min(30.0, ((student_exp - required_exp) / max(required_exp, 1)) * 30)
        return base + extra
    else:
        return max(10.0, (student_exp / required_exp) * 70)


def score_education(student_dept: str, job_requirements: str) -> float:
    """
    Score education relevance based on department matching.
    Simple keyword matching against job requirements text.
    """
    if not student_dept or not job_requirements:
        return 50.0  # Neutral score if data missing

    dept_lower = student_dept.lower()
    req_lower = job_requirements.lower()

    # Department relevance mapping
    relevance_map = {
        "computer science": ["software", "developer", "programming", "web", "full stack",
                             "backend", "frontend", "data", "ml", "ai", "devops", "cloud"],
        "information technology": ["software", "developer", "web", "it", "network",
                                   "system", "database", "cloud", "devops"],
        "electronics": ["embedded", "iot", "hardware", "vlsi", "firmware", "signal",
                        "circuit", "semiconductor", "electronics"],
        "mechanical": ["mechanical", "manufacturing", "automotive", "design",
                       "cad", "simulation", "robotics"],
        "electrical": ["electrical", "power", "energy", "electronics", "embedded",
                       "control", "automation"],
        "civil": ["civil", "construction", "structural", "infrastructure", "building"],
        "mathematics": ["data", "analytics", "statistics", "ml", "research",
                        "quantitative", "algorithm"],
        "mba": ["management", "marketing", "finance", "hr", "business", "consulting",
                "strategy", "operations"],
    }

    score = 40.0  # Base score
    for dept_key, keywords in relevance_map.items():
        if dept_key in dept_lower:
            for kw in keywords:
                if kw in req_lower:
                    score += 10
            break

    return min(100.0, score)


def rank_candidate(
    student_skills: List[str],
    student_cgpa: float,
    student_experience: float,
    student_department: str,
    job_required_skills: List[str],
    job_min_cgpa: float,
    job_experience_required: float,
    job_requirements: str = "",
) -> Dict:
    """
    Compute an AI score for a student-job match.

    Returns dict with:
        - total_score: 0-100 weighted score
        - breakdown: individual category scores
        - matched_skills / missing_skills
    """
    # 1. Skills score
    skill_score, matched, missing = match_skills(student_skills, job_required_skills)

    # 2. CGPA score
    cgpa_score = score_cgpa(student_cgpa, job_min_cgpa)

    # 3. Experience score
    exp_score = score_experience(student_experience, job_experience_required)

    # 4. Education score
    edu_score = score_education(student_department, job_requirements)

    # Weighted total
    total = (
        skill_score * WEIGHTS["skills"]
        + cgpa_score * WEIGHTS["cgpa"]
        + exp_score * WEIGHTS["experience"]
        + edu_score * WEIGHTS["education"]
    )

    return {
        "total_score": round(total, 1),
        "breakdown": {
            "skills": round(skill_score, 1),
            "cgpa": round(cgpa_score, 1),
            "experience": round(exp_score, 1),
            "education": round(edu_score, 1),
        },
        "matched_skills": matched,
        "missing_skills": missing,
        "weights": WEIGHTS,
    }


def rank_candidates_for_job(candidates: List[Dict], job: Dict) -> List[Dict]:
    """
    Rank a list of candidate dicts against a job dict.
    Each candidate dict: {id, skills, cgpa, experience_years, department, name, email}
    Job dict: {required_skills, min_cgpa, experience_required, requirements}

    Returns list sorted by score descending.
    """
    scored = []
    for candidate in candidates:
        result = rank_candidate(
            student_skills=candidate.get("skills", []),
            student_cgpa=candidate.get("cgpa", 0),
            student_experience=candidate.get("experience_years", 0),
            student_department=candidate.get("department", ""),
            job_required_skills=job.get("required_skills", []),
            job_min_cgpa=job.get("min_cgpa", 0),
            job_experience_required=job.get("experience_required", 0),
            job_requirements=job.get("requirements", ""),
        )
        scored.append({
            **candidate,
            "ai_score": result["total_score"],
            "ai_breakdown": result["breakdown"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
        })

    scored.sort(key=lambda x: x["ai_score"], reverse=True)
    return scored
