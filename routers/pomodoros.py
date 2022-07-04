from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException

from models import Pomodoro, PomodoroResponse, ResponseUser, Satisfaction
from data import DB
import query as q
from utils import get_current_user, get_satisfaction_int

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
    pomodoro_date = datetime.today()
    values = (
        pomodoro.project_id, pomodoro.category_id, pomodoro.duration,
        pomodoro_date, user_id
    )
    query = q.create_pomodoro()

    # Execute query
    DB.execute_query(query, values)

    return {"details": f"Pomodoro was created sucessfully"}


@router.get(
    path="/{category_id}/{project_id}",
    response_model=list[PomodoroResponse],
    status_code=status.HTTP_200_OK,
    summary="Get pomodoros in a project"
)
def get_pomodoro(category_id:int, project_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id, project_id)

    df = q.get_pomodoros(values)
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
def update_pomodoro_satisfaction(pomodoro_id:int, satisfaction:Satisfaction, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    satisfaction = get_satisfaction_int(satisfaction.value)
    values = (satisfaction, pomodoro_id, user_id)
    query = q.update_pomodoro_satisfaction()

    # Execute query
    DB.execute_query(query, values)

    return {
        'Detail': f"Satisfaction updated in pomodoro {pomodoro_id}"
    }
