from fastapi import APIRouter, status, Depends, HTTPException, Form
from pypika import Tables, Parameter

from models import Recall, RecallResponse, ResponseUser
from data import DB
import queries
from routers.utils import get_current_user, delete_message

# Constants
RECALLS, RECALL_PROJECTS = Tables('recalls', "recall_projects")
NORMAL_FORM = Form(..., max_length=255, min_length=1, example="Test")

router = APIRouter(
    prefix='/recalls',
    tags=["Recalls"]
)

# Recall paths
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Recall creation"
)
def create_recall(request: Recall, current_user:ResponseUser = Depends(get_current_user)
    ):

    user_id = current_user['user_id']

     # Generate query
    columns = [
        RECALLS.user_id, RECALLS.recall_project_id, 
        RECALLS.recall_title, RECALLS.recall
    ]
    query = queries.insert_query(RECALLS, columns)

    # Generate values
    values = (user_id, request.recall_project_id, request.recall_title, request.recall)

    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {"details": f"New recall added"}



@router.get(
    path="/{project_id}",
    response_model=list[RecallResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recalls in a recall project"
)
def get_recall(project_id: int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    join_on = [
        (RECALL_PROJECTS, (RECALLS.user_id == RECALL_PROJECTS.user_id) & (RECALLS.recall_project_id == RECALL_PROJECTS.recall_project_id))
    ]
    columns = [
        RECALLS.recall_id, RECALL_PROJECTS.recall_project_id, 
        RECALL_PROJECTS.project_name, RECALLS.recall_title, RECALLS.recall
        ]
    condition = (
        (RECALLS.recall_project_id == Parameter("%s")) & (RECALLS.user_id == Parameter("%s"))
    )
    query = queries.select_join_on_query(RECALLS, join_on, columns, condition)

    # Generate values
    values = (project_id, user_id)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {user_id} does not have recalls for project_id {project_id}"
        )

    return df.to_dict('records')

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

    # Generate query
    updates = []
    values = []
    if recall:
        updates.append((RECALL_PROJECTS.recall, Parameter("%s")))
        values.append(recall)
    if recall_title:
        updates.append((RECALL_PROJECTS.recall_title, Parameter("%s")))
        values.append(recall_title)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A recall title or a recall should be pass to update",
            )

    condition = (
        (RECALLS.user_id == Parameter("%s")) & (RECALLS.recall_id == Parameter("%s"))
    )

    values.append(user_id)
    values.append(recall_id)

    query = queries.update_query(RECALLS, updates, condition)

    # Execute query
    DB.execute_query(query.get_sql(), tuple(values))

    return {
        "detail": f"Recall {recall_id} was updated sucessfully"
    }


@router.delete(
    path="/{recall_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a recall"
)
def delete_recalls(recall_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    
    # Generate query
    condition = (
        (RECALLS.recall_id == Parameter('%s')) & (RECALLS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALLS, condition)

    # Generate values
    values = (recall_id, user_id)
    
    # Execute query
    print(query.get_sql())
    print(values)
    DB.execute_query(query.get_sql(), values)

    message = delete_message(DB)

    return {
        'Detail': message
    }

@router.delete(
    path="/recall-project/{recall_project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete all the recalls in a recall project"
)
def delete_recall(recall_project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    
    # Generate query
    condition = (
        (RECALLS.recall_project_id == Parameter('%s')) & (RECALLS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALLS, condition)

    # Generate values
    values = (recall_project_id, user_id)
    
    # Execute query
    DB.execute_query(query.get_sql(), values)

    message = delete_message(DB)

    return {
        'Detail': message
    }



