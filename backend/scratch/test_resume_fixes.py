import sys
import os
sys.path.insert(0, r"c:\Users\Admin\CampusPortalPRG3\backend")

from ai.resume_parser import extract_skills

resume_text = """
Akarsh Sharma
7.7 Vadodara
Education: B.Tech in Computer Science
Achievements: Global Rank 1524 on LeetCode, CodeChef
Skills:
- Languages: Python, C++, C, Java, JavaScript, HTML, CSS
- Web Frameworks & Libraries: React, Node.js, Express.js, Tailwind CSS, FastAPI, pdfplumber, SpaCy, scikit-learn
- Databases: PostgreSQL, SQLite, MongoDB
- Tools & Platforms: Git, GitHub, Postman, Overleaf, Groq
- Core CS Concepts: Operating Systems, Computer Networks, OOP, Data Structures
- AI/Generative AI: NLP, RAG, Prompt Engineering, Agentic AI, LLM

Projects:
- Adaptive Quiz Questions: Built an adaptive quiz platform
- Automated Scoring: Automated scoring using Groq API
- Content Creation Time: Reduced content creation time
- Manual Review Effort: Minimized manual review effort
- NLP
Databases: Explored NLP Databases
- Groq API
GitHub: Hosted Groq API GitHub project
"""

detected = extract_skills(resume_text)

should_be_detected = {
    "Python", "C++", "C", "Java", "React", "Node.js", "Express.js", "HTML", "CSS", 
    "JavaScript", "Tailwind CSS", "FastAPI", "SpaCy", "scikit-learn", "pdfplumber", 
    "PostgreSQL", "SQLite", "MongoDB", "Git", "GitHub", "Postman", "Overleaf", 
    "NLP", "RAG", "Prompt Engineering", "Agentic AI", "LLM", "Groq", 
    "Operating Systems", "Computer Networks", "OOP", "Data Structures"
}

should_not_be_detected = {
    "7.7 Vadodara", "Adaptive Quiz Questions", "Automated Scoring", "Content Creation Time", 
    "Manual Review Effort", "Global Rank 1524", "LeetCode", "NLP Databases", "Groq API GitHub"
}

print("="*60)
print("VERIFICATION RESULTS")
print("="*60)

print("\n--- DETECTED SKILLS ---")
for skill in sorted(detected):
    print(f"  [x] {skill}")

print("\n--- CHECKING SHOULD-BE-DETECTED SKILLS ---")
missing = []
for skill in sorted(should_be_detected):
    # Match case-insensitively
    found = any(s.lower() == skill.lower() for s in detected)
    if found:
        print(f"  [OK] Detected: {skill}")
    else:
        print(f"  [FAIL] Missing: {skill}")
        missing.append(skill)

print("\n--- CHECKING SHOULD-NOT-BE-DETECTED SKILLS ---")
falses = []
for skill in sorted(should_not_be_detected):
    # Match exactly (case-insensitive)
    found = [s for s in detected if s.lower() == skill.lower()]
    if found:
        print(f"  [FAIL] Incorrectly Detected: {skill}")
        falses.extend(found)
    else:
        print(f"  [OK] Correctly Excluded: {skill}")

print("\n" + "="*60)
print(f"SUMMARY: Missing={len(missing)} | False Positives={len(falses)}")
print("="*60)
