from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Depends, HTTPException
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

from models import Todos, Users
from database import SessionLocal


router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class PhoneNumberVerification(BaseModel):
    phone_number: str = Field(min_length=10, max_length=10)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency, user: user_dependency, user_verification: UserVerification):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not user_model:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()

    return user_model



@router.put('/phone_number', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(db: db_dependency, user: user_dependency, phone_number_verification: PhoneNumberVerification):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not user_model:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    user_model.phone_number = phone_number_verification.phone_number
    db.commit()

    return user_model

