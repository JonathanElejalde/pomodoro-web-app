from datetime import date, datetime

from fastapi import APIRouter, status, Depends, HTTPException
from pypika import Tables, MySQLQuery, Parameter

from models import Project, ProjectResponse, ResponseUser
from data import Database
from routers.utils import get_current_user, get_user_id

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
    start = datetime.today()
    values = (user_id, project.category_id, project.project_name, start)

    placeholders = [Parameter("%s") for _ in range(len(values))]

    query = MySQLQuery.into(PROJECTS).columns(
        PROJECTS.user_id, PROJECTS.category_id, 
        PROJECTS.project_name, PROJECTS.start
    ).insert(*placeholders)

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
    query = MySQLQuery \
        .from_(PROJECTS) \
        .join(CATEGORIES) \
        .on_field('category_id', 'user_id') \
        .select(
            PROJECTS.project_id, PROJECTS.category_id,
            CATEGORIES.category_name, PROJECTS.project_name,
            PROJECTS.start, PROJECTS.end, PROJECTS.canceled
        ) \
        .where(
            (PROJECTS.user_id == Parameter('%s')) & (PROJECTS.category_id == Parameter('%s'))
        )
    values = (user_id, category_id)
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
    query = MySQLQuery \
        .from_(PROJECTS) \
        .join(CATEGORIES) \
        .on_field('category_id', 'user_id') \
        .select(
            PROJECTS.project_id, PROJECTS.category_id,
            CATEGORIES.category_name, PROJECTS.project_name,
            PROJECTS.start, PROJECTS.end, PROJECTS.canceled
        ) \
        .where(
            (PROJECTS.user_id == Parameter('%s')) & (PROJECTS.project_id == Parameter('%s'))
        )
    values = (user_id, project_id)
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
    query = MySQLQuery.update(PROJECTS).set(
        PROJECTS.end, Parameter('%s')
        ).where(
            (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
            )
    end = datetime.today().date()
    values = (end, project_id, user_id)
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
    query = MySQLQuery.update(PROJECTS).set(
        PROJECTS.canceled, Parameter('%s')
        ).where(
            (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
            )
    canceled = datetime.today().date()
    values = (canceled, project_id, user_id)
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
    query = MySQLQuery.update(PROJECTS).set(
        PROJECTS.project_name, Parameter('%s')
        ).where(
            (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
            )
    values = (new_project_name, project_id, user_id)
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

    query = MySQLQuery.from_(PROJECTS).delete().where(
        (PROJECTS.project_id == Parameter('%s')) & (PROJECTS.user_id == Parameter('%s'))
        )
    values = (project_id, user_id)
    DB.execute_query(query.get_sql(), values)

    if DB.cursor.rowcount > 0:
        message = f"Project id {project_id} was deleted"
    elif DB.cursor.rowcount == 0:
        message = f"Project id does not exists"
    else:
        message = "Unexpected error occured"

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

