from database import SessionLocal
from models.user import User
from services.auth_service import create_access_token, get_current_user
from datetime import datetime, timezone, timedelta
from jose import jwt

def test_token():
    # 1. Manually create token and decode to check if expiration is valid
    secret = "campus-portal-super-secret-key-change-in-production"
    algo = "HS256"
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode = {"sub": 1, "exp": expire}
    
    token = jwt.encode(to_encode, secret, algorithm=algo)
    print("Encoded token:", token)
    
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
        print("Decoded payload:", payload)
    except Exception as e:
        print("Decode error:", e)

if __name__ == "__main__":
    test_token()
