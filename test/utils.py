from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from models import Todos

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
    yield db
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()



