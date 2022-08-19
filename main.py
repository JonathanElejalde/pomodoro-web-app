import warnings 
warnings.filterwarnings(action= 'ignore')

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app_errors import not_authorized, not_found, server_error
from config import settings
from models import ResponseUser
from routers import pomodoros, projects, recall_projects, recalls, users, categories
from utils import get_current_user

templates = Jinja2Templates(directory="templates")


exception_handlers = {
    401: not_authorized,
    404: not_found,
    500: server_error,
}

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    exception_handlers=exception_handlers
)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(pomodoros.router)
app.include_router(recall_projects.router)
app.include_router(recalls.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, msg:str = None, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "msg":msg}
    )

@app.get('/pomodoro', response_class=HTMLResponse)
def pomodoro(request: Request, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse(
        "general_pages/pomodoro.html", {'request': request}
    )

@app.get("/not_found", response_class=HTMLResponse)
def not_found_page(request: Request):
    return templates.TemplateResponse("general_pages/not_found.html", {"request": request})

@app.get("/server_error", response_class=HTMLResponse)
def server_error_page(request: Request):
    return templates.TemplateResponse("general_pages/server_error.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    if settings.ENV == 'PROD':
        uvicorn.run("main:app")
    elif settings.ENV == 'DEV':
        print("Working on Dev")
        uvicorn.run("main:app", reload=True)
