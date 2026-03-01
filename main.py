from fastapi import FastAPI, Request, status
from database import engine, Base
from routers import todos, auth, users, admin
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


# Create all the tables in the database
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def read_root(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
