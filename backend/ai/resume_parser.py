"""Resume parser — extracts text and skills from PDF/DOCX resumes."""
import os
import re
import json
import requests
from typing import Dict, List, Tuple
import spacy
    
# Comprehensive skills database for matching
TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "ruby", "go",
    "rust", "swift", "kotlin", "php", "scala", "r", "matlab", "perl", "dart", "lua",
    "objective-c", "shell", "bash", "powershell", "sql", "nosql", "graphql",
    # Web Frontend
    "html", "css", "react", "reactjs", "react.js", "angular", "angularjs", "vue",
    "vuejs", "vue.js", "svelte", "nextjs", "next.js", "nuxtjs", "gatsby",
    "tailwind", "tailwindcss", "bootstrap", "sass", "less", "webpack", "vite",
    "jquery", "redux", "mobx", "zustand",
    # Web Backend
    "node", "nodejs", "node.js", "express", "expressjs", "fastapi", "django",
    "flask", "spring", "spring boot", "rails", "ruby on rails", "asp.net", "laravel",
    "nestjs", "koa", "hapi", "gin", "echo", "fiber",
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis", "elasticsearch",
    "cassandra", "dynamodb", "firebase", "supabase", "oracle", "mariadb",
    "neo4j", "couchdb", "influxdb",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "jenkins", "ci/cd", "github actions", "gitlab ci",
    "nginx", "apache", "linux", "unix", "heroku", "vercel", "netlify",
    "cloudflare", "digitalocean",
    # AI/ML/Data
    "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
    "scikit-learn", "sklearn", "pandas", "numpy", "scipy", "matplotlib",
    "seaborn", "plotly", "opencv", "nlp", "natural language processing",
    "computer vision", "reinforcement learning", "neural networks",
    "data science", "data analysis", "data engineering", "spark", "hadoop",
    "airflow", "kafka", "etl", "power bi", "tableau",
    "prompt engineering", "agentic ai", "rag", "retrieval-augmented generation", "llm",
    # Mobile
    "android", "ios", "react native", "flutter", "xamarin", "ionic",
    "swiftui", "jetpack compose",
    # Tools & Others
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack",
    "figma", "adobe xd", "photoshop", "illustrator",
    "rest", "restful", "microservices", "agile", "scrum",
    "unit testing", "integration testing", "selenium", "cypress", "jest",
    "pytest", "junit", "mocha", "chai",
    "blockchain", "solidity", "web3", "ethereum",
    "iot", "arduino", "raspberry pi",
    "excel", "word", "powerpoint",
    "pdfplumber", "object-oriented programming", "oop", "operating systems", "computer networks", "overleaf", "groq",
    "spacy", "data structures", "decision tree", "random forest", "logistic regression", "ml",
}

SOFT_SKILLS = {
    "leadership", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "creativity", "collaboration", "analytical",
    "project management", "presentation", "negotiation", "decision making",
    "conflict resolution", "mentoring", "strategic thinking", "attention to detail",
    "multitasking", "work ethic", "interpersonal", "organization",
}

# Normalize skill names for display
SKILL_DISPLAY_MAP = {
    "reactjs": "React", "react.js": "React", "vuejs": "Vue.js", "vue.js": "Vue.js",
    "angularjs": "Angular", "nodejs": "Node.js", "node.js": "Node.js",
    "nextjs": "Next.js", "next.js": "Next.js", "nuxtjs": "Nuxt.js",
    "expressjs": "Express.js", "nestjs": "NestJS",
    "tailwindcss": "Tailwind CSS", "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mongodb": "MongoDB", "mysql": "MySQL", "sqlite": "SQLite",
    "sklearn": "scikit-learn", "scikit-learn": "scikit-learn",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes",
    "ci/cd": "CI/CD", "github actions": "GitHub Actions",
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "data science": "Data Science", "nlp": "NLP",
    "spring boot": "Spring Boot", "ruby on rails": "Ruby on Rails",
    "react native": "React Native", "google cloud": "Google Cloud",
    "asp.net": "ASP.NET", "c++": "C++", "c#": "C#",
    "javascript": "JavaScript", "typescript": "TypeScript",
    "graphql": "GraphQL", "nosql": "NoSQL",
    "pdfplumber": "pdfplumber",
    "prompt engineering": "Prompt Engineering",
    "agentic ai": "Agentic AI",
    "rag": "RAG",
    "retrieval-augmented generation": "RAG",
    "object-oriented programming": "OOP",
    "oop": "OOP",
    "operating systems": "Operating Systems",
    "computer networks": "Computer Networks",
    "overleaf": "Overleaf",
    "llm": "LLM",
    "groq": "Groq",
    "spacy": "SpaCy",
    "data structures": "Data Structures",
    "decision tree": "Decision Tree",
    "random forest": "Random Forest",
    "logistic regression": "Logistic Regression",
    "ml": "Machine Learning",
    "css": "CSS",
    "html": "HTML",
    "numpy": "NumPy",
    "sql": "SQL",
    "api": "API",
    "github": "GitHub",
    "tailwind": "Tailwind CSS",
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "llm integration": "LLM",
    "groq api": "Groq",
    "fastapi": "FastAPI",
}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""


def extract_text(file_path: str) -> str:
    """Extract text from resume file (PDF or DOCX)."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(file_path)
    return ""


def preprocess_text(text: str) -> str:
    """Normalize line breaks and collapse spaces."""
    if not text:
        return ""
    text = text.replace("\n", " ")
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


nlp = None
_DICT_LEMMAS_CACHED = None


def init_nlp():
    """Initialize spaCy and download model if missing."""
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Programmatic download of model if it isn't installed yet
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            nlp = spacy.load("en_core_web_sm")


def get_dict_lemmas():
    """Pre-compute lemmatized and literal lowercase token sequences for all dictionary skills."""
    global _DICT_LEMMAS_CACHED
    if _DICT_LEMMAS_CACHED is None:
        init_nlp()
        all_skills = TECH_SKILLS | SOFT_SKILLS
        _DICT_LEMMAS_CACHED = {}
        for skill in all_skills:
            doc = nlp(skill.lower())
            lemmas = tuple(t.lemma_.lower() for t in doc if not t.is_space)
            literals = tuple(t.text.lower() for t in doc if not t.is_space)
            _DICT_LEMMAS_CACHED[skill] = (lemmas, literals)
    return _DICT_LEMMAS_CACHED


def is_subsequence(sub: tuple, main: list) -> bool:
    """Check if a sub-sequence of tokens appears in the main sequence."""
    n = len(sub)
    m = len(main)
    if n == 0 or m < n:
        return False
    for i in range(m - n + 1):
        if tuple(main[i:i+n]) == sub:
            return True
    return False


# Words that are never skills — extended blocklist for resume noise
_SKILL_BLOCKLIST = {
    # Generic resume section words
    "resume", "experience", "education", "university", "school", "project",
    "degree", "month", "year", "client", "team", "responsibilities", "work",
    "job", "career", "summary", "role", "name", "email", "phone", "address",
    "gpa", "cgpa", "subject", "semester", "date", "duration", "company",
    "description", "details", "information", "profile", "objective", "skills",
    "hobbies", "interests", "languages", "references", "activities", "achievements",
    "qualification", "course", "curriculum", "present", "current", "gender",
    "status", "nationality", "marriage", "birth", "location", "city", "country",
    "intern", "internship", "developer", "engineer", "manager", "lead", "student",
    "bachelor", "master", "science", "technology", "engineering", "management",
    # Extended blocklist (individual tokens to reject)
    "rank", "rating", "leetcode", "codechef", "platform", "score", "global", "quiz",
    "adaptive", "scoring", "creation", "review", "effort", "contest", "participant",
    "problem", "array", "graph", "tree", "dynamic", "programming",
    "btech", "cs-ai", "cs", "ai", "baseline", "module", "strong", "fundamentals",
    "fundamental", "backend", "frontend", "fullstack", "development", "inconsistencies",
    "inconsistency", "prediction", "performance", "eda", "model", "reliability",
    "langs", "dataset", "concepts", "concept", "framework", "frameworks",
    "database", "databases", "language", "languages", "tech", "technical",
    "skill", "application", "applications", "system", "systems",
    "solution", "solutions", "service", "services", "product", "products",
    "tool", "tools", "topic", "topics", "library", "libraries", "platforms",
    "b.tech", "m.tech", "projects",
    # Generic nouns that appear in resumes but are NOT skills
    "thousands", "hundreds", "millions", "starters", "end", "start", "use",
    "time", "questions", "arrays", "graphs", "trees", "algorithms", "ranking",
    "local", "aug", "jan", "feb", "mar", "apr", "may", "jun", "jul", "sep",
    "oct", "nov", "dec", "pdfs", "pdf", "docs", "api", "apis", "url", "urls",
    "operating", "manual", "automated", "llms", "rag",
    # Additional blocklist entries to stop remaining false positives
    "candidates", "students", "participants", "users", "recruiters",
    "roles", "shortlisting", "matching", "parsing", "recommendations",
    "tracking", "validation", "injection", "workflow", "stage",
    "interaction", "communication", "shortlist", "portal", "placement",
    "concurrent", "session", "endpoint", "dashboard", "interface", "technologies",
}


def is_skill_like(span, matched_dict_skills_lower) -> bool:
    """Check if a parsed span is a valid NLP-detected skill candidate."""
    text = span.text.strip()
    text_lower = text.lower()

    # Length limits: min 2 chars, max 25 chars, max 3 tokens
    if len(text_lower) < 2 or len(text_lower) > 25:
        return False
    if len(span) > 3:
        return False

    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', text):
        return False

    # Must NOT contain any digits (Problem 1a)
    if re.search(r'\d', text):
        return False

    # Only allow safe characters
    if not re.match(r'^[a-zA-Z0-9\s+#./\-_]+$', text):
        return False

    # If ANY token in the span is in the blocklist, reject the span (Problem 1b)
    if any(t.text.lower() in _SKILL_BLOCKLIST for t in span):
        return False

    # POS filtering — block verbs, pronouns, prepositions, determiners, adverbs etc.
    disallowed_pos = {"VERB", "PRON", "ADP", "DET", "ADV", "AUX", "SCONJ", "PART", "CCONJ"}
    for token in span:
        if token.pos_ in disallowed_pos:
            return False
        if token.is_stop:
            return False

    # Block if span is already covered by a dictionary match
    if text_lower in matched_dict_skills_lower:
        return False

    # Reject spans where ALL tokens have pos_ == "PROPN" and the span text appears in the first 100 characters of the resume
    if all(t.pos_ == "PROPN" for t in span) and text_lower in span.doc.text[:100].lower():
        return False

    return True


def format_detected_skill(text: str) -> str:
    """Format a detected skill name cleanly."""
    cleaned = text.strip().strip(".-_")
    if cleaned.isupper():
        return cleaned
    if any(c.isupper() for c in cleaned) and any(c.islower() for c in cleaned):
        return cleaned
    return cleaned.title()


def strip_tag(skill: str) -> str:
    """Strip source tag from a skill string, returning the clean skill name."""
    return re.sub(r'\s*\((matched_from_dictionary|detected_via_nlp|detected_via_llm)\)\s*$', '', skill, flags=re.IGNORECASE).strip()


def extract_skills_llm(text: str) -> List[str]:
    """Helper to extract skills synchronously from Groq API (Layer 2)."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return []

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are a technical skill extractor. Extract ONLY real technical "
        "skills, programming languages, frameworks, tools, libraries, platforms, "
        "and methodologies from the resume text. Do NOT include: soft skills, "
        "job titles, company names, university names, degree names, metrics, "
        "percentages, project descriptions, or generic phrases. Return ONLY a "
        "valid JSON array of strings, nothing else. No explanation, no markdown, "
        "no backticks. Example output: [\"Python\", \"React\", \"PostgreSQL\", \"Docker\"]"
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "max_tokens": 500,
        "temperature": 0.0
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            # Strip markdown block quotes if returned
            if content.startswith("```"):
                content = re.sub(r'^```(?:json)?\s*', '', content)
                content = re.sub(r'\s*```$', '', content)
            
            try:
                skills = json.loads(content)
                if isinstance(skills, list):
                    return [str(s) for s in skills]
            except Exception:
                # Fallback to regex extract if LLM returned extra text surrounding JSON
                match = re.search(r'\[\s*".*?"\s*(?:,\s*".*?"\s*)*\]', content, re.DOTALL)
                if match:
                    skills = json.loads(match.group(0))
                    if isinstance(skills, list):
                        return [str(s) for s in skills]
        else:
            print(f"Warning: Groq API returned status code {response.status_code}")
    except Exception as e:
        print(f"Warning: Failed to parse or fetch LLM skills: {e}")
    return []


def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text using a 2-layer hybrid pipeline."""
    if not text:
        return []

    text = preprocess_text(text)
    
    # ---------------------------------------------------------
    # LAYER 1: SpaCy + Dictionary Matching
    # ---------------------------------------------------------
    init_nlp()
    doc = nlp(text)

    # 1. Match against dictionary skills (lemma + literal)
    lemmatized_tokens = [t.lemma_.lower() for t in doc]
    literal_tokens    = [t.text.lower()   for t in doc]
    dict_lemmas = get_dict_lemmas()

    matched_dict_skills = set()
    for skill, (skill_lemmas, skill_literals) in dict_lemmas.items():
        if is_subsequence(skill_lemmas, lemmatized_tokens) or \
           is_subsequence(skill_literals, literal_tokens):
            matched_dict_skills.add(skill)

    matched_dict_skills_lower = {s.lower() for s in matched_dict_skills}

    # 2. Match candidate noun chunks & entities (ORG, PRODUCT, WORK_OF_ART)
    noise_spans = set()
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "GPE", "LOC", "DATE", "TIME",
                          "CARDINAL", "ORDINAL", "PERCENT", "MONEY",
                          "QUANTITY", "NORP", "FAC", "EVENT", "LAW"):
            noise_spans.add(ent.text.strip().lower())

    detected_skills = {}

    for chunk in doc.noun_chunks:
        if chunk.text.strip().lower() in noise_spans:
            continue
        if is_skill_like(chunk, matched_dict_skills_lower):
            display = format_detected_skill(chunk.text)
            detected_skills[display.lower()] = display

    for ent in doc.ents:
        if ent.label_ not in ("ORG", "PRODUCT", "WORK_OF_ART"):
            continue
        if ent.text.strip().lower() in noise_spans:
            continue
        if is_skill_like(ent, matched_dict_skills_lower):
            display = format_detected_skill(ent.text)
            detected_skills[display.lower()] = display

    # Promote NLP matches to dictionary matches if they exist in dictionary
    all_skills = TECH_SKILLS | SOFT_SKILLS
    all_skills_lower = {s.lower() for s in all_skills}
    for key, display in list(detected_skills.items()):
        if key in all_skills_lower:
            orig = next(s for s in all_skills if s.lower() == key)
            matched_dict_skills.add(orig)
            del detected_skills[key]

    # Format Layer 1 results (with source tags)
    layer1_tagged = []
    for skill in matched_dict_skills:
        display = SKILL_DISPLAY_MAP.get(skill, skill.title())
        layer1_tagged.append(f"{display} (matched_from_dictionary)")

    for display in detected_skills.values():
        display_mapped = SKILL_DISPLAY_MAP.get(display.lower(), display)
        layer1_tagged.append(f"{display_mapped} (detected_via_nlp)")

    # ---------------------------------------------------------
    # LAYER 2: LLM Extraction via Groq
    # ---------------------------------------------------------
    raw_llm_skills = extract_skills_llm(text)
    
    llm_noise_list = {
        "resume", "experience", "education", "university", "bachelor", "master",
        "engineer", "developer", "manager", "intern", "team", "project", "system",
        "application", "solution", "platform", "service", "tool", "framework",
        "language", "technology", "software", "hardware", "company", "organization"
    }

    cleaned_llm_skills = []
    for skill in raw_llm_skills:
        skill = skill.strip()
        if not skill:
            continue
        if len(skill) > 40:
            continue
        if re.match(r'^[\d.\s]+$', skill):
            continue
        if skill.lower() in llm_noise_list:
            continue
        
        # Normalize display name
        display = SKILL_DISPLAY_MAP.get(skill.lower(), skill)
        cleaned_llm_skills.append(display)

    # ---------------------------------------------------------
    # MERGING & DEDUPLICATION LOGIC
    # ---------------------------------------------------------
    merged_skills = {}  # canonical_normalized -> {"tagged": str, "priority": int}
    
    # Helper to get normalized canonical form (independent of tags)
    def normalize_internal(s: str) -> str:
        s_clean = re.sub(r'\s*\((matched_from_dictionary|detected_via_nlp|detected_via_llm)\)\s*$', '', s, flags=re.IGNORECASE).strip().lower()
        # Clean up common synonyms to align
        from ai.skill_matcher import normalize_skill
        return normalize_skill(s_clean)

    # 1. Add Layer 1 results
    for tagged in layer1_tagged:
        norm = normalize_internal(tagged)
        priority = 3 if "matched_from_dictionary" in tagged else 2
        merged_skills[norm] = {"tagged": tagged, "priority": priority}

    # 2. Add Layer 2 results (tag as detected_via_llm)
    for clean in cleaned_llm_skills:
        tagged = f"{clean} (detected_via_llm)"
        norm = normalize_internal(tagged)
        # Keep Layer 1 if already exists, else insert Layer 2
        if norm not in merged_skills:
            merged_skills[norm] = {"tagged": tagged, "priority": 1}

    return sorted([item["tagged"] for item in merged_skills.values()])


def extract_cgpa(text: str) -> float:
    """Try to extract CGPA/GPA from resume text."""
    patterns = [
        r'(?:cgpa|gpa|cpi)\s*[:\-]?\s*(\d+\.?\d*)\s*(?:/\s*(?:10|4))?',
        r'(\d+\.\d+)\s*/\s*(?:10|4)\s*(?:cgpa|gpa|cpi)',
        r'(?:grade|score)\s*[:\-]?\s*(\d+\.?\d*)\s*/\s*10',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            val = float(match.group(1))
            if val <= 10:
                return val
    return 0.0


def extract_experience_years(text: str) -> float:
    """Try to extract years of experience from resume text."""
    patterns = [
        r'(\d+\.?\d*)\+?\s*years?\s*(?:of)?\s*(?:experience|exp)',
        r'experience\s*[:\-]?\s*(\d+\.?\d*)\s*years?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return float(match.group(1))
    return 0.0


def parse_resume(file_path: str) -> Dict:
    """Parse a resume file and extract structured information."""
    text = extract_text(file_path)
    if not text:
        return {"text": "", "skills": [], "cgpa": 0.0, "experience_years": 0.0}

    text = preprocess_text(text)
    skills = extract_skills(text)
    cgpa = extract_cgpa(text)
    experience = extract_experience_years(text)

    return {
        "text": text,
        "skills": skills,
        "cgpa": cgpa,
        "experience_years": experience,
    }
