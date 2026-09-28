import hashlib
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "employee-management-demo-secret-change-me"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash

def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
