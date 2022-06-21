from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from pypika import Tables, Parameter

from models import Pomodoro, PomodoroResponse, ResponseUser, Satisfaction
from data import DB
import queries
from routers.utils import get_current_user, get_satisfaction_int

# Constants
PROJECTS, CATEGORIES, POMODOROS = Tables('projects', 'categories', 'pomodoros')


router = APIRouter(
    prefix='/pomodoros',
    tags=["Pomodoros"]
)


# Pomodoro paths
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create pomodoro"
)
def create_pomodoro(pomodoro:Pomodoro, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    columns = [
        POMODOROS.project_id, POMODOROS.category_id, 
        POMODOROS.duration, POMODOROS.pomodoro_date,
        POMODOROS.user_id
    ]
    query = queries.insert_query(POMODOROS, columns)

    # Generate values
    pomodoro_date = datetime.today()
    values = (
        pomodoro.project_id, pomodoro.category_id, pomodoro.duration,
        pomodoro_date, user_id
    )

    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {"details": f"Pomodoro was created sucessfully"}


@router.get(
    path="/{category_id}/{project_id}",
    response_model=list[PomodoroResponse],
    status_code=status.HTTP_200_OK,
    summary="Get pomodoros in a project"
)
def get_pomodoro(category_id:int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    join_on = [
        (PROJECTS, (POMODOROS.project_id == PROJECTS.project_id) & (POMODOROS.category_id == PROJECTS.category_id)),
        (CATEGORIES, (CATEGORIES.category_id == POMODOROS.category_id))
    ]
    columns = [
        POMODOROS.pomodoro_id, CATEGORIES.category_name, PROJECTS.project_name, POMODOROS.pomodoro_date,
        POMODOROS.duration, POMODOROS.pomodoro_satisfaction
    ]
    condition = (
        (POMODOROS.user_id == Parameter("%s")) & (POMODOROS.category_id == Parameter("%s")) & (POMODOROS.project_id == Parameter("%s"))
    )
    query = queries.select_join_on_query(
        POMODOROS, join_on, columns, condition, 'pomodoro_date'
    )

    # Generate values
    values = (user_id, category_id, project_id)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are not pomodoros for this project"
        )

    # Satisfaction
    df.pomodoro_satisfaction.fillna("", inplace=True)
    satisfaction = {0: "missing", 1: "good", 2: "bad"}
    df.pomodoro_satisfaction.replace(satisfaction, inplace=True)

    return df.to_dict('records')

@router.put(
    path="/{pomodoro_id}",
    status_code=status.HTTP_200_OK,
    summary=""
)
def get_pomodoro(pomodoro_id:int, satisfaction:Satisfaction, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    updates = (POMODOROS.pomodoro_satisfaction, Parameter('%s'))
    condition = (
        (POMODOROS.pomodoro_id == Parameter("%s")) & (POMODOROS.user_id == Parameter('%s'))
    )
    query = queries.update_query(POMODOROS, updates, condition)

    # Generate values
    satisfaction = get_satisfaction_int(satisfaction.value)
    values = (satisfaction, pomodoro_id, user_id)

    # Execute query
    DB.execute_query(query.get_sql(), values)

    return {
        'Detail': f"Satisfaction updated in pomodoro {pomodoro_id}"
    }
