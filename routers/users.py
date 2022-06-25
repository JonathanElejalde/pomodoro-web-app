from datetime import date, timedelta
from tokenize import Token
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, status, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mysql.connector.errors import IntegrityError
from passlib.context import CryptContext
from pydantic import EmailStr, SecretStr
from pypika import Table, Parameter

from config import settings
from data import DB
from models import ResponseUser, Token
import queries
from utils import verify_password, create_access_token, get_current_user, delete_message

# Constants
PWD_CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS = Table("users")

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/users", tags=["Users"])

# User paths

@router.get(
    path="/signup", summary="User registration"
)
def register(request: Request):
    return templates.TemplateResponse("users/signup.html", {"request": request})



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
    try:
        DB.execute_query(query.get_sql(), values)
        return RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            ) 
    except IntegrityError:
        errors = ["User already in database"]
        return templates.TemplateResponse("users/signup.html", context={"request": request, "errors": errors})


@router.get(
    path="/login",
    summary="User login"
)
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
    summary="User login",
    response_model=Token
)
def login_for_token(response: Response, request: Request, auth_data: OAuth2PasswordRequestForm = Depends()):
    # Get email and password from request
    errors = []
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
        errors.append("Email does not exists")
        return templates.TemplateResponse("auth/login.html", context={"request": request, "errors": errors})

    user = user.to_dict("records")[0]
    # Confirm password
    if not verify_password(password, user["password"]):
        errors.append("Wrong password")
        return templates.TemplateResponse("auth/login.html", context={"request": request, "errors": errors})

    # If user authenticas correctly, create an access token.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    # Set HttpOnly cookie in response
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)

    #return templates.TemplateResponse("auth/login.html", context={"request": request, "msg": "Login Successful!"})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="User login",
)
def login(response: Response, request: Request, auth_data: OAuth2PasswordRequestForm = Depends()):

    login_for_token(response, request, auth_data)
    return templates.TemplateResponse("auth/login.html", context={"request": request, "msg": "Login Successful!"})



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

