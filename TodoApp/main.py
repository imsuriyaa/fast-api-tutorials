from fastapi import FastAPI, status, Request
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Create database without writing any SQL query
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates")
app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')

@app.get('/')
def test(request: Request):
    # request is a protocal that we have to follow
    return RedirectResponse(url='/todos/todo-page')


@app.get('/healthy', status_code=status.HTTP_200_OK)
def check_health():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
