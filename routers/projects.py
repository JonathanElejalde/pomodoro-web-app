from fastapi import APIRouter, status

from models import Project
from data import Database

# Constants
DB = Database()


router = APIRouter(
    prefix='/projects',
    tags=["Projects"]
)

# Project paths

@router.post(
    path="/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create project"
)
def create_project():
    pass


@router.get(
    path="/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Get project"
)
def get_project():
    pass

@router.get(
    path="/{project_ids}",
    response_model=list[Project],
    status_code=status.HTTP_200_OK,
    summary="Get projects"
)
def get_projects():
    pass


@router.put(
    path="/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Update project"
)
def update_project():
    pass


@router.delete(
    path="/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Delete project"
)
def delete_project():
    pass

@router.delete(
    path="/{project_ids}",
    response_model=list[Project],
    status_code=status.HTTP_200_OK,
    summary="Delete project"
)
def delete_projects():
    pass

