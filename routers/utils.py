from datetime import datetime, timedelta
import os
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from credentials import SECRET_KEY, ALGORITHM
from models import TokenData

# General utils

def get_user_id():
    user_id = os.getenv('USER_ID')

    return user_id

def delete_message(db):
    if db.cursor.rowcount > 0:
        message = f"Deletion was successfull"
    elif db.cursor.rowcount == 0:
        message = f"There were not delitions"
    else:
        message = "Unexpected error occured"

    return message

# User utils

PWD_CXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_pass, hashed_pass):
    return PWD_CXT.verify(plain_pass, hashed_pass)


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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, credentials_exception)
    return token_data
