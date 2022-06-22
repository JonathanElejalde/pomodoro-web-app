from sre_parse import CATEGORIES
from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException
from pypika import Table, MySQLQuery, Parameter

from models import Category, CategoryResponse, ResponseUser
from data import DB
import queries
from utils import delete_message, get_current_user, delete_message

# Constants
CATEGORIES = Table('categories')

router = APIRouter(
    prefix='/categories',
    tags=["Categories"]
)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Category creation"
)
def create_category(category:Category, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    columns = [
        CATEGORIES.category_name, CATEGORIES.user_id
    ]
    query = queries.insert_query(CATEGORIES, columns)
    values = (category.category_name, user_id)
    DB.execute_query(query.get_sql(), values)

    return {"details": f"Category {category.category_name} was created sucessfully"}

@router.get(
    path="/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get categories"
)
def get_categories(current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    columns = [CATEGORIES.category_id, CATEGORIES.category_name]
    condition = (CATEGORIES.user_id == Parameter("%s"))
    query = queries.select_query(CATEGORIES, columns, condition)
    values = (user_id, )
    df = DB.pandas_query(query.get_sql(), values)
    return df.to_dict('records')


@router.get(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category"
)

def get_category(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']

    # Generate query
    columns = [CATEGORIES.category_id, CATEGORIES.category_name]
    condition = (CATEGORIES.user_id == Parameter("%s")) & (CATEGORIES.category_id == Parameter("%s"))
    query = queries.select_query(CATEGORIES, columns, condition)
    values = (user_id, category_id)
    df = DB.pandas_query(query.get_sql(), values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This project does not exists"
        )
    category = df.to_dict('records')[0]
    return category


@router.put(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update category"
)
def update_category(category_id:int, category_name: Optional[str], current_user:ResponseUser = Depends(get_current_user)):

    # Generate query
    updates = (CATEGORIES.category_name, Parameter('%s'))
    condition = (CATEGORIES.category_id == Parameter("%s"))
    query = queries.update_query(CATEGORIES, updates, condition)
    
    values = (category_name, category_id)
    DB.execute_query(query.get_sql(), values)

    return {
        'category_name': category_name,
        'category_id': category_id
    }


@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete category"
)
def delete_category(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    
    condition = (CATEGORIES.category_id == Parameter('%s'))
    query = queries.delete_query(CATEGORIES, condition)
    values = (category_id,)
    DB.execute_query(query.get_sql(), values)
    message = delete_message(DB)
    return {
        'Detail': message
    }

