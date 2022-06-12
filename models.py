from datetime import date, datetime
from enum import IntEnum
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, SecretStr

# Constants
ID = Field(..., gt=0, example=1)
NAME = Field(..., min_length=1, max_length=255)

# Enums
class PomSatisfaction(IntEnum):
    good = 1
    bad = 2

# User models
class BaseUser(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = NAME
    last_name: str = NAME
    birth_date: Optional[date] = Field(default=None)

class RegisterUser(BaseUser):
    password: SecretStr = Field(..., min_length=8)

class UserLogin(BaseUser):
    password: str = Field(..., min_length=8)

class ResponseUser(BaseUser):
    user_id: UUID = Field(...)


# Category models
class CategoryBase(BaseModel):
    category_name: str = NAME

class Category(CategoryBase):
    user_id: UUID = Field(...)

class CategoryResponse(CategoryBase):
    category_id: int = ID



# Project models
class Project(BaseModel):
    project_id: int = ID
    user_id: UUID = Field(...)
    category_id: int = ID
    project_name: str = NAME
    start: date = Field(...)
    end: Optional[date] = Field(default=None)
    canceled: Optional[date] = Field(default=None)


# Pomodoro models
class Pomodoro(BaseModel):
    pomodoro_id: int = ID
    project_id: int = ID
    user_id: UUID = Field(...)
    category_id: int = ID
    duration: int = Field(..., ge=25)
    pomodoro_date: datetime = Field(...)
    pomodoro_satisfaction: PomSatisfaction = Field(...)


# Recall models
class Recall(BaseModel):
    recall_id: int = ID
    user_id: UUID = Field(...)
    project_name: str = NAME
    recall: str = Field(...)
    recall_title: str = Field(..., max_length=255)

# JWT token models

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str,None] = None
    