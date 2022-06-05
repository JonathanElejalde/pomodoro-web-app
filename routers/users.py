from datetime import date
from uuid import uuid4

from fastapi import APIRouter, status, Form
from passlib.context import CryptContext
from pydantic import EmailStr, SecretStr
from pypika import Table, MySQLQuery, Parameter

from models import ResponseUser
from data import Database

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
    hashed_passw = PWD_CXT.hash(str(password))
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
    response_model= ResponseUser,
    status_code=status.HTTP_200_OK,
    summary="User login"
)
def login():
    pass

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
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
    summary="User deletion",
    tags=["Users"]
)
def delete_user():
    pass

@router.put(
    path="/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
    summary="User update",
    tags=["Users"]
)
def update_user():
    pass