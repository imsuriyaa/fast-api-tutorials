from fastapi import FastAPI, status
import models
from database import engine
from routers import auth, todos, admin, users

app = FastAPI()

# Create database without writing any SQL query
models.Base.metadata.create_all(bind=engine)


@app.get('/healthy', status_code=status.HTTP_200_OK)
def check_health():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
