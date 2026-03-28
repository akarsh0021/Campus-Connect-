from database import SessionLocal
from models.user import User
from services.auth_service import hash_password, verify_password

def test_user():
    db = SessionLocal()
    # Find the newly created user (last user or specific email)
    user = db.query(User).order_by(User.id.desc()).first()
    print("Latest user:", user.email)
    print("Hash:", user.password_hash)
    # try testing the verification
    # we don't know their password, let's create a temporary hash and verify
    hashed = hash_password("test_password123")
    valid = verify_password("test_password123", hashed)
    print("Self-test verify:", valid)
    
if __name__ == "__main__":
    test_user()
