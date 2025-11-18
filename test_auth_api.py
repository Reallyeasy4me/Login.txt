import pytest
from fastapi.testclient import TestClient
from main import app
from db import Base, engine

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_register_and_login():
    # Регистрация
    response = client.post("/register", params={
        "email": "user@mail.com",
        "password": "pass123",
        "role": "user"
    })
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data

    # Логин
    response = client.post("/login", params={
        "email": "user@mail.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "Login successful"