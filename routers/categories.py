from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException

from models import Category, CategoryResponse, ResponseUser
from data import DB
import query as q
from utils import get_current_user

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
    values = (category.category_name, user_id)
    query = q.create_category()
    DB.execute_query(query, values)

    return {"details": f"Category {category.category_name} was created sucessfully"}

@router.get(
    path="/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get categories"
)
def get_categories(current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, )
    df = q.get_categories(values)

    return df.to_dict('records')


@router.get(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category"
)

def get_category(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id)
    df = q.get_category(values)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This category does not exists"
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
    user_id = current_user['user_id']
    values = (category_name, category_id, user_id)
    query = q.update_category()
    DB.execute_query(query, values)

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
    user_id = current_user['user_id']
    values = (category_id, user_id)
    query = q.delete_category()
    DB.execute_query(query, values)

    return {
        'Detail': f"Category {category_id} was deleted"
    }

