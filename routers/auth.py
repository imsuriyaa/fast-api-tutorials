import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from models import Users
from typing import Annotated
from database import SessionLocal
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
# comes with python-multipart package
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# run openssl rand -hex 32 in terminal to generate a secret key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

templates = Jinja2Templates(directory="templates")

# Pages

@router.get('/login-page')
async def login_page(request: Request):
    if request.cookies.get('access_token'):
        user = await get_current_user(request.cookies.get('access_token'))
        if user:
            return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, 'title': 'FASTAPI Todo - Login'})


@router.get('/register-page')
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, 'title': 'FASTAPI Todo - Register'})

# EndPoints


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Depends - it is a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    email: str = Field(min_length=3)
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str
    password: str = Field(min_length=7)
    role: str = Field(min_length=3)
    phone_number: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    to_encode = {"username": username, "id": user_id, "role": role}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@router.post('/')
def create_user(db: db_dependency, user: CreateUserRequest):
    # **user.dict() cannot be used as CreateUserRequest doesn't hvae hashed_password it has password
    create_user_model = Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role,
        is_active=True,
        phone_number=user.phone_number
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


@router.post('/token', response_model=TokenResponse)
def get_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}




