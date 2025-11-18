import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, DBUser
from user import UserRole
from user_repo import UserRepo

# Создаём in-memory SQLite для unit-тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_user(db_session):
    repo = UserRepo(db_session)
    user = repo.create_user("test@example.com", "password123", UserRole.USER)
    assert user.email == "test@example.com"
    assert repo.verify_password("password123", user.hashed_password) is True

def test_get_by_email(db_session):
    repo = UserRepo(db_session)
    repo.create_user("email@example.com", "pass", UserRole.USER)
    user = repo.get_by_email("email@example.com")
    assert user is not None
    assert user.email == "email@example.com"