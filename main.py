from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import ResponseUser
from routers import pomodoros, projects, recall_projects, recalls, users, categories
from utils import get_current_user

templates = Jinja2Templates(directory="templates")


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(pomodoros.router)
app.include_router(recall_projects.router)
app.include_router(recalls.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def home(request: Request, msg:str = None, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "msg":msg}
    )

@app.get('/pomodoro')
def pomodoro(request: Request, current_user:ResponseUser = Depends(get_current_user)):
    return templates.TemplateResponse(
        "general_pages/pomodoro.html", {'request': request}
    )

if __name__ == "__main__":
    import uvicorn

    if settings.ENV == 'PROD':
        uvicorn.run("main:app")
    elif settings.ENV == 'DEV':
        uvicorn.run("main:app", reload=True)