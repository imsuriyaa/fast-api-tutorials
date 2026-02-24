from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
from .auth import get_current_user
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, HTTPException, status
from .auth import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["users"]
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


class UserPasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class UserPhoneNumberChangeRequest(BaseModel):
    current_phone_number: str
    new_phone_number: str


@router.get('/')
def read_user_data(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    return {
        'username': user_model.username,
        'email': user_model.email,
        'first_name': user_model.first_name,
        'last_name': user_model.last_name,
        'role': user_model.role,
        'phone_number': user_model.phone_number
    }

@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db: db_dependency, user_request: UserPasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_request.current_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)
    db.add(user_model)
    db.commit()
    return


@router.put('/change-phone-number', status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(user: user_dependency, db: db_dependency, user_request: UserPhoneNumberChangeRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    print(user_model.phone_number)

    if user_request.current_phone_number != user_model.phone_number and user_model.phone_number:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    user_model.phone_number = user_request.new_phone_number
    db.add(user_model)
    db.commit()
    return

