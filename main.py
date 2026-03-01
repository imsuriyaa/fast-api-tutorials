from fastapi import FastAPI, Request
from database import engine, Base
from routers import todos, auth, users, admin
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Create all the tables in the database
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 'title': 'FASTAPI Todo - Home'})

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
