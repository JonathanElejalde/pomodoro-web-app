from typing import Optional

from fastapi import APIRouter, status, Depends
from pypika import Table, MySQLQuery, Parameter

from models import Category, CategoryResponse, ResponseUser
from data import Database
from routers.utils import get_current_user, get_user_id

# Constants
DB = Database()

router = APIRouter(
    prefix='/categories',
    tags=["Categories"]
)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Category creation"
)
def create_category(category:Category):
    categories = Table('categories')
    query = MySQLQuery.into(categories).columns(
        categories.category_name, categories.user_id
    ).insert(Parameter('%s'), Parameter('%s'))

    values = (category.category_name, str(category.user_id))

    DB.execute_query(query.get_sql(), values)

    return {"details": f"Category {category.category_name} was created sucessfully"}

@router.get(
    path="/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get categories"
)
def get_categories(current_user: ResponseUser = Depends(get_current_user)):
    user_id = get_user_id()
    categories = Table('categories')
    query = MySQLQuery.from_(categories).select(
        categories.category_id, categories.category_name
    ).where(
        categories.user_id == user_id
    )

    df = DB.pandas_query(query.get_sql())
    return df.to_dict('records')


@router.get(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category"
)

def get_category(category_id:int, user_id:str):
    categories = Table('categories')
    query = MySQLQuery.from_(categories).select(
        categories.category_id, categories.category_name
    ).where(
        (categories.user_id == user_id) & (categories.category_id == category_id)
    )

    df = DB.pandas_query(query.get_sql())
    category = df.to_dict('records')[0]
    return category


@router.put(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update category"
)
def update_category(category_id:int, category_name: Optional[str]):
    categories = Table('categories')
    query = MySQLQuery.update(categories).set(
        categories.category_name, Parameter('%s')
        ).where(
            categories.category_id == Parameter("%s")
            )
    
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
def delete_category(category_id:int):
    categories = Table('categories')
    query = MySQLQuery.from_(categories).delete().where(
        categories.category_id == Parameter('%s')
        )
    values = (category_id,)

    DB.execute_query(query.get_sql(), values)

    return {
        'Detail': f"Category ID {category_id} was deleted"
    }

# @router.delete(
#     path="/{category_ids}",
#     response_model=list[Category],
#     status_code=status.HTTP_200_OK,
#     summary="Delete categories",
#  
# )
# def delete_categories():
#     pass
