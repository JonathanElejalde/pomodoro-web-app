from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Form, Request, Header
from fastapi.templating import Jinja2Templates
from mysql.connector.errors import IntegrityError
from pypika import Table, Parameter

from models import RecallProjectResponse, ResponseUser
from data import DB
import queries
from utils import get_current_user, delete_message

# Constants
RECALL_PROJECTS = Table('recall_projects')

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/recall_projects',
    tags=["Recall Projects"]
)

# Recall project paths
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a recall project"
)
def create_recall(
    request: Request,
    project_name: str = Form(...),
    current_user:ResponseUser = Depends(get_current_user),
    hx_request: Optional[str] = Header(None)
    ):

    user_id = current_user['user_id']

     # Generate query
    columns = [RECALL_PROJECTS.user_id, RECALL_PROJECTS.project_name]

    query = queries.insert_query(RECALL_PROJECTS, columns)

    # Generate values
    values = (user_id, project_name)

    # Execute query
    try:
        DB.execute_query(query.get_sql(), values)
    except IntegrityError:
        return "Project name already exists"


    if hx_request:

        print("hx-request")
        # Get project id to return when called with hx-request
        columns = [RECALL_PROJECTS.recall_project_id]
        condition = (
            (RECALL_PROJECTS.user_id == Parameter('%s')) & (RECALL_PROJECTS.project_name == Parameter("%s"))
        )
        query = queries.select_query(RECALL_PROJECTS, columns, condition)
        values = (user_id, project_name)

        query = queries.select_query(RECALL_PROJECTS, columns, condition)

        df = DB.pandas_query(query.get_sql(), values)

        recall_project_id = df.recall_project_id.values[0]
        
        context = {
            "request": request,
            "project_name": project_name,
            "recall_project_id": recall_project_id
        }

        return templates.TemplateResponse("components/new_project.html", context=context)

    return templates.TemplateResponse("general_pages/recall_projects.html", {"request": request})



@router.get(
    path="/",
    response_model=list[RecallProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recall project names",
)
def get_recall_project_names(request: Request, current_user:ResponseUser = Depends(get_current_user), hx_request: Optional[str] = Header(None)):
    user_id = current_user['user_id']

    # Generate query
    columns = [RECALL_PROJECTS.recall_project_id, RECALL_PROJECTS.project_name]
    condition = (RECALL_PROJECTS.user_id == Parameter('%s'))
    query = queries.select_query(RECALL_PROJECTS, columns, condition)

    # Generate values
    values = (user_id,)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)

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
def get_recall_project_names(
    recall_project_id:int, project_name: str, 
    current_user:ResponseUser = Depends(get_current_user)):
    
    user_id = current_user['user_id']

    # Generate query
    updates = (RECALL_PROJECTS.project_name, Parameter('%s'))
    condition = (
        (RECALL_PROJECTS.user_id == Parameter('%s')) & (RECALL_PROJECTS.recall_project_id == Parameter("%s"))
        )
    query = queries.update_query(RECALL_PROJECTS, updates, condition)

    # Generate values
    values = (project_name, user_id, recall_project_id)

    # Execute query
    DB.execute_query(query.get_sql(), values)

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

    # Generate query
    condition = (
        (RECALL_PROJECTS.recall_project_id == Parameter('%s')) & (RECALL_PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALL_PROJECTS, condition)

    # Generate values
    values = (recall_project_id, user_id)
    
    # Execute query
    DB.execute_query(query.get_sql(), values)

    #message = delete_message(DB)

    return "<tr></tr>"