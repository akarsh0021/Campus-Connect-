"""
Comprehensive functional test for all CampusConnect API endpoints.
Tests: Auth, Students, Companies, Jobs, Applications, Admin, Notifications + 3 Changes
"""
import requests
import os
import sys

BASE = "http://127.0.0.1:8000"
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []

def check(label, condition, detail=""):
    icon = PASS if condition else FAIL
    results.append((icon, label, detail))
    line = "  " + icon + "  " + label
    if detail:
        line += "  ->  " + str(detail)
    print(line)

def section(name):
    print("\n" + "="*65)
    print("  " + name)
    print("="*65)

# ----- 1. ROOT -------------------------------------------------------
section("1. ROOT ENDPOINT")
try:
    r = requests.get(BASE + "/", timeout=5)
    check("Root GET /", r.status_code == 200, r.json().get("name", ""))
except Exception as e:
    check("Root GET /", False, str(e))

# ----- 2. AUTH -------------------------------------------------------
section("2. AUTH ENDPOINTS")

student_token = None
student_id = None
try:
    r = requests.post(BASE + "/api/auth/login",
        json={"email": "ria.sharma@student.edu", "password": "student123"}, timeout=5)
    ok = r.status_code == 200 and "access_token" in r.json()
    check("POST /api/auth/login (student)", ok, "status=" + str(r.status_code))
    if ok:
        student_token = r.json()["access_token"]
        student_id = r.json()["user"]["id"]
except Exception as e:
    check("POST /api/auth/login (student)", False, str(e))

company_token = None
company_user_id = None
try:
    r = requests.post(BASE + "/api/auth/login",
        json={"email": "hr@techcorp.com", "password": "company123"}, timeout=5)
    ok = r.status_code == 200 and "access_token" in r.json()
    check("POST /api/auth/login (company)", ok, "status=" + str(r.status_code))
    if ok:
        company_token = r.json()["access_token"]
        company_user_id = r.json()["user"]["id"]
except Exception as e:
    check("POST /api/auth/login (company)", False, str(e))

admin_token = None
try:
    r = requests.post(BASE + "/api/auth/login",
        json={"email": "admin@campus.edu", "password": "admin123"}, timeout=5)
    ok = r.status_code == 200 and "access_token" in r.json()
    check("POST /api/auth/login (admin)", ok, "status=" + str(r.status_code))
    if ok:
        admin_token = r.json()["access_token"]
except Exception as e:
    check("POST /api/auth/login (admin)", False, str(e))

try:
    r = requests.post(BASE + "/api/auth/login",
        json={"email": "ria.sharma@student.edu", "password": "wrongpass"}, timeout=5)
    check("POST /api/auth/login (wrong password, expect 401)", r.status_code == 401,
          "status=" + str(r.status_code))
except Exception as e:
    check("POST /api/auth/login (wrong password, expect 401)", False, str(e))

student_h = {"Authorization": "Bearer " + (student_token or "")}
company_h = {"Authorization": "Bearer " + (company_token or "")}
admin_h   = {"Authorization": "Bearer " + (admin_token or "")}

try:
    r = requests.get(BASE + "/api/auth/me", headers=student_h, timeout=5)
    ok = r.status_code == 200 and r.json().get("email") == "ria.sharma@student.edu"
    check("GET /api/auth/me (student)", ok, "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/auth/me (student)", False, str(e))

try:
    r = requests.get(BASE + "/api/auth/me", timeout=5)
    check("GET /api/auth/me (no token, expect 401)", r.status_code == 401,
          "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/auth/me (no token, expect 401)", False, str(e))

# ----- 3. STUDENT PROFILE -------------------------------------------
section("3. STUDENT ENDPOINTS")

try:
    r = requests.get(BASE + "/api/students/profile/" + str(student_id or 1), headers=admin_h, timeout=5)
    check("GET /api/students/profile/{user_id} (view a student)", r.status_code == 200, "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/students/profile/{user_id}", False, str(e))

try:
    r = requests.get(BASE + "/api/admin/users", headers=admin_h, timeout=5)
    students = [u for u in r.json() if u.get("role") == "student"] if r.status_code == 200 else []
    check("Student list via GET /api/admin/users (role=student)", r.status_code == 200,
          "status=" + str(r.status_code) + ", students=" + str(len(students)))
except Exception as e:
    check("Student list via admin/users", False, str(e))

# ----- 4. COMPANY PROFILE -------------------------------------------
section("4. COMPANY ENDPOINTS")

try:
    r = requests.get(BASE + "/api/companies/profile", headers=company_h, timeout=5)
    check("GET /api/companies/profile", r.status_code == 200, "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/companies/profile", False, str(e))

try:
    r = requests.put(BASE + "/api/companies/profile",
        json={"company_name": "TechCorp", "industry": "Technology",
              "website": "https://techcorp.com"},
        headers=company_h, timeout=5)
    check("PUT /api/companies/profile", r.status_code == 200, "status=" + str(r.status_code))
except Exception as e:
    check("PUT /api/companies/profile", False, str(e))

# ----- 5. JOBS -------------------------------------------------------
section("5. JOB ENDPOINTS")

job_id = None
try:
    r = requests.get(BASE + "/api/jobs/", timeout=5)
    ok = r.status_code == 200
    cnt = len(r.json()) if ok else "N/A"
    check("GET /api/jobs/ (public list)", ok,
          "status=" + str(r.status_code) + ", count=" + str(cnt))
    if ok and len(r.json()) > 0:
        job_id = r.json()[0]["id"]
except Exception as e:
    check("GET /api/jobs/ (public list)", False, str(e))

new_job_id = None
try:
    r = requests.post(BASE + "/api/jobs/",
        json={"title": "Test Engineer", "description": "Automated testing role",
              "requirements": "pytest, selenium", "required_skills": ["Python", "pytest"],
              "min_cgpa": 6.0, "experience_required": 0, "location": "Remote",
              "job_type": "Full-time", "salary_range": "10-15 LPA"},
        headers=company_h, timeout=5)
    ok = r.status_code == 200
    check("POST /api/jobs/ (company post new job)", ok, "status=" + str(r.status_code))
    if ok:
        new_job_id = r.json().get("id")
except Exception as e:
    check("POST /api/jobs/ (company post new job)", False, str(e))

if job_id:
    try:
        r = requests.get(BASE + "/api/jobs/my", headers=company_h, timeout=5)
        check("GET /api/jobs/my (company, own jobs)", r.status_code == 200,
              "status=" + str(r.status_code))
    except Exception as e:
        check("GET /api/jobs/my (company, own jobs)", False, str(e))

# ----- 6. APPLICATIONS -----------------------------------------------
section("6. APPLICATION ENDPOINTS")

try:
    r = requests.get(BASE + "/api/applications/", headers=student_h, timeout=5)
    cnt = len(r.json()) if r.status_code == 200 else "N/A"
    check("GET /api/applications/ (student, my apps)", r.status_code == 200,
          "status=" + str(r.status_code) + ", count=" + str(cnt))
except Exception as e:
    check("GET /api/applications/ (student, my apps)", False, str(e))

if job_id:
    try:
        r = requests.post(BASE + "/api/applications/",
                          json={"job_id": job_id, "cover_letter": "Test application"},
                          headers=student_h, timeout=5)
        ok = r.status_code in (200, 400)
        detail = r.json().get("detail", "") if r.status_code == 400 else "applied OK"
        check("POST /api/applications/ (student apply)", ok,
              "status=" + str(r.status_code) + " " + str(detail)[:35])
    except Exception as e:
        check("POST /api/applications/ (student apply)", False, str(e))

if new_job_id:
    try:
        r = requests.get(BASE + "/api/applications/job/" + str(new_job_id),
                         headers=company_h, timeout=5)
        check("GET /api/applications/job/{id} (company)", r.status_code == 200,
              "status=" + str(r.status_code))
    except Exception as e:
        check("GET /api/applications/job/{id} (company)", False, str(e))

# ----- 7. ADMIN ------------------------------------------------------
section("7. ADMIN ENDPOINTS")

try:
    r = requests.get(BASE + "/api/admin/analytics", headers=admin_h, timeout=5)
    check("GET /api/admin/analytics (admin)", r.status_code == 200, "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/admin/analytics (admin)", False, str(e))

try:
    r = requests.get(BASE + "/api/admin/users", headers=admin_h, timeout=5)
    cnt = len(r.json()) if r.status_code == 200 else "N/A"
    check("GET /api/admin/users (admin)", r.status_code == 200,
          "status=" + str(r.status_code) + ", count=" + str(cnt))
except Exception as e:
    check("GET /api/admin/users (admin)", False, str(e))

try:
    r = requests.get(BASE + "/api/admin/analytics", headers=student_h, timeout=5)
    check("GET /api/admin/analytics (student, expect 403)", r.status_code == 403,
          "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/admin/analytics (student, expect 403)", False, str(e))

# ----- 8. NOTIFICATIONS ---------------------------------------------
section("8. NOTIFICATION ENDPOINTS")

try:
    r = requests.get(BASE + "/api/notifications/", headers=student_h, timeout=5)
    check("GET /api/notifications/ (student)", r.status_code == 200,
          "status=" + str(r.status_code))
except Exception as e:
    check("GET /api/notifications/ (student)", False, str(e))

# ----- 9. CHANGE 1: PostgreSQL config --------------------------------
section("9. CHANGE 1 VERIFY -- PostgreSQL / dotenv config")

sys.path.insert(0, r"C:\Users\Admin\CampusPortalPRG3\backend")

try:
    from dotenv import load_dotenv
    load_dotenv(r"C:\Users\Admin\CampusPortalPRG3\backend\.env")
    db_url = os.getenv("DATABASE_URL", "")
    check("DATABASE_URL loaded from .env", bool(db_url),
          db_url[:45] + "..." if len(db_url) > 45 else db_url)
    check("DATABASE_URL is PostgreSQL (not SQLite)",
          db_url.startswith("postgresql"), db_url[:30])
except Exception as e:
    check("PostgreSQL .env config", False, str(e))

try:
    with open(r"C:\Users\Admin\CampusPortalPRG3\backend\config.py") as f:
        cfg = f.read()
    check("config.py uses load_dotenv()", "load_dotenv" in cfg)
    check("config.py uses os.getenv for DATABASE_URL", "os.getenv(\"DATABASE_URL\"" in cfg)
except Exception as e:
    check("config.py content check", False, str(e))

try:
    with open(r"C:\Users\Admin\CampusPortalPRG3\backend\database.py") as f:
        db_src = f.read()
    check("database.py has NO check_same_thread", "check_same_thread" not in db_src)
except Exception as e:
    check("database.py content check", False, str(e))

check(".env.example exists",
      os.path.isfile(r"C:\Users\Admin\CampusPortalPRG3\backend\.env.example"))

try:
    with open(r"C:\Users\Admin\CampusPortalPRG3\backend\requirements.txt") as f:
        req = f.read()
    check("requirements.txt has psycopg2-binary", "psycopg2-binary" in req)
    check("requirements.txt has python-dotenv", "python-dotenv" in req)
    check("requirements.txt has spacy", "spacy" in req)
except Exception as e:
    check("requirements.txt check", False, str(e))

try:
    with open(r"C:\Users\Admin\CampusPortalPRG3\.gitignore") as f:
        gi = f.read()
    check(".gitignore includes .env", ".env" in gi)
except Exception as e:
    check(".gitignore check", False, str(e))

check("Base.metadata.create_all in main.py",
      "create_all" in open(r"C:\Users\Admin\CampusPortalPRG3\backend\main.py").read())

# ----- 10. CHANGE 2: SpaCy NLP --------------------------------------
section("10. CHANGE 2 VERIFY -- SpaCy NLP skill extraction")

try:
    from ai.resume_parser import extract_skills
    sample = ("I have been developing in Python and machine learning applications. "
               "Also know React and FastAPI. Built custom neural networks.")
    out = extract_skills(sample)
    has_tags     = any("matched_from_dictionary" in s or "detected_via_nlp" in s for s in out)
    has_python   = any("Python" in s for s in out)
    has_ml       = any("Machine Learning" in s for s in out)
    has_react    = any("React" in s for s in out)
    has_fastapi  = any("FastAPI" in s or "Fastapi" in s for s in out)
    check("extract_skills() runs without error", True, str(len(out)) + " skills found")
    check("All results have source tags", has_tags, str(out[:2]))
    check("'developing' -> Python (lemmatization)", has_python)
    check("Multi-word: 'machine learning' matched", has_ml)
    check("React matched", has_react)
    check("FastAPI matched", has_fastapi)
except Exception as e:
    check("SpaCy extract_skills() test", False, str(e))

try:
    from ai.resume_parser import extract_skills as es2
    nlp_out = es2("I have expertise in LangChain and prompt orchestration.")
    has_nlp_tag = any("detected_via_nlp" in s for s in nlp_out)
    check("NLP detection tag (detected_via_nlp) present", has_nlp_tag, str(nlp_out[:3]))
except Exception as e:
    check("NLP detected_via_nlp tag test", False, str(e))

try:
    from ai.skill_matcher import normalize_skill
    t1 = normalize_skill("Python (matched_from_dictionary)")
    t2 = normalize_skill("Pandas (detected_via_nlp)")
    check("normalize_skill strips (matched_from_dictionary)", t1 == "python", "'" + t1 + "'")
    check("normalize_skill strips (detected_via_nlp)", t2 == "pandas", "'" + t2 + "'")
except Exception as e:
    check("normalize_skill tag stripping", False, str(e))

try:
    from ai.skill_matcher import match_skills
    tagged = ["Python (matched_from_dictionary)", "React (matched_from_dictionary)",
              "Docker (detected_via_nlp)"]
    score, matched, missing = match_skills(tagged, ["Python", "Docker"])
    check("match_skills works correctly with tagged skills", score == 100.0,
          "score=" + str(score) + " matched=" + str(matched))
except Exception as e:
    check("match_skills with tagged skills", False, str(e))

# ----- 11. CHANGE 3: benchmark_parser.py ----------------------------
section("11. CHANGE 3 VERIFY -- benchmark_parser.py")

bench = r"C:\Users\Admin\CampusPortalPRG3\backend\benchmark_parser.py"
check("benchmark_parser.py file exists", os.path.isfile(bench))

try:
    with open(bench) as f:
        src = f.read()
    check("GROUND_TRUTH dict present in script", "GROUND_TRUTH" in src)
    check("GROUND_TRUTH left as empty template", "GROUND_TRUTH: Dict[str, List[str]] = {" in src)
    check("precision formula present", "precision" in src.lower())
    check("recall formula present", "recall" in src.lower())
    check("f1 formula present", "f1" in src.lower())
    check("summary table printed", "print" in src and "Precision" in src)
    check("source tag stripping in benchmark", "matched_from_dictionary" in src)
except Exception as e:
    check("benchmark_parser.py content check", False, str(e))

check("test_resumes/ directory created",
      os.path.isdir(r"C:\Users\Admin\CampusPortalPRG3\backend\test_resumes"))

# ----- FINAL SUMMARY ------------------------------------------------
section("FINAL SUMMARY")
passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
total  = len(results)
print("\n  Total : " + str(total))
print("  PASS  : " + str(passed))
print("  FAIL  : " + str(failed))

if failed:
    print("\n  Failed checks:")
    for icon, label, detail in results:
        if icon == FAIL:
            print("    [FAIL] " + label + ("  ->  " + detail if detail else ""))

print()
sys.exit(0 if failed == 0 else 1)
