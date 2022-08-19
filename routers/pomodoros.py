from datetime import datetime, timedelta
import random

from fastapi import APIRouter, status, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import PomodoroResponse, ResponseUser, Satisfaction
from data import DB
import query as q
from utils import get_current_user, get_satisfaction_int

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/pomodoros',
    tags=["Pomodoros"]
)


# Pomodoro paths
@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def get_pomodoros_home(request:Request, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    previous_30_days = datetime.today() - timedelta(days=30)
    values = (user_id, previous_30_days)
    df = q.get_pomodoros(values, all=True)

    pomodoros = df.to_dict('records')
    context = {
        'request': request,
        'pomodoros': pomodoros
    }

    return templates.TemplateResponse("general_pages/pomodoros.html", context=context)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create pomodoro",
    response_class=HTMLResponse
)
def create_pomodoro(
        category_id:int = Form(...),
        project_id:int = Form(...),
        duration:int = Form(...),
        current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    pomodoro_date = datetime.today()
    values = (
        category_id, project_id, duration,
        pomodoro_date, user_id
    )
    query = q.create_pomodoro()

    # Execute query
    DB.execute_query(query, values)

    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    return f'<h3 style="color:{color};" id="placeholder">Pomodoro created, Start the timer</h3>'


@router.put(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Measure pomodoro satisfaction",
    response_class=HTMLResponse,
)
def update_pomodoro_satisfaction(request: Request, satisfaction:Satisfaction = Form(...), current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id,)
    df = q.get_latest_pomodoro(values)
    pomodoro = df.to_dict('records')[0]

    satisfaction = get_satisfaction_int(satisfaction.value)
    values = (satisfaction, pomodoro['pomodoro_id'], user_id)
    query = q.update_pomodoro_satisfaction()

    # Execute query
    DB.execute_query(query, values)

    return '<p id="pomodoro-confirmation">Sent</p>'


@router.get(
    path="/satisfaction",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    include_in_schema=False,
)
def get_satisfaction_modal(request:Request, current_user:ResponseUser = Depends(get_current_user)):
    return '<div id="pomodoro-confirmation"></div>'

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

