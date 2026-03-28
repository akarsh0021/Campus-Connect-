"""Resume parser — extracts text and skills from PDF/DOCX resumes."""
import os
import re
from typing import Dict, List, Tuple

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
    # Mobile
    "android", "ios", "react native", "flutter", "xamarin", "ionic",
    "swiftui", "jetpack compose",
    # Tools & Others
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack",
    "figma", "adobe xd", "photoshop", "illustrator",
    "rest", "restful", "api", "microservices", "agile", "scrum",
    "unit testing", "integration testing", "selenium", "cypress", "jest",
    "pytest", "junit", "mocha", "chai",
    "blockchain", "solidity", "web3", "ethereum",
    "iot", "arduino", "raspberry pi",
    "excel", "word", "powerpoint",
}

SOFT_SKILLS = {
    "leadership", "teamwork", "communication", "problem solving", "critical thinking",
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


def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text using keyword matching."""
    text_lower = text.lower()
    found_skills = set()

    # Check multi-word skills first
    all_skills = TECH_SKILLS | SOFT_SKILLS
    multi_word = sorted([s for s in all_skills if " " in s or "/" in s or "." in s], key=len, reverse=True)
    for skill in multi_word:
        if skill in text_lower:
            display = SKILL_DISPLAY_MAP.get(skill, skill.title())
            found_skills.add(display)

    # Check single-word skills with word boundary matching
    words = set(re.findall(r'\b[a-zA-Z#+.]+\b', text_lower))
    for skill in all_skills:
        if " " not in skill and "/" not in skill:
            if skill in words:
                display = SKILL_DISPLAY_MAP.get(skill, skill.title())
                found_skills.add(display)

    return sorted(list(found_skills))


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

    skills = extract_skills(text)
    cgpa = extract_cgpa(text)
    experience = extract_experience_years(text)

    return {
        "text": text,
        "skills": skills,
        "cgpa": cgpa,
        "experience_years": experience,
    }
