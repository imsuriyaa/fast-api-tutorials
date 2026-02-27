from typing import Optional, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix="/todo",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Depends - it is a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)



@router.post('/', status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoRequest, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = Todos(**todo.dict(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    return {"message": "Todo created successfully"}

@router.get('/', status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    return todos

@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.put('/{todo_id}', status_code=status.HTTP_200_OK)
def update_todo(user: user_dependency, todo: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return {"message": "Todo updated successfully"}
        

@router.delete('/{todo_id}', status_code=status.HTTP_200_OK)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return {"message": "Todo deleted successfully"}



