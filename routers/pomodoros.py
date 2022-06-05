from fastapi import APIRouter, status

from models import Pomodoro
from data import Database

# Constants
DB = Database()


router = APIRouter(
    prefix='/pomodoros',
    tags=["Pomodoros"]
)


# Pomodoro paths
@router.post(
    path="/",
    response_model=Pomodoro,
    status_code=status.HTTP_201_CREATED,
    summary="Create pomodoro"
)
def create_pomodoro():
    pass

@router.get(
    path="/{pomodoro_id}",
    response_model=Pomodoro,
    status_code=status.HTTP_200_OK,
    summary="Get pomodoro"
)
def get_pomodoro():
    pass

@router.get(
    path="/{pomodoro_ids}",
    response_model=list[Pomodoro],
    status_code=status.HTTP_200_OK,
    summary="Get pomodoros"
)
def get_pomodoros():
    pass
