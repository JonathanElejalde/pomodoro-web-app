from pandas import DataFrame
from pypika import Tables, Parameter

from data import DB
import queries

USERS, CATEGORIES, PROJECTS, POMODOROS = Tables('users', 'categories', 'projects', 'pomodoros')
RECALL_PROJECTS, RECALLS = Tables('recall_projects', 'recalls')


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
    condition = (USERS.email == Parameter("%s"))
    query = queries.select_query(USERS, columns, condition)

    # Get user that matches email
    user = DB.pandas_query(query.get_sql(), values)

    return user

def delete_user()-> str:
    delete_condition = (USERS.user_id == Parameter("%s"))
    query = queries.delete_query(USERS, delete_condition)
    
    return query.get_sql()