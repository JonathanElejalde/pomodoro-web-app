from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Form, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import RecallResponse, ResponseUser
from data import DB
import query as q
from utils import get_current_user, markdown_to_html

# Constants
NORMAL_FORM = Form(..., max_length=255, min_length=1, example="Test")

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/recalls',
    tags=["Recalls"]
)


# Recall paths
@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def get_recalls_home(request:Request, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse("general_pages/recalls.html", {"request": request})


# CREATE AN ENDPOINT THAT SEARCHES BY TEXT


@router.put(
    path="/{recall_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a recall"
)
def update_recalls(
    recall_id:int, recall_title:str = None,
    recall:str = None, current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    query, values = q.update_recall(recall_id, recall_title, recall, user_id)

    # Execute query
    DB.execute_query(query, tuple(values))

    return {
        "detail": f"Recall {recall_id} was updated sucessfully"
    }


@router.delete(
    path="/{recall_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a recall"
)
def delete_recall(recall_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (recall_id, user_id)
    query = q.delete_recall()
    
    DB.execute_query(query, values)

    return {
        'Detail': f"Recall {recall_id} was deleted"
    }


@router.get(
    path="/text/",
    response_model=list[RecallResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recalls in a recall project"
)
def get_recalls(request:Request, recall_project_id: int, current_user:ResponseUser = Depends(get_current_user), hx_request: Optional[str] = Header(None)):
    user_id = current_user['user_id']
    values = (recall_project_id, user_id)
    df = q.get_recalls(values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {user_id} does not have recalls for recall_project_id {recall_project_id}"
        )

    df['recall'] = df.recall.apply(markdown_to_html)
    recalls = df.to_dict('records')
    context = {
        'request': request,
        'recalls': recalls
    }

    if hx_request:
        return templates.TemplateResponse("components/recalls.html", context=context)
    return templates.TemplateResponse("general_pages/recalls.html", context=context)


@router.get(
    path="/create_recall",
    summary="Recall creation",
    include_in_schema=False
)
def create_recall(request: Request, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse("general_pages/create_recall.html", {"request": request})

@router.post(
    path="/create_recall",
    status_code=status.HTTP_201_CREATED,
    summary="Recall creation"
)
def create_recall(
    request: Request,
    recall_project_id: int = Form(...),
    recall_title: str = Form(..., min_length=1, max_length=255),
    recall: str = Form(..., min_length=1),
    current_user:ResponseUser = Depends(get_current_user)
    ):

    user_id = current_user['user_id']
    values = (user_id, recall_project_id, recall_title, recall)
    query = q.create_recall()
    
    # Execute query
    DB.execute_query(query, values)

    return templates.TemplateResponse("general_pages/create_recall.html", {"request": request})


@router.delete(
    path="/recall-project/{recall_project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete all the recalls in a recall project"
)
def delete_recalls(recall_project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (recall_project_id, user_id)
    query = q.delete_recalls()
    
    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"Delete all recalls in project {recall_project_id}"
    }



