from fastapi import FastAPI
from database import engine, Base
from routers import todos, auth, users, admin

# Create all the tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
