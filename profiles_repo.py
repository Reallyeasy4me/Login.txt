from sqlalchemy.orm import Session
from profiles_model import Profile, Role

class ProfilesRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, user_id, full_name, department, role: Role, manager_id=None):
        profile = Profile(
            user_id=user_id,
            full_name=full_name,
            department=department,
            role=role,
            manager_id=manager_id
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile(self, user_id):
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()

    def get_subordinates(self, manager_id):
        return self.db.query(Profile).filter(Profile.manager_id == manager_id).all()

    def get_all_profiles(self):
        return self.db.query(Profile).all()