"""Job recommendation engine for students."""
from typing import List, Dict
from ai.skill_matcher import compute_skill_similarity, normalize_skill


def recommend_jobs(student_profile: Dict, jobs: List[Dict], top_n: int = 10) -> List[Dict]:
    """
    Recommend jobs for a student based on profile matching.

    student_profile: {skills, cgpa, experience_years, department}
    jobs: [{id, title, required_skills, min_cgpa, experience_required, ...}]

    Returns top N jobs sorted by match score.
    """
    student_skills = student_profile.get("skills", [])
    student_cgpa = student_profile.get("cgpa", 0)
    student_exp = student_profile.get("experience_years", 0)

    scored_jobs = []

    for job in jobs:
        # Skill similarity (Jaccard)
        skill_sim = compute_skill_similarity(student_skills, job.get("required_skills", []))

        # CGPA eligibility bonus
        min_cgpa = job.get("min_cgpa", 0)
        cgpa_bonus = 1.0 if student_cgpa >= min_cgpa else max(0.3, student_cgpa / max(min_cgpa, 1))

        # Experience fit
        req_exp = job.get("experience_required", 0)
        if req_exp <= 0:
            exp_fit = 1.0
        elif student_exp >= req_exp:
            exp_fit = 1.0
        else:
            exp_fit = max(0.3, student_exp / max(req_exp, 1))

        # Combined score
        match_score = (skill_sim * 0.5 + cgpa_bonus * 0.3 + exp_fit * 0.2) * 100

        scored_jobs.append({
            **job,
            "match_score": round(match_score, 1),
            "skill_match": round(skill_sim * 100, 1),
        })

    # Sort by match score descending
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_jobs[:top_n]
