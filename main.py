from fastapi import FastAPI
from fastapi import status

from models import User, Category, Project, Pomodoro, Recall

app = FastAPI()

# User paths

@app.post(
    path="/signup", 
    response_model= User,
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
    tags=['Users']
)
def signup():
    pass

@app.post(
    path="/login", 
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="User login",
    tags=['Users']
)
def login():
    pass

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Get user information",
    tags=['Users']
)
def get_user():
    pass

@app.delete(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="User deletion",
    tags=["Users"]
)
def delete_user():
    pass

@app.put(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="User update",
    tags=["Users"]
)
def update_user():
    pass

# Category paths

@app.post(
    path="/categories",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    summary="Category creation",
    tags=["Categories"]
)
def create_category():
    pass

@app.get(
    path="/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Get category",
    tags=["Categories"]
)
def get_category():
    pass

@app.get(
    path="/categories/{user_id}",
    response_model=list[Category],
    status_code=status.HTTP_200_OK,
    summary="Get categories",
    tags=["Categories"]
)
def get_categories():
    pass

@app.put(
    path="/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Update category",
    tags=["Categories"]
)
def update_category():
    pass

@app.delete(
    path="/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
    summary="Delete category",
    tags=["Categories"]
)
def delete_category():
    pass

@app.delete(
    path="/categories/{category_ids}",
    response_model=list[Category],
    status_code=status.HTTP_200_OK,
    summary="Delete categories",
    tags=["Categories"]
)
def delete_categories():
    pass


# Project paths

@app.post(
    path="/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Create project",
    tags=["Projects"]
)
def create_project():
    pass


@app.get(
    path="/projects/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Get project",
    tags=["Projects"]
)
def get_project():
    pass

@app.get(
    path="/projects/{project_ids}",
    response_model=list[Project],
    status_code=status.HTTP_200_OK,
    summary="Get projects",
    tags=["Projects"]
)
def get_projects():
    pass


@app.put(
    path="/projects/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Update project",
    tags=["Projects"]
)
def update_project():
    pass


@app.delete(
    path="/projects/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    summary="Delete project",
    tags=["Projects"]
)
def delete_project():
    pass

@app.delete(
    path="/projects/{project_ids}",
    response_model=list[Project],
    status_code=status.HTTP_200_OK,
    summary="Delete project",
    tags=["Projects"]
)
def delete_projects():
    pass


# Pomodoro paths
@app.post(
    path="/pomodoros",
    response_model=Pomodoro,
    status_code=status.HTTP_201_CREATED,
    summary="Create pomodoro",
    tags=["Pomodoros"]
)
def create_pomodoro():
    pass

@app.get(
    path="/pomodoros/{pomodoro_id}",
    response_model=Pomodoro,
    status_code=status.HTTP_200_OK,
    summary="Get pomodoro",
    tags=["Pomodoros"]
)
def get_pomodoro():
    pass

@app.get(
    path="/pomodoros/{pomodoro_ids}",
    response_model=list[Pomodoro],
    status_code=status.HTTP_200_OK,
    summary="Get pomodoros",
    tags=["Pomodoros"]
)
def get_pomodoros():
    pass

@app.get(
    path="/pomodoros/{pomodoro_ids}",
    response_model=list[Pomodoro],
    status_code=status.HTTP_200_OK,
    summary="Get pomodoros",
    tags=["Pomodoros"]
)
def get_pomodoros():
    pass


# Recall paths
@app.post(
    path="recalls",
    response_model=Recall,
    status_code=status.HTTP_201_CREATED,
    summary="Recall creation",
    tags=["Recalls"]
)
def create_recall():
    pass

@app.get(
    path="recalls/{recall_id}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Get recall",
    tags=["Recalls"]
)
def get_recall():
    pass

@app.get(
    path="recalls/{recall_ids}",
    response_model=list[Recall],
    status_code=status.HTTP_200_OK,
    summary="Get recalls",
    tags=["Recalls"]
)
def get_recalls():
    pass

@app.put(
    path="recalls/{recall_ids}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Update recalls",
    tags=["Recalls"]
)
def update_recalls():
    pass

@app.delete(
    path="recalls/{recall_id}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Delete recall",
    tags=["Recalls"]
)
def delete_recall():
    pass

@app.delete(
    path="recalls/{recall_ids}",
    response_model=Recall,
    status_code=status.HTTP_200_OK,
    summary="Delete recalls",
    tags=["Recalls"]
)
def delete_recalls():
    pass

