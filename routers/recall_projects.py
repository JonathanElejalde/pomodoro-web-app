from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Form, Request, Header
from fastapi.templating import Jinja2Templates
from mysql.connector.errors import IntegrityError

from models import RecallProjectResponse, ResponseUser
from data import DB
import query as q
from utils import get_current_user


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/recall_projects',
    tags=["Recall Projects"]
)

# Recall project paths
@router.get(
    path="/create_recall_project",
    include_in_schema=False
)
def create_recall_project_form(request:Request):
    return templates.TemplateResponse("components/create_recall_project.html", {"request": request})


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a recall project"
)
def create_recall_project(
    request: Request,
    project_name: str = Form(...),
    current_user:ResponseUser = Depends(get_current_user),
    ):
    user_id = current_user['user_id']
    values = (user_id, project_name)
    query = q.create_recall_project()

    try:
        DB.execute_query(query, values)
    except IntegrityError:
        # Show this as an error/warning in the template
        return "Project name already exists"

    # Get recall projects and return them
    values = (user_id,)
    df = q.get_recall_projects(values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {user_id} does not have recall projects"
        )

    projects = df.to_dict('records')
    context = {
        "request": request,
        "projects": projects
    }

    return templates.TemplateResponse('components/recall_projects.html', context=context)


@router.get(
    path="/",
    response_model=list[RecallProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recall project names",
)
def get_recall_projects(request: Request, current_user:ResponseUser = Depends(get_current_user), hx_request: Optional[str] = Header(None)):
    user_id = current_user['user_id']
    values = (user_id,)
    df = q.get_recall_projects(values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {user_id} does not have recall projects"
        )

    projects = df.to_dict('records')
    context = {
        "request": request,
        "projects": projects
    }

    if hx_request:
        return templates.TemplateResponse('components/recall_projects.html', context=context)
    return templates.TemplateResponse("general_pages/recall_projects.html", context=context)


@router.put(
    path="/",
    response_model=RecallProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a recall project"
)
def update_recall_project_name(
    recall_project_id:int, project_name: str, 
    current_user:ResponseUser = Depends(get_current_user)):
    
    user_id = current_user['user_id']
    values = (project_name, user_id, recall_project_id)
    query = q.update_recall_project_name()
    
    # Execute query
    DB.execute_query(query, values)

    return {
        "recall_project_id": recall_project_id,
        "project_name": project_name
    }


@router.delete(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Delete a recall project"
)
def get_recall_project_names(
    recall_project_id:int,
    current_user:ResponseUser = Depends(get_current_user)):

    user_id = current_user['user_id']
    values = (recall_project_id, user_id)
    query = q.delete_recall_project()
    
    # Execute query
    DB.execute_query(query, values)

    return "<tr></tr>"
