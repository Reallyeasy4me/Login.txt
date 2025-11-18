from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    id: str
    email: EmailStr
    hashed_password: str
    role: UserRole

    @staticmethod
    def generate_id():
        return str(uuid4())