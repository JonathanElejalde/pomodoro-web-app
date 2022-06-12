from datetime import date, timedelta
import os
from tokenize import Token
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, status, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import EmailStr, SecretStr
from pypika import Table, MySQLQuery, Parameter

from credentials import ACCESS_TOKEN_EXPIRE_MINUTES
from data import Database
from models import ResponseUser, Token, UserLogin
from routers.utils import verify_password, create_access_token

# Constants
PWD_CXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
DB = Database()


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# User paths

@router.post(
    path="/signup", 
    #response_model= ResponseUser,
    status_code=status.HTTP_201_CREATED,
    summary="User registration"
)
def signup(
    email:EmailStr = Form(...), first_name:str = Form(..., min_length=1, max_length=255),
    last_name:str = Form(..., min_length=1, max_length=255), birth_date:date = Form(..., example=date.today()),
    password:SecretStr = Form(..., min_length=8)
):  
    # Get values
    hashed_passw = PWD_CXT.hash(password.get_secret_value())
    user_id = uuid4()
    values = (
        str(user_id), email, hashed_passw,
        first_name, last_name, birth_date
    )

    # Create placeholders
    placeholders = [Parameter('%s') for _ in range(len(values))]

    # Query
    users = Table('users')
    query = MySQLQuery.into(users).columns(
        users.user_id, users.email, users.password,
        users.first_name, users.last_name, users.birth_date
    ).insert(*placeholders)
    
    DB.execute_query(query.get_sql(), values)
    
    return {'Detail': "User created"}

@router.post(
    path="/login", 
    response_model= Token,
    status_code=status.HTTP_200_OK,
    summary="User login"
)
def login(auth_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    # Get email and password from request
    email = auth_data.username
    password = auth_data.password
    
    # Create query
    users = Table('users')
    query = MySQLQuery.from_(users).select(
        users.user_id, users.email, users.first_name,
        users.last_name, users.birth_date, users.password
    ).where(
        users.email == Parameter('%s')
    )
    # Create values
    values = (email,)

    # Get user that matches email
    user = DB.pandas_query(query.get_sql(), values)
    if user.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Email does not exists'
        )
    user = user.to_dict('records')[0]
    # Confirm password
    if not verify_password(
        password, user['password']
        ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password is incorrect'
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )

    # Save user_id in environment
    os.environ['USER_ID'] = user['user_id']

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    path="/",
    response_model=list[ResponseUser],
    status_code=status.HTTP_200_OK,
    summary="Get all users"
)
def get_users():
    users = Table('users')
    query = MySQLQuery.from_(users).select(
        users.user_id, users.email,
        users.first_name, users.last_name,
        users.birth_date
    )
    df = DB.pandas_query(query.get_sql())
    return df.to_dict('records')


@router.get(
    path="/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
    summary="Get specific user information"
)
def get_user():
    pass

@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="User deletion",
    tags=["Users"]
)
def delete_user(user_id:str):
    users = Table('users')
    query = MySQLQuery.from_(users).delete().where(
        users.user_id == Parameter('%s')
        )
    values = (user_id,)
    DB.execute_query(query.get_sql(), values)

    if DB.cursor.rowcount > 0:
        message = f"User ID {user_id} was deleted"
    elif DB.cursor.rowcount == 0:
        message = f"User ID does not exists"
    else:
        message = "Unexpected error occured"

    return {
        'Detail': message
    }
