import datetime
from enum import IntEnum
from pandas import NA

from pydantic import BaseModel, Field, EmailStr


ID = Field(..., gt=0, example=1)
NAME = Field(..., min_length=1)

class PomSatisfaction(IntEnum):
    good = 1
    bad = 2

class User(BaseModel):
    user_id: int = ID
    email: EmailStr
    password: str

class Category(BaseModel):
    category_id: int = ID
    category_name: str = NAME
    user_id: int = ID

class Project(BaseModel):
    project_id: int = ID
    user_id: int = ID
    category_id: int = ID
    project_name: str = NAME
    start: datetime.date = Field(...)
    end: datetime.date
    canceled: datetime.date

class Pomodoro(BaseModel):
    pomodoro_id: int = ID
    project_id: int = ID
    user_id: int = ID
    category_id: int = ID
    duration: int = Field(..., ge=25)
    pomodoro_date: datetime.datetime
    pomodoro_satisfaction: PomSatisfaction

class Recall(BaseModel):
    recall_id: int = ID
    user_id: int = ID
    project_name: str = NAME
    recall: str
    recall_title: str = Field(..., max_length=255)

