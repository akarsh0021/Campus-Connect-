"""Skill matching using exact normalization, synonym mappings, and Jaccard similarity."""
from typing import List, Tuple, Dict
import re

# Synonyms map for normalizing skill names
SYNONYMS: Dict[str, str] = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "ml": "machine learning", "dl": "deep learning", "ai": "artificial intelligence",
    "react.js": "react", "reactjs": "react",
    "vue.js": "vue", "vuejs": "vue",
    "node.js": "nodejs", "node": "nodejs",
    "next.js": "nextjs",
    "express.js": "expressjs", "express": "expressjs",
    "mongo": "mongodb",
    "postgres": "postgresql", "pg": "postgresql",
    "k8s": "kubernetes",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "cpp": "c++", "csharp": "c#",
    "graphql": "graphql", "gql": "graphql",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "rest": "rest api",
    "restful": "rest api",
    "rest api": "rest api",
    "llm integration": "llm",
}


def normalize_skill(skill: str) -> str:
    """Normalize a skill name to a canonical form."""
    # Strip (matched_from_dictionary), (detected_via_nlp), or (detected_via_llm) source tags
    s = re.sub(r'\s*\((?:matched_from_dictionary|detected_via_nlp|detected_via_llm)\)$', '', skill, flags=re.IGNORECASE)
    s = s.strip().lower()
    return SYNONYMS.get(s, s)


def match_skills(student_skills: List[str], required_skills: List[str]) -> Tuple[float, List[str], List[str]]:
    """
    Match student skills against job required skills.

    Returns:
        - match_score (0-100): percentage of required skills matched
        - matched: list of matched skills
        - missing: list of missing skills
    """
    if not required_skills:
        return 100.0, [], []

    # Normalize both lists
    student_normalized = {normalize_skill(s): s for s in student_skills}
    required_normalized = {normalize_skill(s): s for s in required_skills}

    matched = []
    missing = []

    for norm_req, orig_req in required_normalized.items():
        if norm_req in student_normalized:
            matched.append(orig_req)
        else:
            # Fuzzy check: partial matching
            found = False
            for norm_stu in student_normalized:
                if norm_req in norm_stu or norm_stu in norm_req:
                    matched.append(orig_req)
                    found = True
                    break
            if not found:
                missing.append(orig_req)

    total = len(required_normalized)
    score = (len(matched) / total) * 100 if total > 0 else 100.0

    return round(score, 1), matched, missing


def compute_skill_similarity(skills_a: List[str], skills_b: List[str]) -> float:
    """Compute Jaccard similarity between two skill sets."""
    if not skills_a or not skills_b:
        return 0.0

    set_a = {normalize_skill(s) for s in skills_a}
    set_b = {normalize_skill(s) for s in skills_b}

    intersection = set_a & set_b
    union = set_a | set_b

    if not union:
        return 0.0

    return len(intersection) / len(union)
