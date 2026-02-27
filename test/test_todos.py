from routers.todos import get_db, get_current_user
from fastapi import status
from models import Todos
from .utils import *

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_read_all_todos(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'title': 'Learn to Code',
        'description': 'Practice every day',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]


def test_read_todo_by_user(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'Learn to Code',
        'description': 'Practice every day',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }


def test_read_todo_not_found():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found'
    }


def test_create_todo(test_todo):
    request_todo = {
        "title": "Learn to Concentrate",
        "description": "Practice Mindfulness",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.post("/todo", json=request_todo)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "Todo created successfully"
    }
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 2).first()
    assert todo_model.title == request_todo.get("title")
    assert todo_model.description == request_todo.get("description")
    assert todo_model.priority == request_todo.get("priority")
    assert todo_model.complete == request_todo.get("complete")
    assert todo_model.owner_id == request_todo.get("owner_id")



def test_update_todo(test_todo):
    request_todo = {
        "title": "Learn to Concentrate",
        "description": "Practice Mindfulness",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.put("/todo/1", json=request_todo)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Todo updated successfully"}
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model.title == request_todo.get("title")
    assert todo_model.description == request_todo.get("description")
    assert todo_model.priority == request_todo.get("priority")
    assert todo_model.complete == request_todo.get("complete")
    assert todo_model.owner_id == request_todo.get("owner_id")
    

def test_update_todo_not_found(test_todo):
    request_todo = {
        "title": "Learn to Concentrate",
        "description": "Practice Mindfulness",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.put("/todo/999", json=request_todo)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Todo not found"
    }

def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Todo deleted successfully"}
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Todo not found"
    }
