from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Request, Header, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import Category, CategoryResponse, ResponseUser
from data import DB
import query as q
from utils import get_current_user

templates = Jinja2Templates(directory="templates")

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
def get_categories(request:Request, current_user:ResponseUser = Depends(get_current_user), hx_request: Optional[str] = Header(None)):
    user_id = current_user['user_id']
    values = (user_id, )
    df = q.get_categories(values)
    categories = df.to_dict('records')

    context = {
        'request': request,
        'categories': categories
    }

    if hx_request:
        return templates.TemplateResponse("components/categories.html", context=context)
    return templates.TemplateResponse("general_pages/categories.html", context=context)



@router.get(
    path="/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category"
)

def get_category(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (user_id, category_id)
    df = q.get_categories(values, category_id)

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
def update_category(request: Request, category_id:int, category_name:str = Form(...), current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (category_name, category_id, user_id)
    query = q.update_category()
    DB.execute_query(query, values)

    context = {
        "request": request,
        "category": {
            "category_name": category_name, 
            "category_id": category_id
            }
    }

    return templates.TemplateResponse("components/category_edited.html", context=context)

@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete category",
    response_class=HTMLResponse
)
def delete_category(category_id:int, current_user:ResponseUser = Depends(get_current_user)):
    user_id = current_user['user_id']
    values = (category_id, user_id)
    query = q.delete_category()
    DB.execute_query(query, values)

    return "<tr></tr>"

@router.get(
    path="/edit/{category_id}",
    include_in_schema=False,
    response_class=HTMLResponse
)
def edit_recall_project(category_id:int, request:Request, 
    current_user:ResponseUser = Depends(get_current_user)
    ):
    user_id = current_user['user_id']
    values = [user_id, category_id]
    df = q.get_categories(values, category_id)

    category = df.to_dict('records')[0]
    context = {
        "request": request,
        "category": category
    }
    
    return templates.TemplateResponse('components/edit_category.html', context=context)