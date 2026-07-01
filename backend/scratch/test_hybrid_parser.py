import os
import sys
import re
sys.path.insert(0, r"c:\Users\Admin\CampusPortalPRG3\backend")

# Load env variables (simulate server startup)
from dotenv import load_dotenv
_env_path = os.path.join(r"c:\Users\Admin\CampusPortalPRG3\backend", ".env")
load_dotenv(dotenv_path=_env_path)

from ai.resume_parser import extract_skills

resume_akarsh = """
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

resume_kevin = """
Kevin Miller
Education: BTech in CS-AI, GPA: 9.2
Strong Fundamentals in Backend Development.
Skills:
- Langs: Python, C++, Java, JavaScript, SQL
- Frameworks: Django, Flask, HTML, CSS
- Databases: MySQL, NoSQL, DBMS
- Tools: Git, GitHub, Postman, Linux
- Data Science / ML: NumPy, Pandas, Matplotlib, Scikit-learn, Hugging Face, Kaggle
- ML Concepts: Logistic Regression, Random Forest, Decision Tree
- Core CS: Operating Systems, Computer Networks, OOP, Data Structures
- AI: NLP, LLM, RAG, Prompt Engineering

Projects:
- EDA Module: Conducted EDA on baseline dataset.
- Model Reliability: Enhanced model reliability and prediction performance.
- Data Inconsistencies: Resolved data inconsistencies.
"""

def clean_source_tag(skill_with_tag: str) -> str:
    cleaned = re.sub(r'\s*\((?:matched_from_dictionary|detected_via_nlp|detected_via_llm)\)$', '', skill_with_tag, flags=re.IGNORECASE)
    return cleaned.strip()

print("="*60)
print("HYBRID PARSER VERIFICATION")
print("="*60)
print(f"Groq API Key present in .env: {bool(os.getenv('GROQ_API_KEY'))}")
print("="*60)

# Run Resume 1
print("\n--- RESUME 1 (AKARSH) DETECTED SKILLS ---")
skills_1 = extract_skills(resume_akarsh)
clean_1 = sorted(list({clean_source_tag(s) for s in skills_1}))
print(f"Total skills returned: {len(skills_1)}")
print("Raw (tagged):")
for s in skills_1:
    print(f"  - {s}")
print("Clean (de-tagged):")
print(", ".join(clean_1))

# Run Resume 2
print("\n--- RESUME 2 (KEVIN) DETECTED SKILLS ---")
skills_2 = extract_skills(resume_kevin)
clean_2 = sorted(list({clean_source_tag(s) for s in skills_2}))
print(f"Total skills returned: {len(skills_2)}")
print("Raw (tagged):")
for s in skills_2:
    print(f"  - {s}")
print("Clean (de-tagged):")
print(", ".join(clean_2))

print("\n" + "="*60)
