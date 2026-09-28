from fastapi import APIRouter, HTTPException
from ..schemas import UserCreate, UserLogin
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
USERS = {}

@router.post("/register")
def register(user: UserCreate):
    if user.username in USERS:
        raise HTTPException(400, "Username already exists")
    USERS[user.username] = hash_password(user.password)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    stored = USERS.get(user.username)
    if not stored or not verify_password(user.password, stored):
        raise HTTPException(401, "Invalid username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
