from datetime import date, datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID
from pandas import NA

from pydantic import BaseModel, Field, EmailStr, SecretStr

# Constants
ID = Field(..., gt=0, example=1)
NAME = Field(..., min_length=1, max_length=255)

# Enums
class PomSatisfaction(Enum):
    missing = "missing"
    good = "good"
    bad = "bad"
    not_qualified_yet = ""

class Satisfaction(Enum):
    good = "good"
    bad = "bad"

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
    pass

class CategoryResponse(CategoryBase):
    category_id: int = ID



# Project models
class ProjectBase(BaseModel):
    project_name: str = NAME

class Project(ProjectBase):
    category_id: int = ID

class ProjectResponse(ProjectBase):
    project_id: int = ID
    category_id: int = ID
    category_name: str = NAME
    start: date = Field(...)
    end: Optional[date] = Field(default=None)
    canceled: Optional[date] = Field(default=None)


# Pomodoro models
class PomodoroBase(BaseModel):
    duration: int = Field(..., ge=25)

class Pomodoro(PomodoroBase):
    project_id: int = ID
    category_id: int = ID

class PomodoroResponse(PomodoroBase):
    pomodoro_id: int = ID
    pomodoro_date: datetime = Field(...)
    project_name: str = NAME
    category_name: str = NAME
    pomodoro_satisfaction: PomSatisfaction


# Recall project models
class RecallProjectBase(BaseModel):
    project_name: str = NAME

class RecallProject(RecallProjectBase):
    pass

class RecallProjectResponse(RecallProjectBase):
    recall_project_id: int = ID
    project_name: str



# Recall models
class RecallProjectNames(BaseModel):
    project_name: str = NAME

class RecallBase(BaseModel):
    project_name: str = NAME
    recall_title: str = Field(..., max_length=255)
    recall: str = Field(...)
    

class Recall(RecallBase):
    pass

class RecallResponse(RecallBase):
    recall_id: int = ID
    
    
    


# JWT token models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str,None] = None
    