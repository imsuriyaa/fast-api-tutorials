from typing import Optional, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from models import Todos
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
from .auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/todos",
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

templates = Jinja2Templates(directory="templates")


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
        
    except:
        return redirect_to_login()



@router.get('/add-todo-page')
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except:
        return redirect_to_login()


@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(db: db_dependency, request: Request, todo_id: int = Path(gt=0)):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo_model, "user": user})
    except:
        return redirect_to_login()




### Endpoints ###

@router.post('/todo', status_code=status.HTTP_201_CREATED)
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



