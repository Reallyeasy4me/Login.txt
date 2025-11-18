from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from user_repo import UserRepo
from user import UserRole

auth_router = APIRouter(tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register")
def register(email: str, password: str, role: UserRole = UserRole.USER, db: Session = Depends(get_db)):
    repo = UserRepo(db)
    if repo.get_by_email(email):
        raise HTTPException(400, "Email already registered")
    user = repo.create_user(email, password, role)
    return {"msg": "User registered", "user_id": str(user.id)}

@auth_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    repo = UserRepo(db)
    user = repo.get_by_email(email)
    if not user or not repo.verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return {"msg": "Login successful", "role": user.role}