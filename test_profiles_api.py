import pytest
from fastapi.testclient import TestClient
from main import app
from db import Base, engine
from profiles_model import Role
import uuid

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_create_profile_and_get():
    uid = str(uuid.uuid4())
    response = client.post("/profiles", params={
        "user_id": uid,
        "full_name": "Иван Иванов",
        "department": "Продажи",
        "role": Role.USER.value
    })
    assert response.status_code == 200
    profile_id = response.json()["id"]

    get_resp = client.get(f"/profiles/{uid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["full_name"] == "Иван Иванов"

def test_manager_sees_subordinates():
    manager_uid = str(uuid.uuid4())
    resp_mgr = client.post("/profiles", params={
        "user_id": manager_uid,
        "full_name": "Петр Менеджер",
        "department": "Продажи",
        "role": Role.MANAGER.value
    })
    manager_id = resp_mgr.json()["id"]

    sub_uid = str(uuid.uuid4())
    resp_sub = client.post("/profiles", params={
        "user_id": sub_uid,
        "full_name": "Сергей Подчинённый",
        "department": "Продажи",
        "role": Role.USER.value,
        "manager_id": manager_id
    })
    assert resp_sub.status_code == 200

    resp_list = client.get(f"/profiles/{manager_id}/subordinates")
    assert resp_list.status_code == 200
    subs = resp_list.json()
    assert len(subs) == 1
    assert subs[0]["full_name"] == "Сергей Подчинённый"