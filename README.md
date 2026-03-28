# 🎓 CampusConnect: AI-Powered Campus Placement Portal

CampusConnect is a modern, full-stack web application designed to bridge the gap between university students and top recruiters. It automates the recruitment workflow by parsing resumes, analyzing candidate skills mathematically, and generating ranked **AI Match Scores** for every job posting.



## 🚀 Key Features

*   **Role-Based Access Control:** Separate, secure dashboard portals for **Students**, **Companies**, and the University **Admin**.
*   **AI Resume Parsing:** Students upload their PDF resumes, and the backend NLP engine automatically extracts their technical skills using `pdfplumber` and predefined skill dictionaries.
*   **Smart Job Match Engine:** A built-in mathematical matching algorithm evaluates a student's parsed skills, CGPA, and experience against the requirements set by a recruiter, providing a localized "Match Score" (from 0-100%).
*   **Live Analytics:** An administrative dashboard built with Recharts displaying total system placements, active users, and real-time tech skill demands across all job listings.
*   **Premium UI:** A fully custom "Glassmorphism" interface built with React, pure CSS variables, dynamic backgrounds, and smooth micro-animations.

## 🛠️ Technology Stack

*   **Frontend Client:** React 18, Vite, React Router DOM, Axios, Lucide-React Icons.
*   **Backend Server:** Python, FastAPI, SQLAlchemy (ORM), Pydantic Schemas.
*   **Security:** JWT (JSON Web Tokens), Role-Based Auth validation, and direct Bcrypt password hashing.
*   **Database:** Local SQLite (`campus_portal.db`).

## ⚙️ How to Run Locally

### 1. Start the FastAPI Backend
Navigate to the `backend` directory, activate the Python virtual environment, and start the local server:
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python seed.py          # Populates database with dummy data
python -m uvicorn main:app --reload
```
*The backend will run on `http://127.0.0.1:8000`*

### 2. Start the React Frontend
Open a **new terminal tab**, navigate to the `frontend` directory, install the required packages, and run Vite:
```bash
cd frontend
npm install
npm run dev
```
*The frontend will boot up instantly on `http://localhost:5173`*

## 🧑‍💻 Contributing & Testing
- Login to the Admin panel using `admin@campus.edu` | `admin123` to oversee the platform.
- Login to the Student panel using `ria.sharma@student.edu` | `student123` to upload a resume and test matching.
- Login to the Company panel using `hr@techcorp.com` | `company123` to post dummy jobs and review ranked candidate matches.

---
*Built from scratch as an end-to-end full-stack portfolio project.*
