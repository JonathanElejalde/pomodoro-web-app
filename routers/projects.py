from datetime import date, datetime

from fastapi import APIRouter, status, Depends, HTTPException
from pypika import Tables, MySQLQuery, Parameter

from models import Project, ProjectResponse, ResponseUser
from data import Database
import queries
from routers.utils import get_current_user, get_user_id, delete_message

# Constants
DB = Database()
PROJECTS, CATEGORIES = Tables('projects', 'categories')


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
    user_id = get_user_id()

    # Generate query
    columns = [
        PROJECTS.user_id, PROJECTS.category_id, 
        PROJECTS.project_name, PROJECTS.start
    ]
    query = queries.insert_query(PROJECTS, columns)

    # Generate values
    start = datetime.today()
    values = (user_id, project.category_id, project.project_name, start)

    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {"details": f"Project {project.project_name} was created sucessfully"}


@router.get(
    path="/",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get projects"
)
def get_projects(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    on_fields = ('category_id', 'user_id')
    columns = [
        PROJECTS.project_id, PROJECTS.category_id,
        CATEGORIES.category_name, PROJECTS.project_name,
        PROJECTS.start, PROJECTS.end, PROJECTS.canceled
    ]
    condition = (
        (PROJECTS.user_id == Parameter('%s')) & (PROJECTS.category_id == Parameter('%s'))
    )
    query = queries.select_join_query(
        PROJECTS, CATEGORIES, on_fields,
        columns, condition
    )

    # Generate values
    values = (user_id, category_id)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)
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
def get_project(project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    on_fields = ('category_id', 'user_id')
    columns = [
        PROJECTS.project_id, PROJECTS.category_id,
        CATEGORIES.category_name, PROJECTS.project_name,
        PROJECTS.start, PROJECTS.end, PROJECTS.canceled
    ]
    condition = (
        (PROJECTS.user_id == Parameter('%s')) & (PROJECTS.project_id == Parameter('%s'))
    )
    query = queries.select_join_query(
        PROJECTS, CATEGORIES, on_fields,
        columns, condition
    )
    # Generate values
    values = (user_id, project_id)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)
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
def update_project(project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    updates = (PROJECTS.end, Parameter('%s'))
    condition = (
        (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.update_query(PROJECTS, updates, condition)

    # Generate values
    end = datetime.today().date()
    values = (end, project_id, user_id)

    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {
        'Detail': f"The end date for project {project_id} has been updated to {end}"
    }

@router.put(
    path="/{project_id}/canceled",
    status_code=status.HTTP_200_OK,
    summary="Cancel a project"
)
def update_project(project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    updates = (PROJECTS.canceled, Parameter('%s'))
    condition = (
        (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.update_query(PROJECTS, updates, condition)

    # Generate values
    canceled = datetime.today().date()
    values = (canceled, project_id, user_id)
    
    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {
        'Detail': f"The canceled date for project {project_id} has been updated to {canceled}"
    }


@router.put(
    path="/{project_id}/name",
    status_code=status.HTTP_200_OK,
    summary="Cancel a project"
)
def update_project(project_id:int, new_project_name:str, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    updates = (PROJECTS.project_name, Parameter('%s'))
    condition = (
        (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.update_query(PROJECTS, updates, condition)

    # Generate values
    values = (new_project_name, project_id, user_id)
    
    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {
        'Detail': f"The project_name of project:{project_id} has been updated to {new_project_name}"
    }


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete project"
)
def delete_project(project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()

    # Generate query
    condition = (
        (PROJECTS.project_id == Parameter('%s')) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(PROJECTS, condition)

    # Generate values
    values = (project_id, user_id)
    
    # Execute query
    DB.execute_query(query.get_sql(), values)

    message = delete_message(DB, 'projects', project_id)

    return {
        'Detail': message
    }



# @router.delete(
#     path="/{project_ids}",
#     response_model=list[Project],
#     status_code=status.HTTP_200_OK,
#     summary="Delete project"
# )
# def delete_projects():
#     pass

