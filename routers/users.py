from datetime import date, timedelta
import os
from tokenize import Token
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, status, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import EmailStr, SecretStr
from pypika import Table, Parameter

from config import settings
from data import DB
from models import ResponseUser, Token
import queries
from routers.utils import verify_password, create_access_token, get_current_user, delete_message

# Constants
PWD_CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS = Table("users")


router = APIRouter(prefix="/users", tags=["Users"])

# User paths


@router.post(
    path="/signup", status_code=status.HTTP_201_CREATED, summary="User registration"
)
def signup(
    request: Request,
    email: EmailStr = Form(...),
    first_name: str = Form(..., min_length=1, max_length=255),
    last_name: str = Form(..., min_length=1, max_length=255),
    birth_date: date = Form(..., example=date.today()),
    password: SecretStr = Form(..., min_length=8),
):
    # Get values
    hashed_passw = PWD_CXT.hash(password.get_secret_value())
    user_id = uuid4()
    values = (str(user_id), email, hashed_passw, first_name, last_name, birth_date)

    columns = [
        USERS.user_id, USERS.email, USERS.password,
        USERS.first_name, USERS.last_name, USERS.birth_date,
    ]

    query = queries.insert_query(USERS, columns)
    DB.execute_query(query.get_sql(), values)

    return {
        "Detail": "User created",
        "User Data": {
            "user_id": user_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date
        }
        }


@router.post(
    path="/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User login",
)
def login(auth_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    # Get email and password from request
    email = auth_data.username
    password = auth_data.password
    
    # Generate query
    columns = [
        USERS.user_id, USERS.email, USERS.first_name,
        USERS.last_name, USERS.birth_date, USERS.password,
    ]
    condition = (USERS.email == Parameter("%s"))
    query = queries.select_query(USERS, columns, condition)

    # Create values
    values = (email,)

    # Get user that matches email
    user = DB.pandas_query(query.get_sql(), values)
    if user.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email does not exists"
        )
    user = user.to_dict("records")[0]
    # Confirm password
    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect"
        )

    # If user authenticas correctly, create an access token.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.delete(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Delete logged user",
    tags=["Users"],
)
def delete_user(current_user: ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    
    # Generate query
    delete_condition = (USERS.user_id == Parameter("%s"))
    query = queries.delete_query(USERS, delete_condition)
    values = (user_id,)

    DB.execute_query(query.get_sql(), values)
    message = delete_message(DB)

    return {"Detail": message}


# ADMIN ENDPOINT

# @router.get(
#     path="/",
#     response_model=list[ResponseUser],
#     status_code=status.HTTP_200_OK,
#     summary="Get all users",
# )
# def get_users():
#     users = Table("users")
#     query = MySQLQuery.from_(users).select(
#         users.user_id, users.email, users.first_name, users.last_name, users.birth_date
#     )
#     df = DB.pandas_query(query.get_sql())
#     return df.to_dict("records")

# ADMIN ENDPOINT

# @router.get(
#     path="/{user_id}",
#     response_model=ResponseUser,
#     status_code=status.HTTP_200_OK,
#     summary="Get specific user information",
# )
# def get_user():
#     pass

# Admin endpoint

# @router.delete(
#     path="/{user_id}",
#     status_code=status.HTTP_200_OK,
#     summary="Delete user by id",
#     tags=["Users"],
# )
# def delete_user(user_id):
#      pass