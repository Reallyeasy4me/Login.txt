import os
import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db import Base

class Role(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

# помогатор: в тестовом режиме — String, иначе UUID
def uuid_column(nullable=False, fk=None):
    if os.getenv("TESTING", "0") == "1":  # тесты / SQLite
        return Column(String, ForeignKey(fk) if fk else None, nullable=nullable)
    else:  # прод / PostgreSQL
        return Column(UUID(as_uuid=True), ForeignKey(fk) if fk else None, nullable=nullable)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = uuid_column(nullable=False)
    full_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    manager_id = uuid_column(nullable=True, fk="profiles.id")