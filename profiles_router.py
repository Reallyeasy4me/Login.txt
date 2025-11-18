from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from profiles_repo import ProfilesRepo
from profiles_model import Role

profiles_router = APIRouter(tags=["Profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@profiles_router.post("/profiles")
def create_profile(user_id: str, full_name: str, department: str, role: Role, manager_id: str = None, db: Session = Depends(get_db)):
    repo = ProfilesRepo(db)
    profile = repo.create_profile(user_id, full_name, department, role, manager_id)
    return profile

@profiles_router.get("/profiles/{user_id}")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    repo = ProfilesRepo(db)
    profile = repo.get_profile(user_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile

@profiles_router.get("/profiles/{manager_id}/subordinates")
def get_subordinates(manager_id: str, db: Session = Depends(get_db)):
    repo = ProfilesRepo(db)
    subordinates = repo.get_subordinates(manager_id)
    return subordinates