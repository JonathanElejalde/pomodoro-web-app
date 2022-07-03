from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException

from models import Project, ProjectResponse, ResponseUser
from data import DB
import query as q
from utils import get_current_user, delete_message

router = APIRouter(
    prefix='/projects',
    tags=["Projects"]
)

# Project paths

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create project"
)
def create_project(project:Project, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    start = datetime.today()
    values = (user_id, project.category_id, project.project_name, start)
    query = q.create_project()

    # Execute query
    DB.execute_query(query, values)

    return {"details": f"Project {project.project_name} was created sucessfully"}


@router.get(
    path="/",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get projects"
)
def get_projects(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id)
    df = q.get_projects(values)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are not projects in this category"
        )

    return df.to_dict('records')
    

@router.get(
    path="/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Get project"
)
def get_project(category_id: int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id, project_id)
    df = q.get_projects(values, project_id)
    
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This project does not exists"
        )
    project = df.to_dict('records')[0]

    return project


@router.put(
    path="/{project_id}/end",
    status_code=status.HTTP_200_OK,
    summary="Finish a project"
)
def update_project(category_id:int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    end = datetime.today().date()
    values = (end, category_id, project_id, user_id)
    query = q.update_project('end')

    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"The end date for project {project_id} has been updated to {end}"
    }

@router.put(
    path="/{project_id}/canceled",
    status_code=status.HTTP_200_OK,
    summary="Cancel a project"
)
def update_project(category_id:int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    canceled = datetime.today().date()
    values = (canceled, category_id, project_id, user_id)
    query = q.update_project('canceled')
    
    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"The canceled date for project {project_id} has been updated to {canceled}"
    }


@router.put(
    path="/{project_id}/name",
    status_code=status.HTTP_200_OK,
    summary="Cancel a project"
)
def update_project(category_id:int, project_id:int, new_project_name:str, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (new_project_name, category_id, project_id, user_id)
    query = q.update_project('project_name')
    
    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"The project_name of project:{project_id} has been updated to {new_project_name}"
    }


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete project"
)
def delete_project(category_id:int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (category_id, project_id, user_id)
    query = q.delete_project()
    
    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"Project {project_id} was deleted"
    }



# @router.delete(
#     path="/{project_ids}",
#     response_model=list[Project],
#     status_code=status.HTTP_200_OK,
#     summary="Delete project"
# )
# def delete_projects():
#     pass

