from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auth.dependencies import get_current_user
from database.db import Base, get_db
from database.models import User
from main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

with TestingSessionLocal() as db:
    db.add(User(id=1, username="tester", hashed_password="x"))
    db.commit()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return User(id=1, username="tester", hashed_password="x")


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)


def test_create_task_integration():
    response = client.post(
        "/tasks/",
        json={"title": "Новая задача", "description": "Тест"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Новая задача"
    assert data["description"] == "Тест"
    assert data["owner_id"] == 1
