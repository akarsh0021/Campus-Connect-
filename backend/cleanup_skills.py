"""
One-shot DB cleanup: strips source tags from all stored student skills,
removes duplicates, removes blank/numeric entries, and saves clean data back.
"""
import re
import sys
sys.path.insert(0, ".")

from database import SessionLocal
from models.user import StudentProfile

# ---- helpers ---------------------------------------------------------------

TAG_RE = re.compile(r'\s*\((matched_from_dictionary|detected_via_nlp)\)\s*$', re.IGNORECASE)

NOISE = {
    # names / locations / numbers that slipped into DB
    "vadodara", "akarsh sharma", "akarsh", "sharma", "global rank", "leetcode rank",
    # generic resume words
    "resume", "experience", "education", "university", "school", "project",
    "degree", "month", "year", "client", "team", "responsibilities", "work",
    "job", "career", "summary", "role", "name", "email", "phone", "address",
    "gpa", "cgpa", "subject", "semester", "date", "duration", "company",
    "description", "details", "information", "profile", "objective", "skills",
    "hobbies", "interests", "languages", "references", "activities",
    "qualification", "course", "curriculum", "present", "current", "gender",
    "status", "nationality", "birth", "location", "city", "country",
    "intern", "internship", "developer", "engineer", "manager", "lead",
    "bachelor", "master", "science", "technology", "engineering", "management",
    # generic nouns from resumes that are NOT skills
    "libraries", "platforms", "tools", "topics", "applications", "systems",
    "solutions", "services", "products", "features", "modules", "components",
    "participants", "candidates", "users", "students", "clients", "members",
    "thousands", "hundreds", "millions", "starters", "end", "start",
    "time", "effort", "review", "content", "creation", "scoring", "questions",
    "arrays", "graphs", "trees", "dynamic", "programming", "algorithms",
    "rank", "ranking", "global", "local",
    "aug", "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "sep", "oct", "nov", "dec",
    "pdfs", "pdf", "docs", "url", "urls",
    "operating", "manual", "automated", "adaptive", "llms", "rag",
    "admin", "operating systems", "data structures", "dynamic programming",
    "groq api github",
}

def clean_skill(raw: str) -> str:
    """Strip tag, collapse whitespace, return empty string if it's noise."""
    s = TAG_RE.sub("", raw).strip()
    # collapse internal newlines / tabs
    s = re.sub(r'[\r\n\t]+', ' ', s).strip()
    # remove purely numeric or empty
    if not s or re.match(r'^[\d.\s]+$', s):
        return ""
    # too long = likely a sentence, not a skill
    if len(s) > 30:
        return ""
    # check noise blocklist
    if s.lower() in NOISE:
        return ""
    return s


# ---- main ------------------------------------------------------------------

db = SessionLocal()
try:
    profiles = db.query(StudentProfile).all()
    total_fixed = 0

    for profile in profiles:
        original = list(profile.skills or [])
        cleaned = []
        seen = set()
        for raw in original:
            c = clean_skill(raw)
            if c and c.lower() not in seen:
                seen.add(c.lower())
                cleaned.append(c)

        parsed_original = list(profile.parsed_skills or [])
        cleaned_parsed = []
        seen_p = set()
        for raw in parsed_original:
            c = clean_skill(raw)
            if c and c.lower() not in seen_p:
                seen_p.add(c.lower())
                cleaned_parsed.append(c)

        if sorted(cleaned) != sorted(original) or sorted(cleaned_parsed) != sorted(parsed_original):
            profile.skills = sorted(cleaned)
            profile.parsed_skills = sorted(cleaned_parsed)
            total_fixed += 1
            print(f"  Fixed profile user_id={profile.user_id}: {len(original)} -> {len(cleaned)} skills")

    db.commit()
    print(f"\nDone. Fixed {total_fixed} student profiles.")

    # Print what your profile looks like now
    my_profile = db.query(StudentProfile).first()
    if my_profile:
        print("\nSample cleaned skills:")
        for s in (my_profile.skills or []):
            print(f"  - {s}")

finally:
    db.close()
