from tests_setup import * # just a comment
from database import SessionLocal
from models.user import User
from services.auth_service import create_access_token
from passlib.context import CryptContext # wait we use bcrypt
import requests

def test_get_me():
    db = SessionLocal()
    user = db.query(User).order_by(User.id.desc()).first()
    token = create_access_token({"sub": user.id})
    print("Token created.")
    
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("http://127.0.0.1:8000/api/auth/me", headers=headers)
    print("Status:", r.status_code)
    print("Body:", r.text)

if __name__ == "__main__":
    test_get_me()
