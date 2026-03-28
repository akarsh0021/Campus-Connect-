"""
Campus Placement Portal — FastAPI Backend
Main application entry point with routing, CORS, and DB initialization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
from config import CORS_ORIGINS, UPLOAD_DIR

# Import all models so they are registered with Base
from models import User, StudentProfile, CompanyProfile, Job, Application, Notification

# Import routers
from routers.auth import router as auth_router
from routers.students import router as students_router
from routers.companies import router as companies_router
from routers.jobs import router as jobs_router
from routers.applications import router as applications_router
from routers.admin import router as admin_router
from routers.notifications import router as notifications_router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Campus Placement Portal API",
    description="AI-powered campus recruitment platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploaded resumes
if os.path.exists(UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Register routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(companies_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(admin_router)
app.include_router(notifications_router)


@app.get("/")
def root():
    return {
        "name": "Campus Placement Portal API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
