"""Seed the database with demo data for testing."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
from models.user import User, StudentProfile, CompanyProfile
from models.job import Job
from models.application import Application
from models.notification import Notification
from services.auth_service import hash_password
from ai.ranking_engine import rank_candidate
from datetime import datetime, timezone, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # Check if already seeded
    if db.query(User).first():
        print("Database already seeded. Skipping...")
        return

    print("🌱 Seeding database...")

    # ── Admin ──
    admin = User(email="admin@campus.edu", password_hash=hash_password("admin123"),
                 role="admin", full_name="Admin User")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"  ✅ Admin: admin@campus.edu / admin123")

    # ── Companies ──
    companies_data = [
        {
            "email": "hr@techcorp.com", "full_name": "TechCorp Solutions",
            "company_name": "TechCorp Solutions", "industry": "Information Technology",
            "website": "https://techcorp.com", "location": "Bangalore, India",
            "description": "Leading software company specializing in enterprise solutions and cloud computing.",
            "employee_count": "1000-5000",
        },
        {
            "email": "recruit@innovate.io", "full_name": "InnovateLabs",
            "company_name": "InnovateLabs", "industry": "AI/ML Startups",
            "website": "https://innovate.io", "location": "Hyderabad, India",
            "description": "AI-first startup building next-gen machine learning products.",
            "employee_count": "50-200",
        },
        {
            "email": "jobs@dataflow.com", "full_name": "DataFlow Analytics",
            "company_name": "DataFlow Analytics", "industry": "Data Analytics",
            "website": "https://dataflow.com", "location": "Mumbai, India",
            "description": "Premier data analytics and business intelligence firm.",
            "employee_count": "200-500",
        },
        {
            "email": "careers@webcraft.dev", "full_name": "WebCraft Studios",
            "company_name": "WebCraft Studios", "industry": "Web Development",
            "website": "https://webcraft.dev", "location": "Pune, India",
            "description": "Creative web development agency building beautiful digital experiences.",
            "employee_count": "50-200",
        },
    ]

    company_profiles = []
    for c in companies_data:
        user = User(email=c["email"], password_hash=hash_password("company123"),
                    role="company", full_name=c["full_name"])
        db.add(user)
        db.commit()
        db.refresh(user)
        profile = CompanyProfile(
            user_id=user.id, company_name=c["company_name"], industry=c["industry"],
            website=c["website"], description=c["description"], location=c["location"],
            employee_count=c["employee_count"],
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        company_profiles.append(profile)
        print(f"  ✅ Company: {c['email']} / company123")

    # ── Students ──
    students_data = [
        {
            "email": "ria.sharma@student.edu", "full_name": "Ria Sharma",
            "department": "Computer Science", "cgpa": 9.2, "graduation_year": 2026,
            "skills": ["Python", "React", "Node.js", "Machine Learning", "SQL", "Docker", "Git"],
            "experience_years": 1.0, "bio": "Passionate CS student with strong ML background.",
        },
        {
            "email": "arjun.patel@student.edu", "full_name": "Arjun Patel",
            "department": "Information Technology", "cgpa": 8.5, "graduation_year": 2026,
            "skills": ["Java", "Spring Boot", "Angular", "PostgreSQL", "AWS", "Kubernetes"],
            "experience_years": 0.5, "bio": "Full-stack developer with Java expertise.",
        },
        {
            "email": "neha.gupta@student.edu", "full_name": "Neha Gupta",
            "department": "Computer Science", "cgpa": 9.6, "graduation_year": 2026,
            "skills": ["Python", "TensorFlow", "PyTorch", "Data Science", "NLP", "Pandas", "R"],
            "experience_years": 1.5, "bio": "AI/ML enthusiast with research publications.",
        },
        {
            "email": "vikram.singh@student.edu", "full_name": "Vikram Singh",
            "department": "Electronics", "cgpa": 7.8, "graduation_year": 2026,
            "skills": ["C++", "Python", "Embedded Systems", "Arduino", "MATLAB", "Linux"],
            "experience_years": 0.0, "bio": "Electronics eng. with embedded systems interest.",
        },
        {
            "email": "priya.krishnan@student.edu", "full_name": "Priya Krishnan",
            "department": "Computer Science", "cgpa": 8.9, "graduation_year": 2026,
            "skills": ["JavaScript", "TypeScript", "React", "Next.js", "Tailwind CSS", "MongoDB", "Node.js"],
            "experience_years": 1.0, "bio": "Frontend-focused full-stack developer.",
        },
        {
            "email": "rahul.joshi@student.edu", "full_name": "Rahul Joshi",
            "department": "Information Technology", "cgpa": 7.5, "graduation_year": 2027,
            "skills": ["Python", "Django", "Flask", "SQL", "Git", "Linux"],
            "experience_years": 0.0, "bio": "Backend developer learning cloud technologies.",
        },
        {
            "email": "ananya.das@student.edu", "full_name": "Ananya Das",
            "department": "Computer Science", "cgpa": 9.0, "graduation_year": 2026,
            "skills": ["Python", "Java", "React", "SQL", "Machine Learning", "Docker", "AWS"],
            "experience_years": 0.5, "bio": "Versatile developer with cloud and ML skills.",
        },
        {
            "email": "karan.mehta@student.edu", "full_name": "Karan Mehta",
            "department": "Mathematics", "cgpa": 8.7, "graduation_year": 2026,
            "skills": ["Python", "R", "Data Science", "Pandas", "Tableau", "SQL", "Statistics"],
            "experience_years": 0.5, "bio": "Math major passionate about data analytics.",
        },
    ]

    student_profiles = []
    for s in students_data:
        user = User(email=s["email"], password_hash=hash_password("student123"),
                    role="student", full_name=s["full_name"])
        db.add(user)
        db.commit()
        db.refresh(user)
        profile = StudentProfile(
            user_id=user.id, department=s["department"], cgpa=s["cgpa"],
            graduation_year=s["graduation_year"], skills=s["skills"],
            experience_years=s["experience_years"], bio=s["bio"],
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        student_profiles.append(profile)
        print(f"  ✅ Student: {s['email']} / student123")

    # ── Jobs ──
    jobs_data = [
        {
            "company_idx": 0, "title": "Full Stack Developer",
            "description": "Build and maintain scalable web applications using modern frameworks.",
            "requirements": "Strong programming skills, experience with web frameworks, cloud basics.",
            "required_skills": ["React", "Node.js", "SQL", "Docker", "Git"],
            "min_cgpa": 7.5, "experience_required": 0.0, "job_type": "Full-time",
            "location": "Bangalore, India", "salary_min": 800000, "salary_max": 1200000,
        },
        {
            "company_idx": 1, "title": "ML Engineer Intern",
            "description": "Work on cutting-edge ML models for natural language understanding.",
            "requirements": "Strong Python, ML fundamentals, familiarity with deep learning frameworks.",
            "required_skills": ["Python", "TensorFlow", "Machine Learning", "NLP", "Pandas"],
            "min_cgpa": 8.0, "experience_required": 0.0, "job_type": "Internship",
            "location": "Hyderabad, India", "salary_min": 30000, "salary_max": 50000,
        },
        {
            "company_idx": 2, "title": "Data Analyst",
            "description": "Analyze business data to provide actionable insights using visualization tools.",
            "requirements": "Analytical mindset, experience with data tools, SQL proficiency.",
            "required_skills": ["Python", "SQL", "Pandas", "Tableau", "Data Science"],
            "min_cgpa": 7.0, "experience_required": 0.0, "job_type": "Full-time",
            "location": "Mumbai, India", "salary_min": 600000, "salary_max": 900000,
        },
        {
            "company_idx": 3, "title": "Frontend Developer",
            "description": "Create beautiful, responsive web interfaces with modern CSS and JS frameworks.",
            "requirements": "Eye for design, proficiency in React/Vue, responsive design skills.",
            "required_skills": ["React", "JavaScript", "Tailwind CSS", "TypeScript", "Next.js"],
            "min_cgpa": 7.0, "experience_required": 0.5, "job_type": "Full-time",
            "location": "Pune, India", "salary_min": 700000, "salary_max": 1000000,
        },
        {
            "company_idx": 0, "title": "Backend Developer (Java)",
            "description": "Design and implement robust backend services in Java/Spring ecosystem.",
            "requirements": "Java proficiency, Spring Boot experience, database management.",
            "required_skills": ["Java", "Spring Boot", "PostgreSQL", "AWS", "Kubernetes"],
            "min_cgpa": 7.5, "experience_required": 0.0, "job_type": "Full-time",
            "location": "Bangalore, India", "salary_min": 900000, "salary_max": 1400000,
        },
        {
            "company_idx": 1, "title": "AI Research Intern",
            "description": "Conduct research in computer vision and publish findings.",
            "requirements": "Strong math foundation, research aptitude, deep learning experience.",
            "required_skills": ["Python", "PyTorch", "Deep Learning", "Computer Vision", "NLP"],
            "min_cgpa": 9.0, "experience_required": 0.5, "job_type": "Internship",
            "location": "Hyderabad, India", "salary_min": 40000, "salary_max": 60000,
        },
    ]

    job_objects = []
    for j in jobs_data:
        job = Job(
            company_id=company_profiles[j["company_idx"]].id,
            title=j["title"], description=j["description"],
            requirements=j["requirements"], required_skills=j["required_skills"],
            min_cgpa=j["min_cgpa"], experience_required=j["experience_required"],
            job_type=j["job_type"], location=j["location"],
            salary_min=j["salary_min"], salary_max=j["salary_max"],
            deadline=datetime.now(timezone.utc) + timedelta(days=30),
            status="active",
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        job_objects.append(job)
        print(f"  ✅ Job: {j['title']} @ {company_profiles[j['company_idx']].company_name}")

    # ── Sample Applications ──
    application_pairs = [
        (0, 0), (2, 1), (4, 0), (0, 3), (2, 5),  # Various student-job combos
        (1, 4), (6, 0), (7, 2), (3, 0), (5, 2),
        (4, 3), (6, 1), (0, 2), (7, 1), (1, 0),
    ]

    for stu_idx, job_idx in application_pairs:
        student = student_profiles[stu_idx]
        job = job_objects[job_idx]

        # Check for duplicate
        existing = db.query(Application).filter(
            Application.student_id == student.id,
            Application.job_id == job.id,
        ).first()
        if existing:
            continue

        result = rank_candidate(
            student_skills=student.skills or [],
            student_cgpa=student.cgpa,
            student_experience=student.experience_years,
            student_department=student.department,
            job_required_skills=job.required_skills or [],
            job_min_cgpa=job.min_cgpa,
            job_experience_required=job.experience_required,
            job_requirements=job.requirements or "",
        )

        # Assign diverse statuses
        statuses = ["applied", "applied", "shortlisted", "applied", "selected",
                     "applied", "shortlisted", "applied", "rejected", "applied",
                     "shortlisted", "applied", "applied", "shortlisted", "applied"]
        status = statuses[application_pairs.index((stu_idx, job_idx)) % len(statuses)]

        app = Application(
            student_id=student.id, job_id=job.id,
            status=status, ai_score=result["total_score"],
            ai_breakdown=result["breakdown"],
        )
        db.add(app)

    db.commit()
    print(f"  ✅ Created {len(application_pairs)} applications")

    # ── Sample Notifications ──
    for student in student_profiles[:4]:
        notif = Notification(
            user_id=student.user_id,
            message="Welcome to Campus Placement Portal! Complete your profile to get started.",
            type="info", link="/student/profile",
        )
        db.add(notif)

    for company in company_profiles[:2]:
        notif = Notification(
            user_id=company.user_id,
            message="New applications received! Check your dashboard.",
            type="success", link="/company/dashboard",
        )
        db.add(notif)

    db.commit()
    print("  ✅ Notifications created")

    print("\n🎉 Seeding complete!")
    print("\n📋 Login Credentials:")
    print("  Admin:    admin@campus.edu / admin123")
    print("  Company:  hr@techcorp.com / company123")
    print("  Student:  ria.sharma@student.edu / student123")


if __name__ == "__main__":
    seed()
    db.close()
