"""Application configuration."""
import os

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "campus-portal-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Load environment variables — use absolute path so .env is always found
# regardless of which directory VS Code or the terminal is launched from
from dotenv import load_dotenv
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=_env_path)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campus_portal.db")

# Upload settings
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CORS
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
]
