from fastapi import APIRouter, status

from models import Recall
from data import Database

# Constants
DB = Database()


router = APIRouter(
    prefix='/recalls',
    tags=["Recalls"]
)

# Recall paths
@router.post(
    path="/",
    response_model=Recall,
    status_code=status.HTTP_201_CREATED,
    summary="Recall creation"
)
def create_recall():
    pass

@router.get(
    path="/{recall_id}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Get recall"
)
def get_recall():
    pass

@router.get(
    path="/{recall_ids}",
    response_model=list[Recall],
    status_code=status.HTTP_200_OK,
    summary="Get recalls"
)
def get_recalls():
    pass

@router.put(
    path="/{recall_ids}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Update recalls"
)
def update_recalls():
    pass

@router.delete(
    path="/{recall_id}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Delete recall"
)
def delete_recall():
    pass

@router.delete(
    path="/{recall_ids}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Delete recalls"
)
def delete_recalls():
    pass
