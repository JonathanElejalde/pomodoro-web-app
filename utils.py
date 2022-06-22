from curses.ascii import US
from datetime import datetime, timedelta
import os
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pandas import DataFrame
from passlib.context import CryptContext
from pypika import Table, Parameter

from config import settings
from data import DB
from models import TokenData, ResponseUser
import queries

# General utils

def delete_message(db):
    if db.cursor.rowcount > 0:
        message = f"Deletion was successfull"
    elif db.cursor.rowcount == 0:
        message = f"There were not deletions"
    else:
        message = "Unexpected error occured"

    return message

# User utils

PWD_CXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
USERS = Table("users")

def verify_password(plain_pass, hashed_pass):
    return PWD_CXT.verify(plain_pass, hashed_pass)


def select_user(email:str)-> DataFrame:

    # Generate query
    columns = [
        USERS.user_id, USERS.email, USERS.first_name,
        USERS.last_name, USERS.birth_date
    ]
    condition = (USERS.email == Parameter("%s"))
    query = queries.select_query(USERS, columns, condition)
    values = (email, )
    user = DB.pandas_query(query.get_sql(), values)

    return user

# Pomodoros utils

def get_satisfaction_int(satisfaction):
    satisfaction_dict = {
        "good": 1,
        "bad": 2
    }

    value = satisfaction_dict.get(satisfaction)

    if not value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Pomodoro satisfaction has to be either 'good' or 'bad' currently it is {satisfaction}",
            )
    return value
    

# JWT token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def create_access_token(
    data: dict, expires_delta:Union[timedelta, None] = None
    ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    return email

def get_current_user(token:str = Depends(oauth2_scheme)) -> ResponseUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_token(token, credentials_exception)
    user = select_user(email)

    if user.empty:
        raise credentials_exception

    return user.to_dict('records')[0]
