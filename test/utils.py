from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from models import Todos, Users
from routers.auth import bcrypt_context


client = TestClient(app)

SQLALCHEMY_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

async def override_get_current_user():
    return {"username": "testuser", "id": 1, "role": "admin"}

async def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to Code", 
        description="Practice every day", 
        priority=5, 
        complete=False, 
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="testuser",
        email="testuser@test.com",
        hashed_password=bcrypt_context.hash("testpassword"),
        first_name="Test",
        last_name="User",
        role="admin",
        phone_number="1234567890"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()

