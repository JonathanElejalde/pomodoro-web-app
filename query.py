from typing import Union

from fastapi import status, HTTPException
from pandas import DataFrame
from pypika import Tables, Parameter

from data import DB
import queries

USERS, CATEGORIES, PROJECTS, POMODOROS = Tables('users', 'categories', 'projects', 'pomodoros')
RECALL_PROJECTS, RECALLS = Tables('recall_projects', 'recalls')


# Users
def signup_user()-> str:
    columns = [
        USERS.user_id, USERS.email, USERS.password,
        USERS.first_name, USERS.last_name, USERS.birth_date,
    ]
    query = queries.insert_query(USERS, columns)
    return query.get_sql()

def login_user(values:tuple)-> DataFrame:
    columns = [
        USERS.user_id, USERS.email, USERS.first_name,
        USERS.last_name, USERS.birth_date, USERS.password,
    ]
    condition = [USERS.email == Parameter("%s")]
    query = queries.select_query(USERS, columns, condition)

    # Get user that matches email
    user = DB.pandas_query(query.get_sql(), values)

    return user

def delete_user()-> str:
    delete_condition = (USERS.user_id == Parameter("%s"))
    query = queries.delete_query(USERS, delete_condition)
    
    return query.get_sql()


# Categories
def create_category()-> str:
    columns = [
        CATEGORIES.category_name, CATEGORIES.user_id
    ]
    query = queries.insert_query(CATEGORIES, columns)

    return query.get_sql()

def get_categories(values:tuple, category_id:int = None)->DataFrame:
    columns = [CATEGORIES.category_id, CATEGORIES.category_name]
    condition = [CATEGORIES.user_id == Parameter("%s")]

    if category_id:
        condition.append(CATEGORIES.category_id == Parameter("%s"))

    query = queries.select_query(CATEGORIES, columns, condition, criterion='all')
    df = DB.pandas_query(query.get_sql(), values)

    return df

def update_category()->str:
    updates = (CATEGORIES.category_name, Parameter('%s'))
    condition = (
        (CATEGORIES.category_id == Parameter("%s")) & (CATEGORIES.user_id == Parameter("%s"))
    )
    query = queries.update_query(CATEGORIES, updates, condition)
    
    return query.get_sql()

def delete_category()-> str:
    condition = (
        (CATEGORIES.category_id == Parameter('%s')) & (CATEGORIES.user_id == Parameter("%s"))
    )
    query = queries.delete_query(CATEGORIES, condition)

    return query.get_sql()

# Projects
def create_project()-> str:
    columns = [
        PROJECTS.user_id, PROJECTS.category_id, 
        PROJECTS.project_name, PROJECTS.start
    ]
    query = queries.insert_query(PROJECTS, columns)

    return query.get_sql()

def get_projects(values:tuple, project_id:int = None, category_id:int=None)-> DataFrame:
    on_fields = ('category_id', 'user_id')
    columns = [
        PROJECTS.project_id, PROJECTS.category_id,
        CATEGORIES.category_name, PROJECTS.project_name,
        PROJECTS.start, PROJECTS.end, PROJECTS.canceled
    ]
    condition = [
        PROJECTS.user_id == Parameter('%s')
    ]
    if category_id:
        condition.append(PROJECTS.category_id == Parameter("%s"))

    if project_id:
        condition.append(PROJECTS.project_id == Parameter('%s'))

    query = queries.select_join_query(
        PROJECTS, CATEGORIES, on_fields,
        columns, condition, criterion='all'
    )
    # Execute query
    df = DB.pandas_query(query.get_sql(), values)

    return df

def update_project(column)-> str:
    updates = (PROJECTS[column], Parameter("%s"))
    condition = (
        (PROJECTS.project_id == Parameter("%s")) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.update_query(PROJECTS, updates, condition)

    return query.get_sql()

def delete_project()-> str:
    condition = (
        (PROJECTS.project_id == Parameter('%s')) & (PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(PROJECTS, condition)

    return query.get_sql()


# Pomodoros
def create_pomodoro()-> str:
    columns = [
        POMODOROS.category_id, POMODOROS.project_id, 
        POMODOROS.duration, POMODOROS.pomodoro_date,
        POMODOROS.user_id
    ]
    query = queries.insert_query(POMODOROS, columns)

    return query.get_sql()

def get_pomodoros(values:tuple)-> DataFrame:
    join_on = [
        (PROJECTS, (POMODOROS.project_id == PROJECTS.project_id) & (POMODOROS.category_id == PROJECTS.category_id)),
        (CATEGORIES, (CATEGORIES.category_id == POMODOROS.category_id))
    ]
    columns = [
        POMODOROS.pomodoro_id, CATEGORIES.category_name, PROJECTS.project_name, POMODOROS.pomodoro_date,
        POMODOROS.duration, POMODOROS.pomodoro_satisfaction
    ]
    condition = [
        POMODOROS.user_id == Parameter("%s"),
        POMODOROS.category_id == Parameter("%s"),
        POMODOROS.project_id == Parameter("%s"),
    ]
    query = queries.select_join_on_query(
        POMODOROS, join_on, columns, condition, 'pomodoro_date'
    )
    df = DB.pandas_query(query.get_sql(), values)

    return df

def update_pomodoro_satisfaction()-> str:
    updates = (POMODOROS.pomodoro_satisfaction, Parameter('%s'))
    condition = (
        (POMODOROS.pomodoro_id == Parameter("%s")) & (POMODOROS.user_id == Parameter('%s'))
    )
    query = queries.update_query(POMODOROS, updates, condition)

    return query.get_sql()

def get_latest_pomodoro(values:tuple)-> str:
    columns = [POMODOROS.pomodoro_id]
    condition = [
        POMODOROS.user_id == Parameter("%s")
    ]
    query = queries.select_query(POMODOROS, columns=columns, condition=condition, order_by="pomodoro_date", limit=1)
    df = DB.pandas_query(query.get_sql(), values)

    return df


    
# Recall Projects
def create_recall_project()-> str:

    columns = [RECALL_PROJECTS.user_id, RECALL_PROJECTS.project_name]
    query = queries.insert_query(RECALL_PROJECTS, columns)

    return query.get_sql()

def get_recall_projects(values:Union[tuple, list])-> DataFrame:
    columns = [RECALL_PROJECTS.recall_project_id, RECALL_PROJECTS.project_name]

    if type(values) == list:
        condition = [
            RECALL_PROJECTS.user_id == Parameter('%s'), 
            RECALL_PROJECTS.recall_project_id == Parameter("%s")
        ]
    else:
        condition = [RECALL_PROJECTS.user_id == Parameter('%s')]
    query = queries.select_query(RECALL_PROJECTS, columns, condition)
    # Execute query
    df = DB.pandas_query(query.get_sql(), values)

    return df

def update_recall_project_name()-> str:
    updates = (RECALL_PROJECTS.project_name, Parameter('%s'))
    condition = (
        (RECALL_PROJECTS.user_id == Parameter('%s')) & (RECALL_PROJECTS.recall_project_id == Parameter("%s"))
        )
    query = queries.update_query(RECALL_PROJECTS, updates, condition)

    return query.get_sql()
    
def delete_recall_project()-> str:
    condition = (
        (RECALL_PROJECTS.recall_project_id == Parameter('%s')) & (RECALL_PROJECTS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALL_PROJECTS, condition)

    return query.get_sql()
    

# Recalls
def create_recall()-> str:
    columns = [
        RECALLS.user_id, RECALLS.recall_project_id, 
        RECALLS.recall_title, RECALLS.recall
    ]
    query = queries.insert_query(RECALLS, columns)

    return query.get_sql()

def get_recalls(values:tuple, recall_id:int = None)-> DataFrame:
    join_on = [
        (RECALL_PROJECTS, (RECALLS.user_id == RECALL_PROJECTS.user_id) & (RECALLS.recall_project_id == RECALL_PROJECTS.recall_project_id))
    ]
    columns = [
        RECALLS.recall_id, RECALL_PROJECTS.recall_project_id, 
        RECALL_PROJECTS.project_name, RECALLS.recall_title, RECALLS.recall
        ]

    condition = [RECALLS.user_id == Parameter("%s")]

    if recall_id:
        condition.append(RECALLS.recall_id == Parameter("%s"))
    else:
        condition.append(RECALLS.recall_project_id == Parameter("%s"))

    query = queries.select_join_on_query(RECALLS, join_on, columns, condition)

    # Execute query
    df = DB.pandas_query(query.get_sql(), values)

    return df

def update_recall(recall_id:int, recall_title:str, recall:str, user_id:str)-> tuple[str, tuple]:
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

    return query.get_sql(), values

def delete_recall()-> str:
    condition = (
        (RECALLS.recall_id == Parameter('%s')) & (RECALLS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALLS, condition)

    return query.get_sql()

def delete_recalls()-> str:
    condition = (
        (RECALLS.recall_project_id == Parameter('%s')) & (RECALLS.user_id == Parameter('%s'))
    )
    query = queries.delete_query(RECALLS, condition)

    return query.get_sql()