from datetime import datetime
from typing import Optional

from fastapi import APIRouter, status, Depends, Request, Form, Query, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import ResponseUser
from data import DB
import query as q
from utils import get_current_user, get_current_endpoint, get_categories_list

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/projects',
    tags=["Projects"]
)

# Project paths

@router.post(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create project"
)
def create_project(request:Request, category_id:int = Form(...), 
        project_name:str = Form(...), current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    start = datetime.today()
    values = (user_id, category_id, project_name, start)
    query = q.create_project()

    # Execute query
    DB.execute_query(query, values)

    # Get categories
    categories = get_categories_list(user_id)
    context = {
        'request': request,
        'categories': categories
    }

    return templates.TemplateResponse("components/create_project.html", context=context)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    include_in_schema=False
)
def get_projects(request: Request, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse("/general_pages/projects.html", {"request": request})

@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete project",
    response_class=HTMLResponse
)
def delete_project(request: Request, project_id:int = Path(...), current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (project_id, user_id)
    query = q.delete_project()
    
    # Execute query
    DB.execute_query(query, values)

    return "<tr></tr>"


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
def update_project(request: Request, project_id:int = Path(...,), new_project_name:str = Form(...), current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (new_project_name, project_id, user_id)
    query = q.update_project('project_name')
    
    # Execute query
    DB.execute_query(query, values)

    # Get project with new data
    values = [user_id, project_id]
    df = q.get_projects(values, project_id=project_id)

    df.fillna("", inplace=True)
    project = df.to_dict('records')[0]
    context = {
        "request": request,
        "project": project
    }
    
    return templates.TemplateResponse('components/project_edited.html', context=context)


@router.get(
    path="/names",
    status_code=status.HTTP_200_OK,
    summary="Get projects",
    response_class=HTMLResponse
)
def get_projects_names(request: Request, category_id:int = Query(...), current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id)
    df = q.get_projects(values, category_id=category_id)
    if df.empty:
        return '<select id="project-names" name="project_id"></select>'
    df.fillna("", inplace=True)
    projects = df.to_dict('records')
    context = {
        'request': request,
        'projects': projects
    }
    current_url = request.headers.get('hx-current-url')
    endpoint = get_current_endpoint(current_url)

    if endpoint == "pomodoro":
        return templates.TemplateResponse("/components/projects.html", context=context)
    elif endpoint == "projects":
        return templates.TemplateResponse("/components/projects_table.html", context=context)
    else:
        raise ValueError(f"Current url is {endpoint}, it does not match pomodoro or projects")
    

@router.get(
    path="/{project_id}/edit",
    include_in_schema=False,
    response_class=HTMLResponse
)
def edit_recall_project(request:Request, project_id:int = Path(...,), 
    current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    values = [user_id, project_id]
    df = q.get_projects(values, project_id=project_id)

    df.fillna("", inplace=True)
    project = df.to_dict('records')[0]
    context = {
        "request": request,
        "project": project
    }
    
    return templates.TemplateResponse('components/edit_project.html', context=context)

@router.get(
    path="/create_project",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Create project"
)
def create_project_form(request:Request, current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    # Get categories
    categories = get_categories_list(user_id)
    context = {
        'request': request,
        'categories': categories
    }

    return templates.TemplateResponse("components/create_project.html", context=context)