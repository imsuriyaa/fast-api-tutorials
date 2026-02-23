from fastapi import FastAPI
import models
from database import engine
from routers import todos, auth, users

# Create all the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
